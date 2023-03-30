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

run_cfgs['spatial_rad'] = {
    'fig': {
        'figsize':              (15, 7.5),
        'nrows':                3,
        'ncols':                5,
        'args_subplots_adjust': {
            'left':     0.09,
            'bottom':   0.15,
            'right':    0.98,
            'top':      0.92,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [0.06,0.06],
            'wspaces':  [0.10,0.20,0.40,0.10],
        },
        'kwargs_remove_axis_labels': {
            'remove_level':     2,
            'xexcept':          {'0,3':2,'0,4':2},
        },
        'label_cfgs': [
            {'xrel':0.15 ,'yrel':0.96 , 'text':'CTRL'},
            {'xrel':0.315,'yrel':0.96 , 'text':'PGW'},
            {'xrel':0.475,'yrel':0.96 , 'text':'PGW$-$CTRL'},
            {'xrel':0.69 ,'yrel':0.96 , 'text':'PGW$-$CTRL'},
            {'xrel':0.86 ,'yrel':0.96 , 'text':'CMIP6-EM'},
            {'xrel':0.855,'yrel':0.92 , 'text':'SCEN$-$HIST'},

            {'xrel':0.01 ,'yrel':0.71 , 'text':'high clouds',   'rotation':90},
            {'xrel':0.01 ,'yrel':0.45 , 'text':'mid clouds',    'rotation':90},
            {'xrel':0.01 ,'yrel':0.20 , 'text':'low clouds',    'rotation':90},

            {'xrel':0.62 ,'yrel':0.75 , 'text':'LW CRE',        'rotation':90},
            {'xrel':0.62 ,'yrel':0.22 , 'text':'SW CRE',        'rotation':90},
        ],
    },
    'glob_pan_cfg':   {
        'ana_number':       1,
        'agg_level':        TP.ALL_TIME,
        #'plot_domain':      dom_SA_ana_sea,
        'plot_domain':      dom_SA_ana,
        'time_periods':     time_periods_ana,
        'i_plot_cbar':      0,
        'pan_cbar_pos':     'lower center',
        'pan_cbar_pad':     -4.0,
        'cbar_label_mode':  'var_units',
        'title':            '', 
        #'add_bias_labels':  0,
        'i_recompute':      0,
        'add_bias_labels':  0,
    },
    'pan_cfgs':    [
        {
            'mem_cfgs':         [ctrl],
            'var_names':        ['CLCH'], 
        },
        {
            'i_recompute':      0,
            'mem_cfgs':         [pgw],
            'var_names':        ['CLCH'], 
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCH'], 
        },

        {
            'i_recompute':      1,
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRELWDTOA'], 
            #'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cmip6_change],
            'var_names':        ['CRELWDTOA'], 
            #'i_plot_cbar':      1,
        },


        {
            'mem_cfgs':         [ctrl],
            'var_names':        ['CLCM'], 
        },
        {
            'i_recompute':      0,
            'mem_cfgs':         [pgw],
            'var_names':        ['CLCM'], 
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCM'], 
        },
        None,
        None,


        {
            'mem_cfgs':         [ctrl],
            'var_names':        ['CLCL'], 
            'i_plot_cbar':      1,
        },
        {
            'i_recompute':      0,
            'mem_cfgs':         [pgw],
            'var_names':        ['CLCL'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCL'], 
            'i_plot_cbar':      1,
        },

        {
            'i_recompute':      1,
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRESWNDTOA'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cmip6_change],
            'var_names':        ['CRESWNDTOA'], 
            'i_plot_cbar':      1,
        },
    ],
}

##############################################################################

run_cfgs['spatial_cs_cosmo_mpi'] = {
    'fig': {
        'figsize':              (8, 10),
        'nrows':                4,
        'ncols':                2,
        'args_subplots_adjust': {
            'left':     0.14,
            'bottom':   0.05,
            'right':    0.90,
            'top':      0.94,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [0.15,0.35,0.15],
            'wspaces':  [0.02],
        },
        'kwargs_remove_axis_labels': {
            'remove_level':     2,
            #'xexcept':          {'0,3':2,'0,4':2},
        },
        'label_cfgs': [
            {'xrel':0.26 ,'yrel':0.97 , 'text':'COSMO'},
            {'xrel':0.65 ,'yrel':0.97 , 'text':'MPI-ESM'},

            {'xrel':0.01 ,'yrel':0.96 , 'text':'LW',  'fontsize':23},
            {'xrel':0.01 ,'yrel':0.48 , 'text':'SW',  'fontsize':23},

            {'xrel':0.01 ,'yrel':0.77 , 'text':'CTRL | HIST',   'rotation':90},
            {'xrel':0.01 ,'yrel':0.58 , 'text':'change',        'rotation':90},
            {'xrel':0.01 ,'yrel':0.29 , 'text':'CTRL | HIST',   'rotation':90},
            {'xrel':0.01 ,'yrel':0.105, 'text':'change',        'rotation':90},
        ],
    },
    'glob_pan_cfg':   {
        'ana_number':       1,
        'agg_level':        TP.ALL_TIME,
        'plot_domain':      dom_SA_ana_sea,
        'plot_domain':      dom_SA_ana,
        'time_periods':     time_periods_ana,
        'i_plot_cbar':      0,
        'pan_cbar_pos':     'center right',
        'pan_cbar_pad':     -1.0,
        'cbar_label_mode':  'var_units',
        'title':            '', 
        'add_bias_labels':  0,
        'i_recompute':      0,
    },
    'pan_cfgs':    [
        {
            'mem_cfgs':         [ctrl],
            'var_names':        ['CLWDTOA'], 
        },
        {
            'mem_cfgs':         [mpi_hist],
            'time_periods':     time_periods_cmip6_hist,
            'var_names':        ['CLWDTOA'], 
            'i_plot_cbar':      1,
        },


        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLWDTOA'], 
        },
        {
            'mem_cfgs':         [mpi_change],
            'var_names':        ['CLWDTOA'], 
            'i_plot_cbar':      1,
        },


        {
            'mem_cfgs':         [ctrl],
            'var_names':        ['CSWNDTOA'], 
        },
        {
            'mem_cfgs':         [mpi_hist],
            'time_periods':     time_periods_cmip6_hist,
            'var_names':        ['CSWNDTOA'], 
            'i_plot_cbar':      1,
        },


        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CSWNDTOA'], 
        },
        {
            'mem_cfgs':         [mpi_change],
            'var_names':        ['CSWNDTOA'], 
            'i_plot_cbar':      1,
        },
    ],
}

##############################################################################

run_cfgs['spatial_cre_cosmo_mpi'] = {
    'fig': {
        'figsize':              (8, 10),
        'nrows':                4,
        'ncols':                2,
        'args_subplots_adjust': {
            'left':     0.14,
            'bottom':   0.05,
            'right':    0.90,
            'top':      0.94,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [0.15,0.35,0.15],
            'wspaces':  [0.02],
        },
        'kwargs_remove_axis_labels': {
            'remove_level':     2,
            #'xexcept':          {'0,3':2,'0,4':2},
        },
        'label_cfgs': [
            {'xrel':0.26 ,'yrel':0.97 , 'text':'COSMO'},
            {'xrel':0.65 ,'yrel':0.97 , 'text':'MPI-ESM'},

            {'xrel':0.01 ,'yrel':0.97 , 'text':'LW CRE',  'fontsize':23},
            {'xrel':0.01 ,'yrel':0.49 , 'text':'SW CRE',  'fontsize':23},

            {'xrel':0.01 ,'yrel':0.77 , 'text':'CTRL | HIST',   'rotation':90},
            {'xrel':0.01 ,'yrel':0.58 , 'text':'change',        'rotation':90},
            {'xrel':0.01 ,'yrel':0.29 , 'text':'CTRL | HIST',   'rotation':90},
            {'xrel':0.01 ,'yrel':0.105, 'text':'change',        'rotation':90},
        ],
    },
    'glob_pan_cfg':   {
        'ana_number':       1,
        'agg_level':        TP.ALL_TIME,
        'plot_domain':      dom_SA_ana_sea,
        'plot_domain':      dom_SA_ana,
        'time_periods':     time_periods_ana,
        'i_plot_cbar':      0,
        'pan_cbar_pos':     'center right',
        'pan_cbar_pad':     -1.0,
        'cbar_label_mode':  'var_units',
        'title':            '', 
        'add_bias_labels':  0,
        'i_recompute':      0,
    },
    'pan_cfgs':    [
        {
            'mem_cfgs':         [ctrl],
            'var_names':        ['CRELWDTOA'], 
        },
        {
            'mem_cfgs':         [mpi_hist],
            'time_periods':     time_periods_cmip6_hist,
            'var_names':        ['CRELWDTOA'], 
            'i_plot_cbar':      1,
        },


        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRELWDTOA'], 
        },
        {
            'mem_cfgs':         [mpi_change],
            'var_names':        ['CRELWDTOA'], 
            'i_plot_cbar':      1,
        },


        {
            'mem_cfgs':         [ctrl],
            'var_names':        ['CRESWNDTOA'], 
        },
        {
            'mem_cfgs':         [mpi_hist],
            'time_periods':     time_periods_cmip6_hist,
            'var_names':        ['CRESWNDTOA'], 
            'i_plot_cbar':      1,
        },


        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRESWNDTOA'], 
        },
        {
            'mem_cfgs':         [mpi_change],
            'var_names':        ['CRESWNDTOA'], 
            'i_plot_cbar':      1,
        },
    ],
}

##############################################################################

