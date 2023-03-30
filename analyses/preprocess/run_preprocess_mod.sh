#!/bin/bash

n_par=18
#n_par=1

mem_keys=(
    ACCESS-CM2 \ 
    ACCESS-ESM1-5 \ 
    AWI-CM-1-1-MR \ 
    #CAMS-CSM1-0 \
    #BCC-ESM1 \
    CAMS-CSM1-0 \
    CanESM5 \ 
    #CAS-ESM2-0 \
    CESM2 \ 
    #CESM2-FV2 \ 
    CESM2-WACCM \ 
    #CESM2-WACCM-FV2 \ 
    #CIESM \ 
    CMCC-CM2-SR5 \ 
    CMCC-ESM2 \ 
    CNRM-CM6-1 \ 
    CNRM-CM6-1-HR \ 
    CNRM-ESM2-1 \
    E3SM-1-1 \ 
    EC-Earth3 \ 
    EC-Earth3-CC \ 
    EC-Earth3-Veg \ 
    FGOALS-f3-L \ 
    FGOALS-g3 \ 
    GFDL-CM4 \ 
    GFDL-ESM4 \ 
    GISS-E2-1-G \
    #GISS-E2-1-H \
    HadGEM3-GC31-LL \
    #HadGEM3-GC31-MM \
    #IITM-ESM \
    INM-CM4-8 \ 
    INM-CM5-0 \ 
    IPSL-CM6A-LR \ 
    #KACE-1-0-G \
    #KIOST-ESM \
    #MCM-UA-1-0 \
    MIROC6 \ 
    MIROC-ES2L \
    MPI-ESM1-2-HR \ 
    MPI-ESM1-2-LR \ 
    MRI-ESM2-0 \ 
    NorESM2-LM \ 
    NorESM2-MM \ 
    TaiESM1 \ 
    UKESM1-0-LL \ 
)


mem_keys=(
    ACCESS-CM2 \ 
    ACCESS-ESM1-5 \ 
    CAMS-CSM1-0 \
    CanESM5 \ 
    CESM2 \ 
    CESM2-WACCM \ 
    CMCC-CM2-SR5 \ 
    CMCC-ESM2 \ 
    CNRM-CM6-1 \ 
    CNRM-ESM2-1 \
    E3SM-1-1 \ 
    FGOALS-f3-L \ 
    FGOALS-g3 \ 
    GFDL-CM4 \ 
    GFDL-ESM4 \ 
    GISS-E2-1-G \
    HadGEM3-GC31-LL \
    MIROC6 \ 
    MIROC-ES2L \
    #MPI-ESM1-2-HR \ 
    MPI-ESM1-2-LR \ 
    MRI-ESM2-0 \ 
    NorESM2-LM \ 
    NorESM2-MM \ 
    TaiESM1 \ 
    UKESM1-0-LL \ 

)

scenarios=(
    #historical \ 
    ssp585 \ 
    ##ssp245 \ 
)

var_names=(
    #SWDTOA \ 
    #LWUTOA \ 
    #CLWUTOA \ 
    #T2M \ 
    #SLHFLX \ 
    #CLDF \ 
    #U \ 
    #V \ 
    #T \ 
    ##QV \ 
    #RH \ 
    #W \ 
    #CLCT \ 
    #ALT \ 
    #P \ 
    #LWUTOA \ 
    #PP \ 
    TSURF \ 
)

for mem_key in ${mem_keys[@]} 
do
    echo $mem_key
    for scenario in ${scenarios[@]} 
    do
        echo $mem_key
        echo $scenario
        for var_name in ${var_names[@]} 
        do
            echo $mem_key
            echo $scenario
            echo $var_name
            nice python preprocess_mod.py -p $n_par -m ${mem_key}_${scenario} $var_name
        done
    done
done
