#!/bin/bash

#arg 1: njobs
#arg 2: variable
#arg 3: recompute
#arg 4: panel label
#arg 5: domain


domain=full
#domain=Cu
#domain=Sc
#domain=St

coarse_sims=(ERA5_31 COSMO_12 NICAM_7 ICON_10 IFS_9)
coarse_sims_agg=ERA5_31,COSMO_12,NICAM_7,ICON_10,IFS_9

main_sims=(COSMO_4.4 COSMO_2.2 NICAM_3.5 SAM_4 ICON_2.5 \
           UM_5 MPAS_3.75 IFS_4 GEOS_3 ARPEGE-NH_2.5 FV3_3.25 ERA5_31)
main_sims=(COSMO_4.4)
main_sims_agg=COSMO_2.2,NICAM_3.5,SAM_4,ICON_2.5,UM_5,MPAS_3.75,IFS_4,GEOS_3,ARPEGE-NH_2.5,FV3_3.25,ERA5_31
main_sims_agg=COSMO_2.2,NICAM_3.5,SAM_4,ICON_2.5,MPAS_3.75,IFS_4,GEOS_3,ARPEGE-NH_2.5,FV3_3.25,ERA5_31

njobs=18
#njobs=15
njobs=12
#njobs=6
#njobs=4
#njobs=3
#njobs=1


volumes=(total above below)
volumes_agg=total,above,below

recompute=1

comp_modes=(tend_edge tend_vol mean_vol)
#comp_modes=(tend_edge tend_vol)
#comp_modes=(mean_vol)

if [ "$recompute" == 0 ]; then
    model_keys=$coarse_sims_agg
    model_keys=$main_sims_agg
else
    model_keys=${coarse_sims[@]}
    model_keys=${main_sims[@]}
fi


#model_keys=COSMO_4.4,COSMO_2.2
#model_keys=(COSMO_4.4 COSMO_2.2)
#model_keys=(NICAM_3.5)
#model_keys=(SAM_4)
#model_keys=(ICON_2.5)
#model_keys=(UM_5 MPAS_3.75)
#model_keys=(UM_5)
#model_keys=(IFS_4)
#model_keys=(GEOS_3)
#model_keys=(ARPEGE-NH_2.5)
#model_keys=(FV3_3.25)

main_var_names=(POTT QV RHO)
main_var_names=(POTT QV)
main_var_names=(POTT)
#main_var_names=(QV)
main_var_names=(RHO)


for main_var_name in ${main_var_names[@]}; do
    echo $main_var_name
for model_key in ${model_keys[@]}; do
    echo $model_key
    if [ "$recompute" == 0 ]; then
        for volume in ${volumes[@]}; do
            echo $volume
            python 11_bulk.py $njobs $main_var_name $recompute a. $domain $model_key $volume dummy_dummy
        done
    else
        for comp_mode in ${comp_modes[@]}; do
            python 11_bulk.py $njobs $main_var_name $recompute a. $domain $model_key $volumes_agg $comp_mode
        done
    fi
done
done


