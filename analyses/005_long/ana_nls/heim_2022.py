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
    '6x5': {
        'left':0.07,
        'bottom':0.09,
        'right':0.98,
        'top':0.95,
        'wspace':0,
        'hspace':0,
    },
}

run_cfgs = {}

var_name = 'U'
#var_name = 'V'
#var_name = 'T'
#var_name = 'RH'
run_cfgs['suppl_1'] = {
    'fig': {
        'figsize':              (11, 12),
        'nrows':                5,
        'ncols':                4,
        'args_subplots_adjust': {
            'left':     0.12,
            'bottom':   0.12,
            'right':    0.98,
            'top':      0.96,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [0.15,0.15,0.15,0.15],
            'wspaces':  [0.05,0.05,0.05],
        },
        'kwargs_remove_axis_labels': {
            'remove_level': 2,
        },
        'label_cfgs': [
            {'xrel':0.20,'yrel':0.97,   'text':'DJF'},
            {'xrel':0.41,'yrel':0.97,   'text':'MAM'},
            {'xrel':0.64,'yrel':0.97,   'text':'JJA'},
            {'xrel':0.85,'yrel':0.97,   'text':'SON'},

            {'xrel':0.01,'yrel':0.850,   'text':'0.3 km', 'rotation':90},
            {'xrel':0.01,'yrel':0.690,   'text':'3 km',   'rotation':90},
            {'xrel':0.01,'yrel':0.515,   'text':'9 km',   'rotation':90},
            {'xrel':0.01,'yrel':0.340,   'text':'12 km',  'rotation':90},
            {'xrel':0.01,'yrel':0.160,   'text':'16 km',  'rotation':90},
        ],
        'name_dict_append': {
            'var_name': var_name,
        }
    },
    'glob_pan_cfg':   {
        'ana_number':       1,
        'i_recompute':      1,
        'agg_level':        TP.ALL_TIME,
        'plot_domain':      dom_SA_3km_large3,
        'i_plot_cbar':      0,
        'title':            '', 
        'add_bias_labels':  0, 
    },
    'pan_cfgs':    [
        {
            'var_names':        ['{}@alt=300'.format(var_name)],
            'mem_cfgs':         [mpi_change_DJF],
        },
        {
            'var_names':        ['{}@alt=300'.format(var_name)],
            'mem_cfgs':         [mpi_change_MAM],
        },
        {
            'var_names':        ['{}@alt=300'.format(var_name)],
            'mem_cfgs':         [mpi_change_JJA],
        },
        {
            'var_names':        ['{}@alt=300'.format(var_name)],
            'mem_cfgs':         [mpi_change_SON],
        },

        {
            'var_names':        ['{}@alt=3000'.format(var_name)],
            'mem_cfgs':         [mpi_change_DJF],
        },
        {
            'var_names':        ['{}@alt=3000'.format(var_name)],
            'mem_cfgs':         [mpi_change_MAM],
        },
        {
            'var_names':        ['{}@alt=3000'.format(var_name)],
            'mem_cfgs':         [mpi_change_JJA],
        },
        {
            'var_names':        ['{}@alt=3000'.format(var_name)],
            'mem_cfgs':         [mpi_change_SON],
        },

        {
            'var_names':        ['{}@alt=9000'.format(var_name)],
            'mem_cfgs':         [mpi_change_DJF],
        },
        {
            'var_names':        ['{}@alt=9000'.format(var_name)],
            'mem_cfgs':         [mpi_change_MAM],
        },
        {
            'var_names':        ['{}@alt=9000'.format(var_name)],
            'mem_cfgs':         [mpi_change_JJA],
        },
        {
            'var_names':        ['{}@alt=9000'.format(var_name)],
            'mem_cfgs':         [mpi_change_SON],
        },

        {
            'var_names':        ['{}@alt=12000'.format(var_name)],
            'mem_cfgs':         [mpi_change_DJF],
        },
        {
            'var_names':        ['{}@alt=12000'.format(var_name)],
            'mem_cfgs':         [mpi_change_MAM],
        },
        {
            'var_names':        ['{}@alt=12000'.format(var_name)],
            'mem_cfgs':         [mpi_change_JJA],
        },
        {
            'var_names':        ['{}@alt=12000'.format(var_name)],
            'mem_cfgs':         [mpi_change_SON],
        },

        {
            'var_names':        ['{}@alt=16000'.format(var_name)],
            'mem_cfgs':         [mpi_change_DJF],
            'i_plot_cbar':      1,
        },
        {
            'var_names':        ['{}@alt=16000'.format(var_name)],
            'mem_cfgs':         [mpi_change_MAM],
            'i_plot_cbar':      1,
        },
        {
            'var_names':        ['{}@alt=16000'.format(var_name)],
            'mem_cfgs':         [mpi_change_JJA],
            'i_plot_cbar':      1,
        },
        {
            'var_names':        ['{}@alt=16000'.format(var_name)],
            'mem_cfgs':         [mpi_change_SON],
            'i_plot_cbar':      1,
        },
    ],
}




