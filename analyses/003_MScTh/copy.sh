#!/bin/bash -   
#title          :copy.sh
#description    :Copy data from model to scratch
#author         :Christoph Heim
#date           :20190401
#version        :1.00   
#usage          :./copy.sh
#notes          :       
#bash_version   :4.3.48(1)-release
#============================================================================

source setenv.sh

######### MODEL DATA
for sim_name in ${SIM_NAMES[@]}; do
    echo $sim_name
    for model in ${MODELS[@]}; do
        echo '  '$model
        for var_grp in ${VAR_GROUPS[@]}; do
            echo '    '$var_grp
            scra_dir=$SCRA_DATA_DIR/cosmo_out/$sim_name/$model/$var_grp
            mkdir -p $scra_dir
            if [ "$var_grp" == "const" ]
            then
                proj_dir=$PROJ_DATA_DIR/cosmo_out/$sim_name/$model/4_lm_f/output/zlev
                cp -u $proj_dir/lffd2006071100c.nc $scra_dir
            elif [ "$var_grp" == "zlev" ]
            then
                proj_dir=$PROJ_DATA_DIR/cosmo_out/$sim_name/$model/4_lm_f/output/$var_grp
                cp -u $proj_dir/${MODEL_NC_SEL}z.nc $scra_dir
            elif [ "$var_grp" == "mlev" ]
            then
                proj_dir=$PROJ_DATA_DIR/cosmo_out/$sim_name/$model/4_lm_f/output/$var_grp
                cp -u $proj_dir/${MODEL_NC_SEL}.nc $scra_dir
            fi
        done
    done
done

########## SATELLITE DATA
#for sat in ${SATS[@]}; do
#    echo $sat
#    for var in ${SAT_VARS[@]}; do
#        echo '  '$var 
#        proj_dir=$PROJ_DATA_DIR/analyses/$ANA_NAME/${var}_${sat}
#        scra_dir=$SCRA_DATA_DIR/analyses/$ANA_NAME/$sat
#        mkdir -p $scra_dir
#        cp -u $proj_dir/$SAT_NC_SEL $scra_dir
#    done
#done
