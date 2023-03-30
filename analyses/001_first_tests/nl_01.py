#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 001_first_tests:01_domain
author			Christoph Heim
date created    16.09.2019
date changed    08.10.2019
usage			import in another script
"""
###############################################################################
import os, subprocess, sys
from datetime import datetime, timedelta
from package.utilities import set_up_directories
from package.domains import *
from nl_plot import nlp
###############################################################################
## paths O3
plot_base_dir   = '/net/o3/hymet_nobackup/heimc/plots/001_first_tests' 
data_base_dir   = '/net/o3/hymet_nobackup/heimc/data'
cosmo_data_dir  = os.path.join(data_base_dir,'simulations')
obs_data_dir    = os.path.join(data_base_dir,'obs')
ana_base_dir    = '/net/o3/hymet_nobackup/heimc/analyses/001_first_tests'
### paths daint
#plot_base_dir   = '/scratch/snx3000/heimc/plots/001_first_tests' 
#data_base_dir   = '/scratch/snx3000/heimc/data'
#cosmo_data_dir  = os.path.join(data_base_dir,'simulations')
#obs_data_dir    = os.path.join(data_base_dir,'obs')
#ana_base_dir    = '/scratch/snx3000/heimc/analyses/001_first_tests'


## computation
njobs = 1
if len(sys.argv) > 1:
    njobs = int(sys.argv[1])


## plotting
i_save_fig = 0


## time
time_sel = slice(datetime(2016,8,1,0), datetime(2016,8,2,0))
time_sel = slice(datetime(2016,8,3,0), datetime(2016,8,10,0))
time_sel = slice(datetime(2016,8,3,0), datetime(2016,8,29,0))
time_dt = timedelta(hours=1)


## remaping
recompute_sat = 0
recompute_mod = 0
grid_file_path = 'dom_grid_45km'
grid_dx = 45

## simulations
sim_configs = {
    #'full4':{
    #    'mkey':'COSMO',
    #    'res':4.4, 'sim':'SA_test_full',
    #    'label':'COSMO-4  full domain'
    #},
    #'nona4':{
    #    'mkey':'COSMO',
    #    'res':4.4, 'sim':'SA_test_nona',
    #    'label':'COSMO-4  no North Atlantic'
    #},
    #'noitcz4':{
    #    'mkey':'COSMO',
    #    'res':4.4, 'sim':'SA_test_noitcz',
    #    'label':'COSMO-4  no ITCZ'
    #},
    #'small4':{
    #    'mkey':'COSMO',
    #    'res':4.4, 'sim':'SA_test_small',
    #    'label':'COSMO-4  small'
    #},
    #'land4':{
    #    'mkey':'COSMO',
    #    'res':4.4, 'sim':'SA_test_land',
    #    'label':'COSMO-4 more land'
    #},

    '2lev':{
        'mkey':'COSMO',
        'res':2.2, 'sim':'SA_2lev',
        'label':'COSMO-2 two-level nesting'
    },
    '3lev':{
        'mkey':'COSMO',
        'res':2.2, 'sim':'SA_3lev',
        'label':'COSMO-2 three-level nesting'
    },
}

noland12_config = {
    'mkey':'COSMO',
    'res':12, 'sim':'SA_test_noland',
    'label':'COSMO-12  no continents'
}


## script specific run configs
run_configs = {
    'var':{
        'subpath':'domain',
        'nrows':1, 'ncols':1,
        'diffs':[['3lev','2lev'],],
    },
    'eval_seviri':{
        'subpath':'domain',
        'nrows':1, 'ncols':1,
        'var_name':'SWUTOA',
        'nlp':{'2D_type':'pcolormesh'},
    },
}
run_mode = 'eval_seviri'

run_mode = 'var'
var_name = 'U10M'
#var_name = 'V10M'
#var_name = 'SWNDTOA'

# take from input args
if len(sys.argv) > 3:
    run_mode = sys.argv[2]
    var_name = sys.argv[3]


#use_sims = {plot_sim_key:sim_configs[plot_sim_key]}
use_sims = sim_configs

## domain
domain  = dom_SEA
domain  = dom_test

## implement run config
cfg = run_configs[run_mode]
subpath = cfg['subpath']
if var_name in cfg.keys():
    var_name = cfg['var_name']
if 'nlp' in cfg.keys():
    for key,value in cfg['nlp'].items():
        nlp[key] = value
