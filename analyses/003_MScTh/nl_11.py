#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 003_11_ensemble:
author			Christoph Heim
date created    04.11.2019
date changed    04.11.2019
usage			import in main script
"""
###############################################################################
import os, subprocess, sys
from datetime import datetime, timedelta
from package.utilities import set_up_directories
from package.domains import *
###############################################################################
## paths
plot_base_dir   = '/net/o3/hymet_nobackup/heimc/plots/003_MScTh'
sim_base_dir    = '/net/o3/hymet_nobackup/heimc/data/simulations'

## computation
njobs = 1
if len(sys.argv) > 1:
    njobs = int(sys.argv[1])

## run settings
i_recompute = 1
i_save_fig = 0
i_verbosity = 0

## time
time_sel = slice(datetime(2006,7,11,1,0), datetime(2006,7,20,0,0))
time_dt = timedelta(hours=1)


## simulations
use_sims = {
    'COSMO'     :[
        {'res':1.1,   'sim':'alps_MT_RAW1_09'},
        #{'res':1.1,   'sim':'alps_MT_SM1_09'},
        ],
}


## script specific run configs
configs = {
    'time_av':{
        'domain':dom_alpine_region, 
        #'domain':dom_northern_italy, 
        'nrows':1, 'ncols':2,
        'var_name':'PP',
    },
}
run_mode = 'time_av'

## implement run config
cfg = configs[run_mode]
domain  = cfg['domain']
var_name = cfg['var_name']
