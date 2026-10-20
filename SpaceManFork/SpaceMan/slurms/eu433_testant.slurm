#!/bin/bash

#SBATCH --job-name=simulation
#SBATCH --array=1-100
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --output=logs/%A_%a.out
#SBATCH --error=logs/%A_%a.err

cd /home/infres/eribas/SpaceManFork_work_version/SpaceManFork/SpaceMan/src


python simulator.py  --central_point_lat --freq 868.3 --num_sats 100 --pt_dbm 16 --sf 12 --ldro 1 --pkt_per_ed 100 --payload_len 59  --results_file ../data/EU868/eu868_rep100_pt16.csv

##usage: simulator.py [-h] [--central_point_lat] [--central_point_lon] [--circle_radius] [--num_eds] [--pkt_per_ed] [--sf] [--bw] [--freq] [--payload_len] [--cr] [--crc] [--ih] [--ldro] [--preamble_len]
##                    [--num_sats] [--min_elev] [--pt_dbm] [--lftx] [--gt] [--la] [--li] [--ld] [--lp] [--gr] [--lfrx] [--nf] [--temp_0] [--gf] [--ta] [--doppler_points] [--doppler_step]

 --central_point_lat  48.8566 --central_point_lon 2.3522  --pt_dbm 16 --freq 868.3  --num_sats 100 --sf 12 --ldro 1 --pkt_per_ed 100 --payload_len 59  --results_file ../data/EU868/eu868_rep100_pt16.csv # Paris (FRANCE)
 
 --central_point_lat -3.5158 --central_point_lon 23.5801  --pt_dbm 12 --freq 433.75  --num_sats 100 --sf 12 --ldro 1 --pkt_per_ed 100 --payload_len 59  --results_file ../data/EU433/eu433_rep100_pt12.csv # Paris (FRANCE)

 --central_point_lat 29.5551 --central_point_lon 106.3834  --pt_dbm 19 --freq 473.3  --num_sats 100 --sf 12 --ldro 1 --pkt_per_ed 100 --payload_len 15  --results_file ../data/EU470/cn470_rep100_pt19.csv # Paris (FRANCE)
 
 --central_point_lat -15.7938 --central_point_lon -47.8827  --pt_dbm 30 --freq 921.4  --num_sats 100 --sf 12 --ldro 1 --pkt_per_ed 100 --payload_len 59 --results_file ../data/AU915/au915_rep100_pt30.csv # Paris (FRANCE)



freq = 433.375 #
lat = -3.5158  # lodja (CONGO)   
lon = 23.5801

# location config
freq = 473.3 # ch 15  
lat = 29.5551 # Chongqing (CHINA)
lon = 106.3834 

 

# location config 
freq = 921.4 #
lat = -15.7938 # Brasília (BRASIL)
lon = -47.8827 