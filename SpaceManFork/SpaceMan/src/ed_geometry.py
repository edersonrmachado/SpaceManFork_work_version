import folium
import random
import math
import json


OUTPUT_MAP = "../data/circle_map.html"
OUTPUT_DEVICES = "config/devices.json"

ed_geometry_filename = "config/ed_geometry.json"


# =========================
# INPUTS
# =========================

with open(ed_geometry_filename, "r") as f:
    ed_geometry = json.load(f)


latitude = ed_geometry["central_point"]["lat"]
longitude = ed_geometry["central_point"]["lon"]
radius_km = ed_geometry["circle_radius_km"]

N = ed_geometry["number_of_eds"]

SEED = ed_geometry["distribution_seed"]

if SEED is not None:
    random.seed(SEED)


# =========================
# CREATE MAP
# =========================

m = folium.Map(
    location=[latitude, longitude],
    zoom_start=9
    #tiles="CartoDB Positron"
)

m.get_root().html.add_child(folium.Element("""
<style>
    .leaflet-tile-pane {
        filter: grayscale(50%);
    }
</style>
"""))




# =========================
# CIRCLE
# =========================

folium.Circle(
    location=[latitude, longitude],
    radius=radius_km * 1000,
    color="black",
    weight=1.5,
    fill=False,
    fill_opacity=0.2,
    popup=f"Radius: {radius_km} km"
).add_to(m)

folium.Marker(
    location=[latitude, longitude],
    icon=folium.DivIcon(
        html="""
        <div style="
            font-size: 13px;
            font-weight: normal;
            color: red;
            fill_opacity=0.7,
            transform: translate(-50%, -50%);
            
        ">✚</div>
        """
    )
).add_to(m)
# =========================
# RANDOM POINTS
# =========================

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

    # Calculate latitude
    lat2 = math.asin(
        math.sin(lat1) * math.cos(angular_distance)
        +
        math.cos(lat1)
        * math.sin(angular_distance)
        * math.cos(theta)
    )

    # Calculate longitude
    lon2 = lon1 + math.atan2(
        math.sin(theta)
        * math.sin(angular_distance)
        * math.cos(lat1),
        math.cos(angular_distance)
        - math.sin(lat1) * math.sin(lat2)
    )

    point_lat = math.degrees(lat2)
    point_lon = math.degrees(lon2)


    # =========================
    # SAVE DEVICE DATA
    # =========================

    devices.append({
        "devEui": f"e{i + 1:04d}",
        "lat": round(point_lat, 4),
        "lon": round(point_lon, 4)
    })


    

    # =========================
    # BLACK FILLED POINT
    # =========================

    folium.CircleMarker(
        location=[point_lat, point_lon],
        radius=4,
        color="black",
        fill=True,
        fill_color="black",
        fill_opacity=1.0,
        weight=3
    ).add_to(m)


    # =========================
    # BOLD LABEL
    # =========================

    folium.map.Marker(
        [point_lat, point_lon],
        icon=folium.DivIcon(
            icon_size=(100, 20),
            icon_anchor=(20, 22),
            html=f"""
            <div style="
                font-size:14px;
                font-weight:bold;
                color:black;
                white-space:nowrap;
            ">
                ED{i + 1:02d}
            </div>
            """
        )
    ).add_to(m)


# =========================
# SAVE DEVICES JSON
# =========================

with open(OUTPUT_DEVICES, "w") as f:
    json.dump(devices, f, indent=4)


# =========================
# SAVE MAP
# =========================

m.save(OUTPUT_MAP)


# =========================
# OUTPUT
# =========================

print(f"Map saved as {OUTPUT_MAP}")
print(f"Devices saved as {OUTPUT_DEVICES}")
print(f"Random EDs generated: {N}")
print(f"SEED: {SEED}")