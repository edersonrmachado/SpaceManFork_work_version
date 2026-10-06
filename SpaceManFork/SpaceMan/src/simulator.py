# simulator.py

from filelock import FileLock
from config_classes import * 
from doppler_libsat import *
from doppler_classes import *
from doppler_utils import *
from link_budget import *
from generate_endpoint_positions import *
from parser_args import *
from datetime import datetime, timezone
from skyfield.api import load
import json
import csv 
import time

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

# start simulation time counter

simulation_start = time.perf_counter()

############################################################
# SIMULATION CONFIGURATION
############################################################

# Load general configuration (from class file) 
config = Config(
    simulation=SimulationConfig(),
    satellite=SatelliteConfig(),
    endpoint=EndpointConfig(
        geometry=EDGeometryConfig(
            central_point=CentralPointConfig()
        )
    ),
    lora=LoRaConfig(),
    link_margin=LinkMarginConfig(
        iot_node=IoTNodeConfig(),
        propagation_losses=PropagationLossesConfig(),
        satellite_receiver=SatelliteReceiverConfig()
    ),
    doppler=DopplerConfig()
)

print(config.lora.sf)

## Replace config for arguments if provided
args = parse_arguments()
apply_overrides(config, args)

print(config.lora.sf)
#quit()

# files 
tle_filename=config.satellite.tle_filename
devices_filename=config.simulation.devices_filename
payload_generated_filename=config.simulation.payload_generated_filename

# simulation, satellite, endpoint, link and doppler config
simulation_config=config.simulation
satellite_config = config.satellite 
endpoint_config = config.endpoint
link_config = config.link_margin
doppler_config = config.doppler

#derivative_npoints=config.doppler.derivative_num_of_points
#derivative_step_sec=config.doppler.derivative_step_sec

# simulation times 
PRINT_SIMULATION_DEBUG=simulation_config.print_simulation_debug

SIMULATION_START = datetime(
    simulation_config.simulation_start_year,
    simulation_config.simulation_start_month,
    simulation_config.simulation_start_day,
    simulation_config.simulation_start_hour,
    simulation_config.simulation_start_minute,
    simulation_config.simulation_start_second,
    tzinfo=timezone.utc
)

SIMULATION_END = datetime(
    simulation_config.simulation_end_year,
    simulation_config.simulation_end_month,
    simulation_config.simulation_end_day,
    simulation_config.simulation_end_hour,
    simulation_config.simulation_end_minute,
    simulation_config.simulation_end_second,     
    tzinfo=timezone.utc
)   

START_TS = SIMULATION_START.timestamp()
END_TS = SIMULATION_END.timestamp()
evaluation_time = END_TS-START_TS

# elevation angle
MIN_ELEVATION = satellite_config.min_elevation_angle

# generate Eds position
generate_endpoint_positions(endpoint_config, simulation_config)

# find satellites TLEs locally/network
def select_satellite_names(satellite_config):

    num_sats = satellite_config.num_sats
    
    # read tle file
    with open(tle_filename, "r") as f:
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
            f"but only {len(satellite_names)} were found in {tle_filename}."
        )            
    return satellite_names

SATELLITES=select_satellite_names(config.satellite)


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

    if PRINT_SIMULATION_DEBUG:
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
        if PRINT_SIMULATION_DEBUG:
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
        if PRINT_SIMULATION_DEBUG:
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
    print(network.transmissions[0][2])
    
    #for i in range(len(network.transmissions)):
        
        #print(network.transmissions[i][2])
    
    
    
    print("\n--- > Active PHY Configurations (From Pre-loaded and Manual Configurations) ---")

    print(f"SFs         : {sfs}")

    print(f"BWs         : {bws}")

    print(f"Frequencies : {freqs}")
    
    match network.transmissions[0][2].ldro:

        case 0:
            print(f"LDRO        : [OFF]")
        case 1:
            print(f"LDRO        : [ON]")
        case 2: 
            print(f"LDRO        : [AUTO]")


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

