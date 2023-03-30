#!/bin/bash

#arg 1: njobs
#arg 2: variable
#arg 3: i_recompute
#arg 4: panel label
#arg 5: domain

#plot_dir=/net/o3/hymet_nobackup/heimc/plots/004_dyamond/02_profiles

njobs=18

i_recompute=0
i_save_fig=3

run_mode=SEA_Sc


#python 03_corr.py $njobs $i_save_fig CLCL2 ALBEDO $i_recompute dya_all c. $run_mode
#exit 1
#python 03_corr.py $njobs $i_save_fig TQC ALBEDO $i_recompute dya_all a. $run_mode
#python 03_corr.py $njobs $i_save_fig ALBEDO LWUTOA $i_recompute dya_all a. $run_mode
#python 03_corr.py $njobs $i_save_fig INVHGT ALBEDO $i_recompute dya_all a. $run_mode
#python 03_corr.py $njobs $i_save_fig INVSTRV ALBEDO $i_recompute dya_all a. $run_mode
#python 03_corr.py $njobs $i_save_fig ENTR SLHFLX $i_recompute dya_all a. $run_mode
#python 03_corr.py $njobs $i_save_fig ENTR INVHGT $i_recompute dya_all a. $run_mode
#python 03_corr.py $njobs $i_save_fig ENTR ALBEDO $i_recompute dya_all a. $run_mode


#python 03_corr.py $njobs $i_save_fig POTTFT POTTVFT $i_recompute dya_all a. $run_mode
#python 03_corr.py $njobs $i_save_fig QVFT POTTVFT $i_recompute dya_all a. $run_mode
#python 03_corr.py $njobs $i_save_fig QVFT POTTFT $i_recompute dya_all a. $run_mode


#################### PAPER FIGURES

######### Fig. 4
## turn off turbulence members
#python 03_corr.py $njobs $i_save_fig TQC ALBEDO $i_recompute dya_all a. $run_mode
#if [ $i_recompute == 0 ]
#then
#python 03_corr.py $njobs $i_save_fig TQC ALBEDO $i_recompute dya_main b. $run_mode
#fi
#exit 1

## turn on i_use_obs
#python 03_corr.py $njobs $i_save_fig CLCL2 ALBEDO $i_recompute dya_all c. $run_mode
#if [ $i_recompute == 0 ]; then
#python 03_corr.py $njobs $i_save_fig CLCL2 ALBEDO $i_recompute dya_main d. $run_mode
#fi
#exit 1
### turn off i_use_obs


######### Fig. 5
##exit 1
## turn on i_use_obs
#python 03_corr.py $njobs $i_save_fig ALBEDO LWUTOA $i_recompute dya_all a. $run_mode
#if [ $i_recompute == 0 ]; then
#python 03_corr.py $njobs $i_save_fig ALBEDO LWUTOA $i_recompute dya_main b. $run_mode
#fi
#
#python 03_corr.py $njobs $i_save_fig TQV LWUTOA $i_recompute dya_all c. $run_mode
#if [ $i_recompute == 0 ]; then
#python 03_corr.py $njobs $i_save_fig TQV LWUTOA $i_recompute dya_main d. $run_mode
#fi
#exit 1
## turn off i_use_obs


######### Fig. 7
## turn on turbulence members
#python 03_corr.py $njobs $i_save_fig INVHGT ALBEDO $i_recompute dya_all a. $run_mode
#if [ $i_recompute == 0 ]; then
#python 03_corr.py $njobs $i_save_fig INVHGT ALBEDO $i_recompute dya_main b. $run_mode
#fi
#
##python 03_corr.py $njobs $i_save_fig INVSTR ALBEDO $i_recompute dya_all c. $run_mode
##if [ $i_recompute == 0 ]; then
##python 03_corr.py $njobs $i_save_fig INVSTR ALBEDO $i_recompute dya_main d. $run_mode
##fi
#
#python 03_corr.py $njobs $i_save_fig INVSTRV ALBEDO $i_recompute dya_all c. $run_mode
#if [ $i_recompute == 0 ]; then
#python 03_corr.py $njobs $i_save_fig INVSTRV ALBEDO $i_recompute dya_main d. $run_mode
#fi
#
#python 03_corr.py $njobs $i_save_fig SUBS ALBEDO $i_recompute dya_all e. $run_mode
#if [ $i_recompute == 0 ]; then
#python 03_corr.py $njobs $i_save_fig SUBS ALBEDO $i_recompute dya_main f. $run_mode
#fi




########## Fig. 12
#if [ $i_recompute == 0 ]; then
#python 03_corr.py $njobs $i_save_fig ENTR INVHGT $i_recompute dya_all a. $run_mode
#python 03_corr.py $njobs $i_save_fig ENTR INVHGT $i_recompute dya_main b. $run_mode
#fi
#
### turn off MPAS for recompute
#python 03_corr.py $njobs $i_save_fig ENTR SLHFLX $i_recompute dya_all c. $run_mode
#if [ $i_recompute == 0 ]; then
#python 03_corr.py $njobs $i_save_fig ENTR SLHFLX $i_recompute dya_main d. $run_mode
#fi
### turn on MPAS for recompute
#
#python 03_corr.py $njobs $i_save_fig ENTR ALBEDO $i_recompute dya_all e. $run_mode
#if [ $i_recompute == 0 ]; then
#python 03_corr.py $njobs $i_save_fig ENTR ALBEDO $i_recompute dya_main f. $run_mode
#fi





######## Fig. 13
#run_mode=SEA_Sc_sub_Sc
### unhide legend
#python 03_corr.py $njobs $i_save_fig ENTR INVSTR $i_recompute dya_main a. $run_mode
#python 03_corr.py $njobs $i_save_fig ENTR INVSTRV $i_recompute dya_main a. $run_mode
#exit 1
# unhide legend
#python 03_corr.py $njobs $i_save_fig INVSTR ALBEDO $i_recompute dya_main c. $run_mode
#python 03_corr.py $njobs $i_save_fig INVSTRV ALBEDO $i_recompute dya_main c. $run_mode
#if [ $i_recompute == 0 ]; then
#python 03_corr.py $njobs $i_save_fig ENTR ALBEDO $i_recompute dya_main e. $run_mode
#fi
#run_mode=SEA_Sc_sub_Cu
#python 03_corr.py $njobs $i_save_fig ENTR INVSTR $i_recompute dya_main b. $run_mode
#python 03_corr.py $njobs $i_save_fig ENTR INVSTRV $i_recompute dya_main b. $run_mode
#python 03_corr.py $njobs $i_save_fig INVSTR ALBEDO $i_recompute dya_main d. $run_mode
#python 03_corr.py $njobs $i_save_fig INVSTRV ALBEDO $i_recompute dya_main d. $run_mode
#if [ $i_recompute == 0 ]; then
#python 03_corr.py $njobs $i_save_fig ENTR ALBEDO $i_recompute dya_main f. $run_mode
#fi

