#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    analysis namelist
author			Christoph Heim
"""
###############################################################################
import copy
from datetime import datetime, timedelta
from package.time_processing import Time_Processing as TP
from base.nl_domains import *
from base.nl_time_periods import *
from nl_plot_org_ana import nlp
from package.nl_variables import nlv,get_plt_units
from ana_nls.glob_cfgs import *
###############################################################################
args_subplots_adjust = {
    '5x3': {
        'left':0.11,
        'bottom':0.11,
        'right':0.92,
        'top':0.95,
        'wspace':0,
        'hspace':0,
    },
    '6x3': {
        'left':0.06,
        'bottom':0.09,
        'right':0.95,
        'top':0.95,
        'wspace':0,
        'hspace':0,
    },
}

run_cfgs = {}

##############################################################################

run_cfgs['spatial'] = {
    'fig': {
        'figsize':              (16, 13),
        'nrows':                3,
        'ncols':                4,
        'args_subplots_adjust': {
            'left':     0.09,
            'bottom':   0.10,
            'right':    0.98,
            'top':      0.96,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [0.18,0.18],
            'wspaces':  [0.20,0.20,0.20,0.20],
        },
        'kwargs_remove_axis_labels': {
            'remove_level':     2,
            'xexcept':          {'0,3':2,'0,4':2},
        },
        'label_cfgs': [
        ],
    },
    'glob_pan_cfg':   {
        'ana_number':       22,
        'agg_level':        TP.ALL_TIME,
        'plot_domain':      dom_SA_ana_sea,
        #'plot_domain':      dom_trades,
        'time_periods':     time_periods_ana,
        'time_periods':     time_periods_ana_FMA,
        'time_periods':     time_periods_ana_MJJ,
        'time_periods':     time_periods_ana_ASO,
        'time_periods':     time_periods_ana_NDJ,
        #'time_periods':     get_time_periods_for_month(2008, 8),
        #'time_periods':     time_periods_2008,
        'i_plot_cbar':      1,
        'pan_cbar_pos':     'lower center',
        'pan_cbar_pad':     -4.0,
        'cbar_label_mode':  'var_units',
        'title':            '', 
        'add_bias_labels':  0,
        'i_recompute':      0,
        'mem_cfgs':         [cosmo_change],
        #'plot_type':        'corr',
    },
    'pan_cfgs':    [
        {
            'i_recompute':      0,
            #'var_names':        ['CRESWNDTOA'], 
            #'title':            nlv['CRESWNDTOA']['label'], 
            'var_names':        ['CLCL'], 
            'title':            nlv['CLCL']['label'], 
        },
        {
            'i_recompute':      0,
            'var_names':        ['LTS'], 
            'title':            nlv['LTS']['label'], 
        },
        {
            'i_recompute':      0,
            'var_names':        ['SST'], 
            'title':            nlv['SST']['label'], 
        },
        {
            'i_recompute':      0,
            'var_names':        ['DQVINV'], 
            'title':            nlv['DQVINV']['label'], 
        },
        {
            'i_recompute':      0,
            'var_names':        ['RH@alt=3000'], 
            'title':            '{}'.format(nlv['RH']['label'])+'$_{3km}$',
        },
        {
            'i_recompute':      0,
            'var_names':        ['UV10M'], 
            'title':            nlv['UV10M']['label'], 
        },
        {
            'i_recompute':      0,
            'var_names':        ['SLHFLX'], 
            'title':            nlv['SLHFLX']['label'], 
        },
        {
            'i_recompute':      0,
            'var_names':        ['ENTR'], 
            'title':            nlv['ENTR']['label'], 
        },
        {
            'i_recompute':      0,
            'var_names':        ['INVHGT'], 
            'title':            nlv['INVHGT']['label'], 
        },
        {
            'i_recompute':      0,
            'var_names':        ['W@alt=3000'], 
            'title':            '{}'.format(nlv['W']['label'])+'$_{3km}$',
        },
        #{
        #    'var_names':        ['INVF'], 
        #    'title':            nlv['INVF']['label'], 
        #    #'mem_cfgs':         [ctrl],
        #},

    ],
}


use_cfg = 'spatial'

i_recompute = 1

run_cfg = run_cfgs[use_cfg]

name_dict = {
    'cfg':use_cfg,
    'seas':'FMA',
    'seas':'MJJ',
    'seas':'ASO',
    'seas':'NDJ',
}
if 'name_dict_append' in run_cfg['fig']:
    for key,val in run_cfg['fig']['name_dict_append'].items():
        name_dict[key] = val

nrows = run_cfg['fig']['nrows']
ncols = run_cfg['fig']['ncols']

cfg = {
    'sub_dir':              'lowcloud',
    'name_dict':            name_dict,
    'fig':                  run_cfg['fig'],
    'kwargs_pan_labels' : {
        'shift_right':  -0.18,
        'shift_up':     0.09,
    },

    'panels':
    {
    }
}


#### global optional user-specified arguments
#for attr in [
#    'kwargs_remove_axis_labels',
#    'kwargs_pan_labels',
#    'grid_spec',
#    ]:
#    if attr in run_cfg:
#        cfg[attr] = run_cfg[attr]

for pan_ind,pan_cfg in enumerate(run_cfg['pan_cfgs']):
    #print(mem_cfg)
    col_ind = pan_ind % ncols
    row_ind = int(pan_ind/ncols)
    pan_key = '{},{}'.format(row_ind, col_ind)

    if pan_cfg is not None:
        use_pan_cfg = copy.deepcopy(run_cfg['glob_pan_cfg'])
        for key,val in pan_cfg.items():
            use_pan_cfg[key] = val

        if i_recompute == 0:
            use_pan_cfg['i_recompute'] = 0
        else:
            if 'i_recompute' not in use_pan_cfg:
                use_pan_cfg['i_recompute'] = 0

        cfg['panels'][pan_key] = use_pan_cfg


#print(cfg['pans']['0,0'])
#quit()
