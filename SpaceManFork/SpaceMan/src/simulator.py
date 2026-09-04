# simulator.py

from doppler_libsat import *
from doppler_classes import *
from doppler_utils import *
# link budget functions
from link_budget import *
import time

from datetime import datetime, timezone
import json

from skyfield.api import load

from entity import (
    Device,
    LoRaCFG,
    Position,
    Packet,
    Network,
    Satellite,
    Gateway
)

from LISTutils import (
    random_transmissions,
    generate_payloads,
    load_devices_from_json,
    check_collisions,
    fetch_tle_from_celestrak,
    filter_tles_by_name,
    calculate_lora_toa
)


import csv 


############################################################
# SIMULATION CONFIGURATION
############################################################

start = time.perf_counter()

link_config_filename = "config/link_config.json"

RANDOM_PAYLOAD=False

SIMULATION_START = datetime(
    2026, 6, 20,
    3, 20, 0,
    tzinfo=timezone.utc
)

SIMULATION_END = datetime(
    2026, 6, 22,
    4, 0, 0,
    tzinfo=timezone.utc
)

START_TS = SIMULATION_START.timestamp()
END_TS = SIMULATION_END.timestamp()

MIN_ELEVATION = 5

"""
SATELLITES = [
    "STARLINK-1017",
    "STARLINK-1012",
    "STARLINK-1042",
    "STARLINK-1048",
    "STARLINK-1068"
]
print(SATELLITES)
"""


def select_satellite_names():

    CONFIG_FILE = "config/sat_config.json"
    TLE_FILE = "tle_active.txt"

    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
    num_sats = config["num_sats"]
    with open(TLE_FILE, "r") as f:
        lines = f.readlines()
    satellite_names = []

    for line in lines:

        name = line.strip()

        if name.startswith("STARLINK-"):

            satellite_names.append(name)

            if len(satellite_names) >= num_sats:
                break

    if len(satellite_names) < num_sats:
        raise ValueError(
            f"Requested {num_sats} Starlinks, "
            f"but only {len(satellite_names)} were found in {TLE_FILE}."
        )            
    
    return satellite_names



SATELLITES=select_satellite_names()

# end additional code to store satellites list


############################################################
# REPORTING HELPERS
############################################################

def print_simulation_configuration():

    print("\n============================================================")
    print("                SIMULATION CONFIGURATION")
    print("============================================================")

    print(
        "Start GMT : "
        f"{SIMULATION_START.strftime('%Y-%m-%d %H:%M:%S')} GMT"
    )

    print(
        "End GMT   : "
        f"{SIMULATION_END.strftime('%Y-%m-%d %H:%M:%S')} GMT"
    )


def print_network_entities(network):

    print("\n============================================================")
    print("                    NETWORK ENTITIES")
    print("============================================================")

    print("\n=== Pre-Loaded Devices ===")


    for dev in network.devices.all_devices():

        print(
             f"--- > {dev.devEui}: "
            f"{dev.position}"
        )

    print("\n=== Gateways ===")

    for gw_id, gw in network.gateways.items():

        sat_name = (
            gw.satellite.id
            if gw.satellite
            else "None"
        )

        print(
            f"--- > {gw.gatewayId}: "
            f"{gw.position}, "
            f"linked to satellite {sat_name}"
        )

    print("\n=== Satellites ===")

    for sat_id, sat in network.satellites.items():

        gw_name = (
            sat.gateway.gatewayId
            if sat.gateway
            else "None"
        )

        print(
            f"--- > {sat.id}, "
            f"gateway: {gw_name}, "
            f"position: {sat.position}"
        )


def print_phy_summary(network):

    sfs = sorted(
        set(cfg.sf for _, _, cfg in network.transmissions)
    )

    bws = sorted(
        set(cfg.bw for _, _, cfg in network.transmissions)
    )

    freqs = sorted(
        set(cfg.frequency for _, _, cfg in network.transmissions)
    )

    print("\n--- > Active PHY Configurations (From Pre-loaded and Manual Configurations) ---")

    print(f"SFs         : {sfs}")

    print(f"BWs         : {bws}")

    print(f"Frequencies : {freqs}")


