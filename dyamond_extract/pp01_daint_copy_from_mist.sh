#!/bin/bash

source_base_dir=b380876@mistral.dkrz.de:/work/ka1081/2019_06_Hackathon_Mainz/christoph_heim
dest_base_dir=/project/pr04/heimc/data

models=(NICAM_7 NICAM_3.5 \
        SAM_4 \
        ICON_10 ICON_2.5 \
        UM_5 \
        MPAS_7.5 MPAS_3.75 \
        IFS_9 IFS_4 \
        GEOS_3 \
        ARPEGE-NH_2.5 \
        FV3_3.25)

models=($1)

vars=(QV QC T W H U V P \
      HSURF \
      MSLP PS T2M U10M V10M \
      LWUTOA SWUTOA SWNDTOA SWDTOA SWDSFC SWNDSFC SWDIFFUSFC\
      SST SLHFLX SSHFLX \
      TQC TQI TQV
      CLCL CLCT PP PPCONV PPGRID)

vars=(T)
#####################

case_names=(DYAMOND_2)


for model in  ${models[@]}; do
    echo $model

    for case_name in ${case_names[@]}; do
        echo '   '$case_name

        for var in ${vars[@]}; do 
            echo '       '$var

            dest_dir=$dest_base_dir/simulations/$model/$case_name/native/$var
            mkdir -p $dest_dir
            #dest_dir=$dest_base_dir/simulations/$model/$case_name
            #mkdir -p $dest_dir

            source_file=$source_base_dir/newdata/$model/tmp/${var}_*.nc
            #source_file=$source_base_dir/newdata/$model/$case_name/${var}.nc

            echo copy $source_file to $dest_dir

            #scp $source_file $dest_dir
            rsync -u $source_file $dest_dir
        done
        #do not delete here because empty folders are necessary in pp03
        #find $dest_base_dir/simulations/$model/$case_name/native -empty -type d -delete
    done
done