tp_winter = time_periods_ana_FMA
tp_spring = time_periods_ana_MJJ
tp_summer = time_periods_ana_ASO
tp_autumn = time_periods_ana_NDJ
run_cfgs['spatial_rad_seas'] = {
    'fig': {
        'figsize':              (15, 12.5),
        'nrows':                5,
        'ncols':                5,
        'args_subplots_adjust': {
            'left':     0.09,
            'bottom':   0.15,
            'right':    0.98,
            'top':      0.92,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [0.06,0.06,0.60,0.10],
            'wspaces':  [0.20,0.10,0.10,0.10],
        },
        'kwargs_remove_axis_labels': {
            'remove_level':     2,
            'xexcept':          {'0,3':2,'0,4':2},
        },
        'label_cfgs': [
            {'xrel':0.15 ,'yrel':0.95 , 'text':'full year'},
            {'xrel':0.35 ,'yrel':0.95 , 'text':'FMA'},
            {'xrel':0.55 ,'yrel':0.95 , 'text':'MJJ'},
            {'xrel':0.70 ,'yrel':0.95 , 'text':'ASO'},
            {'xrel':0.90 ,'yrel':0.95 , 'text':'NDJ'},

            {'xrel':0.01 ,'yrel':0.80 , 'text':'high clouds',   'rotation':90},
            {'xrel':0.01 ,'yrel':0.66 , 'text':'mid clouds',    'rotation':90},
            {'xrel':0.01 ,'yrel':0.50 , 'text':'low clouds',    'rotation':90},
            {'xrel':0.01 ,'yrel':0.35 , 'text':'LW CRE',        'rotation':90},
            {'xrel':0.01 ,'yrel':0.20 , 'text':'SW CRE',        'rotation':90},

        ],
    },
    'glob_pan_cfg':   {
        'ana_number':       1,
        'agg_level':        TP.ALL_TIME,
        #'plot_domain':      dom_SA_ana_sea,
        'plot_domain':      dom_SA_ana,
        'i_plot_cbar':      0,
        'pan_cbar_pos':     'lower center',
        'pan_cbar_pad':     -4.0,
        'cbar_label_mode':  'var_units',
        'title':            '', 
        #'add_bias_labels':  0,
        'i_recompute':      0,
    },
    'pan_cfgs':    [
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCH'], 
            'time_periods':     time_periods_ana,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCH'], 
            'time_periods':     tp_winter,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCH'], 
            'time_periods':     tp_spring,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCH'], 
            'time_periods':     tp_summer,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCH'], 
            'time_periods':     tp_autumn,
        },


        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCM'], 
            'time_periods':     time_periods_ana,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCM'], 
            'time_periods':     tp_winter,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCM'], 
            'time_periods':     tp_spring,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCM'], 
            'time_periods':     tp_summer,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCM'], 
            'time_periods':     tp_autumn,
        },


        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCL'], 
            'time_periods':     time_periods_ana,
            'i_plot_cbar':      1,
            'pan_cbar_pad':     -3.0,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCL'], 
            'time_periods':     tp_winter,
            'i_plot_cbar':      1,
            'pan_cbar_pad':     -3.0,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCL'], 
            'time_periods':     tp_spring,
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCL'], 
            'time_periods':     tp_summer,
            'i_plot_cbar':      1,
            'pan_cbar_pad':     -3.0,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCL'], 
            'time_periods':     tp_autumn,
            'pan_cbar_pad':     -3.0,
        },


        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     time_periods_ana,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     tp_winter,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     tp_spring,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     tp_summer,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     tp_autumn,
        },


        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRESWNDTOA'], 
            'time_periods':     time_periods_ana,
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRESWNDTOA'], 
            'time_periods':     tp_winter,
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRESWNDTOA'], 
            'time_periods':     tp_spring,
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRESWNDTOA'], 
            'time_periods':     tp_summer,
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRESWNDTOA'], 
            'time_periods':     tp_autumn,
            'i_plot_cbar':      1,
        },
    ],
}


##############################################################################

tp_winter = time_periods_ana_FMA
tp_spring = time_periods_ana_MJJ
tp_summer = time_periods_ana_ASO
tp_autumn = time_periods_ana_NDJ
cmip6_hist_winter = cmip6_hist_FMA
cmip6_hist_spring = cmip6_hist_MJJ
cmip6_hist_summer = cmip6_hist_ASO 
cmip6_hist_autumn = cmip6_hist_NDJ
cmip6_change_winter = cmip6_change_FMA
cmip6_change_spring = cmip6_change_MJJ
cmip6_change_summer = cmip6_change_ASO 
cmip6_change_autumn = cmip6_change_NDJ
mpi_change_winter = mpi_change_FMA
mpi_change_spring = mpi_change_MJJ
mpi_change_summer = mpi_change_ASO 
mpi_change_autumn = mpi_change_NDJ
run_cfgs['spatial_rad_seas_cmip6'] = {
    'fig': {
        'figsize':              (15, 10.0),
        'nrows':                4,
        'ncols':                5,
        'args_subplots_adjust': {
            'left':     0.09,
            'bottom':   0.12,
            'right':    0.98,
            'top':      0.94,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [0.06,0.30,0.06],
            'wspaces':  [0.10,0.10,0.10,0.10],
        },
        'kwargs_remove_axis_labels': {
            'remove_level':     2,
            'xexcept':          {'1,0':0,'1,1':0,'1,2':0,'1,3':0,'1,4':0},
        },
        'label_cfgs': [
            {'xrel':0.15 ,'yrel':0.95 , 'text':'full year'},
            {'xrel':0.35 ,'yrel':0.95 , 'text':'FMA'},
            {'xrel':0.55 ,'yrel':0.95 , 'text':'MJJ'},
            {'xrel':0.70 ,'yrel':0.95 , 'text':'ASO'},
            {'xrel':0.90 ,'yrel':0.95 , 'text':'NDJ'},

            {'xrel':0.01 ,'yrel':0.96 , 'text':'LW CRE',   'fontsize':22},
            {'xrel':0.01 ,'yrel':0.53 , 'text':'SW CRE',   'fontsize':22},

            {'xrel':0.01 ,'yrel':0.80 , 'text':'COSMO',      'rotation':90},
            {'xrel':0.01 ,'yrel':0.59 , 'text':'CMIP6-EM',   'rotation':90},
            {'xrel':0.01 ,'yrel':0.37 , 'text':'COSMO',      'rotation':90},
            {'xrel':0.01 ,'yrel':0.15 , 'text':'CMIP6-EM',   'rotation':90},

        ],
    },
    'glob_pan_cfg':   {
        'ana_number':       1,
        'agg_level':        TP.ALL_TIME,
        #'plot_domain':      dom_SA_ana_sea,
        'plot_domain':      dom_SA_ana,
        'i_plot_cbar':      0,
        'pan_cbar_pos':     'lower center',
        'pan_cbar_pad':     -4.0,
        'cbar_label_mode':  'var_units',
        'title':            '', 
        #'add_bias_labels':  0,
        'i_recompute':      0,
    },
    'pan_cfgs':    [
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     time_periods_ana,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     tp_winter,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     tp_spring,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     tp_summer,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     tp_autumn,
        },


        {
            'mem_cfgs':         [cmip6_change],
            'var_names':        ['CRELWDTOA'], 
        },
        {
            'mem_cfgs':         [cmip6_change_winter],
            'var_names':        ['CRELWDTOA'], 
        },
        {
            'mem_cfgs':         [cmip6_change_spring],
            'var_names':        ['CRELWDTOA'], 
        },
        {
            'mem_cfgs':         [cmip6_change_summer],
            'var_names':        ['CRELWDTOA'], 
        },
        {
            'mem_cfgs':         [cmip6_change_autumn],
            'var_names':        ['CRELWDTOA'], 
        },


        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRESWNDTOA'], 
            'time_periods':     time_periods_ana,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRESWNDTOA'], 
            'time_periods':     tp_winter,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRESWNDTOA'], 
            'time_periods':     tp_spring,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRESWNDTOA'], 
            'time_periods':     tp_summer,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRESWNDTOA'], 
            'time_periods':     tp_autumn,
        },


        {
            'mem_cfgs':         [cmip6_change],
            'var_names':        ['CRESWNDTOA'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cmip6_change_winter],
            'var_names':        ['CRESWNDTOA'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cmip6_change_spring],
            'var_names':        ['CRESWNDTOA'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cmip6_change_summer],
            'var_names':        ['CRESWNDTOA'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cmip6_change_autumn],
            'var_names':        ['CRESWNDTOA'], 
            'i_plot_cbar':      1,
        },


    ],
}



run_cfgs['spatial_LW'] = {
    'fig': {
        'figsize':              (15, 10.0),
        'nrows':                4,
        'ncols':                5,
        'args_subplots_adjust': {
            'left':     0.09,
            'bottom':   0.12,
            'right':    0.98,
            'top':      0.94,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [0.06,0.60,0.06],
            'wspaces':  [0.10,0.10,0.10,0.10],
        },
        'kwargs_remove_axis_labels': {
            'remove_level':     2,
            'xexcept':          {'1,0':0,'1,1':0,'1,2':0,'1,3':0,'1,4':0},
        },
        'label_cfgs': [
            {'xrel':0.15 ,'yrel':0.95 , 'text':'full year'},
            {'xrel':0.35 ,'yrel':0.95 , 'text':'FMA'},
            {'xrel':0.55 ,'yrel':0.95 , 'text':'MJJ'},
            {'xrel':0.70 ,'yrel':0.95 , 'text':'ASO'},
            {'xrel':0.90 ,'yrel':0.95 , 'text':'NDJ'},

            {'xrel':0.01 ,'yrel':0.96 , 'text':'LW CRE',   'fontsize':22},
            {'xrel':0.01 ,'yrel':0.53 , 'text':'SW CRE',   'fontsize':22},

            {'xrel':0.01 ,'yrel':0.80 , 'text':'COSMO',      'rotation':90},
            {'xrel':0.01 ,'yrel':0.59 , 'text':'CMIP6-EM',   'rotation':90},
            {'xrel':0.01 ,'yrel':0.37 , 'text':'COSMO',      'rotation':90},
            {'xrel':0.01 ,'yrel':0.15 , 'text':'CMIP6-EM',   'rotation':90},

        ],
    },
    'glob_pan_cfg':   {
        'ana_number':       1,
        'agg_level':        TP.ALL_TIME,
        #'plot_domain':      dom_SA_ana_sea,
        'plot_domain':      dom_SA_ana,
        'i_plot_cbar':      0,
        'pan_cbar_pos':     'lower center',
        'pan_cbar_pad':     -4.0,
        'cbar_label_mode':  'var_units',
        'title':            '', 
        #'add_bias_labels':  0,
        'i_recompute':      0,
    },
    'pan_cfgs':    [
        {
            'mem_cfgs':         [ctrl],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     time_periods_ana,
        },
        {
            'mem_cfgs':         [ctrl],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     tp_winter,
        },
        {
            'mem_cfgs':         [ctrl],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     tp_spring,
        },
        {
            'mem_cfgs':         [ctrl],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     tp_summer,
        },
        {
            'mem_cfgs':         [ctrl],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     tp_autumn,
        },

        {
            'mem_cfgs':         [cmip6_hist],
            'var_names':        ['CRELWDTOA'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cmip6_hist_winter],
            'var_names':        ['CRELWDTOA'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cmip6_hist_spring],
            'var_names':        ['CRELWDTOA'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cmip6_hist_summer],
            'var_names':        ['CRELWDTOA'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cmip6_hist_autumn],
            'var_names':        ['CRELWDTOA'], 
            'i_plot_cbar':      1,
        },



        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     time_periods_ana,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     tp_winter,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     tp_spring,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     tp_summer,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     tp_autumn,
        },



        {
            'mem_cfgs':         [cmip6_change],
            'var_names':        ['CRELWDTOA'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cmip6_change_winter],
            'var_names':        ['CRELWDTOA'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cmip6_change_spring],
            'var_names':        ['CRELWDTOA'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cmip6_change_summer],
            'var_names':        ['CRELWDTOA'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cmip6_change_autumn],
            'var_names':        ['CRELWDTOA'], 
            'i_plot_cbar':      1,
        },
    ],
}





