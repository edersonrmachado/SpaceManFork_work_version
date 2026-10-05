#!/bin/bash

#SBATCH --job-name=simulation
#SBATCH --array=1-10%5
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=02:00:00
#SBATCH --output=logs/%A_%a.out
#SBATCH --error=logs/%A_%a.err

#set -e

echo "Running task $SLURM_ARRAY_TASK_ID"

mkdir -p logs

git clone https://github.com/USER/MEU_REPO.git repo_$SLURM_ARRAY_TASK_ID

cd repo_$SLURM_ARRAY_TASK_ID

python A${SLURM_ARRAY_TASK_ID}.py