#!/bin/bash -l
#
#SBATCH --job-name="cp extr"
#SBATCH --time=12:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --account='pr133'
#SBATCH --constraint=gpu
#SBATCH --partition=xfer
#SBATCH --output=bOut/cout0
#SBATCH --error=bOut/cerr0

#module unload xalt

echo -e "$SLURM_JOB_NAME started on $(date):\n $command $1 $2\n"


#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh gulf_12 COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh gulf_2 COSMO_2.2

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_50_ctrl COSMO_50

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_ctrl COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_pgw COSMO_12

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw3 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_ctrl COSMO_3.3
srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_ctrl_4dx COSMO_3.3
srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_ctrl_4dxL COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw2 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_itcz_pgw COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw_Amon COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw_300hPa_rdheight2 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_ctrl_rdheight2 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw_300hPa COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw_100hPa COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw_500hPa COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw_200hPa COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw_final_test COSMO_3.3

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_ctrl INT2LM_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw INT2LM_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgwnp INT2LM_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw2 INT2LM_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw3 INT2LM_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw4 INT2LM_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw5 INT2LM_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw6 INT2LM_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw9 INT2LM_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw10 INT2LM_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw11 INT2LM_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw12 INT2LM_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw14 INT2LM_3.3

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw2_rdheight2 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw2_rdheight2_spubc1 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw3_rdheight2 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw3_rdheight2_spubc1 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw4_rdheight2 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw4_rdheight2_spubc1 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw5_rdheight2 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw5_rdheight2_spubc1 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw6_rdheight2 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw6_rdheight2_spubc1 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw7_rdheight2 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw8_rdheight2 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw9_rdheight2_spubc1 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw9_rdheight2_spubc1_mlev COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw9_rdheight2 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw10_rdheight2_spubc1 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw11_rdheight2_spubc1 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw12_rdheight2_spubc1 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw14_rdheight2_spubc1 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw15_rdheight2 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw16_rdheight2 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw17 COSMO_3.3

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_ctrl_ref COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_ctrl_rdheight_spubc1 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_ctrl_rdheight2_spubc1 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_ctrl_rdheight2_spubc1_mlev COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_ctrl_rdheight2 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_ctrl_nodamp COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_ctrl_rdheight COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_ctrl_spubc1 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_ctrl_qi0 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_ctrl_cloudnum COSMO_3.3

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw_ref COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw_rdheight_spubc1 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw_rdheight2_spubc1 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw_rdheight2 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw_nodamp COSMO_3.3
##srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw_rdheight COSMO_3.3
##srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw_spubc1 COSMO_3.3
##srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw_qi0 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw_cloudnum COSMO_3.3
#
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgwnp_ref COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgwnp_rdheight2_spubc1 COSMO_3.3

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw2_ref COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_pgw2_rdheight2_spubc1 COSMO_3.3

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_tuned COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_ref COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_roshyd COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_afr COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_dwd7 COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_expl COSMO_12

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_ctrl_sens1 COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_ctrl_sens2 COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_ctrl_sens3 COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_ctrl_sens4 COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_ctrl_sens5 COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_ctrl_sens6 COSMO_12

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_50_tuned COSMO_50
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_50_ref COSMO_50
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_50_roshyd COSMO_50
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_50_afr COSMO_50
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_50_dwd7 COSMO_50
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_50_expl COSMO_50

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_expl_ctrl COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_ctrl_test COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_ctrl_test0 COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_ctrl_test2 COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_ctrl_test3 COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_ctrl_test4 COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_ctrl_test5 COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_ctrl_test6 COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_ctrl_test7 COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_ctrl_test8 COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_ctrl_test9 COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_ctrl_test10 COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_ctrl_test11 COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_ctrl_test12 COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_ctrl_test13 COSMO_12


#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_ctrl_oldalb COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_ctrl_newspinup COSMO_3.3

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_ctrl_wsoil_aug COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_ctrl_oldalb_wsoil_aug COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_ctrl_newspinup_wsoil_aug COSMO_3.3

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_ctrl_wsoil_dec COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_ctrl_oldalb_wsoil_dec COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_ctrl_newspinup_wsoil_dec COSMO_3.3

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh soil_spinup COSMO_24

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_ctrl_nospinup COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_ctrl_oldspinup COSMO_3.3

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_long_large2 COSMO_3.3