run_cfgs['spatial_LW_COSMO'] = {
    'fig': {
        'figsize':              (15, 20),
        'nrows':                7,
        'ncols':                5,
        'args_subplots_adjust': {
            'left':     0.09,
            'bottom':   0.12,
            'right':    0.98,
            'top':      0.94,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [0.80,0.80,0.80,0.80,0.80,0.80],
            'wspaces':  [0.10,0.10,0.10,0.10],
        },
        'kwargs_remove_axis_labels': {
            'remove_level':     2,
            #'xexcept':          {'1,0':0,'1,1':0,'1,2':0,'1,3':0,'1,4':0},
        },
        'label_cfgs': [
            {'xrel':0.15 ,'yrel':0.95 , 'text':'full year'},
            {'xrel':0.35 ,'yrel':0.95 , 'text':'FMA'},
            {'xrel':0.55 ,'yrel':0.95 , 'text':'MJJ'},
            {'xrel':0.70 ,'yrel':0.95 , 'text':'ASO'},
            {'xrel':0.90 ,'yrel':0.95 , 'text':'NDJ'},

            #{'xrel':0.01 ,'yrel':0.96 , 'text':'LW CRE',   'fontsize':22},
            #{'xrel':0.01 ,'yrel':0.53 , 'text':'SW CRE',   'fontsize':22},

            #{'xrel':0.01 ,'yrel':0.80 , 'text':'COSMO',      'rotation':90},
            #{'xrel':0.01 ,'yrel':0.59 , 'text':'CMIP6-EM',   'rotation':90},
            #{'xrel':0.01 ,'yrel':0.37 , 'text':'COSMO',      'rotation':90},
            #{'xrel':0.01 ,'yrel':0.15 , 'text':'CMIP6-EM',   'rotation':90},

        ],
    },
    'glob_pan_cfg':   {
        'ana_number':       1,
        'agg_level':        TP.ALL_TIME,
        #'plot_domain':      dom_SA_ana_sea,
        'plot_domain':      dom_SA_ana,
        'i_plot_cbar':      0,
        'pan_cbar_pos':     'lower center',
        #'pan_cbar_pad':     -4.0,
        'pan_cbar_pad':     -2.2,
        'cbar_label_mode':  'var_units',
        'title':            '', 
        #'add_bias_labels':  0,
        'i_recompute':      0,
    },
    'pan_cfgs':    [
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     time_periods_ana,
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     tp_winter,
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     tp_spring,
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     tp_summer,
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     tp_autumn,
            'i_plot_cbar':      1,
        },


        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['TSURF'], 
            'time_periods':     time_periods_ana,
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['TSURF'], 
            'time_periods':     tp_winter,
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['TSURF'], 
            'time_periods':     tp_spring,
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['TSURF'], 
            'time_periods':     tp_summer,
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['TSURF'], 
            'time_periods':     tp_autumn,
            'i_plot_cbar':      1,
        },


        #{
        #    'mem_cfgs':         [mpi_change],
        #    'var_names':        ['TSURF'], 
        #    'i_plot_cbar':      1,
        #},
        #{
        #    'mem_cfgs':         [mpi_change_winter],
        #    'var_names':        ['TSURF'], 
        #    'i_plot_cbar':      1,
        #},
        #{
        #    'mem_cfgs':         [mpi_change_spring],
        #    'var_names':        ['TSURF'], 
        #    'i_plot_cbar':      1,
        #},
        #{
        #    'mem_cfgs':         [mpi_change_summer],
        #    'var_names':        ['TSURF'], 
        #    'i_plot_cbar':      1,
        #},
        #{
        #    'mem_cfgs':         [mpi_change_autumn],
        #    'var_names':        ['TSURF'], 
        #    'i_plot_cbar':      1,
        #},



        {
            'mem_cfgs':         [{
                'mem_oper':'bias',
                'mem_keys':[
                    cosmo_change,
                    mpi_change,
                ],
                'time_periods': time_periods_ana,
            }],
            'var_names':        ['CRELWDTOA'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [{
                'mem_oper':'bias',
                'mem_keys':[
                    cosmo_change,
                    mpi_change_winter,
                ],
                'time_periods': tp_winter,
            }],
            'var_names':        ['CRELWDTOA'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [{
                'mem_oper':'bias',
                'mem_keys':[
                    cosmo_change,
                    mpi_change_spring,
                ],
                'time_periods': tp_spring,
            }],
            'var_names':        ['CRELWDTOA'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [{
                'mem_oper':'bias',
                'mem_keys':[
                    cosmo_change,
                    mpi_change_summer,
                ],
                'time_periods': tp_summer,
            }],
            'var_names':        ['CRELWDTOA'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [{
                'mem_oper':'bias',
                'mem_keys':[
                    cosmo_change,
                    mpi_change_autumn,
                ],
                'time_periods': tp_autumn,
            }],
            'var_names':        ['CRELWDTOA'], 
            'i_plot_cbar':      1,
        },




        {
            'mem_cfgs':         [{
                'mem_oper':'bias',
                'mem_keys':[
                    cosmo_change,
                    mpi_change,
                ],
                'time_periods': time_periods_ana,
            }],
            'var_names':        ['TSURF'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [{
                'mem_oper':'bias',
                'mem_keys':[
                    cosmo_change,
                    mpi_change_winter,
                ],
                'time_periods': tp_winter,
            }],
            'var_names':        ['TSURF'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [{
                'mem_oper':'bias',
                'mem_keys':[
                    cosmo_change,
                    mpi_change_spring,
                ],
                'time_periods': tp_spring,
            }],
            'var_names':        ['TSURF'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [{
                'mem_oper':'bias',
                'mem_keys':[
                    cosmo_change,
                    mpi_change_summer,
                ],
                'time_periods': tp_summer,
            }],
            'var_names':        ['TSURF'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [{
                'mem_oper':'bias',
                'mem_keys':[
                    cosmo_change,
                    mpi_change_autumn,
                ],
                'time_periods': tp_autumn,
            }],
            'var_names':        ['TSURF'], 
            'i_plot_cbar':      1,
        },




        {
            'mem_cfgs':         [{
                'mem_oper':'bias',
                'mem_keys':[
                    cosmo_change,
                    mpi_change,
                ],
                'time_periods': time_periods_ana,
            }],
            'var_names':        ['QV@alt=3000'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [{
                'mem_oper':'bias',
                'mem_keys':[
                    cosmo_change,
                    mpi_change_winter,
                ],
                'time_periods': tp_winter,
            }],
            'var_names':        ['QV@alt=3000'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [{
                'mem_oper':'bias',
                'mem_keys':[
                    cosmo_change,
                    mpi_change_spring,
                ],
                'time_periods': tp_spring,
            }],
            'var_names':        ['QV@alt=3000'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [{
                'mem_oper':'bias',
                'mem_keys':[
                    cosmo_change,
                    mpi_change_summer,
                ],
                'time_periods': tp_summer,
            }],
            'var_names':        ['QV@alt=3000'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [{
                'mem_oper':'bias',
                'mem_keys':[
                    cosmo_change,
                    mpi_change_autumn,
                ],
                'time_periods': tp_autumn,
            }],
            'var_names':        ['QV@alt=3000'], 
            'i_plot_cbar':      1,
        },




        {
            'mem_cfgs':         [{
                'mem_oper':'bias',
                'mem_keys':[
                    cosmo_change,
                    mpi_change,
                ],
                'time_periods': time_periods_ana,
            }],
            'var_names':        ['T@alt=3000'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [{
                'mem_oper':'bias',
                'mem_keys':[
                    cosmo_change,
                    mpi_change_winter,
                ],
                'time_periods': tp_winter,
            }],
            'var_names':        ['T@alt=3000'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [{
                'mem_oper':'bias',
                'mem_keys':[
                    cosmo_change,
                    mpi_change_spring,
                ],
                'time_periods': tp_spring,
            }],
            'var_names':        ['T@alt=3000'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [{
                'mem_oper':'bias',
                'mem_keys':[
                    cosmo_change,
                    mpi_change_summer,
                ],
                'time_periods': tp_summer,
            }],
            'var_names':        ['T@alt=3000'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [{
                'mem_oper':'bias',
                'mem_keys':[
                    cosmo_change,
                    mpi_change_autumn,
                ],
                'time_periods': tp_autumn,
            }],
            'var_names':        ['T@alt=3000'], 
            'i_plot_cbar':      1,
        },




        {
            'mem_cfgs':         [{
                'mem_oper':'bias',
                'mem_keys':[
                    cosmo_change,
                    mpi_change,
                ],
                'time_periods': time_periods_ana,
            }],
            'var_names':        ['RH@alt=3000'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [{
                'mem_oper':'bias',
                'mem_keys':[
                    cosmo_change,
                    mpi_change_winter,
                ],
                'time_periods': tp_winter,
            }],
            'var_names':        ['RH@alt=3000'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [{
                'mem_oper':'bias',
                'mem_keys':[
                    cosmo_change,
                    mpi_change_spring,
                ],
                'time_periods': tp_spring,
            }],
            'var_names':        ['RH@alt=3000'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [{
                'mem_oper':'bias',
                'mem_keys':[
                    cosmo_change,
                    mpi_change_summer,
                ],
                'time_periods': tp_summer,
            }],
            'var_names':        ['RH@alt=3000'], 
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [{
                'mem_oper':'bias',
                'mem_keys':[
                    cosmo_change,
                    mpi_change_autumn,
                ],
                'time_periods': tp_autumn,
            }],
            'var_names':        ['RH@alt=3000'], 
            'i_plot_cbar':      1,
        },



        #{
        #    'mem_cfgs':         [cosmo_change],
        #    'var_names':        ['RH@alt=3000'], 
        #    'time_periods':     time_periods_ana,
        #    'i_plot_cbar':      1,
        #},
        #{
        #    'mem_cfgs':         [cosmo_change],
        #    'var_names':        ['RH@alt=3000'], 
        #    'time_periods':     tp_winter,
        #    'i_plot_cbar':      1,
        #},
        #{
        #    'mem_cfgs':         [cosmo_change],
        #    'var_names':        ['RH@alt=3000'], 
        #    'time_periods':     tp_spring,
        #    'i_plot_cbar':      1,
        #},
        #{
        #    'mem_cfgs':         [cosmo_change],
        #    'var_names':        ['RH@alt=3000'], 
        #    'time_periods':     tp_summer,
        #    'i_plot_cbar':      1,
        #},
        #{
        #    'mem_cfgs':         [cosmo_change],
        #    'var_names':        ['RH@alt=3000'], 
        #    'time_periods':     tp_autumn,
        #    'i_plot_cbar':      1,
        #},

        #{
        #    'mem_cfgs':         [{
        #        'mem_oper':'diff',
        #        'mem_keys':[
        #            {
        #                'mem_oper':     'diff',
        #                'mem_keys':     [pgw, ctrl],
        #                'time_periods': tp_autumn,
        #            },
        #            mpi_change_autumn,
        #        ],
        #    }],
        #    'var_names':        ['TSURF'], 
        #    'i_plot_cbar':      1,
        #},
    ],
}





tp_winter = time_periods_ana_JFM
tp_spring = time_periods_ana_AMJ
tp_summer = time_periods_ana_JAS
tp_autumn = time_periods_ana_OND
run_cfgs['spatial_anncycle'] = {
    'fig': {
        'figsize':              (15, 12.5),
        'nrows':                5,
        'ncols':                5,
        'args_subplots_adjust': {
            'left':     0.09,
            'bottom':   0.12,
            'right':    0.98,
            'top':      0.94,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [0.06,0.60,0.06,0.06],
            'wspaces':  [0.10,0.10,0.10,0.10],
        },
        'kwargs_remove_axis_labels': {
            'remove_level':     2,
            'xexcept':          {'1,0':0,'1,1':0,'1,2':0,'1,3':0,'1,4':0},
        },
        'label_cfgs': [
            {'xrel':0.15 ,'yrel':0.95 , 'text':'full year'},
            #{'xrel':0.35 ,'yrel':0.95 , 'text':'FMA'},
            #{'xrel':0.55 ,'yrel':0.95 , 'text':'MJJ'},
            #{'xrel':0.70 ,'yrel':0.95 , 'text':'ASO'},
            #{'xrel':0.90 ,'yrel':0.95 , 'text':'NDJ'},

            {'xrel':0.35 ,'yrel':0.95 , 'text':'JFM'},
            {'xrel':0.55 ,'yrel':0.95 , 'text':'AMJ'},
            {'xrel':0.70 ,'yrel':0.95 , 'text':'JAS'},
            {'xrel':0.90 ,'yrel':0.95 , 'text':'OND'},

            #{'xrel':0.01 ,'yrel':0.96 , 'text':'LW CRE',   'fontsize':22},
            #{'xrel':0.01 ,'yrel':0.53 , 'text':'SW CRE',   'fontsize':22},

            #{'xrel':0.01 ,'yrel':0.80 , 'text':'COSMO',      'rotation':90},
            #{'xrel':0.01 ,'yrel':0.59 , 'text':'CMIP6-EM',   'rotation':90},
            #{'xrel':0.01 ,'yrel':0.37 , 'text':'COSMO',      'rotation':90},
            #{'xrel':0.01 ,'yrel':0.15 , 'text':'CMIP6-EM',   'rotation':90},

        ],
    },
    'glob_pan_cfg':   {
        'ana_number':       1,
        'agg_level':        TP.ALL_TIME,
        #'plot_domain':      dom_SA_ana_sea,
        'plot_domain':      dom_SA_ana,
        'i_plot_cbar':      0,
        'pan_cbar_pos':     'lower center',
        'pan_cbar_pad':     -4.0,
        'cbar_label_mode':  'var_units',
        'title':            '', 
        #'add_bias_labels':  0,
        'i_recompute':      0,
    },
    'pan_cfgs':    [
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     time_periods_ana,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     tp_winter,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     tp_spring,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     tp_summer,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRELWDTOA'], 
            'time_periods':     tp_autumn,
        },


        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCH'], 
            'time_periods':     time_periods_ana,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCH'], 
            'time_periods':     tp_winter,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCH'], 
            'time_periods':     tp_spring,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCH'], 
            'time_periods':     tp_summer,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCH'], 
            'time_periods':     tp_autumn,
        },


        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRESWNDTOA'], 
            'time_periods':     time_periods_ana,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRESWNDTOA'], 
            'time_periods':     tp_winter,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRESWNDTOA'], 
            'time_periods':     tp_spring,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRESWNDTOA'], 
            'time_periods':     tp_summer,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CRESWNDTOA'], 
            'time_periods':     tp_autumn,
        },


        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCM'], 
            'time_periods':     time_periods_ana,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCM'], 
            'time_periods':     tp_winter,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCM'], 
            'time_periods':     tp_spring,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCM'], 
            'time_periods':     tp_summer,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCM'], 
            'time_periods':     tp_autumn,
        },


        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCL'], 
            'time_periods':     time_periods_ana,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCL'], 
            'time_periods':     tp_winter,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCL'], 
            'time_periods':     tp_spring,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCL'], 
            'time_periods':     tp_summer,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLCL'], 
            'time_periods':     tp_autumn,
        },
    ],
}




##############################################################################
use_domain = dom_trades_full
use_domain = dom_trades_NA

mem_dicts = dict(ctrl=[],pgw=[],diff=[],rel=[])
tp_dict = {
    #'SON':  time_periods_ana_SON,
    #'DJF':  time_periods_ana_DJF,
    #'MAM':  time_periods_ana_MAM,
    #'JJA':  time_periods_ana_JJA,
    #'ASO':  time_periods_ana_ASO,
    #'NDJ':  time_periods_ana_NDJ,
    #'FMA':  time_periods_ana_FMA,
    #'MJJ':  time_periods_ana_MJJ,
    'JAS':  time_periods_ana_JAS,
    'OND':  time_periods_ana_OND,
    'JFM':  time_periods_ana_JFM,
    'AMJ':  time_periods_ana_AMJ,
    'annual': time_periods_ana, 
}
colors = ['red','orange','green','blue','k']
linestyles = ['-','-','-','-','-']
linewidths = [1,1,1,1,2]
i = 0
for tp_key,tp in tp_dict.items():
    mem_dicts['ctrl'].append({
        'mem_key':      ctrl['mem_key'], 
        'time_periods': tp,
        'color':        colors[i], 
        #'linestyle':    linestyles[i], 
        #'linestyle':    '-', 
        'linewidth':    linewidths[i], 
        'label':        tp_key, 
    })
    mem_dicts['pgw'].append({
        'mem_key':      pgw['mem_key'], 
        'time_periods': tp,
        'color':        colors[i], 
        'linestyle':    '--', 
        'linewidth':    linewidths[i], 
        'label':        tp_key, 
    })
    mem_dicts['diff'].append({
        'mem_oper':     'diff',
        'mem_keys':     [pgw, ctrl],
        'time_periods': tp,
        'color':        colors[i], 
        #'linestyle':    linestyles[i], 
        'linewidth':    linewidths[i], 
        'label':        tp_key, 
    })
    mem_dicts['rel'].append({
        'mem_oper':     'rel0.001',
        'mem_keys':     [pgw, ctrl],
        'time_periods': tp,
        'color':        colors[i], 
        #'linestyle':    linestyles[i], 
        'linewidth':    linewidths[i], 
        'label':        tp_key, 
    })
    i += 1

mem_dicts['abs'] = []
mem_dicts['abs'].extend(mem_dicts['ctrl'])
mem_dicts['abs'].extend(mem_dicts['pgw'])


run_cfgs['trades_env'] = {
    'fig': {
        'figsize':              (12, 11.5),
        'nrows':                5,
        'ncols':                4,
        'args_subplots_adjust': {
            'left':     0.07,
            'bottom':   0.05,
            'right':    0.98,
            'top':      0.90,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [0.30,0.30,0.80,0.30],
            'wspaces':  [0.30,0.50,0.30],
        },
        'kwargs_remove_axis_labels': {
            'remove_level':     1,
            'xexcept':          {
                '0,0':2,'0,1':2,'0,2':2,'0,3':2,
                '1,0':0,'1,1':0,'1,2':2,'1,3':2,
                                '2,2':0,'2,3':0,
                '3,0':2,'3,1':2,'3,2':2,'3,3':2,
                '4,0':0,'4,1':0,'4,2':0,'4,3':0,
            },
            'yexcept':          {'0,2':0,'1,2':0,'2,2':0,'3,2':0,'4,2':0},
        },
        'label_cfgs': [
            {'xrel':0.13 ,'yrel':0.97 , 'text':'CTRL',          'fontsize':22},
            {'xrel':0.32 ,'yrel':0.97 , 'text':'PGW$-$CTRL',    'fontsize':22},
            {'xrel':0.63 ,'yrel':0.97 , 'text':'CTRL',          'fontsize':22},
            {'xrel':0.82 ,'yrel':0.97 , 'text':'PGW$-$CTRL',    'fontsize':22},

            #{'xrel':0.22 ,'yrel':0.93 , 'text':'SW CRE',        'fontsize':22},
            #{'xrel':0.22 ,'yrel':0.74 , 'text':'stability',     'fontsize':22},
            #{'xrel':0.68 ,'yrel':0.74 , 'text':'thermodynamic', 'fontsize':22},
            #{'xrel':0.22 ,'yrel':0.23 , 'text':'dynamic',       'fontsize':22},

            {'xrel':0.21 ,'yrel':0.93 , 'text':'cloud field',   'fontsize':22},
            {'xrel':0.725,'yrel':0.93 , 'text':'stability',     'fontsize':22},
            {'xrel':0.72 ,'yrel':0.37 , 'text':'dynamic',       'fontsize':22},
            {'xrel':0.18 ,'yrel':0.37 , 'text':'thermodynamic', 'fontsize':22},
        ],
        'name_dict_append': {
            'dom': use_domain['key'],
        }
    },
    'glob_pan_cfg':   {
        'ana_number':       15,
        'agg_level':        TP.ALL_TIME,
        'plot_domain':      use_domain,
        'line_along':       'lon',
        'line_at':          slice(dom_trades_full['lat'].start,dom_trades_full['lat'].stop),
        'time_periods':     time_periods_ana,
        'i_plot_legend':    0,
        'i_recompute':      0,
    },
    'pan_cfgs':    [
        {
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['CLCL']}, 
            'i_plot_legend':    1,
            'title':            nlv['CLCL']['label'],
        },
        {
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['CLCL']}, 
            'title':            nlv['CLCL']['label'],
        },


        {
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['LTS']}, 
            'title':            nlv['LTS']['label'],
        },
        {
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['LTS']}, 
            'title':            nlv['LTS']['label'],
        },



        {
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['CRESWNDTOA']}, 
            'title':            nlv['CRESWNDTOA']['label'],
        },
        {
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['CRESWNDTOA']}, 
            'title':            nlv['CRESWNDTOA']['label'],
        },


        {
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['SST']}, 
            'title':            nlv['SST']['label'],
        },
        {
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['SST']}, 
            'title':            nlv['SST']['label'],
        },

        

        None,
        None,


        {
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['T@alt=3000']}, 
            'title':            '{}'.format(nlv['T']['label'])+'$_{3km}$',
        },
        {
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['T@alt=3000']}, 
            'title':            '{}'.format(nlv['T']['label'])+'$_{3km}$',
        },



        {
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['DQVINV']}, 
            'title':            nlv['DQVINV']['label'],
        },
        {
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['DQVINV']}, 
            'title':            nlv['DQVINV']['label'],
        },


        {
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['W@alt=3000']}, 
            'title':            '{}'.format(nlv['W']['label'])+'$_{3km}$',
        },
        {
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['W@alt=3000']}, 
            'title':            '{}'.format(nlv['W']['label'])+'$_{3km}$',
            'i_recompute':      1,
        },



        {
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['RH@alt=3000']}, 
            'title':            '{}'.format(nlv['RH']['label'])+'$_{3km}$',
        },
        {
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['RH@alt=3000']}, 
            'title':            '{}'.format(nlv['RH']['label'])+'$_{3km}$',
        },


        {
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['UV10M']}, 
            'title':            nlv['UV10M']['label'],
        },
        {
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['UV10M']}, 
            'title':            nlv['UV10M']['label'],
            'i_recompute':      1,
        },
    ],
}

