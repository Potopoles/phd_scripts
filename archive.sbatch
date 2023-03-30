#!/bin/bash -l
#
#SBATCH --job-name="arch dyamond2"
#SBATCH --time=23:00:00
#SBATCH --cpus-per-task=12
#SBATCH --partition=normal
#SBATCH --output=bOut/out5
#SBATCH --error=bOut/err5
#SBATCH --ntasks=1
#SBATCH --account='pr133'
#SBATCH --constraint=gpu

source ../load_modules_daint.sh
echo -e "$SLURM_JOB_NAME started on $(date):\n $command $1 $2\n"

compr_dir=/scratch/snx3000/heimc/data/archive/mscth
compr_dir=/scratch/snx3000/heimc/data/archive/tuning
compr_dir=/scratch/snx3000/heimc/data/archive/dyamond

#srun -c $SLURM_CPUS_PER_TASK tar -czvf $compr_dir.tgz $compr_dir/ 
#srun -c $SLURM_CPUS_PER_TASK tar -tzvf $compr_dir.tgz > $compr_dir.list 

srun -c $SLURM_CPUS_PER_TASK tar -cvf $compr_dir.tar $compr_dir/ 
srun -c $SLURM_CPUS_PER_TASK tar -tvf $compr_dir.tar > $compr_dir.list2

