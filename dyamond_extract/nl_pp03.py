#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description:    Namelist for pp03_preproc_dyamond.py
author:         Christoph Heim
date created:   11.03.2020
date changed:   12.03.2020
usage:          import in pp03
"""
###############################################################################
import os, sys
from datetime import datetime, timedelta
from package.domains import *
###############################################################################
proj_base_dir = os.path.join('/project','pr04','heimc', 'data',
                             'simulations')
scra_base_dir = os.path.join('/scratch','snx3000','heimc', 'data',
                             'simulations')

tasks = [
    {'sim':'DYAMOND_2',
     'do': {'func':'mergetime'},
     'src_dir': proj_base_dir,
     'dest_dir': proj_base_dir,
    },
    {'sim':'SA',
    },
]


# GENERAL SETTINGS
###########################################################################
# base directory to simulations

# computation
if len(sys.argv) < 3:
    raise ValueError('2 Input Arguments needed')
njobs = int(sys.argv[1])
skey = sys.argv[2]
print('running {} with {} parallel jobs'.format(skey, njobs))

# domains (sim names) to use
inp_domain = dom_dya_2
out_domain = dom_SA


first_date = datetime(2016,8,1)
last_date = datetime(2016,9,9)
#last_date = datetime(2016,8,3)

#first_date = datetime(2016,9,4)
#last_date = datetime(2016,9,5)



cfg = {
    'ARPEGE_fix_timeaxis':0,
    'merge':0,
    'del15':0,
    'selbox':0,
    'compr_inp_daily':0,
    'compr_out_daily':2,
}

### FV3
# 2D: compr2 max 7 fields

# variables to extract
all_var_names = ['QV', 'QC', 'T', 'W', 'U', 'V', 'H', 'P',
             'U10M', 'V10M', 'T2M', 'PS', 'MSLP', 
             'LWUTOA', 'SWNDTOA', 'SWDTOA', 'SWUTOA',
             'SST', 'SLHFLX', 'SSHFLX',
             'TQC', 'TQI', 'TQV',
             'CLCL', 'CLCT', 'PP', 'PPCONV', 'PPGRID']



# ARPEGE 2D 6 tasks: 11.6min
var_names_dict = {
}

if skey in var_names_dict:
    var_names = var_names_dict[skey]
else:
    var_names = all_var_names


if len(sys.argv) == 4:
    var_names = sys.argv[3].split(',')
print('run for variables:')
print(var_names)

## optionally take var_names from input arguments
#if len(sys.argv) == 4:
#    var_names = sys.argv[3].split(',')