##############################################################################

run_cfgs['trades_mbl'] = {
    'fig': {
        'figsize':              (6.5, 7.5),
        'nrows':                3,
        'ncols':                2,
        'args_subplots_adjust': {
            'left':     0.12,
            'bottom':   0.08,
            'right':    0.98,
            'top':      0.92,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [0.30,0.30,0.30],
            'wspaces':  [0.40],
        },
        'kwargs_remove_axis_labels': {
            'remove_level':     1,
            'xexcept':          {'0,0':2,'0,1':2,'1,0':2,'1,1':2,},
        },
        'label_cfgs': [
            {'xrel':0.25 ,'yrel':0.97 , 'text':'CTRL'},
            {'xrel':0.69 ,'yrel':0.97 , 'text':'PGW$-$CTRL'},
        ],
    },
    'glob_pan_cfg':   {
        'ana_number':       15,
        'agg_level':        TP.ALL_TIME,
        'plot_domain':      dom_trades_full,
        'time_periods':     time_periods_ana,
        'i_plot_legend':    0,
        'line_along':       'lon',
        'i_recompute':      1,
    },
    'pan_cfgs':    [
        {
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['ENTR']}, 
            'title':            nlv['ENTR']['label'],
        },
        {
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['ENTR']}, 
            'title':            nlv['ENTR']['label'],
        },

        {
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['INVHGT']}, 
            'i_plot_legend':    1,
            'title':            nlv['INVHGT']['label'],
        },
        {
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['INVHGT']}, 
            'title':            nlv['INVHGT']['label'],
        },

        {
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['LCL']}, 
            'title':            nlv['LCL']['label'],
        },
        {
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['LCL']}, 
            'title':            nlv['LCL']['label'],
        },
    ],
}

