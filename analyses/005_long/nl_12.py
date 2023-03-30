#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 005_12_dardar:
author			Christoph Heim
date created    28.04.2020
date changed    11.05.2021
usage			import in another script
"""
###############################################################################
import os, subprocess, sys, warnings, argparse
from datetime import datetime, timedelta
from dateutil.relativedelta import *
from base.nl_global import (plot_glob_base_dir, inp_glob_base_dir,
                               ana_glob_base_dir)
from base.nl_domains import *
from nl_mem_src import *
from nl_var_src import set_up_var_src_dict
from nl_plot_12 import nlp
###############################################################################
## input arguments
parser = argparse.ArgumentParser(description = 'Interpolate model data onto dardar tracks.')
# member to compute
parser.add_argument('mem_key', type=str)
# number of parallel processes
parser.add_argument('-p', '--n_par', type=int, default=1)
# save or not? (0: show, 1: png, 2: pdf, 3: jpg)
parser.add_argument('-s', '--i_save_fig', type=int, default=0)
# recompute?
parser.add_argument('-r', '--i_recompute', type=int, default=0)
args = parser.parse_args()

## paths
ana_name        = '005_long'
inp_base_dir    = inp_glob_base_dir
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name, '02_profiles')
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)
pickle_dir      = os.path.join(ana_base_dir, '12')
#pickle_dir      = os.path.join(ana_base_dir, '09')

# path to dardar data
dardar_dict = mem_src['obs']['DARDAR_CLOUD']
dardar_inp_dir = os.path.join(inp_base_dir,
                       dardar_dict['sim'], dardar_dict['case'],
                       dom_SEA_Sc['key'], 'daily')


## analysis members
sim_group = 'all_members'
sim_src_dict = mem_src[sim_group]

obs_key = 'DARDAR_CLOUD'

ANNUAL_CYCLE = 'annualcycle'
HOURLY_SERIES = 'hourly'
DAILY_SERIES = 'daily'
MONTHLY_SERIES = 'monthly'
YEARLY_SERIES = 'yearly'

time_mode = ANNUAL_CYCLE

####
i_debug     = 2
# draw plot
i_plot = 1
if args.i_recompute: i_plot = 0
i_skip_missing = 1
panel_label = 'a'
i_draw_legend = 1
alt_limits = slice(0,3000)


time_periods = []
start_day = 2
end_day = 3
year = 2006
for month in range(8,13):
    time_periods.append(
        {
            'first_date':    datetime(year,month,start_day),
            'last_date':     datetime(year,month,1)+relativedelta(months=1)-timedelta(days=1),
            #'last_date':     datetime(year,month,end_day),
        },
    )
for year in [2007,2008,2009]:
#for year in [2007,2008]:
    for month in range(1,13):
        time_periods.append(
            {
                'first_date':    datetime(year,month,start_day),
                'last_date':     datetime(year,month,1)+relativedelta(months=1)-timedelta(days=1),
                #'last_date':     datetime(year,month,end_day),
            },
        )


#time_periods = [{'first_date':datetime(2006,8,1),
#                 'last_date':datetime(2006,8,3)}]

ANA_NATIVE_domain = dom_trades
plot_domain = dom_trades
#domain = dom_trades_shallow
#domain = dom_trades_medium
#domain = dom_trades_deep

var_name = 'CLDMASK'
var_name = 'LCLDTOP'
var_name = 'INVHGT'

if var_name == 'INVHGT':
    dar_var_name = 'CLDMASK'
    #dar_var_name = 'T'
    mod_var_name = 'INVHGT'
elif var_name == 'CLDMASK':
    dar_var_name = 'CLDMASK'
    mod_var_name = 'CLDMASK'
elif var_name == 'LCLDTOP':
    dar_var_name = 'CLDMASK'
    mod_var_name = 'CLDMASK'


if var_name in ['']:
    xlims = (280,297)
    min_zero = False
    xticks  = np.linspace(280, 295, 4)
else:
    xlims = None
    min_zero = False
    xticks = None

#time_mode = 'daily'

### set up var_src
var_src_dict = set_up_var_src_dict(inp_base_dir, ana_base_dir,
                                   ANA_NATIVE_domain)