var_name = 'TSURF'
run_cfgs['suppl_2'] = {
    'fig': {
        'figsize':              (11, 4),
        'nrows':                1,
        'ncols':                4,
        'args_subplots_adjust': {
            'left':     0.12,
            'bottom':   0.32,
            'right':    0.98,
            'top':      0.94,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [0.15,0.15,0.15,0.15],
            'wspaces':  [0.05,0.05,0.05],
        },
        'kwargs_remove_axis_labels': {
            'remove_level': 2,
        },
        'label_cfgs': [
            {'xrel':0.20,'yrel':0.92,   'text':'DJF'},
            {'xrel':0.41,'yrel':0.92,   'text':'MAM'},
            {'xrel':0.64,'yrel':0.92,   'text':'JJA'},
            {'xrel':0.85,'yrel':0.92,   'text':'SON'},

            #{'xrel':0.01,'yrel':0.850,   'text':nlv['TSURF']['label'], 'rotation':90},
        ],
        'name_dict_append': {
            'var_name': var_name,
        }
    },
    'glob_pan_cfg':   {
        'ana_number':       1,
        'i_recompute':      1,
        'agg_level':        TP.ALL_TIME,
        'plot_domain':      dom_SA_3km_large3,
        'i_plot_cbar':      1,
        'title':            '', 
        'add_bias_labels':  0, 
        'pan_cbar_pos':     'lower center',
        'pan_cbar_pad':     -5,
    },
    'pan_cfgs':    [
        {
            'var_names':        ['TSURF'],
            'mem_cfgs':         [mpi_change_DJF],
        },
        {
            'var_names':        ['TSURF'],
            'mem_cfgs':         [mpi_change_MAM],
        },
        {
            'var_names':        ['TSURF'],
            'mem_cfgs':         [mpi_change_JJA],
        },
        {
            'var_names':        ['TSURF'],
            'mem_cfgs':         [mpi_change_SON],
        },
    ],
}





## ATLANTIC CS
domain = dom_SA_ana_merid_cs
time_periods_ana_NH_max = time_periods_ana_JAS
time_periods_cmip6_hist_NH_max = time_periods_cmip6_hist_JAS
label_NH_max = 'July-Sep'
time_periods_ana_SH_max = time_periods_ana_FMA
time_periods_cmip6_hist_SH_max = time_periods_cmip6_hist_FMA
label_SH_max = 'Feb-Apr'

#### AFRICA CS
#domain = dom_SA_ana_merid_cs_afr
#time_periods_ana_NH_max = time_periods_ana_JJA
#time_periods_cmip6_hist_NH_max = time_periods_cmip6_hist_JJA
#label_NH_max = 'June-Aug'
#time_periods_ana_SH_max = time_periods_ana_DJF
#time_periods_cmip6_hist_SH_max = time_periods_cmip6_hist_DJF
#label_SH_max = 'Dec-Jan'
run_cfgs['clouds_eval'] = {
    'fig': {
        'figsize':              (10, 12),
        'nrows':                5,
        'ncols':                3,
        'args_subplots_adjust': args_subplots_adjust['{}x{}'.format(5,3)],
        'grid_spec':            dict(
                                    hspaces=[0.2,0.2,0.2,0.2,0.2],
                                    wspaces=[0.11,0.11],
                                ),
        'kwargs_remove_axis_labels': {
            'remove_level':     2,
        },
        'label_cfgs': [
            {'xrel':0.16,'yrel':0.97,   'text':'annual mean'},
            {'xrel':0.47,'yrel':0.97,   'text':label_SH_max},
            {'xrel':0.74,'yrel':0.97,   'text':label_NH_max},
            {'xrel':0.01,'yrel':0.82 ,  'text':'ERA5 07-10',   'rotation':90},
            {'xrel':0.01,'yrel':0.645,  'text':'ERA5 85-14',   'rotation':90},
            {'xrel':0.01,'yrel':0.51,   'text':'CTRL',         'rotation':90},
            {'xrel':0.01,'yrel':0.305,  'text':'CMIP6-EM',     'rotation':90},
            {'xrel':0.01,'yrel':0.14,   'text':'MPI-ESM',      'rotation':90},
        ],
        'name_dict_append': {
            'dom': domain['key'],
        }
    },
    'glob_pan_cfg':   {
        'ana_number':       4,
        'agg_level':        TP.ALL_TIME,
        'line_at':          None,
        'alt_lims':         (0,18000),
        'line_along':       'lat',
        'plot_domain':      domain,
        'norm_inv':         0,
        'time_periods':     time_periods_ana,
        'i_plot_cbar':      0,
        'var_type':         'CLDF_CLDF_PP', 
        'title':            '', 
    },
    'pan_cfgs':    [
        {
            'mem_cfgs':         [era,'GPM_IMERG'],
        },
        {
            'mem_cfgs':         [era,'GPM_IMERG'],
            'time_periods':     time_periods_ana_SH_max,
        },
        {
            'mem_cfgs':         [era,'GPM_IMERG'],
            'time_periods':     time_periods_ana_NH_max,
        },

        {
            'mem_cfgs':         [era],
            'time_periods':     time_periods_cmip6_hist,
        },
        {
            'mem_cfgs':         [era],
            'time_periods':     time_periods_cmip6_hist_SH_max,
        },
        {
            'mem_cfgs':         [era],
            'time_periods':     time_periods_cmip6_hist_NH_max,
        },

        {
            'mem_cfgs':         [ctrl],
        },
        {
            'mem_cfgs':         [ctrl],
            'time_periods':     time_periods_ana_SH_max,
        },
        {
            'mem_cfgs':         [ctrl],
            'time_periods':     time_periods_ana_NH_max,
        },

        {
            'mem_cfgs':         [cmip6_hist],
            'time_periods':     time_periods_cmip6_hist,
        },
        {
            'mem_cfgs':         [cmip6_hist],
            'time_periods':     time_periods_cmip6_hist_SH_max,
        },
        {
            'mem_cfgs':         [cmip6_hist],
            'time_periods':     time_periods_cmip6_hist_NH_max,
        },

        {
            'mem_cfgs':         [mpi_hist],
            'time_periods':     time_periods_cmip6_hist,
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [mpi_hist],
            'time_periods':     time_periods_cmip6_hist_SH_max,
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [mpi_hist],
            'time_periods':     time_periods_cmip6_hist_NH_max,
            'i_plot_cbar':      1,
        },
    ],
}



