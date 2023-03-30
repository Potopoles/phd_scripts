#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 005_22:
author			Christoph Heim
date created    24.01.2023
date changed    24.01.2023
usage			import in another script
"""
###############################################################################
import os
from datetime import datetime, timedelta
from base.nl_global import (plot_glob_base_dir, inp_glob_base_dir,
                               ana_glob_base_dir)
from base.nl_domains import *
from base.nl_time_periods import *
from package.time_processing import Time_Processing as TP
from package.nl_models import models_cmip6, models_cmip6_cldf
from nl_mem_src import *
from nl_plot_22 import nlp
#from ana_nls.glob_cfgs import (
#    cmip6_change_FMA,
#    cmip6_change_MJJ,
#    cmip6_change_ASO,
#    cmip6_change_NDJ,
#)
###############################################################################

## paths
ana_name        = '005_long'
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name, '22_lowcloud')
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)

ANA_NATIVE_domain = dom_SA_3km_large3
#plot_domain = dom_gulf_2
#plot_domain = dom_SA_3km_large3
plot_domain = dom_SA_ana_sea
#plot_domain = dom_trades_deep
#plot_domain = dom_trades_shallow
#plot_domain = dom_trades

#plot_domain = dom_trades_east
#plot_domain = dom_trades_west
#plot_domain = dom_trades_full

#plot_domain = dom_SA_ana_merid_cs

#plot_domain = dom_tuning

## run settings
i_debug = 2
i_plot = 1
i_skip_missing = 1
i_coarse_grain = 0
i_coarse_grain = 100
i_coarse_grain = 300
#i_coarse_grain = 500


#agg_level = TP.NONE
agg_level = TP.ALL_TIME
#agg_level = TP.DIURNAL_CYCLE
#agg_level = TP.ANNUAL_CYCLE
#agg_level = TP.SEASONAL_CYCLE
#agg_level = TP.MONTHLY_SERIES

agg_operators = [TP.MEAN]

pickle_append = ''
#pickle_append = 'cg50'
#pickle_append = 'cg100'

plot_append = ''

time_periods = time_periods_ana
#time_periods = get_time_periods_for_month(2008, 8)
#time_periods = time_periods_2008

time_periods = time_periods_ana_FMA
time_periods = time_periods_ana_MJJ
time_periods = time_periods_ana_ASO
time_periods = time_periods_ana_NDJ

#start_date = datetime(2007,8,1)
#end_date = datetime(2007,8,10)
#time_periods = [{
#    'first_date':start_date,
#    'last_date':end_date
#}]

plot_type = 'spatial'
#plot_type = 'corr'
#plot_type = 'corr2d'

corr_var = 'CRESWNDTOA'
corr_var = 'CLCL'

var_names = ['LTS','CRESWNDTOA','DQVINV']
#var_names = ['LTS','DQVINV']
#var_names = ['CRESWNDTOA']
#var_names = ['W@alt=3000']
#var_names = ['RH@alt=3000']
#var_names = ['UV10M']
var_names = ['LTS','CLCL','CRESWNDTOA','SST','DQVINV','W@alt=3000','RH@alt=3000','UV10M']
#var_names = ['CRESWNDTOA']
#var_names = ['CLCL']
#var_names = ['DQVINV']
#var_names = ['SST']
var_names = ['SLHFLX']
var_names = ['ENTR']
#var_names = ['INVHGT']
var_names = ['SLHFLX','ENTR','INVHGT']

# grid points with INVF below therhold will be masked in average
invf_threshold = 0.10

#var_names = [
#    'CRESWNDTOA',
#    'LTS', 
#    'DQVINV',
#]

models_cmip6 = models_cmip6_cldf#[2:]
mem_keys_cmip6_hist = ['{}_historical'.format(model) for model in models_cmip6]
mem_keys_cmip6_scen = ['{}_ssp585'.format(model) for model in models_cmip6]


mem_cfgs = [
    'COSMO_3.3_ctrl',
    'COSMO_3.3_pgw3',
    #'COSMO_3.3_pgw',
    #{
    #    'mem_oper':     'diff',
    #    'mem_keys':     ['COSMO_3.3_pgw3', 'COSMO_3.3_ctrl'], 
    #    'label':        'PGW3$-$CTRL',
    #},
]


dask_chunks = {'lon':50,'lat':50}

#### plot
nrows = 1
ncols = 1
figsize = (4.5,3)

#nrows = 2
#ncols = 2
#figsize = (9,6)


title = None # take automatic title
#title = '' # manually set title




i_plot_cbar = 1
pan_cbar_pos = 'center right'
pan_cbar_pad = -1
pan_cbar_pos = 'lower center'
pan_cbar_pad = -4
cbar_label_mode = 'both'
#cbar_label_mode = 'var_units'
#cbar_label_mode = 'var_name'
#cbar_label_mode = 'neither'

add_bias_labels = 1

plot_glob_cbar = 0

arg_subplots_adjust = nlp['subplts_cfgs']['{}x{}'.format(nrows,ncols)]
glob_cbar_pos = [0.20, 0.12, 0.73, 0.03]