##############################################################################
use_domain = dom_trades_full
#use_domain = dom_trades_NA

run_cfgs['trades_qv'] = {
    'fig': {
        'figsize':              (17.0, 12.5),
        'nrows':                6,
        'ncols':                6,
        'args_subplots_adjust': {
            'left':     0.06,
            'bottom':   0.08,
            'right':    0.98,
            'top':      0.92,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [0.30,0.30,0.30,0.30,0.30],
            'wspaces':  [0.30,0.50,0.30,0.50,0.30],
        },
        'kwargs_remove_axis_labels': {
            'remove_level':     1,
            'xexcept':          {'0,0':2,'0,1':2,'1,0':2,'1,1':2,},
            'yexcept':          {'0,4':0,'1,4':0,'2,4':0,},
        },
        'label_cfgs': [
            {'xrel':0.25 ,'yrel':0.97 , 'text':'CTRL'},
            {'xrel':0.69 ,'yrel':0.97 , 'text':'PGW$-$CTRL'},
        ],
        'name_dict_append': {
            'dom': use_domain['key'],
        }
    },
    'glob_pan_cfg':   {
        'ana_number':       15,
        'agg_level':        TP.ALL_TIME,
        'plot_domain':      use_domain,
        'time_periods':     time_periods_ana,
        #'time_periods':     time_periods_2007,
        #'time_periods':     get_time_periods_for_month(2007, 8),
        'i_plot_legend':    0,
        'line_along':       'lon',
        'i_recompute':      1,
    },
    'pan_cfgs':    [
        {
            #'mem_cfgs':         [ctrl],
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['CLCL']}, 
            'title':            nlv['CLCL']['label'],
            'i_plot_legend':    1,
        },
        {
            #'mem_cfgs':         [cosmo_change],
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['CLCL']}, 
            'title':            nlv['CLCL']['label'],
        },
        None,
        None,
        None,
        None,
        

        {
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['dQVdt_MBL_LH']}, 
            'title':            nlv['dQVdt_MBL_LH']['label'],
        },
        {
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['dQVdt_MBL_LH']}, 
            'title':            nlv['dQVdt_MBL_LH']['label'],
        },
        {
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['dTdt_MBL_SH']}, 
            'title':            nlv['dTdt_MBL_SH']['label'],
        },
        {
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['dTdt_MBL_SH']}, 
            'title':            nlv['dTdt_MBL_SH']['label'],
        },
        {
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['dRHdt_MBL_FLX']}, 
            'title':            nlv['dRHdt_MBL_FLX']['label'],
        },
        {
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['dRHdt_MBL_FLX']}, 
            'title':            nlv['dRHdt_MBL_FLX']['label'],
        },



        {
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['QVHDIV@alt=100']}, 
            'title':            nlv['QVHDIV']['label'],
        },
        {
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['QVHDIV@alt=100']}, 
            'title':            nlv['QVHDIV']['label'],
        },

        {
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['POTTHDIV@alt=100']}, 
            'title':            nlv['POTTHDIV']['label'],
        },
        {
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['POTTHDIV@alt=100']}, 
            'title':            nlv['POTTHDIV']['label'],
        },

        {
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['dRHdt@alt=100']}, 
            'title':            nlv['dRHdt']['label'],
        },
        {
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['dRHdt@alt=100']}, 
            'title':            nlv['dRHdt']['label'],
        },



        {
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['QVXDIV@alt=100']}, 
            'title':            nlv['QVXDIV']['label'],
        },
        {
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['QVXDIV@alt=100']}, 
            'title':            nlv['QVXDIV']['label'],
        },

        {
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['POTTXDIV@alt=100']}, 
            'title':            nlv['POTTXDIV']['label'],
        },
        {
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['POTTXDIV@alt=100']}, 
            'title':            nlv['POTTXDIV']['label'],
        },
        None,
        None,



        {
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['QVYDIV@alt=100']}, 
            'title':            nlv['QVYDIV']['label'],
        },
        {
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['QVYDIV@alt=100']}, 
            'title':            nlv['QVYDIV']['label'],
        },

        {
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['POTTYDIV@alt=100']}, 
            'title':            nlv['POTTYDIV']['label'],
        },
        {
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['POTTYDIV@alt=100']}, 
            'title':            nlv['POTTYDIV']['label'],
        },
        None,
        None,



        {
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['QVVDIV@alt=100']}, 
            'title':            nlv['QVVDIV']['label'],
        },
        {
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['QVVDIV@alt=100']}, 
            'title':            nlv['QVVDIV']['label'],
        },

        {
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['POTTVDIV@alt=100']}, 
            'title':            nlv['POTTVDIV']['label'],
        },
        {
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['POTTVDIV@alt=100']}, 
            'title':            nlv['POTTVDIV']['label'],
        },
        None,
        None,



        #{
        #    'mem_cfgs':         mem_dicts['ctrl'],
        #    'plot_dict':        {'l1':['QV@alt=100']}, 
        #    'title':            nlv['QV']['label'],
        #},
        #{
        #    'mem_cfgs':         mem_dicts['diff'],
        #    'plot_dict':        {'l1':['QV@alt=100']}, 
        #    'title':            nlv['QV']['label'],
        #},

        #{
        #    'mem_cfgs':         mem_dicts['ctrl'],
        #    'plot_dict':        {'l1':['T@alt=100']}, 
        #    'title':            nlv['T']['label'],
        #},
        #{
        #    'mem_cfgs':         mem_dicts['diff'],
        #    'plot_dict':        {'l1':['T@alt=100']}, 
        #    'title':            nlv['T']['label'],
        #},



        #{
        #    'mem_cfgs':         [ctrl],
        #    'plot_dict':        {'l1':['QVHDIV@alt=3000']}, 
        #    'title':            nlv['QVHDIV']['label'],
        #},
        #{
        #    'mem_cfgs':         [cosmo_change],
        #    'plot_dict':        {'l1':['QVHDIV@alt=3000']}, 
        #    'title':            nlv['QVHDIV']['label'],
        #},



    ],
}

##############################################################################


