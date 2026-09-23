import json
import folium


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = "config/devices.json"
OUTPUT_MAP = "../data/devices_map.html"


# ============================================================
# LOAD DEVICES
# ============================================================

with open(INPUT_FILE, "r") as f:
    devices = json.load(f)


# ============================================================
# MAP CENTER
# ============================================================

center_lat = sum(d["lat"] for d in devices) / len(devices)
center_lon = sum(d["lon"] for d in devices) / len(devices)


# ============================================================
# CREATE MAP
# ============================================================

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=14
)


# ============================================================
# ADD BLACK FILLED POINTS + BOLD LABELS
# ============================================================

for dev in devices:

    lat = dev["lat"]
    lon = dev["lon"]
    name = dev["devEui"]


    # Black filled circle
    folium.CircleMarker(
        location=[lat, lon],
        radius=6,
        color="black",
        fill=True,
        fill_color="black",
        fill_opacity=1.0,
        weight=1
    ).add_to(m)


    # Bold device label
    folium.map.Marker(
        [lat, lon],
        icon=folium.DivIcon(
            icon_size=(100, 20),
            icon_anchor=(0, -12),
            html=f"""
            <div style="
                font-size:13px;
                font-weight:bold;
                color:black;
                white-space:nowrap;
                ">
                {name}
            </div>
            """
        )
    ).add_to(m)


# ============================================================
# SAVE MAP
# ============================================================

m.save(OUTPUT_MAP)

print("Map generated:", OUTPUT_MAP)
print("Devices plotted:", len(devices))