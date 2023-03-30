#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 004_10_olr_bias:
author			Christoph Heim
date created    14.01.2021
date changed    21.01.2021
usage			import in another script
"""
###############################################################################
import os, sys
import numpy as np
from datetime import datetime, timedelta
from base.nl_global import (plot_glob_base_dir, inp_glob_base_dir,
                               ana_glob_base_dir)
from nl_plot_10 import nlp
from base.nl_domains import *
from nl_mem_src import *
from nl_var_src import set_up_var_src_dict
###############################################################################
## paths
ana_name        = '004_dyamond'
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name, '10_olr_bias')
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)
pickle_dir      = os.path.join(ana_base_dir, '10')

if len(sys.argv) <= 5:
    raise ValueError('Not 5 arguments given')

## computation
njobs = int(sys.argv[1])

## analysis members
obs_src_dict = mem_src['obs']
sim_group = 'all_members'
#sim_group = 'sensitivity'
#sim_group = 'debug'
#sim_group = 'iav'
sim_src_dict_tmp = mem_src[sim_group]
# select members in sim_src_dict based on user input
mem_keys = sys.argv[5].split(',')
sim_src_dict = {}
for mem_key in mem_keys:
    print(mem_key)
    if mem_key in sim_src_dict_tmp:
        sim_src_dict[mem_key] = sim_src_dict_tmp[mem_key]
    else: raise ValueError('mem_key {} not in sim_src_dict'.format(mem_key))
# add OBS
sim_src_dict['OBS'] = {}

## observation
#obs_key = 'ERA5_31'

# observations
var_obs_mapping = {
    #'INVHGT':'ERA5_31',
    'LWUTOA':'CM_SAF_MSG_AQUA_TERRA',
    'ALBEDO':'CM_SAF_MSG_AQUA_TERRA',
    'TQI':'CM_SAF_MSG',
    'TQV':'CM_SAF_HTOVS',
}

# var_names
var_names = ['LWUTOA', 'ALBEDO', 'TQI', 'TQV']

## run settings
i_save_fig = 1
i_debug = 1
i_aggreg_days = 0
i_skip_missing = 1
i_plot = 0
i_regression = 1
i_recompute = int(sys.argv[2])
if i_recompute: i_plot = 0; i_regression = 0;
panel_label = sys.argv[3]

### time
time_periods = [
    {
        'first_date':    datetime(2016,8,6),
        'last_date':     datetime(2016,9,9),
        #'first_date':    datetime(2016,8,6),
        #'last_date':     datetime(2016,8,6),
    },
]


cfg = {}
dom_key = sys.argv[4]
if dom_key == 'full':
    cfg['domain']       = dom_SEA_Sc
elif dom_key == 'Cu':
    cfg['domain']       = dom_SEA_Sc_sub_Cu
elif dom_key == 'Sc':
    cfg['domain']       = dom_SEA_Sc_sub_Sc
elif dom_key == 'St':
    cfg['domain']       = dom_SEA_Sc_sub_St
else:
    raise NotImplementedError()
print('run on domain {}'.format(cfg['domain']['label']))


### set up var_src
var_src_dict = set_up_var_src_dict(inp_base_dir, ana_base_dir)
