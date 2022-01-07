#!/bin/bash 
#SBATCH --mem=0 
#SBATCH -A ABC123 
#SBATCH -t 10:00:00
#SBATCH -N 1
##SBATCH -d PREV
#SBATCH -J JOBS 
#SBATCH -o o_2
#SBATCH -e e_2

module load python/3.7-anaconda3

counter=0

for ((i=0;i<=1046;i=i+20)); 
do 
   echo ${i}
   srun -N1 -n1 -c1 --exclusive python3 ../codes/bytes_xfs_common.py ${i} &
   sleep 1
done;
wait