def apply_doppler_and_visibility(
    network,
    non_colliding,
    ts,
    min_elevation,
    doppler_config,
    link_config
    ):

    print("\n============================================================")
    print("             VISIBILITY + LINK MARGIN + DOPPLER ANALYSIS      ")
    print("============================================================")

    # visibility registers 

    visible_count = 0

    non_visible_count = 0

    # doppler registers 

    doppler_failed = 0

    doppler_static_failed_count = 0
    
    doppler_rate_failed_count = 0
    
    doppler_static_and_rate_failed_count = 0
    
    successfully_received = 0
    
    visible_packet_count = 0
    
    doppler_exception_count=0

    ## link margin registers

    link_margin_ok_count=0

    link_margin_failed_count=0

    repeated_link_margin_tx_count = 0

    pkt_tx_anterior = 0
    
    visible_sat_height=[]

    
    for dev, pkt, cfg in non_colliding:

        tx_start = pkt.txTime
        
        toa = calculate_lora_toa(
            len(pkt.payload),
            cfg.sf,
            cfg.bw,
            de=cfg.ldro
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

                lora_cfg = LoRaConfig(
                    sf=config.lora.sf,
                    bw=config.lora.bw * 1E3,
                    frequency=config.lora.frequency * 1E6,
                    payload_len=len(pkt.payload),
                    ldro=config.lora.ldro,
                )
                
                ed_pos = GPSPosition(
                    dev.position.lat,
                    dev.position.lon
                )

                sat_name = sat.id

                #tx_time = int(tx_start) # important it was not commented before
                tx_time = tx_start # added

                tx_dt = datetime.fromtimestamp(
                    tx_time,
                    tz=timezone.utc
                )

                # link margin analysis before Doppler check                                      
                visible_packet_count += 1
                
                visible_sat_height.append(sat_height(sat_name,tx_time))
                
                link_margin_1, link_margin_2, link_pass = compute_link_margin(
                    sat_name, 
                    lora_cfg, 
                    ed_pos, 
                    tx_time,
                    link_config
                )

                #  count link pass transmission if it was not count before    
                if link_pass == 0:
                    if tx_time != pkt_tx_anterior:
                        link_margin_failed_count += 1
                        pkt_tx_anterior=tx_time
                    continue

                link_margin_ok_count += 1
                
                if tx_time==pkt_tx_anterior:
                    repeated_link_margin_tx_count+=1

                try:
                    
                    ## add ds_error dr_error to specify doppler error type    
                    
                    status, max_payload, ds_error,dr_error = checkComm(
                            sat_name,
                            lora_cfg,
                            ed_pos,
                            tx_time,
                            doppler_config
                    )

                    
                    ####################################################
                    # PASSED
                    ####################################################

                    if status:

                        # doppler pass e tempos diferentes
                        if tx_time!=pkt_tx_anterior:
                                                
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
                        # count doppler error only if pkt tx are different from anterior
                        if tx_time!=pkt_tx_anterior:
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

                pkt_tx_anterior=tx_time 

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

    visible_sat_height_mean = sum(visible_sat_height) / len(visible_sat_height) if visible_sat_height else None

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
        "link_margin_failed_count":link_margin_failed_count,
        "repeated_link_margin_tx_pass":repeated_link_margin_tx_count,
        "visible_sat_height_mean": visible_sat_height_mean
    }


