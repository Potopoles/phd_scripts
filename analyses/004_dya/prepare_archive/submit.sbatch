#!/bin/bash -l
#
#SBATCH --job-name="tar dya"
#SBATCH --time=23:30:00
#SBATCH --cpus-per-task=12
#SBATCH --partition=normal
#SBATCH --output=bOut/out1
#SBATCH --error=bOut/err1
#SBATCH --ntasks=1
#SBATCH --account='pr94'
#SBATCH --constraint=gpu

source ../load_modules_daint.sh
echo -e "$SLURM_JOB_NAME started on $(date):\n $command $1 $2\n"

#year=2016
##sim_tag=SA_12
##sim_tag=SA_4_2
##sim_tag=SA_4_1
#sim_tag=SA_4_05
#sub_dir=lm_f_DYA
#var_grps=(3h_3D_zlev 1h_2D)
##var_grp=3h_3D_zlev
##var_grp=1h_2D
#for var_grp in ${var_grps[@]}; do
#    echo $var_grp
#    data_dir=/scratch/snx3000/heimc/data/archive/$sim_tag/$sub_dir/$var_grp/$year
#    for file_name in $data_dir/*; do
#        echo "    " $file_name
#        # 3h_3D_zlev var group
#        if [ "$var_grp" = "3h_3D_zlev" ]; then
#            ncks -d altitude,0,20 -v QC,QV,P,U,V,W,T -O $file_name $file_name
#        # 1h_2D var group
#        elif [ "$var_grp" = "1h_2D" ]; then
#            ncks -v ALHFL_S,TQV,ASOB_T,ASOD_T,ATHB_T -O $file_name $file_name
#        fi
#    done
#done




#data_dir=/scratch/snx3000/heimc/data/archive
#tar -cvf $data_dir/cosmo_out.tar $data_dir/SA_*

data_dir=/scratch/snx3000/heimc/data/archive
tar -cvf $data_dir/dyamond_out.tar $data_dir/dyamond

echo -e "$SLURM_JOB_NAME finished on $(date)\n"


