import json
import subprocess

# print debug info
PRINT_SIMULATION_DEBUG=False
PRINT_LINK_MARGIN_DEBUG=False
PRINT_DOPPLER_DEBUG=False

# filenames
lora_config_filename = "config/lora_config.json"
link_margin_config_filename = "config/link_margin_config.json"
results_config_filename="config/results_config.json"
simulation_config_filename="config/simulation_config.json"

# regional parameters for EU868
results_file="../data/eu868_second_eirp16.csv"
freq=868.3
eirp_max = 16 # dBm
tx_power_dbm = eirp_max - 3  # dBm for our link

# [sf, bw, PHYPayload, ldro, tx_power_dbm]  (DR0 a DR5)
configs = [
    [12, 125, 64,  1, freq, tx_power_dbm],
    [11, 125, 64,  1, freq, tx_power_dbm],
    [10, 125, 64,  0, freq, tx_power_dbm],
    [9,  125, 128, 0, freq, tx_power_dbm],
    [8,  125, 128, 0, freq, tx_power_dbm],
    [7,  125, 128, 0, freq, tx_power_dbm],
]

# enable/disable PRINT DEBUG options
with open(simulation_config_filename,'r') as f:
    simulation_config = json.load(f)

simulation_config["print_simulation_debug"]=PRINT_SIMULATION_DEBUG
simulation_config["print_link_margin_debug"]=PRINT_LINK_MARGIN_DEBUG
simulation_config["print_doppler_debug"]=PRINT_DOPPLER_DEBUG

with open(simulation_config_filename, "w") as f:
    json.dump(simulation_config, f, indent=4)

# update config files with sf, bw, pkt_len, ldro and tx_power_dbm    
for sf, bw, pkt_len, ldro, freq, tx_power_dbm in configs:
    
    # lora config    
    with open(lora_config_filename) as f:
        lora_config = json.load(f)
    lora_config[0]["sf"] = sf
    lora_config[0]["bw"] = bw
    lora_config[0]["pkt_len"] = pkt_len
    lora_config[0]["frequency"] = freq
    lora_config[0]["ldro"] = ldro
    with open(lora_config_filename, "w") as f:
        json.dump(lora_config, f, indent=4)

    # link margin config
    with open(link_margin_config_filename) as f:
        link_cfg = json.load(f)
    link_cfg['iot_node']["pt_dbm"] = tx_power_dbm
    print(tx_power_dbm)
    with open(link_margin_config_filename, "w") as f:
        json.dump(link_cfg, f, indent=4)
    
    # results file
    with open(results_config_filename) as f:
        results_config = json.load(f)
    results_config["results_file"] = results_file
    
    with open(results_config_filename, "w") as f:
        json.dump(results_config, f, indent=4)
    
    # run simulation
    subprocess.run(["python", "simulator.py"], check=True)

