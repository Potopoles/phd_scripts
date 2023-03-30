
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 005_09_timeline:
author			Christoph Heim
date created    21.11.2020
date changed    14.06.2022
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
from package.functions import get_comb_mem_key
from package.nl_models import models_cmip6, models_cmip6_cldf
from nl_mem_src import *
###############################################################################
## paths
ana_name        = '005_long'
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name, '09_timeline')
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)

## domain average
#pickle_dir      = os.path.join(ana_base_dir, '09')
### dardar lines
##pickle_dir      = os.path.join(ana_base_dir, '12')

models_cmip6 = models_cmip6_cldf
mem_keys_cmip6_hist = ['{}_historical'.format(model) for model in models_cmip6]
mem_keys_cmip6_scen = ['{}_ssp585'.format(model) for model in models_cmip6]
mem_keys_cmip6_change = []
for model in models_cmip6:
    mem_keys_cmip6_change.append(
        {
            'mem_oper':     'diff',
            'mem_keys':     [
                {
                    'mem_key':      '{}_ssp585'.format(model),
                    'time_periods': time_periods_cmip6_scen,
                },
                {
                    'mem_key':      '{}_historical'.format(model), 
                    'time_periods': time_periods_cmip6_hist,
                },
            ],
        }
    )




ANA_NATIVE_domain = dom_SA_3km_large3
plot_domain = dom_SA_3km_large3
plot_domain = dom_SA_ana
plot_domain = dom_SA_ana_land
plot_domain = dom_SA_ana_sea
#plot_domain = dom_ITCZ
#plot_domain = dom_trades_deep
#plot_domain = dom_trades_shallow
#plot_domain = dom_trades

#plot_domain = dom_ITCZ_feedback
#plot_domain = dom_trades_east
#plot_domain = dom_trades_west

## run settings
i_debug = 1
i_plot = 1
i_skip_missing = 1


i_subtract_mean = 0


agg_level = TP.HOURLY_SERIES
agg_level = TP.DIURNAL_CYCLE
agg_level = TP.DAILY_SERIES
#agg_level = TP.ANNUAL_CYCLE
agg_level = TP.MONTHLY_SERIES
#agg_level = TP.YEARLY_SERIES

pickle_append = ''

plot_lines = {
    TP.HOURLY_SERIES:   [TP.MEAN],
    TP.DIURNAL_CYCLE:   [TP.MEAN],
    TP.ANNUAL_CYCLE:    [TP.MEAN],
    TP.DAILY_SERIES:    [TP.MEAN],
    TP.MONTHLY_SERIES:  [TP.MEAN],
    TP.YEARLY_SERIES:   [TP.MEAN],
}
# spread interval limits
plot_spread = {
    #TP.ANNUAL_CYCLE:    [TP.MIN,TP.MAX], 
    TP.DIURNAL_CYCLE:   [TP.P25,TP.P75], 
}


plot_append = ''
#plot_append = 'ceres'
#plot_append = 'diff'
#plot_append = 'change'

#if plot_append == 'diff':
#elif plot_append == 'change':
#else:

time_periods = time_periods_ceres_ebaf
time_periods = time_periods_full
time_periods = time_periods_ana
#time_periods = time_periods_2006
#time_periods = time_periods_2007
#time_periods = time_periods_ana_MAM
#time_periods = get_time_periods_for_month(2006, 8)

#start_date = datetime(2006,8,1)
#end_date = datetime(2006,12,31)
#time_periods = [{
#    'first_date':start_date,
#    'last_date':end_date
#}]

mem_cfgs = [
    #'CM_SAF_MSG_AQUA_TERRA',
    #'CERES_EBAF',
    #'GPM_IMERG',
    #'COSMO_3.3_ctrl',
    #'COSMO_3.3_pgw',
    #'COSMO_3.3_pgw_itcz',

    {
        'mem_oper':     'diff',
        'mem_keys':     ['COSMO_3.3_pgw', 'COSMO_3.3_ctrl'], 
        'label':        'PGW$-$CTRL',
    },
    #{
    #    'mem_oper':     'diff',
    #    'mem_keys':     ['COSMO_3.3_itcz_pgw', 'COSMO_3.3_ctrl'], 
    #    'label':        'PGW ITCZ$-$CTRL',
    #},
    #{
    #    'mem_oper':     'diff',
    #    'mem_keys':     ['COSMO_3.3_pgw2', 'COSMO_3.3_ctrl'], 
    #    'label':        'PGW2$-$CTRL',
    #},
    {
        'mem_oper':     'diff',
        'mem_keys':     ['COSMO_3.3_pgw3', 'COSMO_3.3_ctrl'], 
        'label':        'PGW3$-$CTRL',
    },

    #{
    #    'mem_oper':     'mean',
    #    'mem_keys':     mem_keys_cmip6_change,
    #    'label':        'SCEN$-$HIST',
    #}

    #'CMORPH',
    #{
    #    'mem_key':      'COSMO_3.3_ctrl',
    #    'label':        'CTRL',
    #},
    #{
    #    'mem_key':      'COSMO_3.3_pgw',
    #    'label':        'PGW',
    #},
    ##'COSMO_3.3_ctrl',

    #{
    #    'mem_oper':     'diff',
    #    'mem_keys':     ['COSMO_3.3_pgw', 'COSMO_3.3_ctrl'], 
    #},
    #{
    #    'mem_oper':     'diff',
    #    'mem_keys':     ['COSMO_3.3_pgw_OLD', 'COSMO_3.3_ctrl'], 
    #    'label':        'old pgw',
    #},
    #{
    #    'mem_oper':     'diff',
    #    'mem_keys':     ['COSMO_3.3_pgw_300hPa', 'COSMO_3.3_ctrl'], 
    #    'label':        '300hPa',
    #},
    #{
    #    'mem_oper':     'diff',
    #    'mem_keys':     ['COSMO_3.3_pgw_rdheight2', 'COSMO_3.3_ctrl_rdheight2'], 
    #    'label':        'rdh2',
    #},

]



ref_key = None
ref2_key = None
#ref_key = 'CM_SAF_MSG_AQUA_TERRA'
#ref2_key = 'CERES_EBAF'
#ref_key = 'GPM_IMERG'
#ref2_key = 'CMORPH'

dask_chunks = {'lon':50,'lat':50}

#### plot
i_draw_grid = 0

nrows = 1
ncols = 1
stretch = 1.4
figsize = (3.5*stretch,2.5*stretch)

arg_subplots_adjust = {
    'left':0.18,
    'bottom':0.13,
    'right':0.98,
    'top':0.95,
    'wspace':0.10,
    'hspace':0.30,
}