def print_collision_summary(
    generated_packets,
    collided,
    non_colliding
):

    print("\n============================================================")
    print("                 COLLISION ANALYSIS")
    print("============================================================")

    print(
        f"Generated transmissions : "
        f"{generated_packets}"
    )

    print(
        f"Collided transmissions  : "
        f"{len(collided)}"
    )

    print(
        f"Collision-free packets  : "
        f"{len(non_colliding)}"
    )

    initial_pdr = (
        len(non_colliding)
        /
        generated_packets
    ) * 100 if generated_packets else 0

    print(
        f"Initial PDR             : "
        f"{initial_pdr:.2f}%"
    )

## add file to config link variables 
def load_link_config(link_config_filename):
    with open(link_config_filename, "r") as f:
        link_config = json.load(f)

    return link_config

def apply_doppler_and_visibility(
    network,
    non_colliding,
    ts,
    min_elevation
):

    print("\n============================================================")
    print("             VISIBILITY + DOPPLER ANALYSIS")
    print("============================================================")

    visible_count = 0

    non_visible_count = 0

    doppler_failed = 0

    doppler_static_failed_count = 0
    
    doppler_rate_failed_count = 0
    
    doppler_static_and_rate_failed_count = 0
    
    successfully_received = 0
    
    visible_packet_count = 0
    
    doppler_exception_count=0

    ## add link margin registers

    link_margin_ok_count=0

    link_margin_failed_count=0

    link_config = load_link_config(link_config_filename)

    ## 

    for dev, pkt, cfg in non_colliding:

        tx_start = pkt.txTime

        toa = calculate_lora_toa(
            len(pkt.payload),
            cfg.sf,
            cfg.bw
        )

        tx_end = tx_start + toa

        visible_satellites = []

        packet_received = False

        for sat in network.satellites.values():

            if packet_received:
                break

            if sat.visible_during_transmission(
                dev.position,
                ts,
                tx_start,
                tx_end,
                min_elevation=min_elevation
            ):

                visible_satellites.append(
                    sat.id
                )

                lora_cfg = LoraConfig(
                    cfg.sf,
                    cfg.bw * 1E3,
                    cfg.frequency * 1E6,
                    len(pkt.payload)
                )

                ed_pos = GPSPosition(
                    dev.position.lat,
                    dev.position.lon
                )

                sat_name = sat.id

                tx_time = int(tx_start)

                tx_dt = datetime.fromtimestamp(
                    tx_time,
                    tz=timezone.utc
                )

                # link margin analysis before Doppler check                                      
                visible_packet_count += 1

                
                link_margin_1, link_margin_2, link_pass = compute_link_margin(
                    sat_name, 
                    lora_cfg, 
                    ed_pos, 
                    tx_time,
                    link_config
                )


                if link_pass == 0:
                    link_margin_failed_count += 1
                    continue

                link_margin_ok_count += 1
                    

                try:
                    
                    ## add ds_error dr_error to specify doppler error type    
                    
                    status, max_payload, ds_error,dr_error = checkComm(
                            sat_name,
                            lora_cfg,
                            ed_pos,
                            tx_time
                    )
                    
                    ####################################################
                    # PASSED
                    ####################################################

                    if status:
                            
                        successfully_received += 1

                        packet_received = True

                        #print(
                        #    f"✅ [PASSED] "
                        #    f"TX={tx_dt.strftime('%Y-%m-%d %H:%M:%S')} GMT "
                        #    f"Device={dev.devEui} "
                        #    f"SAT={sat_name} "
                        #    f"Payload={len(pkt.payload)}B "
                        #    f"MaxPayload={max_payload}B"
                        #)

                        if sat.gateway:

                            sat.gateway.receive(
                                dev,
                                pkt,
                                cfg
                            )

                    ####################################################
                    # FAILED
                    ####################################################

                    else:

                        doppler_failed += 1
                        if ds_error==1 and dr_error==0:
                            doppler_static_failed_count+=1
                        elif dr_error==1 and ds_error==0:
                            doppler_rate_failed_count+=1
                        elif dr_error==1 and ds_error==1:
                            doppler_static_and_rate_failed_count+=1
                        #print(
                        #    f"❌ [DOPPLER FAILED] " # add DOPPLER to specify error origin
                        #    f"TX={tx_dt.strftime('%Y-%m-%d %H:%M:%S')} GMT "
                        #    f"Device={dev.devEui} "
                        #    f"SAT={sat_name}"
                        #)

                except Exception as e:

                    doppler_failed += 1
                    doppler_exception_count+=1
                    

                    print(
                        f"⚠ [CHECKCOMM ERROR] "
                        f"Satellite={sat_name} "
                        f"Error={e}"
                    )

        ########################################################
        # Count visibility once per packet
        ########################################################

        if visible_satellites:

            visible_count += 1

        else:

            non_visible_count += 1

    ############################################################
    # Return statistics
    ############################################################

    #print(f"Total checkComm calls: {visible_packet_count}")
    
    return {
        "visible_count": visible_count,
        "non_visible_count": non_visible_count,
        "doppler_failed": doppler_failed,
        "successfully_received": successfully_received,
        
        "doppler_static_failed_count":doppler_static_failed_count,
        "doppler_rate_failed_count":doppler_rate_failed_count,
        "doppler_static_and_rate_count":doppler_static_and_rate_failed_count,
        "visible_packet_count":visible_packet_count,
        "doppler_exception_count":doppler_exception_count,
        "toa":toa,
        "link_margin_ok_count":link_margin_ok_count,
        "link_margin_failed_count":link_margin_failed_count
    }


