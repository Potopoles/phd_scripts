#!/bin/bash

base_dir=/scratch/snx3000/heimc/data

models=(NICAM_7 NICAM_3.5 \
        SAM_4 \
        ICON_10 ICON_2.5 \
        UM_5 \
        MPAS_7.5 MPAS_3.75 \
        IFS_9 IFS_4 \
        GEOS_3 \
        ARPEGE-NH_2.5 \
        FV3_3.25)

models=(IFS_9)


vars=(W H SWUTOA SWNDTOA TQC U10M V10M SLHFLX SSHFLX \
      LWUTOA QV QC T SWDSFC PP T2M)
vars=(SWUTOA SWNDTOA TQC)

case_names=(DYAMOND_2)


my_dates=()
for i in {0..40}; do
#for i in {0..1}; do
    #echo $(date -I -d "2016-08-01 +$i days" )
    my_dates+=($(date "+%Y%m%d" -d "2016-08-01 +$i days"))
done


for model in  ${models[@]}; do
    echo $model

    for case_name in ${case_names[@]}; do
        echo '   '$case_name

        for var in ${vars[@]}; do 
            echo '       '$var

            src_dir=$base_dir/simulations/$model/$case_name/native/$var
            dest_dir=$base_dir/simulations/$model/$case_name/daily/$var

            mkdir -p $dest_dir

            for this_date in ${my_dates[@]}; do
                #echo '          '$this_date
                src_files=$src_dir/${var}_${this_date}*.nc
                cdo -O mergetime $src_files $dest_dir/${var}_${this_date}.nc
            done
        done
    done
done

