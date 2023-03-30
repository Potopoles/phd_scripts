#!/bin/bash

year=2016
#sim_tag=SA_12
sim_tag=SA_4_2
sub_dir=lm_c_DYA
var_grps=(3h_3D_zlev 1h_2D)
#var_grp=3h_3D_zlev
#var_grp=1h_2D
for var_grp in ${var_grps[@]}; do
    echo $var_grp
    data_dir=/scratch/snx3000/heimc/data/archive/$sim_tag/$sub_dir/$var_grp/$year
    for file_name in $data_dir/*; do
        echo "    " $file_name
        # 3h_3D_zlev var group
        if [ "$var_grp" = "3h_3D_zlev" ]; then
            ncks -d altitude,0,20 -v QC,QV,P,U,V,W,T -O $file_name $file_name
        # 1h_2D var group
        elif [ "$var_grp" = "1h_2D" ]; then
            ncks -v ALHFL_S,TQV,ASOB_T,ASOD_T,ATHB_T -O $file_name $file_name
        fi
    done
done
