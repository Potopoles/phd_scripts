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
from package.nl_variables import nlv
###############################################################################
args_subplots_adjust = {
    '1x3': {
        'left':0.05,
        'bottom':0.07,
        'right':0.95,
        'top':0.96,
        'wspace':0.40,
        'hspace':0.40,
    },
    '2x3': {
        'left':0.05,
        'bottom':0.10,
        'right':0.90,
        'top':0.93,
        'wspace':0.50,
        'hspace':0.40,
    },
    '2x4': {
        'left':0.05,
        'bottom':0.10,
        'right':0.95,
        'top':0.93,
        'wspace':0.40,
        'hspace':0.40,
    },
    '3x3': {
        'left':0.05,
        'bottom':0.07,
        'right':0.94,
        'top':0.96,
        'wspace':0.40,
        'hspace':0.40,
    },
    '3x3_twinx': {
        'left':0.05,
        'bottom':0.03,
        'right':0.94,
        'top':0.96,
        'wspace':0.50,
        'hspace':0.25,
    },
    '3x4': {
        'left':0.05,
        'bottom':0.10,
        'right':0.95,
        'top':0.93,
        'wspace':0.40,
        'hspace':0.40,
    },
    '4x3': {
        'left':0.05,
        'bottom':0.07,
        'right':0.94,
        'top':0.96,
        'wspace':0.40,
        'hspace':0.40,
    },
    '4x3_twinx': {
        'left':0.05,
        'bottom':0.03,
        'right':0.94,
        'top':0.96,
        'wspace':0.50,
        'hspace':0.25,
    },
    '4x4': {
        'left':0.05,
        'bottom':0.10,
        'right':0.95,
        'top':0.93,
        'wspace':0.40,
        'hspace':0.40,
    },
    #'4x6': {
    #    'left':0.04,
    #    'bottom':0.05,
    #    'right':0.97,
    #    'top':0.97,
    #    'wspace':0.30,
    #    'hspace':0.40,
    #},
    '6x4': {
        'left':0.04,
        'bottom':0.04,
        'right':0.96,
        'top':0.98,
        'wspace':0.30,
        'hspace':0.40,
    },
}


rel_oper = 'rel0.00000000001'

models_cmip6 = models_cmip6_cldf#[0:10]
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
mem_keys_cmip6_rel_change = [{
    'mem_oper':rel_oper,
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
mem_keys_cmip6_bias = [{
    'mem_oper':'bias',
    'mem_keys':[
        {
            'mem_key':      '{}_historical'.format(model), 
            'time_periods': time_periods_cmip6_hist,
        },
        {
            'mem_key':      'ERA5', 
            'time_periods': time_periods_ana,
        },
    ]} for model in models_cmip6
]

ctrl = {
    'mem_key':      'COSMO_3.3_ctrl', 
}
ctrl_rdheight2_spubc1 = {
    'mem_key':      'COSMO_3.3_ctrl_rdheight2_spubc1', 
}
ctrl_rdheight2 = {
    'mem_key':      'COSMO_3.3_ctrl_rdheight2', 
}
pgw = {
    'mem_key':      'COSMO_3.3_pgw', 
}
pgw_rdheight2 = {
    'mem_key':      'COSMO_3.3_pgw_rdheight2', 
}
era = {
    'mem_key':      'ERA5', 
}
mpi_hist = {
    'mem_key':      'MPI-ESM1-2-HR_historical', 
}
mpi_scen = {
    'mem_key':      'MPI-ESM1-2-HR_ssp585', 
}
cmip6_hist = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_hist,
}
cmip6_scen = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_scen,
}
cmip6_change = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_change,
}
cmip6_rel_change = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_rel_change,
}
cosmo_bias = {
    'mem_oper':     'bias',
    'mem_keys':     [ctrl, era],
}
cosmo_rel_bias = {
    'mem_oper':     rel_oper,
    'mem_keys':     [ctrl, era],
}
#bias_mpi = {
#    'mem_oper':     'bias',
#    'mem_keys':     [
#        {
#            'mem_key':      'MPI-ESM1-2-HR_hist', 
#            'time_periods': time_periods_cmip6_hist,
#        },
#        {
#            'mem_key':      'ERA5', 
#            'time_periods': time_periods,
#        },
#    ],
#}
cosmo_change = {
    'mem_oper':     'diff',
    'mem_keys':     [pgw, ctrl],
    #'time_periods': time_periods,
}
cosmo_rel_change = {
    'mem_oper':     'rel0.00000000001',
    'mem_keys':     [pgw, ctrl],
}
mpi_change = {
    'mem_oper':     'diff',
    'mem_keys':     [
        {
            'mem_key':      'MPI-ESM1-2-HR_ssp585', 
            'time_periods': time_periods_cmip6_scen,
        },
        {
            'mem_key':      'MPI-ESM1-2-HR_historical', 
            'time_periods': time_periods_cmip6_hist,
        },
    ],
}
mpi_rel_change = {
    'mem_oper':     rel_oper,
    'mem_keys':     [
        {
            'mem_key':      'MPI-ESM1-2-HR_ssp585', 
            'time_periods': time_periods_cmip6_scen,
        },
        {
            'mem_key':      'MPI-ESM1-2-HR_historical', 
            'time_periods': time_periods_cmip6_hist,
        },
    ],
}
cmip6_change = {
    'mem_oper':     'diff',
    'mem_keys':     [
        {
            'mem_oper':     'mean',
            'mem_keys':     mem_keys_cmip6_scen,
            'time_periods': time_periods_cmip6_scen,
        },
        {
            'mem_oper':     'mean',
            'mem_keys':     mem_keys_cmip6_hist,
            'time_periods': time_periods_cmip6_hist,
        },
    ],
}
cmip6_bias = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_bias,
}



