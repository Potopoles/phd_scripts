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
from package.nl_variables import nlv, get_plt_units
###############################################################################

def fmt_var_title(var_name):
    return(
        '{} [{}]'.format(
            nlv[var_name]['label'], 
            get_plt_units(var_name)
        )
    )

args_subplots_adjust = {
    '1x2': {
        'left':0.15,
        'bottom':0.15,
        'right':0.95,
        'top':0.90,
        'wspace':0.30,
        'hspace':0.40,
    },
    '1x6': {
        'left':0.05,
        'bottom':0.20,
        'right':0.98,
        'top':0.90,
        'wspace':0.30,
        'hspace':0.40,
    },
    '3x2': {
        'left':0.11,
        'bottom':0.08,
        'right':0.98,
        'top':0.95,
        'wspace':0.30,
        'hspace':0.40,
    },
    '3x6': {
        'left':0.04,
        'bottom':0.08,
        'right':0.98,
        'top':0.95,
        'wspace':0.30,
        'hspace':0.40,
    },
    '4x6': {
        'left':0.04,
        'bottom':0.06,
        'right':0.98,
        'top':0.97,
        'wspace':0.30,
        'hspace':0.40,
    },
    '4x8': {
        'left':0.04,
        'bottom':0.06,
        'right':0.98,
        'top':0.97,
        'wspace':0.30,
        'hspace':0.40,
    },
    '5x8': {
        'left':0.04,
        'bottom':0.06,
        'right':0.98,
        'top':0.97,
        'wspace':0.30,
        'hspace':0.40,
    },
}


