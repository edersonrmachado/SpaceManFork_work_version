import json
import random
import math
PRINT_MSG=False


def generate_endpoint_positions(endpoint_config_filename, output_filename):

    # read ed config file
    with open(endpoint_config_filename, "r") as f:
        ed_config = json.load(f)

    latitude = ed_config["ed_geometry"]["central_point"]["lat"]
    longitude = ed_config["ed_geometry"]["central_point"]["lon"]

    radius_km = ed_config["ed_geometry"]["circle_radius_km"]

    N = ed_config["number_of_eds"]
    SEED = ed_config["ed_geometry"]["distribution_seed"]

    # random seed if none
    if SEED is not None:
        random.seed(SEED)

    earth_radius_km = 6371.0


    # generate ed positions
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
            "lat": round(point_lat, 4),
            "lon": round(point_lon, 4)
        })


    # save devices position
    with open(output_filename, "w") as f:
        json.dump(devices, f, indent=4)

    # print summary
    if PRINT_MSG:
        print("ED positions generated successfully")
        print("###################################")
        print(f"Output file: {output_filename}")
        print(f"Number of EDs: {N}")
        print(f"Radius from ref point: {radius_km} km")
        print(f"SEED: {SEED}")
        print("###################################")
