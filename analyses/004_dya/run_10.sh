#!/bin/bash

#arg 1: njobs
#arg 2: variable
#arg 3: recompute
#arg 4: panel label
#arg 5: domain

#njobs=21
njobs=15
njobs=12
#njobs=4
#njobs=3
#njobs=1

recompute=0

domain=full
#domain=Cu
#domain=Sc
#domain=St

main_sims=ERA5_31,COSMO_4.4,COSMO_2.2,NICAM_3.5,SAM_4,ICON_2.5,UM_5,MPAS_3.75,IFS_4,GEOS_3,ARPEGE-NH_2.5,FV3_3.25
#all_sims=ERA5_31,COSMO_12,COSMO_1.1,COSMO_0.5,NICAM_7,ICON_10,MPAS_7.5,IFS_9,COSMO_4.4,COSMO_2.2,NICAM_3.5,SAM_4,ICON_2.5,UM_5,MPAS_3.75,IFS_4,GEOS_3,ARPEGE-NH_2.5,FV3_3.25
all_sims=ERA5_31,COSMO_12,NICAM_7,ICON_10,MPAS_7.5,IFS_9,COSMO_4.4,COSMO_2.2,NICAM_3.5,SAM_4,ICON_2.5,UM_5,MPAS_3.75,IFS_4,GEOS_3,ARPEGE-NH_2.5,FV3_3.25



#mem_keys=ERA5_31
mem_keys=$main_sims


python 10_olr_bias.py $njobs $recompute a. $domain $mem_keys
