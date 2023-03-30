#!/bin/bash

#arg 1: njobs
#arg 2: variable
#arg 3: recompute
#arg 4: panel label
#arg 5: domain

plot_dir=/net/o3/hymet_nobackup/heimc/plots/004_dyamond/02_profiles

#njobs=21
njobs=18
#njobs=12
#njobs=9
#njobs=6
#njobs=4
#njobs=4
#njobs=1

recompute=0

domain=full
#domain=Cu
#domain=Sc
#domain=St


#python 02_profiles.py $njobs T $recompute a. $domain 0
#python 02_profiles.py $njobs TNORMI $recompute d. $domain 0
#python 02_profiles.py $njobs QC $recompute b. $domain 1
#python 02_profiles.py $njobs QCNORMI $recompute e. $domain 0
#python 02_profiles.py $njobs QV $recompute c. $domain 0
#python 02_profiles.py $njobs QVNORMI $recompute f. $domain 0


#################### PAPER FIGURES DYAMOND
####### Fig. 7 DYAMOND
python 02_profiles.py $njobs T $recompute a. $domain 0
python 02_profiles.py $njobs TNORMI $recompute d. $domain 0
python 02_profiles.py $njobs QC $recompute b. $domain 1
python 02_profiles.py $njobs QCNORMI $recompute b. $domain 1
if [ $recompute == 0 ]
then
    mv $plot_dir/SEA_Sc/prof_dom_SEA_Sc_dya_main_QCNORMI.jpg \
            $plot_dir/SEA_Sc/prof_dom_SEA_Sc_dya_main_QCNORMI_label_b.jpg
    python 02_profiles.py $njobs QCNORMI $recompute e. $domain 0
fi
python 02_profiles.py $njobs QV $recompute c. $domain 0
python 02_profiles.py $njobs QVNORMI $recompute f. $domain 0
#exit 1

######### Fig. 8
python 02_profiles.py $njobs W $recompute a. $domain 1
python 02_profiles.py $njobs WNORMI $recompute c. $domain 0 
## turn on SQRTMEAN
python 02_profiles.py $njobs WTURB $recompute b. $domain 0
#python 02_profiles.py $njobs WTURBNORMI $recompute d. $domain 0
python 02_profiles.py $njobs WTURBNORMISCI $recompute d. $domain 0
## turn off SQRTMEAN
#python 02_profiles.py $njobs UVFLXDIV $recompute b. $domain 1
#python 02_profiles.py $njobs UVFLXDIVNORMI $recompute e. $domain 0
#python 02_profiles.py $njobs AW $recompute c. $domain 0
#python 02_profiles.py $njobs AWNORMI $recompute f. $domain 0
#exit 1

######## Fig. 9 
python 02_profiles.py $njobs DIABHNORMI $recompute a. $domain 0
python 02_profiles.py $njobs POTTDIVMEANNORMI $recompute c. $domain 0
python 02_profiles.py $njobs POTTDIVTURBNORMI $recompute d. $domain 0






##################### PAPER FIGURES COSMO
######### Fig. 7
#python 02_profiles.py $njobs T $recompute g. $domain 0
#python 02_profiles.py $njobs TNORMI $recompute j. $domain 0
#python 02_profiles.py $njobs QC $recompute h. $domain 1
#python 02_profiles.py $njobs QCNORMI $recompute k. $domain 0
#python 02_profiles.py $njobs QV $recompute i. $domain 0
#python 02_profiles.py $njobs QVNORMI $recompute l. $domain 0
#
#
########## Fig. 8
#python 02_profiles.py $njobs W $recompute e. $domain 1
#python 02_profiles.py $njobs WNORMI $recompute g. $domain 0 
### turn on SQRTMEAN
#python 02_profiles.py $njobs WTURB $recompute f. $domain 0
#python 02_profiles.py $njobs WTURBNORMI $recompute h. $domain 0
#python 02_profiles.py $njobs WTURBNORMISCI $recompute h. $domain 0
## turn off SQRTMEAN
#python 02_profiles.py $njobs UVFLXDIV $recompute b. $domain 1
#python 02_profiles.py $njobs UVFLXDIVNORMI $recompute e. $domain 0
#python 02_profiles.py $njobs AW $recompute c. $domain 0
#python 02_profiles.py $njobs AWNORMI $recompute f. $domain 0

######### Fig. 9 
#python 02_profiles.py $njobs DIABHNORMI $recompute a. $domain 0
#python 02_profiles.py $njobs POTTDIVMEANNORMI $recompute c. $domain 0
#python 02_profiles.py $njobs POTTDIVTURBNORMI $recompute d. $domain 0











########## OLD STUFF

######### Fig. 9 
#python 02_profiles.py $njobs DIABH $recompute a. $domain 0
#python 02_profiles.py $njobs DIABHNORMI $recompute a. $domain 0
#python 02_profiles.py $njobs POTTDIVMEANNORMI $recompute c. $domain 0
#python 02_profiles.py $njobs POTTDIVTURBNORMI $recompute d. $domain 0
#python 02_profiles.py $njobs POTTHDIV $recompute a. $domain 0
#python 02_profiles.py $njobs POTTVDIV $recompute b. $domain 1
#python 02_profiles.py $njobs POTTHDIVNORMI $recompute d. $domain 0 
#python 02_profiles.py $njobs POTTVDIVNORMI $recompute e. $domain 0


#################### EXTRA FIGURES
#python 02_profiles.py $njobs DIABH $recompute a. $domain 0
#python 02_profiles.py $njobs POTTHDIV $recompute a. $domain 0
#python 02_profiles.py $njobs POTTVDIV $recompute b. $domain 1
#python 02_profiles.py $njobs POTTHDIVNORMI $recompute d. $domain 0 
#python 02_profiles.py $njobs POTTVDIVNORMI $recompute e. $domain 0
#python 02_profiles.py $njobs RHL $recompute a. $domain 0
#python 02_profiles.py $njobs RHLNORMI $recompute b. $domain 0
#python 02_profiles.py $njobs POTT $recompute a. $domain 0
#python 02_profiles.py $njobs POTTNORMI $recompute b. $domain 0
#python 02_profiles.py $njobs POTTVDIVMEAN $recompute a. $domain 1
#python 02_profiles.py $njobs POTTVDIVTURB $recompute b. $domain 0
#python 02_profiles.py $njobs POTTHDIVMEAN $recompute a. $domain 1
#python 02_profiles.py $njobs POTTHDIVTURB $recompute b. $domain 0
#python 02_profiles.py $njobs POTTVDIVMEANNORMI $recompute c. $domain 0
#python 02_profiles.py $njobs POTTVDIVTURBNORMI $recompute d. $domain 0
#python 02_profiles.py $njobs POTTHDIVMEANNORMI $recompute c. $domain 0
#python 02_profiles.py $njobs POTTHDIVTURBNORMI $recompute d. $domain 0
##exit 1
