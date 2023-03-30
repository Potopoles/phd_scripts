#!/bin/bash

n_par=12
i_recompute=1


#nice python 00_compute_fields.py -p $n_par T NorESM2-MM_historical
#nice python 00_compute_fields.py -p $n_par QV NorESM2-MM_historical
#nice python 00_compute_fields.py -p $n_par P NorESM2-MM_historical

#nice python org_ana.py -s 3 ana_nls/sp_02_change.py -p $n_par -r $i_recompute
#nice python an_04.py -p $n_par -r $i_recompute


#nice python 00_compute_fields.py -p $n_par T ERA5_gulf
#nice python 00_compute_fields.py -p $n_par P ERA5_gulf
#nice python 00_compute_fields.py -p $n_par QV ERA5_gulf
#nice python 00_compute_fields.py -p $n_par QC ERA5_gulf
#nice python 00_compute_fields.py -p $n_par QI ERA5_gulf
#nice python 00_compute_fields.py -p $n_par U ERA5_gulf
#nice python 00_compute_fields.py -p $n_par V ERA5_gulf
#nice python 00_compute_fields.py -p $n_par W ERA5_gulf

#mod_key=COSMO_3.3_ctrl_rdheight2
#mod_key=COSMO_3.3_pgw_rdheight2
#mod_key=COSMO_3.3_ctrl
#mod_key=COSMO_3.3_pgw
#mod_key=ERA5
#mod_key=MPI-ESM1-2-HR_historical
#mod_key=MPI-ESM1-2-HR_ssp585



###### Reynolds averaging
#mem_keys=(COSMO_3.3_ctrl COSMO_3.3_pgw)
##mem_keys=(COSMO_3.3_pgw)
#for mem_key in ${mem_keys[@]} 
#do
#    echo $mem_key
#    nice python 00_compute_fields.py -p $n_par INVHGT $mem_key
#    nice python 00_compute_fields.py -p $n_par POTTV $mem_key
#    nice python 00_compute_fields.py -p $n_par W $mem_key
#    nice python 00_compute_fields.py -p $n_par QV $mem_key
#    nice python 00_compute_fields.py -p $n_par U $mem_key
#    nice python 00_compute_fields.py -p $n_par V $mem_key
#    nice python 00_compute_fields.py -p $n_par POTT $mem_key
#done


###nice python an_02.py -p $n_par -r $i_recompute CLDFNORMI
###nice python an_04.py -p $n_par -r $i_recompute CLDF_CLDF
#nice python an_02.py -p $n_par -r $i_recompute POTTNORMI
#nice python an_04.py -p $n_par -r $i_recompute POTT_CLDF
#nice python an_02.py -p $n_par -r $i_recompute QVNORMI
#nice python an_04.py -p $n_par -r $i_recompute QV_CLDF
#nice python an_02.py -p $n_par -r $i_recompute RHNORMI
#nice python an_04.py -p $n_par -r $i_recompute compute


mem_keys=(COSMO_3.3_ctrl COSMO_3.3_pgw3)
mem_keys=(COSMO_3.3_pgw)
mem_keys=(COSMO_3.3_pgw3)
#mem_keys=(COSMO_3.3_ctrl)
#mem_keys=(ERA5)
for mem_key in ${mem_keys[@]} 
do
    #nice python 00_compute_fields.py -p $n_par INVHGT $mem_key
    #nice python 00_compute_fields.py -p $n_par LCL $mem_key
    #nice python 00_compute_fields.py -p $n_par POTT $mem_key
    #nice python 00_compute_fields.py -p $n_par RH $mem_key
    #nice python 00_compute_fields.py -p $n_par RHO $mem_key

    #nice python 00_compute_fields.py -p $n_par LTS $mem_key
    #nice python 00_compute_fields.py -p $n_par DQVINV $mem_key

    #nice python 00_compute_fields.py -p $n_par EQPOTT $mem_key

    #nice python 00_compute_fields.py -p $n_par ENTRVSCL $mem_key
    #nice python 00_compute_fields.py -p $n_par LOWCLDBASE $mem_key
    #nice python 00_compute_fields.py -p $n_par TV $mem_key

    #nice python 00_compute_fields.py -p $n_par ZCPTPP $mem_key
    #nice python 00_compute_fields.py -p $n_par PCPTPP $mem_key

    #nice python 00_compute_fields.py -p $n_par ENTR $mem_key

    nice python 00_compute_fields.py -p $n_par dRHdt $mem_key
done




##for year in ${years[@]} 
##do
#    echo $year
#    for var_name in ${var_names[@]} 
#    do
#        echo $var_name
#        for mem_key in ${mem_keys[@]} 
#        do
#            echo $mem_key
#            python 00_compute_fields.py -p $n_par $var_name $mem_key
#        done
#    done
##done
#
