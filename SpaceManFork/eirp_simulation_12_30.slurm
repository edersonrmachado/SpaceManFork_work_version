#!/bin/bash

#SBATCH --job-name=simulation
#SBATCH --array=1-12
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=04:00:00
#SBATCH --output=logs/%A_%a.out
#SBATCH --error=logs/%A_%a.err

# scripts to run
PYTHON_SCRIPTS=(
    "batch_simulation_eirpEU868_A.py" 
    "batch_simulation_eirpEU868_B.py" 
    "batch_simulation_eirpEU868_C.py" 
    "batch_simulation_eirpCN470_A.py" 
    "batch_simulation_eirpCN470_B.py" 
    "batch_simulation_eirpCN470_C.py" 
    "batch_simulation_eirpEU433_A.py" 
    "batch_simulation_eirpEU433_B.py" 
    "batch_simulation_eirpEU433_C.py" 
    "batch_simulation_eirpAU915_A.py" 
    "batch_simulation_eirpAU915_B.py" 
    "batch_simulation_eirpAU915_C.py")

# select script based on SLURM_ARRAY_TASK_ID
SCRIPT=${PYTHON_SCRIPTS[$SLURM_ARRAY_TASK_ID-1]}

echo "Running task $SLURM_ARRAY_TASK_ID"
echo "Running script: $SCRIPT"

# Create a directory for the task and navigate into it
mkdir -p ${SLURM_ARRAY_TASK_ID}
cd ${SLURM_ARRAY_TASK_ID}

# clone the repository
git clone https://github.com/edersonrmachado/SpaceManFork_work_version.git



# go to the src directory
cd SpaceManFork_work_version/SpaceManFork/SpaceMan/

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd src


# run python script
python "$SCRIPT"