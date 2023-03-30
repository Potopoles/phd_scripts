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
from package.nl_models import models_cmip6
from nl_plot_org_ana import nlp
from package.nl_variables import nlv
###############################################################################

args_subplots_adjust = {
    '2x4': {
        'left':0.05,
        'bottom':0.10,
        'right':0.95,
        'top':0.93,
        'wspace':0.40,
        'hspace':0.40,
    },
    '3x4': {
        'left':0.05,
        'bottom':0.10,
        'right':0.95,
        'top':0.93,
        'wspace':0.40,
        'hspace':0.40,
    },
    '4x4': {
        'left':0.03,
        'bottom':0.10,
        'right':0.90,
        'top':0.93,
        'wspace':0.60,
        'hspace':0.40,
    },
    '4x6': {
        'left':0.04,
        'bottom':0.05,
        'right':0.97,
        'top':0.97,
        'wspace':0.30,
        'hspace':0.40,
    },
    '5x6': {
        'left':0.03,
        'bottom':0.05,
        'right':0.96,
        'top':0.97,
        'wspace':0.60,
        'hspace':0.40,
    },
    '7x4': {
        'left':0.04,
        'bottom':0.05,
        'right':0.97,
        'top':0.97,
        'wspace':0.30,
        'hspace':0.40,
    },
}

agg_level = TP.ALL_TIME

ctrl = 'COSMO_3.3_ctrl'
pgw = 'COSMO_3.3_pgw'


