from datetime import timedelta
import time
from skyfield.api import load, wgs84
import matplotlib.pyplot as plt
import numpy as np
import copy
from doppler_classes import *
from doppler_tle import *
from doppler_lora import *
import matplotlib.dates as mdates 
from pathlib import Path
import os


MIN_ALT = 0 # min elevation angle in degrees
ANALYSIS_INTERVAL = 10 # in minutes
EARTH_RADIUS = 6378137 # radius of the Earth in meters
GRAVITY = 9.80665 # gravity acceleration in m/s^2
LIGHTSPEED = 299792458 # light speed in vacuum in m/s


def search_satellite_tle_locally(sat_name, tle_file="tle_active.txt", output_dir="TLE"):
    
    with open(tle_file, "r") as f:
        lines = [line.rstrip("\n") for line in f]

    for i, line in enumerate(lines):

        if line.strip() == sat_name:

            if i + 2 >= len(lines):
                raise ValueError(
                    f"Incomplete TLE for satellite {sat_name}"
                )

            name = lines[i].strip()
            line1 = lines[i + 1].strip()
            line2 = lines[i + 2].strip()

            if not line1.startswith("1 "):
                raise ValueError(
                    f"Invalid line 1 {sat_name}: {line1}"
                )

            if not line2.startswith("2 "):
                raise ValueError(
                    f"Invalid line 2 {sat_name}: {line2}"
                )

            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(
                output_dir,
                f"{sat_name}.tle"
            )

            with open(output_file, "w") as f:
                f.write(f"{name}\n")
                f.write(f"{line1}\n")
                f.write(f"{line2}\n")

            print(f"TLE saved: {output_file}")

            return True

    print(f"Satellite not found locally: {sat_name}")

    return False


def loadSat(sat_name):
    """Return a satellite TLE object from its satellite name"""
    
    sat_file = Path(f"TLE/{sat_name}.tle")

    if not sat_file.exists():
        sat_find_loccaly= search_satellite_tle_locally(sat_name) # search TLE locally

        if not sat_find_loccaly:
            downloadTLE(sat_name) # download TLE

    satellite = load.tle_file(f"{TLE_DIRECTORY}/{sat_name}.tle")[0] # get satellite info from TLE file

    #satellites = load.tle_file("tle_active.txt")
    #for satellite in satellites:

    #    if satellite.name == sat_name:
    #        return satellite

    #raise ValueError(f"Satellite '{sat_name}' not found in tle_active.txt")
    return satellite



def calculateF(h, t, f0):
    """ calculates Doppler with circular orbit approximation without using TLE"""
    f = (
        1/(1+((1/LIGHTSPEED)*np.sqrt((GRAVITY*EARTH_RADIUS)/(1+h/EARTH_RADIUS)))*(np.sin((np.sqrt(GRAVITY/EARTH_RADIUS)/(1+h/EARTH_RADIUS)**(3/2))*t) /
        np.sqrt((1+h/EARTH_RADIUS)**2-2*(1+h/EARTH_RADIUS)*np.cos((np.sqrt(GRAVITY/EARTH_RADIUS)/(1+h/EARTH_RADIUS)**(3/2))*t)+1)))*f0
    )
    return f

def calculateDeltaF(H,t):
    R = 6371000  # Raio da Terra em metros
    g = 9.80665  # Aceleração da gravidade em m/s^2
    c = 299792458 # velocidade da luz no vacuo em m/s
    deltaF=1/(1+((1/c)*np.sqrt((g*R)/(1+H/R)))*(np.sin((np.sqrt(g / R) / (1 + H / R) ** (3 / 2)) * t)/np.sqrt((1+H/R)**2-2*(1+H/R)*np.cos((np.sqrt(g / R) / (1 + H / R) ** (3 / 2)) * t)+1)))-1
    return deltaF


def D_rate(tempo, vetorParaProcurar,f0, t_gerador):
    t_gerador = np.asarray(t_gerador)  # converte lista para array
    index_tempo = np.abs(t_gerador - tempo).argmin()
    return vetorParaProcurar[index_tempo]*f0   

def computeDoppler(h, t, f0):
    f = calculateF(h, t, f0)
    return f - f0


def evaluates_static_doppler(Ds,SF,BW,freq):
    """Evaluate static Doppler shift limits for a given SF, BW and frequency"""

    Ds=np.abs(Ds)
    if SF==10:
        max_accept_DS=min(BW/4,freq*200/1e6)
    elif SF==11:    
        max_accept_DS=min(BW/4,freq*100/1e6)
    elif SF==12:    
        max_accept_DS=min(BW/4,freq*50/1e6)
    else:
        max_accept_DS=BW/4
    
    ds_pass=max_accept_DS>=Ds
    return  ds_pass


