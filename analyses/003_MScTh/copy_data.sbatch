#!/bin/bash -l
#
#SBATCH --job-name="003_copy"
#SBATCH --time=00:30:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --account='pr04'
#SBATCH --partition=xfer
#SBATCH --output=bOut/copy.out
#SBATCH --error=bOut/copy.err

module unload xalt

echo -e "$SLURM_JOB_NAME started on $(date):\n $command $1 $2\n"


./copy.sh


echo -e "$SLURM_JOB_NAME finished on $(date)\n"
