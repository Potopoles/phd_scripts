#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 004_02_profiles:
author			Christoph Heim
date created    04.12.2019
date changed    18.01.2021
usage			import in another script
                args:
                1st:    number of parallel tasks
                2nd:    var_name
                3nd:    i_recompute (1: yes, 0: no)
                4th:    pane_label 
                5th:    domain
                6th:    draw legend
"""
###############################################################################
import os, sys
import numpy as np
from datetime import datetime, timedelta
from base.nl_global import (plot_glob_base_dir, inp_glob_base_dir,
                               ana_glob_base_dir)
from nl_plot_02 import nlp
from base.nl_domains import *
from nl_mem_src import *
from nl_var_src import set_up_var_src_dict
###############################################################################
## paths
ana_name        = '004_dyamond'
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name, '02_profiles')
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)
pickle_dir      = os.path.join(ana_base_dir, '02')

# check input arguments
if len(sys.argv) < 7:
    raise ValueError('Not Enough inputs arguments')

## computation
njobs = int(sys.argv[1])

## observations
var_obs_mapping = {
    #'P':        'ERA5',
    #'PNORMI':   'ERA5',
    #'POTT':     'ERA5',
    #'POTTNORMI':'ERA5',
    #'QV':       'ERA5',
    #'QVNORMI':  'ERA5',
    #'QC':       'ERA5',
    #'QCNORMI':  'ERA5',
    #'T':        'ERA5',
    #'TNORMI':   'ERA5',
    #'W':        'ERA5',
    #'WNORMI':   'ERA5',
    #'KEW':      'ERA5',
    #'KEWNORMI': 'ERA5',
}

## analysis members
obs_src_dict = mem_src['obs']
sim_group = 'dya_all'
sim_group = 'dya_main'
#sim_group = 'cosmo'
#sim_group = 'sensitivity'
#sim_group = 'debug'
#sim_group = 'iav'
sim_src_dict = mem_src[sim_group]

mode = 'MEAN'
#mode = 'SQRTMEAN'

# variables
var_name = sys.argv[2]
if mode != 'MEAN':
    out_var_name = '{}{}'.format(mode,var_name)
else:
    out_var_name = var_name
obs_key = 'ERA5_31'

## run settings
i_save_fig = 3
i_debug = 1
i_aggreg_days = 1
i_skip_missing = 1
i_plot = 1
i_recompute = int(sys.argv[3])
if i_recompute: i_plot = 0
panel_label = sys.argv[4]
i_draw_legend = int(sys.argv[6])

### time
time_periods = [
    {
        'first_date':    datetime(2016,8,6),
        'last_date':     datetime(2016,9,9),
        #'last_date':     datetime(2016,8,20),
    },
]


i_use_obs = 0
if var_name in var_obs_mapping:
    i_use_obs = 1 


cfg = {}
if len(sys.argv) > 5:
    dom_key = sys.argv[5]
    if dom_key == 'full':
        cfg['domain']       = dom_SEA_Sc
        #alt_limits = slice(0,4000)
    elif dom_key == 'Cu':
        cfg['domain']       = dom_SEA_Sc_sub_Cu
        #alt_limits = slice(0,3000)
    elif dom_key == 'Sc':
        cfg['domain']       = dom_SEA_Sc_sub_Sc
        #alt_limits = slice(0,3000)
    elif dom_key == 'St':
        cfg['domain']       = dom_SEA_Sc_sub_St
        #alt_limits = slice(0,3000)
    else:
        raise NotImplementedError()
else:
    cfg['domain']       = dom_SEA_Sc
alt_limits = slice(0,3000)
rel_alt_limits = slice(0,2)
print('run on domain {}'.format(cfg['domain']['label']))


# specific manual settings
plot_semilogx = False
if var_name in ['T', 'TNORMI']:
    xlims = (280,297)
    min_zero = False
    xticks  = np.linspace(280, 295, 4)
elif var_name in ['QC', 'QCNORMI']:
    xlims = (0, 0.0004)
    min_zero = True
    xticks  = np.linspace(0, 0.0003, 4)
elif var_name in ['QV', 'QVNORMI']:
    xlims = (0, 0.013)
    min_zero = False
    xticks  = np.linspace(0, 0.015, 4)
elif var_name in ['W', 'WNORMI']:
    xlims = (-0.01, 0.00)
    min_zero = False
    xticks  = np.linspace(-0.01, 0.000, 3)
elif var_name in ['UVFLXDIV', 'UVFLXDIVNORMI']:
    xlims = (-0.000028, 0.000016)
    min_zero = False
    xticks = np.linspace(-0.00001, 0.00002, 4) 
elif var_name in ['UV', 'UVNORMI']:
    xlims = (4, 11)
    min_zero = False
    xticks = np.linspace(4, 10, 7) 
elif var_name in ['POTTHDIV', 'POTTHDIVNORMI',
                  'POTTVDIV', 'POTTVDIVNORMI']:
    xlims = (-0.0004, 0.0002)
    min_zero = False
    xticks = np.linspace(-0.0004, 0.0001, 6) 
#TODO
elif var_name in ['POTTVDIVWPOS', 'POTTVDIVWPOSNORMI',
                  'POTTVDIVWNEG', 'POTTVDIVWNEGNORMI',]:
    xlims = (-0.0001, 0.0008)
    min_zero = False
    xticks = np.linspace(-0.0001, 0.0007, 8) 
elif var_name in ['DIABH', 'DIABHNORMI',
                  'POTTHDIVMEANNORMI', 'POTTHDIVTURBNORMI',
                  'POTTVDIVMEANNORMI', 'POTTVDIVTURBNORMI',
                  'POTTDIVMEANNORMI', 'POTTDIVTURBNORMI',
                  'POTTHDIVMEAN', 'POTTHDIVTURB',
                  'POTTVDIVMEAN', 'POTTVDIVTURB',
                  'POTTDIVMEAN', 'POTTDIVTURB']:
    xlims = (-0.0003, 0.0001)
    min_zero = False
    xticks = np.linspace(-0.0004, 0.0000, 3) 
elif var_name in ['KEW', 'KEWNORMI']:
    xlims = (1E-6, 5E-2)
    plot_semilogx = True
    min_zero = False
    xticks = None
elif var_name in ['AW', 'AWNORMI']:
    xlims = (0, 0.175)
    min_zero = False
    xticks = None
elif var_name in ['AWU', 'AWUNORMI']:
    xlims = (0, 0.175)
    min_zero = False
    xticks = None
elif var_name in ['AWD', 'AWDNORMI']:
    xlims = (-0.175, 0)
    min_zero = False
elif var_name in ['WTURBNORMISCI']:
    xlims = (0.0, 0.75)
    min_zero = True
    xticks = None
elif var_name in ['WTURB', 'WTURBNORMI']:
    xlims = (0.0, 0.25)
    min_zero = True
    xticks = np.linspace(0.0, 0.2, 5) 
else:
    xlims = None
    min_zero = False
    xticks = None

stretch = 1.3
## script specific run configs

### set up var_src
var_src_dict = set_up_var_src_dict(inp_base_dir, ana_base_dir)

