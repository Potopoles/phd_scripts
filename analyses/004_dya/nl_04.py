#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 004_04_cross_sects:
author			Christoph Heim
date created    29.01.2021
date changed    10.02.2021
usage			import in another script
"""
###############################################################################
import os, copy, subprocess, sys
import numpy as np
from datetime import datetime, timedelta
from base.nl_global import (plot_glob_base_dir, inp_glob_base_dir,
                               ana_glob_base_dir)
from base.nl_domains import *
from nl_mem_src import *
from nl_var_src import set_up_var_src_dict
from nl_plot_04 import nlp
###############################################################################
## paths
ana_name        = '004_dyamond'
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name, '04_cross_sects')
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)
pickle_dir      = os.path.join(ana_base_dir, '04')

# check input args
if len(sys.argv) <= 3:
    raise ValueError()

## computation
njobs = int(sys.argv[1])

time_periods = [
    {
        #'first_date':    datetime(2016,8,1),
        #'last_date':     datetime(2016,9,9),
        #'first_date':    datetime(2016,8,6),
        #'last_date':     datetime(2016,8,6),
        #'first_date':    datetime(2016,8,2),
        #'last_date':     datetime(2016,8,2),
        'first_date':    datetime(2016,8,3),
        'last_date':     datetime(2016,8,3),

        #'first_date':    datetime(2016,8,1),
        #'last_date':     datetime(2016,8,6),
    },
]

## run settings
i_save_fig = int(sys.argv[2])
panel_label = ''
i_use_obs = 0
i_debug = 1
i_skip_missing = 1
i_plot = 1
i_recompute = int(sys.argv[3])
if i_recompute: i_plot = 0;
perc = (25,75)

# plotting settings
i_force_axis_limits = 1

run_mode = 'SEA_Sc'
run_mode = 'SEA_Sc_sub_Cu'
run_mode = 'SEA_Sc_sub_Sc'
#run_mode = 'SEA_Sc_sub_St'

## analysis members
obs_src_dict = mem_src['obs']
sim_group = 'all_members'
sim_src_dict = mem_src[sim_group]

mem_subsel = None
mem_subsel = ['UM_5', 'IFS_4', 'SAM_4',
              'MPAS_3.75', 'NICAM_3.5','FV3_3.25', 'GEOS_3',
              'ARPEGE-NH_2.5', 'ICON_2.5', 'COSMO_2.2']
#mem_subsel = ['FV3_3.25']
              
#mem_subsel = ['UM_5', 'SAM_4',
#              'NICAM_3.5','GEOS_3',
#              'ICON_2.5']
#mod_sel=0
##mem_subsel = ['IFS_4', 'MPAS_3.75',
##              'FV3_3.25', 'ARPEGE-NH_2.5',
##              'COSMO_2.2']
##mod_sel=1
#
#mem_subsel = ['UM_5', 'SAM_4',
#              'NICAM_3.5','GEOS_3',
#              'ICON_2.5']

subsel = {}
if mem_subsel is not None:
    for mem_key in mem_subsel:
        subsel[mem_key] = sim_src_dict[mem_key]
sim_src_dict = subsel

#if sim_group == 'dya_main':
#    i_aggreg = 'none'
#elif sim_group == 'dya_all':
#    i_aggreg = 'all'
#i_aggreg = 'none'
#i_aggreg = 'monthly'
#i_aggreg = 'yearly'
#i_aggreg = 'all'

plot_hours = ['00 UTC', '03 UTC', '06 UTC',
              '09 UTC', '12 UTC', '15 UTC',
              '18 UTC', '21 UTC']
#plot_hours = ['00 UTC']
plot_hours = ['03 UTC']
#plot_hours = ['06 UTC']


#var_names_2d = ['LCL', 'INVHGT', 'LCLDBASE']
var_names_3d_fc = ['W']
var_names_3d_lc = ['QC']
var_names_2d = ['INVHGT', 'LCL']
var_names = copy.deepcopy(var_names_2d)
var_names.extend(var_names_3d_fc)
var_names.extend(var_names_3d_lc)

### set up var_src
var_src_dict = set_up_var_src_dict(inp_base_dir, ana_base_dir)


domains = [dom_SEA_Sc_sub_Cu, dom_SEA_Sc_sub_Sc]
alt_lims = (0,3000) 

#cfg = {}
#if run_mode == 'SEA_Sc_sub_Cu':
#    cfg['domain']       = dom_SEA_Sc_sub_Cu 
#    #cfg['cross_sect']   = {'lon':None, 'lat':-6.5} 
#    cfg['cross_sect']   = {'lon':None, 'lat':-8.8} 
#    cfg['alt_lims']     = (0,3000) 
#elif run_mode == 'SEA_Sc_sub_Sc':
#    cfg['domain']       = dom_SEA_Sc_sub_Sc
#    #cfg['cross_sect']   = {'lon':None, 'lat':-13} 
#    cfg['cross_sect']   = {'lon':None, 'lat':-15} 
#    #cfg['alt_lims']     = (0,2000) 
#    cfg['alt_lims']     = (0,3000) 
#elif run_mode == 'combination':
#    cfg['domains']       = dom_SEA_Sc_sub_Sc
#    #cfg['cross_sect']   = {'lon':None, 'lat':-13} 
#    cfg['cross_sect']   = {'lon':None, 'lat':-15} 
#    #cfg['alt_lims']     = (0,2000) 
#    cfg['alt_lims']     = (0,3000) 
#else: raise ValueError()

#plot_domains = {
#    'SEA_Sc_sub_Cu'
#}
#dom_1 = dom_SEA_Sc_sub_Cu 
#dom_2 = dom_SEA_Sc_sub_Sc

#cfg['domain']       = dom_SEA_Sc_sub_St
#cfg['cross_sect']   = {'lon':None, 'lat':-16} 
#cfg['alt_lims']     = (0,1500) 

