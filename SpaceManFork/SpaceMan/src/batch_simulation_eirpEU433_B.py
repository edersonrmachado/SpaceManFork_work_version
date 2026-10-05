import json
import subprocess

from filelock import FileLock

import time


simulation_batch_start = time.perf_counter()
# print debug info
PRINT_SIMULATION_DEBUG = False
PRINT_LINK_MARGIN_DEBUG = False
PRINT_DOPPLER_DEBUG = False

# filenames
lora_config_filename = "config/lora_config.json"
link_margin_config_filename = "config/link_margin_config.json"
results_config_filename = "config/results_config.json"
simulation_config_filename = "config/simulation_config.json"
endpoint_config_filename = "config/endpoint_config.json"

results_file="../data/eirpEU433_12_30_gt0_t.csv"
simulation_batch_time_filename="../data/eirpEU433_simulation_time_t"
# regional parameters for EU433
freq = 433.375 # 

# location config 
lat = -3.5158  # lodja (CONGO)   
lon = 23.5801

#eirp_max = 12 # dBm
geometry_seed = None

# [dr, sf, bw, PHYPayload, ldro, tx_power_dbm]

configs = [
    [0, 12, 125, 59,  1, freq],
    [1, 11, 125, 59,  1, freq],
    [2, 10, 125, 59,  0, freq],
    [3, 9,  125, 123, 0, freq],
    [4, 8,  125, 240, 0, freq],
    [5, 7,  125, 240, 0, freq],
]


# load endpoint position config 
with open(endpoint_config_filename) as f:
    endpoint_config = json.load(f)
endpoint_config["ed_geometry"]["central_point"]["lat"] = lat
endpoint_config["ed_geometry"]["central_point"]["lon"] = lon
endpoint_config["ed_geometry"]["distribution_seed"] = geometry_seed
with open(endpoint_config_filename, "w") as f:
    json.dump(endpoint_config, f, indent=4)

# eirp calculation
with open(link_margin_config_filename, "r") as f:
        link_config = json.load(f)  
gt=link_config["iot_node"]["gt"]
lftx=link_config["iot_node"]["lftx"]
    

for eirp_max in range(18, 24):

    for dr, sf, bw, pkt_len, ldro, freq in configs:
        
        # tx power
        tx_power_dbm = (eirp_max-2*dr) - gt + lftx

        eirp = eirp_max-2*dr
        
        phy_len=pkt_len + 5
        
        print(f"\nSF = {sf} bw = {bw} EIRP = {eirp} dBm | TX = {tx_power_dbm} dBm PHYPayload = {phy_len} bytes LDRO = {ldro} Freq = {freq} MHz")
        
        # LoRa config
        with open(lora_config_filename) as f:
            lora_config = json.load(f)

        lora_config[0]["sf"] = sf   
        lora_config[0]["bw"] = bw
        lora_config[0]["pkt_len"] = phy_len
        lora_config[0]["frequency"] = freq
        lora_config[0]["ldro"] = ldro

        with open(lora_config_filename, "w") as f:
            json.dump(lora_config, f, indent=4)

        # Link margin config
        with open(link_margin_config_filename) as f:
            link_cfg = json.load(f)

        link_cfg["iot_node"]["pt_dbm"] = tx_power_dbm

        with open(link_margin_config_filename, "w") as f:
            json.dump(link_cfg, f, indent=4)

        # Mesmo reseirpults file para todas as simulações
        with open(results_config_filename) as f:
            results_config = json.load(f)

        results_config["results_file"] = results_file

        with open(results_config_filename, "w") as f:
            json.dump(results_config, f, indent=4)

        # Run simulation
        
        subprocess.run(["python", "simulator.py"], check=True)
simulation_batch_end = time.perf_counter()
simulation_batch_time=simulation_batch_end - simulation_batch_start

seconds = simulation_batch_time
minutes = simulation_batch_time / 60
hours = simulation_batch_time / 3600

with FileLock(simulation_batch_time_filename + ".lock"):
    with open(simulation_batch_time_filename, "w") as f:
        f.write(f"{results_file}\n")
        f.write(f"simulation time: {seconds:.2f} s\n")
        f.write(f"simulation time: {minutes:.2f} min\n")
        f.write(f"simulation time: {hours:.2f} h\n")