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
import datetime

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

    return satellite

def evaluates_static_doppler(Ds,SF,BW,freq):
    """Evaluate static Doppler shift limits for a given SF, BW and frequency.
       Returns true if it passed and false otherwise
    """

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


def calculate_derivative_npoints(values, h_distance, npoints):
    """
    First derivative at the central point using
    an N-point central finite-difference formula.
    Returns the central derivative 
    """

    values = np.asarray(values, dtype=float)
    if npoints < 3 or npoints % 2 == 0:
        logger.error("Derivative num of points must be an odd number >= 3")
        raise ValueError("Derivative num of points must be an odd number >= 3")
    if len(values) != npoints:
        logger.error("len(values) must be equal to num points")
        raise ValueError("len(values) must be equal to num points")
    half = npoints // 2

    # Normalized positions: -half, ..., -1, 0, +1, ..., +half
    x = np.arange(-half, half + 1, dtype=float)

    # Vandermonde-like matrix
    A = np.array([
        x**k for k in range(npoints)
    ])

    # First derivative
    b = np.zeros(npoints)
    b[1] = 1.0
    coefficients = np.linalg.solve(A, b) # find the coefficients 
    return np.dot(coefficients, values) / h_distance


def checkComm(sat_id, lora_cfg, ed_pos, tx_time, derivative_npoints, derivative_step_sec):



    local = wgs84.latlon(latitude_degrees=ed_pos.latitude, longitude_degrees=ed_pos.longitude)

    satellite = loadSat(sat_id)
    
    # Load timescale and set time
    ts = load.timescale()
    
    # Unix timestamp UTC -> datetime UTC
    tx_datetime = datetime.datetime.fromtimestamp(tx_time, datetime.timezone.utc)

    # datetime UTC -> Skyfield Time
    t = ts.from_datetime(tx_datetime)

    # compute satellite position relative to observer
    difference = satellite - local

    # compute where the satellite is at time t
    topocentric = difference.at(t) 
    alt, az, distance = topocentric.altaz()                                        

    # time vector for derivative computation 
    tx_index = derivative_npoints // 2
    time_offsets = (
        np.arange(-tx_index, tx_index + 1)
        * derivative_step_sec
    )
    datetime_derivative_times = [
        tx_datetime + datetime.timedelta(seconds=float(offset))
        for offset in time_offsets
    ]
    ts_vector = ts.from_datetimes(datetime_derivative_times)

    # calculate distance and velocity vectors
    topo = (satellite - local).at(ts_vector) # creates a relative vector between satellite and observer for the times in ts_vector
    pos_km = topo.position.km  # relative position vector in km      
    vel_km_s = topo.velocity.km_per_s  # relative velocity vector in km/s
    r_norm_km = np.linalg.norm(pos_km, axis=0) # magnitude of the relative position vector in km
    dot_rv_km2_s = np.sum(pos_km * vel_km_s, axis=0) # dot product of the relative position and velocity vectors in km^2/s
    range_rate_m_s = (dot_rv_km2_s / r_norm_km) * 1000.0  # m/s    # range rate in m/s (v(t) = (r · v) / |r|)  
    f_received = lora_cfg.fc * (1.0 - range_rate_m_s / LIGHTSPEED) # received frequency in Hz (f_received = f0 * (1 - v_rad / c))
    doppler_hz_vec = f_received - lora_cfg.fc 

    # Doppler shift in Hz  
    doppler_hz_tx = doppler_hz_vec[tx_index]

    # Doppler rater in Hz/s
    doppler_hz_sec_tx=calculate_derivative_npoints(doppler_hz_vec, derivative_step_sec, derivative_npoints)

    #doppler_hz_sec_vec=np.gradient(doppler_hz_vec,derivative_step)
    #doppler_hz_sec_tx=doppler_hz_sec_vec[tx_index]
        
    # evaluates doppler shift limit at syncronization
    ds_pass=evaluates_static_doppler(doppler_hz_tx,lora_cfg.sf,lora_cfg.bw,lora_cfg.fc)

    # packet number of symbols
    pkt_symbols = funcGetSymbolsN(lora_cfg)                  

    # evaluates doppler rate
    n_first_fail = computeFirstFail(lora_cfg,doppler_hz_sec_tx)
    
    dr_pass = n_first_fail > pkt_symbols
    max_symbols=n_first_fail-1
    
    new_lora_cfg = copy.deepcopy(lora_cfg)
    n_bytes_list,n_symbols_list=bytes_symbols(new_lora_cfg)
    
    if n_symbols_list[0]>max_symbols:
        max_pay_bytes=0
    else:
        max_pay_bytes = max(i for i, valor in enumerate(n_symbols_list) if valor <= max_symbols)+1
        
    ds_value = doppler_hz_tx
    dr_value = doppler_hz_sec_tx
    ds_error = 0 if ds_pass else 1  
    dr_error = 0 if dr_pass else 1
    
    if ds_error or dr_error:
        status=False
    else:
        status=True
        
    #height_vec = wgs84.height_of(satellite.at(ts_vector)).m

    #print(f"Doppler shift{ds_value:.2f} Hz, rate {dr_value:.2f} Hz/s, {pkt_symbols} sym, 1st sym error {n_first_fail}, ds_error {ds_error}, dr_error {dr_error}")
    
    return status, max_pay_bytes, ds_error, dr_error 
