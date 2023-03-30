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
from package.nl_models import models_cmip6, models_cmip6_cldf
from nl_plot_org_ana import nlp
from package.nl_variables import nlv, get_plt_units
###############################################################################
change_type = 'rel'
change_type = 'abs'

def fmt_var_title(var_name):
    return(
        '{} [{}]'.format(
            nlv[var_name]['label'], 
            get_plt_units(var_name)
        )
    )

args_subplots_adjust = {
    '2x3': {
        'left':0.03,
        'bottom':0.08,
        'right':0.92,
        'top':0.95,
        'wspace':0.55,
        'hspace':0.40,
    },
    '3x4': {
        'left':0.03,
        'bottom':0.08,
        'right':0.92,
        'top':0.95,
        'wspace':0.55,
        'hspace':0.40,
    },
    '3x2': {
        'left':0.06,
        'bottom':0.05,
        'right':0.92,
        'top':0.97,
        'wspace':0.60,
        'hspace':0.40,
    },
    '4x3': {
        'left':0.06,
        'bottom':0.05,
        'right':0.92,
        'top':0.97,
        'wspace':0.60,
        'hspace':0.40,
    },
    '4x4': {
        'left':0.06,
        'bottom':0.05,
        'right':0.92,
        'top':0.97,
        'wspace':0.60,
        'hspace':0.40,
    },
    '5x4': {
        'left':0.06,
        'bottom':0.05,
        'right':0.92,
        'top':0.97,
        'wspace':0.80,
        'hspace':0.40,
    },
}


rel_oper = 'rel0.001'

models_cmip6 = models_cmip6_cldf
#models_cmip6 = models_cmip6_cldf[0:10]
#models_cmip6 = models_cmip6_cldf[2:]
mem_keys_cmip6_hist = ['{}_historical'.format(model) for model in models_cmip6]
mem_keys_cmip6_scen = ['{}_ssp585'.format(model) for model in models_cmip6]
mem_keys_cmip6_abs_change = []
for model in models_cmip6:
    mem_keys_cmip6_abs_change.append(
        {
            'mem_oper':     'diff',
            'mem_keys':     [
                {
                    'mem_key':      '{}_ssp585'.format(model),
                    'time_periods': time_periods_cmip6_scen,
                },
                {
                    'mem_key':      '{}_historical'.format(model), 
                    'time_periods': time_periods_cmip6_hist,
                },
            ],
        }
    )
