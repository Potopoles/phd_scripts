#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 004_03_corr:
author			Christoph Heim
date created    25.11.2019
date changed    02.03.2021
usage			import in another script
"""
###############################################################################
import os, subprocess, sys
import numpy as np
from datetime import datetime, timedelta
from base.nl_global import (plot_glob_base_dir, inp_glob_base_dir,
                               ana_glob_base_dir)
from base.nl_domains import *
from nl_mem_src import *
from nl_var_src import set_up_var_src_dict
from nl_plot_03 import nlp
###############################################################################
## paths
ana_name        = '004_dyamond'
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name, '03_corr')
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)
pickle_dir      = os.path.join(ana_base_dir, '03')

## computation
njobs = 1
if len(sys.argv) > 1:
    njobs = int(sys.argv[1])

## observations
var_obs_mapping = {
    #'INVHGT':'RADIO_SOUNDING',
    'INVHGT':'ERA5_31',
    'INVSTR':'ERA5_31',
    'INVSTRA':'ERA5_31',
    'CLDBASENORMI':'ERA5_31',
    'TQV0_5':'ERA5_31',
    'TQVBLI':'ERA5_31',
    'TQVFTI':'ERA5_31',
    'SWUTOA':'CM_SAF_MSG_AQUA_TERRA',
    'ALBEDO':'CM_SAF_MSG_AQUA_TERRA',
    'LWUTOA':'CM_SAF_MSG_AQUA_TERRA',
    'CLCL'  :'CM_SAF_MSG',
    'CLCL2' :'CM_SAF_MSG',
    'SUBS'  :'ERA5_31',
    'TQV'   :'CM_SAF_HTOVS',
    'TQI'   :'CM_SAF_MSG',
    'DINVHGTLCL':'ERA5_31',
    'LCL'   :'ERA5_31',
    'ENTR'  :'ERA5_31',
    'ENTRH' :'ERA5_31',
    'ENTRV' :'ERA5_31',
    'SLHFLX':'ERA5_31',
}


marker_dict = {
    'COSMO_4.4':1,
    'COSMO_4.4_calib_7':1,
    'COSMO_4.4_calib_8':1,
    'COSMO_4.4_calib_6':1,
    'COSMO_2.2':0,
    'NICAM_3.5':0,
    'SAM_4':0,
    'ICON_2.5':0,
    'UM_5':0,
    'MPAS_3.75':0,
    'IFS_4':0,
    'GEOS_3':0,
    'ARPEGE-NH_2.5':0,
    'FV3_3.25':0,

    'COSMO_12':4,
    'COSMO_1.1':2,
    'COSMO_0.5':3,
    'NICAM_7':1,
    'ICON_10':1,
    'MPAS_7.5':1,
    'IFS_9':1,

    'C12':0,
    'C12_wkf':1,
    'C4':0,
    'C4_wkf':1,
    'C4_kmin0.01':2,
    'C2':0,
    'C2_wkf':1,
    'C1':0,
    'C1_wkf':1,
}

# 0: none, 1: shallow, 2: deep&shallow
convpar_dict = {
    'C4_calibrated':0,
    'COSMO_4.4':0,
    'COSMO_2.2':0,
    'NICAM_3.5':0,
    'SAM_4':0,
    'ICON_2.5':0,
    'UM_5':1,
    'MPAS_3.75':2,
    'IFS_4':1,
    'GEOS_3':2,
    'ARPEGE-NH_2.5':0,
    'FV3_3.25':1,

    'COSMO_12':0,
    'COSMO_1.1':0,
    'COSMO_0.5':0,
    'NICAM_7':0,
    'ICON_10':0,
    'MPAS_7.5':2,
    'IFS_9':1,
}


time_periods = [
    {
        #'first_date':    datetime(2016,8,2),
        'first_date':    datetime(2016,8,6),
        #'last_date':     datetime(2016,8,20),
        'last_date':     datetime(2016,9,9),
    },
]
#init_period_until = datetime(2016,8,5)

#years = np.arange(2005,2019+1)
#time_periods = []
#for year in years:
#    time_periods.append(
#        {
#            'first_date':    datetime(year,8,6),
#            'last_date':     datetime(year,8,31),
#        }
#    )



## run settings
i_save_fig = int(sys.argv[2])
panel_label = sys.argv[7]
#panel_label = ''
i_use_obs = 1
i_debug = 1
i_skip_missing = 1
i_plot = 1
perc = (25,75)

# plotting settings
i_force_axis_limits = 1

i_recompute = int(sys.argv[5])
#i_recompute = 0
if i_recompute: i_plot = 0


#run_mode = 'iav_trades'
#run_mode = 'SEA_Sc'
#run_mode = 'SEA_Sc_sub_Cu'
#run_mode = 'SEA_Sc_sub_Sc'
#run_mode = 'SEA_Sc_sub_St'
run_mode = sys.argv[8]

## analysis members
obs_src_dict = mem_src['obs']
sim_group = sys.argv[6]
#sim_group = 'dya_all'
#sim_group = 'dya_main'
#sim_group = 'sensitivity'
#sim_group = 'cosmo'
#sim_group = 'debug'
#sim_group = 'iav'
if sim_group == 'dya_main':
    i_aggreg = 'none'
elif sim_group == 'dya_all':
    i_aggreg = 'all'
#i_aggreg = 'none'
#i_aggreg = 'monthly'
#i_aggreg = 'yearly'
#i_aggreg = 'all'
if i_recompute: sim_group = 'dya_all'
sim_src_dict = mem_src[sim_group]

# subselect specific members
mem_subsel = None
#mem_subsel = ['UM_5']
subsel = {}
if mem_subsel is not None:
    for mem_key in mem_subsel:
        subsel[mem_key] = sim_src_dict[mem_key]
    sim_src_dict = subsel
#print(sim_src_dict)
#quit()

var_names = [sys.argv[3], sys.argv[4]]

#var_names = ['U10M_W', 'ALBEDO']   # aggall: -0.80 ; daily: -0.42
#var_names = ['U10M_E', 'ALBEDO']   # aggall: -0.80 ; daily: -0.42
#var_names = ['V10M_S', 'ALBEDO']   # aggall: -0.80 ; daily: -0.42
#var_names = ['V10M_N', 'ALBEDO']   # aggall: -0.80 ; daily: -0.42
#var_names = ['V10M_S', 'INVHGT']   # aggall: -0.80 ; daily: -0.42
#var_names = ['V10M_S', 'INVSTR']   # aggall: -0.80 ; daily: -0.42
#var_names = ['V10M', 'ALBEDO']   # aggall: -0.80 ; daily: -0.42
#var_names = ['SUBS','V10M']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['SUBS','V10M_S']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['TQC', 'ALBEDO']   # aggall: -0.80 ; daily: -0.42
#var_names = ['TQC', 'CLCL2']   # aggall: -0.80 ; daily: -0.42
#var_names = ['CLCL2', 'ALBEDO']   # aggall: -0.80 ; daily: -0.42
#var_names = ['ALBEDO', 'LWUTOA']   # aggall: -0.68 ; daily: -0.50
#var_names = ['TQV', 'LWUTOA']   # aggall: -0.80 ; daily: -0.42
#var_names = ['TQI', 'LWUTOA']   # aggall: -0.80 ; daily: -0.42
#var_names = ['SUBS','INVHGT']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['SUBS','ALBEDO']  # aggall:  0.xx ; daily: -0.xx

#var_names = ['INVHGT', 'ALBEDO']   # aggall:  0.72 ; daily:  0.24
#var_names = ['ENTR','INVHGT']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['ENTR','ALBEDO']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['ENTR','SLHFLX']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['INVSTR','ALBEDO']  # aggall:  0.xx ; daily: -0.xx

#var_names = ['ENTR','INVSTR']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['LTS','SUBS']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['LTS','ALBEDO']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['LTS','ENTR']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['LTS','INVHGT']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['LTS','POTTBL']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['LTS','POTTFT']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['POTTBL', 'ALBEDO']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['POTTBL', 'ENTR']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['POTTBL', 'INVHGT']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['POTTFT', 'ALBEDO']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['POTTFT', 'ENTR']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['POTTFT', 'INVHGT']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['POTTFT','POTTBL']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['INVSTR','SUBS']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['INVSTR','ENTR']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['INVSTR','INVHGT']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['INVSTR','LTS']  # aggall:  0.xx ; daily: -0.xx

#var_names = ['bulk_tend_edge_POTT_below_S', 'INVHGT']   # aggall: -0.80 ; daily: -0.42
#var_names = ['bulk_tend_edge_POTT_below_E', 'INVHGT']   # aggall: -0.80 ; daily: -0.42
#var_names = ['bulk_tend_edge_POTT_below_N', 'INVHGT']   # aggall: -0.80 ; daily: -0.42
#var_names = ['bulk_tend_edge_POTT_below_W', 'INVHGT']   # aggall: -0.80 ; daily: -0.42
#
#var_names = ['bulk_tend_edge_POTT_below_S', 'ENTR']   # aggall: -0.80 ; daily: -0.42
#var_names = ['bulk_tend_edge_POTT_below_E', 'ENTR']   # aggall: -0.80 ; daily: -0.42
#var_names = ['bulk_tend_edge_POTT_below_N', 'ENTR']   # aggall: -0.80 ; daily: -0.42
##var_names = ['bulk_tend_edge_POTT_below_W', 'ENTR']   # aggall: -0.80 ; daily: -0.42
#
#var_names = ['bulk_tend_edge_POTT_below_S', 'ALBEDO']   # aggall: -0.80 ; daily: -0.42

#var_names = ['bulk_tend_edge_POTT_below_S', 'POTTBL']   # aggall: -0.80 ; daily: -0.42
#var_names = ['POTTBL', 'bulk_tend_edge_POTT_below_S']   # aggall: -0.80 ; daily: -0.42

#var_names = ['POTTMBLI','LTS']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['POTTHDIVMBLI','ALBEDO']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['POTTHDIVMBLI','ENTR']  # aggall:  0.xx ; daily: -0.xx
##var_names = ['POTTHDIVMBLI','SUBS']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['POTTMBLI','ALBEDO']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['POTTMBLI','SUBS']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['POTTMBLI','LWUTOA']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['POTTMBLI','POTTHDIVMBLI']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['POTTMBLI','WFLXI']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['INVHGT','DINVHGTLCL']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['DINVHGTLCL', 'ALBEDO']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['LCL', 'ALBEDO']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['INVHGT', 'LWUTOA']   # aggall: -0.80 ; daily: -0.42
#var_names = ['WFLXI','INVHGT']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['WFLXI','ALBEDO']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['ENTRH','INVHGT']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['ENTRV','INVHGT']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['ENTRH','ALBEDO']  # aggall:  0.xx ; daily: -0.xx
#var_names = ['ENTRV','ALBEDO']  # aggall:  0.xx ; daily: -0.xx


## remove some members for daily
#if (i_aggreg == 'none') and (not i_recompute):
#    for mem_key in ['COSMO_12', 'COSMO_12_SHAL', 'COSMO_4.4_SHAL',
#                    'COSMO_2.2_SHAL', 'COSMO_1.1', 'COSMO_0.5',
#                    'NICAM_7', 'ICON_10',
#                    'MPAS_7.5', 'IFS_9']:
#        if mem_key in sim_src_dict:
#            del sim_src_dict[mem_key]
#    #if key in use_sims:
#    #    use_sims['COSMO_4.4']['marker'] = 4



## script specific run configs
configs = {
    'iav_trades':{
        'domain'    :dom_iav_trades,
    },
    'SEA_Sc':{
        'domain'    :dom_SEA_Sc,
    },
    'SEA_Sc_sub_Cu':{
        'domain'    :dom_SEA_Sc_sub_Cu,
    },
    'SEA_Sc_sub_Sc':{
        'domain'    :dom_SEA_Sc_sub_Sc,
    },
    'SEA_Sc_sub_St':{
        'domain'    :dom_SEA_Sc_sub_St,
    },
    'test':{
        'domain'    :dom_test,
    },
}
cfg = configs[run_mode]


### set up var_src
var_src_dict = set_up_var_src_dict(inp_base_dir, ana_base_dir)


# add use_sims members to nlp.plot_order if not in there
# (default value at the end)
for mem_key,mem_dict in sim_src_dict.items():
    if mem_key not in nlp['plot_order']:
        nlp['plot_order'].append(mem_key)