use_domain = dom_trades_full
line_along = 'lon'
#use_domain = dom_trades_NA
#line_along = 'lon'
#use_domain = dom_trades_merid
#line_along = 'lat'
run_cfgs['trades_vertical'] = {
    'fig': {
        'figsize':              (10, 8),
        'nrows':                3,
        'ncols':                2,
        'args_subplots_adjust': {
            'left':     0.07,
            'bottom':   0.08,
            'right':    0.90,
            'top':      0.95,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [0.35,0.35],
            'wspaces':  [0.45],
        },
        'kwargs_remove_axis_labels': {
            'remove_level':     1,
            #'xexcept':          {'0,0':2,'0,1':2,'1,0':2,'1,1':2,'1,2':2,'1,3':2,
            #                     '2,0':2,'2,1':2,'2,2':2,'2,3':2,'3,2':2,'3,3':2},
            #'yexcept':          {'1,2':0,'2,2':0,'4,2':0},
        },
        'label_cfgs': [
        ],
        'name_dict_append': {
            'dom': use_domain['key'],
        }
    },
    'glob_pan_cfg':   {
        'ana_number':       4,
        'agg_level':        TP.ALL_TIME,
        'plot_domain':      use_domain,
        'norm_inv':         1,
        'line_along':       line_along,
        'line_at':          None,
        'time_periods':     time_periods_ana,
        #'time_periods':     get_time_periods_for_month(2007, 8),
        'pan_cbar_pos':     'center right',
        'pan_cbar_pad':     -2,
        'i_recompute':      0,
    },
    'pan_cfgs':    [
        {
            'mem_cfgs':         [cosmo_change],
            'var_type':         'CLDF_CLDF', 
            'title':            nlv['CLDF']['label'],
        },
        None,

        {
            'mem_cfgs':         [cosmo_change],
            'var_type':         'POTT_CLDF', 
            'title':            nlv['POTT']['label'],
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_type':         'RH_CLDF', 
            'title':            nlv['RH']['label'],
        },

        {
            'mem_cfgs':         [cosmo_change],
            'var_type':         'BVF_CLDF', 
            'title':            nlv['BVF']['label'],
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_type':         'QV_CLDF', 
            'title':            nlv['QV']['label'],
        },
    ],
}

##############################################################################


run_cfgs['itcz_diabh'] = {
    'fig': {
        #'figsize':              (9, 9.5),
        'figsize':              (9, 7.5),
        #'nrows':                4,
        'nrows':                3,
        'ncols':                3,
        'args_subplots_adjust': {
            'left':     0.12,
            #'bottom':   0.13,
            'bottom':   0.17,
            'right':    0.98,
            'top':      0.92,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            #'hspaces':  [0.15,0.15,0.15],
            'hspaces':  [0.15,0.15],
            'wspaces':  [0.11,0.11],
        },
        'kwargs_remove_axis_labels': {
            'remove_level':     2,
        },
        'label_cfgs': [
            {'xrel':0.175,'yrel':0.96 , 'text':'CTRL | HIST'},
            {'xrel':0.47 ,'yrel':0.96 , 'text':'PGW | SCEN'},
            {'xrel':0.80 ,'yrel':0.96 , 'text':'change'},

            #{'xrel':0.01 ,'yrel':0.805, 'text':'ERA5',      'rotation':90},
            #{'xrel':0.01 ,'yrel':0.585, 'text':'COSMO',     'rotation':90},
            #{'xrel':0.01 ,'yrel':0.365, 'text':'CMIP6-EM',  'rotation':90},
            #{'xrel':0.01 ,'yrel':0.17 , 'text':'MPI-ESM',   'rotation':90},

            {'xrel':0.01 ,'yrel':0.775, 'text':'ERA5',      'rotation':90},
            {'xrel':0.01 ,'yrel':0.49 , 'text':'COSMO',     'rotation':90},
            {'xrel':0.01 ,'yrel':0.21 , 'text':'CMIP6-EM',  'rotation':90},
        ],
    },
    'glob_pan_cfg':   {
        'ana_number':       4,
        'agg_level':        TP.ALL_TIME,
        'plot_domain':      dom_SA_ana_merid_cs,
        'norm_inv':         0,
        'line_along':       'lat',
        'line_at':          None,
        'time_periods':     time_periods_ana,
        'alt_lims':         (0,18000),
        'i_plot_cbar':      0,
        'i_recompute':      0,
        'var_type':         'POTTDIV_CLDF',
        'title':            '',
    },
    'pan_cfgs':    [
        {
            'mem_cfgs':         ['ERA5'],
        },
        None,
        None,

        {
            'mem_cfgs':         [ctrl],
        },
        {
            'mem_cfgs':         [pgw],
        },
        {
            'mem_cfgs':         [cosmo_change],
        },

        {
            'mem_cfgs':         [cmip6_hist],
            'time_periods':     time_periods_cmip6_hist,
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cmip6_scen],
            'time_periods':     time_periods_cmip6_scen,
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cmip6_change],
            'i_plot_cbar':      1,
        },

        #{
        #    'mem_cfgs':         [mpi_hist],
        #    'time_periods':     time_periods_cmip6_hist,
        #    'i_plot_cbar':      1,
        #},
        #{
        #    'mem_cfgs':         [mpi_scen],
        #    'time_periods':     time_periods_cmip6_scen,
        #    'i_plot_cbar':      1,
        #},
        #{
        #    'mem_cfgs':         [mpi_change],
        #    'i_plot_cbar':      1,
        #},
    ],
}

##############################################################################

run_cfgs['itcz_diabh_FMA'] = copy.deepcopy(run_cfgs['itcz_diabh'])
run_cfgs['itcz_diabh_FMA']['glob_pan_cfg']['time_periods'] = time_periods_ana_FMA
run_cfgs['itcz_diabh_FMA']['pan_cfgs'][6]['time_periods'] = time_periods_cmip6_hist_FMA
run_cfgs['itcz_diabh_FMA']['pan_cfgs'][7]['time_periods'] = time_periods_cmip6_scen_FMA
run_cfgs['itcz_diabh_FMA']['pan_cfgs'][8]['mem_cfgs'] = [cmip6_change_FMA]

##############################################################################

run_cfgs['itcz_diabh_JAS'] = copy.deepcopy(run_cfgs['itcz_diabh'])
run_cfgs['itcz_diabh_JAS']['glob_pan_cfg']['time_periods'] = time_periods_ana_JAS
run_cfgs['itcz_diabh_JAS']['pan_cfgs'][6]['time_periods'] = time_periods_cmip6_hist_JAS
run_cfgs['itcz_diabh_JAS']['pan_cfgs'][7]['time_periods'] = time_periods_cmip6_scen_JAS
run_cfgs['itcz_diabh_JAS']['pan_cfgs'][8]['mem_cfgs'] = [cmip6_change_JAS]

##############################################################################

run_cfgs['itcz_w'] = copy.deepcopy(run_cfgs['itcz_diabh'])
run_cfgs['itcz_w']['glob_pan_cfg']['var_type'] = 'WFLX_CLDF'


##############################################################################

run_cfgs['itcz_w_FMA'] = copy.deepcopy(run_cfgs['itcz_w'])
run_cfgs['itcz_w_FMA']['glob_pan_cfg']['time_periods'] = time_periods_ana_FMA
run_cfgs['itcz_w_FMA']['pan_cfgs'][6]['time_periods'] = time_periods_cmip6_hist_FMA
run_cfgs['itcz_w_FMA']['pan_cfgs'][7]['time_periods'] = time_periods_cmip6_scen_FMA
run_cfgs['itcz_w_FMA']['pan_cfgs'][8]['mem_cfgs'] = [cmip6_change_FMA]

##############################################################################

run_cfgs['itcz_w_JAS'] = copy.deepcopy(run_cfgs['itcz_w'])
run_cfgs['itcz_w_JAS']['glob_pan_cfg']['time_periods'] = time_periods_ana_JAS
run_cfgs['itcz_w_JAS']['pan_cfgs'][6]['time_periods'] = time_periods_cmip6_hist_JAS
run_cfgs['itcz_w_JAS']['pan_cfgs'][7]['time_periods'] = time_periods_cmip6_scen_JAS
run_cfgs['itcz_w_JAS']['pan_cfgs'][8]['mem_cfgs'] = [cmip6_change_JAS]

##############################################################################


run_cfgs['suppl_cosmo_diabh'] = {
    'fig': {
        'figsize':              (9, 5.5),
        'nrows':                2,
        'ncols':                3,
        'args_subplots_adjust': {
            'left':     0.12,
            'bottom':   0.23,
            'right':    0.98,
            'top':      0.92,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [0.15],
            'wspaces':  [0.11,0.11],
        },
        'kwargs_remove_axis_labels': {
            'remove_level':     2,
        },
        'label_cfgs': [
            {'xrel':0.235,'yrel':0.95 , 'text':'CTRL'},
            {'xrel':0.515,'yrel':0.95 , 'text':'PGW'},
            {'xrel':0.775,'yrel':0.95 , 'text':'PGW$-$CTRL'},

            {'xrel':0.01 ,'yrel':0.73 , 'text':nlv['POTTDIV']['label'],     'rotation':90},
            {'xrel':0.01 ,'yrel':0.30 , 'text':nlv['NCOLIPOTTDIV']['label'],'rotation':90},
        ],
    },
    'glob_pan_cfg':   {
        'ana_number':       4,
        'agg_level':        TP.ALL_TIME,
        'plot_domain':      dom_SA_ana_merid_cs,
        'norm_inv':         0,
        'line_along':       'lat',
        'line_at':          None,
        'time_periods':     time_periods_ana,
        'alt_lims':         (0,18000),
        'i_plot_cbar':      0,
        'i_recompute':      0,
        'title':            '',
        'cbar_label_mode':  'var_units'
    },
    'pan_cfgs':    [
        {
            'mem_cfgs':         [ctrl],
            'var_type':         'POTTDIV_CLDF',
        },
        {
            'mem_cfgs':         [pgw],
            'var_type':         'POTTDIV_CLDF',
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_type':         'POTTDIV_CLDF',
        },

        {
            'mem_cfgs':         [ctrl],
            'var_type':         'NCOLIPOTTDIV_CLDF',
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [pgw],
            'var_type':         'NCOLIPOTTDIV_CLDF',
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_type':         'NCOLIPOTTDIV_CLDF',
            'i_plot_cbar':      1,
        },
    ],
}


##############################################################################


domain = dom_SA_ana_merid_cs
domain = dom_SA_ana_merid_cs_2

