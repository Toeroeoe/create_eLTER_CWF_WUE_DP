#!/bin/bash -x
#SBATCH --job-name=eLTER_CWF_WUE_DP
#SBATCH --account=jibg31
#SBATCH --partition=dc-cpu
#SBATCH --output=out/log/wue_dp_%j.out
#SBATCH --error=out/log/wue_dp_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem 1024000
#SBATCH --time=2:00:00



source venv/activate.sh

srun -n 1 python src/create_dp.py


