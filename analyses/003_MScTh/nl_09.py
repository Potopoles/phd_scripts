#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 003_09_cross_sect_CS:
author			Christoph Heim
date created    10.10.2019
date changed    10.10.2019
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
i_save_fig = 0
i_verbosity = 0

## time
time_sel = slice(datetime(2006,7,12,16,0), datetime(2006,7,12,17,0))
time_dt = timedelta(minutes=60)


## simulations
use_sims = {
    #'COSMO'     :[{'res':50,    'sim':'alps_50km'}],
    #'COSMO'     :[{'res':1.1,   'sim':'MScTh'},]


    'COSMO'     :[{'res':50,    'sim':'alps_50km'},
                  {'res':1.1,   'sim':'MScTh'},]
}

var_names = ['HSURF', 'QC', 'QI']
var_names = ['HSURF', 'QC']

#use_vars = {
#    'QC'    :[
#}


## script specific run configs
configs = {
    'test':{
        'domain':dom_lm_alps_50km, 
        'nrows':1, 'ncols':2,
        #'lon_slice':slice(-3.00,-2.00),
        'lon_slice':slice(-2.00,-1.00),
        'lat_slice':slice(-4.5,2.5),
    },

    '3d':{
        'domain':dom_lm_alps_50km, 
        'nrows':1, 'ncols':2,
        'lon_slice':slice(-4.10,5.10),
        'lat_slice':slice(-4.1,2.1),
        #'lon_slice':slice(-9.10,10.10),
        #'lat_slice':slice(-9.1,7.1),
    },
}
run_mode = 'test'
run_mode = '3d'

## implement run config
cfg = configs[run_mode]
domain  = cfg['domain']
