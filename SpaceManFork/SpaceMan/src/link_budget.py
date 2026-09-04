
from datetime import timedelta
import time
from skyfield.api import load, wgs84
import matplotlib.pyplot as plt
import numpy as np
import copy
from doppler_classes import *
from doppler_tle import *
from doppler_lora import *
from doppler_libsat import *
import json 

import math

BOLTZMANN_CONSTANT = 1.38e-23  # Boltzmann constant in J/K
LIGHT_SPEED = 299792458.0
PRINT_LINK_BUDGET = False # debug


def snr_min_db(sf):
    return -7.5 - 2.5 * (sf - 7)

def free_space_loss(sat_id, lora_cfg, ed_pos, tx_time):
    """Calculate the free space loss in dB.
    Args:
        sat_id (str): Satellite ID to extract TLE.
        lora_cfg (dict): LoRa configuration parameters.
        ed_position (xxx): End device position with latitude and longitude. 
        tx_time (xx): Transmission time.
        
    Returns:
        lfs (float): Free space loss in dB.
    """
    local = wgs84.latlon(
        latitude_degrees=ed_pos.latitude, longitude_degrees=ed_pos.longitude
    )
    satellite = loadSat(sat_id)

    # Load timescale and set time
    ts = load.timescale()

    # epoch to struct_time
    tstp = time.gmtime(tx_time)

    # struct_time to tuple
    t_tuple = (tstp.tm_year, tstp.tm_mon, tstp.tm_mday,
                tstp.tm_hour, tstp.tm_min, tstp.tm_sec)
    t = ts.utc(*t_tuple) # objeto tempo do skyfield represent. instante de transmissao

    # compute satellite position relative to observer
    difference = satellite - local
    topocentric = difference.at(t) # calcula onde o sat esta no instante t
    #alt, az, distance = topocentric.altaz()                  
    distance = topocentric.distance().m # distance in m

    lfs=20*np.log10(distance)+20*np.log10(lora_cfg.fc)+20*np.log10(4*math.pi/LIGHT_SPEED) # free space propagation loss in dB

    return -lfs


