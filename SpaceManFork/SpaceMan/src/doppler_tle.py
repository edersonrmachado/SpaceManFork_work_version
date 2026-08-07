'''
Docstring for tle
'''

import os
import requests

TLE_DIRECTORY = "./TLE"


def getTLEUrl(sat_name):
    return f"https://celestrak.org/NORAD/elements/gp.php?NAME={sat_name}&FORMAT=TLE"


def downloadTLE(sat_name, overwrite=False):
    if not os.path.exists(f'{TLE_DIRECTORY}/{sat_name}.tle') or overwrite:

        print(f"Dowloading {sat_name} TLE...")

        # GET request
        response = requests.get(getTLEUrl(sat_name))

        # successful request
        if response.status_code == 200:
            # Check if the response actually contains TLE data
            if "No GP data found" in response.text:
                print("[ERROR] Satellite name not found in CelesTrak database.")
            else:
                # Save the TLE to a text file
                with open(f'TLE/{sat_name}.tle', 'w') as file:
                    file.write(response.text)
                print(f"TLE downloaded to {TLE_DIRECTORY}/{sat_name}.tle")
        else:
            print(f"[{{response.status_code}}] Failed to fetch data.")


if __name__ == '__main__':
    downloadTLE("STARLINK-1008") # if this file is directly executed without being imported 
