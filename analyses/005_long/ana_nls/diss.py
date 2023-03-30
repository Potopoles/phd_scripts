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
    #'5x3': {
    #    'left':0.11,
    #    'bottom':0.11,
    #    'right':0.92,
    #    'top':0.95,
    #    'wspace':0,
    #    'hspace':0,
    #},
}

run_cfgs = {}


run_cfgs['ChA_tuning'] = {
    'fig': {
        'figsize':              (12.5, 19),
        'nrows':                11,
        'ncols':                5,
        'args_subplots_adjust': {
            'left':     0.15,
            'bottom':   0.07,
            'right':    0.99,
            'top':      0.94,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10],
            'wspaces':  [0.06,0.06,0.06,0.06],
        },
        'kwargs_remove_axis_labels': {
            'remove_level':     2,
            'yexcept':          {'1,4':2,'3,4':2,'4,3':2,'5,2':2,'6,3':2,},
            'xexcept':          {'0,3':2,'1,0':2,'1,1':2,'1,4':2,'3,1':2,'3,2':2,'3,4':2,'5,2':2,'5,4':2,'6,0':2,'7,1':2,},
        },
        'label_cfgs': [
            {'xrel':0.16 ,'yrel':0.98 ,  'text':'tur_len [m]',  'fontsize':25},
            {'xrel':0.01 ,'yrel':0.80 ,  'text':'tkXmin [m$^2$ s$^{-1}$]',  'rotation':90,  'fontsize':25},

            {'xrel':0.21 ,'yrel':0.96 ,  'text':300},
            {'xrel':0.37 ,'yrel':0.96 ,  'text':200},
            {'xrel':0.54 ,'yrel':0.96 ,  'text':100},
            {'xrel':0.72 ,'yrel':0.96 ,  'text':50},
            {'xrel':0.89 ,'yrel':0.96 ,  'text':10},

            {'xrel':0.05 ,'yrel':0.90 ,  'text':0.01,   'rotation':90},
            {'xrel':0.05 ,'yrel':0.82 ,  'text':0.1 ,   'rotation':90},
            {'xrel':0.05 ,'yrel':0.73 ,  'text':0.2 ,   'rotation':90},
            {'xrel':0.05 ,'yrel':0.655,  'text':0.3 ,   'rotation':90},
            {'xrel':0.05 ,'yrel':0.577,  'text':0.4 ,   'rotation':90},
            {'xrel':0.05 ,'yrel':0.497,  'text':0.5 ,   'rotation':90},
            {'xrel':0.05 ,'yrel':0.417,  'text':0.6 ,   'rotation':90},
            {'xrel':0.05 ,'yrel':0.335,  'text':0.7 ,   'rotation':90},
            {'xrel':0.05 ,'yrel':0.255,  'text':0.8 ,   'rotation':90},
            {'xrel':0.05 ,'yrel':0.174,  'text':0.9 ,   'rotation':90},
            {'xrel':0.05 ,'yrel':0.097,  'text':1.0 ,   'rotation':90},

        ],
    },
    'glob_pan_cfg':   {
        'i_recompute':      1,
        'ana_number':       1,
        'agg_level':        TP.ALL_TIME,
        'plot_domain':      dom_tuning,
        'time_periods':     time_periods_tuning,
        'i_plot_cbar':      0,
        #'pan_cbar_pos':     'lower center',
        'pan_cbar_pad':     -4,
        'cbar_label_mode':  'var_units',
        'title':            '', 
        'var_names':        ['ALBEDO'], 
        'pickle_append':    'cg50',
        'i_coarse_grain':   50,
    },
    'pan_cfgs':    [
    ],
}

numbers = [
    None,None,'03','09','08',
    '12','11','02',None,'01',
    None,None,'13',None,None,
    None,'19','14',None,'37',
    '31',None,None,'41',None,
    '32',None,'23','25','28',
    '33','34',None,'36',None,
    None,'35','24','26','29',
    None,None,'40',None,None,
    None,'39',None,None,None,
    '38',None,None,None,None,
]
cbar_numbers = ['38','39','40','26','29']
for number in numbers:
    if number is not None:
        run_cfgs['ChA_tuning']['pan_cfgs'].append(
            {
                'mem_cfgs':         [
                    {
                        'mem_oper':'bias',
                        'mem_keys':['COSMO_4.4_test_{}'.format(number),'CM_SAF_MSG_AQUA_TERRA_DAILY']
                    }
                ],
            }
        )
    else:
        run_cfgs['ChA_tuning']['pan_cfgs'].append(
            None
        )

    if number in cbar_numbers:
        run_cfgs['ChA_tuning']['pan_cfgs'][-1]['i_plot_cbar'] = 1


print(run_cfgs['ChA_tuning']['pan_cfgs'])
#quit()

use_cfg = 'ChA_tuning'


i_recompute = 1

run_cfg = run_cfgs[use_cfg]

name_dict = {
    'cfg':use_cfg,
}
if 'name_dict_append' in run_cfg['fig']:
    for key,val in run_cfg['fig']['name_dict_append'].items():
        name_dict[key] = val

nrows = run_cfg['fig']['nrows']
ncols = run_cfg['fig']['ncols']

cfg = {
    'sub_dir':              'diss',
    'name_dict':            name_dict,
    'fig':                  run_cfg['fig'],
    'kwargs_pan_labels' : {
        'shift_right':  -0.18,
        'shift_up':     0.07,
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
