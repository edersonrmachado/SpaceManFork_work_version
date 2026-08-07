import numpy as np
from datetime import timedelta
import time
from skyfield.api import load, wgs84
from doppler_libsat import *

def funcGetSymbolsN(lora_cfg):

    # auto LDRO???
    # DE = 1 if Ts > 16E-3 else 0

    n_payload = 8 + \
        max(np.ceil((8*lora_cfg.payload_len-4*lora_cfg.sf+28+16*lora_cfg.crc-20 *
            int(lora_cfg.ih))/(4*(lora_cfg.sf-2*int(lora_cfg.ldro))))*(lora_cfg.cr+4), 0)
    n_payload = int(n_payload)

    return n_payload + lora_cfg.preamble_len


def computeFirstFail(lora_cfg,DR):

    nmax=np.floor( (lora_cfg.bw**2)/(np.abs(DR)*2**(2*lora_cfg.sf+1)))
    first_fail_symbol = nmax +1
    return int(first_fail_symbol)

def bytes_symbols(lora_cfg):
    n_symbols_list=[]
    n_bytes_list=[]
    
    lora_cfg.payload_len=0
    for n_bytes in range(1,256):
        lora_cfg.payload_len+=1
        n_symbols=funcGetSymbolsN(lora_cfg)
        n_symbols_list.append(n_symbols)
        n_bytes_list.append(n_bytes)
    return n_bytes_list,n_symbols_list
