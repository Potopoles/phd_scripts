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
from package.nl_models import models_cmip6, models_cmip6_cldf
from nl_plot_org_ana import nlp
###############################################################################

nrows = 2
ncols = 2

agg_level = TP.ANNUAL_CYCLE
#agg_level = TP.ALL_TIME
#agg_level = TP.SEASONAL_CYCLE

era5 = 'ERA5'
ctrl_3 = 'COSMO_3.3_ctrl'
pgw_3 = 'COSMO_3.3_pgw'
ctrl_12 = 'COSMO_12_ctrl'
mpi_hist = 'MPI-ESM1-2-HR_historical'
mpi_ssp585 = 'MPI-ESM1-2-HR_ssp585'
cmip6 = 'cmip6'
ceres = 'CERES_EBAF'
cmsaf = 'CM_SAF_MSG_AQUA_TERRA'
cmorph = 'CMORPH'
gpm = 'GPM_IMERG'

ana_sea = dom_SA_ana_sea['key']
itcz = dom_ITCZ['key']
itcz = dom_ITCZ['key']

i_recompute = {
    dom_SA_ana_sea['key']:      1,
    dom_ITCZ['key']:            1,
    dom_trades_deep['key']:     1,
    dom_trades_shallow['key']:  1,
    #dom_SA_ana_land['key']:     1,
}

### useful to evaluate
var_name = 'LWUTOA'
var_name = 'ALBEDO'
var_name = 'PP'

#var_name = 'LWDTOA'
#var_name = 'SWNDTOA'
#var_name = 'T2M'
#var_name = 'LTS'

#models_cmip6 = models_cmip6[0:5]
#models_cmip6_cldf = models_cmip6_cldf[3:]
mem_keys_cmip6 = ['{}_historical'.format(model) for model in models_cmip6_cldf]
#mem_keys_cmip6 = ['{}_historical'.format(model) for model in models_cmip6]

mem_cfg = [
    #{
    #    'mem_oper':     'perc0',
    #    'mem_keys':     mem_keys_cmip6,
    #    'time_periods': time_periods_cmip_historical,
    #    'spread':       [0,'lower']
    #},
    #{
    #    'mem_oper':     'perc100',
    #    'mem_keys':     mem_keys_cmip6,
    #    'time_periods': time_periods_cmip_historical,
    #    'spread':       [0,'upper']
    #},
    #{
    #    'mem_oper':     'perc25',
    #    'mem_keys':     mem_keys_cmip6,
    #    'time_periods': time_periods_cmip_historical,
    #    'spread':       [1,'lower']
    #},
    #{
    #    'mem_oper':     'perc75',
    #    'mem_keys':     mem_keys_cmip6,
    #    'time_periods': time_periods_cmip_historical,
    #    'spread':       [1,'upper']
    #},
    #{
    #    'mem_oper':     'mean',
    #    'mem_keys':     mem_keys_cmip6,
    #    'time_periods': time_periods_cmip_historical,
    #    'label':        'CMIP6'
    #},
]
i_use_obs = 0
ref_key = None
ref2_key = None
if i_use_obs:
    if var_name in ['LWUTOA', 'LWDTOA', 'ALBEDO', 'SWNDTOA']:
        mem_cfg.extend([
            {
                'mem_key':      ceres,
                'time_periods': time_periods_ana,
                'label':        'CERES 2007-2010',
            },
            {
                'mem_key':      ceres,
                'time_periods': time_periods_ceres_ebaf,
                'label':        'CERES 2004-2014',
            },
        ])
        mem_cfg.extend([
            {
                'mem_key':      cmsaf,
                'time_periods': time_periods_ana,
                'label':        'CM SAF 2007-2010',
            },
            {
                'mem_key':      cmsaf,
                'time_periods': time_periods_cm_saf_msg_aqua_terra,
                'label':        'CM SAF 2004-2010',
            },
        ])
    elif var_name == 'PP':
        #mem_cfg.extend([cmorph, gpm])
        #ref_key = cmorph
        #ref2_key = gpm
        mem_cfg.extend([
            {
                'mem_key':      gpm,
                'time_periods': time_periods_ana,
                'label':        'GPM 2007-2010',
            },
            {
                'mem_key':      gpm,
                'time_periods': time_periods_gpm_imerg,
                'label':        'GPM 2001-2014',
            },
        ])
else:
    ref_key = ''
    ref2_key = ''

mem_cfg.extend([
    era5,
    #ctrl_3,

    #{
    #    'mem_key':      'MPI-ESM1-2-HR_historical',
    #    'time_periods': time_periods_cmip_historical,
    #    'label':        'MPI-ESM1-2-HR HIST'
    #},
])


name_dict = {
    var_name:'',
    #var_name:'cmip6_climatology',
    #var_name:'paper',
    var_name:'papercmsaf',
}

cfg = {
    'serial_time_plt_sels': [None],
    'sub_dir':              'tl_eval',
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
    'kwargs_remove_axis_labels': {
        'remove_level': 1,
    },
    'kwargs_panel_labels' : {
    },
    'all_panels':
        {
            'ana_number':   9,
            'var_names':    [var_name],
            'time_periods': time_periods_ana,
            'agg_level':    agg_level,
            'plot_ax_cbars':{
                                'abs':  1,
                                'diff': 1,
                            },
            'i_recompute':  0,
            'mem_cfgs':     mem_cfg,
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
        #'2,0':
        #{
        #    'plot_domain':      dom_SA_ana_land,
        #    'i_recompute':      i_recompute[dom_SA_ana_land['key']],
        #    'i_plot_legend':    0,
        #    'title':            dom_SA_ana_land['label'],
        #},

    }
}

