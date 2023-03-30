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
time_periods = time_periods_ana
#time_periods = time_periods_ana_FMA
#time_periods = time_periods_ana_JAS
time_periods_cmip_hist = time_periods_cmip_historical
#time_periods_cmip_hist = time_periods_cmip_historical_FMA
#time_periods_cmip_hist = time_periods_cmip_historical_JAS
time_periods_cmip_ssp = time_periods_cmip_ssp585
#time_periods_cmip_ssp = time_periods_cmip_ssp585_FMA
#time_periods_cmip_ssp = time_periods_cmip_ssp585_JAS

cmip_ind = 10
var_type = 'CLDF_CLDF_PP'
var_type = 'W_CLDF'

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
        'right':0.95,
        'top':0.93,
        'wspace':0.40,
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
    '5x3_twinx': {
        'left':0.05,
        'bottom':0.03,
        'right':0.94,
        'top':0.96,
        'wspace':0.50,
        'hspace':0.25,
    },
    '5x4': {
        'left':0.04,
        'bottom':0.04,
        'right':0.96,
        'top':0.98,
        'wspace':0.30,
        'hspace':0.40,
    },
    '6x4': {
        'left':0.04,
        'bottom':0.04,
        'right':0.96,
        'top':0.98,
        'wspace':0.30,
        'hspace':0.40,
    },
}


models_cmip6 = models_cmip6_cldf#[5:7]
mem_keys_cmip6_historical = ['{}_historical'.format(model) for model in models_cmip6]
mem_keys_cmip6_ssp585 = ['{}_ssp585'.format(model) for model in models_cmip6]
mem_keys_cmip6_change = [{
    'mem_oper':'diff',
    'mem_keys':[
        {
            'mem_key':      '{}_ssp585'.format(model), 
            'time_periods': time_periods_cmip_ssp585,
        },
        {
            'mem_key':      '{}_historical'.format(model), 
            'time_periods': time_periods_cmip_historical,
        },
    ]} for model in models_cmip6
]
mem_keys_cmip6_bias = [{
    'mem_oper':'bias',
    'mem_keys':[
        {
            'mem_key':      '{}_historical'.format(model), 
            'time_periods': time_periods_cmip_historical,
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
cmip_hist = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_historical,
}
cmip_scen = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_ssp585,
}
cmip_change = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_change,
}
cosmo_bias = {
    'mem_oper':     'bias',
    'mem_keys':     [ctrl, era],
}
cosmo_rel = {
    'mem_oper':     'rel0.0001',
    'mem_keys':     [ctrl, era],
}
#bias_mpi = {
#    'mem_oper':     'bias',
#    'mem_keys':     [
#        {
#            'mem_key':      'MPI-ESM1-2-HR_historical', 
#            'time_periods': time_periods_cmip_hist,
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
cosmo_rdheight2_change = {
    'mem_oper':     'diff',
    'mem_keys':     [
        {
            'mem_key':      'COSMO_3.3_pgw_300hPa_rdheight2', 
        },
        {
            'mem_key':      'COSMO_3.3_ctrl_rdheight2', 
        },
    ],
}
mpi_change = {
    'mem_oper':     'diff',
    'mem_keys':     [
        {
            'mem_key':      'MPI-ESM1-2-HR_ssp585', 
            'time_periods': time_periods_cmip_ssp,
        },
        {
            'mem_key':      'MPI-ESM1-2-HR_historical', 
            'time_periods': time_periods_cmip_hist,
        },
    ],
}
cmip_change = {
    'mem_oper':     'diff',
    'mem_keys':     [
        {
            'mem_oper':     'mean',
            'mem_keys':     mem_keys_cmip6_ssp585,
            'time_periods': time_periods_cmip_ssp585,
        },
        {
            'mem_oper':     'mean',
            'mem_keys':     mem_keys_cmip6_historical,
            'time_periods': time_periods_cmip_historical,
        },
    ],
}
cmip_bias = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_bias,
}
cmip_rel = {
    'mem_oper':     'rel0.0001',
    'mem_keys':     mem_keys_cmip6_bias,
}