#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_qi0_1e-5 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_qi0_1e-6 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_qi0_1e-4 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_qi0_1e-7 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_long_pgw COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_long_interim2_529ppm COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_long_interim COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_long_interim2 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_long_large COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_long COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_long_oldref COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_long_pgw COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_long_pgw_co2 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_long_pgw_sst COSMO_3.3

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_long COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_long_2 COSMO_4.4

################################################################
########## INTER-ANNUAL VARIABILITY
################################################################
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_iav COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_iav COSMO_2.2

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_iav_old COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_iav_old COSMO_2.2

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SSA_test COSMO_4.4


################################################################
########## FINAL DYAMOND PAPER SIMS
################################################################
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_DYA_new COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_DYA_new_dt20 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_DYA_calib COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_DYA_calib_2 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_DYA_calib_27 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_DYA_calib_46 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_test_1 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_test_9 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_test_10 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_test_11 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_test_12 COSMO_3.3

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_test_ens_1 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_test_ens_2 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_test_ens_3 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SSA_3_test_ens_1 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SSA_3_test_ens_2 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SSA_3_test_ens_3 COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_3_test_ens_1_orig_alb COSMO_3.3

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_long COSMO_3.3
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_DYA COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_DYA COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_DYA COSMO_2.2
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_DYA COSMO_1.1
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_DYA COSMO_0.5

################################################################
########## LATEST SENSITIVITY TESTS
################################################################
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_kmin0.01 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_kmin0.01 COSMO_2.2
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SSA_test_kmin_1.0 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SSA_test_kmin_1.5 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SSA_test_kmin_3.0 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SSA_test_kmin_0.01_rlam_0.1 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SSA_test_kmin_0.01_rlam_1.0 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh test_01 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh test_final_25 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_tl100 COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_sst COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_bc_1h_2 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_bc_1h_3 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_bc_1h_4 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_bc_1h_5 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_bc_1h_6 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_bc_1h_7 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_bc_1h_8 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_bc_1h_9 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_bc_3h_1 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_bc_3h_2 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_bc_3h_3 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_bc_6h_1 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_bc_6h_2 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_bc_6h_3 COSMO_4.4

################################################################
########## MLO
################################################################
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_MLO_off COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_MLO_bc COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_MLO_tau_6_depth_0.5 COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_MLO_tau_3_depth_1 COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_MLO_tau_6_depth_5 COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_MLO_tau_3_depth_3 COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_MLO_tau_3_depth_4 COSMO_12

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_4_2_noMLO COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_4_2_noMLO COSMO_2.2
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_4_2_MLO COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_4_2_MLO COSMO_2.2

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_4_2_ice0 COSMO_2.2
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_4_2_tl300 COSMO_2.2

##### DYAMOND SIMULATIONS
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12 COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_12_SHAL COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_4_2_tl150 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_4_2 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_4_2 COSMO_2.2
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_4_2_SHAL COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_4_2_SHAL COSMO_2.2
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_4_1 COSMO_1.1
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh SA_4_05 COSMO_0.5




### OLD
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh test_ERAI_12_2 COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh test_ERAI_12_2 COSMO_2.2

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh test_ERA5_4_2_3hr COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh test_ERA5_4_2_3hr COSMO_2.2

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh test_ERA5_4_2_itcz COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh test_ERA5_4_2_itcz COSMO_2.2

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh test_ERA5_4_2_itcz_soil COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh test_ERA5_4_2_itcz_soil COSMO_2.2

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh test_ERA5_12_4_2 COSMO_12
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh test_ERA5_12_4_2 COSMO_4.4
#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh test_ERA5_12_4_2 COSMO_2.2

#srun -n $SLURM_NTASKS copy_scratch_to_proj.sh test_ERA5_4_2_itcz_80lev COSMO_2.2
### DONE




echo -e "$SLURM_JOB_NAME finished on $(date)\n"