def print_final_summary(
    network,
    generated_packets,
    collided,
    non_colliding,
    stats,
    lora_cfgs
):

    print("\n============================================================")
    print("                SIMULATION FINAL SUMMARY")
    print("============================================================")

    print("\n[CONFIGURATION]")

    print(
        f"Simulation Start GMT : "
        f"{SIMULATION_START.strftime('%Y-%m-%d %H:%M:%S')} GMT"
    )

    print(
        f"Simulation End GMT   : "
        f"{SIMULATION_END.strftime('%Y-%m-%d %H:%M:%S')} GMT"
    )

    print(
        f"Devices              : "
        f"{len(network.devices.all_devices())}"
    )

    print(
        f"Satellites           : "
        f"{len(network.satellites)}"
    )

    print(
        f"Gateways             : "
        f"{len(network.gateways)}"
    )

    print(
        f"LoRa Configurations  : "
        f"{len(lora_cfgs)}"
    )

    print("\n------------------------------------------------------------")
    print("[PACKET FLOW]")
    print("------------------------------------------------------------")

    print(
        f"Generated Packets        : "
        f"{generated_packets}"
    )

    collision_free_rate = (
        len(non_colliding)
        /
        generated_packets
    ) * 100 if generated_packets else 0

    print(
        f"Collision-Free           : "
        f"{len(non_colliding)} "
        f"({collision_free_rate:.2f}%)"
    )

    visibility_rate = (
        stats["visible_count"]
        /
        len(non_colliding)
    ) * 100 if len(non_colliding) else 0

    print(
        f"Visible                  : "
        f"{stats['visible_count']} "
        f"({visibility_rate:.2f}%)"
    )

    doppler_rate = (
        stats["successfully_received"]
        /
        stats["visible_count"]
    ) * 100 if stats["visible_count"] else 0

    print(
        f"Doppler Passed           : "
        f"{stats['successfully_received']} "
        f"({doppler_rate:.2f}%)"
    )

    final_pdr = (
        stats["successfully_received"]
        /
        generated_packets
    ) * 100 if generated_packets else 0

    print(
        f"Successfully Received    : "
        f"{stats['successfully_received']} "
        f"({final_pdr:.2f}%)"
    )

    print("\n------------------------------------------------------------")
    print("[PACKET FLOW 2]")
    print("------------------------------------------------------------")

    print(
        f"Generated Packets        : "
        f"{generated_packets}"
    )

    
    collision_rate = (
        len(collided)
        /
        generated_packets
    ) * 100 if generated_packets else 0

    print(
        f"Collided transmissions   : "
        f"{len(collided)} "
        f"({collision_rate:.2f}%)"
    )
    
    non_visibility_rate = (
        stats["non_visible_count"]
        /
        len(non_colliding)
    ) * 100 if len(non_colliding) else 0

    print(
        f"Non Visible transmission : "
        f"{stats['non_visible_count']} "
        f"({non_visibility_rate:.2f}%)"
    )
    
    
    print(
        f"Visible transmission     : "
        f"{stats['visible_count']} "
        f"({visibility_rate:.2f}%)" 
    )
    
    print(
        f"Vis. packets             : "
        f"{stats['visible_packet_count']} "
    )
    
    link_margin_pass_rate = (
        stats["link_margin_ok_count"]
        /
        stats["visible_packet_count"]
    ) * 100 if stats["visible_packet_count"] else 0

    print(
        f"Link margin passed       : "
        f"{stats['link_margin_ok_count']} "
        f"({link_margin_pass_rate:.2f}%)"
    )


    
    doppler_fail_rate = (
        stats["doppler_failed"]
        /
        stats["visible_packet_count"]
    ) * 100 if stats["visible_packet_count"] else 0

    doppler_static_fail_rate = (
        stats["doppler_static_failed_count"]
        /
        stats["visible_packet_count"]
    ) * 100 if stats["visible_packet_count"] else 0
    
    doppler_rate_fail_rate = (
        stats["doppler_rate_failed_count"]
        /
        stats["visible_packet_count"]
    ) * 100 if stats["visible_packet_count"] else 0

    
    print(
        f"Doppler Failed           : "
        f"{stats['doppler_failed']} "
        f"({doppler_fail_rate:.2f}%)"
    )

    print(
        f"Doppler static Failed    : "
        f"{stats['doppler_static_failed_count']} "
        f"({doppler_static_fail_rate:.2f}%)"
    )

    print(
        f"Doppler rate Failed      : "
        f"{stats['doppler_rate_failed_count']} "
        f"({doppler_rate_fail_rate:.2f}%)"
    )
    
    doppler_exception_rate = (
        stats["doppler_exception_count"]
        /
        stats["visible_packet_count"]
    ) * 100 if stats["visible_packet_count"] else 0

    print(
        f"Doppler exception        : "
        f"{stats['doppler_exception_count']} "
        f"({doppler_exception_rate:.2f}%)"
    )
    
    
    final_pdr = (
        stats["successfully_received"]
        /
        generated_packets
    ) * 100 if generated_packets else 0

    print(
        f"Successfully Rec. packets: "
        f"{stats['successfully_received']} "
        f"({final_pdr:.2f}%)"
    )
    
        
    if (stats['successfully_received']-(stats['visible_packet_count']-stats['visible_count']))>0:
        successfully_tx_received=stats['successfully_received']-(stats['visible_packet_count']-stats['visible_count'])
    else:
        successfully_tx_received=stats['successfully_received']
            
    
    final_pdr_transmissions = (
        successfully_tx_received
        /
        generated_packets
    ) * 100 if generated_packets else 0


    print(
        f"Successfully transmiss.  : "
        f"{successfully_tx_received} "
        f"({final_pdr_transmissions:.2f}%)"
    )
    
    pkt_energy=stats['toa']*tx_power
    total_energy=stats['toa']*tx_power*generated_packets
    successfully_energy_transm=successfully_tx_received*pkt_energy
    failed_energy_collided=len(collided)*pkt_energy
    failed_energy_visibility=stats['non_visible_count']*pkt_energy
    failed_energy_doppler=stats['doppler_failed']*pkt_energy
    link_margin_energy_pass=stats['link_margin_ok_count']*pkt_energy
    failed_energy_link_margin=stats['link_margin_failed_count']*pkt_energy
    bytes_per_joule=(pkt_len*successfully_tx_received)/total_energy if total_energy>0 else 0



    num_sats=len(SATELLITES)
    
    with open("config/devices.json", "r") as f:
        devs = json.load(f)
        num_eds = len(devs)
    
    with open(data_filename, "a", newline="") as csv_file:
        writer = csv.writer(csv_file)

       
        if csv_file.tell() == 0:
            writer.writerow([
                "sf","bw","ldro","freqMHz","pkt_len","pkt_toa",
                "tx_power","pkt_energy","total_pkt","total_energy",
                "collided","non_visible","doppler_error","ds_error",
                "dr_error","doppler_except_count","succes_rec_pkt","succes_rec_tx",
                "final_pdr","succes_energy_trans","failed_energy_col","failed_energy_vis",
                "failed_energy_dop","num_sats","num_devs","link_margin_energy_pass",
                "failed_energy_link_margin","bytes_per_joule"
            ])
        
        writer.writerow([f"{lora_cfgs[0].sf}", 
                         f"{lora_cfgs[0].bw}",
                         f"{ldro}", 
                         f"{lora_cfgs[0].frequency}",
                         f"{len(payloads[0])}",
                         f"{stats['toa']:.6f}",
                         f"{tx_power}", 
                         f"{pkt_energy:.6f}",
                         f"{generated_packets}",
                         f"{total_energy:.6f}",
                         f"{len(collided)}",
                         f"{stats['non_visible_count']}",
                         f"{stats['doppler_failed']}",
                         f"{stats['doppler_static_failed_count']}",
                         f"{stats['doppler_rate_failed_count']}",
                         f"{stats['doppler_exception_count']}",
                         f"{stats['successfully_received']}",
                         f"{successfully_tx_received}",
                         f"{final_pdr:.2f}",
                         f"{successfully_energy_transm:.6f}",
                         f"{failed_energy_collided:.6f}",
                         f"{failed_energy_visibility:.6f}",
                         f"{failed_energy_doppler:.6f}",
                         f"{num_sats}",
                         f"{num_eds}",
                         f"{link_margin_energy_pass:.6f}",
                         f"{failed_energy_link_margin:.6f}",
                         f"{bytes_per_joule:.2f}"
                         ])
       
