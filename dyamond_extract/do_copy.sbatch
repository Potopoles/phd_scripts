#!/bin/bash -l
#
#SBATCH --job-name="copy_GEOS"
#SBATCH --time=01:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --account='pr04'
#SBATCH --constraint=gpu
#SBATCH --partition=xfer
#SBATCH --output=bOut/copy0.out
#SBATCH --error=bOut/copy0.err

module unload xalt

echo -e "$SLURM_JOB_NAME started on $(date):\n $command $1 $2\n"

#srun -n $SLURM_NTASKS pp02_proj_to_scratch.sh
srun -n $SLURM_NTASKS pp04_scratch_to_proj.sh

###DONE
#srun -n $SLURM_NTASKS pp01_daint_copy_from_mist.sh NICAM_7
#srun -n $SLURM_NTASKS pp01_daint_copy_from_mist.sh NICAM_3.5
#srun -n $SLURM_NTASKS pp01_daint_copy_from_mist.sh SAM_4
#srun -n $SLURM_NTASKS pp01_daint_copy_from_mist.sh ICON_10
#srun -n $SLURM_NTASKS pp01_daint_copy_from_mist.sh ICON_2.5
#srun -n $SLURM_NTASKS pp01_daint_copy_from_mist.sh UM_5
#srun -n $SLURM_NTASKS pp01_daint_copy_from_mist.sh MPAS_7.5
#srun -n $SLURM_NTASKS pp01_daint_copy_from_mist.sh MPAS_3.75
#srun -n $SLURM_NTASKS pp01_daint_copy_from_mist.sh IFS_9
#srun -n $SLURM_NTASKS pp01_daint_copy_from_mist.sh IFS_4
#srun -n $SLURM_NTASKS pp01_daint_copy_from_mist.sh GEOS_3
#srun -n $SLURM_NTASKS pp01_daint_copy_from_mist.sh ARPEGE-NH_2.5
#srun -n $SLURM_NTASKS pp01_daint_copy_from_mist.sh FV3_3.25
###DONE


echo -e "$SLURM_JOB_NAME finished on $(date)\n"