var_type_cfgs = {
    'thermodynamic':  {
        'var_types':    [
            'RH_CLDF',
            'T_CLDF',
            'QV_CLDF',
            'BVF_CLDF',
        ],
        'figsize':      (14, 5),
        'nrows':        2,
        'ncols':        4,
        'adjust_key':   '2x4',
        'plot_domain':  dom_trades,
    },
    'circulation':  {
        'var_types':    [
            'W_CLDF',
            'U_CLDF',
            'TKE_CLDF',
            'V_CLDF',
        ],
        'figsize':      (14, 5),
        'nrows':        2,
        'ncols':        4,
        'adjust_key':   '2x4',
        'plot_domain':  dom_trades,
    },

    'heating':  {
        'var_types':    [
            'RH_CLDF',
            'T_CLDF',
            'QV_CLDF',
            'POTTDIV3_CLDF',
            'POTTVDIV3_CLDF',
            'POTTHDIV3_CLDF',
            'POTTDIV3MEAN_CLDF',
            'POTTVDIV3MEAN_CLDF',
            'POTTHDIV3MEAN_CLDF',
            'POTTDIV3TURB_CLDF',
            'POTTVDIV3TURB_CLDF',
            'POTTHDIV3TURB_CLDF',
        ],
        'figsize':      (22, 11),
        'nrows':        4,
        'ncols':        6,
        'adjust_key':   '4x6',
        'plot_domain':  dom_trades,
    },

    'moistening':  {
        'var_types':    [
            'RH_CLDF',
            'T_CLDF',
            'QV_CLDF',
            'QVDIV3_CLDF',
            'QVVDIV3_CLDF',
            'QVHDIV3_CLDF',
            'QVDIV3MEAN_CLDF',
            'QVVDIV3MEAN_CLDF',
            'QVHDIV3MEAN_CLDF',
            'QVDIV3TURB_CLDF',
            'QVVDIV3TURB_CLDF',
            'QVHDIV3TURB_CLDF',
        ],
        'figsize':      (22, 11),
        'nrows':        4,
        'ncols':        6,
        'adjust_key':   '4x6',
        'plot_domain':  dom_trades,
    },

    'moistening_mean':  {
        'var_types':    [
            'QV_CLDF',
            'QVHDIV3MEAN_CLDF',
            'QVDIV3MEAN_CLDF',
            'QVVDIV3MEAN_CLDF',
        ],
        'figsize':      (14, 5),
        'nrows':        2,
        'ncols':        4,
        'adjust_key':   '2x4',
        'plot_domain':  dom_trades,
    },

    'moistening_3d':  {
        'var_types':    [
            'QV_CLDF',
            'QVDIV3MEAN_CLDF',
            'QVDIV3_CLDF',
            'QVDIV3TURB_CLDF',
            'QCDIV3_CLDF',
        ],
        'figsize':      (14, 7.5),
        'nrows':        3,
        'ncols':        4,
        'adjust_key':   '3x4',
        'plot_domain':  dom_trades,
    },

    'moistening_2d_1d':  {
        'var_types':    [
            'QVHDIV3MEAN_CLDF',
            'QVVDIV3MEAN_CLDF',
            'QVHDIV3TURB_CLDF',
            'QVVDIV3TURB_CLDF',
        ],
        'figsize':      (14, 5),
        'nrows':        2,
        'ncols':        4,
        'adjust_key':   '2x4',
        'plot_domain':  dom_trades_full,
    },

    'heating_3d':  {
        'var_types':    [
            'T_CLDF',
            'POTTDIV3MEAN_CLDF',
            'POTTDIV3_CLDF',
            'POTTDIV3TURB_CLDF',
        ],
        'figsize':      (14, 5),
        'nrows':        2,
        'ncols':        4,
        'adjust_key':   '2x4',
        'plot_domain':  dom_trades,
    },

    'heating_2d_1d':  {
        'var_types':    [
            'POTTHDIV3MEAN_CLDF',
            'POTTVDIV3MEAN_CLDF',
            'POTTHDIV3TURB_CLDF',
            'POTTVDIV3TURB_CLDF',
        ],
        'figsize':      (14, 5),
        'nrows':        2,
        'ncols':        4,
        'adjust_key':   '2x4',
        'plot_domain':  dom_trades,
    },

    'summary_tendencies':  {
        'var_types':    [
            'QVDIV3_CLDF',
            'EQPOTTDIV3_CLDF',
            'POTTDIV3_CLDF',
            'LATH_CLDF',
        ],
        'figsize':      (14, 5),
        'nrows':        2,
        'ncols':        4,
        'adjust_key':   '2x4',
        'plot_domain':  dom_trades,
    },


    'summary':  {
        'var_types':    [
            'T_CLDF',
            'POTTDIV3_CLDF',
            'QV_CLDF',
            'QVDIV3_CLDF',
        ],
        'figsize':      (14, 5),
        'nrows':        2,
        'ncols':        4,
        'adjust_key':   '2x4',
        'plot_domain':  dom_trades,
    },


    'moistening_2d_1d_cloud':  {
        'var_types':    [
            'QVHDIV3TURB_CLDF',
            'QVVDIV3TURB_CLDF',
            'CLDQVHDIV3TURB_CLDF',
            'CLDQVVDIV3TURB_CLDF',
            'CSQVHDIV3TURB_CLDF',
            'CSQVVDIV3TURB_CLDF',
        ],
        'figsize':      (14, 7.5),
        'nrows':        3,
        'ncols':        4,
        'adjust_key':   '3x4',
        #'figsize':      (22, 11),
        #'nrows':        4,
        #'ncols':        6,
        #'adjust_key':   '4x6',
        'plot_domain':  dom_trades,
    },

    'moistening_paper':  {
        'var_types':    [
            'W_CLDF',
            'TKE_CLDF',
            'QV_CLDF',
            'QVDIV3_CLDF',
            'QVDIV3MEAN_CLDF',
            'QVDIV3TURB_CLDF',
        ],
        'figsize':      (14, 7.5),
        'nrows':        3,
        'ncols':        4,
        'adjust_key':   '3x4',
        'plot_domain':  dom_trades_full,
    },


    'heating_paper':  {
        'var_types':    [
            'T_CLDF',
            'POTTDIV3_CLDF',
            'EQPOTTDIV3_CLDF',
            'LATH_CLDF',
            'POTTDIV3MEAN_CLDF',
            'POTTDIV3TURB_CLDF',
        ],
        'figsize':      (14, 7.5),
        'nrows':        3,
        'ncols':        4,
        'adjust_key':   '3x4',
        'plot_domain':  dom_trades,
    },

    'heating_paper2':  {
        'var_types':    [
            'POTTHDIV3MEAN_CLDF',
            'POTTVDIV3MEAN_CLDF',
            'POTTHDIV3TURB_CLDF',
            'POTTVDIV3TURB_CLDF',
            'CLDPOTTHDIV3TURB_CLDF',
            'CLDPOTTVDIV3TURB_CLDF',
            'CSPOTTHDIV3TURB_CLDF',
            'CSPOTTVDIV3TURB_CLDF',
        ],
        'figsize':      (14, 10),
        'nrows':        4,
        'ncols':        4,
        'adjust_key':   '4x4',
        'plot_domain':  dom_trades,
    },

    'itcz':  {
        'var_types':    [
            'POTTDIV3_CLDF',
            'CSPOTTDIV3_CLDF',
            'CLDPOTTDIV3_CLDF',
            'EQPOTTDIV3_CLDF',
            'CSEQPOTTDIV3_CLDF',
            'CLDEQPOTTDIV3_CLDF',
            'LATH_CLDF',
            'CSLATH_CLDF',
            'CLDLATH_CLDF',
        ],
        'figsize':      (22, 11),
        'nrows':        4,
        'ncols':        6,
        'adjust_key':   '4x6',
        'plot_domain':  dom_SA_ana_merid_cs,
    },

    'moistening_paper2':  {
        'var_types':    [
            'QVDIV3MEAN_CLDF',
            'QVHDIV3MEAN_CLDF',
            'RH_CLDF',
            'QVDIV3TURB_CLDF',
            'QVVDIV3MEAN_CLDF',
            'POTT_CLDF',
            'QVDIV3_CLDF',
            'CLDQVDIV3TURB_CLDF',
            'QV_CLDF',
            'BVF_CLDF',
            'CSQVDIV3TURB_CLDF',
            'BUOYIFLX_CLDF',
            'CSPOTTDIV_CLDF',
            'CLDPOTTDIV_CLDF',
            'CLDF_CLDF',
            #'POTTDIV3_CLDF',
            #'CLDPOTTDIV3_CLDF',
            #'QVVDIV3_CLDF',
            #'QVHDIV3TURB_CLDF',
            #'QVVDIV3TURB_CLDF',
            #'QVHDIV3_CLDF',
            #'CLDQVHDIV3TURB_CLDF',
            #'CLDQVVDIV3TURB_CLDF',
            #'CSQVHDIV3TURB_CLDF',
            #'CSQVVDIV3TURB_CLDF',
        ],
        'figsize':          (24, 12.5),
        'nrows':            5,
        'ncols':            6,
        'adjust_key':       '5x6',
        'plot_domain':      dom_trades_full,
        #'plot_domain':      dom_trades_extended,
        'line_along':       'lon',
        'line_at':          slice(dom_trades_full['lat'].start+1,dom_trades_full['lat'].stop-1),
        'time_periods':     time_periods_ana,
        'name_dict_append': {},
        #'time_periods':     time_periods_ana_JJA,
        #'name_dict_append': {'month':'JJA'},
        #'time_periods':     time_periods_ana_SON,
        #'name_dict_append': {'month':'SON'},
        #'time_periods':     time_periods_ana_DJF,
        #'name_dict_append': {'month':'DJF'},
        #'time_periods':     time_periods_ana_MAM,
        #'name_dict_append': {'month':'MAM'},
    },

}