def print_gateway_statistics(network):

    print("\n------------------------------------------------------------")
    print("[GATEWAY STATISTICS]")
    print("------------------------------------------------------------")

    for gw_id, gw in network.gateways.items():

        sat_name = (
            gw.satellite.id
            if gw.satellite
            else "None"
        )

        print(f"\n{gw_id}")

        print(
            f"  Satellite             : "
            f"{sat_name}"
        )

        print(
            f"  Received Packets      : "
            f"{len(gw.buffer)}"
        )

        if gw.buffer:

            device_stats = {}

            for dev, pkt, cfg in gw.buffer:

                if dev.devEui not in device_stats:

                    device_stats[dev.devEui] = 0

                device_stats[dev.devEui] += 1

            print("\n  Devices:")

            for dev_id, count in device_stats.items():

                print(
                    f"    - {dev_id:<20}: "
                    f"{count} packets"
                )


############################################################
# CREATE NETWORK
############################################################

print_simulation_configuration()

print("\n--- Defining the network ---")

network = Network()

print("--- > Network created ---")

############################################################
# DEVICES
############################################################

print("\n--- Defining Devices ---")

load_devices_from_json(
    network,
    "config/devices.json"
)

print("--- > Devices added to the network ---")

############################################################
# SATELLITES + GATEWAYS
############################################################

