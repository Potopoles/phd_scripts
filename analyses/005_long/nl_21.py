#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 005_21_buoy:
author			Christoph Heim
date created    21.07.2022
date changed    21.07.2022
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
from package.nl_models import models_cmip6, models_cmip6_cldf
###############################################################################
## paths
ana_name        = '005_long'
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name, '21_buoy')
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)

models_cmip6 = models_cmip6_cldf[0:2]
mem_keys_cmip6_hist = ['{}_historical'.format(model) for model in models_cmip6]
mem_keys_cmip6_scen = ['{}_ssp585'.format(model) for model in models_cmip6]
mem_keys_cmip6_change = [{
    'mem_oper':'diff',
    'mem_keys':[
        {
            'mem_key':      '{}_ssp585'.format(model), 
            'time_periods': time_periods_cmip6_scen,
        },
        {
            'mem_key':      '{}_historical'.format(model), 
            'time_periods': time_periods_cmip6_hist,
        },
    ]} for model in models_cmip6
]
cmip_hist = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_hist,
}
cmip_scen = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_scen,
}
cmip_change = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_change,
}
mpi_change = {
    'mem_oper':'diff',
    'mem_keys':[
        {
            'mem_key':      '{}_ssp585'.format('MPI-ESM1-2-HR'), 
            'time_periods': time_periods_cmip6_scen,
        },
        {
            'mem_key':      '{}_historical'.format('MPI-ESM1-2-HR'), 
            'time_periods': time_periods_cmip6_hist,
        },
    ]
}

ANA_NATIVE_domain = dom_SA_3km_large3
#plot_domain = dom_SA_ana_sea
#plot_domain = dom_trades_east
#plot_domain = dom_trades_west
plot_domain = dom_ITCZ_feedback

## run settings
i_debug = 2
i_plot = 1
i_skip_missing = 1

alt_lims = (0,18000) 
#alt_lims = (0,30000) 
#rel_alt_lims = (0.0,1.5) 
rel_alt_lims = (0.0,2) 

time_periods = time_periods_ana
#time_periods = time_periods_2007
#time_periods = get_time_periods_for_month(2007, 8)
#time_periods = time_periods_ana_SON

#time_periods = [{
#    'first_date':datetime(2008,8,1),
#    'last_date':datetime(2008,8,20)
#}]



agg_level = TP.ALL_TIME
#agg_level = TP.DAILY_SERIES
#agg_level = TP.ANNUAL_CYCLE
#agg_level = TP.NONE

agg_operators = [TP.MEAN]


plot_append = ''
#plot_append = 'abs'
#plot_append = 'change'

legend_type = 'member'
legend_type = 'variable'

plot_var_names = ['TV','UPDTV']
#plot_var_names = ['UPDTV']
plot_var_names = ['UPDBUOYI']
plot_var_names = ['PARCBUOYI']
plot_var_names = ['UPDBUOYI','PARCBUOYI']
#plot_var_names = ['TV','PARCTV','UPDTV']
#plot_var_names = ['PARCTV']
plot_var_names = ['TV']

## analysis members
mem_cfgs = [
    #{
    #    'mem_key':      'COSMO_3.3_ctrl', 
    #},
    #{
    #    'mem_key':      'COSMO_3.3_pgw', 
    #},

    {
        'mem_oper':     'diff',
        'mem_keys':     ['COSMO_3.3_pgw', 'COSMO_3.3_ctrl'], 
    },

    #mpi_change,
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
ncols = 1
#figsize = (12,4.5)
figsize = (4,4)


arg_subplots_adjust = {
    'left':0.18,
    'bottom':0.15,
    'right':0.97,
    'top':0.93,
    'wspace':0.10,
    'hspace':0.30,
}