def checkComm(sat_id, lora_cfg, ed_pos, tx_time):

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
    alt, az, distance = topocentric.altaz()                                        

    if alt.degrees < MIN_ALT:
        print("❌  [Visibility] Fail elevation angle!")
        return False, 0
    else:
        # compute relative time
        t0 = ts.utc(t.utc_datetime() - timedelta(minutes=ANALYSIS_INTERVAL)) # seleciona tempo de inicio da analise
        tf = ts.utc(t.utc_datetime() + timedelta(minutes=ANALYSIS_INTERVAL)) # seleciona tempo final da analise
        # create time vector and compute altitudes
        times = ts.linspace(t0, tf, 2*ANALYSIS_INTERVAL*60+1) # cria um vetor de segundos de t0 a tf com intervalo de 1 segundo
        altitudes = difference.at(times).altaz()[0].degrees # calcula el angles para o vetor de segundos

    # get argmax (maximum altitude) and zenith timestamp
    max_index = np.argmax(altitudes) # calcula zenith pelo argmax (revisar posteriormente)
    zenith_time = times[max_index] # obtem o tempo do zenith
    # print(f"Zenith timestamp = {zenith_time.utc_datetime()}"v ,mm m,v,v
    # compute relative time
    t_relative = t.utc_datetime() - zenith_time.utc_datetime()
    

    
    t_relative_s = t_relative.total_seconds()
    #print(f"Relative time = {t_relative_s} seconds")

    # satellite height
    height = wgs84.height_of(satellite.at(t)).m
    
    # doppler
    doppler = computeDoppler(height, t_relative_s, lora_cfg.fc)

    print(f"Doppler shift: {doppler} Hz")
    
    t_relative_vec_s = [(dt - zenith_time.utc_datetime()).total_seconds()
    for dt in times.utc_datetime()] # vetor de tempo 
    height_vec = wgs84.height_of(satellite.at(times)).m
    doppler_vec= computeDoppler(height_vec, t_relative_vec_s, lora_cfg.fc)
    
    ds_pass=evaluates_static_doppler(doppler,lora_cfg.sf,lora_cfg.bw,lora_cfg.fc)
 
    
    # recalcula times vector para encontrar DR
    fs=lora_cfg.bw                                  # sampling frequency
    N=2**lora_cfg.sf                                # number of samples per symbol
    offsetSeconds=0.01                                # offset time in seconds to compute doppler around the symbol sequence
    num_points=int(offsetSeconds*fs*2+1)                     # number of points in the analysis interval
    t0 = ts.utc(t.utc_datetime() - timedelta(seconds=offsetSeconds)) # seleciona tempo de inicio da analise
    tf = ts.utc(t.utc_datetime() + timedelta(seconds=offsetSeconds)) # seleciona tempo final da analise
    # create time vector and compute altitudes
    times = ts.linspace(t0, tf, num_points) # cria um vetor de segundos de t0-offsetSeconds  a 
    #tf+offsetSeconds com intervalo de 1/fs segundos
    
    t_relative_vec_s = [(dt - zenith_time.utc_datetime()).total_seconds()
    for dt in times.utc_datetime()] # vetor de tempo 
    height_vec = wgs84.height_of(satellite.at(times)).m
    doppler_vec= computeDoppler(height_vec, t_relative_vec_s, lora_cfg.fc)
    #print(doppler_vec)
    
    deltaFppm=calculateDeltaF(height_vec,t_relative_vec_s)
    deltaF_ppm_sec = np.gradient(deltaFppm) / np.gradient(t_relative_vec_s)

    DR=D_rate(t_relative_s,deltaF_ppm_sec,lora_cfg.fc,t_relative_vec_s)

    ## ateh aqui
    
    pkt_symbols = funcGetSymbolsN(lora_cfg)                  
    n_first_fail = computeFirstFail(lora_cfg,DR)
    
    dr_pass = n_first_fail > pkt_symbols
    max_symbols=n_first_fail-1
    
    new_lora_cfg = copy.deepcopy(lora_cfg)
    n_bytes_list,n_symbols_list=bytes_symbols(new_lora_cfg)
    
    if n_symbols_list[0]>max_symbols:
        max_pay_bytes=0
    else:
        max_pay_bytes = max(i for i, valor in enumerate(n_symbols_list) if valor <= max_symbols)+1
    
    
    ds_value = doppler
    dr_value = DR
    ds_error = 0 if ds_pass else 1  
    dr_error = 0 if dr_pass else 1
    
    if ds_error or dr_error:
        status=False
    else:
        status=True
        
    #print(f"[Doppler evaluation] {t_relative_s} s, {ds_value:.2f} Hz, {dr_value:.2f} Hz/s, {pkt_symbols} sym, 1st sym error {n_first_fail}, ds_error {ds_error}, dr_error {dr_error}")
    #print(dr_error)
    return status, max_pay_bytes, ds_error, dr_error 
