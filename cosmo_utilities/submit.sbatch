#!/bin/bash -l
#
#SBATCH --job-name="replace QI"
#SBATCH --time=10:00:00
#SBATCH --cpus-per-task=1
#SBATCH --partition=normal
#SBATCH --output=bOut/sbatch0.out
#SBATCH --error=bOut/sbatch0.err
#SBATCH --ntasks=1
#SBATCH --account='pr94'
#SBATCH --constraint=gpu


source ../load_modules_daint.sh
echo -e "$SLURM_JOB_NAME started on $(date):\n $command $1 $2\n"

srun -c $SLURM_CPUS_PER_TASK python -u remove_qi.py

echo -e "$SLURM_JOB_NAME finished on $(date)\n"


