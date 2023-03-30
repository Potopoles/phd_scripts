#!/bin/bash -l
#
#SBATCH --job-name="cp sim"
#SBATCH --time=23:30:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --account='pr133'
#SBATCH --constraint=gpu
#SBATCH --partition=xfer
#SBATCH --output=bOut/cout0
#SBATCH --error=bOut/cerr0

#module unload xalt

echo -e "$SLURM_JOB_NAME started on $(date):\n $command $1 $2\n"

####### COPY simulation output
###############################################################################
#year=2010
#month=12
#day=01
#
#sim_names=(SA_3_ctrl)
#sim_names=(SA_3_pgw)
#sim_names=(SA_3_itcz_pgw)
#sim_names=(SA_3_pgw2)
#sim_names=(SA_3_pgw3)
##sim_names=(SA_3_itcz_pgw2)
##sim_names=(SA_3_pgw_hmo3)
##sim_names=(SA_3_ctrl SA_3_pgw)
#
#for sim_name in ${sim_names[@]}; do
#    srun -n $SLURM_NTASKS copy_sim.sh $year$month$day $sim_name
#done




##### COPY from project to compress cosmo
#############################################################################
#sim_names=(SA_3_pgw SA_3_ctrl)
sim_names=(\
    SA_3_pgw3 \
    SA_3_ctrl \
)
years=(2006 2007 2008 2009 2010)
#years=(2006 2007 2008)
#years=(2006)
#years=(2007)
#years=(2008)
#years=(2009)
#years=(2010)
#years=(2015)
var_grps=(1h_2D 1h_2D_cg 3h_3D 30min_water 3h_3D_cloud 24h)
#var_grps=(3h_3D)
#var_grps=(3h_3D_zlev 30min_water 3h_3D_cloud 24h)
#var_grps=(1h_2D_cg)
selector=lffd*
for sim_name in ${sim_names[@]}; do
    echo $sim_name
    for year in ${years[@]}; do
        echo "   " $year
        for var_grp in ${var_grps[@]}; do
            echo $var_grp
            #src_path=/project/pr133/heimc/data/cosmo_out/$sim_name/lm_c/$var_grp/$year
            #targ_path=/scratch/snx3000/heimc/data/compr_cosmo/$sim_name/lm_c/$var_grp/$year

            src_path=/scratch/snx3000/heimc/data/compr_cosmo/$sim_name/lm_c/$var_grp/$year
            targ_path=/scratch/snx3000/heimc/data/compr_cosmo2/$sim_name/lm_c/$var_grp/$year
            mkdir -p $targ_path
            echo copy from $src_path to $targ_path
            cp -ur $src_path/$selector $targ_path/.
        done
    done
done


echo -e "$SLURM_JOB_NAME finished on $(date)\n"
