import json
import random
import math

import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as ctx

from matplotlib.ticker import FuncFormatter
from shapely.geometry import Point, Polygon
from pyproj import Geod, Transformer

from matplotlib.ticker import LinearLocator
from matplotlib.lines import Line2D


# set plot  fonts
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'


SAVE_PLOTS = True
# files 
ED_GEOMETRY = "config/ed_geometry.json"
OUTPUT_PDF = "../data/circle_map.pdf"
OUTPUT_EPS = "../data/circle_map.eps"
OUTPUT_PS = "../data/circle_map.ps"


# Desired map window
map_width_km =  500
map_height_km = 400




# plots - customized style
fig_facecolor='#FFFFFF'
dpi_set=700
fig_width=3.5
fig_height=2
fontsize_ticks=6
fontsize_text=5
fontsize_xy_labels=7
ed_marker=4
basemap_alpha=0.9
circle_linewidth=0.7
circle_color='gray'
ed_marker_color='mediumblue'
cross_marker_color='red'
cross_marker_size=18
cross_marker_linewidth=1
ed_label_distance_x=2.5
ed_label_distance_y=-2
grid_linewidth=0.6
grid_alpha=0.7
num_y_ticks=4
num_x_ticks=4
bondary_linewidth=0.5
tick_pad_x=1
legend_circle_marker_size=3
legend_cross_marker_size=4

# read geometry file
with open(ED_GEOMETRY, "r") as f:
    ed_geometry = json.load(f)

latitude = ed_geometry["central_point"]["lat"]
longitude = ed_geometry["central_point"]["lon"]

radius_km = ed_geometry["circle_radius_km"]

N = ed_geometry["number_of_eds"]
SEED = ed_geometry["distribution_seed"]

# generate random ED positions 
if SEED is not None:
    random.seed(SEED)


earth_radius_km = 6371.0

devices = []

for i in range(N):

    # Random angle
    theta = random.uniform(0, 2 * math.pi)

    # Uniform distribution inside circle
    distance = radius_km * math.sqrt(random.random())

    angular_distance = distance / earth_radius_km
    lat1 = math.radians(latitude)
    lon1 = math.radians(longitude)

    # Latitude
    lat2 = math.asin(
        math.sin(lat1) * math.cos(angular_distance)
        +
        math.cos(lat1)
        * math.sin(angular_distance)
        * math.cos(theta)
    )

    # Longitude
    lon2 = lon1 + math.atan2(
        math.sin(theta)
        * math.sin(angular_distance)
        * math.cos(lat1),
        math.cos(angular_distance)
        - math.sin(lat1) * math.sin(lat2)
    )

    point_lat = math.degrees(lat2)
    point_lon = math.degrees(lon2)

    devices.append({
        "devEui": f"e{i + 1:04d}",
        "lat": point_lat,
        "lon": point_lon
    })

# creates devices  GeodataFrame
gdf_devices = gpd.GeoDataFrame(
    devices,
    geometry=[
        Point(device["lon"], device["lat"])
        for device in devices
    ],
    crs="EPSG:4326"
)
# reference point GeodataFrame
gdf_center = gpd.GeoDataFrame(
    {
        "name": ["Center"]
    },
    geometry=[
        Point(longitude, latitude)
    ],
    crs="EPSG:4326"
)

#create geodesic circle

# WGS84 ellipsoid
geod = Geod(ellps="WGS84")

# Number of points used to represent the circle
num_points = 3000
circle_points = []

for i in range(num_points):

    azimuth = i * 360.0 / num_points

    lon_point, lat_point, _ = geod.fwd(
        longitude,
        latitude,
        azimuth,
        radius_km * 1000
    )

    circle_points.append(
        (lon_point, lat_point)
    )

# Close polygon
circle_points.append(circle_points[0])


# Create geodesic polygon in WGS84
circle_polygon = Polygon(circle_points)