#models_cmip6 = models_cmip6_cldf[4:10]
models_cmip6 = models_cmip6_cldf
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
    'time_periods': time_periods_cmip6_hist,
}
mpi_scen = {
    'mem_key':      'MPI-ESM1-2-HR_ssp585', 
    'time_periods': time_periods_cmip6_scen,
}
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
cmip6_change = {
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
    'mem_oper':     'rel0.000001',
    'mem_keys':     [pgw, ctrl],
    #'time_periods': time_periods,
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
cmip6_rel = {
    'mem_oper':     'rel0.0001',
    'mem_keys':     mem_keys_cmip6_bias,
}



run_cfgs = {


    'qvdivtest':  {
        'panel_cfgs':    [
            None,
            None,
            None,
            None,
            None,
            None,


            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                #'var_names':    ['QVDIV', 'CSQVDIV', 'CLDQVDIV'], 
                #'title':        fmt_var_title('QVDIV'),
                'var_names':    ['POTTDIV'], 
                'title':        fmt_var_title('POTTDIV'),
                'i_recompute':  0, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                #'var_names':    ['QVDIV', 'CSQVDIV', 'CLDQVDIV'], 
                'var_names':    ['POTTDIV'], 
                #'title':        'PGW - CTRL', 
            },
            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                #'var_names':    ['QVDIV2', 'CSQVDIV2', 'CLDQVDIV2'], 
                #'title':        fmt_var_title('QVDIV2'),
                'var_names':    ['POTTDIV2'], 
                'title':        fmt_var_title('POTTDIV2'),
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                #'var_names':    ['QVDIV2', 'CSQVDIV2', 'CLDQVDIV2'], 
                'var_names':    ['POTTDIV2'], 
                'title':        'PGW - CTRL', 
            },
            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                #'var_names':    ['QVDIV3', 'CSQVDIV3', 'CLDQVDIV3'], 
                #'title':        fmt_var_title('QVDIV3'),
                'var_names':    ['POTTDIV3'], 
                'title':        fmt_var_title('POTTDIV3'),
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                #'var_names':    ['QVDIV3', 'CSQVDIV3', 'CLDQVDIV3'], 
                'var_names':    ['POTTDIV3'], 
                'title':        'PGW - CTRL', 
            },



            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                #'var_names':    ['QVHDIV','CSQVHDIV','CLDQVHDIV',], 
                #'title':        fmt_var_title('QVHDIV'),
                'var_names':    ['POTTHDIV'], 
                'title':        fmt_var_title('POTTHDIV'),
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                #'var_names':    ['QVHDIV','CSQVHDIV','CLDQVHDIV',], 
                'var_names':    ['POTTHDIV'], 
                'title':        'PGW - CTRL', 
            },
            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                #'var_names':    ['QVHDIV2','CSQVHDIV2','CLDQVHDIV2',], 
                #'title':        fmt_var_title('QVHDIV2'),
                'var_names':    ['POTTHDIV2'], 
                'title':        fmt_var_title('POTTHDIV2'),
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                #'var_names':    ['QVHDIV2','CSQVHDIV2','CLDQVHDIV2',], 
                'var_names':    ['POTTHDIV2'], 
                'title':        'PGW - CTRL', 
            },
            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                #'var_names':    ['QVHDIV3','CSQVHDIV3','CLDQVHDIV3',], 
                #'title':        fmt_var_title('QVHDIV3'),
                'var_names':    ['POTTHDIV3'], 
                'title':        fmt_var_title('POTTHDIV3'),
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                #'var_names':    ['QVHDIV3','CSQVHDIV3','CLDQVHDIV3',], 
                'var_names':    ['POTTHDIV3'], 
                'title':        'PGW - CTRL', 
            },



            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                #'var_names':    ['QVVDIV','CSQVVDIV','CLDQVVDIV',], 
                #'title':        fmt_var_title('QVVDIV'),
                'var_names':    ['POTTVDIV'], 
                'title':        fmt_var_title('POTTVDIV'),
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                #'var_names':    ['QVVDIV','CSQVVDIV','CLDQVVDIV',], 
                'var_names':    ['POTTVDIV'], 
                'title':        'PGW - CTRL', 
            },
            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                #'var_names':    ['QVVDIV2','CSQVVDIV2','CLDQVVDIV2',], 
                #'title':        fmt_var_title('QVVDIV2'),
                'var_names':    ['POTTVDIV2'], 
                'title':        fmt_var_title('POTTVDIV2'),
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                #'var_names':    ['QVVDIV2','CSQVVDIV2','CLDQVVDIV2',], 
                'var_names':    ['POTTVDIV2'], 
                'title':        'PGW - CTRL', 
            },
            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                #'var_names':    ['QVVDIV3','CSQVVDIV3','CLDQVVDIV3',], 
                #'title':        fmt_var_title('QVVDIV3'),
                'var_names':    ['POTTVDIV3'], 
                'title':        fmt_var_title('POTTVDIV3'),
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                #'var_names':    ['QVVDIV3','CSQVVDIV3','CLDQVVDIV3',], 
                'var_names':    ['POTTVDIV3'], 
                'title':        'PGW - CTRL', 
            },

        ],
        'default_var_names':[],
        'figsize':          (16, 10),
        'nrows':            4,
        'ncols':            6,
        'adjust_key':       '4x6',
        'plot_domain':      dom_ITCZ_feedback,
        #'plot_domain':      dom_trades_east,
        #'plot_domain':      dom_trades_west,
        #'plot_domain':      dom_trades_full,
    },
    

    'qvdivtest_cmip':  {
        'panel_cfgs':    [
            None,
            None,
            None,
            None,
            None,
            None,


            {
                'mem_cfgs':     [cmip6_hist, cmip6_scen],
                'var_names':    ['QVDIV'], 
                'title':        fmt_var_title('QVDIV'),
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cmip6_change],
                'var_names':    ['QVDIV'], 
                'title':        'SCEN$-$HIST', 
            },
            {
                'mem_cfgs':     [cmip6_hist, cmip6_scen],
                'var_names':    ['QVDIV2'], 
                'title':        fmt_var_title('QVDIV2'),
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cmip6_change],
                'var_names':    ['QVDIV2'], 
                'title':        'SCEN$-$HIST', 
            },
            {
                'mem_cfgs':     [cmip6_hist, cmip6_scen],
                'var_names':    ['QVDIV3'], 
                'title':        fmt_var_title('QVDIV3'),
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cmip6_change],
                'var_names':    ['QVDIV3'], 
                'title':        'PGW - CTRL', 
            },



            {
                'mem_cfgs':     [cmip6_hist, cmip6_scen],
                'var_names':    ['QVHDIV'], 
                'title':        fmt_var_title('QVHDIV'),
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cmip6_change],
                'var_names':    ['QVHDIV'], 
                'title':        'PGW - CTRL', 
            },
            {
                'mem_cfgs':     [cmip6_hist, cmip6_scen],
                'var_names':    ['QVHDIV2'], 
                'title':        fmt_var_title('QVHDIV2'),
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cmip6_change],
                'var_names':    ['QVHDIV2'], 
                'title':        'PGW - CTRL', 
            },
            {
                'mem_cfgs':     [cmip6_hist, cmip6_scen],
                'var_names':    ['QVHDIV3'], 
                'title':        fmt_var_title('QVHDIV3'),
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cmip6_change],
                'var_names':    ['QVHDIV3'], 
                'title':        'PGW - CTRL', 
            },



            {
                'mem_cfgs':     [cmip6_hist, cmip6_scen],
                'var_names':    ['QVVDIV'], 
                'title':        fmt_var_title('QVVDIV'),
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cmip6_change],
                'var_names':    ['QVVDIV'], 
                'title':        'PGW - CTRL', 
            },
            {
                'mem_cfgs':     [cmip6_hist, cmip6_scen],
                'var_names':    ['QVVDIV2'], 
                'title':        fmt_var_title('QVVDIV2'),
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cmip6_change],
                'var_names':    ['QVVDIV2'], 
                'title':        'PGW - CTRL', 
            },
            {
                'mem_cfgs':     [cmip6_hist, cmip6_scen],
                'var_names':    ['QVVDIV3'], 
                'title':        fmt_var_title('QVVDIV3'),
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cmip6_change],
                'var_names':    ['QVVDIV3'], 
                'title':        'PGW - CTRL', 
            },

        ],
        'default_var_names':[],
        'figsize':          (16, 10),
        'nrows':            4,
        'ncols':            6,
        'adjust_key':       '4x6',
        'plot_domain':      dom_ITCZ_feedback,
    },


    'qvdiv':  {
        'panel_cfgs':    [
            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['CSQVDIV3','CLDQVDIV3','QVDIV3',], 
                'title':        fmt_var_title('QVDIV3'),
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['CSQVDIV3','CLDQVDIV3','QVDIV3',], 
                'title':        'PGW$-$CTRL', 
            },

            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['CSQVHDIV3','CLDQVHDIV3','QVHDIV3',], 
                'title':        fmt_var_title('QVHDIV3'),
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['CSQVHDIV3','CLDQVHDIV3','QVHDIV3',], 
                'title':        'PGW$-$CTRL', 
            },

            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['CSQVVDIV3','CLDQVVDIV3','QVVDIV3',], 
                'title':        fmt_var_title('QVVDIV3'),
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['CSQVVDIV3','CLDQVVDIV3','QVVDIV3',], 
                'title':        'PGW$-$CTRL', 
            },

        ],
        'default_var_names':[],
        'figsize':          (5.5, 7.5),
        'nrows':            3,
        'ncols':            2,
        'adjust_key':       '3x2',
        'plot_domain':      dom_ITCZ_feedback,
    },



    'qvdiv_cmip':  {
        'panel_cfgs':    [
            {
                'mem_cfgs':     [cmip6_hist, cmip6_scen],
                'var_names':    ['QVDIV3'], 
                'title':        fmt_var_title('QVDIV3'),
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cmip6_change],
                'var_names':    ['QVDIV3'], 
                'title':        'SCEN$-$HIST', 
            },

            {
                'mem_cfgs':     [cmip6_hist, cmip6_scen],
                'var_names':    ['QVHDIV3'], 
                'title':        fmt_var_title('QVHDIV3'),
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cmip6_change],
                'var_names':    ['QVHDIV3'], 
                'title':        'SCEN$-$HIST', 
            },

            {
                'mem_cfgs':     [cmip6_hist, cmip6_scen],
                'var_names':    ['QVVDIV3'], 
                'title':        fmt_var_title('QVVDIV3'),
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cmip6_change],
                'var_names':    ['QVVDIV3'], 
                'title':        'SCEN$-$HIST', 
            },

        ],
        'default_var_names':[],
        'figsize':          (5.5, 7.5),
        'nrows':            3,
        'ncols':            2,
        'adjust_key':       '3x2',
        'plot_domain':      dom_ITCZ_feedback,
    },


    'itcz':  {
        'panel_cfgs':    [
            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['CLDF'], 
                'title':        fmt_var_title('CLDF'),
                'i_recompute':  0, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['CLDF'], 
                'title':        'PGW$-$CTRL', 
            },

            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['W'], 
                'title':        fmt_var_title('W'),
                'i_recompute':  0, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['W'], 
                'title':        'PGW$-$CTRL', 
            },

            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['POTT','EQPOTT'], 
                'title':        fmt_var_title('POTT'),
                'i_recompute':  0, 
                'i_plot_legend':1, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['POTT','EQPOTT'], 
                'title':        'PGW$-$CTRL', 
            },

            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['CSPOTTDIV3','CLDPOTTDIV3','POTTDIV3'], 
                'title':        fmt_var_title('POTTDIV3'),
                'i_recompute':  0, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['CSPOTTDIV3','CLDPOTTDIV3','POTTDIV3'], 
                'title':        'PGW$-$CTRL', 
            },

            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['CSPOTTHDIV3','CLDPOTTHDIV3','POTTHDIV3'], 
                'title':        fmt_var_title('POTTHDIV3'),
                'i_recompute':  0, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['CSPOTTHDIV3','CLDPOTTHDIV3','POTTHDIV3'], 
                'title':        'PGW$-$CTRL', 
            },

            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['CSPOTTVDIV3','CLDPOTTVDIV3','POTTVDIV3'], 
                'title':        fmt_var_title('POTTVDIV3'),
                'i_recompute':  0, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['CSPOTTVDIV3','CLDPOTTVDIV3','POTTVDIV3'], 
                'title':        'PGW$-$CTRL', 
                'i_plot_legend':1, 
            },

            #{
            #    #'mem_cfgs':     [mpi_hist, mpi_scen],
            #    'mem_cfgs':     [mpi_hist],
            #    'var_names':    ['POTT'], 
            #    'title':        fmt_var_title('POTT'),
            #    'i_recompute':  1, 
            #    'i_plot_legend':1, 
            #},
            #{
            #    #'mem_cfgs':     [cosmo_change,mpi_change],
            #    'mem_cfgs':     [cosmo_change],
            #    'var_names':    ['POTT'], 
            #    'title':        'SCEN$-$HIST', 
            #},

            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['QVHDIV3','QVVDIV3'], 
                'title':        fmt_var_title('QVHDIV3'),
                'i_recompute':  0, 
            },
            {
                #'mem_cfgs':     [cosmo_change],
                #'title':        'PGW$-$CTRL', 
                'mem_cfgs':     [cosmo_rel_change],
                'title':        'PGW$/$CTRL$-$1', 
                'var_names':    ['QVHDIV3','QVVDIV3'], 
                'i_plot_legend':1, 
            },

            {
                'ana_number':   21,
                'mem_cfgs':     [cosmo_change],
                'plot_var_names':
                                ['TV','UPDTV','PARCTV'], 
                'time_periods': time_periods_ana,
                'title':        fmt_var_title('TV'),
                'i_plot_legend':1, 
            },
            {
                'ana_number':   21,
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'plot_var_names':
                                ['UPDBUOYI','PARCBUOYI'], 
                'time_periods': time_periods_ana,
                'title':        fmt_var_title('UPDBUOYI'),
            },
            {
                'ana_number':   21,
                'mem_cfgs':     [cosmo_change],
                'plot_var_names':
                                ['UPDBUOYI','PARCBUOYI'], 
                'time_periods': time_periods_ana,
                'title':        fmt_var_title('UPDBUOYI'),
            },
        ],
        'default_var_names':[],
        'figsize':          (16, 7.5),
        'nrows':            3,
        'ncols':            6,
        'adjust_key':       '3x6',
        'plot_domain':      dom_ITCZ_feedback,
    },



    'large_scale':  {
        'panel_cfgs':    [
            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['CLDF'], 
                'title':        fmt_var_title('CLDF'),
                'i_plot_legend':1, 
                'i_recompute':  0, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['CLDF'], 
                'title':        'PGW - CTRL', 
            },
            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['W'], 
                'title':        fmt_var_title('W'),
                'i_plot_legend':1, 
                'i_recompute':  0, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['W'], 
                'title':        'PGW - CTRL', 
            },

            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['BVF'], 
                'title':        fmt_var_title('BVF'),
                'i_plot_legend':1, 
                'i_recompute':  0, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['BVF'], 
                'title':        'PGW - CTRL', 
            },


            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['POTTDIV3', 'CSPOTTDIV3', 'CLDPOTTDIV3'], 
                'title':        fmt_var_title('POTTDIV3'),
                'i_plot_legend':1, 
                'i_recompute':  0, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['POTTDIV3', 'CSPOTTDIV3', 'CLDPOTTDIV3'], 
                'title':        'PGW - CTRL', 
            },


            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['QVDIV3', 'CSQVDIV3', 'CLDQVDIV3'], 
                'title':        fmt_var_title('QVDIV3'),
                'i_plot_legend':1, 
                'i_recompute':  0, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['QVDIV3', 'CSQVDIV3', 'CLDQVDIV3'], 
                'title':        'PGW - CTRL', 
            },


            None,
            None,


            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['POTTDIV3','POTTHDIV3','POTTVDIV3'], 
                'title':        fmt_var_title('POTTDIV3'),
                'i_recompute':  1, 
                'i_plot_legend':1, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['POTTDIV3','POTTHDIV3','POTTVDIV3'], 
                'title':        'PGW - CTRL', 
            },


            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['QVDIV3','QVHDIV3','QVVDIV3'], 
                'title':        fmt_var_title('QVHDIV3'),
                'i_recompute':  0, 
                'i_plot_legend':1, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['QVDIV3','QVHDIV3','QVVDIV3'], 
                'title':        'PGW - CTRL', 
            },

        
            None,
            None,
            None,
            None,
            None,
            None,


        ],
        'default_var_names':[],
        'figsize':          (16, 10),
        'nrows':            4,
        'ncols':            6,
        'adjust_key':       '4x6',
        'plot_domain':      dom_ITCZ_feedback,
        'plot_domain':      dom_trades_west,
        #'plot_domain':      dom_trades_full,
        #'plot_domain':      dom_trades_east,
    },


    'subtr_cooling':  {
        'panel_cfgs':    [
            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['CSPOTTDIV3','CLDPOTTDIV3','POTTDIV3'], 
                'title':        fmt_var_title('POTTDIV3'),
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['CSPOTTDIV3','CLDPOTTDIV3','POTTDIV3'], 
                'title':        'PGW - CTRL', 
                'i_plot_legend':1, 
            },

            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['QV'], 
                'title':        fmt_var_title('QV'),
                'i_plot_legend':1, 
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['QV'], 
                'title':        'PGW - CTRL', 
            },

            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['QI'], 
                'title':        fmt_var_title('QI'),
                'i_plot_legend':1, 
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['QI'], 
                'title':        'PGW - CTRL', 
            },

        ],
        'default_var_names':[],
        'figsize':          (16, 3),
        'nrows':            1,
        'ncols':            6,
        'adjust_key':       '1x6',
        'plot_domain':      dom_trades_full,
        'plot_domain':      dom_trades_west,
        #'plot_domain':      dom_trades_east,
    },

    'trades_turb_test':  {
        'panel_cfgs':    [
            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['CLDF'], 
                'title':        fmt_var_title('CLDF'),
                'i_plot_legend':1,
                'i_recompute':  0, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['CLDF'], 
                'title':        'PGW - CTRL', 
            },

            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                #'var_names':    ['RH','CSRH','CLDRH'], 
                'var_names':    ['RH'], 
                'title':        fmt_var_title('RH'),
                'i_plot_legend':1,
                'i_recompute':  0, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                #'var_names':    ['RH','CSRH','CLDRH'], 
                'var_names':    ['RH'], 
                'title':        'PGW - CTRL', 
            },

            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                #'var_names':    ['QV','CLDQV','CSQV'], 
                'var_names':    ['QV'], 
                'title':        fmt_var_title('QV'),
                'i_plot_legend':1,
                'i_recompute':  0, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['QV'], 
                'title':        'PGW - CTRL', 
            },

            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['W','CSW'], 
                'title':        fmt_var_title('W'),
                'i_plot_legend':1,
                'i_recompute':  0, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['W','CSW'], 
                'title':        'PGW - CTRL', 
            },




            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                #'var_names':    ['QVDIV3','CSQVDIV3','CLDQVDIV3'], 
                'var_names':    ['QVDIV3'], 
                'title':        fmt_var_title('QVDIV3'),
                'i_plot_legend':1,
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                #'var_names':    ['QVDIV3','CSQVDIV3','CLDQVDIV3'], 
                'var_names':    ['QVDIV3'], 
                'title':        'PGW - CTRL', 
            },

            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['QVDIV3MEAN'], 
                'title':        fmt_var_title('QVDIV3MEAN'),
                'i_recompute':  0, 
            },
            {
                'mem_cfgs':     [cosmo_rel_change],
                'var_names':    ['QVDIV3MEAN'], 
                'title':        'PGW - CTRL', 
            },

            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['QVDIV3TURB','CSQVDIV3TURB','CLDQVDIV3TURB'], 
                'title':        fmt_var_title('QVDIV3TURB'),
                'i_recompute':  0, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['QVDIV3TURB','CSQVDIV3TURB','CLDQVDIV3TURB'], 
                'title':        'PGW - CTRL', 
            },

            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                #'var_names':    ['POTTV','POTT'], 
                'var_names':    ['POTT'], 
                'title':        fmt_var_title('POTTV'),
                'i_plot_legend':1,
                'i_recompute':  0, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                #'var_names':    ['POTTV','POTT'], 
                'var_names':    ['POTT'], 
                'title':        'PGW - CTRL', 
            },


            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                #'var_names':    ['QVHDIV3','CSQVHDIV3','CLDQVHDIV3'], 
                'var_names':    ['QVHDIV3'], 
                'title':        fmt_var_title('QVHDIV3'),
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                #'var_names':    ['QVHDIV3','CSQVHDIV3','CLDQVHDIV3'], 
                'var_names':    ['QVHDIV3'], 
                'title':        'PGW - CTRL', 
            },

            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['QVHDIV3MEAN'], 
                'title':        fmt_var_title('QVHDIV3MEAN'),
                'i_recompute':  0, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['QVHDIV3MEAN'], 
                'title':        'PGW - CTRL', 
            },

            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['QVHDIV3TURB','CSQVHDIV3TURB','CLDQVHDIV3TURB'], 
                'title':        fmt_var_title('QVHDIV3TURB'),
                'i_recompute':  0, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['QVHDIV3TURB','CSQVHDIV3TURB','CLDQVHDIV3TURB'], 
                'title':        'PGW - CTRL', 
            },

            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                #'var_names':    ['TKEV','CSTKEV'], 
                'var_names':    ['TKEV'], 
                'title':        fmt_var_title('TKEV'),
                'i_plot_legend':1,
                'i_recompute':  0, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                #'var_names':    ['TKEV','CSTKEV'], 
                'var_names':    ['TKEV'], 
                'title':        'PGW - CTRL', 
            },




            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                #'var_names':    ['QVVDIV3','CSQVVDIV3','CLDQVVDIV3'], 
                'var_names':    ['QVVDIV3'], 
                'title':        fmt_var_title('QVVDIV3'),
                'i_recompute':  1, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                #'var_names':    ['QVVDIV3','CSQVVDIV3','CLDQVVDIV3'], 
                'var_names':    ['QVVDIV3'], 
                'title':        'PGW - CTRL', 
            },

            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['QVVDIV3MEAN'], 
                'title':        fmt_var_title('QVVDIV3MEAN'),
                'i_recompute':  0, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['QVVDIV3MEAN'], 
                'title':        'PGW - CTRL', 
            },

            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['QVVDIV3TURB','CSQVVDIV3TURB','CLDQVVDIV3TURB'], 
                'title':        fmt_var_title('QVVDIV3TURB'),
                'i_recompute':  0, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['QVVDIV3TURB','CSQVVDIV3TURB','CLDQVVDIV3TURB'], 
                'title':        'PGW - CTRL', 
            },

            #{
            #    'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
            #    'var_names':    ['CLDTKEV'], 
            #    'title':        fmt_var_title('CLDTKEV'),
            #    'i_plot_legend':1,
            #    'i_recompute':  0, 
            #},
            #{
            #    'mem_cfgs':     [cosmo_change],
            #    'var_names':    ['CLDTKEV'], 
            #    'title':        'PGW - CTRL', 
            #},
            {
                'mem_cfgs':     ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw'],
                'var_names':    ['BVF'], 
                'title':        fmt_var_title('BVF'),
                'i_plot_legend':1,
                'i_recompute':  0, 
            },
            {
                'mem_cfgs':     [cosmo_change],
                'var_names':    ['BVF'], 
                'title':        'PGW - CTRL', 
            },

        ],
        'default_var_names':[],
        #'figsize':          (16, 10),
        #'nrows':            4,
        #'ncols':            6,
        #'adjust_key':       '4x6',
        'figsize':          (20, 10),
        'nrows':            4,
        'ncols':            8,
        'adjust_key':       '4x8',
        #'figsize':          (20, 12.5),
        #'nrows':            5,
        #'ncols':            8,
        #'adjust_key':       '5x8',
        #'plot_domain':      dom_trades_full,
        'plot_domain':      dom_trades_west,
        'plot_domain':      dom_trades_east,
        'plot_domain':      dom_trades_easternmost,
        'time_periods':     time_periods_ana,
        'name_dict_append': {},
        #'time_periods':     time_periods_ana_SON,
        #'name_dict_append': {'months':'SON'},
        #'time_periods':     time_periods_ana_JJA,
        #'name_dict_append': {'months':'JJA'},
        #'time_periods':     time_periods_ana_MAM,
        #'name_dict_append': {'months':'MAM'},
        #'time_periods':     time_periods_ana_DJF,
        #'name_dict_append': {'months':'DJF'},
    },
}