run_cfgs['thermo_dyn_eval'] = {
    'fig': {
        'figsize':              (12.5, 13),
        'nrows':                5,
        'ncols':                4,
        'args_subplots_adjust': {
            'left':     0.09,
            'bottom':   0.10,
            'right':    0.98,
            'top':      0.95,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [0.2,0.2,1.0,0.2],
            'wspaces':  [0.08,0.08,0.08],
        },
        'kwargs_remove_axis_labels': {
            'remove_level':     2,
            'xexcept':          {'2,0':0,'2,1':0,'2,2':0,'2,3':0},
        },
        'label_cfgs': [
            {'xrel':0.18,'yrel':0.97 ,  'text':nlv['VFLX']['label']},
            {'xrel':0.41,'yrel':0.97 ,  'text':nlv['WFLX']['label']},
            {'xrel':0.64,'yrel':0.97 ,  'text':nlv['T']['label']},
            {'xrel':0.86,'yrel':0.97 ,  'text':nlv['RH']['label']},

            {'xrel':0.01,'yrel':0.865,  'text':'ERA5',              'rotation':90},
            {'xrel':0.01,'yrel':0.71 ,  'text':'CTRL',              'rotation':90},
            {'xrel':0.01,'yrel':0.53 ,  'text':'CMIP6-EM',          'rotation':90},
            {'xrel':0.01,'yrel':0.27 ,  'text':'CTRL$-$ERA5',       'rotation':90},
            {'xrel':0.01,'yrel':0.08 ,  'text':'CMIP6-EM$-$ERA5',   'rotation':90},
        ],
    },
    'glob_pan_cfg':   {
        'ana_number':       4,
        'agg_level':        TP.ALL_TIME,
        'line_at':          None,
        'alt_lims':         (0,18000),
        'line_along':       'lat',
        'plot_domain':      dom_SA_ana_merid_cs,
        'norm_inv':         0,
        'time_periods':     time_periods_ana,
        'i_plot_cbar':      0,
        'title':            '', 
    },
    'pan_cfgs':    [
        {
            'mem_cfgs':         ['ERA5'],
            'var_type':         'VFLX_CLDF', 
        },
        {
            'mem_cfgs':         ['ERA5'],
            'var_type':         'VFLX_CLDF', 
            'var_type':         'WFLX_CLDF', 
        },
        {
            'mem_cfgs':         ['ERA5'],
            'var_type':         'VFLX_CLDF', 
            'var_type':         'T_CLDF', 
        },
        {
            'mem_cfgs':         ['ERA5'],
            'var_type':         'VFLX_CLDF', 
            'var_type':         'RH_CLDF', 
        },


        {
            'mem_cfgs':         [ctrl],
            'var_type':         'VFLX_CLDF', 
        },
        {
            'mem_cfgs':         [ctrl],
            'var_type':         'WFLX_CLDF', 
        },
        {
            'mem_cfgs':         [ctrl],
            'var_type':         'T_CLDF', 
        },
        {
            'mem_cfgs':         [ctrl],
            'var_type':         'RH_CLDF', 
        },


        {
            'mem_cfgs':         [cmip6_hist],
            'time_periods':     time_periods_cmip6_hist,
            'var_type':         'VFLX_CLDF', 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cmip6_hist],
            'time_periods':     time_periods_cmip6_hist,
            'var_type':         'WFLX_CLDF', 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cmip6_hist],
            'time_periods':     time_periods_cmip6_hist,
            'var_type':         'T_CLDF', 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cmip6_hist],
            'time_periods':     time_periods_cmip6_hist,
            'var_type':         'RH_CLDF', 
            'i_plot_cbar':      1,
        },


        {
            'mem_cfgs':         [ctrl_bias],
            'var_type':         'VFLX_CLDF', 
        },
        {
            'mem_cfgs':         [ctrl_bias],
            'var_type':         'WFLX_CLDF', 
        },
        {
            'mem_cfgs':         [ctrl_bias],
            'var_type':         'T_CLDF', 
        },
        {
            'mem_cfgs':         [ctrl_bias],
            'var_type':         'RH_CLDF', 
        },


        {
            'mem_cfgs':         [cmip6_bias],
            'time_periods':     time_periods_cmip6_hist,
            'var_type':         'VFLX_CLDF', 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cmip6_bias],
            'time_periods':     time_periods_cmip6_hist,
            'var_type':         'WFLX_CLDF', 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cmip6_bias],
            'time_periods':     time_periods_cmip6_hist,
            'var_type':         'T_CLDF', 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cmip6_bias],
            'time_periods':     time_periods_cmip6_hist,
            'var_type':         'RH_CLDF', 
            'i_plot_cbar':      1,
        },
    ],
}



run_cfgs['suppl_subs'] = {
    'fig': {
        'figsize':              (9, 4.0),
        'nrows':                1,
        'ncols':                3,
        'args_subplots_adjust': {
            'left':     0.10,
            'bottom':   0.30,
            'right':    0.95,
            'top':      0.90,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [],
            'wspaces':  [0.08,0.08],
        },
        'kwargs_remove_axis_labels': {
            'remove_level':     2,
        },
        'label_cfgs': [
        ],
    },
    'glob_pan_cfg':   {
        'ana_number':       4,
        'agg_level':        TP.ALL_TIME,
        'line_at':          None,
        'alt_lims':         (0,18000),
        'line_along':       'lat',
        'plot_domain':      dom_SA_ana_merid_cs,
        'norm_inv':         0,
        'time_periods':     time_periods_ana,
        'i_plot_cbar':      0,
    },
    'pan_cfgs':    [
        {
            'mem_cfgs':         [ctrl_bias],
            'var_type':         'WFLX_CLDF', 
            'i_plot_cbar':      1,
            'title':            '{}'.format(nlv['WFLX']['label']), 
        },
        {
            'mem_cfgs':         [ctrl_bias],
            'var_type':         'POTTDIV_CLDF', 
            'i_plot_cbar':      1,
            'title':            '{}'.format(nlv['POTTDIV']['label']), 
        },
        {
            'mem_cfgs':         [ctrl_bias],
            'var_type':         'BVF_CLDF', 
            'i_plot_cbar':      1,
            'title':            '{}'.format(nlv['BVF']['label']), 
        },
    ],
}



