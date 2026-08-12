
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


import math


PRINT_LINK_BUDGET = True

def snr_min_db(sf):
    return -7.5 - 2.5 * (sf - 7)



# iot node EIRP
pt_dbm = 22 # transmission power in dBm
pt_dbw = pt_dbm - 30 # transmission power in dBW

lftx = 1 # transmitter feeder (equipment) loss in dB
gt = 4 # transmitter antenna gain in dBi
eirp_dbm = pt_dbm - lftx + gt  # Effective Isotropic Radiated Power in dBm
eirp_dbw = eirp_dbm - 30 # Effective Isotropic Radiated Power in dBW

# free space propagation loss
lfs = -150.1 # free space propagation loss in dB

# other progagation losses
la = -0.11 # atmospheric attenuation Loss in dB              
li = -0.16 # ionospheric attenuation Loss in dB
ld = -3.0 # depointing Losses (antenna misalignment) in dB
lp = -3.0 # polarization Mismatch Loss in dB   
l  = la + li + ld + lp # other propagation losses in dB

# satellite figure of merit
gr = -3.5 # satellite antenna gain in dBi
lfrx = 1 # receiver feeder (equipment) loss in dB
nf = 6.5 #	Receiver noise figure (EBYTE) in dB 		
temp_0 = 290 #	refererence temperature	in K

tf = (10**(lfrx/10)-1)*temp_0 # receiver line noise temperature in K
terx = (10**(nf/10)-1)*tf # receiver module noise temperature in K

#terx = (10**(nf/10) - 1) * temp_0

gf= -1.0 # receiver line gain in dB 
ta = 290 # antenna noise temperature in K   
t_sis = ta + tf + terx/(10**(gf/10)) # system noise temperature in K
gr_ts = gr - lfrx - 10*math.log10(t_sis) # receiver figure of merit in dB/K
    
k = 1.38e-23  # Boltzmann constant times reference temperature
bw = 125000   # bandwidth in Hz
sf=11

snr_min = snr_min_db(sf) # minimal SNR in dB for correspondent SF

pr=eirp_dbm + lfs + l # received power in dBm


### method 1

link_margin_1=eirp_dbw+lfs+l-10*math.log10(bw)+gr_ts+10*math.log10(1/k)-snr_min


## method 2

sensitivity_2=-174+nf+10*math.log10(bw)+snr_min # receiver sensitivity in dBm
link_margin_2=pr-sensitivity_2



sensitivity_1=10*math.log10(k*t_sis*bw)+snr_min +30 # receiver sensitivity in dBm
dif=sensitivity_1-sensitivity_2 


if  PRINT_LINK_BUDGET:

    print("------------ EIRP IoT node ----------")


    print("pt_dbm =", pt_dbm, "dBm")
    print("lftx =", lftx, "dB")
    print("gt =", gt, "dBi")
    print("eirp_dbm =", eirp_dbm, "dBm")
    print("eirp_dbw =", eirp_dbw, "dBW")

    print("----------- Free space loss ---------")

    print("lfs =", lfs, "dB")

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

    print("------- Boltzmann Constant --------")

    print("k =", k, "W/K/Hz")

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














'''
def check_link_margin(eirp,lfs,l,bw,gr_ts,snr_min):
    """Check if the link budget margin is within acceptable limits.
    Returns:
        bool: True if the link margin is acceptable, False otherwise.
    """

    margin=eirp+lfs+l+10*math.log10(bw)+gr_ts+10*math.log10(1/k)
    
    if MIN_LINK_BUDGET <= link_budget <= MAX_LINK_BUDGET:
        return True
    else:
        return False
'''