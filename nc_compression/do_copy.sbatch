#!/bin/bash -l
#
#SBATCH --job-name="cp cmpressed"
#SBATCH --time=23:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --account='pr133'
#SBATCH --constraint=gpu
#SBATCH --partition=xfer
#SBATCH --output=bOut/cout0
#SBATCH --error=bOut/cerr0

#source ~/phd_scripts/load_modules_daint.sh
#module unload xalt

echo -e "$SLURM_JOB_NAME started on $(date):\n $command $1 $2\n"

years=(2006 2007 2008 2009 2010)
#years=(2006)
#years=(2009 2010)
#years=(2010)
## simulation name


sim_names=(
    #gulf/lm_c/
    #gulf/lm_f/
    #SA_3_ctrl/lm_c/
    #SA_3_pgw/lm_c/
    #SA_3_pgw2/lm_c/
    SA_3_pgw3/lm_c/
    #SA_3_pgw_300hPa_rdheight2/lm_c/
    #SA_3_ctrl_rdheight2/lm_c/
    )


direction_proj_to_scr=0
scratch_dir=/scratch/snx3000/heimc/data/compr_cosmo
#scratch_dir=/scratch/snx3000/heimc/data/coarse_grain
project_dir=/project/pr133/heimc/data/cosmo_out


for sim_name in ${sim_names[@]}; do
    echo $sim_name
    for year in ${years[@]}; do
        echo "  "$year

        # COSMO output groups to compress
        output_groups=(1h_2D/$year 1h_2D_cg/$year 30min_water/$year \ 
                       3h_3D/$year 3h_3D_cloud/$year 24h/$year)
        #output_groups=(1h_2D_cg/$year)
        #output_groups=(3h_3D_cloud_NATIVE/$year)

        for out_group in ${output_groups[@]}; do
            echo "     "$out_group

            ## project to scratch
            if [ $direction_proj_to_scr -eq 1 ]
            then
                mkdir -p $scratch_dir/$sim_name/$out_group
                rsync -ru $project_dir/$sim_name/$out_group/* \
                            $scratch_dir/$sim_name/$out_group/.
            else
                # scratch to project
                mkdir -p $project_dir/$sim_name/$out_group
                rsync -ru $scratch_dir/$sim_name/$out_group/* \
                            $project_dir/$sim_name/$out_group/.
            fi

        done
    done
    echo ""
done

echo -e "$SLURM_JOB_NAME finished on $(date)\n"


