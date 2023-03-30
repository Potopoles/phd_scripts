#!/bin/bash

PROJ_DATA_DIR="heimc@ela.cscs.ch:/project/pr04/heimc"
SCRA_DATA_DIR=/net/o3/hymet_nobackup/heimc/data
MODEL_NC_SEL=lffd2006*
SIM_NAMES=(MScTh)
#VAR_GROUPS=(mlev zlev const)
VAR_GROUPS=(zlev mlev)
VAR_GROUPS=(zlev)
MODELS=(RAW4 SM4 RAW2 SM2 RAW1 SM1)
MODELS=(SM4 RAW2 SM2 RAW1 SM1)
MODELS=(RAW4)

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
                proj_dir=$PROJ_DATA_DIR/data/cosmo_out/$sim_name/$model/4_lm_f/output/zlev
                scp $proj_dir/lffd2006071100c.nc $scra_dir
            elif [ "$var_grp" == "zlev" ]
            then
                #proj_dir=$PROJ_DATA_DIR/01_rawData/topocut/$model
                #scp $proj_dir/${MODEL_NC_SEL}z.nc $scra_dir
                proj_dir=$PROJ_DATA_DIR/data/cosmo_out/$sim_name/$model/4_lm_f/output/$var_grp
                scp $proj_dir/${MODEL_NC_SEL}z.nc $scra_dir
            elif [ "$var_grp" == "mlev" ]
            then
                proj_dir=$PROJ_DATA_DIR/data/cosmo_out/$sim_name/$model/4_lm_f/output/$var_grp
                scp $proj_dir/${MODEL_NC_SEL}[0-9].nc $scra_dir
            fi
        done
    done
done
