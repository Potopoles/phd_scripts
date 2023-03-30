#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    plotting namelist for 005_20_cld3d:
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
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name, '20_cld3d')
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)
ANA_NATIVE_domain = dom_SA_3km_large3

plot_domain = dom_trades_full
plot_domain = dom_trades_west
#plot_domain = dom_trades_east
#plot_domain = dom_test

## run settings
i_debug = 2
i_plot = 1
i_skip_missing = 1

time_periods = time_periods_2007
#time_periods = time_periods_ana
time_periods = get_time_periods_for_month(2007, 9)

time_periods = [{
    'first_date':datetime(2007,8,1),
    'last_date':datetime(2007,9,30)
}]

time_periods = [
    {
    'first_date':datetime(2007,1,15),
    'last_date':datetime(2007,1,17)
    },
    #{
    #'first_date':datetime(2007,5,24),
    #'last_date':datetime(2007,5,31)
    #},
]



agg_level = TP.ALL_TIME
#agg_level = TP.DAILY_SERIES
#agg_level = TP.ANNUAL_CYCLE
#agg_level = TP.NONE

agg_operators = [TP.MEAN]


filter_type = 'all_clouds'
filter_type = 'deep_clouds'
filter_type = 'shallow_clouds'

#filter_type = 'inversion_clouds'

pickle_append = ''

plot_append = ''

main_var_name = 'QVDIV'
#main_var_name = 'QVHDIV'
#main_var_name = 'QVVDIV'
#main_var_name = 'W'
main_var_name = 'QC'

var_names = ['INVHGT',main_var_name]

comp_var_names = [
    'CORE_CLOUD_AREA','CORE_TANGMEAN_{}'.format(main_var_name),
    'STRAT_CLOUD_AREA','STRAT_TANGMEAN_{}'.format(main_var_name),
    'BOTH_CLOUD_AREA','BOTH_TANGMEAN_{}'.format(main_var_name),
]


#cell_size = 6.6**2
model_dx = 6.6
max_dist_core_strat = 100

#W_thresh_core = 0.01 # leads to too large (too connected) cores
#W_thresh_core = 0.05 # has connected cores but still captures some of the Sc cores
#W_thresh_core = 0.10 # perfect for trades_west but misses stratocumulus cores
W_thresh_core = 0.15/3600 #  W/invhgt

## analysis members
mem_cfgs = [
    {
        'mem_key':      'COSMO_3.3_ctrl', 
    },
    {
        'mem_key':      'COSMO_3.3_pgw', 
    },
]

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
ncols = 3
#figsize = (6,5)
#figsize = (12,4)
figsize = (16,4)


arg_subplots_adjust = {
    'left':0.05,
    'bottom':0.15,
    'right':0.95,
    'top':0.95,
    'wspace':0.30,
    #'hspace':0.30,
}