agg_level = TP.ALL_TIME
#agg_level = TP.ANNUAL_CYCLE

i_norm_inv = 0

#use_cfg = 'test'
use_cfg = 'qvdivtest'
#use_cfg = 'qvdivtest_cmip'
#use_cfg = 'qvdiv'
#use_cfg = 'qvdiv_cmip'
#use_cfg = 'itcz'
#use_cfg = 'large_scale'
#use_cfg = 'trades_turb_test'
#use_cfg = 'subtr_cooling'

default_time_periods = time_periods_ana
#default_time_periods = time_periods_ana_MAM
#default_time_periods = time_periods_ana_SON
#default_time_periods = time_periods_2007
default_time_periods = get_time_periods_for_month(2007, 8)


run_cfg = run_cfgs[use_cfg]

name_dict = {
    'cfg':use_cfg,
    #'norminv':i_norm_inv,
    run_cfg['plot_domain']['key']:'',
}
if i_norm_inv:
    name_dict.update({'norminv':''})
    for pani,panel_cfg in enumerate(run_cfg['panel_cfgs']):
        if panel_cfg is not None:
            for vari,var_name in enumerate(panel_cfg['var_names']):
                run_cfg['panel_cfgs'][pani]['var_names'][vari] = '{}NORMI'.format(var_name)
