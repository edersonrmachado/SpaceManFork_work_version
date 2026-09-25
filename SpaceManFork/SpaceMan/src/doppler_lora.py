import numpy as np
from datetime import timedelta
import time
from skyfield.api import load, wgs84
from doppler_libsat import *

def packet_bytes_to_symbols(lora_cfg):
    """Return the number of symbols corresponding to a LoRa packet"""
    
    de=lora_cfg.ldro 
    
    # LDRO in auto mode, de=1 if t_symb>=16.386ms 
    if de is 2:
        #de = 1 if (lora_cfg.sf >= 11 and lora_cfg.bw == 125e3) else 0
        tsymb=(2**(lora_cfg.sf))/lora_cfg.bw 
        if tsymb >= 0.016384:
            de = 1
        else:
            de = 0
    
    
    n_payload = 8 + \
        max(np.ceil((8*lora_cfg.payload_len-4*lora_cfg.sf+28+16*lora_cfg.crc-20 *
            int(lora_cfg.ih))/(4*(lora_cfg.sf-2*int(de))))*(lora_cfg.cr+4), 0)
    n_payload = int(n_payload)

    return n_payload + lora_cfg.preamble_len


def compute_first_doppler_error(lora_cfg,DR):
    """Compute the first error symbol due to the Doppler"""
    
    # adjust SF to SF-2 if LDRO is activated 
    sf = lora_cfg.sf
    t_sym=(2**(lora_cfg.sf))/lora_cfg.bw 
    if lora_cfg.ldro == 1 or (lora_cfg.ldro == 2 and t_sym >= 0.016384):
        sf = lora_cfg.sf -2
    
    # number maximum of symbols without error    
    nmax=np.floor( (lora_cfg.bw**2)/(np.abs(DR)*2**(2*sf+1)))
    
    # first symbol error
    first_fail_symbol = nmax +1
    
    return int(first_fail_symbol)

def bytes_to_symbols(lora_cfg):
    """Return payload sizes from 1 to 255 bytes and their corresponding LoRa symbol counts."""
    
    n_symbols_list=[]
    n_bytes_list=[]
    
    lora_cfg.payload_len=0
    
    for n_bytes in range(1,256):
        lora_cfg.payload_len+=1
        n_symbols=packet_bytes_to_symbols(lora_cfg)
        n_symbols_list.append(n_symbols)
        n_bytes_list.append(n_bytes)
    
    return n_bytes_list,n_symbols_list