print("\n--- Defining Satellites and Gateways---")

ts = load.timescale()

tle_data = fetch_tle_from_celestrak(
    group="active"
)

selected_tles = filter_tles_by_name(
    tle_data,
    SATELLITES
    
)

print(
    "--- > Selected satellites "
    "and adding gateways ---"
)

for name, line1, line2 in selected_tles:

    sat = Satellite(
        name,
        line1,
        line2
    )


    sat.update_position(
        ts,
        START_TS
    )

    network.add_satellite(sat)

    print(
        f"--- >> Gateway created: GW_{name}"
    )

    gw = Gateway(
        f"GW_{name}",
        satellite=sat
    )

    network.add_gateway(gw)

############################################################
# REPORT NETWORK
############################################################

print_network_entities(network)

############################################################
# RANDOM TRAFFIC
############################################################

print("\n============================================================")
print("                TRANSMISSION GENERATION")
print("============================================================")

#print("\n--- > Generating random payloads ---")

#payloads = generate_payloads(
#    35,
#    35,
    #51,
#    save_to="config/random_payloads.json"
#)

print(
    "--- > Loading LoRa configurations ---"
)

with open("config/config.json", "r") as f:

    lora_data = json.load(f)

lora_cfgs = [
    LoRaCFG(
        cfg["sf"],
        cfg["bw"],
        cfg["frequency"]
    )
    for cfg in lora_data
]

