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

# constants [m], [m/s^2], [m/s] 
EARTH_RADIUS = 6378137 
GRAVITY = 9.80665 
LIGHTSPEED = 299792458

# filenames
tle_directory="TLE/"
tle_filename="tle_active.txt"

# debug option
PRINT_DEBUG_DOPPLER=False


def loadSat(sat_name):
    """Return a satellite TLE object from its satellite name"""
    
    sat_file = Path(f"{tle_directory}{sat_name}.tle")
    
    if not sat_file.exists():
        # search TLE locally
        sat_find_loccaly= search_satellite_tle_locally(sat_name) 

        if not sat_find_loccaly:
            # download TLE from network
            downloadTLE(sat_name) 
    
    # get satellite info from TLE file
    satellite = load.tle_file(f"{tle_directory}{sat_name}.tle")[0] 

    return satellite

def search_satellite_tle_locally(sat_name, tle_filename, output_dir="TLE"):
    """ Search for a satellite TLE in a local file. 
    Return True if found, False otherwise"""
    
    with open(tle_filename, "r") as f:
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

            if PRINT_DEBUG_DOPPLER:
                print(f"TLE saved: {output_file}")

            return True

    if PRINT_DEBUG_DOPPLER:
        print(f"Satellite {sat_name} not found locally")

    return False


def evaluates_static_doppler(Ds,SF,BW,freq):
    """Evaluate static Doppler shift limits for a given SF, BW and frequency.
       Returns True if it passed and False otherwise
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
    First derivative at the central point using an N-point central 
    finite-difference formula. Returns the central derivative 
    """

    values = np.asarray(values, dtype=float)
    if npoints < 3 or npoints % 2 == 0:
        raise ValueError("Derivative num of points must be an odd number >= 3")
    if len(values) != npoints:
        raise ValueError("len(values) must be equal to num points")
    half = npoints // 2

    # normalized positions: -half, ..., -1, 0, +1, ..., +half
    x = np.arange(-half, half + 1, dtype=float)

    # vaFalsendermonde-like matrix
    A = np.array([
        x**k for k in range(npoints)
    ])

    # first derivative
    b = np.zeros(npoints)
    b[1] = 1.0

    # find the coefficients 
    coefficients = np.linalg.solve(A, b) 
    
    return np.dot(coefficients, values) / h_distance


def checkComm(sat_id, lora_cfg, ed_pos, tx_time, derivative_npoints, derivative_step_sec):
    """Check whether a Doppler error occurs. Return True if it passes (no Doppler error), 
    False otherwise."""

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

    if PRINT_DEBUG_DOPPLER:
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

    if PRINT_DEBUG_DOPPLER:
        print(f"Doppler rate central derivative ({derivative_npoints} points): {doppler_hz_sec_tx:.3f} Hz/s")
        doppler_hz_sec_vec_gr=np.gradient(doppler_hz_vec,derivative_step_sec)
        doppler_hz_sec_tx_gr=doppler_hz_sec_vec_gr[tx_index]
        print(f"Doppler rate with  gradient func (2 points): {doppler_hz_sec_tx_gr:.3f} Hz/s")
                    
    # evaluates doppler shift limit at syncronization
    ds_pass=evaluates_static_doppler(doppler_hz_tx,lora_cfg.sf,lora_cfg.bw,lora_cfg.fc)

    # packet number of symbols
    pkt_symbols = packet_bytes_to_symbols(lora_cfg)                  

    # Evaluates doppler rate  
    first_symbol_error = compute_first_doppler_error(lora_cfg,doppler_hz_sec_tx)
    dr_pass = first_symbol_error > pkt_symbols
    
    # max allowable number of symbols for the Doppler rate
    max_symbols=first_symbol_error-1

    # max allowable number of bytes
    new_lora_cfg = copy.deepcopy(lora_cfg)
    n_bytes_list,n_symbols_list=bytes_to_symbols(new_lora_cfg)
    if n_symbols_list[0]>max_symbols:
        max_pay_bytes=0
    else:
        max_pay_bytes = max(i for i, valor in enumerate(n_symbols_list) if valor <= max_symbols)+1

    # error flags    
    ds_error = 0 if ds_pass else 1  
    dr_error = 0 if dr_pass else 1

    # final status (logic OR)    
    if ds_error or dr_error:
        status=False
    else:
        status=True

    if PRINT_DEBUG_DOPPLER:    
        height_vec = wgs84.height_of(satellite.at(ts_vector)).m
        print(f"Doppler shift: {doppler_hz_tx:.2f} Hz, rate: {doppler_hz_sec_tx:.2f} Hz/s, {pkt_symbols} sym, 1st sym error {first_symbol_error}, ds_error {ds_error}, dr_error {dr_error}")
    
    return status, max_pay_bytes, ds_error, dr_error 
