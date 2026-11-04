import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


# ============================================================
# Configuration
# ============================================================

RADIUS_KM = 200

regions = {
    "EU868": {
        "lat": 48.8566,
        "lon": 2.3522,
        "label_pos": (7, 55),
    },

    "EU433": {
        "lat": -3.5158,
        "lon": 23.5801,
        "label_pos": (30, 3),
    },

    "AU915": {
        "lat": -15.7938,
        "lon": -47.8827,
        "label_pos": (-48, -5),
    },

    "CN470": {
        "lat": 29.5551,
        "lon": 106.3834,
        "label_pos": (106, 39),
    },
}


# ============================================================
# Function to create a geodesic circle
# with a real radius in kilometers
# ============================================================

def create_circle(lat_center, lon_center, radius_km):

    # Mean Earth radius in kilometers
    earth_radius_km = 6371.0

    # Number of points used to draw the circle
    angles = np.linspace(
        0,
        2 * np.pi,
        300
    )

    # Angular radius in radians
    angular_radius = radius_km / earth_radius_km

    # Convert center coordinates to radians
    lat_center_rad = np.radians(lat_center)
    lon_center_rad = np.radians(lon_center)

    # --------------------------------------------------------
    # Geodesic latitude
    # --------------------------------------------------------

    lat_circle = np.arcsin(
        np.sin(lat_center_rad) * np.cos(angular_radius)
        +
        np.cos(lat_center_rad)
        * np.sin(angular_radius)
        * np.cos(angles)
    )

    # --------------------------------------------------------
    # Geodesic longitude
    # --------------------------------------------------------

    lon_circle = (
        lon_center_rad
        +
        np.arctan2(
            np.sin(angles)
            * np.sin(angular_radius)
            * np.cos(lat_center_rad),

            np.cos(angular_radius)
            -
            np.sin(lat_center_rad)
            * np.sin(lat_circle)
        )
    )

    # Convert back to degrees
    lat_circle = np.degrees(lat_circle)
    lon_circle = np.degrees(lon_circle)

    # Keep longitude between -180 and +180
    lon_circle = (lon_circle + 180) % 360 - 180

    return lat_circle, lon_circle


# ============================================================
# Create global map
# ============================================================

fig = plt.figure(
    figsize=(14, 7)
)

ax = plt.axes(
    projection=ccrs.PlateCarree()
)

ax.set_global()


# ============================================================
# Map features
# ============================================================

ax.add_feature(
    cfeature.LAND,
    facecolor="lightgray"
)

ax.add_feature(
    cfeature.OCEAN,
    facecolor="white"
)

ax.add_feature(
    cfeature.COASTLINE,
    linewidth=0.7
)

ax.add_feature(
    cfeature.BORDERS,
    linewidth=0.4,
    linestyle=":"
)


# ============================================================
# Grid
# ============================================================

gl = ax.gridlines(
    draw_labels=True,
    linewidth=0.4,
    linestyle="--",
    alpha=0.5
)

gl.top_labels = False
gl.right_labels = False


# ============================================================
# Plot LoRaWAN regions
# ============================================================

for region_name, data in regions.items():

    lat = data["lat"]
    lon = data["lon"]

    label_lon, label_lat = data["label_pos"]

    # --------------------------------------------------------
    # Create 100 km radius circle
    # --------------------------------------------------------

    circle_lat, circle_lon = create_circle(
        lat,
        lon,
        RADIUS_KM
    )

    # --------------------------------------------------------
    # Blue filled circle
    # --------------------------------------------------------

    ax.fill(
        circle_lon,
        circle_lat,
        color="blue",
        alpha=0.20,
        transform=ccrs.PlateCarree(),
        zorder=3
    )

    # --------------------------------------------------------
    # Blue circle boundary
    # --------------------------------------------------------

    ax.plot(
        circle_lon,
        circle_lat,
        color="blue",
        linewidth=1.5,
        transform=ccrs.PlateCarree(),
        zorder=4
    )

    # --------------------------------------------------------
    # Central point
    # --------------------------------------------------------

    ax.scatter(
        lon,
        lat,
        s=35,
        color="blue",
        edgecolor="black",
        linewidth=0.7,
        transform=ccrs.PlateCarree(),
        zorder=5
    )

    # --------------------------------------------------------
    # Region label
    # --------------------------------------------------------

    ax.text(
        label_lon,
        label_lat,
        region_name,
        fontsize=11,
        fontweight="bold",
        ha="center",
        va="center",
        transform=ccrs.PlateCarree(),
        zorder=10,

        bbox=dict(
            boxstyle="round,pad=0.25",
            facecolor="white",
            edgecolor="none",
            alpha=0.9
        )
    )


# ============================================================
# Title
# ============================================================

plt.title(
    "LoRaWAN simulation regions",
    fontsize=14
)


# ============================================================
# Layout
# ============================================================

plt.tight_layout()


# ============================================================
# Save figure
# ============================================================

plt.savefig(
    "global_lorawan_regions.png",
    dpi=600,
    bbox_inches="tight"
)

plt.savefig(
    "global_lorawan_regions.pdf",
    bbox_inches="tight"
)


# ============================================================
# Show
# ============================================================

plt.show()

