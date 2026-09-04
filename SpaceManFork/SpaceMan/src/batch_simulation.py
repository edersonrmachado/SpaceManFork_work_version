import json
import subprocess

bw=125
ldro_mode=0
#freqs=[433,868,915]
#pkt_lens=[35,50,100,200]
freqs=[433]
pkt_lens=[35,100,200]
pkt_per_endpoint=100
tx_power=1

for freq in freqs:
    
    for pkt_len in pkt_lens:
        
        save_results_to= f"../data/bw{bw}_ldro{ldro_mode}_f{freq}_plen{pkt_len}_pped{pkt_per_endpoint}_txp{tx_power}.csv"

        configs = [
            {"sf": sf,"bw": bw,"ldro": ldro_mode,"frequency": freq,"pkt_len": pkt_len,"tx_power": tx_power,"pkt_per_endpoint": pkt_per_endpoint,"results_file":save_results_to,
        }
            for sf in range(7, 13)
        ]


        for config in configs:
            with open("config/config.json", "w") as f:
                json.dump([config], f)
            subprocess.run(["python", "simulator.py"])