var_type_cfgs['compare_seas'] = copy.deepcopy(var_type_cfgs['moistening_paper2'])

default_time_periods = time_periods_ana
#default_time_periods = time_periods_ana_JJA
#default_time_periods = time_periods_ana_SON
#default_time_periods = time_periods_ana_DJF
#default_time_periods = time_periods_ana_MAM
#default_time_periods = get_time_periods_for_month(2006, 8)

norm_inv = 1

#use_cfg = 'thermodynamic'
#use_cfg = 'circulation'
#use_cfg = 'moistening'
#use_cfg = 'moistening_3d'
#use_cfg = 'moistening_2d_1d_cloud'
#use_cfg = 'heating'
#use_cfg = 'heating_3d'
#use_cfg = 'heating_2d_1d'
#use_cfg = 'summary_tendencies'
#use_cfg = 'summary'
#use_cfg = 'moistening_paper'
#use_cfg = 'heating_paper'
#use_cfg = 'heating_paper2'
#use_cfg = 'itcz'
use_cfg = 'moistening_2d_1d'
use_cfg = 'moistening_paper2'
#use_cfg = 'compare_seas'

var_type_cfg = var_type_cfgs[use_cfg]

if 'time_periods' in var_type_cfg:
    use_time_periods = var_type_cfg['time_periods']
else:
    use_time_periods = default_time_periods

if norm_inv:
    norm_str = 'norm'