run_cfgs['spatial_eval'] = {
    'fig': {
        'figsize':              (13, 6.5),
        'nrows':                3,
        'ncols':                4,
        'args_subplots_adjust': {
            'left':     0.10,
            'bottom':   0.08,
            'right':    0.92,
            'top':      0.92,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [0.10,0.10],
            'wspaces':  [0.06,0.65,0.06],
        },
        'kwargs_remove_axis_labels': {
            'remove_level':     2,
            'yexcept':          {'0,2':1,'1,2':1,'2,2':1},
        },
        'label_cfgs': [
            {'xrel':0.165,'yrel':0.96 ,  'text':'CTRL'},
            {'xrel':0.33 ,'yrel':0.96 ,  'text':'CMIP6-EM'},
            {'xrel':0.60 ,'yrel':0.96 ,  'text':'CTRL$-$OBS'},
            {'xrel':0.76 ,'yrel':0.96 ,  'text':'CMIP6-EM$-$OBS'},

            {'xrel':0.01 ,'yrel':0.73 ,
            'text':'{}'.format(nlv['ALBEDO']['label']),  'rotation':90},
            {'xrel':0.01 ,'yrel':0.44 ,
            'text':'{}'.format(nlv['PP']['label']),  'rotation':90},
            {'xrel':0.01 ,'yrel':0.17 ,
            'text':'{}'.format(nlv['LWUTOA']['label']),  'rotation':90},
        ],
    },
    'glob_pan_cfg':   {
        'ana_number':       1,
        'agg_level':        TP.ALL_TIME,
        'plot_domain':      dom_SA_ana,
        'time_periods':     time_periods_ana,
        'i_plot_cbar':      0,
        'pan_cbar_pos':     'center right',
        'pan_cbar_pad':     -1.3,
        'cbar_label_mode':  'var_units',
        'title':            '', 
    },
    'pan_cfgs':    [
        {
            'mem_cfgs':         [ctrl],
            'var_names':        ['ALBEDO'], 
        },
        {
            'mem_cfgs':         [cmip6_hist],
            'time_periods':     time_periods_cmip6_hist,
            'var_names':        ['ALBEDO'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cosmo_bias_cm_saf],
            'var_names':        ['ALBEDO'], 
        },
        {
            'mem_cfgs':         [cmip6_hist_bias_cm_saf],
            'var_names':        ['ALBEDO'], 
            'i_plot_cbar':      1,
        },

        {
            'mem_cfgs':         [ctrl],
            'var_names':        ['PP'], 
        },
        {
            'mem_cfgs':         [cmip6_hist],
            'time_periods':     time_periods_cmip6_hist,
            'var_names':        ['PP'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cosmo_bias_gpm_imerg],
            'var_names':        ['PP'], 
        },
        {
            'mem_cfgs':         [cmip6_hist_bias_gpm_imerg],
            'var_names':        ['PP'], 
            'i_plot_cbar':      1,
        },

        {
            'mem_cfgs':         [ctrl],
            'var_names':        ['LWUTOA'], 
        },
        {
            'mem_cfgs':         [cmip6_hist],
            'time_periods':     time_periods_cmip6_hist,
            'var_names':        ['LWUTOA'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cosmo_bias_cm_saf],
            'var_names':        ['LWUTOA'], 
        },
        {
            'mem_cfgs':         [cmip6_hist_bias_cm_saf],
            'var_names':        ['LWUTOA'], 
            'i_plot_cbar':      1,
        },
    ],
}



var_name = 'ALBEDO'
var_name = 'PP'
#var_name = 'LWUTOA'
mem_cfgs = [
    ctrl,
    'ERA5',
    {'mem_oper':'mean','mem_keys':mem_keys_cmip6_hist,'time_periods':time_periods_cmip6_hist,'label':'CMIP6'},
    {'mem_oper':'perc25','mem_keys':mem_keys_cmip6_hist,'time_periods':time_periods_cmip6_hist,'label':'CMIP6','spread':[1,'lower']},
    {'mem_oper':'perc75','mem_keys':mem_keys_cmip6_hist,'time_periods':time_periods_cmip6_hist,'label':'CMIP6','spread':[1,'upper']},
    {'mem_oper':'perc10','mem_keys':mem_keys_cmip6_hist,'time_periods':time_periods_cmip6_hist,'label':'CMIP6','spread':[0,'lower']},
    {'mem_oper':'perc90','mem_keys':mem_keys_cmip6_hist,'time_periods':time_periods_cmip6_hist,'label':'CMIP6','spread':[0,'upper']},

    
    ]
if var_name in ['ALBEDO','LWUTOA']:
    i_subtract_mean = 1
    mem_cfgs.extend([
        {'mem_key':'CERES_EBAF','label':'CERES 07-10','zorder':3},
        {'mem_key':'CERES_EBAF','label':'CERES 04-14','time_periods':time_periods_ceres_ebaf,'zorder':3},
        {'mem_key':'CM_SAF_MSG_AQUA_TERRA','label':'CM SAF 07-10','zorder':2},
        {'mem_key':'CM_SAF_MSG_AQUA_TERRA','label':'CM SAF 04-10','time_periods':time_periods_cm_saf_msg_aqua_terra,'zorder':2},
    ])
elif var_name == 'PP':
    i_subtract_mean = 1
    mem_cfgs.extend([
        {'mem_key':'GPM_IMERG','label':'GPM 07-10','zorder':2},
        {'mem_key':'GPM_IMERG','label':'GPM 01-14','time_periods':time_periods_gpm_imerg,'zorder':2},
    ])
