
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 005_13_rad:
author			Christoph Heim
date created    02.07.2021
date changed    02.07.2021
usage			import in another script
"""
###############################################################################
import argparse, os#, subprocess, sys
#import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import *
from base.nl_global import (plot_glob_base_dir, inp_glob_base_dir,
                               ana_glob_base_dir)
from base.nl_domains import *
#from package.utilities import Time_Processing as TP
from nl_mem_src import *
from nl_var_src import set_up_var_src_dict
from nl_plot_13 import nlp
###############################################################################
## input arguments
parser = argparse.ArgumentParser(description = 'Compute and plot radiative balance.')
# number of parallel processes
parser.add_argument('-p', '--n_par', type=int, default=1)
# save or not? (0: show, 1: png, 2: pdf, 3: jpg)
parser.add_argument('-s', '--i_save_fig', type=int, default=0)
# recompute?
parser.add_argument('-r', '--i_recompute', type=int, default=0)
args = parser.parse_args()

## paths
ana_name        = '005_long'
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name, '13_rad')
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)
pickle_dir      = os.path.join(ana_base_dir, '13')

## members
obs_src_dict = mem_src['obs']

## run settings
i_debug = 2
i_plot = 1
if args.i_recompute: i_plot = 0
i_skip_missing = 1

ANA_NATIVE_domain = dom_trades
ANA_NATIVE_domain = dom_SA_3km_large3
plot_domain = dom_trades
#plot_domain = dom_SA_3km_large3

ref_mem_key = 'COSMO_3.3_ctrl'
ref_src_dict = mem_src['pgw']

mem_src_key = 'pgw'

var_names = ['SWDTOA', 'SWNDTOA', 'CSWNDTOA', 'SWUTOA', 'CSWUTOA',
             'LWUTOA', 'CLWUTOA', 'RADNDTOA', 'CRADNDTOA']
#var_names = ['RADNDTOA', 'CRADNDTOA']

plot_mode = 'abs_val'
plot_mode = 'abs_diff'
#plot_mode = 'rel_diff'

time_periods = []
end_day = 31
start_month = 8
end_month = 12
time_periods = [{'first_date':datetime(2006,start_month,1),
                 'last_date':datetime(2006,end_month,end_day)}]


### set up mem_src
mem_src_dict = mem_src[mem_src_key]
# add reference key
mem_src_dict[ref_mem_key] = ref_src_dict[ref_mem_key]

### set up var_src
var_src_dict = set_up_var_src_dict(inp_base_dir, ana_base_dir,
                                    ANA_NATIVE_domain)