seas_type = '2'
tp_winter = time_periods_ana_JFM
tp_spring = time_periods_ana_AMJ
tp_summer = time_periods_ana_JAS
tp_autumn = time_periods_ana_OND
cmip6_hist_winter = cmip6_hist_JFM
cmip6_hist_spring = cmip6_hist_AMJ
cmip6_hist_summer = cmip6_hist_JAS 
cmip6_hist_autumn = cmip6_hist_OND
cmip6_change_winter = cmip6_change_JFM
cmip6_change_spring = cmip6_change_AMJ
cmip6_change_summer = cmip6_change_JAS 
cmip6_change_autumn = cmip6_change_OND
mpi_hist_winter = mpi_hist_JFM
mpi_hist_spring = mpi_hist_AMJ
mpi_hist_summer = mpi_hist_JAS 
mpi_hist_autumn = mpi_hist_OND
mpi_change_winter = mpi_change_JFM
mpi_change_spring = mpi_change_AMJ
mpi_change_summer = mpi_change_JAS 
mpi_change_autumn = mpi_change_OND
tp_winter_name = 'JFM'
tp_spring_name = 'AMJ'
tp_summer_name = 'JAS'
tp_autumn_name = 'OND'

var_type = 'CLDF_CLDF_PP'
var_type = 'RH_CLDF_TSURF'
#var_type = 'WFLX_CLDF_TSURF'
#var_type = 'VFLX_CLDF_TSURF'
#var_type = 'T_CLDF'
#var_type = 'BVF_CLDF'

run_cfgs['cs1'] = {
    'fig': {
        'figsize':              (15, 17.5),
        'nrows':                7,
        'ncols':                5,
        'args_subplots_adjust': {
            'left':     0.08,
            'bottom':   0.08,
            'right':    0.96,
            'top':      0.96,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [0.15,0.15,0.15,0.80,0.15,0.15],
            'wspaces':  [0.20,0.10,0.10,0.10],
        },
        'kwargs_remove_axis_labels': {
            'remove_level':     2,
            'xexcept':          {'3,0':0,'3,1':0,'3,2':0,'3,3':0,'3,4':0},
        },
        'label_cfgs': [
            {'xrel':0.15 ,'yrel':0.98 , 'text':'full year'},
            {'xrel':0.35 ,'yrel':0.98 , 'text':tp_winter_name},
            {'xrel':0.55 ,'yrel':0.98 , 'text':tp_spring_name},
            {'xrel':0.70 ,'yrel':0.98 , 'text':tp_summer_name},
            {'xrel':0.90 ,'yrel':0.98 , 'text':tp_autumn_name},

            {'xrel':0.01 ,'yrel':0.90 , 'text':'ERA5',      'rotation':90},
            {'xrel':0.01 ,'yrel':0.77 , 'text':'COSMO',     'rotation':90},
            {'xrel':0.01 ,'yrel':0.64 , 'text':'CMIP6-EM',  'rotation':90},
            {'xrel':0.01 ,'yrel':0.53 , 'text':'MPI-ESM',   'rotation':90},

            {'xrel':0.01 ,'yrel':0.34 , 'text':'COSMO',     'rotation':90},
            {'xrel':0.01 ,'yrel':0.22 , 'text':'CMIP6-EM',  'rotation':90},
            {'xrel':0.01 ,'yrel':0.10 , 'text':'MPI-ESM',   'rotation':90},
        ],
        'name_dict_append': {
            'SEAS':     seas_type,
            'var':      var_type,
            'dom':      domain['key'],
        }
    },
    'glob_pan_cfg':   {
        'ana_number':       4,
        'agg_level':        TP.ALL_TIME,
        'plot_domain':      domain,
        'norm_inv':         0,
        'line_along':       'lat',
        'line_at':          None,
        #'time_periods':     time_periods_ana,
        'alt_lims':         (0,18000),
        'i_plot_cbar':      0,
        'i_recompute':      0,
        'title':            '',
        'time_periods':     time_periods_ana,
        'var_type':         var_type,
    },
    'pan_cfgs':    [
        {
            'mem_cfgs':         ['ERA5'],
        },
        {
            'mem_cfgs':         ['ERA5'],
            'time_periods':     tp_winter,
        },
        {
            'mem_cfgs':         ['ERA5'],
            'time_periods':     tp_spring,
        },
        {
            'mem_cfgs':         ['ERA5'],
            'time_periods':     tp_summer,
        },
        {
            'mem_cfgs':         ['ERA5'],
            'time_periods':     tp_autumn,
        },



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
            'mem_cfgs':         [cmip6_hist],
            'time_periods':     time_periods_cmip6_hist,
        },
        {
            'mem_cfgs':         [cmip6_hist_winter],
        },
        {
            'mem_cfgs':         [cmip6_hist_spring],
        },
        {
            'mem_cfgs':         [cmip6_hist_summer],
        },
        {
            'mem_cfgs':         [cmip6_hist_autumn],
        },


        {
            'mem_cfgs':         [mpi_hist],
            'time_periods':     time_periods_cmip6_hist,
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [mpi_hist_winter],
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [mpi_hist_spring],
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [mpi_hist_summer],
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [mpi_hist_autumn],
            'i_plot_cbar':      1,
        },





        {
            'mem_cfgs':         [cosmo_change],
        },
        {
            'mem_cfgs':         [cosmo_change],
            'time_periods':     tp_winter,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'time_periods':     tp_spring,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'time_periods':     tp_summer,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'time_periods':     tp_autumn,
        },


        {
            'mem_cfgs':         [cmip6_change],
        },
        {
            'mem_cfgs':         [cmip6_change_winter],
        },
        {
            'mem_cfgs':         [cmip6_change_spring],
        },
        {
            'mem_cfgs':         [cmip6_change_summer],
        },
        {
            'mem_cfgs':         [cmip6_change_autumn],
        },


        {
            'mem_cfgs':         [mpi_change],
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [mpi_change_winter],
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [mpi_change_spring],
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [mpi_change_summer],
            'i_plot_cbar':      1,
        },
        {
            'mem_cfgs':         [mpi_change_autumn],
            'i_plot_cbar':      1,
        },
    ],
}






domain = dom_SA_ana_merid_cs
vertical_line = None
domain = dom_SA_ana_merid_cs_2
vertical_line = 5.5
run_cfgs['itcz_final'] = {
    'fig': {
        'figsize':              (12, 16),
        'nrows':                6,
        'ncols':                4,
        'args_subplots_adjust': {
            'left':     0.09,
            'bottom':   0.08,
            'right':    0.94,
            'top':      0.96,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [0.15,0.45,0.95,0.15,0.45],
            'wspaces':  [0.30,0.15,0.15],
        },
        'kwargs_remove_axis_labels': {
            'remove_level':     2,
            'xexcept':          {
                '2,0':0,'2,1':0,'2,2':0,'2,3':0},
            'yexcept':          {
                '0,0':0,#'0,3':0,
                '1,0':0,#'1,3':0,
                '2,0':0,#'2,3':{'main':2,'twinx':0},
                '3,0':0,#'3,3':0,
                '4,0':0,#'6,3':0,
                '5,0':0,#'5,3':{'main':2,'twinx':0},
            },
        },
        'label_cfgs': [
            {'xrel':0.11 ,'yrel':0.98 , 'text':nlv['CLDF']['label'],    'fontsize':20},
            {'xrel':0.41 ,'yrel':0.98 , 'text':nlv['RH']['label'],      'fontsize':20},
            {'xrel':0.62 ,'yrel':0.98 , 'text':nlv['WFLX']['label'],    'fontsize':20},
            {'xrel':0.84 ,'yrel':0.98 , 'text':nlv['VFLX']['label'],    'fontsize':20},

            {'xrel':0.01 ,'yrel':0.89 , 'text':'CTRL',          'rotation':90,  'fontsize':20},
            {'xrel':0.01 ,'yrel':0.767, 'text':'PGW',           'rotation':90,  'fontsize':20},
            {'xrel':0.01 ,'yrel':0.58 , 'text':'PGW$-$CTRL',    'rotation':90,  'fontsize':20},
            {'xrel':0.01 ,'yrel':0.40 , 'text':'HIST',          'rotation':90,  'fontsize':20},
            {'xrel':0.01 ,'yrel':0.27 , 'text':'SCEN',          'rotation':90,  'fontsize':20},
            {'xrel':0.01 ,'yrel':0.085, 'text':'SCEN$-$HIST',   'rotation':90,  'fontsize':20},

            #{'xrel':0.01 ,'yrel':0.94 , 'text':'COSMO',     'fontsize':20},
            #{'xrel':0.01 ,'yrel':0.49 , 'text':'CMIP6-EM',  'fontsize':20},
        ],
        'name_dict_append': {
            'dom':      domain['key'],
        }
    },
    'glob_pan_cfg':   {
        'ana_number':       4,
        'agg_level':        TP.ALL_TIME,
        'plot_domain':      domain,
        'norm_inv':         0,
        'line_along':       'lat',
        'line_at':          None,
        #'time_periods':     time_periods_ana,
        'alt_lims':         (0,18000),
        'i_plot_cbar':      1,
        'i_recompute':      0,
        'title':            '',
        'time_periods':     time_periods_ana,
        'pan_cbar_pos':     'lower center',
        'pan_cbar_pad':     -5.0,
        'vertical_line':    vertical_line,
    },
    'pan_cfgs':    [
        {
            'mem_cfgs':         [ctrl],
            'var_type':         'CLDF_CLDF_PP',
            'i_plot_cbar':      0,
        },
        {
            'mem_cfgs':         [ctrl],
            'var_type':         'RH_CLDF',
            'i_plot_cbar':      0,
        },
        {
            'mem_cfgs':         [ctrl],
            'var_type':         'WFLX_CLDF_TSURF',
            'i_plot_cbar':      0,
        },
        {
            'mem_cfgs':         [ctrl],
            'var_type':         'VFLX_CLDF_TSURF',
            'i_plot_cbar':      0,
        },


        {
            'mem_cfgs':         [pgw],
            'var_type':         'CLDF_CLDF_PP',
            'pan_cbar_pad':     -2.0,
            'cbar_label_mode':  'neither',
        },
        {
            'mem_cfgs':         [pgw],
            'var_type':         'RH_CLDF',
            'pan_cbar_pad':     -2.0,
            'cbar_label_mode':  'neither',
        },
        {
            'mem_cfgs':         [pgw],
            'var_type':         'WFLX_CLDF_TSURF',
            'pan_cbar_pad':     -2.0,
            'cbar_label_mode':  'neither',
        },
        {
            'mem_cfgs':         [pgw],
            'var_type':         'VFLX_CLDF_TSURF',
            'pan_cbar_pad':     -2.0,
            'cbar_label_mode':  'neither',
        },


        {
            'mem_cfgs':         [cosmo_change],
            'var_type':         'CLDF_CLDF_PP',
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_type':         'RH_CLDF',
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_type':         'WFLX_CLDF_TSURF',
        },
        {
            'mem_cfgs':         [cosmo_change],
            'var_type':         'VFLX_CLDF_TSURF',
        },


        {
            'mem_cfgs':         [cmip6_hist],
            'time_periods':     time_periods_cmip6_hist,
            'var_type':         'CLDF_CLDF_PP',
            'i_plot_cbar':      0,
        },
        {
            'mem_cfgs':         [cmip6_hist],
            'time_periods':     time_periods_cmip6_hist,
            'var_type':         'RH_CLDF',
            'i_plot_cbar':      0,
        },
        {
            'mem_cfgs':         [cmip6_hist],
            'time_periods':     time_periods_cmip6_hist,
            'var_type':         'WFLX_CLDF_TSURF',
            'i_plot_cbar':      0,
        },
        {
            'mem_cfgs':         [cmip6_hist],
            'time_periods':     time_periods_cmip6_hist,
            'var_type':         'VFLX_CLDF_TSURF',
            'i_plot_cbar':      0,
        },


        {
            'mem_cfgs':         [cmip6_scen],
            'time_periods':     time_periods_cmip6_scen,
            'var_type':         'CLDF_CLDF_PP',
            'pan_cbar_pad':     -2.0,
            'cbar_label_mode':  'neither',
        },
        {
            'mem_cfgs':         [cmip6_scen],
            'time_periods':     time_periods_cmip6_scen,
            'var_type':         'RH_CLDF',
            'pan_cbar_pad':     -2.0,
            'cbar_label_mode':  'neither',
        },
        {
            'mem_cfgs':         [cmip6_scen],
            'time_periods':     time_periods_cmip6_scen,
            'var_type':         'WFLX_CLDF_TSURF',
            'pan_cbar_pad':     -2.0,
            'cbar_label_mode':  'neither',
        },
        {
            'mem_cfgs':         [cmip6_scen],
            'time_periods':     time_periods_cmip6_scen,
            'var_type':         'VFLX_CLDF_TSURF',
            'pan_cbar_pad':     -2.0,
            'cbar_label_mode':  'neither',
        },


        {
            'mem_cfgs':         [cmip6_change],
            'var_type':         'CLDF_CLDF_PP',
        },
        {
            'mem_cfgs':         [cmip6_change],
            'var_type':         'RH_CLDF',
        },
        {
            'mem_cfgs':         [cmip6_change],
            'var_type':         'WFLX_CLDF_TSURF',
        },
        {
            'mem_cfgs':         [cmip6_change],
            'var_type':         'VFLX_CLDF_TSURF',
        },
    ],
}



