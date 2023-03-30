#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    plotting namelist for 005_19_cldsize:
author			Christoph Heim
date changed    14.06.2022
date changed    14.06.2022
usage			import in another script
                args:
"""
###############################################################################
import os
from datetime import datetime, timedelta
from base.nl_global import (plot_glob_base_dir, inp_glob_base_dir,
                               ana_glob_base_dir)
from package.time_processing import Time_Processing as TP
from base.nl_domains import *
from base.nl_time_periods import *
from nl_mem_src import *
from nl_var_src import set_up_var_src_dict
###############################################################################
## paths
ana_name        = '005_long'
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name, '19_cldsize')
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)
ANA_NATIVE_domain = dom_SA_3km_large3

plot_domain = dom_SA_ana
plot_domain = dom_ITCZ_feedback
plot_domain = dom_trades_full
plot_domain = dom_trades_west
plot_domain = dom_trades_east

## run settings
i_debug = 2
i_plot = 1
i_skip_missing = 1

p_lims = (1000,200)
#alt_lims = (0,18000) 
##alt_lims = (0,30000) 
##rel_alt_lims = (0.0,1.5) 
#rel_alt_lims = (0.0,2) 

time_periods = time_periods_2007
time_periods = time_periods_ana
#time_periods = get_time_periods_for_month(2007, 8)
#time_periods = time_periods_ana_SON

#time_periods = [{
#    'first_date':datetime(2007,1,7),
#    'last_date':datetime(2007,1,7)
#}]


agg_level = TP.ALL_TIME
#agg_level = TP.DAILY_SERIES
#agg_level = TP.ANNUAL_CYCLE
#agg_level = TP.NONE

agg_operators = [TP.MEAN]


pickle_append = ''
#pickle_append = '1e-4'
#pickle_append = '5e-4'

plot_append = ''
#plot_append = '1e-4'
#plot_append = '5e-4'

plot_cfg = {
    'CLDFNORMI': {
        #'vlevs':    [0.3,0.6,0.9],
        'vlevs':    [0.4,0.9],
        'dx':       6.6,
    },
    'CLCW': {
        'vlevs':    ['lev'],
        'dx':       3.3,
    },
}

vlev = 0.3
#vlev = 0.4
#vlev = 0.5
#vlev = 0.6
#vlev = 0.7
#vlev = 0.8
#vlev = 0.9
#vlev = 1.0


var_names = ['CLCW']
var_names = ['CLDFNORMI']


## analysis members
mem_cfgs = [
    {
        'mem_key':      'COSMO_3.3_ctrl', 
    },
    {
        'mem_key':      'COSMO_3.3_pgw', 
    },
]

ref_key = 'ERA5'
ref2_key = None

dask_chunks = {'lon':50,'lat':50}

# plotting settings
i_force_axis_limits = 1
plot_semilogx = False
i_plot_legend = 1



### set up var_src
var_src_dict = set_up_var_src_dict(inp_base_dir, ana_base_dir,
                                    ANA_NATIVE_domain)


#### plot
nrows = 1
ncols = 2
#figsize = (6,3.5)
figsize = (10,3.5)


arg_subplots_adjust = {
    'left':0.15,
    'bottom':0.20,
    'right':0.85,
    'top':0.95,
    'wspace':0.30,
    'hspace':0.30,
}

