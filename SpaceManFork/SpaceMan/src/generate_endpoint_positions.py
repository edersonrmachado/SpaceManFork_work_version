import json
import random
import math

from filelock import FileLock


PRINT_ENDPOINT_DEBUG = False

def generate_endpoint_positions(endpoint_config, simulation_config):
    """Generate endpoint positions based on config, store their position in output file"""
    
    
    latitude = endpoint_config.geometry.central_point.lat
    longitude = endpoint_config.geometry.central_point.lon
  
    radius_km = endpoint_config.geometry.circle_radius_km
    
    N=endpoint_config.number_of_eds
    
    SEED = endpoint_config.geometry.distribution_seed

    # random seed if none
    if SEED is not None:
        random.seed(SEED)
    else:
        random.seed(None)

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
    with FileLock(simulation_config.devices_filename + ".lock"):
        with open(simulation_config.devices_filename, "w") as f:
            json.dump(devices, f, indent=4)

    # print summary
    if PRINT_ENDPOINT_DEBUG:
        print("ED positions generated successfully")
        print("###################################")
        print(f"Output file: {simulation_config.devices_filename}")
        print(f"Number of EDs: {N}")
        print(f"Radius from ref point: {radius_km} km")
        print(f"SEED: {SEED}")
        print("###################################")