run_cfgs = {
    'merid_cs':  {
        'panel_cfgs':    [
            {
                'mem_cfgs':     ['ERA5'],
                'title':        'ERA5', 
            },
            {
                'mem_cfgs':     [cosmo_bias],
                #'mem_cfgs':     [cosmo_rel],
                'title':        'CTRL - ERA5', 
            },
            {
                'mem_cfgs':     [cmip6_bias],
                'title':        'CMIP6 - ERA5', 
            },

            {
                'mem_cfgs':     ['COSMO_3.3_ctrl'],
                'title':        'CTRL' ,
            },
            {
                'mem_cfgs':     ['COSMO_3.3_pgw'],
                'title':        'PGW' ,
            },
            {
                'mem_cfgs':     [cosmo_change],
                'title':        'PGW - CTRL', 
            },

        ],
        'line_along':       'lat',
        'figsize':          (12, 10),
        'nrows':            4,
        'ncols':            3,
        'adjust_key':       '4x3',
        'plot_domain':      dom_SA_ana_merid_cs,
    },

    'change':  {
        'panel_cfgs':    [
            {
                'mem_cfgs':     ['COSMO_3.3_ctrl'],
                'title':        'CTRL' ,
            },
            {
                'mem_cfgs':     ['COSMO_3.3_pgw'],
                'title':        'PGW' ,
            },
            {
                'mem_cfgs':     [cosmo_change],
                'title':        'PGW - CTRL', 
                #'mem_cfgs':     [cosmo_rel_change],
                #'title':        'PGW / CTRL - 1', 
            },
        ],
        'line_along':       'lat',
        'figsize':          (13, 5),
        'nrows':            2,
        'ncols':            3,
        'adjust_key':       '2x3',
        'plot_domain':      dom_SA_ana_merid_cs,
    },
}
agg_level = TP.ALL_TIME
#agg_level = TP.ANNUAL_CYCLE