run_cfgs = {
    'change_clouds_test_cmip6':  {
        'panel_cfgs':    [
            {
                'mem_cfgs':     ['{}_historical'.format(models_cmip6_cldf[cmip_ind+0])],
                'time_periods': time_periods_cmip_historical,
                'title':        '{} HIST'.format(models_cmip6_cldf[cmip_ind+0]),
            },
            {
                'mem_cfgs':     ['{}_ssp585'.format(models_cmip6_cldf[cmip_ind+0])],
                'time_periods': time_periods_cmip_ssp585,
                'title':        '{} SCEN'.format(models_cmip6_cldf[cmip_ind+0]),
            },
            {
                'mem_cfgs':     [
                    {
                        'mem_oper':     'diff',
                        'mem_keys':     [
                            {
                                'mem_key':      '{}_ssp585'.format(models_cmip6_cldf[cmip_ind+0]), 
                                'time_periods': time_periods_cmip_ssp,
                            },
                            {
                                'mem_key':      '{}_historical'.format(models_cmip6_cldf[cmip_ind+0]), 
                                'time_periods': time_periods_cmip_hist,
                            },
                        ],
                    },],
                'title':        '{} SCEN$-$HIST'.format(models_cmip6_cldf[cmip_ind+0]),
                #'var_type':     'CLDF_CLDF',
            },


            {
                'mem_cfgs':     ['{}_historical'.format(models_cmip6_cldf[cmip_ind+1])],
                'time_periods': time_periods_cmip_historical,
                'title':        '{} HIST'.format(models_cmip6_cldf[cmip_ind+1]),
            },
            {
                'mem_cfgs':     ['{}_ssp585'.format(models_cmip6_cldf[cmip_ind+1])],
                'time_periods': time_periods_cmip_ssp585,
                'title':        '{} SCEN'.format(models_cmip6_cldf[cmip_ind+1]),
            },
            {
                'mem_cfgs':     [
                    {
                        'mem_oper':     'diff',
                        'mem_keys':     [
                            {
                                'mem_key':      '{}_ssp585'.format(models_cmip6_cldf[cmip_ind+1]), 
                                'time_periods': time_periods_cmip_ssp,
                            },
                            {
                                'mem_key':      '{}_historical'.format(models_cmip6_cldf[cmip_ind+1]), 
                                'time_periods': time_periods_cmip_hist,
                            },
                        ],
                    },],
                'title':        '{} SCEN$-$HIST'.format(models_cmip6_cldf[cmip_ind+1]),
                #'var_type':     'CLDF_CLDF',
            },


            {
                'mem_cfgs':     ['{}_historical'.format(models_cmip6_cldf[cmip_ind+2])],
                'time_periods': time_periods_cmip_historical,
                'title':        '{} HIST'.format(models_cmip6_cldf[cmip_ind+2]),
            },
            {
                'mem_cfgs':     ['{}_ssp585'.format(models_cmip6_cldf[cmip_ind+2])],
                'time_periods': time_periods_cmip_ssp585,
                'title':        '{} SCEN'.format(models_cmip6_cldf[cmip_ind+2]),
            },
            {
                'mem_cfgs':     [
                    {
                        'mem_oper':     'diff',
                        'mem_keys':     [
                            {
                                'mem_key':      '{}_ssp585'.format(models_cmip6_cldf[cmip_ind+2]), 
                                'time_periods': time_periods_cmip_ssp,
                            },
                            {
                                'mem_key':      '{}_historical'.format(models_cmip6_cldf[cmip_ind+2]), 
                                'time_periods': time_periods_cmip_hist,
                            },
                        ],
                    },],
                'title':        '{} SCEN$-$HIST'.format(models_cmip6_cldf[cmip_ind+2]),
                #'var_type':     'CLDF_CLDF',
            },


            {
                'mem_cfgs':     ['{}_historical'.format(models_cmip6_cldf[cmip_ind+3])],
                'time_periods': time_periods_cmip_historical,
                'title':        '{} HIST'.format(models_cmip6_cldf[cmip_ind+3]),
            },
            {
                'mem_cfgs':     ['{}_ssp585'.format(models_cmip6_cldf[cmip_ind+3])],
                'time_periods': time_periods_cmip_ssp585,
                'title':        '{} SCEN'.format(models_cmip6_cldf[cmip_ind+3]),
            },
            {
                'mem_cfgs':     [
                    {
                        'mem_oper':     'diff',
                        'mem_keys':     [
                            {
                                'mem_key':      '{}_ssp585'.format(models_cmip6_cldf[cmip_ind+3]), 
                                'time_periods': time_periods_cmip_ssp,
                            },
                            {
                                'mem_key':      '{}_historical'.format(models_cmip6_cldf[cmip_ind+3]), 
                                'time_periods': time_periods_cmip_hist,
                            },
                        ],
                    },],
                'title':        '{} SCEN$-$HIST'.format(models_cmip6_cldf[cmip_ind+3]),
                #'var_type':     'CLDF_CLDF',
            },


            {
                'mem_cfgs':     ['{}_historical'.format(models_cmip6_cldf[cmip_ind+4])],
                'time_periods': time_periods_cmip_historical,
                'title':        '{} HIST'.format(models_cmip6_cldf[cmip_ind+4]),
            },
            {
                'mem_cfgs':     ['{}_ssp585'.format(models_cmip6_cldf[cmip_ind+4])],
                'time_periods': time_periods_cmip_ssp585,
                'title':        '{} SCEN'.format(models_cmip6_cldf[cmip_ind+4]),
            },
            {
                'mem_cfgs':     [
                    {
                        'mem_oper':     'diff',
                        'mem_keys':     [
                            {
                                'mem_key':      '{}_ssp585'.format(models_cmip6_cldf[cmip_ind+4]), 
                                'time_periods': time_periods_cmip_ssp,
                            },
                            {
                                'mem_key':      '{}_historical'.format(models_cmip6_cldf[cmip_ind+4]), 
                                'time_periods': time_periods_cmip_hist,
                            },
                        ],
                    },],
                'title':        '{} SCEN$-$HIST'.format(models_cmip6_cldf[cmip_ind+4]),
                #'var_type':     'CLDF_CLDF',
            },
        ],
        'default_var_type': var_type,
        'line_along':       'lat',
        'figsize':          (12, 17),
        'nrows':            5,
        'ncols':            3,
        'adjust_key':       '5x3_twinx',
        'plot_domain':      dom_SA_ana_merid_cs,
        'pan_cbar_pos':     'bottom',
        'pan_cbar_pad':     0.2,
        'kwargs_remove_axis_labels': {
            'remove_level': 0,
        },
    },
}

agg_level = TP.ALL_TIME
#agg_level = TP.ANNUAL_CYCLE



norm_inv = 0

use_cfg = 'change_clouds_test_cmip6'

i_recompute = 1

default_time_periods = time_periods_ana 
#var_type = 'T_CLDW'
#var_type = 'QV_CLDW'
#var_type = 'U_CLDW'
#var_type = 'V_CLDW'
#var_type = 'W_CLDW'
#var_type = 'POTT_CLDW'
#var_type = 'BVF_CLDW'
#var_type = 'UVDIV_CLDW'
#var_type = 'POTTDIV_CLDW'
#var_type = 'EQPOTTDIV_CLDW'
#var_type = 'LATH_CLDW'

run_cfg = run_cfgs[use_cfg]

name_dict = {
    'cfg':use_cfg,
    'norm':norm_inv,
    'cmip':cmip_ind,
    'vartype':var_type,
}


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
    'sub_dir':              'alcs_cmip',
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
        
        if 'var_type' in panel_cfg:
            var_type = panel_cfg['var_type']
        else:
            var_type = run_cfg['default_var_type']

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

