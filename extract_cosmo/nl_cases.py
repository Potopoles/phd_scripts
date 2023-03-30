#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description:    Namelist for cosmo output extraction that maps the simulation
                tag to a case name used in subsequent analyses
author:         Christoph Heim
date created:   13.09.2019
date changed:   24.04.2021
usage:          import in extract_case
"""
###############################################################################

# cases
cases = {

    ############# MASTER THESIS FENGGE PERSIAN GULF
    ###########################################################################
    'gulf_12' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'gulf', 'sub_dir':'lm_c',
        'sim_name':'gulf_12',
    },
    'gulf_2' :{
        'model':'COSMO',   'res':2.2,
        'inp_tag':'gulf', 'sub_dir':'lm_f',
        'sim_name':'gulf_2',
    },

    ############# FINAL LONG-TERM SIMULATION
    ###########################################################################
    #### 50km simulation start
    'SA_50_tuned' :{
        'model':'COSMO',   'res':50,
        'inp_tag':'SA_50_tuned', 'sub_dir':'lm_c',
        'sim_name':'SA_50_tuned',
    },
    'SA_50_ref' :{
        'model':'COSMO',   'res':50,
        'inp_tag':'SA_50_ref', 'sub_dir':'lm_c',
        'sim_name':'SA_50_ref',
    },
    'SA_50_roshyd' :{
        'model':'COSMO',   'res':50,
        'inp_tag':'SA_50_roshyd', 'sub_dir':'lm_c',
        'sim_name':'SA_50_roshyd',
    },
    'SA_50_afr' :{
        'model':'COSMO',   'res':50,
        'inp_tag':'SA_50_afr', 'sub_dir':'lm_c',
        'sim_name':'SA_50_afr',
    },
    'SA_50_dwd7' :{
        'model':'COSMO',   'res':50,
        'inp_tag':'SA_50_dwd7', 'sub_dir':'lm_c',
        'sim_name':'SA_50_dwd7',
    },
    'SA_50_expl' :{
        'model':'COSMO',   'res':50,
        'inp_tag':'SA_50_expl', 'sub_dir':'lm_c',
        'sim_name':'SA_50_expl',
    },


    'SA_50_ctrl' :{
        'model':'COSMO',   'res':50,
        'inp_tag':'SA_50_ctrl', 'sub_dir':'lm_c',
        'sim_name':'SA_50_ctrl',
    },



    #### 24km simulation start
    'soil_spinup' :{
        'model':'COSMO',   'res':24,
        'inp_tag':'soil_spinup', 'sub_dir':'lm_c',
        'sim_name':'soil_spinup',
    },
    #### 24km simulation stop


    #### 12km simulation start
    'SA_12_ctrl' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_ctrl', 'sub_dir':'lm_c',
        'sim_name':'SA_12_ctrl',
    },
    'SA_12_pgw' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_pgw', 'sub_dir':'lm_c',
        'sim_name':'SA_12_pgw',
    },



    'SA_12_expl_ctrl' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_expl_ctrl', 'sub_dir':'lm_c',
        'sim_name':'SA_12_expl_ctrl',
    },
    'SA_12_ctrl_test' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_ctrl_test', 'sub_dir':'lm_c',
        'sim_name':'SA_12_ctrl_test',
    },
    'SA_12_ctrl_test0' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_ctrl_test0', 'sub_dir':'lm_c',
        'sim_name':'SA_12_ctrl_test0',
    },
    'SA_12_ctrl_test2' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_ctrl_test2', 'sub_dir':'lm_c',
        'sim_name':'SA_12_ctrl_test2',
    },
    'SA_12_ctrl_test3' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_ctrl_test3', 'sub_dir':'lm_c',
        'sim_name':'SA_12_ctrl_test3',
    },
    'SA_12_ctrl_test4' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_ctrl_test4', 'sub_dir':'lm_c',
        'sim_name':'SA_12_ctrl_test4',
    },
    'SA_12_ctrl_test5' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_ctrl_test5', 'sub_dir':'lm_c',
        'sim_name':'SA_12_ctrl_test5',
    },
    'SA_12_ctrl_test6' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_ctrl_test6', 'sub_dir':'lm_c',
        'sim_name':'SA_12_ctrl_test6',
    },
    'SA_12_ctrl_test7' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_ctrl_test7', 'sub_dir':'lm_c',
        'sim_name':'SA_12_ctrl_test7',
    },
    'SA_12_ctrl_test8' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_ctrl_test8', 'sub_dir':'lm_c',
        'sim_name':'SA_12_ctrl_test8',
    },
    'SA_12_ctrl_test9' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_ctrl_test9', 'sub_dir':'lm_c',
        'sim_name':'SA_12_ctrl_test9',
    },
    'SA_12_ctrl_test10' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_ctrl_test10', 'sub_dir':'lm_c',
        'sim_name':'SA_12_ctrl_test10',
    },
    'SA_12_ctrl_test11' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_ctrl_test11', 'sub_dir':'lm_c',
        'sim_name':'SA_12_ctrl_test11',
    },
    'SA_12_ctrl_test12' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_ctrl_test12', 'sub_dir':'lm_c',
        'sim_name':'SA_12_ctrl_test12',
    },
    'SA_12_ctrl_test13' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_ctrl_test13', 'sub_dir':'lm_c',
        'sim_name':'SA_12_ctrl_test13',
    },


    'SA_12_tuned' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_tuned', 'sub_dir':'lm_c',
        'sim_name':'SA_12_tuned',
    },
    'SA_12_ref' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_ref', 'sub_dir':'lm_c',
        'sim_name':'SA_12_ref',
    },
    'SA_12_roshyd' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_roshyd', 'sub_dir':'lm_c',
        'sim_name':'SA_12_roshyd',
    },
    'SA_12_afr' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_afr', 'sub_dir':'lm_c',
        'sim_name':'SA_12_afr',
    },
    'SA_12_dwd7' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_dwd7', 'sub_dir':'lm_c',
        'sim_name':'SA_12_dwd7',
    },
    'SA_12_expl' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_expl', 'sub_dir':'lm_c',
        'sim_name':'SA_12_expl',
    },


    'SA_12_ctrl_sens1' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_ctrl_sens1', 'sub_dir':'lm_c',
        'sim_name':'SA_12_ctrl_sens1',
    },
    'SA_12_ctrl_sens2' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_ctrl_sens2', 'sub_dir':'lm_c',
        'sim_name':'SA_12_ctrl_sens2',
    },
    'SA_12_ctrl_sens3' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_ctrl_sens3', 'sub_dir':'lm_c',
        'sim_name':'SA_12_ctrl_sens3',
    },
    'SA_12_ctrl_sens4' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_ctrl_sens4', 'sub_dir':'lm_c',
        'sim_name':'SA_12_ctrl_sens4',
    },
    'SA_12_ctrl_sens5' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_ctrl_sens5', 'sub_dir':'lm_c',
        'sim_name':'SA_12_ctrl_sens5',
    },
    'SA_12_ctrl_sens6' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_ctrl_sens6', 'sub_dir':'lm_c',
        'sim_name':'SA_12_ctrl_sens6',
    },


    #### 3.3km simulation start
    'SA_3_ctrl_BC' :{
        'model':'INT2LM',   'res':3.3,
        'inp_tag':'SA_3_ctrl_BC', 'sub_dir':'lm_c',
        'sim_name':'SA_3_ctrl',
    },
    'SA_3_pgw_BC' :{
        'model':'INT2LM',   'res':3.3,
        'inp_tag':'SA_3_pgw_BC', 'sub_dir':'lm_c',
        'sim_name':'SA_3_pgw',
    },
    'SA_3_pgw5_BC' :{
        'model':'INT2LM',   'res':3.3,
        'inp_tag':'SA_3_pgw5_BC', 'sub_dir':'lm_c',
        'sim_name':'SA_3_pgw5',
    },
    'SA_3_pgw9_BC' :{
        'model':'INT2LM',   'res':3.3,
        'inp_tag':'SA_3_pgw9_BC', 'sub_dir':'lm_c',
        'sim_name':'SA_3_pgw9',
    },
    'SA_3_pgw14_BC' :{
        'model':'INT2LM',   'res':3.3,
        'inp_tag':'SA_3_pgw14_BC', 'sub_dir':'lm_c',
        'sim_name':'SA_3_pgw14',
    },

    'SA_3_ctrl' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_ctrl', 'sub_dir':'lm_c',
        'sim_name':'SA_3_ctrl',
    },
    'SA_3_ctrl_4dx' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_ctrl_4dx', 'sub_dir':'lm_c',
        'sim_name':'SA_3_ctrl_4dx',
    },
    'SA_3_ctrl_4dxL' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_ctrl_4dxL', 'sub_dir':'lm_c',
        'sim_name':'SA_3_ctrl_4dxL',
    },
    'SA_3_pgw' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_pgw', 'sub_dir':'lm_c',
        'sim_name':'SA_3_pgw',
    },
    'SA_3_pgw2' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_pgw2', 'sub_dir':'lm_c',
        'sim_name':'SA_3_pgw2',
    },
    'SA_3_pgw3' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_pgw3', 'sub_dir':'lm_c',
        'sim_name':'SA_3_pgw3',
    },
    'SA_3_itcz_pgw' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_itcz_pgw', 'sub_dir':'lm_c',
        'sim_name':'SA_3_itcz_pgw',
    },
    'SA_3_itcz_pgw2' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_itcz_pgw2', 'sub_dir':'lm_c',
        'sim_name':'SA_3_itcz_pgw2',
    },
    'SA_3_pgw_300hPa' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_pgw_300hPa', 'sub_dir':'lm_c',
        'sim_name':'SA_3_pgw_300hPa',
    },
    'SA_3_pgw_100hPa' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_pgw_100hPa', 'sub_dir':'lm_c',
        'sim_name':'SA_3_pgw_100hPa',
    },
    'SA_3_pgw_500hPa' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_pgw_500hPa', 'sub_dir':'lm_c',
        'sim_name':'SA_3_pgw_500hPa',
    },
    'SA_3_pgw_200hPa' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_pgw_200hPa', 'sub_dir':'lm_c',
        'sim_name':'SA_3_pgw_200hPa',
    },

    'SA_3_ctrl_ref' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_ctrl_ref', 'sub_dir':'lm_c',
        'sim_name':'SA_3_ctrl_ref',
    },
    'SA_3_ctrl_rdheight2' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_ctrl_rdheight2', 'sub_dir':'lm_c',
        'sim_name':'SA_3_ctrl_rdheight2',
    },
    'SA_3_ctrl_spubc1' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_ctrl_spubc1', 'sub_dir':'lm_c',
        'sim_name':'SA_3_ctrl_spubc1',
    },
    'SA_3_ctrl_rdheight2_spubc1' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_ctrl_rdheight2_spubc1', 'sub_dir':'lm_c',
        'sim_name':'SA_3_ctrl_rdheight2_spubc1',
    },



    'SA_3_pgw_Amon' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_pgw_Amon', 'sub_dir':'lm_c',
        'sim_name':'SA_3_pgw_Amon',
    },
    'SA_3_pgw_ref' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_pgw_ref', 'sub_dir':'lm_c',
        'sim_name':'SA_3_pgw_ref',
    },
    'SA_3_pgw_300hPa_rdheight2' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_pgw_300hPa_rdheight2', 'sub_dir':'lm_c',
        'sim_name':'SA_3_pgw_300hPa_rdheight2',
    },
    'SA_3_pgw_rdheight2' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_pgw_rdheight2', 'sub_dir':'lm_c',
        'sim_name':'SA_3_pgw_rdheight2',
    },
    'SA_3_pgw_spubc1' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_pgw_spubc1', 'sub_dir':'lm_c',
        'sim_name':'SA_3_pgw_spubc1',
    },
    'SA_3_pgw_rdheight2_spubc1' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_pgw_rdheight2_spubc1', 'sub_dir':'lm_c',
        'sim_name':'SA_3_pgw_rdheight2_spubc1',
    },
    'SA_3_pgw_hmo3' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_pgw_hmo3', 'sub_dir':'lm_c',
        'sim_name':'SA_3_pgw_hmo3',
    },



    'SA_3_pgw5_rdheight2' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_pgw5_rdheight2', 'sub_dir':'lm_c',
        'sim_name':'SA_3_pgw5_rdheight2',
    },
    'SA_3_pgw5_rdheight2_spubc1' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_pgw5_rdheight2_spubc1', 'sub_dir':'lm_c',
        'sim_name':'SA_3_pgw5_rdheight2_spubc1',
    },



    'SA_3_pgw9_rdheight2_spubc1' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_pgw9_rdheight2_spubc1', 'sub_dir':'lm_c',
        'sim_name':'SA_3_pgw9_rdheight2_spubc1',
    },
    'SA_3_pgw9_rdheight2' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_pgw9_rdheight2', 'sub_dir':'lm_c',
        'sim_name':'SA_3_pgw9_rdheight2',
    },


    'SA_3_pgw10_rdheight2_spubc1' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_pgw10_rdheight2_spubc1', 'sub_dir':'lm_c',
        'sim_name':'SA_3_pgw10_rdheight2_spubc1',
    },

    'SA_3_pgw11_rdheight2_spubc1' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_pgw11_rdheight2_spubc1', 'sub_dir':'lm_c',
        'sim_name':'SA_3_pgw11_rdheight2_spubc1',
    },

    'SA_3_pgw14_rdheight2_spubc1' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_pgw14_rdheight2_spubc1', 'sub_dir':'lm_c',
        'sim_name':'SA_3_pgw14_rdheight2_spubc1',
    },

    'SA_3_pgw17' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_pgw17', 'sub_dir':'lm_c',
        'sim_name':'SA_3_pgw17',
    },


    'SA_3_ctrl_wsoil_aug' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_ctrl', 'sub_dir':'lm_c_wsoil_aug',
        'sim_name':'SA_3_ctrl_wsoil_aug',
    },
    'SA_3_ctrl_oldalb_wsoil_aug' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_ctrl_oldalb', 'sub_dir':'lm_c_wsoil_aug',
        'sim_name':'SA_3_ctrl_oldalb_wsoil_aug',
    },
    'SA_3_ctrl_newspinup_wsoil_aug' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_ctrl_newspinup', 'sub_dir':'lm_c_wsoil_aug',
        'sim_name':'SA_3_ctrl_newspinup_wsoil_aug',
    },
    'SA_3_ctrl_wsoil_dec' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_ctrl', 'sub_dir':'lm_c_wsoil_dec',
        'sim_name':'SA_3_ctrl_wsoil_dec',
    },
    'SA_3_ctrl_oldalb_wsoil_dec' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_ctrl_oldalb', 'sub_dir':'lm_c_wsoil_dec',
        'sim_name':'SA_3_ctrl_oldalb_wsoil_dec',
    },
    'SA_3_ctrl_newspinup_wsoil_dec' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_ctrl_newspinup', 'sub_dir':'lm_c_wsoil_dec',
        'sim_name':'SA_3_ctrl_newspinup_wsoil_dec',
    },








    'SA_3_ctrl_oldalb' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_ctrl_oldalb', 'sub_dir':'lm_c',
        'sim_name':'SA_3_ctrl_oldalb',
    },
    'SA_3_ctrl_newspinup' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_ctrl_newspinup', 'sub_dir':'lm_c',
        'sim_name':'SA_3_ctrl_newspinup',
    },
    'SA_3_ctrl_nospinup' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_ctrl_nospinup', 'sub_dir':'lm_c',
        'sim_name':'SA_3_ctrl_nospinup',
    },
    'SA_3_ctrl_oldspinup' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_ctrl_oldspinup', 'sub_dir':'lm_c',
        'sim_name':'SA_3_ctrl_oldspinup',
    },
    'SA_3_long_large2' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_long_large', 'sub_dir':'lm_c_new',
        'sim_name':'SA_3_long_large2',
    },

    'SA_3_qi0_1e-5' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_long_interim2_qi0_1', 'sub_dir':'lm_c',
        'sim_name':'SA_3_qi0_1e-5',
    },
    'SA_3_qi0_1e-6' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_long_interim2_qi0_2', 'sub_dir':'lm_c',
        'sim_name':'SA_3_qi0_1e-6',
    },
    'SA_3_qi0_1e-4' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_long_interim2_qi0_3', 'sub_dir':'lm_c',
        'sim_name':'SA_3_qi0_1e-4',
    },
    'SA_3_qi0_1e-7' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_long_interim2_qi0_4', 'sub_dir':'lm_c',
        'sim_name':'SA_3_qi0_1e-7',
    },


    'SA_3_long_interim2_529ppm' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_long_interim2_529ppm', 'sub_dir':'lm_c',
        'sim_name':'SA_3_long_interim2_529ppm',
    },
    'SA_3_long_interim2' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_long_interim2', 'sub_dir':'lm_c',
        'sim_name':'SA_3_long_interim2',
    },
    'SA_3_long' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_long_OLD', 'sub_dir':'lm_c',
        'sim_name':'SA_3_long',
    },
    'SA_3_long_oldref' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_long_OLD', 'sub_dir':'lm_c_oldref',
        'sim_name':'SA_3_long_oldref',
    },
    'SA_3_long_OLD_pgw' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_long_OLD', 'sub_dir':'lm_c_pgw',
        'sim_name':'SA_3_long_OLD_pgw',
    },
    'SA_3_long_OLD_pgw_co2' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_long_OLD', 'sub_dir':'lm_c_pgw_co2',
        'sim_name':'SA_3_long_OLD_pgw_co2',
    },
    'SA_3_long_OLD_pgw_sst' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_long_OLD', 'sub_dir':'lm_c_pgw_sst',
        'sim_name':'SA_3_long_OLD_pgw_sst',
    },

    ############# TEST NEW SIM SETUP
    ###########################################################################
    #### 4.4km simulation start
    'SSA_test_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SSA_test', 'sub_dir':'lm_c',
        'sim_name':'SSA_test',
    },


    ############# INTER-ANNUAL VARIABILITY
    ###########################################################################
    #### 4.4km simulation start
    'SA_4_2_iav_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2', 'sub_dir':'lm_c_iav',
        'sim_name':'SA_iav',
    },
    'SA_4_2_iav_old_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2', 'sub_dir':'lm_c_iav_old',
        'sim_name':'SA_iav_old',
    },
    #### 4.4km simulation end
    #### 2.2km simulation start
    'SA_4_2_iav_2.2km' :{
        'model':'COSMO',   'res':2.2,
        'inp_tag':'SA_4_2', 'sub_dir':'lm_f_iav',
        'sim_name':'SA_iav',
    },
    'SA_4_2_iav_old_2.2km' :{
        'model':'COSMO',   'res':2.2,
        'inp_tag':'SA_4_2', 'sub_dir':'lm_f_iav_old',
        'sim_name':'SA_iav_old',
    },
    #### 2.2km simulation end

    ############# FINAL DYAMOND PAPER SIMS
    ###########################################################################
    #### 12km simulation start
    'SA_12_DYA_12km' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12', 'sub_dir':'lm_c_DYA',
        'sim_name':'SA_DYA',
    },
    #### 12km simulation end
    #### 4.4km simulation start
    'SA_4_2_DYA_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2', 'sub_dir':'lm_c_DYA',
        'sim_name':'SA_DYA',
    },
    'SA_4_2_DYA_calib_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib', 'sub_dir':'lm_c',
        'sim_name':'SA_DYA_calib',
    },
    'SA_4_2_DYA_calib_2_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib', 'sub_dir':'lm_c_2',
        'sim_name':'SA_DYA_calib_2',
    },
    'SA_4_2_DYA_calib_3_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib', 'sub_dir':'lm_c_3',
        'sim_name':'SA_DYA_calib_3',
    },
    'SA_4_2_DYA_calib_4_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib', 'sub_dir':'lm_c_4',
        'sim_name':'SA_DYA_calib_4',
    },
    'SA_4_2_DYA_calib_5_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib', 'sub_dir':'lm_c_5',
        'sim_name':'SA_DYA_calib_5',
    },
    'SA_4_2_DYA_calib_6_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib', 'sub_dir':'lm_c_6',
        'sim_name':'SA_DYA_calib_6',
    },
    'SA_4_2_DYA_calib_7_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib', 'sub_dir':'lm_c_7',
        'sim_name':'SA_DYA_calib_7',
    },
    'SA_4_2_DYA_calib_8_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib', 'sub_dir':'lm_c_8',
        'sim_name':'SA_DYA_calib_8',
    },
    'SA_4_2_DYA_calib_9_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib', 'sub_dir':'lm_c_9',
        'sim_name':'SA_DYA_calib_9',
    },
    'SA_4_2_DYA_calib_10_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib_2', 'sub_dir':'lm_c',
        'sim_name':'SA_DYA_calib_10',
    },
    'SA_4_2_DYA_calib_11_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib_3', 'sub_dir':'lm_c',
        'sim_name':'SA_DYA_calib_11',
    },
    'SA_4_2_DYA_calib_12_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib', 'sub_dir':'lm_c_10',
        'sim_name':'SA_DYA_calib_12',
    },
    'SA_4_2_DYA_calib_13_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib_2', 'sub_dir':'lm_c_2',
        'sim_name':'SA_DYA_calib_13',
    },
    'SA_4_2_DYA_calib_14_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib_3', 'sub_dir':'lm_c_2',
        'sim_name':'SA_DYA_calib_14',
    },
    'SA_4_2_DYA_calib_15_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib_4', 'sub_dir':'lm_c',
        'sim_name':'SA_DYA_calib_15',
    },


    'SA_4_2_DYA_calib_16_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib', 'sub_dir':'lm_c_11',
        'sim_name':'SA_DYA_calib_16',
    },
    'SA_4_2_DYA_calib_17_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib_2', 'sub_dir':'lm_c_3',
        'sim_name':'SA_DYA_calib_17',
    },
    'SA_4_2_DYA_calib_18_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib_3', 'sub_dir':'lm_c_3',
        'sim_name':'SA_DYA_calib_18',
    },
    'SA_4_2_DYA_calib_19_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib_4', 'sub_dir':'lm_c_2',
        'sim_name':'SA_DYA_calib_19',
    },
    'SA_4_2_DYA_calib_20_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib', 'sub_dir':'lm_c_12',
        'sim_name':'SA_DYA_calib_20',
    },
    'SA_4_2_DYA_calib_21_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib_2', 'sub_dir':'lm_c_4',
        'sim_name':'SA_DYA_calib_21',
    },
    'SA_4_2_DYA_calib_22_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib_3', 'sub_dir':'lm_c_4',
        'sim_name':'SA_DYA_calib_22',
    },
    'SA_4_2_DYA_calib_23_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib_4', 'sub_dir':'lm_c_3',
        'sim_name':'SA_DYA_calib_23',
    },
    'SA_4_2_DYA_calib_24_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib', 'sub_dir':'lm_c_13',
        'sim_name':'SA_DYA_calib_24',
    },
    'SA_4_2_DYA_calib_25_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib_2', 'sub_dir':'lm_c_5',
        'sim_name':'SA_DYA_calib_25',
    },
    'SA_4_2_DYA_calib_26_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib_3', 'sub_dir':'lm_c_5',
        'sim_name':'SA_DYA_calib_26',
    },
    'SA_4_2_DYA_calib_27_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib_4', 'sub_dir':'lm_c_4',
        'sim_name':'SA_DYA_calib_27',
    },
    'SA_4_2_DYA_calib_28_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib', 'sub_dir':'lm_c_14',
        'sim_name':'SA_DYA_calib_28',
    },

    'SA_4_2_DYA_calib_29_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib', 'sub_dir':'lm_c_15',
        'sim_name':'SA_DYA_calib_29',
    },
    'SA_4_2_DYA_calib_30_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib_2', 'sub_dir':'lm_c_6',
        'sim_name':'SA_DYA_calib_30',
    },
    'SA_4_2_DYA_calib_31_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib_3', 'sub_dir':'lm_c_6',
        'sim_name':'SA_DYA_calib_31',
    },
    'SA_4_2_DYA_calib_32_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib_4', 'sub_dir':'lm_c_5',
        'sim_name':'SA_DYA_calib_32',
    },

    'SA_4_2_DYA_calib_33_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib', 'sub_dir':'lm_c_16',
        'sim_name':'SA_DYA_calib_33',
    },
    'SA_4_2_DYA_calib_34_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib_2', 'sub_dir':'lm_c_7',
        'sim_name':'SA_DYA_calib_34',
    },
    'SA_4_2_DYA_calib_35_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib_3', 'sub_dir':'lm_c_7',
        'sim_name':'SA_DYA_calib_35',
    },
    'SA_4_2_DYA_calib_36_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib_4', 'sub_dir':'lm_c_6',
        'sim_name':'SA_DYA_calib_36',
    },
    'SA_4_2_DYA_calib_37_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib', 'sub_dir':'lm_c_17',
        'sim_name':'SA_DYA_calib_37',
    },
    'SA_4_2_DYA_calib_38_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib', 'sub_dir':'lm_c_18',
        'sim_name':'SA_DYA_calib_38',
    },
    'SA_4_2_DYA_calib_39_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib', 'sub_dir':'lm_c_19',
        'sim_name':'SA_DYA_calib_39',
    },
    'SA_4_2_DYA_calib_40_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib_2', 'sub_dir':'lm_c_8',
        'sim_name':'SA_DYA_calib_40',
    },
    'SA_4_2_DYA_calib_41_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib_3', 'sub_dir':'lm_c_8',
        'sim_name':'SA_DYA_calib_41',
    },


    'SA_4_2_DYA_calib_42_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib', 'sub_dir':'lm_c_20',
        'sim_name':'SA_DYA_calib_42',
    },
    'SA_4_2_DYA_calib_43_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib_2', 'sub_dir':'lm_c_9',
        'sim_name':'SA_DYA_calib_43',
    },
    'SA_4_2_DYA_calib_44_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib_3', 'sub_dir':'lm_c_9',
        'sim_name':'SA_DYA_calib_44',
    },
    'SA_4_2_DYA_calib_45_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib_4', 'sub_dir':'lm_c_7',
        'sim_name':'SA_DYA_calib_45',
    },
    'SA_4_2_DYA_calib_46_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_calib', 'sub_dir':'lm_c_21',
        'sim_name':'SA_DYA_calib_46',
    },



    'SA_3_test_1_3.3km' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_test', 'sub_dir':'lm_c',
        'sim_name':'SA_3_test_1',
    },
    'SA_3_test_2_3.3km' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_test', 'sub_dir':'lm_c_2',
        'sim_name':'SA_3_test_2',
    },
    'SA_3_test_3_3.3km' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_test_2', 'sub_dir':'lm_c',
        'sim_name':'SA_3_test_3',
    },
    'SA_3_test_4_3.3km' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_test', 'sub_dir':'lm_c_3',
        'sim_name':'SA_3_test_4',
    },
    'SA_3_test_5_3.3km' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_test_2', 'sub_dir':'lm_c_2',
        'sim_name':'SA_3_test_5',
    },
    'SA_3_test_6_3.3km' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_test', 'sub_dir':'lm_c_4',
        'sim_name':'SA_3_test_6',
    },
    'SA_long_3.3km' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_long', 'sub_dir':'lm_c',
        'sim_name':'SA_long',
    },

    'SA_3_test_7_3.3km' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_test', 'sub_dir':'lm_c_5',
        'sim_name':'SA_3_test_7',
    },
    'SA_3_test_8_3.3km' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_test_2', 'sub_dir':'lm_c_3',
        'sim_name':'SA_3_test_8',
    },
    'SA_3_test_9_3.3km' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_test', 'sub_dir':'lm_c_6',
        'sim_name':'SA_3_test_9',
    },
    'SA_3_test_10_3.3km' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_test', 'sub_dir':'lm_c_7',
        'sim_name':'SA_3_test_10',
    },
    'SA_3_test_11_3.3km' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_test', 'sub_dir':'lm_c_8',
        'sim_name':'SA_3_test_11',
    },



    'SA_3_test_ens_1' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_test', 'sub_dir':'lm_c_ens_1',
        'sim_name':'SA_3_test_ens_1',
    },
    'SA_3_test_ens_2' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_test', 'sub_dir':'lm_c_ens_2',
        'sim_name':'SA_3_test_ens_2',
    },
    'SA_3_test_ens_3' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_test', 'sub_dir':'lm_c_ens_3',
        'sim_name':'SA_3_test_ens_3',
    },

    'SSA_3_test_ens_1' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SSA_3_test', 'sub_dir':'lm_c_ens_1',
        'sim_name':'SSA_3_test_ens_1',
    },
    'SSA_3_test_ens_2' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SSA_3_test', 'sub_dir':'lm_c_ens_2',
        'sim_name':'SSA_3_test_ens_2',
    },
    'SSA_3_test_ens_3' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SSA_3_test', 'sub_dir':'lm_c_ens_3',
        'sim_name':'SSA_3_test_ens_3',
    },

    'SA_3_test_ens_1_orig_alb' :{
        'model':'COSMO',   'res':3.3,
        'inp_tag':'SA_3_test_2', 'sub_dir':'lm_c_ens_1_orig_alb',
        'sim_name':'SA_3_test_ens_1_orig_alb',
    },


    #### 4.4km simulation end
    #### 2.2km simulation start
    'SA_4_2_DYA_2.2km' :{
        'model':'COSMO',   'res':2.2,
        'inp_tag':'SA_4_2', 'sub_dir':'lm_f_DYA',
        'sim_name':'SA_DYA',
    },
    #### 2.2km simulation end
    #### 1.1km simulation start
    'SA_4_1_DYA_1.1km' :{
        'model':'COSMO',   'res':1.1,
        'inp_tag':'SA_4_1', 'sub_dir':'lm_f_DYA',
        'sim_name':'SA_DYA',
    },
    #### 1.1km simulation end
    #### 0.55km simulation start
    'SA_4_05_DYA_0.5km' :{
        'model':'COSMO',   'res':0.5,
        'inp_tag':'SA_4_05', 'sub_dir':'lm_f_DYA',
        'sim_name':'SA_DYA',
    },
    #### 0.55km simulation end

    ############# LATEST SENSITIVITY TESTS
    ###########################################################################
    #### 12km simulation start
    'SA_12_12km' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12', 'sub_dir':'lm_c_DYA',
        'sim_name':'SA',
    },
    'SA_12_tl100_12km' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_tl100', 'sub_dir':'lm_c',
        'sim_name':'SA_tl100',
    },
    'SA_12_sst_12km' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_sst', 'sub_dir':'lm_c',
        'sim_name':'SA_sst',
    },
    #### 12km simulation end
    #### 4.4km simulation start
    'SA_4_2_bc_1h_2' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2', 'sub_dir':'lm_c_bc_1h_2',
        'sim_name':'SA_bc_1h_2',
    },
    'SA_4_2_bc_1h_3' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2', 'sub_dir':'lm_c_bc_1h_3',
        'sim_name':'SA_bc_1h_3',
    },
    'SA_4_2_bc_1h_4' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2', 'sub_dir':'lm_c_bc_1h_4',
        'sim_name':'SA_bc_1h_4',
    },
    'SA_4_2_bc_1h_5' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2', 'sub_dir':'lm_c_bc_1h_5',
        'sim_name':'SA_bc_1h_5',
    },
    'SA_4_2_bc_1h_6' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2', 'sub_dir':'lm_c_bc_1h_6',
        'sim_name':'SA_bc_1h_6',
    },
    'SA_4_2_bc_1h_7' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2', 'sub_dir':'lm_c_bc_1h_7',
        'sim_name':'SA_bc_1h_7',
    },
    'SA_4_2_bc_1h_8' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2', 'sub_dir':'lm_c_bc_1h_8',
        'sim_name':'SA_bc_1h_8',
    },
    'SA_4_2_bc_1h_9' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2', 'sub_dir':'lm_c_bc_1h_9',
        'sim_name':'SA_bc_1h_9',
    },
    'SA_4_2_bc_3h_1' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2', 'sub_dir':'lm_c_bc_3h_1',
        'sim_name':'SA_bc_3h_1',
    },
    'SA_4_2_bc_3h_2' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2', 'sub_dir':'lm_c_bc_3h_2',
        'sim_name':'SA_bc_3h_2',
    },
    'SA_4_2_bc_3h_3' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2', 'sub_dir':'lm_c_bc_3h_3',
        'sim_name':'SA_bc_3h_3',
    },
    'SA_4_2_bc_6h_1' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2', 'sub_dir':'lm_c_bc_6h_1',
        'sim_name':'SA_bc_6h_1',
    },
    'SA_4_2_bc_6h_2' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2', 'sub_dir':'lm_c_bc_6h_2',
        'sim_name':'SA_bc_6h_2',
    },
    'SA_4_2_bc_6h_3' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2', 'sub_dir':'lm_c_bc_6h_3',
        'sim_name':'SA_bc_6h_3',
    },
    'SA_4_2_kmin0.01_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2', 'sub_dir':'lm_c_kmin0.01',
        'sim_name':'SA_kmin0.01',
    },
    'SSA_test_kmin_1.0_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SSA_test_kmin_1.0', 'sub_dir':'lm_c',
        'sim_name':'SSA_test_kmin_1.0',
    },
    'SSA_test_kmin_1.5_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SSA_test_kmin_1.5', 'sub_dir':'lm_c',
        'sim_name':'SSA_test_kmin_1.5',
    },
    'SSA_test_kmin_3.0_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SSA_test_kmin_3.0', 'sub_dir':'lm_c',
        'sim_name':'SSA_test_kmin_3.0',
    },
    'SSA_test_kmin_0.01_rlam_0.1_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SSA_test_kmin_0.01_rlam_0.1', 'sub_dir':'lm_c',
        'sim_name':'SSA_test_kmin_0.01_rlam_0.1',
    },
    'SSA_test_kmin_0.01_rlam_1.0_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SSA_test_kmin_0.01_rlam_1.0', 'sub_dir':'lm_c',
        'sim_name':'SSA_test_kmin_0.01_rlam_1.0',
    },
    'SA_4_2_tl150_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_wkf_tl150', 'sub_dir':'lm_c',
        'sim_name':'SA_wkf_tl150',
    },
    'test_01_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_01', 'sub_dir':'lm_c',
        'sim_name':'test_01',
    },
    'test_02_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_02', 'sub_dir':'lm_c',
        'sim_name':'test_02',
    },
    'test_03_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_03', 'sub_dir':'lm_c',
        'sim_name':'test_03',
    },
    'test_04_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_04', 'sub_dir':'lm_c',
        'sim_name':'test_04',
    },
    'test_05_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_05', 'sub_dir':'lm_c',
        'sim_name':'test_05',
    },
    'test_06_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_06', 'sub_dir':'lm_c',
        'sim_name':'test_06',
    },
    'test_07_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_07', 'sub_dir':'lm_c',
        'sim_name':'test_07',
    },
    'test_08_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_08', 'sub_dir':'lm_c',
        'sim_name':'test_08',
    },
    'test_09_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_09', 'sub_dir':'lm_c',
        'sim_name':'test_09',
    },
    'test_10_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_10', 'sub_dir':'lm_c',
        'sim_name':'test_10',
    },
    'test_11_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_11', 'sub_dir':'lm_c',
        'sim_name':'test_11',
    },
    'test_12_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_12', 'sub_dir':'lm_c',
        'sim_name':'test_12',
    },
    'test_13_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_13', 'sub_dir':'lm_c',
        'sim_name':'test_13',
    },
    'test_14_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_14', 'sub_dir':'lm_c',
        'sim_name':'test_14',
    },
    'test_15_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_15', 'sub_dir':'lm_c',
        'sim_name':'test_15',
    },
    'test_16_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_16', 'sub_dir':'lm_c',
        'sim_name':'test_16',
    },
    'test_17_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_17', 'sub_dir':'lm_c',
        'sim_name':'test_17',
    },
    'test_18_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_18', 'sub_dir':'lm_c',
        'sim_name':'test_18',
    },
    'test_19_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_19', 'sub_dir':'lm_c',
        'sim_name':'test_19',
    },
    'test_20_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_20', 'sub_dir':'lm_c',
        'sim_name':'test_20',
    },
    'test_21_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_21', 'sub_dir':'lm_c',
        'sim_name':'test_21',
    },
    'test_22_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_22', 'sub_dir':'lm_c',
        'sim_name':'test_22',
    },
    'test_23_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_23', 'sub_dir':'lm_c',
        'sim_name':'test_23',
    },
    'test_24_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_24', 'sub_dir':'lm_c',
        'sim_name':'test_24',
    },
    'test_25_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_25', 'sub_dir':'lm_c',
        'sim_name':'test_25',
    },
    'test_26_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_26', 'sub_dir':'lm_c',
        'sim_name':'test_26',
    },
    'test_27_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_27', 'sub_dir':'lm_c',
        'sim_name':'test_27',
    },
    'test_28_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_28', 'sub_dir':'lm_c',
        'sim_name':'test_28',
    },
    'test_29_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_29', 'sub_dir':'lm_c',
        'sim_name':'test_29',
    },
    'test_30_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_30', 'sub_dir':'lm_c',
        'sim_name':'test_30',
    },
    'test_31_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_31', 'sub_dir':'lm_c',
        'sim_name':'test_31',
    },
    'test_32_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_32', 'sub_dir':'lm_c',
        'sim_name':'test_32',
    },
    'test_33_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_33', 'sub_dir':'lm_c',
        'sim_name':'test_33',
    },
    'test_34_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_34', 'sub_dir':'lm_c',
        'sim_name':'test_34',
    },
    'test_35_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_35', 'sub_dir':'lm_c',
        'sim_name':'test_35',
    },
    'test_36_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_36', 'sub_dir':'lm_c',
        'sim_name':'test_36',
    },
    'test_37_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_37', 'sub_dir':'lm_c',
        'sim_name':'test_37',
    },
    'test_38_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_38', 'sub_dir':'lm_c',
        'sim_name':'test_38',
    },
    'test_39_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_39', 'sub_dir':'lm_c',
        'sim_name':'test_39',
    },
    'test_40_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_40', 'sub_dir':'lm_c',
        'sim_name':'test_40',
    },
    'test_41_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_41', 'sub_dir':'lm_c',
        'sim_name':'test_41',
    },
    'test_42_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_42', 'sub_dir':'lm_c',
        'sim_name':'test_42',
    },
    'test_43_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_43', 'sub_dir':'lm_c',
        'sim_name':'test_43',
    },
    'test_44_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_44', 'sub_dir':'lm_c',
        'sim_name':'test_44',
    },
    'test_45_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_45', 'sub_dir':'lm_c',
        'sim_name':'test_45',
    },
    'test_final_25_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'test_final_25', 'sub_dir':'lm_c',
        'sim_name':'test_final_25',
    },
    #### 4.4km simulation end
    #### 2.2km simulation start
    'SA_4_2_kmin0.01_2.2km' :{
        'model':'COSMO',   'res':2.2,
        'inp_tag':'SA_4_2', 'sub_dir':'lm_f_kmin0.01',
        'sim_name':'SA_kmin0.01',
    },
    'SA_4_2_tl300_2.2km' :{
        'model':'COSMO',   'res':2.2,
        'inp_tag':'SA_4_2', 'sub_dir':'lm_f_tl300',
        'sim_name':'SA_tl300',
    },
    #### 2.2km simulation end

    ### testing MLO
    #'SA_MLO_off' :{
    #    'sims':{'12km'  :{'model':'COSMO',   'res':12,
    #                      'inp_tag':'SA_12_MLO',
    #                      'sub_dir':'lm_c_off'},}},
    #'SA_MLO_bc' :{
    #    'sims':{'12km'  :{'model':'COSMO',   'res':12,
    #                      'inp_tag':'SA_12_MLO',
    #                      'sub_dir':'lm_c_bc'},}},
    #'SA_MLO_tau_6_depth_0.5' :{
    #    'sims':{'12km'  :{'model':'COSMO',   'res':12,
    #                      'inp_tag':'SA_12_MLO',
    #                      'sub_dir':'lm_c_tau_6_depth_0.5'},}},
    #'SA_MLO_tau_3_depth_1' :{
    #    'sims':{'12km'  :{'model':'COSMO',   'res':12,
    #                      'inp_tag':'SA_12_MLO',
    #                      'sub_dir':'lm_c_tau_3_depth_1'},}},
    #'SA_MLO_tau_6_depth_5' :{
    #    'sims':{'12km'  :{'model':'COSMO',   'res':12,
    #                      'inp_tag':'SA_12_MLO',
    #                      'sub_dir':'lm_c_tau_6_depth_5'},}},
    #'SA_MLO_tau_3_depth_3' :{
    #    'sims':{'12km'  :{'model':'COSMO',   'res':12,
    #                      'inp_tag':'SA_12_MLO',
    #                      'sub_dir':'lm_c_tau_3_depth_3'},}},
    #'SA_MLO_tau_3_depth_4' :{
    #    'sims':{'12km'  :{'model':'COSMO',   'res':12,
    #                      'inp_tag':'SA_12_MLO',
    #                      'sub_dir':'lm_c_tau_3_depth_4'},}},

    #'SA_4_2_noMLO' :{
    #    'sims':{
    #        '4.4km'  :{'model':'COSMO',   'res':4.4,
    #                   'inp_tag':'SA_4_2', 'sub_dir':'lm_c_MLO_ref'},
    #        '2.2km'  :{'model':'COSMO',   'res':2.2,
    #                   'inp_tag':'SA_4_2', 'sub_dir':'lm_f_MLO_ref'},
    #            },},

    #'SA_4_2_MLO' :{
    #    'sims':{
    #        '4.4km'  :{'model':'COSMO',   'res':4.4,
    #                   'inp_tag':'SA_4_2_MLO', 'sub_dir':'lm_c'},
    #        '2.2km'  :{'model':'COSMO',   'res':2.2,
    #                   'inp_tag':'SA_4_2_MLO', 'sub_dir':'lm_f'},
    #            },},

    #'SA_4_2_ice0' :{
    #    'sims':{
    #        '2.2km'  :{'model':'COSMO',   'res':2.2,
    #                   'inp_tag':'SA_4_2_ice0', 'sub_dir':'lm_f'},
    #            },},


    ### ERA5
    #'ERA5' :{
    #    'sims':{'30km'  :{'model':'ERA5',   'res':30,
    #                      'inp_tag':'ERA5', 'sub_dir':'SA'},}},

    ############# ORIG SA DYAMOND SIMS
    ###########################################################################
    #### 12km simulation start
    'SA_12_wkf_2.2km' :{
        'model':'COSMO',   'res':12,
        'inp_tag':'SA_12_wkf', 'sub_dir':'lm_c',
        'sim_name':'SA_wkf',
    },
    #### 12km simulation end
    #### 4.4km simulation start
    'SA_4_2_wkf_4.4km' :{
        'model':'COSMO',   'res':4.4,
        'inp_tag':'SA_4_2_wkf', 'sub_dir':'lm_c',
        'sim_name':'SA_wkf',
    },
    #### 4.4km simulation end
    #### 2.2km simulation start
    'SA_4_2_wkf' :{
        'model':'COSMO',   'res':2.2,
        'inp_tag':'SA_4_2_wkf', 'sub_dir':'lm_f',
        'sim_name':'SA_wkf',
    },
    #### 2.2km simulation end


    #'SA_12_SHAL_wkf' :{
    #    'sims':{'12km'  :{'model':'COSMO',   'res':12,
    #                      'inp_tag':'SA_12_SHAL', 'sub_dir':'lm_c'},}},
    #'SA_4_2_SHAL' :{
    #    'sims':{'4.4km' :{'res':4.4,'inp_tag':'SA_4_2_SHAL', 'sub_dir':'lm_c'},
    #            '2.2km' :{'res':2.2,'inp_tag':'SA_4_2_SHAL', 'sub_dir':'lm_f'},}},

    #'SA_4_1' :{
    #    'sims':{'1.1km' :{'res':1.1,'inp_tag':'SA_4_1',   'sub_dir':'lm_f'},}},

    #'SA_4_1_SHAL' :{
    #    'sims':{'1.1km' :{'res':1.1,'inp_tag':'SA_4_1_SHAL', 'sub_dir':'lm_f'},}},

    #'SA_4_05' :{
    #    'sims':{'0.5km' :{'res':0.5,'inp_tag':'SA_4_05', 'sub_dir':'lm_f'},}},




    ### ERA5 tests
    #'test_ERAI_12_2' :{
    #    'sims':{'12km'  :{'res':12  ,'inp_tag':'test_ERAI_12_2', 'sub_dir':'lm_c'},
    #            '2.2km' :{'res':2.2 ,'inp_tag':'test_ERAI_12_2', 'sub_dir':'lm_f'},}},

    #'test_ERA5_12_2' :{
    #    'sims':{'12km'  :{'res':12  ,'inp_tag':'test_ERA5_12_2', 'sub_dir':'lm_c'},
    #            '2.2km' :{'res':2.2 ,'inp_tag':'test_ERA5_12_2', 'sub_dir':'lm_f'},}},

    #'test_ERA5_4_2_3hr' :{
    #    'sims':{'4.4km' :{'res':4.4 ,'inp_tag':'test_ERA5_4_2_3hr', 'sub_dir':'lm_c'},
    #            '2.2km' :{'res':2.2 ,'inp_tag':'test_ERA5_4_2_3hr', 'sub_dir':'lm_f'},}},

    #'test_ERA5_4_2_1hr' :{
    #    'sims':{'4.4km' :{'res':4.4 ,'inp_tag':'test_ERA5_4_2_1hr', 'sub_dir':'lm_c'},
    #            '2.2km' :{'res':2.2 ,'inp_tag':'test_ERA5_4_2_1hr', 'sub_dir':'lm_f'},}},

    #'test_ERA5_12_4_2' :{
    #    'sims':{'12km'  :{'res':12  ,'inp_tag':'test_ERA5_12_4_2_outer', 'sub_dir':'lm_c'},
    #            '4.4km' :{'res':4.4 ,'inp_tag':'test_ERA5_12_4_2_outer', 'sub_dir':'lm_f'},
    #            '2.2km' :{'res':2.2 ,'inp_tag':'test_ERA5_12_4_2_inner', 'sub_dir':'lm_f'},}},

    #'test_ERA5_4_2_itcz' :{
    #    'sims':{'4.4km' :{'res':4.4 ,'inp_tag':'test_ERA5_4_2_itcz', 'sub_dir':'lm_c'},
    #            '2.2km' :{'res':2.2 ,'inp_tag':'test_ERA5_4_2_itcz', 'sub_dir':'lm_f'},}},

    #'test_ERA5_4_2_itcz_soil' :{
    #    'sims':{
    #        '4.4km' :{'res':4.4 ,'inp_tag':'test_ERA5_4_2_itcz_soil', 'sub_dir':'lm_c'},
    #        '2.2km' :{'res':2.2 ,'inp_tag':'test_ERA5_4_2_itcz_soil', 'sub_dir':'lm_f'},}},

    #'test_ERAI_4_2_itcz' :{
    #    'sims':{
    #        '4.4km' :{'res':4.4 ,'inp_tag':'test_ERAI_4_2_itcz', 'sub_dir':'lm_c'},
    #        '2.2km' :{'res':2.2 ,'inp_tag':'test_ERAI_4_2_itcz', 'sub_dir':'lm_f'},}},

    #'test_ERA5_4_2_itcz_80lev' :{
    #    'sims':{
    #        '2.2km' :{'res':2.2 ,'inp_tag':'test_ERA5_4_2_itcz_80lev', 'sub_dir':'lm_f'},}},


    #'test_ERA5_4_1' :{
    #    'sims':{
    #        '1.1km' :{'res':1.1 ,   'inp_tag':'test_ERA5_4_1_itcz', 'sub_dir':'lm_f'},}},




    #'SA_3D' :{
    #    'inp_tag':'SA_4_2',
    #    'sims':{'2.2km' :{'res':2.2 ,'sub_dir':'lm_f'},}},

    ##'SA_3lev_cont' :{
    ##    'inp_tag':'SA_4_2',
    ##    'sims':{'2.2km' :{'res':2.2 ,'sub_dir':'2km_more_continent'},}},

    #'SA_2lev' :{
    #    'inp_tag':'SA_12_2',
    #    'sims':{'2.2km' :{'res':2.2 ,'sub_dir':'lm_f'},}},
    #'SA_3lev' :{
    #    'inp_tag':'SA_4_2',
    #    'sims':{'4.4km' :{'res':4.4 ,'sub_dir':'lm_c'},
    #            '2.2km' :{'res':2.2 ,'sub_dir':'2km_less_land'},}},
    #    #'inp_tag':'SA_12_4',
    #    #'sims':{'12km'  :{'res':12 ,'sub_dir':'lm_c'},}},


    #'alps_MT_RAW1' :{
    #    'inp_tag':'alps_MT_RAW1',
    #    'sims':{'1.1km' :{'res':1.1 ,'sub_dir':'lm_f'},}},


    ##'SA_12km' :{
    ##    'inp_tag':'SA_12_4', 'res':12,
    ##    'sub_folder':'12km',},
    ##'SA_4km' :{
    ##    'inp_tag':'SA_12_4', 'res':4.4,
    ##    'sub_folder':'4km',},

    ### domain tests
    #'SA_test_nona' :{
    #    'inp_tag':'SA_12_4_test_nona',
    #    'sims':{'12km'  :{'res':12  ,'sub_dir':'lm_c'},
    #            '4.4km' :{'res':4.4 ,'sub_dir':'lm_f'},}},

    #'SA_test_small' :{
    #    'inp_tag':'SA_12_4_test_small',
    #    'sims':{'12km'  :{'res':12  ,'sub_dir':'lm_c'},
    #            '4.4km' :{'res':4.4 ,'sub_dir':'lm_f'},}},

    #'SA_test_noitcz' :{
    #    'inp_tag':'SA_12_4_test_noitcz',
    #    'sims':{'12km'  :{'res':12  ,'sub_dir':'lm_c'},
    #            '4.4km' :{'res':4.4 ,'sub_dir':'lm_f'},}},

    #'SA_test_land' :{
    #    'inp_tag':'SA_12_4_test_land',
    #    'sims':{'12km'  :{'res':12  ,'sub_dir':'lm_c'},
    #            '4.4km' :{'res':4.4 ,'sub_dir':'lm_f'},}},


    #'alps_50km' :{
    #    'inp_tag':'alps_50km',
    #    'sims':{'50km' :{'res':50 ,'sub_dir':'lm_c'},}},

}