gdf_circle = gpd.GeoDataFrame(
    {
        "radius_km": [radius_km]
    },
    geometry=[circle_polygon],
    crs="EPSG:4326"
)

# projection to Web Mercator (EPSG:3857) for plotting

gdf_devices_mercator = gdf_devices.to_crs(epsg=3857)
gdf_center_mercator = gdf_center.to_crs(epsg=3857)
gdf_circle_mercator = gdf_circle.to_crs(epsg=3857)


# figure properties




# fig
fig,ax=plt.subplots(figsize=(fig_width, fig_height),dpi=dpi_set,facecolor=fig_facecolor) 






#fig, ax = plt.subplots(
#    figsize=(10, 10)
#)

# region to show in plot

# Transform central point to Web Mercator
center_x = gdf_center_mercator.geometry.iloc[0].x
center_y = gdf_center_mercator.geometry.iloc[0].y


# Half dimensions
half_width_m = (map_width_km * 1000) / 2
half_height_m = (map_height_km * 1000) / 2

# Exact limits
ax.set_xlim(
    center_x - half_width_m,
    center_x + half_width_m
)

ax.set_ylim(
    center_y - half_height_m,
    center_y + half_height_m
)

# Keep the same scale in X and Y
ax.set_aspect("equal")


# ============================================================
# BASEMAP
# ============================================================
ctx.add_basemap(
    ax,
    source=ctx.providers.Esri.WorldStreetMap,
    zoom="auto",
    alpha=basemap_alpha,
    attribution=False
)

# ============================================================
# CIRCLE
# ============================================================

gdf_circle_mercator.boundary.plot(
    ax=ax,
    color=circle_color,
    linewidth=circle_linewidth,
    #linestyle="--",
    zorder=0
)

# ============================================================
# CENTRAL POINT
# ============================================================

gdf_center_mercator.plot(
    ax=ax,
    marker="+",
    color=cross_marker_color,
    markersize=cross_marker_size,
    linewidth=cross_marker_linewidth,
    linestyle="-",
    zorder=0
)


# ============================================================
# ED POINTS
# ============================================================

gdf_devices_mercator.plot(
    ax=ax,
    color=ed_marker_color,
    markersize=ed_marker,
    zorder=3
)


# ============================================================
# ED LABELS
# ============================================================

for i, row in gdf_devices_mercator.iterrows():

    x = row.geometry.x
    y = row.geometry.y

    ax.annotate(
        f"{i + 1:02d}",
        xy=(x, y),
        xytext=(ed_label_distance_x, ed_label_distance_y),
        textcoords="offset points",
        fontsize=fontsize_text,
        fontweight="normal",
        color="black",
        zorder=10
    )


# ============================================================
# CONVERT AXIS FROM EPSG:3857 TO LONGITUDE/LATITUDE
# ============================================================

transformer = Transformer.from_crs(
    "EPSG:3857",
    "EPSG:4326",
    always_xy=True
)


def format_longitude(x, pos):
    lon, _ = transformer.transform(x, 0)

    if lon > 0:
        #return f"{lon:.1f}°E"
        return f"{lon:.1f}"

    elif lon < 0:
        #return f"{abs(lon):.1f}°W"
        return f"{abs(lon):.1f}"
        
    else:
        #return "0°"
        return "0"


def format_latitude(y, pos):
    _, lat = transformer.transform(0, y)

    if lat > 0:
        #return f"{lat:.1f}°N"
        return f"{lat:.1f}"

    elif lat < 0:
        #return f"{abs(lat):.1f}°S"
        return f"{abs(lat):.1f}"
        
    else:
        #return "0°"
        return "0"


ax.xaxis.set_major_formatter(
    FuncFormatter(format_longitude)
)

ax.yaxis.set_major_formatter(
    FuncFormatter(format_latitude)
)


# ============================================================
# AXIS LABELS
# ============================================================

ax.set_xlabel(
    "Longitude (°E)",
    fontsize=fontsize_xy_labels
)