def print_final_summary(
    network,
    generated_packets,
    collided,
    non_colliding,
    stats,
    lora_cfgs,
    satellite_config,
    endpoint_config,
    link_config
):


    # calculations
    
    collision_free_rate = (
        len(non_colliding)
        /
        generated_packets
    ) * 100 if generated_packets else 0
    
    visibility_rate = (
        stats["visible_count"]
        /
        len(non_colliding)
    ) * 100 if len(non_colliding) else 0
    
    doppler_rate = (
        stats["successfully_received"]
        /
        stats["visible_count"]
    ) * 100 if stats["visible_count"] else 0
    
    final_pdr = (
        stats["successfully_received"]
        /
        generated_packets
    ) * 100 if generated_packets else 0
    
    
    # accounting tx instead pkts for link margin
    link_margin_tx_pass = stats["link_margin_ok_count"]-stats["repeated_link_margin_tx_pass"]
    
    non_received = generated_packets-stats['successfully_received']
    
    non_received_rate = (
            non_received
            /
            generated_packets
        ) * 100 if generated_packets else 0
    
        
    collision_rate = (
        len(collided)
        /
        generated_packets
    ) * 100 if generated_packets else 0

    non_visibility_rate = (
        stats["non_visible_count"]
        /
        generated_packets
        ) * 100 if generated_packets else 0
    
    link_margin_tx_pass_rate=(
        link_margin_tx_pass
        /
            generated_packets
        ) * 100 if generated_packets else 0
        
    link_margin_tx_failed_rate=(
        stats["link_margin_failed_count"]
        /
            generated_packets
        ) * 100 if generated_packets else 0
        
    doppler_fail_rate = (
        stats["doppler_failed"]
        /
            generated_packets
        ) * 100 if generated_packets else 0
        
    doppler_static_fail_rate = (
        stats["doppler_static_failed_count"]
        /
            generated_packets
        ) * 100 if generated_packets else 0
    
    doppler_rate_fail_rate = (
        stats["doppler_rate_failed_count"]
        /
            generated_packets
        ) * 100 if generated_packets else 0
    
    doppler_exception_rate = (
            stats["doppler_exception_count"]
            /
                generated_packets
            ) * 100 if generated_packets else 0
    
    
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
    print(f"[PACKET FLOW]              :      num (% of tot.)")
    print("------------------------------------------------------------")

    print(
        f"Generated transmissions    : "
        f"{generated_packets:>8} "
        f"({100.00:>6.2f}%)"
    )
    print(
        f"  Collided                 : "
        f"{len(collided):>8} "
        f"({collision_rate:>6.2f}%)"
    )
    print(
        f"  Non Visible              : "
        f"{stats['non_visible_count']:>8} "
        f"({non_visibility_rate:>6.2f}%)"
    )
    print(
        f"  Link margin failed       : "
        f"{stats['link_margin_failed_count']:>8} "
        f"({link_margin_tx_failed_rate:>6.2f}%)"
    )
    print(
        f"  Doppler failed           : "
        f"{stats['doppler_failed']:>8} "
        f"({doppler_fail_rate:>6.2f}%)"
    )
    print(
        f"  Successfully received    : "
        f"{stats['successfully_received']:>8} "
        f"({final_pdr:>6.2f}%)"
    )

    print()
    print("------------------------------------------------------------")
    print(f"[DOPPLER]                  :      num (% of tot.)")    
    print("------------------------------------------------------------")

    print(
        f"  Doppler static failed    : "
        f"{stats['doppler_static_failed_count']:>8} "
        f"({doppler_static_fail_rate:>6.2f}%)"
    )
    print(
        f"  Doppler rate failed      : "
        f"{stats['doppler_rate_failed_count']:>8} "
        f"({doppler_rate_fail_rate:>6.2f}%)"
    )
    print(
        f"  Doppler code exception   : "
        f"{stats['doppler_exception_count']:>8} "
        f"({doppler_exception_rate:>6.2f}%)"
    )

    print("\n------------------------------------------------------------")
    print(f"[PACKET FLOW AUX]          :      num (% of tot.)")
    print("------------------------------------------------------------")

    print(
        f"Generated transmissions    : "
        f"{generated_packets:>8} "
        f"({100.00:>6.2f}%)"
    )
    print(
        f"  Collision-Free           : "
        f"{len(non_colliding):>8} "
        f"({collision_free_rate:>6.2f}%)"
    )
    print(
        f"  Visible                  : "
        f"{stats['visible_count']:>8} "
        f"({visibility_rate:>6.2f}%)"
    )
    print(
        f"  Link margin passed       : "
        f"{link_margin_tx_pass:>8} "
        f"({link_margin_tx_pass_rate:>6.2f}%)"
    )
    print(
        f"  Doppler passed           : "
        f"{stats['successfully_received']:>8} "
        f"({final_pdr:>6.2f}%)"
    )
    print(
        f"  Non received             : "
        f"{non_received:>8} "
        f"({non_received_rate:>6.2f}%)"
    )
            
    # evaluation statistics (energy in joules)

    successfully_tx_received = stats['successfully_received']
   
    pkt_energy = stats['toa'] * tx_power 
    
    total_energy = pkt_energy * generated_packets 
    
    successfully_energy_transm = successfully_tx_received * pkt_energy
    
    failed_energy_collided = len(collided) * pkt_energy
    
    failed_energy_visibility = stats['non_visible_count'] * pkt_energy
    
    failed_energy_doppler = stats['doppler_failed'] * pkt_energy
    
    link_margin_energy_pass = link_margin_tx_pass * pkt_energy
    
    failed_energy_link_margin = stats['link_margin_failed_count']*pkt_energy
    
    bytes_per_joule = (pkt_len * successfully_tx_received) / total_energy if total_energy > 0 else 0

    num_sats=satellite_config.num_sats
    
    if num_sats !=len(SATELLITES):
        raise ValueError("Num sats diverge")
    min_elevation_angle=satellite_config.min_elevation_angle
     
    # duty cycle calculation
    duty_cycle=stats['toa']*(generated_packets/endpoint_config.number_of_eds)*100/evaluation_time
    
    # eirp calculation
    eirp_dbm = link_config.iot_node.pt_dbm - link_config.iot_node.lftx + link_config.iot_node.gt
   
    lock_filename=results_filename + ".lock"
    # using lock to avoid race conditions when writing to the CSV file
    with FileLock(lock_filename):
    
        # write results to csv file
        with open(results_filename, "a", newline="") as csv_file:

            row = {
                # simulation config
                "sim_start":START_TS,
                "sim_end":END_TS,
                
                # lora config
                "sf": lora_cfgs[0].sf,
                "bw": lora_cfgs[0].bw,
                "ldro": lora_cfgs[0].ldro,
                "freqMHz": lora_cfgs[0].frequency,
                "pkt_len": len(payloads[0]),
                "pkt_toa": round(stats["toa"],6),
                            
                # endpoint config
                "central_point_lat": endpoint_config.geometry.central_point.lat,
                "central_point_lon": endpoint_config.geometry.central_point.lon,
                "num_of_eds": endpoint_config.number_of_eds,
                "pkt_per_endpoint": endpoint_config.pkt_per_endpoint,
                
                # satellite config
                "num_sats": num_sats,
                "min_elevation_angle": min_elevation_angle,
                
                # link margin config
                "tx_power": round(tx_power,3),
                "tx_power_dbm": tx_power_dbm,
                "eirp_dbm": eirp_dbm,
            
                # tx results
                "total_num_pkt": generated_packets,
                "collided": len(collided),
                "non_collided": len(non_colliding),
                "visible": stats['visible_count'],
                "non_visible": stats["non_visible_count"],
                "link_margin_pass": link_margin_tx_pass, 
                "link_margin_failed":stats["link_margin_failed_count"],   
                "doppler_pass":successfully_tx_received,
                "doppler_failed": stats["doppler_failed"],
                "doppler_shift_failed": stats["doppler_static_failed_count"],
                "doppler_rate_failed": stats["doppler_rate_failed_count"],
                "doppler_except_count" :stats["doppler_exception_count"],
                "non_received":non_received,
                "success_tx": successfully_tx_received,
                
                # tx rates
                "collided_rate": round(collision_rate, 2),
                "non_collided_rate": round(collision_free_rate, 2),
                "visibility_rate": round(visibility_rate, 2),
                "non_visibility_rate": round(non_visibility_rate, 2),
                "link_margin_pass_rate": round(link_margin_tx_pass_rate, 2),
                "link_margin_failed_rate": round(link_margin_tx_failed_rate, 2),
                "doppler_pass_rate": round(final_pdr, 2),
                "doppler_failed_rate": round(doppler_fail_rate, 2),
                "doppler_shift_failed_rate": round(doppler_static_fail_rate, 2),
                "doppler_rate_failed_rate": round(doppler_rate_fail_rate, 2),
                "doppler_except_count_rate": round(doppler_exception_rate, 2),
                "non_received_rate": round(non_received_rate,2),
                "final_pdr": round(final_pdr, 2),
                
                # energy budget
                "pkt_energy": round(pkt_energy, 6),
                "total_energy": round(total_energy, 6),
                "failed_energy_col": round(failed_energy_collided, 6),
                "failed_energy_vis": round(failed_energy_visibility, 6),
                "failed_energy_dop": round(failed_energy_doppler, 6),
                "failed_energy_link_margin": round(failed_energy_link_margin, 6),
                "link_margin_energy_pass": round(link_margin_energy_pass, 6),
                "succes_energy_trans": round(successfully_energy_transm, 6),
                "bytes_per_joule": round(bytes_per_joule,3),
                "duty_cycle":round(duty_cycle,3),
                
                # other
                "visible_sat_heigh_mean":round(stats['visible_sat_height_mean'],1)
            }

            writer = csv.DictWriter(
                csv_file,
                fieldnames=row.keys()
            )

            if csv_file.tell() == 0:
                writer.writeheader()

            writer.writerow(row)
     
    
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
    devices_filename
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

    if PRINT_SIMULATION_DEBUG:
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


