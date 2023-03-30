#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    plotting namelist for 005_16_skewt:
author			Christoph Heim
date changed    13.06.2022
date changed    13.06.2022
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
from package.nl_models import models_cmip6, models_cmip6_cldf
from nl_mem_src import *
from nl_var_src import set_up_var_src_dict
###############################################################################
## paths
ana_name        = '005_long'
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name, '16_skewt')
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)
ANA_NATIVE_domain = dom_SA_3km_large3

plot_domain = dom_SA_ana
#plot_domain = dom_SA_ana_sea
plot_domain = dom_ITCZ_feedback

## run settings
i_debug = 1
i_plot = 1
i_skip_missing = 1

p_lims = (1000,200)
#alt_lims = (0,18000) 
##alt_lims = (0,30000) 
##rel_alt_lims = (0.0,1.5) 
#rel_alt_lims = (0.0,2) 

time_periods = time_periods_ana
#time_periods = time_periods_2007

time_periods = [{
    'first_date':datetime(2008,8,1),
    'last_date':datetime(2008,8,20)
}]

agg_level = TP.ALL_TIME
#agg_level = TP.DAILY_SERIES
#agg_level = TP.ANNUAL_CYCLE
#agg_level = TP.NONE

agg_operators = [TP.MEAN]


plot_append = ''
#plot_append = 'abs'
#plot_append = 'change'


## analysis members
mem_cfgs = [
    #{
    #    'mem_key':      'ACCESS-CM2_historical', 
    #},
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
#figsize = (12,4.5)
figsize = (9,3.5)


arg_subplots_adjust = {
    'left':0.10,
    'bottom':0.10,
    'right':0.97,
    'top':0.98,
    'wspace':0.30,
    'hspace':0.30,
}

