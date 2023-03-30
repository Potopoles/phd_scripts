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
from base.nl_time_periods import *
from package.nl_models import models_cmip6
#from ana_nls.tl_01_eval import mem_cfg as mem_cfgs_eval
#from ana_nls.tl_02_change import mem_cfg as mem_cfgs_change
from nl_plot_org_ana import nlp
###############################################################################

i_use_cmip6     = 1
i_use_mpi       = 1
i_use_era       = 1
i_use_cosmo     = 1
i_use_obs       = 1

#### MEMBERS
##############################################################################

era5 = 'ERA5'
ctrl = 'COSMO_3.3_ctrl'
pgw = 'COSMO_3.3_pgw'
mpi_historical = 'MPI-ESM1-2-HR_historical'
mpi_ssp585 = 'MPI-ESM1-2-HR_ssp585'
ceres = 'CERES_EBAF'
cmsaf = 'CM_SAF_MSG_AQUA_TERRA'
cmorph = 'CMORPH'
gpm = 'GPM_IMERG'

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


#### EVAL
##############################################################################
mem_cfgs_eval = []

if i_use_cosmo:
    mem_cfgs_eval.extend([
        {
            'mem_key':      ctrl,
            'time_periods': time_periods_ana,
        },
    ])
if i_use_era:
    mem_cfgs_eval.extend([
        {
            'mem_key':      era5,
            'time_periods': time_periods_ana,
        },
    ])

if i_use_mpi:
    mem_cfgs_eval.extend([
        {
            'mem_key':      'MPI-ESM1-2-HR_historical',
            'time_periods': time_periods_cmip_historical,
            'label':        'MPI-ESM1-2-HR HIST'
        },
    ])

if i_use_cmip6:
    mem_cfgs_eval.extend([
        {
            'mem_oper':     'perc0',
            'mem_keys':     mem_keys_cmip6_historical,
            'time_periods': time_periods_cmip_historical,
            'spread':       [0,'lower']
        },
        {
            'mem_oper':     'perc100',
            'mem_keys':     mem_keys_cmip6_historical,
            'time_periods': time_periods_cmip_historical,
            'spread':       [0,'upper']
        },
        {
            'mem_oper':     'perc25',
            'mem_keys':     mem_keys_cmip6_historical,
            'time_periods': time_periods_cmip_historical,
            'spread':       [1,'lower']
        },
        {
            'mem_oper':     'perc75',
            'mem_keys':     mem_keys_cmip6_historical,
            'time_periods': time_periods_cmip_historical,
            'spread':       [1,'upper']
        },
        {
            'mem_oper':     'mean',
            'mem_keys':     mem_keys_cmip6_historical,
            'time_periods': time_periods_cmip_historical,
            'label':        'CMIP6'
        },
    ])


#### CHANGE
##############################################################################
mem_cfgs_change = []


if i_use_cosmo:
    mem_cfgs_change.extend([
        {
            'mem_oper':     'diff',
            'mem_keys':     [
                {
                    'mem_key':      pgw,
                    'time_periods': time_periods_ana,
                },
                {
                    'mem_key':      ctrl,
                    'time_periods': time_periods_ana,
                },
            ],
            'label':        'PGW - CTRL',
        },
    ])