cmip6_hist = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_hist,
    'time_periods': time_periods_cmip6_hist,
    'label':        'CMIP6 HIST',
}
cmip6_scen = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_scen,
    'time_periods': time_periods_cmip6_scen,
    'label':        'CMIP6 SCEN',
}
cmip6_abs_change = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_abs_change,
    'label':        'SCEN$-$HIST',
}
cmip6_rel_change = {
    'mem_oper':     rel_oper,
    'mem_keys':     [cmip6_scen,cmip6_hist],
    'label':        'SCEN/HIST$-$1',
}
cosmo_abs_change = {
    'mem_oper':     'diff',
    'mem_keys':     ['COSMO_3.3_pgw', 'COSMO_3.3_ctrl'],
    'label':        'PGW$-$CTRL',
}
cosmo_rel_change = {
    'mem_oper':     rel_oper,
    'mem_keys':     ['COSMO_3.3_pgw', 'COSMO_3.3_ctrl'],
    'label':        'PGW$-$CTRL',
}
mpi_hist = {
    'mem_key':      'MPI-ESM1-2-HR_historical', 
    'time_periods': time_periods_cmip6_hist,
}
mpi_scen = {
    'mem_key':      'MPI-ESM1-2-HR_ssp585', 
    'time_periods': time_periods_cmip6_scen,
}
mpi_abs_change = {
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


if change_type == 'abs':
    cosmo_change = cosmo_abs_change
elif change_type == 'rel':
    cosmo_change = cosmo_rel_change

run_cfgs = {
    'itcz_overview':  {
        'panel_cfgs':    [
            {
                'i_recompute':  1, 
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'plot_dict':    {
                    'l1':['IWPHCONV'],
                    'r1':['SWNDTOA','LWDTOA','RADNDTOA'],
                    'r2':['CLDF@alt=10000:15000'],
                },
                'i_plot_legend':1, 
                'title':        'CTRL & PGW',
            },
            {
                'i_recompute':  1, 
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'plot_dict':    {
                    #'l1':['QVHDIV3@alt=0:3000','QVVDIV3@alt=0:3000'],
                    'l1':['PP'],
                    'r1':['SLHFLX','WVPHCONV'],
                },
                'i_plot_legend':1, 
                'title':        'CTRL & PGW',
            },
            {
                'i_recompute':  1, 
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'plot_dict':    {
                    'l1':['PP'],
                    #'r1':['QVWFLX@alt=8000','QVWFLX@alt=5000'],
                    #'r2':['T2M'],
                    'r1':['QVVFLX@alt=14000'],
                    'r2':['QV@alt=14000'],
                    #'r2':['QVVFLX@alt=5000'],
                },
                'i_plot_legend':1, 
                'title':        'CTRL & PGW',
            },



            {
                'i_recompute':  1, 
                'mem_cfgs':     [cmip6_hist, cmip6_scen],
                'plot_dict':    {
                    'r1':['SWNDTOA','LWDTOA','RADNDTOA'],
                    'r2':['CLDF@alt=10000:15000'],
                },
                'title':        'HIST & SCEN',
            },
            {
                'i_recompute':  1, 
                'mem_cfgs':     [cmip6_hist, cmip6_scen],
                'plot_dict':    {
                    #'l1':['QVHDIV3@alt=0:3000','QVVDIV3@alt=0:3000'],
                    'l1':['PP'],
                    'r1':['SLHFLX','WVPHCONV'],
                },
                'i_plot_legend':1, 
                'title':        'HIST & SCEN',
            },
            {
                'i_recompute':  1, 
                'mem_cfgs':     [cmip6_hist, cmip6_scen],
                'plot_dict':    {
                    'l1':['PP'],
                    'r1':['QVWFLX@alt=8000','QVWFLX@alt=5000'],
                    #'r2':['T2M'],
                },
                'i_plot_legend':1, 
                'title':        'HIST & SCEN',
            },




            {
                'mem_cfgs':     [cosmo_change],
                'plot_dict':    {
                    'l1':['IWPHCONV'],
                    'r1':['SWNDTOA','LWDTOA','RADNDTOA'],
                    'r2':['CLDF@alt=10000:15000'],
                },
            },
            {
                'mem_cfgs':     [cosmo_change],
                'plot_dict':    {
                    #'l1':['QVHDIV3@alt=0:3000','QVVDIV3@alt=0:3000'],
                    'l1':['PP'],
                    'r1':['SLHFLX','WVPHCONV'],
                },
            },
            {
                'mem_cfgs':     [cosmo_change],
                'plot_dict':    {
                    'l1':['PP'],
                    #'r1':['QVWFLX@alt=8000','QVWFLX@alt=5000'],
                    #'r2':['T2M'],
                    'r1':['QVVFLX@alt=14000'],
                    'r2':['QV@alt=14000'],
                    #'r2':['QVVFLX@alt=5000'],

                },
            },




            {
                'mem_cfgs':     [cmip6_abs_change],
                'plot_dict':    {
                    'r1':['SWNDTOA','LWDTOA','RADNDTOA'],
                    'r2':['CLDF@alt=10000:15000'],
                },
            },
            {
                'mem_cfgs':     [cmip6_abs_change],
                'plot_dict':    {
                    #'l1':['QVHDIV3@alt=0:3000','QVVDIV3@alt=0:3000'],
                    'l1':['PP'],
                    'r1':['SLHFLX','WVPHCONV'],
                },
            },
            {
                'mem_cfgs':     [cmip6_abs_change],
                'plot_dict':    {
                    'l1':['PP'],
                    'r1':['QVWFLX@alt=8000','QVWFLX@alt=5000'],
                    #'r2':['T2M'],
                },
            },
        ],
        'figsize':          (18, 11),
        'nrows':            4,
        'ncols':            3,
        'adjust_key':       '4x3',
        'line_along':       'lat',
        'plot_domain':      dom_SA_ana_merid_cs,
    },


    'trades_overview':  {
        'panel_cfgs':    [
            {
                'i_recompute':  1, 
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'plot_dict':    {
                    'l1':['SWNDTOA','LWDTOA','RADNDTOA'],
                },
                'i_plot_legend':1, 
                'title':        'CTRL & PGW',
            },
            {
                'i_recompute':  1, 
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'plot_dict':    {
                    'l1':['T2M','T@alt=3000'],
                    'r1':['LTS'],
                },
                'i_plot_legend':1, 
                'title':        'CTRL & PGW',
            },
            {
                'i_recompute':  1, 
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'plot_dict':    {
                    'l1':['QV@alt=300','QV@alt=3000'],
                    'r1':['SLHFLX'],
                },
                'i_plot_legend':1, 
                'title':        'CTRL & PGW',
            },



            {
                'i_recompute':  1, 
                'mem_cfgs':     [cmip6_hist, cmip6_scen],
                'plot_dict':    {
                    'l1':['SWNDTOA','LWDTOA','RADNDTOA'],
                },
                'title':        'HIST & SCEN',
            },
            {
                'i_recompute':  1, 
                'mem_cfgs':     [cmip6_hist, cmip6_scen],
                'plot_dict':    {
                    'l1':['T2M','T@alt=3000'],
                    'r1':['LTS'],
                },
                'i_plot_legend':1, 
                'title':        'HIST & SCEN',
            },
            {
                'i_recompute':  1, 
                'mem_cfgs':     [cmip6_hist, cmip6_scen],
                'plot_dict':    {
                    'l1':['QV@alt=300','QV@alt=3000'],
                    'r1':['SLHFLX'],
                },
                'i_plot_legend':1, 
                'title':        'HIST & SCEN',
            },




            {
                'mem_cfgs':     [cosmo_change],
                'plot_dict':    {
                    'l1':['SWNDTOA','LWDTOA','RADNDTOA'],
                },
            },
            {
                'mem_cfgs':     [cosmo_change],
                'plot_dict':    {
                    'l1':['T2M','T@alt=3000'],
                    'r1':['LTS'],
                },
            },
            {
                'mem_cfgs':     [cosmo_change],
                'plot_dict':    {
                    'l1':['QV@alt=300','QV@alt=3000'],
                    'r1':['SLHFLX'],
                },
            },




            {
                'mem_cfgs':     [cmip6_abs_change],
                'plot_dict':    {
                    'l1':['SWNDTOA','LWDTOA','RADNDTOA'],
                },
            },
            {
                'mem_cfgs':     [cmip6_abs_change],
                'plot_dict':    {
                    'l1':['T2M','T@alt=3000'],
                    'r1':['LTS'],
                },
            },
            {
                'mem_cfgs':     [cmip6_abs_change],
                'plot_dict':    {
                    'l1':['QV@alt=300','QV@alt=3000'],
                    'r1':['SLHFLX'],
                },
            },
        ],
        'figsize':          (18, 11),
        'nrows':            4,
        'ncols':            3,
        'adjust_key':       '4x3',
        'line_along':       'lon',
        'plot_domain':      dom_trades_full,
        #'time_periods':     get_time_periods_for_month(2007, 8),
    },


    'trades_change':  {
        'panel_cfgs':    [
            {
                'i_recompute':  1, 
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'plot_dict':    {
                    'l1':['ENTR'],
                    'r1':['ENTRSCL'],
                },
                'i_plot_legend':1, 
                'title':        'CTRL & PGW',
            },
            {
                'mem_cfgs':     [cosmo_change],
                'plot_dict':    {
                    'l1':['ENTR'],
                    'r1':['ENTRSCL'],
                },
            },

            {
                'i_recompute':  1, 
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'plot_dict':    {
                    'l1':['W@alt=3000','W@alt=5000'],
                },
                'i_plot_legend':1, 
                'title':        'CTRL & PGW',
            },
            {
                'mem_cfgs':     [cosmo_change],
                'plot_dict':    {
                    'l1':['W@alt=3000','W@alt=5000'],
                },
            },


            {
                'i_recompute':  1, 
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'plot_dict':    {
                    'l1':['LCL','LOWCLDBASE','INVHGT'],
                    'r1':['DINVHGTLCL'],
                    'r2':['DINVHGTLOWCLDBASE'],
                },
                'i_plot_legend':1, 
                'title':        'CTRL & PGW',
            },
            {
                'mem_cfgs':     [cosmo_change],
                'plot_dict':    {
                    'l1':['LCL','LOWCLDBASE','INVHGT'],
                    'r1':['DINVHGTLCL'],
                    'r2':['DINVHGTLOWCLDBASE'],
                },
            },


            {
                'i_recompute':  1, 
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'plot_dict':    {
                    'l1':['SLHFLX'],
                    'r1':['ENTRDRY'],
                    'r2':['PP'],
                },
                'i_plot_legend':1, 
                'title':        'CTRL & PGW',
            },
            {
                'mem_cfgs':     [cosmo_change],
                'plot_dict':    {
                    'l1':['SLHFLX'],
                    'r1':['ENTRDRY'],
                    'r2':['PP'],
                },
            },

            {
                'i_recompute':  1, 
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'plot_dict':    {
                    'l1':['INVSTRV'],
                    'r1':['LTS'],
                    'r2':['DQVINV'],
                },
                'i_plot_legend':1, 
                'title':        'CTRL & PGW',
            },
            {
                'mem_cfgs':     [cosmo_change],
                'plot_dict':    {
                    'l1':['INVSTRV'],
                    'r1':['LTS'],
                    'r2':['DQVINV'],
                },
            },

            {
                'i_recompute':  1, 
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'plot_dict':    {
                    #'l1':['CLWDTOA','LWDTOA'],
                    'l1':['ENTRDRY'],
                    'r1':['CLCL','CLCH'],
                    'r2':['ALBEDO'],
                    #'r2':['CRESWNDTOA','CSWNDTOA'],
                },
                'i_plot_legend':1, 
                'title':        'CTRL & PGW',
            },
            {
                'mem_cfgs':     [cosmo_change],
                'plot_dict':    {
                    #'l1':['CLWDTOA','LWDTOA'],
                    'l1':['ENTRDRY'],
                    'r1':['CLCL','CLCH'],
                    'r2':['ALBEDO'],
                    #'r2':['CRESWNDTOA','CSWNDTOA'],
                },
            },


            {
                'i_recompute':  1, 
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'plot_dict':    {
                    'l1':['T2M'],
                    'r1':['PP'],
                    'r2':['BUOYIFLX@alt=300'],
                },
                'i_plot_legend':1, 
                'title':        'CTRL & PGW',
            },
            {
                'mem_cfgs':     [cosmo_change],
                'plot_dict':    {
                    'l1':['T2M'],
                    'r1':['PP'],
                    'r2':['BUOYIFLX@alt=300'],
                },
            },


            {
                'i_recompute':  1, 
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'plot_dict':    {
                    'l1':['T@alt=3000'],
                    'r1':['QV@alt=3000'],
                    'r2':['RH@alt=3000'],
                },
                'i_plot_legend':1, 
                'title':        'CTRL & PGW',
            },
            {
                'mem_cfgs':     [cosmo_change],
                'plot_dict':    {
                    'l1':['T@alt=3000'],
                    'r1':['QV@alt=3000'],
                    'r2':['RH@alt=3000'],
                },
            },


            {
                'i_recompute':  1, 
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'plot_dict':    {
                    'l1':['SLHFLX'],
                    'r1':['UV10M'],
                    'r2':['SSHFLX'],
                },
                'i_plot_legend':1, 
                'title':        'CTRL & PGW',
            },
            {
                'mem_cfgs':     [cosmo_change],
                'plot_dict':    {
                    'l1':['SLHFLX'],
                    'r1':['UV10M'],
                    'r2':['SSHFLX'],
                },
            },


            {
                'i_recompute':  1, 
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'plot_dict':    {
                    'l1':['T@alt=300'],
                    'r1':['QV@alt=300'],
                    'r2':['RH@alt=300'],
                },
                'i_plot_legend':1, 
                'title':        'CTRL & PGW',
            },
            {
                'mem_cfgs':     [cosmo_change],
                'plot_dict':    {
                    'l1':['T@alt=300'],
                    'r1':['QV@alt=300'],
                    'r2':['RH@alt=300'],
                },
            },

        ],
        'figsize':          (22, 14),
        'nrows':            5,
        'ncols':            4,
        'adjust_key':       '5x4',
        'line_along':       'lon',
        'plot_domain':      dom_trades_full,
        'time_periods':     time_periods_ana,
        'name_dict_append': {'change':change_type},
        #'time_periods':     time_periods_ana_JJA,
        #'name_dict_append': {'month':'JJA','change':change_type},
        #'time_periods':     time_periods_ana_SON,
        #'name_dict_append': {'month':'SON','change':change_type},
        #'time_periods':     time_periods_ana_DJF,
        #'name_dict_append': {'month':'DJF','change':change_type},
        #'time_periods':     time_periods_ana_MAM,
        #'name_dict_append': {'month':'MAM','change':change_type},
    },

    'subtr_cooling':  {
        'panel_cfgs':    [
            #{
            #    'i_recompute':  1, 
            #    'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
            #    'plot_dict':    {
            #        'l1':['QV@alt=14000'],
            #        'r1':['QV@alt=12000'],
            #        'r2':['QV@alt=16000'],
            #    },
            #    'i_plot_legend':1, 
            #    'title':        'CTRL & PGW',
            #},

            #{
            #    'i_recompute':  1, 
            #    'mem_cfgs':     [mpi_hist, mpi_scen],
            #    'plot_dict':    {
            #        'l1':['QV@alt=14000'],
            #        'r1':['QV@alt=12000'],
            #        'r2':['QV@alt=16000'],
            #    },
            #    'title':        'HIST & SCEN',
            #},

            #{
            #    'mem_cfgs':     [cosmo_abs_change],
            #    'plot_dict':    {
            #        'l1':['QV@alt=14000'],
            #        'r1':['QV@alt=12000'],
            #        'r2':['QV@alt=16000'],
            #    },
            #},

            #{
            #    'mem_cfgs':     [mpi_abs_change],
            #    'plot_dict':    {
            #        'l1':['QV@alt=14000'],
            #        'r1':['QV@alt=12000'],
            #        'r2':['QV@alt=16000'],
            #    },
            #},

            #{
            #    'mem_cfgs':     [cosmo_rel_change],
            #    'plot_dict':    {
            #        'l1':['QV@alt=14000'],
            #        'r1':['QV@alt=12000'],
            #        'r2':['QV@alt=16000'],
            #    },
            #},

            #{
            #    'mem_cfgs':     [mpi_rel_change],
            #    'plot_dict':    {
            #        'l1':['QV@alt=14000'],
            #        'r1':['QV@alt=12000'],
            #        'r2':['QV@alt=16000'],
            #    },
            #},





            #{
            #    'i_recompute':  1, 
            #    'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
            #    'plot_dict':    {
            #        'l1':['T@alt=14000'],
            #        'r1':['T@alt=12000'],
            #        'r2':['T@alt=16000'],
            #    },
            #    'i_plot_legend':1, 
            #    'title':        'CTRL & PGW',
            #},

            #{
            #    'i_recompute':  1, 
            #    'mem_cfgs':     [mpi_hist, mpi_scen],
            #    'plot_dict':    {
            #        'l1':['T@alt=14000'],
            #        'r1':['T@alt=12000'],
            #        'r2':['T@alt=16000'],
            #    },
            #    'title':        'HIST & SCEN',
            #},

            #{
            #    'mem_cfgs':     [cosmo_abs_change],
            #    'plot_dict':    {
            #        'l1':['T@alt=14000'],
            #        'r1':['T@alt=12000'],
            #        'r2':['T@alt=16000'],
            #    },
            #},

            #{
            #    'mem_cfgs':     [mpi_abs_change],
            #    'plot_dict':    {
            #        'l1':['T@alt=14000'],
            #        'r1':['T@alt=12000'],
            #        'r2':['T@alt=16000'],
            #    },
            #},

            #{
            #    'mem_cfgs':     [cosmo_rel_change],
            #    'plot_dict':    {
            #        'l1':['T@alt=14000'],
            #        'r1':['T@alt=12000'],
            #        'r2':['T@alt=16000'],
            #    },
            #},

            #{
            #    'mem_cfgs':     [mpi_rel_change],
            #    'plot_dict':    {
            #        'l1':['T@alt=14000'],
            #        'r1':['T@alt=12000'],
            #        'r2':['T@alt=16000'],
            #    },
            #},



            {
                'mem_cfgs':     [cosmo_rel_change],
                'plot_dict':    {
                    'l1':['QV@alt=14000'],
                    'r1':['QV@alt=12000'],
                    'r2':['QV@alt=16000'],
                },
            },
            {
                'mem_cfgs':     [mpi_rel_change],
                'plot_dict':    {
                    'l1':['QV@alt=14000'],
                    'r1':['QV@alt=12000'],
                    'r2':['QV@alt=16000'],
                },
            },
            {
                'mem_cfgs':     [cmip6_rel_change],
                'plot_dict':    {
                    'l1':['QV@alt=14000'],
                    'r1':['QV@alt=12000'],
                    'r2':['QV@alt=16000'],
                },
            },


            {
                'mem_cfgs':     [cosmo_abs_change],
                'plot_dict':    {
                    'l1':['T@alt=14000'],
                    'r1':['T@alt=12000'],
                    'r2':['T@alt=16000'],
                },
            },

            {
                'mem_cfgs':     [mpi_abs_change],
                'plot_dict':    {
                    'l1':['T@alt=14000'],
                    'r1':['T@alt=12000'],
                    'r2':['T@alt=16000'],
                },
            },

            {
                'mem_cfgs':     [cmip6_abs_change],
                'plot_dict':    {
                    'l1':['T@alt=14000'],
                    'r1':['T@alt=12000'],
                    'r2':['T@alt=16000'],
                },
            },
        ],
        'figsize':          (12, 6),
        'nrows':            2,
        'ncols':            3,
        'adjust_key':       '2x3',
        'line_along':       'lat',
        'plot_domain':      dom_SA_ana_merid_cs,
    },
}

trades_seas = copy.deepcopy(run_cfgs['trades_change'])
test_memb = {
    'mem_key':'COSMO_3.3_ctrl',
    'time_periods':run_cfgs['trades_change']['time_periods'], 
}
ctrl_memb = {
    'mem_key':'COSMO_3.3_ctrl',
    'time_periods':time_periods_ana, 
}
for pi,pan_cfg in enumerate(trades_seas['panel_cfgs']):
    if pan_cfg['mem_cfgs'][0] == 'COSMO_3.3_ctrl':
        pan_cfg['mem_cfgs'][0] = ctrl_memb
        pan_cfg['mem_cfgs'][1] = test_memb
    else:
        if change_type == 'abs':
            diff = {
                'mem_oper':     'diff',
                'mem_keys':     [test_memb,ctrl_memb],
                'label':        'PGW$-$CTRL',
            }
        elif change_type == 'rel':
            diff = {
                'mem_oper':     'rel0.01',
                'mem_keys':     [test_memb,ctrl_memb],
                'label':        'PGW$/$CTRL$-$1',
            }
        pan_cfg['mem_cfgs'][0] = diff
        ## delete some variables
        remove_vars = [
            'BUOYIFLX@alt=300',
            #'QV@alt=20',
            #'QV@alt=3000',
            #'RH@alt=3000',
            #'T@alt=3000',
            #'RH@alt=300',
            #'T@alt=300',
            #'QV@alt=300',
        ]
        for rmv in remove_vars:
            for axkey in ['l1','r1','r2']:
                try:
                    pan_cfg['plot_dict'][axkey].remove(rmv)
                except KeyError:
                    pass
                except ValueError:
                    pass
        #print(pan_cfg['plot_dict'])
    trades_seas['panel_cfgs'][pi] = pan_cfg
run_cfgs['trades_seas'] = trades_seas

agg_level = TP.ALL_TIME
#agg_level = TP.ANNUAL_CYCLE

use_cfg = 'subtr_cooling'
#use_cfg = 'itcz_overview'
#use_cfg = 'trades_change'
#use_cfg = 'trades_seas'
#use_cfg = 'test'

default_time_periods = time_periods_ana
default_time_periods = time_periods_2007
#default_time_periods = get_time_periods_for_month(2007, 8)

run_cfg = run_cfgs[use_cfg]

name_dict = {
    'cfg':use_cfg,
    run_cfg['plot_domain']['key']:  run_cfg['line_along'],
}
if 'name_dict_append' in run_cfg:
    name_dict.update(run_cfg['name_dict_append'])


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


cfg = {
    'serial_time_plt_sels': serial_time_plt_sels,
    'sub_dir':              'lls_paper_fb',
    'name_dict':            name_dict,
    'figsize':              run_cfg['figsize'],
    'nrows':                nrows,
    'ncols':                ncols,
    'subplots_adjust_spatial':
                            '1x1', # dummy
    'args_subplots_adjust': args_subplots_adjust[run_cfg['adjust_key']],
    'kwargs_remove_axis_labels': {
        'remove_level': 0,
    },
    'kwargs_panel_labels' : {
        'shift_right':  -0.18,
        'shift_up':     0.06,
    },

    'all_panels':
        {
            'ana_number':   15,
            'agg_level':    agg_level,
            'i_recompute':  0,
            'plot_domain':  run_cfg['plot_domain'],
            'time_periods': default_time_periods,
            #'var_names':    run_cfg['default_var_names'],
            'i_plot_legend':0,
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
for attr in ['time_periods','line_along']:
    if attr in run_cfg:
        cfg['all_panels'][attr] = run_cfg[attr]


mi = 0
for panel_cfg in run_cfg['panel_cfgs']:
    #print(mem_cfg)
    col_ind = mi % ncols
    row_ind = int(mi/ncols)
    pan_key = '{},{}'.format(row_ind, col_ind)

    if panel_cfg is not None:
        print(panel_cfg)
        
        #pan_dict = {
        #    'mem_cfgs':     panel_cfg['mem_cfgs'],
        #}

        #if 'i_recompute' in panel_cfg:
        #    pan_dict['i_recompute'] = panel_cfg['i_recompute']
        #if 'time_periods' in panel_cfg:
        #    pan_dict['time_periods'] = panel_cfg['time_periods']
        #if 'title' in panel_cfg:
        #    pan_dict['title'] = panel_cfg['title']
        #if 'var_names' in panel_cfg:
        #    pan_dict['var_names'] = panel_cfg['var_names']
        #if 'i_plot_legend' in panel_cfg:
        #    pan_dict['i_plot_legend'] = panel_cfg['i_plot_legend']
        #for attr in check_attrs:
        #    if attr in panel_cfg:
        #        pan_dict[attr] = panel_cfg[attr]

        #cfg['panels'][pan_key] = pan_dict
        cfg['panels'][pan_key] = panel_cfg

    mi += 1
#print(cfg['panels']['0,0'])
#quit()

