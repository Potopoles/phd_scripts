#!/bin/bash -l
#
#SBATCH --job-name="MPAS_pp"
#SBATCH --time=00:30:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=6
#SBATCH --account='pr94'
#SBATCH --constraint=gpu
#SBATCH --partition=debug
#SBATCH --output=bOut/sbatch0.out
#SBATCH --error=bOut/sbatch0.err

source ~/phd_scripts/load_modules_daint.sh

echo -e "$SLURM_JOB_NAME started on $(date):\n $command $1 $2\n"

model_arg=MPAS_3.75
#model_arg=NICAM_3.5

#var_names=(QV QC T W U V H P \
#           U10M V10M T2M PS MSLP \
#           LWUTOA SWNDTOA SWDTOA SWUTOA \
#           SST SLHFLX SSHFLX \
#           TQC TQI TQV \
#           CLCL CLCT PP PPCONV PPGRID)

#var_arg=LWUTOA,SWNDTOA,SWDTOA,SWUTOA
#var_arg=SST,SLHFLX,SSHFLX
#var_arg=TQC,TQI,TQV
var_arg=T

## 6/6 tasks
srun -c $SLURM_CPUS_PER_TASK python -u pp03_preproc_dyamond.py\
                                           $SLURM_CPUS_PER_TASK $model_arg $var_arg


#srun -c $SLURM_CPUS_PER_TASK python -u pp02.5_test_files.py $SLURM_CPUS_PER_TASK NICAM 7
#srun -c $SLURM_CPUS_PER_TASK python -u pp02.5_test_files.py $SLURM_CPUS_PER_TASK NICAM 3.5
#srun -c $SLURM_CPUS_PER_TASK python -u pp02.5_test_files.py $SLURM_CPUS_PER_TASK SAM 4
#srun -c $SLURM_CPUS_PER_TASK python -u pp02.5_test_files.py $SLURM_CPUS_PER_TASK ICON 10
#srun -c $SLURM_CPUS_PER_TASK python -u pp02.5_test_files.py $SLURM_CPUS_PER_TASK ICON 2.5
#srun -c $SLURM_CPUS_PER_TASK python -u pp02.5_test_files.py $SLURM_CPUS_PER_TASK UM 5
#srun -c $SLURM_CPUS_PER_TASK python -u pp02.5_test_files.py $SLURM_CPUS_PER_TASK MPAS 7.5
#srun -c $SLURM_CPUS_PER_TASK python -u pp02.5_test_files.py $SLURM_CPUS_PER_TASK MPAS 3.75
#srun -c $SLURM_CPUS_PER_TASK python -u pp02.5_test_files.py $SLURM_CPUS_PER_TASK IFS 9
#srun -c $SLURM_CPUS_PER_TASK python -u pp02.5_test_files.py $SLURM_CPUS_PER_TASK IFS 4
#srun -c $SLURM_CPUS_PER_TASK python -u pp02.5_test_files.py $SLURM_CPUS_PER_TASK GEOS 3
#srun -c $SLURM_CPUS_PER_TASK python -u pp02.5_test_files.py $SLURM_CPUS_PER_TASK ARPEGE-NH 2.5
#srun -c $SLURM_CPUS_PER_TASK python -u pp02.5_test_files.py $SLURM_CPUS_PER_TASK FV3 3.25

echo -e "$SLURM_JOB_NAME finished on $(date)\n"


