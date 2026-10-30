#!/bin/bash

#SBATCH --job-name=eirp_constant_poisson
#SBATCH --array=1-25
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=10:00:00
#SBATCH --output=logs/%A_%a.out
#SBATCH --error=logs/%A_%a.err

cd /home/infres/eribas/SpaceManFork_work_version/SpaceManFork/SpaceMan/src

# ============================================================
# EU868 - Paris
# ============================================================

LAT=48.8566
LON=2.3522
FREQ=868.3
EIRP_MAX=30
RESULTS_FILE="../data/eu868_eirp_constant_poisson.csv"

NUM_SATS=100
DR_VALUES=(0 1 2 3 4 5)
SF_VALUES=(12 11 10 9 8 7)
MAC_PAYLOAD_LEN=(59 59 59 123 240 240)
LDRO_VALUES=(1 1 0 0 0 0)
NUM_SIM_BY_REGION=4

for run in $(seq 1 "$NUM_SIM_BY_REGION")
do
    for i in "${!DR_VALUES[@]}"
    do
        DR=${DR_VALUES[$i]}
        SF=${SF_VALUES[$i]}
        LDRO=${LDRO_VALUES[$i]}
        PAYLOAD_LEN=$((MAC_PAYLOAD_LEN[$i] + 5))
        PTX_DBM=$(( EIRP_MAX + 1 ))

        python simulator.py \
            --central_point_lat "$LAT" \
            --central_point_lon "$LON" \
            --pt_dbm "$PTX_DBM" \
            --freq "$FREQ" \
            --num_sats "$NUM_SATS" \
            --sf "$SF" \
            --ldro "$LDRO" \
            --payload_len "$PAYLOAD_LEN" \
            --results_file "$RESULTS_FILE"
    done
done

# ============================================================
# EU433
# ============================================================

LAT=-3.5158
LON=23.5801
FREQ=433.375
EIRP_MAX=30
RESULTS_FILE="../data/eu433_eirp_constant_poisson.csv"

NUM_SATS=100
DR_VALUES=(0 1 2 3 4 5)
SF_VALUES=(12 11 10 9 8 7)
MAC_PAYLOAD_LEN=(59 59 59 123 240 240)
LDRO_VALUES=(1 1 0 0 0 0)
NUM_SIM_BY_REGION=4

for run in $(seq 1 "$NUM_SIM_BY_REGION")
do
    for i in "${!DR_VALUES[@]}"
    do
        DR=${DR_VALUES[$i]}
        SF=${SF_VALUES[$i]}
        LDRO=${LDRO_VALUES[$i]}
        PAYLOAD_LEN=$((MAC_PAYLOAD_LEN[$i] + 5))
        PTX_DBM=$(( EIRP_MAX + 1 ))

        python simulator.py \
            --central_point_lat "$LAT" \
            --central_point_lon "$LON" \
            --pt_dbm "$PTX_DBM" \
            --freq "$FREQ" \
            --num_sats "$NUM_SATS" \
            --sf "$SF" \
            --ldro "$LDRO" \
            --payload_len "$PAYLOAD_LEN" \
            --results_file "$RESULTS_FILE"
    done
done


# ============================================================
# AU915 - Brasília
# ============================================================

LAT=-15.7938
LON=-47.8827
FREQ=921.4
EIRP_MAX=30
RESULTS_FILE="../data/au915_eirp_constant_poission.csv"

NUM_SATS=100
DR_VALUES=(0 1 2 3 4 5)
SF_VALUES=(12 11 10 9 8 7)
MAC_PAYLOAD_LEN=(59 59 59 123 240 240)
LDRO_VALUES=(1 1 0 0 0 0)
NUM_SIM_BY_REGION=4

for run in $(seq 1 "$NUM_SIM_BY_REGION")
do
    for i in "${!DR_VALUES[@]}"
    do
        DR=${DR_VALUES[$i]}
        SF=${SF_VALUES[$i]}
        LDRO=${LDRO_VALUES[$i]}
        PAYLOAD_LEN=$((MAC_PAYLOAD_LEN[$i] + 5))
       PTX_DBM=$(( EIRP_MAX + 1 ))

        python simulator.py \
            --central_point_lat "$LAT" \
            --central_point_lon "$LON" \
            --pt_dbm "$PTX_DBM" \
            --freq "$FREQ" \
            --num_sats "$NUM_SATS" \
            --sf "$SF" \
            --ldro "$LDRO" \
            --payload_len "$PAYLOAD_LEN" \
            --results_file "$RESULTS_FILE"
    done
done



# ============================================================
# CN470
# ============================================================

LAT=29.5551
LON=106.3834
FREQ=473.3
EIRP_MAX=30
RESULTS_FILE="../data/cn470_eirp_constant_poisson.csv"

NUM_SATS=100
DR_VALUES=(0 1 2 3 4 5)
SF_VALUES=(12 11 10 9 8 7)
MAC_PAYLOAD_LEN=(15 31 94 194 230 230)
LDRO_VALUES=(1 1 0 0 0 0)
NUM_SIM_BY_REGION=4

for run in $(seq 1 "$NUM_SIM_BY_REGION")
do
    for i in "${!DR_VALUES[@]}"
    do
        DR=${DR_VALUES[$i]}
        SF=${SF_VALUES[$i]}
        LDRO=${LDRO_VALUES[$i]}
        PAYLOAD_LEN=$((MAC_PAYLOAD_LEN[$i] + 5))
        PTX_DBM=$(( EIRP_MAX  + 1 ))

        python simulator.py \
            --central_point_lat "$LAT" \
            --central_point_lon "$LON" \
            --pt_dbm "$PTX_DBM" \
            --freq "$FREQ" \
            --num_sats "$NUM_SATS" \
            --sf "$SF" \
            --ldro "$LDRO" \
            --payload_len "$PAYLOAD_LEN" \
            --results_file "$RESULTS_FILE"
    done
done


