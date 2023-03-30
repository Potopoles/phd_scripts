#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 001_first_tests:00_precision
author			Christoph Heim
date created    10.09.2019
date changed    12.09.2019
usage			import in another script
"""
###############################################################################
import os, subprocess, sys
from datetime import datetime, timedelta
from package.utilities import set_up_directories
from package.domains import *
###############################################################################
## paths
plot_base_dir = '/net/o3/hymet_nobackup/heimc/plots/001_first_tests' 
data_base_dir = '/net/o3/hymet_nobackup/heimc/data/preproc_cosmo'


## computation
njobs = 1
if len(sys.argv) > 1:
    njobs = int(sys.argv[1])


## plotting
i_save_fig = 1


## time
time_sel = slice(datetime(2016,8,10,0), datetime(2016,8,10,1))
time_sel = slice(datetime(2016,8,1,1), datetime(2016,9,1,0))
#time_sel = slice(datetime(2016,8,1,1), datetime(2016,10,1,0))
time_dt = timedelta(hours=1)


## simulations
use_sims = {
    'double':{
        'mkey':'COSMO',
        'prec':'double',
        'res':12, 'sim':'SA_12km_double',
        'label':'COSMO-12 double'
    },
    'double_pert1':{
        'mkey':'COSMO',
        'prec':'double',
        'res':12, 'sim':'SA_12km_double_pert1',
        'label':'COSMO-12 double pert1'
    },
    'double_pert2':{
        'mkey':'COSMO',
        'prec':'double',
        'res':12, 'sim':'SA_12km_double_pert2',
        'label':'COSMO-12 double pert2'
    },
    'double_pert3':{
        'mkey':'COSMO',
        'prec':'double',
        'res':12, 'sim':'SA_12km_double_pert3',
        'label':'COSMO-12 double pert3'
    },
    'double_pert4':{
        'mkey':'COSMO',
        'prec':'double',
        'res':12, 'sim':'SA_12km_double_pert4',
        'label':'COSMO-12 double pert4'
    },

    'double_pert5':{
        'mkey':'COSMO',
        'prec':'double',
        'res':12, 'sim':'SA_12km_double_pert5',
        'label':'COSMO-12 double pert5'
    },
    'double_pert6':{
        'mkey':'COSMO',
        'prec':'double',
        'res':12, 'sim':'SA_12km_double_pert6',
        'label':'COSMO-12 double pert6'
    },
    'double_pert7':{
        'mkey':'COSMO',
        'prec':'double',
        'res':12, 'sim':'SA_12km_double_pert7',
        'label':'COSMO-12 double pert7'
    },
    'double_pert8':{
        'mkey':'COSMO',
        'prec':'double',
        'res':12, 'sim':'SA_12km_double_pert8',
        'label':'COSMO-12 double pert8'
    },



    'float':{
        'mkey':'COSMO',
        'prec':'float',
        'res':12, 'sim':'SA_12km_float',
        'label':'COSMO-12 float'
    },
    'float_pert1':{
        'mkey':'COSMO',
        'prec':'float',
        'res':12, 'sim':'SA_12km_float_pert1',
        'label':'COSMO-12 float pert1'
    },
    'float_pert2':{
        'mkey':'COSMO',
        'prec':'float',
        'res':12, 'sim':'SA_12km_float_pert2',
        'label':'COSMO-12 float pert2'
    },
    'float_pert3':{
        'mkey':'COSMO',
        'prec':'float',
        'res':12, 'sim':'SA_12km_float_pert3',
        'label':'COSMO-12 float pert3'
    },
    'float_pert4':{
        'mkey':'COSMO',
        'prec':'float',
        'res':12, 'sim':'SA_12km_float_pert4',
        'label':'COSMO-12 float pert4'
    },
    'float_pert5':{
        'mkey':'COSMO',
        'prec':'float',
        'res':12, 'sim':'SA_12km_float_pert5',
        'label':'COSMO-12 float pert5'
    },
    'float_pert6':{
        'mkey':'COSMO',
        'prec':'float',
        'res':12, 'sim':'SA_12km_float_pert6',
        'label':'COSMO-12 float pert6'
    },
    'float_pert7':{
        'mkey':'COSMO',
        'prec':'float',
        'res':12, 'sim':'SA_12km_float_pert7',
        'label':'COSMO-12 float pert7'
    },
    'float_pert8':{
        'mkey':'COSMO',
        'prec':'float',
        'res':12, 'sim':'SA_12km_float_pert8',
        'label':'COSMO-12 float pert8'
    },
}


## script specific run configs
configs = {
    'diff':{
        'domain':dom_lm_12, 'subpath':'precision',
        'nrows':1, 'ncols':1,
    },
    'float':{
        'domain':dom_lm_12, 'subpath':'precision',
        'nrows':1, 'ncols':1,
    },
    'double':{
        'domain':dom_lm_12, 'subpath':'precision',
        'nrows':1, 'ncols':1,
    },
}
run_mode = 'diff'
#run_mode = 'float'
#run_mode = 'double'


## variable
var_name = 'LWUTOA'

#var_name = 'SWDSFC'
#var_name = 'U10M'
#var_name = 'V10M'
#var_name = 'CLCL'


## implement run config
cfg = configs[run_mode]
domain  = cfg['domain']
subpath = cfg['subpath']
