import json
import subprocess

lora_config_filename = "config/lora_config.json"
link_margin_config_filename = "config/link_margin_config.json"
results_config_filename="config/results_config.json"

# regional parameters for EU868
restults_file="../data/eu868_t2.csv"
freq=868.3
eirp_max = 30            # dBm
tx_power = eirp_max - 3  # dBm for our link
# [sf, bw, PHYPayload, ldro, tx_power]  (DR0 a DR5)
configs = [
    [12, 125, 64,  1, freq, tx_power],
    [11, 125, 64,  1, freq, tx_power],
    [10, 125, 64,  0, freq, tx_power],
    [9,  125, 128, 0, freq, tx_power],
    [8,  125, 128, 0, freq, tx_power],
    [7,  125, 128, 0, freq, tx_power],
]

# update config files with sf, bw, pkt_len, ldro and tx_power
    
for sf, bw, pkt_len, ldro, freq, tx_power in configs:
    
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
    link_cfg["tx_power"] = tx_power
    with open(link_margin_config_filename, "w") as f:
        json.dump(link_cfg, f, indent=4)
    
    # results file
    with open(results_config_filename) as f:
        results_config = json.load(f)
    results_config["results_file"] = restults_file
    with open(results_config_filename, "w") as f:
        json.dump(results_config, f, indent=4)
    
    # run simulation
    subprocess.run(["python", "simulator.py"], check=True)
#   subprocess.run(["python", "simulator.py"]) # rodar a simulação