else:
    norm_str = ''

name_dict = {
    'cfg':use_cfg,
    norm_str:'',
    'dom':var_type_cfg['plot_domain']['key'],
}
if 'name_dict_append' in var_type_cfg:
    name_dict.update(var_type_cfg['name_dict_append'])

if var_type_cfg['plot_domain']['key'] in [
    'dom_trades_deep','dom_trades_shallow','dom_trades','dom_trades_deep','dom_trades_full','dom_trades_extended']:
    alt_lims = (0,4000) 
elif var_type_cfg['plot_domain']['key'] in ['dom_ITCZ', 'dom_NS_cs']:
    alt_lims = (0,18000) 
    #alt_lims = (0,6000) 
else:
    raise NotImplementedError()

nrows = var_type_cfg['nrows']
ncols = var_type_cfg['ncols']

diff_mem_cfg = [
    {
        'mem_oper':     'diff',
        'mem_keys':     [pgw, ctrl],
    },
]
#diff_mem_cfg = [
#    {
#        'mem_oper':     'rel0.001',
#        'mem_keys':     [pgw, ctrl],
#    },
#]
#name_dict.update({'change':'rel'})
if use_cfg == 'compare_seas':
    test_memb = {
        'mem_key':'COSMO_3.3_ctrl',
        'time_periods':var_type_cfgs['moistening_paper2']['time_periods'], 
    }
    ctrl = {
        'mem_key':'COSMO_3.3_ctrl',
        'time_periods':time_periods_ana, 
        #'time_periods':time_periods_ana_SON, 
    }
    diff_mem_cfg = [
        {
            'mem_oper':     'diff',
            'mem_keys':     [test_memb, ctrl],
        },
    ]

#diff_mem_cfg = [
#    {
#        'mem_oper':     'rel0.01',
#        'mem_keys':     [pgw, ctrl],
#    },
#]



cfg = {
    'serial_time_plt_sels': [None],
    'sub_dir':              'alcs_combo',
    'name_dict':            name_dict,
    ##'figsize':              (14, 6), # 2x3
    ##'figsize':              (14, 6), # 2x3
    ##'figsize':              (16, 11), # 3x4
    #'figsize':              (22, 11), # 3x5
    'figsize':              var_type_cfg['figsize'],
    'nrows':                nrows,
    'ncols':                ncols,
    'subplots_adjust_spatial':
                            '1x1', # dummy
    'args_subplots_adjust': args_subplots_adjust[var_type_cfg['adjust_key']],
    'i_remove_axis_labels': 1,
    'kwargs_remove_axis_labels': {
        'remove_level': 2,
    },
    'kwargs_panel_labels' : {
        'shift_right':      -0.35,
        'shift_up':          0.10,
    },
    'all_panels':
        {
            'ana_number':   4,
            'time_periods': use_time_periods,
            'agg_level':    agg_level,
            'i_recompute':  0,
            'plot_domain':  var_type_cfg['plot_domain'],
            'line_along':   var_type_cfg['line_along'],
            'line_at':      var_type_cfg['line_at'],
            'alt_lims':     alt_lims,
        },
    'panels':
    {
    }
}


vi = 0
for var_type in var_type_cfg['var_types']:
    print(var_type)
    if var_type is not None:
        col_ind = vi % ncols
        row_ind = int(vi/ncols)
        pan_key = '{},{}'.format(row_ind, col_ind)
        print(pan_key)

        pan_dict = {
            'i_recompute':  0,
            'var_type':     var_type,
            'norm_inv':     norm_inv,
            'mem_cfgs':     [ctrl],
            'title':        '{}: CTRL'.format(nlv[var_type.split('_')[0]]['label']),
        }
        cfg['panels'][pan_key] = pan_dict

        vi += 1
        col_ind = vi % ncols
        row_ind = int(vi/ncols)
        pan_key = '{},{}'.format(row_ind, col_ind)
        print(pan_key)

        pan_dict = {
            'i_recompute':  1,
            'var_type':     var_type,
            'norm_inv':     norm_inv,
            'mem_cfgs':     diff_mem_cfg,
            'title':        '{}: PGW - CTRL'.format(nlv[var_type.split('_')[0]]['label']),
        }
        cfg['panels'][pan_key] = pan_dict

    vi += 1
#quit()