run_cfgs['anncycle'] = {
    'fig': {
        'figsize':              (9, 6),
        'nrows':                2,
        'ncols':                2,
        'args_subplots_adjust': {
            'left':     0.09,
            'bottom':   0.09,
            'right':    0.98,
            'top':      0.95,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [0.25],
            'wspaces':  [0.18],
        },
        'kwargs_remove_axis_labels': {
            'remove_level':     1,
        },
        'label_cfgs': [
        ],
        'name_dict_append': {
            'var_name': var_name,
        }
    },
    'glob_pan_cfg':   {
        'ana_number':       9,
        'agg_level':        TP.ANNUAL_CYCLE,
        'time_periods':     time_periods_ana,
        'i_subtract_mean':  i_subtract_mean,
    },
    'pan_cfgs':    [
        {
            'mem_cfgs':         mem_cfgs,
            'var_names':        [var_name], 
            'plot_domain':      dom_SA_ana_sea,
            'title':            dom_SA_ana_sea['label'],
        },
        {
            'mem_cfgs':         mem_cfgs,
            'var_names':        [var_name], 
            'plot_domain':      dom_ITCZ,
            'title':            dom_ITCZ['label'],
            'i_plot_legend':    0,
        },
        {
            'mem_cfgs':         mem_cfgs,
            'var_names':        [var_name], 
            'plot_domain':      dom_trades_deep,
            'title':            dom_trades_deep['label'],
            'i_plot_legend':    0,
        },
        {
            'mem_cfgs':         mem_cfgs,
            'var_names':        [var_name], 
            'plot_domain':      dom_trades_shallow,
            'title':            dom_trades_shallow['label'],
            'i_plot_legend':    0,
        },
    ],
}



