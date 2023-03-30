#!/bin/bash -l
#
#SBATCH --job-name="calc_WVP"
#SBATCH --time=00:30:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --account='pr04'
#SBATCH --constraint=gpu
#SBATCH --partition=debug
#SBATCH --output=bOut/sbatch.out
#SBATCH --error=bOut/sbatch.err

echo -e "$SLURM_JOB_NAME started on $(date):\n $command $1 $2\n"

source setenv.sh

srun -c $SLURM_CPUS_PER_TASK -n $SLURM_NTASKS python -u 02_*.py $SLURM_CPUS_PER_TASK


echo -e "$SLURM_JOB_NAME finished on $(date)\n"