if 'name_dict_append' in run_cfg:
    name_dict.update(run_cfg['name_dict_append'])


if run_cfg['plot_domain']['key'] in ['dom_trades_deep', 'dom_trades_shallow', 'dom_trades']:
    alt_lims = (0,4000) 
elif run_cfg['plot_domain']['key'] in ['dom_trades_east', 'dom_trades_west', 'dom_trades_full']:
    alt_lims = (0,4000) 
    alt_lims = (0,18000) 
elif run_cfg['plot_domain']['key'] in ['dom_ITCZ', 'dom_ITCZ_feedback', 'dom_NS_cs', 
    'dom_NS_cs_afr']:
    alt_lims = (0,18000) 
    #alt_lims = (0,6000) 
else:
    alt_lims = (0,18000) 

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
    'sub_dir':              'pr_paper_fb',
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
            'ana_number':   2,
            'agg_level':    agg_level,
            'i_recompute':  0,
            'plot_domain':  run_cfg['plot_domain'],
            'alt_lims':     alt_lims,
            'time_periods': default_time_periods,
            'var_names':    run_cfg['default_var_names'],
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
for attr in ['time_periods']:
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
        
        cfg['panels'][pan_key] = panel_cfg

        #for attr in ['i_recompute','time_periods','title','var_names','i_plot_legend']:
        #    if attr in panel_cfg:
        #        cfg['panels'][pan_key][attr] = panel_cfg[attr]

        ###if 'i_recompute' in panel_cfg:
        ###    pan_dict['i_recompute'] = panel_cfg['i_recompute']
        ###if 'time_periods' in panel_cfg:
        ###    pan_dict['time_periods'] = panel_cfg['time_periods']
        ###if 'title' in panel_cfg:
        ###    pan_dict['title'] = panel_cfg['title']
        ###if 'var_names' in panel_cfg:
        ###    pan_dict['var_names'] = panel_cfg['var_names']
        ###if 'i_plot_legend' in panel_cfg:
        ###    pan_dict['i_plot_legend'] = panel_cfg['i_plot_legend']


    mi += 1
#print(cfg['panels']['0,0'])
#quit()