domain = dom_SA_ana_merid_cs
vertical_line = None
#domain = dom_SA_ana_merid_cs_2
#vertical_line = 5.5

var_type ='CLDF_CLDF_PP'
var_type ='RH_CLDF'
var_type ='WFLX_CLDF_TSURF'
var_type ='VFLX_CLDF_TSURF'
run_cfgs['itcz_final_seas'] = {
    'fig': {
        'figsize':              (15, 15),
        'nrows':                6,
        'ncols':                5,
        'args_subplots_adjust': {
            'left':     0.09,
            'bottom':   0.04,
            'right':    0.90,
            'top':      0.96,
            'wspace':   0.00,
            'hspace':   0.00,
        },
        'grid_spec': {
            'hspaces':  [0.15,0.15,0.15,0.15,0.15],
            'wspaces':  [0.20,0.10,0.10,0.10],
        },
        'kwargs_remove_axis_labels': {
            'remove_level':     2,
            #'xexcept':          {
            #    '2,0':0,'2,1':0,'2,2':0,'2,3':0},
            #'yexcept':          {
            #    '0,0':0,#'0,3':0,
            #    '1,0':0,#'1,3':0,
            #    '2,0':0,#'2,3':{'main':2,'twinx':0},
            #    '3,0':0,#'3,3':0,
            #    '4,0':0,#'6,3':0,
            #    '5,0':0,#'5,3':{'main':2,'twinx':0},
            #},
        },
        'label_cfgs': [
            {'xrel':0.135,'yrel':0.98 , 'text':'annual',                    'fontsize':20},
            {'xrel':0.33 ,'yrel':0.98 , 'text':'JFM',                       'fontsize':20},
            {'xrel':0.49 ,'yrel':0.98 , 'text':'AMJ',                       'fontsize':20},
            {'xrel':0.652,'yrel':0.98 , 'text':'JAS',                       'fontsize':20},
            {'xrel':0.805,'yrel':0.98 , 'text':'OND',                       'fontsize':20},

            {'xrel':0.01 ,'yrel':0.875, 'text':'CTRL',                      'rotation':90,  'fontsize':20},
            {'xrel':0.01 ,'yrel':0.69 , 'text':'PGW$-$CTRL',                'rotation':90,  'fontsize':20},
            {'xrel':0.01 ,'yrel':0.545, 'text':'MPI-ESM\n   HIST',          'rotation':90,  'fontsize':20},
            {'xrel':0.01 ,'yrel':0.375, 'text':'  MPI-ESM\nSCEN$-$HIST',    'rotation':90,  'fontsize':20},
            {'xrel':0.01 ,'yrel':0.225, 'text':'CMIP6-EM\n    HIST',        'rotation':90,  'fontsize':20},
            {'xrel':0.01 ,'yrel':0.06 , 'text':' CMIP6-EM\nSCEN$-$HIST',    'rotation':90,  'fontsize':20},

            #{'xrel':0.01 ,'yrel':0.94 , 'text':'COSMO',     'fontsize':20},
            #{'xrel':0.01 ,'yrel':0.49 , 'text':'CMIP6-EM',  'fontsize':20},
        ],
        'name_dict_append': {
            'dom':      domain['key'],
            'var':      var_type,
        }
    },
    'glob_pan_cfg':   {
        'ana_number':       4,
        'agg_level':        TP.ALL_TIME,
        'plot_domain':      domain,
        'norm_inv':         0,
        'line_along':       'lat',
        'line_at':          None,
        'var_type':         var_type,
        'alt_lims':         (0,18000),
        'i_plot_cbar':      0,
        'i_recompute':      0,
        'title':            '',
        'time_periods':     time_periods_ana,
        'pan_cbar_pos':     'center right',
        'pan_cbar_pad':     -6.0,
        'vertical_line':    vertical_line,
    },
    'pan_cfgs':    [
        {
            'mem_cfgs':         [ctrl],
        },
        {
            'mem_cfgs':         [ctrl],
            'time_periods':     time_periods_ana_JFM,
        },
        {
            'mem_cfgs':         [ctrl],
            'time_periods':     time_periods_ana_AMJ,
        },
        {
            'mem_cfgs':         [ctrl],
            'time_periods':     time_periods_ana_JAS,
        },
        {
            'mem_cfgs':         [ctrl],
            'time_periods':     time_periods_ana_OND,
            'i_plot_cbar':      1,
        },


        {
            'mem_cfgs':         [cosmo_change],
        },
        {
            'mem_cfgs':         [cosmo_change],
            'time_periods':     time_periods_ana_JFM,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'time_periods':     time_periods_ana_AMJ,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'time_periods':     time_periods_ana_JAS,
        },
        {
            'mem_cfgs':         [cosmo_change],
            'time_periods':     time_periods_ana_OND,
            'i_plot_cbar':      1,
        },


        {
            'mem_cfgs':         [mpi_hist],
            'time_periods':     time_periods_cmip6_hist,
        },
        {
            'mem_cfgs':         [mpi_hist_JFM],
        },
        {
            'mem_cfgs':         [mpi_hist_AMJ],
        },
        {
            'mem_cfgs':         [mpi_hist_JAS],
        },
        {
            'mem_cfgs':         [mpi_hist_OND],
            'i_plot_cbar':      1,
        },


        {
            'mem_cfgs':         [mpi_change],
        },
        {
            'mem_cfgs':         [mpi_change_JFM],
        },
        {
            'mem_cfgs':         [mpi_change_AMJ],
        },
        {
            'mem_cfgs':         [mpi_change_JAS],
        },
        {
            'mem_cfgs':         [mpi_change_OND],
            'i_plot_cbar':      1,
        },


        {
            'mem_cfgs':         [cmip6_hist],
            'time_periods':     time_periods_cmip6_hist,
        },
        {
            'mem_cfgs':         [cmip6_hist_JFM],
        },
        {
            'mem_cfgs':         [cmip6_hist_AMJ],
        },
        {
            'mem_cfgs':         [cmip6_hist_JAS],
        },
        {
            'mem_cfgs':         [cmip6_hist_OND],
            'i_plot_cbar':      1,
        },


        {
            'mem_cfgs':         [cmip6_change],
        },
        {
            'mem_cfgs':         [cmip6_change_JFM],
        },
        {
            'mem_cfgs':         [cmip6_change_AMJ],
        },
        {
            'mem_cfgs':         [cmip6_change_JAS],
        },
        {
            'mem_cfgs':         [cmip6_change_OND],
            'i_plot_cbar':      1,
        },
    ],
}





use_cfg = 'spatial_rad'
use_cfg = 'spatial_cs_cosmo_mpi'
#use_cfg = 'spatial_cre_cosmo_mpi'
#use_cfg = 'trades_env'
#use_cfg = 'trades_mbl'
#use_cfg = 'trades_vertical'
#use_cfg = 'itcz_final'
#use_cfg = 'itcz_final_seas'

#use_cfg = 'spatial_rad_seas'
#use_cfg = 'spatial_rad_seas_cmip6'
#use_cfg = 'spatial_LW'
#use_cfg = 'spatial_LW_COSMO'
#use_cfg = 'spatial_anncycle'
#use_cfg = 'trades_qv'
#use_cfg = 'itcz_diabh'
#use_cfg = 'itcz_diabh_FMA'
#use_cfg = 'itcz_diabh_JAS'
#use_cfg = 'itcz_w'
#use_cfg = 'itcz_w_FMA'
#use_cfg = 'itcz_w_JAS'
#use_cfg = 'cs1'
#use_cfg = 'test_qv'

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
    'sub_dir':              'heim_2023',
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
