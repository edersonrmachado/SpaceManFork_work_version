#!/bin/bash

#SBATCH --job-name=visibility_variable_poisson
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
EIRP_MAX=16
RESULTS_FILE="../data/eu868_visibility_variable_sf12.csv"

#NUM_SATS=(5 25 50 75 100 125 150)

NUM_SATS=(10 15 20 30 35 40 45 55 60 65 70 80 85 90 95 105 110 115 120 130 135 140 145 155 160 165 170 175)
DR_VALUE=0
SF=12
MAC_PAYLOAD_LEN=59
LDRO=1 
NUM_SIM_BY_REGION=4

for run in $(seq 1 "$NUM_SIM_BY_REGION")
do
    for i in "${!NUM_SATS[@]}"
    do
        PAYLOAD_LEN=$((MAC_PAYLOAD_LEN + 5))
        PTX_DBM=$(( EIRP_MAX - 2 * DR_VALUE + 1 ))

        python simulator.py \
            --central_point_lat "$LAT" \
            --central_point_lon "$LON" \
            --pt_dbm "$PTX_DBM" \
            --freq "$FREQ" \
            --num_sats  "${NUM_SATS[$i]}" \
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
EIRP_MAX=12
RESULTS_FILE="../data/eu433_visibility_variable_sf12.csv"

#NUM_SATS=(5 25 50 75 100 125 150)
NUM_SATS=(10 15 20 30 35 40 45 55 60 65 70 80 85 90 95 105 110 115 120 130 135 140 145 155 160 165 170 175)
DR_VALUE=0
SF=12
MAC_PAYLOAD_LEN=59
LDRO=1 
NUM_SIM_BY_REGION=4

for run in $(seq 1 "$NUM_SIM_BY_REGION")
do
    for i in "${!NUM_SATS[@]}"
    do
        PAYLOAD_LEN=$((MAC_PAYLOAD_LEN + 5))
        PTX_DBM=$(( EIRP_MAX - 2 * DR_VALUE + 1 ))

        python simulator.py \
            --central_point_lat "$LAT" \
            --central_point_lon "$LON" \
            --pt_dbm "$PTX_DBM" \
            --freq "$FREQ" \
            --num_sats  "${NUM_SATS[$i]}" \
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
RESULTS_FILE="../data/au915_visibility_variable_sf12.csv"

#NUM_SATS=(5 25 50 75 100 125 150)
NUM_SATS=(10 15 20 30 35 40 45 55 60 65 70 80 85 90 95 105 110 115 120 130 135 140 145 155 160 165 170 175)

DR_VALUE=0
SF=12
MAC_PAYLOAD_LEN=59
LDRO=1 
NUM_SIM_BY_REGION=4

for run in $(seq 1 "$NUM_SIM_BY_REGION")
do
    for i in "${!NUM_SATS[@]}"
    do
        PAYLOAD_LEN=$((MAC_PAYLOAD_LEN + 5))
        PTX_DBM=$(( EIRP_MAX - 2 * DR_VALUE + 1 ))

        python simulator.py \
            --central_point_lat "$LAT" \
            --central_point_lon "$LON" \
            --pt_dbm "$PTX_DBM" \
            --freq "$FREQ" \
            --num_sats  "${NUM_SATS[$i]}" \
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
EIRP_MAX=19
RESULTS_FILE="../data/cn470_visibility_variable_sf12.csv"

#NUM_SATS=(5 25 50 75 100 125 150)
NUM_SATS=(10 15 20 30 35 40 45 55 60 65 70 80 85 90 95 105 110 115 120 130 135 140 145 155 160 165 170 175)

DR_VALUE=0
SF=12
MAC_PAYLOAD_LEN=15
LDRO=1 
NUM_SIM_BY_REGION=4

for run in $(seq 1 "$NUM_SIM_BY_REGION")
do
    for i in "${!NUM_SATS[@]}"
    do
        PAYLOAD_LEN=$((MAC_PAYLOAD_LEN + 5))
        PTX_DBM=$(( EIRP_MAX - 2 * DR_VALUE + 1 ))

        python simulator.py \
            --central_point_lat "$LAT" \
            --central_point_lon "$LON" \
            --pt_dbm "$PTX_DBM" \
            --freq "$FREQ" \
            --num_sats  "${NUM_SATS[$i]}" \
            --sf "$SF" \
            --ldro "$LDRO" \
            --payload_len "$PAYLOAD_LEN" \
            --results_file "$RESULTS_FILE"
    done
done
