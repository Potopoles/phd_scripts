#!/bin/bash

models=(NICAM_7 NICAM_3.5 \
        SAM_4 \
        ICON_10 ICON_2.5 \
        UM_5 \
        MPAS_7.5 MPAS_3.75 \
        IFS_9 IFS_4 \
        GEOS_3 \
        ARPEGE-NH_2.5 \
        FV3_3.25)
#models=(COSMO_1.1)
#models=(COSMO_2.2)
#models=(COSMO_4.4)
#models=(COSMO_12)

# done:
#models=(NICAM_7)
#models=(ICON_10 \
#        UM_5 \
#        MPAS_7.5 \
#        IFS_9 IFS_4)
models=(NICAM_3.5 \
        SAM_4 \
        MPAS_3.75 \
        GEOS_3
        ICON_2.5)
#models=(FV3_3.25)
#models=(ARPEGE-NH_2.5)
models=(SAM_4)

source_base_dir=/scratch/snx3000/heimc/data
dest_base_dir=/project/pr94/heimc/data
source_base_dir=/project/pr94/heimc/data
dest_base_dir=/scratch/snx3000/heimc/data

vars=(W H SWUTOA SWNDTOA SWDTOA TQC U10M V10M SLHFLX SSHFLX LWUTOA)
vars=(W)
vars=(SWUTOA TQC)

case_names=(DYAMOND_2)
#case_names=(SA)
#case_names=(SA_2lev)

echo copy from $source_base_dir to $dest_base_dir

for model in  ${models[@]}; do
    echo $model

    for case_name in ${case_names[@]}; do
        echo '   '$case_name

        for var in ${vars[@]}; do 
            echo '       '$var

            #dest_dir=$dest_base_dir/simulations/$model/$case_name
            #source_file=$source_base_dir/simulations/$model/$case_name/${var}.nc

            dest_dir=$dest_base_dir/simulations/$model/$case_name/native/$var
            src_dir=$source_base_dir/simulations/$model/$case_name/native/$var

            mkdir -p $dest_dir
            #cp -u $src_dir/${var}_*.nc $dest_dir
            cp $src_dir/${var}_*.nc $dest_dir
        done
    done
done