ax.set_ylabel(
    "Latitude (°N)",
    fontsize=fontsize_xy_labels
)


# ============================================================
# TITLE
# ============================================================

#ax.set_title(
#    f"ED Distribution — Radius = {radius_km} km",
#    fontsize=14,
#    fontweight="bold"
#)


# ============================================================
# GRID
# ============================================================

ax.grid(
    True,
    linestyle="--",
    linewidth=grid_linewidth,
    alpha=grid_alpha
)



# ============================================================
# SHOW AXES ON ALL FOUR SIDES
# ============================================================

ax.tick_params(
    axis="both",
    which="both",
    top=False,
    bottom=False,
    left=True,
    right=False,
    labeltop=False,
    labelbottom=True,
    labelleft=True,
    labelright=False
)


for spine in ax.spines.values():
    spine.set_linewidth(bondary_linewidth)

# Longitude labels on top and bottom
#ax.xaxis.set_ticks_position("both")

# Latitude labels on left and right
#ax.yaxis.set_ticks_position("both")

# ============================================================
# NORTH ARROW
# ============================================================

ax.annotate(
    "N",
    xy=(0.93, 0.92),
    xycoords="axes fraction",
    ha="center",
    va="center",
    fontsize=fontsize_xy_labels,
    fontweight="normal"
)

ax.annotate(
    "",
    xy=(0.93, 0.90),
    xytext=(0.93, 0.76),
    xycoords="axes fraction",
    arrowprops=dict(
        arrowstyle="->",
        linewidth=0.9,
        mutation_scale=8,
    )
)


ax.tick_params(
    axis="both",
    labelsize=fontsize_ticks
)

ax.tick_params(axis="y", length=0)
ax.tick_params(axis="x", which="major", pad=tick_pad_x)



# ============================================================
# LEGEND
# ============================================================



ax.xaxis.set_major_locator(LinearLocator(num_x_ticks))
ax.yaxis.set_major_locator(LinearLocator(num_y_ticks))



legend_elements = [
    Line2D(
        [0], [0],
        marker="o",
        color="none",
        markerfacecolor=ed_marker_color,
        markeredgecolor="none",
        markersize=legend_circle_marker_size,
        label="ED position"
    ),
    Line2D(
        [0], [0],
        marker="+",
        color=cross_marker_color,
        markersize=legend_cross_marker_size,
        markeredgewidth=1,
        linestyle="none",
        label="Ref. point"
    )
]

ax.legend(
    handles=legend_elements,
    loc="upper center",
    bbox_to_anchor=(0.47, 1.16),
    ncol=2,
    frameon=False,
    fontsize=fontsize_ticks,
    handletextpad=-0.38,
    columnspacing=1.2
)




# ============================================================
# LAYOUT
# ============================================================



plt.tight_layout()
if SAVE_PLOTS:
# ============================================================
# SAVE PDF
# ============================================================

    fig.savefig(
        OUTPUT_PDF,
        format="pdf",
        bbox_inches="tight"
    )


    # ============================================================
    # SAVE EPS
    # ============================================================

    fig.savefig(
        OUTPUT_EPS,
        format="eps",
        bbox_inches="tight"
    )


    # ============================================================
    # SAVE PS
    # ============================================================

    fig.savefig(
        OUTPUT_PS,
        format="ps",
        bbox_inches="tight"
    )


    # ============================================================
    # SHOW
    # ============================================================

#plt.show()


# ============================================================
# OUTPUT
# ============================================================

print()
print("============================================")
print("MAP GENERATED SUCCESSFULLY")
print("============================================")
print(f"PDF saved: {OUTPUT_PDF}")
print(f"EPS saved: {OUTPUT_EPS}")
print(f"PS saved:  {OUTPUT_PS}")
print(f"EDs generated: {N}")
print(f"Radius: {radius_km} km")
print(f"SEED: {SEED}")
print("Circle: exact geodesic radius on WGS84")
print("Axis: longitude/latitude in degrees")
print("============================================")