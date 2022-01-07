#!/bin/bash 
#SBATCH --mem=0 
#SBATCH -A ABC123 
#SBATCH -t 5:00:00
#SBATCH -N 1 
##SBATCH -d PREV
#SBATCH -J MACHINE 
#SBATCH -o o-mx.MACHINE
#SBATCH -e e-mx.MACHINE

module load python/3.7-anaconda3

srun -N1 -n1  python3 "${GIT2_DIR}/ml-io-2021/code/missing_jobs_domain.py"

