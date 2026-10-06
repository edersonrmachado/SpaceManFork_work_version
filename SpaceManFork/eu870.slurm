#!/bin/bash

#SBATCH --job-name=simulation
#SBATCH --array=1-10
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --output=logs/%A_%a.out
#SBATCH --error=logs/%A_%a.err

home/infres/eribas/SpaceManFork_work_version/SpaceManFork/SpaceMan/src


python simulation.py  --freq 868.3 --num_sats 5 --pt_dbm 16 --sf 12 --ldro 1 --pkt_per_ed 100 --payload_len 59  --results_file ../data/eu868.csv


##usage: simulator.py [-h] [--central_point_lat] [--central_point_lon] [--circle_radius] [--num_eds] [--pkt_per_ed] [--sf] [--bw] [--freq] [--payload_len] [--cr] [--crc] [--ih] [--ldro] [--preamble_len]
##                    [--num_sats] [--min_elev] [--pt_dbm] [--lftx] [--gt] [--la] [--li] [--ld] [--lp] [--gr] [--lfrx] [--nf] [--temp_0] [--gf] [--ta] [--doppler_points] [--doppler_step]