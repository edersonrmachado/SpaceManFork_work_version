# Modifications

## Organization of files

 
- creating folders
  - `src`: for all code files.  
  - `data`: for data files, for instance TLEs, results.txt.  
  - `docs`: for explanations, documentation.  
  - `figures` for plots, other figures, etc.  
  
- creating `.gitignore` for following files:
  - `src/__pycache__/`
  - `venv/`
  - `src/GitMerge.sh`
  - `src/GitMerge.sh`
  - `src/GitMerge.sh`

- removed file
  - `myenv` (185MB), replaced by `venv` which was added to `.gitignore`
  - `__pycache__/` removed and added to `.gitignore`



## How to use this repo:

1. Creates a venv and install required packages: 

```bash
    python3 -m venv venv 
    source venv/bin/activate 
    pip install -r requirements.txt
```


2. Run one simulation it will load the test configuration of  [config.json](src/config/config.json):  
   
  
```bash
cd src  
python simulation.py 
```
3. Run simulation batch (the configuration block can be defined in `batch_simulation.py`file):
   
```bash
python batch_simulation.py 
```
4. Plots: once one or more simulation files were generated, check their names on [data](data) folder and pass it to the [graphs.py](src/graphs.py) file

```python
# files to evaluate
files=[
"../data/bw31.25_ldro0_f915_plen35_pped100_txp1.csv",
"../data/bw31.25_ldro0_f915_plen50_pped100_txp1.csv",
"../data/bw31.25_ldro0_f915_plen100_pped100_txp1.csv",
"../data/bw31.25_ldro0_f915_plen200_pped100_txp1.csv"
]
```

Then choose the output pdf filenames (PDR and energy plots),
```
# output filenames  (freq_bw)
fig_1='pdr915_3125.pdf'
fig_2="energy915_3125.pdf"
```
and run the  [graphs.py](src/graphs.py) file:

```bash
python graphs.py
```

## License

This project is licensed under the XXXX License ...


# Using LCTI server to speed up the simulations

 
## Step 1: Connect to the SSH gateway:
```
ssh eribas@ssh.enst.fr
```
After entering your password, you'll be on the gateway server.

## Step 2: From the gateway, connect to the cluster:
```
ssh eribas@gpu-gw
```

## Step 3: Request resources to run the code

 It uses Slurm (Simple Linux Utility for Resource Management), a widely-used workload manager and job scheduler. 

### Two ways to run jobs#

Slurm provides two primary methods for running computational work:

    - Interactive - For real-time interaction with compute resources
    - Batch - Submit your task and disconnect

Let's explore both methods in detail.

#### Interactive jobs

Interactive jobs give you a shell session on a compute node to run commands in real time — ideal for testing and debugging. The cluster provides a wrapper command, sinteractive, for starting them:
```
sinteractive
```
You'll see output like this:
```
srun: job 12345 queued and waiting for resources
srun: job 12345 has been allocated resources
```
After a few moments (or longer if the cluster is busy), you'll get a shell prompt on a compute node:

```
<tp-username>@node19 ~$
```


