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
models=(MPAS_3.75)
#models=(NICAM_3.5)


source_base_dir=/scratch/snx3000/heimc/data
dest_base_dir=/project/pr04/heimc/data

vars=(QV QC T W H U V P \
      HSURF \
      MSLP PS T2M U10M V10M \
      LWUTOA SWUTOA SWNDTOA SWDTOA\
      SST SLHFLX SSHFLX \
      TQC TQI TQV
      CLCL CLCT PP PPCONV PPGRID)
vars=(T)


echo copy from $source_base_dir to $dest_base_dir

case_names=(SA DYAMOND_2)

for model in  ${models[@]}; do
    echo $model

    for case_name in ${case_names[@]}; do
        echo '   '$case_name

        for var in ${vars[@]}; do 
            echo '       '$var

            dest_dir=$dest_base_dir/simulations/$model/$case_name/daily/$var
            src_dir=$source_base_dir/simulations/$model/$case_name/daily/$var

            mkdir -p $dest_dir
            cp -u $src_dir/${var}_*.nc $dest_dir
            #cp $src_dir/${var}_*.nc $dest_dir
        done
        find $dest_base_dir/simulations/$model/$case_name/daily -empty -type d -delete
    done
done

