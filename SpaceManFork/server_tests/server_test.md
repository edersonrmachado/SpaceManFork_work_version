## STEPS

### 1.  Enter to school net

```
ssh eribas@ssh.enst.fr
eribas@ssh.enst.fr's password:
```
### 2.  Enter to server network

```
ssh eribas@gpu-gw.enst.fr
```
Expected result: 


```
----------------------------------------------------------------------------
   __         ______   ______     __
  /\ \       /\__  _\ /\  ___\   /\ \
  \ \ \____  \/_/\ \/ \ \ \____  \ \ \
   \ \_____\    \ \_\  \ \_____\  \ \_\
    \/_____/     \/_/   \/_____/   \/_/
   ______     __         __  __     ______     ______   ______     ______
  /\  ___\   /\ \       /\ \/\ \   /\  ___\   /\__  _\ /\  ___\   /\  == \
  \ \ \____  \ \ \____  \ \ \_\ \  \ \___  \  \/_/\ \/ \ \  __\   \ \  __<
   \ \_____\  \ \_____\  \ \_____\  \/\_____\    \ \_\  \ \_____\  \ \_\ \_\
    \/_____/   \/_____/   \/_____/   \/_____/     \/_/   \/_____/   \/_/ /_/
----------------------------------------------------------------------------

```


### There is two modes interactive jobs and batch jobs

### Batch jobs


**1. Pass slurm file via ssh**
```
scp -J eribas@ssh.enst.fr eirp_simultion_12_30.slurm eribas@gpu-gw.enst.fr:/home/infres/eribas/
```

**2 On the folder /home/infres/eribas**  

Run  slurm file:

Example:

```
sbatch eirp_simulation_12_30.slurm
Submitted batch job 1022033
```

ID = 102233 (save this number)

**3. Verify status queue**
```
squeue -u eribas
```

**4. Copy back results files** 
Example:

```bash
scp -J eribas@ssh.enst.fr eribas@gpu-gw.enst.fr:/home/infres/eribas/file .
```
```bash
 scp -r -J eribas@ssh.enst.fr eribas@gpu-gw.enst.fr:/home/infres/eribas/1/SpaceManFork_work_version/SpaceManFork/SpaceMan/data 
```


**Copy folder**

```
scp -r -J eribas@ssh.enst.fr eribas@gpu-gw.enst.fr:/home/infres/eribas/SpaceManFork_work_version/SpaceManFork/SpaceMan/data 
```

**Check  elapsed time for a  job** 

```
sacct -j 1025110 --format=JobID,Start,End,Elapsed
```

**Check  elapsed time for a  job array** 
```
sacct -j 1025110 --array \
    --format=JobID,JobName,State,Start,End,Elapsed
```
**Check how many lines a file has**

```bash

```