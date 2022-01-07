#!/bin/bash 
#SBATCH --mem=0 
#SBATCH -A ABC123
#SBATCH -t 10:00:00
#SBATCH -N 4 
##SBATCH -d PREV
#SBATCH -J MACHINE 
#SBATCH -o o-ml.MACHINE
#SBATCH -e e-ml.MACHINE

module load python/3.7-anaconda3

IFS=,
months='Jan2020,Feb2020,Mar2020,Apr2020,May2020,Jun2020,Jul2020,Aug2020,Sep2020,Oct2020,Nov2020,Dec2020'
days_lst='31,29,31,30,31,30,31,31,30,31,30,31'
months=($months)
days_lst=($days_lst)
counter=0
for month in ${months[@]}; do
    days=${days_lst[counter]}
    day=1 
    while [ $day -le ${days} ] ; do
	srun -N1 -n1 -c1 --exclusive python3 "${GIT2_DIR}/ml-io-2021/code/darshan_ml_jobs.py" ${month} ${day} &
	sleep 2
	((day++))
    done;
    ((counter=counter+1))
done;
wait

