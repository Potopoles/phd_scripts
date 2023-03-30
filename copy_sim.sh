#!/bin/bash
# copy model output from scratch dir 'wd' to project storage dir
# also compress nc files using nczip

# arguments
# 1st: date
start_date=$1
sim_name=$2


proj_cosmo_out_dir=/project/pr133/heimc/data/cosmo_out
scr_lmp_dir=/scratch/snx3000/heimc/lmp
scr_compr_dir=/scratch/snx3000/heimc/data/compr_cosmo

copy_lm_c=1
copy_lm_f=0

copy_restart=1
copy_const=1
copy_debug=1
copy_output=1
copy_output_to_project=0
copy_output_to_compr=1

selector=lffd*
#init_date="${year:2:4}"${month}${day}00
init_date=$(date -d $start_date +'%y%m%d%H')

## restart  files
restart_file_bin_lm_c=$(date -d "$start_date +1 month" +lrfd'%Y%m%d%H%M%S'o)
restart_file_bc_lm_c=$(date -d "$start_date +1 month -3 hour" +lbfd'%Y%m%d%H%M%S'.nc)

year=$(date -d $start_date +'%Y')

echo $init_date
echo $restart_file_bin_lm_c
echo $restart_file_bc_lm_c
echo $year

#var_groups=(1h_water 1h_2D 1h_rad 1h_clsky 3h_3D_zlev 30min_water 3h_totwat 24h)
var_groups=(1h_2D_cg 3h_3D 3h_3D_cloud 1h_2D 30min_water 24h)
#var_groups=(1h_2D_cg)
#var_groups=(3h_3D)
#var_groups=(1h_2D)
#var_groups=(30min_water)
#var_groups=(3h_3D_cloud)
#var_groups=(24h)


lm_c_pr=lm_c

# name of lm_c/lm_f subdirectories in project/cosmo_out
#lm_f_pr=lm_f
#lm_c_pr=lm_c



echo $sim_name
echo $lm_c_pr

sim_scr_wd_dir=$scr_lmp_dir/wd/${init_date}_$sim_name
sim_scr_cache_dir=$scr_lmp_dir/cache/$sim_name
sim_scr_compr_dir=$scr_compr_dir/$sim_name
sim_pr_dir=$proj_cosmo_out_dir/$sim_name
echo $sim_pr_dir

#mkdir -p $sim_pr_dir/$lm_c_pr

if (( $copy_lm_c == 1 )); then
    echo '############### LM C ###############'
    mkdir -p $sim_pr_dir/$lm_c_pr

    # copy restart files
    if (( $copy_restart == 1 )); then
        echo '##### copy restart'
        mkdir -p $sim_pr_dir/$lm_c_pr/restart 
        cp -u $sim_scr_cache_dir/lm_c/restart/$restart_file_bin_lm_c \
                                    $sim_pr_dir/$lm_c_pr/restart
        cp -u $sim_scr_cache_dir/lm_c/restart/$restart_file_bc_lm_c \
                                    $sim_pr_dir/$lm_c_pr/restart
        #ls $sim_pr_dir/$lm_c_pr/restart
        echo ""
    fi


    # copy constant fields
    if (( $copy_const == 1 )); then
        echo '##### copy constant fields'
        # model output
        cp -u $sim_scr_wd_dir/lm_coarse/lffd*c.nc $sim_pr_dir/$lm_c_pr
    fi


    # copy debug
    if (( $copy_debug == 1 )); then
        echo '##### copy debug'
        debug_dir=$sim_pr_dir/$lm_c_pr/debug/$init_date
        mkdir -p $debug_dir
        cp $sim_scr_wd_dir/output/YU* $debug_dir
        cp $sim_scr_wd_dir/debug/stdeoJob* $debug_dir
    fi


    # copy model output files
    if (( $copy_output == 1 )); then
        echo '##### copy output fields'
        for group in ${var_groups[@]}; do
            echo '    '$group

            # scratch lmp/wd directory of output group
            lm_c_scr_sim=$sim_scr_wd_dir/lm_coarse/$group
            # project storage directory of output group
            lm_c_pr_store=$sim_pr_dir/$lm_c_pr/$group/$year
            # compression directory of output group
            lm_c_scr_compr=$sim_scr_compr_dir/$lm_c_pr/$group/$year

            # copy to project storage
            if (( $copy_output_to_project == 1 )); then
                echo '       copy to project'
                mkdir -p $lm_c_pr_store
                cp -u $lm_c_scr_sim/$selector $lm_c_pr_store
            fi

            # copy to scratch for compression
            if (( $copy_output_to_compr == 1 )); then
                echo '       copy to compression'
                mkdir -p $lm_c_scr_compr
                cp -u $lm_c_scr_sim/$selector $lm_c_scr_compr
            fi
        done
    fi
    echo '####################################'
fi



#########################################################################
#########################################################################


if (( $copy_lm_f == 1 )); then
    echo '############### LM F ###############'
    mkdir -p $sim_pr_dir/$lm_f_pr

    # copy restart files
    if (( $copy_restart == 1 )); then
        echo '##### copy restart'
        mkdir -p $sim_pr_dir/$lm_f_pr/restart 
        cp -u $sim_scr_cache_dir/lm_f/restart/$restart_file_bin_lm_f \
                                    $sim_pr_dir/$lm_f_pr/restart
        cp -u $sim_scr_cache_dir/lm_f/restart/$restart_file_bc_lm_f \
                                    $sim_pr_dir/$lm_f_pr/restart
        #ls $sim_pr_dir/$lm_f_pr/restart
        echo ""
    fi


    # copy constant fields
    if (( $copy_const == 1 )); then
        echo '##### copy constant fields'
        # model output
        cp -u $sim_scr_wd_dir/lm_fine/lffd*c.nc $sim_pr_dir/$lm_f_pr
    fi


    # copy debug
    if (( $copy_debug == 1 )); then
        echo '##### copy debug'
        debug_dir=$sim_pr_dir/$lm_f_pr/debug/$init_date
        mkdir -p $debug_dir
        cp $sim_scr_wd_dir/output/YU* $debug_dir
        cp $sim_scr_wd_dir/debug/stdeoJob* $debug_dir
    fi


    # copy model output files
    if (( $copy_output == 1 )); then
        echo '##### copy output fields'
        for group in ${var_groups[@]}; do
            echo '    '$group

            # scratch lmp/wd directory of output group
            lm_f_scr_sim=$sim_scr_wd_dir/lm_fine/$group
            # project storage directory of output group
            lm_f_pr_store=$sim_pr_dir/$lm_f_pr/$group/$year
            # compression directory of output group
            lm_f_scr_compr=$sim_scr_compr_dir/$lm_f_pr/$group/$year

            # copy to project store
            if (( $copy_output_to_project == 1 )); then
                echo '       copy to project'
                mkdir -p $lm_f_pr_store
                cp -u $lm_f_scr_sim/$selector $lm_f_pr_store
            fi

            # copy to scratch for compression
            if (( $copy_output_to_compr == 1 )); then
                echo '       copy to compression'
                mkdir -p $lm_f_scr_compr
                cp -u $lm_f_scr_sim/$selector $lm_f_scr_compr
            fi
        done
    fi
    echo '####################################'
fi