#var_type = 'CLDF_CLDF'
#var_type = 'POTTDIV_CLDF'
#var_type = 'CLDPOTTDIV_CLDF'
#var_type = 'CSPOTTDIV_CLDF'
#var_type = 'CSUVDIV_CLDF'
#var_type = 'CLDUVDIV_CLDF'
#var_type = 'LATH_CLDF'
#var_type = 'CSLATH_CLDF'
#var_type = 'CLDLATH_CLDF'
#var_type = 'BVF_CLDF'
#var_type = 'V_CLDF'
#var_type = 'W_CLDF'
#var_type = 'T_CLDF'
#var_type = 'QVHDIV_CLDF'
#var_type = 'QVVDIV_CLDF'
#var_type = 'QVDIV_CLDF'
#var_type = 'POTTDIV3_CLDF'
var_type = 'POTTDIV_CLDF'
#var_type = 'POTTDIV4_CLDF'
#var_type = 'CSPOTTDIV_CLDF'
#var_type = 'NCOLIPOTTDIV3_CLDF'
#var_type = 'NCOLIPOTTDIV_CLDF'
#var_type = 'CLDPOTTDIV_CLDF'
#var_type = 'POTTHDIV3_CLDF'
#var_type = 'POTTHDIV_CLDF'
#var_type = 'POTTVDIV3_CLDF'
#var_type = 'POTTVDIV_CLDF'
#var_type = 'CLDW_CLDF'
#var_type = 'CSW_CLDF'
#var_type = 'EQPOTTDIV3_CLDF'
#var_type = 'CSEQPOTTDIV3_CLDF'
#var_type = 'CLDEQPOTTDIV3_CLDF'
#var_type = 'RH0LCSPOTTDIV3_CLDF'
#var_type = 'RH1LCSPOTTDIV3_CLDF'
#var_type = 'RH2LCSPOTTDIV3_CLDF'
#var_type = 'RH0GCSPOTTDIV3_CLDF'
#var_type = 'RH1GCSPOTTDIV3_CLDF'
#var_type = 'RH2GCSPOTTDIV3_CLDF'
#var_type = 'QIDIV3_CLDF'
#var_type = 'QV_CLDF'
#var_type = 'NCOLIQV_CLDF'

i_use_cmip = 0

norm_inv = 0

use_cfg = 'merid_cs'
use_cfg = 'change'

i_recompute = 1

default_time_periods = time_periods_ana 
#default_time_periods = time_periods_2007
#default_time_periods = get_time_periods_for_month(2007, 8)
#default_time_periods = time_periods_ana_DJF
#default_time_periods = time_periods_ana_MAM
#default_time_periods = time_periods_ana_JJA
#default_time_periods = time_periods_ana_SON

name_dict = {
    'cfg':use_cfg,
    'norm':norm_inv,
    'var':var_type,
    #'month':'200608',
    #'month':'DJF',
    #'month':'MAM',
    #'month':'JJA',
    #'month':'SON',
}

if i_use_cmip:
    run_cfgs[use_cfg]['panel_cfgs'].extend([
            {
                'mem_cfgs':     [cmip6_hist],
                'time_periods': time_periods_cmip6_hist,
                'title':        'CMIP6 HIST', 
            },
            {
                'mem_cfgs':     [cmip6_scen],
                'time_periods': time_periods_cmip6_scen,
                'title':        'CMIP6 SCEN', 
            },
            {
                'mem_cfgs':     [cmip6_change],
                'title':        'CMIP6 SCEN - HIST', 
                #'mem_cfgs':     [cmip6_rel_change],
                #'title':        'CMIP6 SCEN / HIST - 1', 
            },

            #{
            #    'mem_cfgs':     [mpi_hist],
            #    'time_periods': time_periods_cmip6_hist,
            #    'title':        'MPI-ESM HIST', 
            #},
            #{
            #    'mem_cfgs':     [mpi_scen],
            #    'time_periods': time_periods_cmip6_scen,
            #    'title':        'MPI-ESM SCEN', 
            #},
            #{
            #    #'mem_cfgs':     [mpi_change],
            #    #'title':        'MPI-ESM SCEN - HIST', 
            #    'mem_cfgs':     [mpi_rel_change],
            #    'title':        'MPI-ESM SCEN / HIST - 1', 
            #},
    ])


run_cfg = run_cfgs[use_cfg]

#run_cfg['panel_cfgs'][1] = None
#run_cfg['panel_cfgs'][5] = None



