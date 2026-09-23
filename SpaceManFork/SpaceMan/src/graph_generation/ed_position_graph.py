import json
import math

import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as ctx

from matplotlib.ticker import FuncFormatter
from shapely.geometry import Point, Polygon
from pyproj import Geod, Transformer

from matplotlib.ticker import LinearLocator
from matplotlib.lines import Line2D


# ============================================================
# PLOT FONTS
# ============================================================

plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'


# ============================================================
# SETTINGS
# ============================================================

SAVE_PLOTS = True

endpoint_config_filename = "../config/endpoint_config.json"

INPUT_DEVICES = "../config/endpoint_positions/devices.json"

OUTPUT_PDF = "../../figures/circle_map.pdf"
OUTPUT_EPS = "../../figures/circle_map.eps"
OUTPUT_PS = "../../figures/circle_map.ps"


# Desired map window
map_width_km = 500
map_height_km = 400


# ============================================================
# PLOT STYLE
# ============================================================

fig_facecolor = '#FFFFFF'
dpi_set = 700

fig_width = 3.5
fig_height = 2

fontsize_ticks = 6
fontsize_text = 5
fontsize_xy_labels = 7

ed_marker = 4
basemap_alpha = 0.9

circle_linewidth = 0.7
circle_color = 'gray'

ed_marker_color = 'mediumblue'

cross_marker_color = 'red'
cross_marker_size = 18
cross_marker_linewidth = 1

ed_label_distance_x = 2.5
ed_label_distance_y = -2

grid_linewidth = 0.6
grid_alpha = 0.7

num_y_ticks = 4
num_x_ticks = 4

bondary_linewidth = 0.5
tick_pad_x = 1

legend_circle_marker_size = 3
legend_cross_marker_size = 4


# ============================================================
# READ GEOMETRY CONFIGURATION
# ============================================================

# read ed config file
with open(endpoint_config_filename, "r") as f:
    ed_config = json.load(f)

latitude = ed_config["ed_geometry"]["central_point"]["lat"]
longitude = ed_config["ed_geometry"]["central_point"]["lon"]

radius_km = ed_config["ed_geometry"]["circle_radius_km"]



# ============================================================
# READ ED POSITIONS
# ============================================================

with open(INPUT_DEVICES, "r") as f:
    devices = json.load(f)


N = len(devices)


# ============================================================
# CREATE DEVICES GEODATAFRAME
# ============================================================

gdf_devices = gpd.GeoDataFrame(
    devices,
    geometry=[
        Point(device["lon"], device["lat"])
        for device in devices
    ],
    crs="EPSG:4326"
)


# ============================================================
# REFERENCE POINT
# ============================================================

gdf_center = gpd.GeoDataFrame(
    {
        "name": ["Center"]
    },
    geometry=[
        Point(longitude, latitude)
    ],
    crs="EPSG:4326"
)


# ============================================================
# CREATE GEODESIC CIRCLE
# ============================================================

geod = Geod(ellps="WGS84")

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


circle_points.append(circle_points[0])


circle_polygon = Polygon(circle_points)


gdf_circle = gpd.GeoDataFrame(
    {
        "radius_km": [radius_km]
    },
    geometry=[circle_polygon],
    crs="EPSG:4326"
)


# ============================================================
# PROJECT TO WEB MERCATOR
# ============================================================

gdf_devices_mercator = gdf_devices.to_crs(epsg=3857)
gdf_center_mercator = gdf_center.to_crs(epsg=3857)
gdf_circle_mercator = gdf_circle.to_crs(epsg=3857)


# ============================================================
# FIGURE
# ============================================================

fig, ax = plt.subplots(
    figsize=(fig_width, fig_height),
    dpi=dpi_set,
    facecolor=fig_facecolor
)


# ============================================================
# MAP WINDOW
# ============================================================

center_x = gdf_center_mercator.geometry.iloc[0].x
center_y = gdf_center_mercator.geometry.iloc[0].y

half_width_m = (map_width_km * 1000) / 2
half_height_m = (map_height_km * 1000) / 2


ax.set_xlim(
    center_x - half_width_m,
    center_x + half_width_m
)

ax.set_ylim(
    center_y - half_height_m,
    center_y + half_height_m
)

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
        xytext=(
            ed_label_distance_x,
            ed_label_distance_y
        ),
        textcoords="offset points",
        fontsize=fontsize_text,
        fontweight="normal",
        color="black",
        zorder=10
    )


# ============================================================
# CONVERT AXIS TO LONGITUDE / LATITUDE
# ============================================================

transformer = Transformer.from_crs(
    "EPSG:3857",
    "EPSG:4326",
    always_xy=True
)


def format_longitude(x, pos):

    lon, _ = transformer.transform(x, 0)

    if lon > 0:
        return f"{lon:.1f}"

    elif lon < 0:
        return f"{abs(lon):.1f}"

    else:
        return "0"


def format_latitude(y, pos):

    _, lat = transformer.transform(0, y)

    if lat > 0:
        return f"{lat:.1f}"

    elif lat < 0:
        return f"{abs(lat):.1f}"

    else:
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
# GRID
# ============================================================

ax.grid(
    True,
    linestyle="--",
    linewidth=grid_linewidth,
    alpha=grid_alpha
)


# ============================================================
# TICKS
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


ax.tick_params(
    axis="both",
    labelsize=fontsize_ticks
)

ax.tick_params(
    axis="y",
    length=0
)

ax.tick_params(
    axis="x",
    which="major",
    pad=tick_pad_x
)


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


# ============================================================
# LEGEND
# ============================================================

ax.xaxis.set_major_locator(
    LinearLocator(num_x_ticks)
)

ax.yaxis.set_major_locator(
    LinearLocator(num_y_ticks)
)


legend_elements = [

    Line2D(
        [0],
        [0],
        marker="o",
        color="none",
        markerfacecolor=ed_marker_color,
        markeredgecolor="none",
        markersize=legend_circle_marker_size,
        label="ED position"
    ),

    Line2D(
        [0],
        [0],
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


# ============================================================
# SAVE
# ============================================================

if SAVE_PLOTS:

    fig.savefig(
        OUTPUT_PDF,
        format="pdf",
        bbox_inches="tight"
    )

    fig.savefig(
        OUTPUT_EPS,
        format="eps",
        bbox_inches="tight"
    )

    fig.savefig(
        OUTPUT_PS,
        format="ps",
        bbox_inches="tight"
    )


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
print(f"EDs plotted: {N}")
print(f"Radius: {radius_km} km")
print("Circle: exact geodesic radius on WGS84")
print("Axis: longitude/latitude in degrees")
print("============================================")