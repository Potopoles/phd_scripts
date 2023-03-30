#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    analysis namelist
author			Christoph Heim
"""
###############################################################################
from datetime import datetime, timedelta
from package.time_processing import Time_Processing as TP
from base.nl_domains import *
from package.nl_models import models_cmip6
from nl_plot_org_ana import nlp
###############################################################################

i_use_cmip6 = 0
i_use_mpi = 0

start_year = 2007
end_year = 2009
start_month = 1
end_month = 12
start_day = 1
end_day = 31
time_periods = [{
    'first_date':datetime(start_year,start_month,start_day),
    'last_date':datetime(end_year,end_month,end_day)
}]



start_year = 1985
end_year = 2014
#end_year = 1985
start_month = 1
end_month = 12
start_day = 1
end_day = 31
time_periods_cmip_historical = [{
    'first_date':datetime(start_year,start_month,start_day),
    'last_date':datetime(end_year,end_month,end_day)
}]

start_year = 2070
end_year = 2099
#end_year = 2070
start_month = 1
end_month = 12
start_day = 1
end_day = 31
time_periods_cmip_ssp585 = [{
    'first_date':datetime(start_year,start_month,start_day),
    'last_date':datetime(end_year,end_month,end_day)
}]

nrows = 3
ncols = 2

agg_level = TP.ANNUAL_CYCLE
#agg_level = TP.ALL_TIME
#agg_level = TP.SEASONAL_CYCLE

ctrl = 'COSMO_3.3_ctrl'
pgw = 'COSMO_3.3_pgw'
mpi_historical = 'MPI-ESM1-2-HR_historical'
mpi_ssp585 = 'MPI-ESM1-2-HR_ssp585'

#models_cmip6 = models_cmip6[0:5]
mem_keys_cmip6_historical = ['{}_historical'.format(model) for model in models_cmip6]
mem_keys_cmip6_ssp585 = ['{}_ssp585'.format(model) for model in models_cmip6]
mem_keys_cmip6_change = []
for model in models_cmip6:
    mem_keys_cmip6_change.append(
        {
            'mem_oper':     'diff',
            'mem_keys':     [
                {
                    'mem_key':      '{}_ssp585'.format(model),
                    'time_periods': time_periods_cmip_ssp585,
                },
                {
                    'mem_key':      '{}_historical'.format(model), 
                    'time_periods': time_periods_cmip_historical,
                },
            ],
        }
    )

i_recompute = {
    dom_SA_ana_sea['key']:      0,
    dom_ITCZ['key']:            0,
    dom_trades_deep['key']:     0,
    dom_trades_shallow['key']:  0,
    dom_SA_ana_land['key']:     1,
}

### these have strong annual cycle
var_name = 'ALBEDO'
var_name = 'LWUTOA'
var_name = 'PP'

mem_cfg = [
    pgw
    #{
    #    'mem_oper':     'diff',
    #    'mem_keys':     [pgw, ctrl],
    #    'label':        'PGW - CTRL',
    #},
]

### MPI-ESM1-2-HR
if i_use_mpi:
    mem_cfg.extend([
        {
            'mem_oper':     'diff',
            'mem_keys':     [
                {
                    'mem_key':      'MPI-ESM1-2-HR_ssp585',
                    'time_periods': time_periods_cmip_ssp585,
                },
                {
                    'mem_key':      'MPI-ESM1-2-HR_historical',
                    'time_periods': time_periods_cmip_historical,
                },
            ],
            'label':        'MPI-ESM1-2-HR SSP5-8.5 - HIST',
        },
    ])

if i_use_cmip6:
    ### CMIP6 ensemble mean
    mem_cfg.append(
        {
            'mem_oper':     'mean',
            'mem_keys':     mem_keys_cmip6_change,
            'label':        'CMIP6 SSP5-8.5 - HIST',
        }
    )

    ### CMIP6 spread
    mem_cfg.extend([
        {
            'mem_oper':     'perc0',
            'mem_keys':     mem_keys_cmip6_change,
            'label':        'CMIP6',
            'spread':       [0,'lower']
        },
        {
            'mem_oper':     'perc100',
            'mem_keys':     mem_keys_cmip6_change,
            'label':        'CMIP6',
            'spread':       [0,'upper']
        },
        {
            'mem_oper':     'perc25',
            'mem_keys':     mem_keys_cmip6_change,
            'label':        'CMIP6',
            'spread':       [1,'lower']
        },
        {
            'mem_oper':     'perc75',
            'mem_keys':     mem_keys_cmip6_change,
            'label':        'CMIP6',
            'spread':       [1,'upper']
        },
    ])




name_dict = {
    var_name:'test',
}

cfg = {
    'serial_time_plt_sels': [None],
    'sub_dir':              'tl_change',
    'name_dict':            name_dict,
    'figsize':              (nlp['figsize_lineplot']['{}x{}'.format(
                                    nrows,ncols).format(nrows,ncols)][0],
                             nlp['figsize_lineplot']['{}x{}'.format(
                                    nrows,ncols).format(nrows,ncols)][1]),
    'nrows':                nrows,
    'ncols':                ncols,
    'subplots_adjust_lineplot':     
                            '{}x{}'.format(nrows,ncols),
    'i_remove_axis_labels': 1,
    'arg_subplots_adjust':  {
                            },
    'all_panels':
        {
            'ana_number':   9,
            'var_names':    [var_name],
            'time_periods': time_periods,
            'agg_level':    agg_level,
            'plot_ax_cbars':{
                                'abs':  1,
                                'diff': 1,
                            },
            'i_recompute':  0,
            'mem_cfgs':     mem_cfg,
        },
    'panels':
    {
        '0,0':
        {
            'plot_domain':      dom_SA_ana_sea,
            'i_recompute':      i_recompute[dom_SA_ana_sea['key']],
            'title':            dom_SA_ana_sea['label'],
        },
        '0,1':
        {
            'plot_domain':      dom_ITCZ,
            'i_recompute':      i_recompute[dom_ITCZ['key']],
            'i_plot_legend':    0,
            'title':            dom_ITCZ['label'],
        },
        '1,0':
        {
            'plot_domain':      dom_trades_deep,
            'i_recompute':      i_recompute[dom_trades_deep['key']],
            'i_plot_legend':    0,
            'title':            dom_trades_deep['label'],
        },
        '1,1':
        {
            'plot_domain':      dom_trades_shallow,
            'i_recompute':      i_recompute[dom_trades_shallow['key']],
            'i_plot_legend':    0,
            'title':            dom_trades_shallow['label'],
        },
        '2,0':
        {
            'plot_domain':      dom_SA_ana_land,
            'i_recompute':      i_recompute[dom_SA_ana_land['key']],
            'i_plot_legend':    0,
            'title':            dom_SA_ana_land['label'],
        },

    }
}

