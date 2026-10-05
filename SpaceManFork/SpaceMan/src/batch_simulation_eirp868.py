import json
import subprocess

# print debug info
PRINT_SIMULATION_DEBUG = False
PRINT_LINK_MARGIN_DEBUG = False
PRINT_DOPPLER_DEBUG = False

# filenames
lora_config_filename = "config/lora_config.json"
link_margin_config_filename = "config/link_margin_config.json"
results_config_filename = "config/results_config.json"
simulation_config_filename = "config/simulation_config.json"

#results_file="../data/eu868_second_eirp16_30_gt0.csv"
results_file="../data/_eirp16_30_gt0.csv"

# regional parameters for EU868
freq = 868.3

# [sf, bw, PHYPayload, ldro, tx_power_dbm]
configs = [
    [12, 125, 64,  1, freq],
    [11, 125, 64,  1, freq],
    [10, 125, 64,  0, freq],
    [9,  125, 128, 0, freq],
    [8,  125, 235, 0, freq],
    [7,  125, 235, 0, freq],
]

 # eirp calculation
with open(link_margin_config_filename, "r") as f:
        link_config = json.load(f)  
gt=link_config["iot_node"]["gt"]
lftx=link_config["iot_node"]["lftx"]
    
print(gt,lftx)


for eirp in range(16, 31):

    tx_power_dbm = eirp - gt + lftx
    
    print(f"\nEIRP = {eirp} dBm | TX = {tx_power_dbm} dBm")

    for sf, bw, pkt_len, ldro, freq in configs:

        # LoRa config
        with open(lora_config_filename) as f:
            lora_config = json.load(f)

        lora_config[0]["sf"] = sf   
        lora_config[0]["bw"] = bw
        lora_config[0]["pkt_len"] = pkt_len
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

        # Mesmo results file para todas as simulações
        with open(results_config_filename) as f:
            results_config = json.load(f)

        results_config["results_file"] = results_file

        with open(results_config_filename, "w") as f:
            json.dump(results_config, f, indent=4)

        # Run simulation
        subprocess.run(["python", "simulator.py"], check=True)