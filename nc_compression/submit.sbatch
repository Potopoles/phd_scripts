#!/bin/bash -l
#SBATCH --job-name="cmpr"
#SBATCH --time=23:30:00
#SBATCH --cpus-per-task=12
#SBATCH --partition=normal
#SBATCH --ntasks=1
#SBATCH --account='pr133'
#SBATCH --constraint=gpu
#SBATCH --output=bOut/out0
#SBATCH --error=bOut/err0

source ~/phd_scripts/load_modules_daint.sh
module load CDO

sim_names=(SA_3_ctrl/lm_c)
#sim_names=(SA_3_pgw/lm_c)
sim_names=(SA_3_pgw2/lm_c)
sim_names=(SA_3_pgw3/lm_c)
#sim_names=(SA_3_itcz_pgw/lm_c)

#sim_names=(SA_3_ctrl/lm_c SA_3_pgw/lm_c)

## COSMO output groups to compress
output_groups=1h_2D,1h_2D_cg,30min_water,3h_3D,3h_3D_cloud,24h
#output_groups=1h_2D_cg
#output_groups=3h_3D
#output_groups=3h_3D_cloud
#output_groups=3h_3D,3h_3D_cloud,24h
#output_groups=30min_water
#output_groups=3h_3D_cloud
#output_groups=3h_3D_cloud_NATIVE

run_coarse_grain=0
run_compression=1

first_year=2010
first_month=01
first_day=01
first_hour=00
first_min=30

last_year=2011
last_month=01
last_day=01
last_hour=00
last_min=00


first_date=${first_year}${first_month}${first_day}${first_hour}${first_min}
last_date=${last_year}${last_month}${last_day}${last_hour}${last_min}


echo -e "$SLURM_JOB_NAME started on $(date):\n $command $1 $2\n"

#srun -c $SLURM_CPUS_PER_TASK python -u split_output_1h_2D.py \
#                -p $SLURM_CPUS_PER_TASK 2009

for sim_name in ${sim_names[@]}; do
    echo $sim_name
    srun -c $SLURM_CPUS_PER_TASK python -u run_compression.py \
                    -p $SLURM_CPUS_PER_TASK $sim_name -o $output_groups \
                    -f $first_date -l $last_date \
                    -c $run_compression -g $run_coarse_grain
done

echo -e "$SLURM_JOB_NAME finished on $(date)\n"


