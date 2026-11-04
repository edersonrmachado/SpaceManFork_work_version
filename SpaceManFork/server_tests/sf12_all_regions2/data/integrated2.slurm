#!/bin/bash

#SBATCH --job-name=itegrated
#SBATCH --array=1-30
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=04:00:00
#SBATCH --output=logs/%A_%a.out
#SBATCH --error=logs/%A_%a.err
cd /home/infres/eribas/SpaceManFork_work_version/SpaceManFork/SpaceMan/src


# ============================================================
# EU868 - Paris
# ============================================================

LAT=48.8566
LON=2.3522
PT_DBM=16
FREQ=868.3
NUM_SATS=100
SF=12
LDRO=1
PKT_PER_ED=100
PAYLOAD_LEN=59
RESULTS_FILE="../data/EU868/eu868_rep100_pt16.csv"

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

# ============================================================
# EU433
# ============================================================

LAT=-3.5158
LON=23.5801
PT_DBM=12
FREQ=433.75
NUM_SATS=100
SF=12
LDRO=1
PKT_PER_ED=100
PAYLOAD_LEN=59
RESULTS_FILE="../data/EU433/eu433_rep100_pt12.csv"

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


# ============================================================
# CN470
# ============================================================

LAT=29.5551
LON=106.3834
PT_DBM=19
FREQ=473.3
NUM_SATS=100
SF=12
LDRO=1
PKT_PER_ED=100
PAYLOAD_LEN=15
RESULTS_FILE="../data/EU470/cn470_rep100_pt19.csv"

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

# ============================================================
# AU915 - Brasília
# ============================================================

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
