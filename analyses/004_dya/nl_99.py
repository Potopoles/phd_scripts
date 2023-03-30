
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 004_99_merge_figs:
author			Christoph Heim
date created    15.06.2021
date changed    15.06.2021
usage			import in another script
"""
###############################################################################
import os
#import numpy as np
#from datetime import datetime, timedelta
from base.nl_global import (plot_glob_base_dir, inp_glob_base_dir,
                               ana_glob_base_dir)
#from base.nl_domains import *
#from nl_mem_src import *
#from nl_var_src import set_up_var_src_dict
#from nl_plot_01 import nlp
###############################################################################
## paths
ana_name        = '004_dyamond'
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name)


merged_name = 'fig_01'
merged_name = 'fig_02'
merged_name = 'fig_03'
merged_name = 'fig_04'
merged_name = 'fig_05'
#merged_name = 'fig_06'
#merged_name = 'fig_07'
#merged_name = 'fig_08'
#merged_name = 'fig_09'
#merged_name = 'fig_10'
#merged_name = 'fig_11'
#merged_name = 'fig_12'

fig_type = 'jpg'

merge_dict = {
    'fig_01':{
        'inp_path':os.path.join(plot_glob_base_dir, '000_sim_setup'),
        'merge_figs':[
            ['ana_1_mod_1_dya_0_trnsp_False.jpg']
        ]
    },

    'fig_02':{
        'inp_path':os.path.join(plot_base_dir, '01_spatial'),
        'merge_figs':[
            [os.path.join('spatial_snapshot_var_CORREFL',
                        'spatial_SEA_Sc_snapshot_CORREFL_dt_20160814_1200.jpg')],
            [os.path.join('spatial_cosmo_clouds_var_CORREFL',
                        'spatial_test_cosmo_clouds_CORREFL_dt_20160814_1200.jpg')],
        ]
    },

    'fig_03':{
        'inp_path':os.path.join(plot_base_dir, '01_spatial'),
        'merge_figs':[
            ['spatial_SEA_Sc_dya_ALBEDO.jpg'],
            ['spatial_SEA_Sc_dya_LWUTOA.jpg'],
        ]
    },
    
    'fig_04':{
        'inp_path':os.path.join(plot_base_dir, '03_corr', 'SEA_Sc'),
        'merge_figs':[
            ['corr_dom_SEA_Sc_sim_dya_all_agg_all_TQC_ALBEDO.jpg',
             'corr_dom_SEA_Sc_sim_dya_main_agg_none_TQC_ALBEDO.jpg'],

            ['corr_dom_SEA_Sc_sim_dya_all_agg_all_CLCL2_ALBEDO.jpg',
             'corr_dom_SEA_Sc_sim_dya_main_agg_none_CLCL2_ALBEDO.jpg'],
        ]
    },

    'fig_05':{
        'inp_path':os.path.join(plot_base_dir, '03_corr', 'SEA_Sc'),
        'merge_figs':[
            ['corr_dom_SEA_Sc_sim_dya_all_agg_all_ALBEDO_LWUTOA.jpg',
             'corr_dom_SEA_Sc_sim_dya_main_agg_none_ALBEDO_LWUTOA.jpg'],

            ['corr_dom_SEA_Sc_sim_dya_all_agg_all_TQV_LWUTOA.jpg',
             'corr_dom_SEA_Sc_sim_dya_main_agg_none_TQV_LWUTOA.jpg'],
        ]
    },

    'fig_06':{
        'inp_path':os.path.join(plot_base_dir, '01_spatial'),
        'merge_figs':[
            ['spatial_SEA_Sc_dya_INVHGT.jpg'],
        ]
    },

    'fig_07':{
        'inp_path':os.path.join(plot_base_dir, '03_corr', 'SEA_Sc'),
        'merge_figs':[
            ['corr_dom_SEA_Sc_sim_dya_all_agg_all_INVHGT_ALBEDO.jpg',
             'corr_dom_SEA_Sc_sim_dya_main_agg_none_INVHGT_ALBEDO.jpg'],

            ['corr_dom_SEA_Sc_sim_dya_all_agg_all_INVSTRV_ALBEDO.jpg',
             'corr_dom_SEA_Sc_sim_dya_main_agg_none_INVSTRV_ALBEDO.jpg'],

            ['corr_dom_SEA_Sc_sim_dya_all_agg_all_SUBS_ALBEDO.jpg',
             'corr_dom_SEA_Sc_sim_dya_main_agg_none_SUBS_ALBEDO.jpg'],
        ]
    },

    'fig_08':{
        'inp_path':os.path.join(plot_base_dir, '04_cross_sects'),
        'merge_figs':[
            #[{'fig':'cs_mem_UM_5_date_20160803_0.jpg','bottom':100},
            ['cs_mem_UM_5_date_20160803_0.jpg',
             'cs_mem_IFS_4_date_20160803_0.jpg'],

            ['cs_mem_SAM_4_date_20160803_0.jpg',
             'cs_mem_MPAS_375_date_20160803_0.jpg'],

            ['cs_mem_NICAM_35_date_20160803_0.jpg',
             'cs_mem_FV3_325_date_20160803_0.jpg'],

            ['cs_mem_GEOS_3_date_20160803_0.jpg',
             'cs_mem_ARPEGE-NH_25_date_20160803_0.jpg'],

            ['cs_mem_ICON_25_date_20160803_0.jpg',
             'cs_mem_COSMO_22_date_20160803_0.jpg'],
        ]
    },

    'fig_09':{
        'inp_path':os.path.join(plot_base_dir, '02_profiles', 'SEA_Sc'),
        'merge_figs':[
            ['prof_dom_SEA_Sc_dya_main_T.jpg',
             'prof_dom_SEA_Sc_dya_main_QC.jpg',
             'prof_dom_SEA_Sc_dya_main_QV.jpg'],

            ['prof_dom_SEA_Sc_dya_main_TNORMI.jpg',
             'prof_dom_SEA_Sc_dya_main_QCNORMI.jpg',
             'prof_dom_SEA_Sc_dya_main_QVNORMI.jpg'],
        ]
    },

    'fig_10':{
        'inp_path':os.path.join(plot_base_dir, '02_profiles', 'SEA_Sc'),
        'merge_figs':[
            ['prof_dom_SEA_Sc_dya_main_W.jpg',
             'prof_dom_SEA_Sc_dya_main_WTURB.jpg'],

            ['prof_dom_SEA_Sc_dya_main_WNORMI.jpg',
             'prof_dom_SEA_Sc_dya_main_WTURBNORMISCI.jpg'],
        ]
    },

    'fig_11':{
        'inp_path':os.path.join(plot_base_dir, '02_profiles', 'SEA_Sc'),
        'merge_figs':[
            ['prof_dom_SEA_Sc_dya_main_DIABHNORMI.jpg',
             'prof_dom_SEA_Sc_dya_main_QCNORMI_label_b.jpg'],

            ['prof_dom_SEA_Sc_dya_main_POTTDIVMEANNORMI.jpg',
             'prof_dom_SEA_Sc_dya_main_POTTDIVTURBNORMI.jpg'],
        ]
    },

    'fig_12':{
        'inp_path':os.path.join(plot_base_dir, '03_corr', 'SEA_Sc'),
        'merge_figs':[
            ['corr_dom_SEA_Sc_sim_dya_all_agg_all_ENTR_INVHGT.jpg',
             'corr_dom_SEA_Sc_sim_dya_main_agg_none_ENTR_INVHGT.jpg'],

            ['corr_dom_SEA_Sc_sim_dya_all_agg_all_ENTR_SLHFLX.jpg',
             'corr_dom_SEA_Sc_sim_dya_main_agg_none_ENTR_SLHFLX.jpg'],

            ['corr_dom_SEA_Sc_sim_dya_all_agg_all_ENTR_ALBEDO.jpg',
             'corr_dom_SEA_Sc_sim_dya_main_agg_none_ENTR_ALBEDO.jpg'],
        ]
    },
}

img_names = merge_dict[merged_name]['merge_figs']
inp_path = merge_dict[merged_name]['inp_path']