for cfg in lora_data:
    ldro = cfg["ldro"]
    pkt_len = cfg["pkt_len"]
    tx_power = cfg["tx_power"]
    pkt_per_endpoint=cfg["pkt_per_endpoint"]
    data_filename=cfg["results_file"]


print("\n--- > Generating random payloads ---")

payloads = generate_payloads(
    pkt_len,
    pkt_len,
    #51,
    save_to="config/random_payloads.json"
)





print(
    "--- > Planning random transmissions ---"
)

random_transmissions(
    network,
    payloads,
    lora_cfgs,
    t_start=START_TS,
    t_end=END_TS,
    n_packets=pkt_per_endpoint,
    seed=12345
)

############################################################
# MANUAL TRANSMISSIONS
############################################################
'''
print(
    "--- > Planning manual transmissions (To use for Scheduling Techniques)---"
)

cfg1 = LoRaCFG(
    sf=8,
    bw=125,
    frequency=433.1
)

new_dev = Device(
    "e9999",
    Position(
        lat=49.620,
        lon=6.140
    ),
    network=network
)

network.devices.add_device(new_dev)

network.devices.get_device(
    "e9999"
).transmit(
    Packet(
        b"Hello",
        START_TS + 120
    ),
    cfg1
)
'''
############################################################
# PHY SUMMARY
############################################################

print_phy_summary(network)

############################################################
# COLLISION ANALYSIS
############################################################

print(
    " \n--- > Checking Collision ---"
)

collided, non_colliding = check_collisions(
    network
)

generated_packets = len(
    network.transmissions
)

print_collision_summary(
    generated_packets,
    collided,
    non_colliding
)

############################################################
# VISIBILITY + DOPPLER
############################################################

stats = apply_doppler_and_visibility(
    network,
    non_colliding,

    ts,
    MIN_ELEVATION
)

############################################################
# FINAL REPORTS
############################################################

print_final_summary(
    network,
    generated_packets,
    collided,
    non_colliding,
    stats,
    lora_cfgs
)

#print_gateway_statistics(network)

print("\n============================================================")
print("                 END OF SIMULATION")
print("============================================================")


end = time.perf_counter()

print(end - start)