### MPI-ESM1-2-HR
if i_use_mpi:
    mem_cfgs_change.extend([
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
    mem_cfgs_change.append(
        {
            'mem_oper':     'mean',
            'mem_keys':     mem_keys_cmip6_change,
            'label':        'CMIP6 SSP5-8.5 - HIST',
        }
    )

    ### CMIP6 spread
    mem_cfgs_change.extend([
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

#### MAIN SETTINGS
##############################################################################

nrows = 5
ncols = 2

agg_level = TP.ANNUAL_CYCLE
#agg_level = TP.ALL_TIME
#agg_level = TP.SEASONAL_CYCLE

i_recompute = {
    dom_SA_ana_sea['key']:      1,
    dom_ITCZ['key']:            1,
    dom_trades_deep['key']:     1,
    dom_trades_shallow['key']:  1,
    dom_SA_ana_land['key']:     1,
}

### these have strong annual cycle
var_name = 'ALBEDO'
var_name = 'LWUTOA'
var_name = 'PP'

name_dict = {
    #var_name:'',
    var_name:'equal_scale',
    #var_name:'reduced',
    #var_name:'obsclim',
}

if i_use_obs:
    if var_name in ['LWUTOA', 'ALBEDO']:
        mem_cfgs_eval.extend([
            {
                'mem_key':      cmsaf,
                'time_periods': time_periods_ana,
            },
            {
                'mem_key':      ceres,
                'time_periods': time_periods_ana,
                #'time_periods': time_periods_ceres,
            },
        ])
        ref_key = ceres
        ref2_key = cmsaf
    elif var_name == 'PP':
        mem_cfgs_eval.extend([
            {
                'mem_key':      gpm,
                'time_periods': time_periods_ana,
                #'time_periods': time_periods_gpm,
            },
            {
                'mem_key':      cmorph,
                'time_periods': time_periods_ana,
            },
        ])
        ref_key = gpm
        ref2_key = cmorph
    else:
        ref_key = ''
        ref2_key = ''
else:
    ref_key = ''
    ref2_key = ''

cfg = {
    'serial_time_plt_sels':     [None],
    'sub_dir':                  'tl_combined',
    'name_dict':                name_dict,
    'figsize':                  (nlp['figsize_lineplot']['{}x{}'.format(
                                        nrows,ncols).format(nrows,ncols)][0],
                                 nlp['figsize_lineplot']['{}x{}'.format(
                                        nrows,ncols).format(nrows,ncols)][1]),
    'nrows':                    nrows,
    'ncols':                    ncols,
    'subplots_adjust_lineplot': '{}x{}'.format(nrows,ncols),
    'i_remove_axis_labels':     1,
    'arg_subplots_adjust':      {
    },
    'all_panels':
        {
            'ana_number':       9,
            'var_names':        [var_name],
            'agg_level':        agg_level,
            'plot_ax_cbars':    {
                                    'abs':  1,
                                    'diff': 1,
                                },
            'i_recompute':      0,
            'i_plot_legend':    0,
            'ref_key':      ref_key,
            'ref2_key':     ref2_key,
        },
    'panels':
    {
        '0,0':
        {
            'plot_domain':      dom_SA_ana_sea,
            'i_recompute':      i_recompute[dom_SA_ana_sea['key']],
            'title':            dom_SA_ana_sea['label'],
            'mem_cfgs':         mem_cfgs_eval,
            'i_plot_legend':    1,
        },
        '0,1':
        {
            'plot_domain':      dom_SA_ana_sea,
            'i_recompute':      i_recompute[dom_SA_ana_sea['key']],
            'title':            'change',
            'mem_cfgs':         mem_cfgs_change,
            'i_plot_legend':    1,
        },
        '1,0':
        {
            'plot_domain':      dom_ITCZ,
            'i_recompute':      i_recompute[dom_ITCZ['key']],
            'title':            dom_ITCZ['label'],
            'mem_cfgs':         mem_cfgs_eval,
        },
        '1,1':
        {
            'plot_domain':      dom_ITCZ,
            'i_recompute':      i_recompute[dom_ITCZ['key']],
            'title':            'change',
            'mem_cfgs':         mem_cfgs_change,
        },
        '2,0':
        {
            'plot_domain':      dom_trades_deep,
            'i_recompute':      i_recompute[dom_trades_deep['key']],
            'title':            dom_trades_deep['label'],
            'mem_cfgs':         mem_cfgs_eval,
        },
        '2,1':
        {
            'plot_domain':      dom_trades_deep,
            'i_recompute':      i_recompute[dom_trades_deep['key']],
            'title':            'change',
            'mem_cfgs':         mem_cfgs_change,
        },
        '3,0':
        {
            'plot_domain':      dom_trades_shallow,
            'i_recompute':      i_recompute[dom_trades_shallow['key']],
            'title':            dom_trades_shallow['label'],
            'mem_cfgs':         mem_cfgs_eval,
        },
        '3,1':
        {
            'plot_domain':      dom_trades_shallow,
            'i_recompute':      i_recompute[dom_trades_shallow['key']],
            'title':            'change',
            'mem_cfgs':         mem_cfgs_change,
        },
        '4,0':
        {
            'plot_domain':      dom_SA_ana_land,
            'i_recompute':      i_recompute[dom_SA_ana_land['key']],
            'title':            dom_SA_ana_land['label'],
            'mem_cfgs':         mem_cfgs_eval,
        },
        '4,1':
        {
            'plot_domain':      dom_SA_ana_land,
            'i_recompute':      i_recompute[dom_SA_ana_land['key']],
            'title':            'change',
            'mem_cfgs':         mem_cfgs_change,
        },
    }
}

