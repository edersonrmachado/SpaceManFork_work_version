
# iot node EIRP
import math


pt = 22 # transmission power in dBm
lftx = 1 # transmitter feeder (equipment) loss in dB
gt = 4 # transmitter antenna gain in dBi
eirp = pt - lftx + gt  # Effective Isotropic Radiated Power in dBm

# free space propagation loss
lfs = -150.1 # free space propagation loss in dB

# other progagation losses
la = -0.11 # atmospheric attenuation Loss in dB              
li = -0.16 # ionospheric attenuation Loss in dB
ld = -3.0 # depointing Losses (antenna misalignment) in dB
lp = -3.0 # pola'''rization Mismatch Loss in dB   
l  = la + li + ld + lp # other propagation losses in dB

# satellite figure of merit
gr = -3.5 # satellite antenna gain in dBi
lfrx = 1 # receiver feeder (equipment) loss in dB
nf = 6.5 #	Receiver noise figure (EBYTE) in dB 		
temp_0 = 290 #	refererence temperature	in K

tf = (10**(lfrx/10)-1)*temp_0 # receiver line noise temperature in K
terx = (10**(nf/10)-1)*tf # receiver module noise temperature in K

gf= -1.0 # receiver line gain in dB 
ta = 290 # antenna noise temperature in K   
t_sis = ta + tf + terx/(10**(gf/10)) # system noise temperature in K
gr_ts = gr - lfrx - 10*math.log10(t_sis) # receiver figure of merit in dB/K
    
k = 1.38e-23  # Boltzmann constant times reference temperature
bw = 250000
snr_min = -17.5




# PRINT RESULTS

print("pt =", pt, "dBm")
print("lftx =", lftx, "dB")
print("gt =", gt, "dBi")
print("eirp =", eirp, "dBm")

print("-----------------------------")

print("lfs =", lfs, "dB")

print("la =", la, "dB")
print("li =", li, "dB")
print("ld =", ld, "dB")
print("lp =", lp, "dB")
print("l =", l, "dB")

print("-----------------------------")

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

print("-----------------------------")

print("k =", k, "W/K/Hz")
print("bw =", bw, "Hz")
print("snr_min =", snr_min, "dB")




















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