def compute_link_margin(sat_id, lora_cfg, ed_pos, tx_time,link_config):
    """Compute the link budget for a given satellite and LoRa configuration.
    Args:
        sat_id (str): Satellite ID to extract TLE.
        lora_cfg (dict): LoRa configuration parameters.
        ed_pos (dict): End device position with latitude and longitude.
        tx_time (float): Transmission time in seconds since epoch.
        link_config (dict): Link configuration parameters.
    
    Returns:
        link_margin_1 (float): Link margin in dB "our" method.
        link_margin_2 (float): Link margin in dB "articles" method.
        link_pass (int): 1 if link margin is positive, 0 otherwise.

    """

    # iot node EIRP
    pt_dbm =link_config["iot_node"]["pt_dbm"] # transmission power in dBm
    pt_dbw = pt_dbm - 30 # transmission power in dBW
        
    # free space propagation loss
    lfs = free_space_loss(sat_id, lora_cfg, ed_pos, tx_time)
    
    # other progagation losses
    la = link_config["propagation_losses"]["la"] # atmospheric attenuation Loss in dB   
    li = link_config["propagation_losses"]["li"] # ionospheric attenuation Loss in dB
    ld = link_config["propagation_losses"]["ld"] # depointing Losses (antenna misalignment) in dB
    lp = link_config["propagation_losses"]["lp"] # polarization Mismatch Loss in dB   

    l  = la + li + ld + lp # all propagation losses in dB
    
    lftx = link_config["iot_node"]["lftx"] # transmitter feeder (equipment) loss in dB
    gt = link_config["iot_node"]["gt"] # transmitter antenna gain in dBi
    eirp_dbm = pt_dbm - lftx + gt  # Effective Isotropic Radiated Power in dBm
    eirp_dbw = eirp_dbm - 30 # Effective Isotropic Radiated Power in dBW

    # satellite figure of merit
    gr = link_config["satellite_receiver"]["gr"] # satellite antenna gain in dBi
    lfrx = link_config["satellite_receiver"]["lfrx"] # receiver feeder (equipment) loss in dB
    nf = link_config["satellite_receiver"]["nf"] #	Receiver noise figure (EBYTE) in dB 		
    temp_0 = link_config["satellite_receiver"]["temp_0"] #	refererence temperature	in K

    tf = (10**(lfrx/10)-1)*temp_0 # receiver line noise temperature in K
    terx = (10**(nf/10)-1)*tf # receiver module noise temperature in K

    gf= link_config["satellite_receiver"]["gf"] # receiver line gain in dB 
    ta = link_config["satellite_receiver"]["ta"] # antenna noise temperature in K   

    # System temperature 
    t_sis = ta + tf + terx/(10**(gf/10)) # system noise temperature in K
    gr_ts = gr - lfrx - 10*math.log10(t_sis) # receiver figure of merit in dB/K
        
    bw =lora_cfg.bw   # bandwidth in Hz
    sf=lora_cfg.sf   # spreading factor           

    snr_min = snr_min_db(sf) # minimal SNR in dB for correspondent SF
    pr=eirp_dbm + lfs + l # received power in dBm

    ## method 1 (our)
    link_margin_1=eirp_dbw+lfs+l-10*math.log10(bw)+gr_ts+10*math.log10(1/BOLTZMANN_CONSTANT)-snr_min
    sensitivity_1=10*math.log10(BOLTZMANN_CONSTANT*t_sis*bw)+snr_min +30 # receiver sensitivity in dBm
    
    ## method 2 (articles)
    sensitivity_2=-174+nf+10*math.log10(bw)+snr_min # receiver sensitivity in dBm

    dif=sensitivity_1-sensitivity_2 
    link_margin_2=pr-sensitivity_2    

    if  PRINT_LINK_BUDGET:

        print("------------ EIRP IoT node ----------")


        print("pt_dbm =", pt_dbm, "dBm")
        print("lftx =", lftx, "dB")
        print("gt =", gt, "dBi")
        print("eirp_dbm =", eirp_dbm, "dBm")
        print("eirp_dbw =", eirp_dbw, "dBW")

        print("----------- Free space loss ---------")

        print(f"lfs = {lfs:.2f} dB")

        print("----- Other Propagation Losses ------")

        print("la =", la, "dB")
        print("li =", li, "dB")
        print("ld =", ld, "dB")
        print("lp =", lp, "dB")
        print("l =", l, "dB")

        print("----- Receiver Figure of Merit -----")

        print("gr =", gr, "dBi")
        print("lfrx =", lfrx, "dB")
        print("nf =", nf, "dB")
        print("temp_0 =", temp_0, "K")

        print(f"tf = {tf:.1f} K")
        print(f"terx = {terx:.1f} K")
        print("gf =", gf, "dB")
        print("ta =", ta, "K")
        print(f"t_sis = {t_sis:.1f} K")
        print(f"gr_ts = {gr_ts:.1f} dB/K")

        print(f"lfs = {lfs:.2f} dB")


        print("------- Boltzmann Constant --------")

        print("k =", BOLTZMANN_CONSTANT, "W/K/Hz")

        print("---------- Bandwidth --------------")
        print("bw =", bw, "Hz")
        print("- Required Carrier to noise Ratio -")
        print("snr_min =", snr_min, "dB")

        print("---------- Received Power -----------")
        print(f"pr = {pr:.1f} dBm")

        print("---------- Link Margin -----------")
        print(f"link_margin_1 = {link_margin_1:.2f} dB")
        print(f"link_margin_2 = {link_margin_2:.2f} dB")

        print("-------- Receiver Sensitivity ---------")
        print(f"sensitivity_1 = {sensitivity_1:.2f} dBm")
        print(f"sensitivity_2 = {sensitivity_2:.2f} dBm")
        print(f"difference = {dif:.2f} dB") 

    link_pass = 0 if link_margin_1 < 0 else 1     

    return link_margin_1, link_margin_2, link_pass