run_cfgs['spatial_change'] = {
    'fig': {
        'figsize':              (11, 6.5),
        'nrows':                3,
        'ncols':                3,
        'args_subplots_adjust': {
            'left':     0.12,
            'bottom':   0.08,
            'right':    0.90,
            'top':      0.92,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [0.12,0.12],
            'wspaces':  [0.06,0.60],
        },
        'kwargs_remove_axis_labels': {
            'remove_level':     2,
            'yexcept':          {'0,2':1,'1,2':1,'2,2':1},
        },
        'label_cfgs': [
            {'xrel':0.17 ,'yrel':0.96 , 'text':'CTRL | HIST'},
            {'xrel':0.39 ,'yrel':0.96 , 'text':'PGW | SCEN'},
            #{'xrel':0.66 ,'yrel':0.96 , 'text':'PGW$-$CTRL / SCEN$-$HIST'},
            {'xrel':0.76 ,'yrel':0.96 , 'text':'change'},

            {'xrel':0.01 ,'yrel':0.73 , 'text':'COSMO',     'rotation':90},
            {'xrel':0.01 ,'yrel':0.41 , 'text':'CMIP6-EM',  'rotation':90},
            {'xrel':0.01 ,'yrel':0.13 , 'text':'MPI-ESM',   'rotation':90},
        ],
    },
    'glob_pan_cfg':   {
        'ana_number':       1,
        'agg_level':        TP.ALL_TIME,
        'plot_domain':      dom_SA_ana,
        'time_periods':     time_periods_ana,
        'i_plot_cbar':      0,
        'pan_cbar_pos':     'center right',
        'pan_cbar_pad':     -1.3,
        'cbar_label_mode':  'var_units',
        'title':            '', 
        'add_bias_labels':  0,
    },
    'pan_cfgs':    [
        {
            'mem_cfgs':         [ctrl],
            'var_names':        ['PP'], 
            'pickle_append':    'cg50',
        },
        {
            'mem_cfgs':         [pgw],
            'var_names':        ['PP'], 
            'i_plot_cbar':      1,
            'pickle_append':    'cg50',
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['PP'], 
            'i_plot_cbar':      1,
            'pickle_append':    'cg50',
        },

        {
            'mem_cfgs':         [cmip6_hist],
            'time_periods':     time_periods_cmip6_hist,
            'var_names':        ['PP'], 
        },
        {
            'mem_cfgs':         [cmip6_scen],
            'time_periods':     time_periods_cmip6_scen,
            'var_names':        ['PP'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cmip6_change],
            'var_names':        ['PP'], 
            'i_plot_cbar':      1,
        },

        {
            'mem_cfgs':         [mpi_hist],
            'time_periods':     time_periods_cmip6_hist,
            'var_names':        ['PP'], 
        },
        {
            'mem_cfgs':         [mpi_scen],
            'time_periods':     time_periods_cmip6_scen,
            'var_names':        ['PP'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [mpi_change],
            'var_names':        ['PP'], 
            'i_plot_cbar':      1,
        },
    ],
}



run_cfgs['thermo_change'] = {
    'fig': {
        'figsize':              (12.5, 8.5),
        'nrows':                3,
        'ncols':                4,
        'args_subplots_adjust': {
            'left':     0.09,
            'bottom':   0.15,
            'right':    0.98,
            'top':      0.88,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [0.15,0.15],
            'wspaces':  [0.10,0.30,0.10],
        },
        'kwargs_remove_axis_labels': {
            'remove_level':     2,
            'yexcept':          {'0,2':1,'1,2':1,'2,2':1},
        },
        'label_cfgs': [
            {'xrel':0.29,'yrel':0.96 ,  'text':nlv['T']['label'], 'fontsize':22},
            {'xrel':0.75,'yrel':0.96 ,  'text':nlv['RH']['label'],'fontsize':22},

            {'xrel':0.13,'yrel':0.92 ,  'text':'CTRL | HIST'},
            {'xrel':0.37,'yrel':0.92 ,  'text':'change'},
            {'xrel':0.61,'yrel':0.92 ,  'text':'CTRL | HIST'},
            {'xrel':0.85,'yrel':0.92 ,  'text':'change'},

            {'xrel':0.01,'yrel':0.72 ,  'text':'COSMO',     'rotation':90},
            {'xrel':0.01,'yrel':0.45 ,  'text':'CMIP6-EM',  'rotation':90},
            {'xrel':0.01,'yrel':0.21 ,  'text':'MPI-ESM',   'rotation':90},
        ],
    },
    'glob_pan_cfg':   {
        'ana_number':       4,
        'agg_level':        TP.ALL_TIME,
        'line_at':          None,
        'alt_lims':         (0,18000),
        'line_along':       'lat',
        'plot_domain':      dom_SA_ana_merid_cs,
        'norm_inv':         0,
        'time_periods':     time_periods_ana,
        'i_plot_cbar':      0,
        'title':            '', 
        'pan_cbar_pad':     -5.5,
        'i_recompute':      0,
    },
    'pan_cfgs':    [
        {
            'mem_cfgs':         [ctrl],
            'var_type':         'T_CLDF', 
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_type':         'T_CLDF', 
        },
        {
            'mem_cfgs':         [ctrl],
            'var_type':         'RH_CLDF', 
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_type':         'RH_CLDF', 
        },

        {
            'mem_cfgs':         [cmip6_hist],
            'time_periods':     time_periods_cmip6_hist,
            'var_type':         'T_CLDF', 
        },
        {
            'mem_cfgs':         [cmip6_change],
            'var_type':         'T_CLDF', 
        },
        {
            'mem_cfgs':         [cmip6_hist],
            'time_periods':     time_periods_cmip6_hist,
            'var_type':         'RH_CLDF', 
        },
        {
            'mem_cfgs':         [cmip6_change],
            'var_type':         'RH_CLDF', 
        },

        {
            'mem_cfgs':         [mpi_hist],
            'time_periods':     time_periods_cmip6_hist,
            'var_type':         'T_CLDF', 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [mpi_change],
            'var_type':         'T_CLDF', 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [mpi_hist],
            'time_periods':     time_periods_cmip6_hist,
            'var_type':         'RH_CLDF', 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [mpi_change],
            'var_type':         'RH_CLDF', 
            'i_plot_cbar':      1,
        },
    ],
}



domain = dom_SA_ana_merid_cs
domain = dom_SA_ana_merid_cs_2
run_cfgs['clouds_change'] = {
    'fig': {
        'figsize':              (10.5, 8.5),
        'nrows':                3,
        'ncols':                3,
        'args_subplots_adjust': {
            'left':     0.09,
            'bottom':   0.15,
            'right':    0.98,
            'top':      0.93,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [0.15,0.15],
            'wspaces':  [0.10,0.40],
        },
        'kwargs_remove_axis_labels': {
            'remove_level':     2,
            'yexcept':          {'0,1':{'main':2,'twinx':0},'1,1':{'main':2,'twinx':0},'2,1':{'main':2,'twinx':0},
                                 '0,2':1,'1,2':1,'2,2':1},
        },
        'label_cfgs': [
            {'xrel':0.17,'yrel':0.97 ,  'text':'CTRL | HIST'},
            {'xrel':0.43,'yrel':0.97 ,  'text':'PGW | SCEN'},
            {'xrel':0.82,'yrel':0.97 ,  'text':'change'},

            {'xrel':0.01,'yrel':0.76 ,  'text':'COSMO',     'rotation':90},
            {'xrel':0.01,'yrel':0.47 ,  'text':'CMIP6-EM',  'rotation':90},
            {'xrel':0.01,'yrel':0.21 ,  'text':'MPI-ESM',   'rotation':90},
        ],
        'name_dict_append': {
            'dom': domain['key'],
        }
    },
    'glob_pan_cfg':   {
        'ana_number':       4,
        'agg_level':        TP.ALL_TIME,
        'line_at':          None,
        'alt_lims':         (0,18000),
        'line_along':       'lat',
        'plot_domain':      domain,
        'norm_inv':         0,
        'time_periods':     time_periods_ana,
        'i_plot_cbar':      0,
        'title':            '', 
        'pan_cbar_pad':     -5.5,
        'i_recompute':      0,
    },
    'pan_cfgs':    [
        {
            'mem_cfgs':         [ctrl],
            'var_type':         'CLDF_CLDF_PP', 
        },
        {
            'mem_cfgs':         [pgw],
            'var_type':         'CLDF_CLDF_PP', 
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_type':         'CLDF_CLDF', 
        },

        {
            'mem_cfgs':         [cmip6_hist],
            'time_periods':     time_periods_cmip6_hist,
            'var_type':         'CLDF_CLDF_PP', 
        },
        {
            'mem_cfgs':         [cmip6_scen],
            'time_periods':     time_periods_cmip6_scen,
            'var_type':         'CLDF_CLDF_PP', 
        },
        {
            'mem_cfgs':         [cmip6_change],
            'var_type':         'CLDF_CLDF', 
        },

        {
            'mem_cfgs':         [mpi_hist],
            'time_periods':     time_periods_cmip6_hist,
            'var_type':         'CLDF_CLDF_PP', 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [mpi_scen],
            'time_periods':     time_periods_cmip6_scen,
            'var_type':         'CLDF_CLDF_PP', 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [mpi_change],
            'var_type':         'CLDF_CLDF', 
            'i_plot_cbar':      1,
        },
    ],
}




run_cfgs['dyn_change'] = {
    'fig': {
        'figsize':              (9.5, 15),
        'nrows':                6,
        'ncols':                3,
        'args_subplots_adjust': {
            'left':     0.11,
            'bottom':   0.09,
            'right':    0.98,
            'top':      0.95,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [0.17,0.17,1.0,0.17,0.17],
            'wspaces':  [0.08,0.08],
        },
        'kwargs_remove_axis_labels': {
            'remove_level':     2,
            'xexcept':          {'2,0':0,'2,1':0,'2,2':0},
        },
        'label_cfgs': [
            {'xrel':0.01,'yrel':0.97,'text':nlv['VFLX']['label'],'fontsize':25},
            {'xrel':0.01,'yrel':0.49,'text':nlv['WFLX']['label'],'fontsize':25},

            {'xrel':0.18,'yrel':0.97 ,  'text':'CTRL | HIST'},
            {'xrel':0.46,'yrel':0.97 ,  'text':'PGW | SCEN'},
            {'xrel':0.79,'yrel':0.97 ,  'text':'change'},

            {'xrel':0.01,'yrel':0.87 ,  'text':'COSMO',     'rotation':90},
            {'xrel':0.01,'yrel':0.73 ,  'text':'CMIP6-EM',  'rotation':90},
            {'xrel':0.01,'yrel':0.60 ,  'text':'MPI-ESM',   'rotation':90},

            {'xrel':0.01,'yrel':0.38 ,  'text':'COSMO',     'rotation':90},
            {'xrel':0.01,'yrel':0.245,  'text':'CMIP6-EM',  'rotation':90},
            {'xrel':0.01,'yrel':0.115,  'text':'MPI-ESM',   'rotation':90},
        ],
    },
    'glob_pan_cfg':   {
        'ana_number':       4,
        'agg_level':        TP.ALL_TIME,
        'line_at':          None,
        'alt_lims':         (0,18000),
        'line_along':       'lat',
        'plot_domain':      dom_SA_ana_merid_cs,
        'norm_inv':         0,
        'time_periods':     time_periods_ana,
        'i_plot_cbar':      0,
        'title':            '',
    },
    'pan_cfgs':    [
        {
            'mem_cfgs':         [ctrl],
            'var_type':         'VFLX_CLDF', 
        },
        {
            'mem_cfgs':         [pgw],
            'var_type':         'VFLX_CLDF', 
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_type':         'VFLX_CLDF', 
        },

        {
            'mem_cfgs':         [cmip6_hist],
            'time_periods':     time_periods_cmip6_hist,
            'var_type':         'VFLX_CLDF', 
        },
        {
            'mem_cfgs':         [cmip6_scen],
            'time_periods':     time_periods_cmip6_scen,
            'var_type':         'VFLX_CLDF', 
        },
        {
            'mem_cfgs':         [cmip6_change],
            'var_type':         'VFLX_CLDF', 
        },

        {
            'mem_cfgs':         [mpi_hist],
            'time_periods':     time_periods_cmip6_hist,
            'var_type':         'VFLX_CLDF', 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [mpi_scen],
            'time_periods':     time_periods_cmip6_scen,
            'var_type':         'VFLX_CLDF', 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [mpi_change],
            'var_type':         'VFLX_CLDF', 
            'i_plot_cbar':      1,
        },




        {
            'mem_cfgs':         [ctrl],
            'var_type':         'WFLX_CLDF', 
        },
        {
            'mem_cfgs':         [pgw],
            'var_type':         'WFLX_CLDF', 
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_type':         'WFLX_CLDF', 
        },

        {
            'mem_cfgs':         [cmip6_hist],
            'time_periods':     time_periods_cmip6_hist,
            'var_type':         'WFLX_CLDF', 
        },
        {
            'mem_cfgs':         [cmip6_scen],
            'time_periods':     time_periods_cmip6_scen,
            'var_type':         'WFLX_CLDF', 
        },
        {
            'mem_cfgs':         [cmip6_change],
            'var_type':         'WFLX_CLDF', 
        },

        {
            'mem_cfgs':         [mpi_hist],
            'time_periods':     time_periods_cmip6_hist,
            'var_type':         'WFLX_CLDF', 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [mpi_scen],
            'time_periods':     time_periods_cmip6_scen,
            'var_type':         'WFLX_CLDF', 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [mpi_change],
            'var_type':         'WFLX_CLDF', 
            'i_plot_cbar':      1,
        },

    ],
}



## ATLANTIC CS
domain = dom_SA_ana_merid_cs
tp_winter = time_periods_ana_FMA
tp_spring = time_periods_ana_MJ
tp_summer = time_periods_ana_JAS
tp_autumn = time_periods_ana_ONDJ

tp_winter = time_periods_ana_DJF
tp_spring = time_periods_ana_MAM
tp_summer = time_periods_ana_JJA
tp_autumn = time_periods_ana_SON

tp_winter = time_periods_ana_FMA
tp_spring = time_periods_ana_MJJ
tp_summer = time_periods_ana_ASO
tp_autumn = time_periods_ana_NDJ

run_cfgs['test_dyn_seas'] = {
    'fig': {
        'figsize':              (15, 14),
        'nrows':                6,
        'ncols':                5,
        'args_subplots_adjust': args_subplots_adjust['{}x{}'.format(6,5)],
        'grid_spec':            dict(
                                    hspaces=[0.2,0.7,0.9,0.2,0.7],
                                    wspaces=[0.11,0.11,0.11,0.11],
                                ),
        'kwargs_remove_axis_labels': {
            'remove_level':     2,
        },
        'label_cfgs': [
            #{'xrel':0.12,'yrel':0.97,   'text':'Jan-Dec'},
            #{'xrel':0.30,'yrel':0.97,   'text':'Feb-Apr'},
            #{'xrel':0.49,'yrel':0.97,   'text':'May-June'},
            #{'xrel':0.68,'yrel':0.97,   'text':'July-Sep'},
            #{'xrel':0.87,'yrel':0.97,   'text':'Oct-Jan'},

            #{'xrel':0.12,'yrel':0.97,   'text':'Jan-Dec'},
            #{'xrel':0.30,'yrel':0.97,   'text':'DJF'},
            #{'xrel':0.49,'yrel':0.97,   'text':'MAM'},
            #{'xrel':0.68,'yrel':0.97,   'text':'JJA'},
            #{'xrel':0.87,'yrel':0.97,   'text':'SON'},

            {'xrel':0.12,'yrel':0.97,   'text':'Jan-Dec'},
            {'xrel':0.30,'yrel':0.97,   'text':'FMA'},
            {'xrel':0.49,'yrel':0.97,   'text':'MJJ'},
            {'xrel':0.68,'yrel':0.97,   'text':'ASO'},
            {'xrel':0.87,'yrel':0.97,   'text':'NDJ'},

            {'xrel':0.01,'yrel':0.88 ,  'text':'CTRL',      'rotation':90},
            {'xrel':0.01,'yrel':0.76 ,  'text':'PGW',       'rotation':90},
            {'xrel':0.01,'yrel':0.57 ,  'text':'PGW$-$CTRL','rotation':90},
            {'xrel':0.01,'yrel':0.43 ,  'text':'HIST',      'rotation':90},
            {'xrel':0.01,'yrel':0.28 ,  'text':'SCEN',      'rotation':90},
            {'xrel':0.01,'yrel':0.09 ,  'text':'SCEN$-$HIST',
                                                            'rotation':90},
        ],
        'name_dict_append': {
            'dom': domain['key'],
        }
    },
    'glob_pan_cfg':   {
        'ana_number':       4,
        'agg_level':        TP.ALL_TIME,
        'line_at':          None,
        'alt_lims':         (0,18000),
        'line_along':       'lat',
        'plot_domain':      domain,
        'norm_inv':         0,
        'time_periods':     time_periods_ana,
        'i_plot_cbar':      0,
        'var_type':         'WFLX_CLDF', 
        'title':            '', 
        'pan_cbar_pad':     -2,
    },
    'pan_cfgs':    [
        {
            'mem_cfgs':         [ctrl],
        },
        {
            'mem_cfgs':         [ctrl],
            'time_periods':     tp_winter,
        },
        {
            'mem_cfgs':         [ctrl],
            'time_periods':     tp_spring,
        },
        {
            'mem_cfgs':         [ctrl],
            'time_periods':     tp_summer,
        },
        {
            'mem_cfgs':         [ctrl],
            'time_periods':     tp_autumn,
        },


        {
            'mem_cfgs':         [pgw],
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [pgw],
            'time_periods':     tp_winter,
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [pgw],
            'time_periods':     tp_spring,
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [pgw],
            'time_periods':     tp_summer,
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [pgw],
            'time_periods':     tp_autumn,
            'i_plot_cbar':      1,
        },


        {
            'mem_cfgs':         [cosmo_change],
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'time_periods':     tp_winter,
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'time_periods':     tp_spring,
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'time_periods':     tp_summer,
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'time_periods':     tp_autumn,
            'i_plot_cbar':      1,
        },


        #{
        #    'mem_cfgs':         [cmip6_hist],
        #    'time_periods':     time_periods_cmip6_hist,
        #},
        #{
        #    'mem_cfgs':         [cmip6_hist],
        #    'time_periods':     time_periods_cmip6_hist_FMA,
        #},
        #{
        #    'mem_cfgs':         [cmip6_hist],
        #    'time_periods':     time_periods_cmip6_hist_MJ,
        #},
        #{
        #    'mem_cfgs':         [cmip6_hist],
        #    'time_periods':     time_periods_cmip6_hist_JAS,
        #},
        #{
        #    'mem_cfgs':         [cmip6_hist],
        #    'time_periods':     time_periods_cmip6_hist_ONDJ,
        #},


        #{
        #    'mem_cfgs':         [cmip6_scen],
        #    'time_periods':     time_periods_cmip6_scen,
        #    'i_plot_cbar':      1,
        #},
        #{
        #    'mem_cfgs':         [cmip6_scen],
        #    'time_periods':     time_periods_cmip6_scen_FMA,
        #    'i_plot_cbar':      1,
        #},
        #{
        #    'mem_cfgs':         [cmip6_scen],
        #    'time_periods':     time_periods_cmip6_scen_MJ,
        #    'i_plot_cbar':      1,
        #},
        #{
        #    'mem_cfgs':         [cmip6_scen],
        #    'time_periods':     time_periods_cmip6_scen_JAS,
        #    'i_plot_cbar':      1,
        #},
        #{
        #    'mem_cfgs':         [cmip6_scen],
        #    'time_periods':     time_periods_cmip6_scen_ONDJ,
        #    'i_plot_cbar':      1,
        #},


        #{
        #    'mem_cfgs':         [cmip6_change],
        #    'i_plot_cbar':      1,
        #    'pan_cbar_pad':     -5,
        #},
        #{
        #    'mem_cfgs':         [cmip6_change_FMA],
        #    'i_plot_cbar':      1,
        #    'pan_cbar_pad':     -5,
        #},
        #{
        #    'mem_cfgs':         [cmip6_change_MJ],
        #    'i_plot_cbar':      1,
        #    'pan_cbar_pad':     -5,
        #},
        #{
        #    'mem_cfgs':         [cmip6_change_JAS],
        #    'i_plot_cbar':      1,
        #    'pan_cbar_pad':     -5,
        #},
        #{
        #    'mem_cfgs':         [cmip6_change_ONDJ],
        #    'i_plot_cbar':      1,
        #    'pan_cbar_pad':     -5,
        #},
    ],
}

##############################################################################

run_cfgs['test_dyn_seas_W'] = copy.deepcopy(run_cfgs['test_dyn_seas'])
run_cfgs['test_dyn_seas_W']['glob_pan_cfg']['var_type'] = 'W_CLDF'

##############################################################################


use_cfg = 'suppl_1'
use_cfg = 'suppl_2'
#use_cfg = 'clouds_eval'
#use_cfg = 'thermo_dyn_eval'
#use_cfg = 'suppl_subs'
#
#use_cfg = 'spatial_eval'
#use_cfg = 'anncycle'
#use_cfg = 'spatial_change'
#use_cfg = 'thermo_change'
use_cfg = 'clouds_change'
#use_cfg = 'dyn_change'
##
#use_cfg = 'test_dyn_seas'
#use_cfg = 'test_dyn_seas_W'


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
    'sub_dir':              'heim_2022',
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
