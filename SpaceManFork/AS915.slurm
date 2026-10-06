#!/bin/bash

#SBATCH --job-name=repetition
#SBATCH --array=1-100
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --output=logs/%A_%a.out
#SBATCH --error=logs/%A_%a.err

LAT=-15.7938
LON=-47.8827
PT_DBM=30
FREQ=921.4
NUM_SATS=100
SF=12
LDRO=1
PKT_PER_ED=100
PAYLOAD_LEN=59
RESULTS_FILE="../data/AU915/au915_rep100_pt30.csv"

cd /home/infres/eribas/SpaceManFork_work_version/SpaceManFork/SpaceMan/src

python simulator.py \
    --central_point_lat "$LAT" \
    --central_point_lon "$LON" \
    --pt_dbm "$PT_DBM" \
    --freq "$FREQ" \
    --num_sats "$NUM_SATS" \
    --sf "$SF" \
    --ldro "$LDRO" \
    --pkt_per_ed "$PKT_PER_ED" \
    --payload_len "$PAYLOAD_LEN" \
    --results_file "$RESULTS_FILE"