print(
    "--- > Loading LoRa configurations ---"
)

# lora, payload len     
lora_cfgs = [config.lora]
pkt_len=config.lora.payload_len    

#results
results_filename=config.simulation.results_file

# endpoint
pkt_per_endpoint=config.endpoint.pkt_per_endpoint
policy_tx=config.endpoint.policy_tx

# link margin
tx_power_dbm=config.link_margin.iot_node.pt_dbm
tx_power=10 ** ((tx_power_dbm - 30) / 10)

print("\n--- > Generating random payloads ---")

payloads = generate_payloads(
    pkt_len,
    pkt_len,
    save_to=payload_generated_filename
)

print(
    "--- > Planning random transmissions ---"
)

random_transmissions(
    network,
    payloads,
    lora_cfgs,
    policy_tx,
    t_start=START_TS,
    t_end=END_TS,
    n_packets=pkt_per_endpoint,
    seed=None
)

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
    MIN_ELEVATION,
    doppler_config,
    link_config
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
    lora_cfgs,
    satellite_config,
    endpoint_config,
    link_config
)

#print_gateway_statistics(network)

print("\n============================================================")
print("                 END OF SIMULATION")
print("============================================================")


simulation_end = time.perf_counter()
simulation_time=simulation_end - simulation_start
print(f"simulation time: {simulation_time:.2f} s")