if run_cfg['plot_domain']['key'] in ['dom_trades_deep', 'dom_trades_shallow', 'dom_trades']:
    alt_lims = (0,4000) 
elif run_cfg['plot_domain']['key'] in ['dom_ITCZ', 'dom_NS_cs', 'dom_NS_cs_afr']:
    alt_lims = (0,18000) 
    #alt_lims = (0,6000) 
else:
    raise NotImplementedError()

if agg_level == TP.ALL_TIME:
    serial_time_plt_sels = [None]
elif agg_level == TP.ANNUAL_CYCLE:
    serial_time_plt_sels = []
    for month in range(1,13,1):
        serial_time_plt_sels.append({'month':month})
elif agg_level == TP.SEASONAL_CYCLE:
    serial_time_plt_sels = []
    for season in ['DJF', 'MAM', 'JJA', 'SON']:
        serial_time_plt_sels.append({'season':season})
elif agg_level == TP.DIURNAL_CYCLE:
    serial_time_plt_sels = []
    for hour in range(0,23,3):
        serial_time_plt_sels.append({'hour':hour})
else:
    raise NotImplementedError()

nrows = run_cfg['nrows']
ncols = run_cfg['ncols']

if run_cfg['line_along'] == 'lat':
    average_along = 'lon'
elif run_cfg['line_along'] == 'lon':
    average_along = 'lat'
else:
    raise NotImplementedError()
    

cfg = {
    'serial_time_plt_sels': serial_time_plt_sels,
    'sub_dir':              'alcs_vars',
    'name_dict':            name_dict,
    'figsize':              run_cfg['figsize'],
    'nrows':                nrows,
    'ncols':                ncols,
    'subplots_adjust_spatial':
                            '1x1', # dummy
    'args_subplots_adjust': args_subplots_adjust[run_cfg['adjust_key']],
    'kwargs_remove_axis_labels': {
        'remove_level': 1,
    },
    'kwargs_panel_labels' : {
        'shift_right':  -0.18,
        'shift_up':     0.06,
    },

    'all_panels':
        {
            'ana_number':   4,
            'agg_level':    agg_level,
            'i_recompute':  i_recompute,
            'plot_domain':  run_cfg['plot_domain'],
            'alt_lims':     alt_lims,
            'line_along':   run_cfg['line_along'],
            'line_at':      slice(run_cfg['plot_domain'][average_along].start+1,
                                run_cfg['plot_domain'][average_along].stop-1),
        },
    'panels':
    {
    }
}


### global optional user-specified arguments
if 'kwargs_remove_axis_labels' in run_cfg:
    cfg['kwargs_remove_axis_labels'] = run_cfg['kwargs_remove_axis_labels']
if 'kwargs_panel_labels' in run_cfg:
    cfg['kwargs_panel_labels'] = run_cfg['kwargs_panel_labels']

### all_panel optional user-specified arguments
if 'pan_cbar_pos' in run_cfg:
    cfg['all_panels']['pan_cbar_pos'] = run_cfg['pan_cbar_pos']
if 'pan_cbar_pad' in run_cfg:
    cfg['all_panels']['pan_cbar_pad'] = run_cfg['pan_cbar_pad']
        


mi = 0
for panel_cfg in run_cfg['panel_cfgs']:
    #print(mem_cfg)
    col_ind = mi % ncols
    row_ind = int(mi/ncols)
    pan_key = '{},{}'.format(row_ind, col_ind)

    if panel_cfg is not None:
        print(panel_cfg)
        
        if 'time_periods' in panel_cfg:
            time_periods = panel_cfg['time_periods']
        else:
            time_periods = default_time_periods


        pan_dict = {
            'var_type':     var_type,
            'norm_inv':     norm_inv,
            'mem_cfgs':     panel_cfg['mem_cfgs'],
            #'title':        '{}: CTRL'.format(nlv[var_type.split('_')[0]]['label']),
            'time_periods': time_periods
        }

        if 'title' in panel_cfg:
            pan_dict['title'] = panel_cfg['title']

        cfg['panels'][pan_key] = pan_dict

    mi += 1
#print(cfg['panels']['0,0'])
#quit()

