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
###############################################################################

time_periods = []
start_year = 2006
end_year = 2007
start_month = 8
end_month = 12
start_day = 1
end_day = 31

#start_year = 2006
#end_year = 2006
#start_month = 8
#end_month = 8
#start_day = 1
#end_day = 1
time_periods = [{'first_date':datetime(start_year,start_month,start_day),
                 'last_date':datetime(end_year,end_month,end_day)}]

plot_domain = dom_SA_ana_sea
#plot_domain = dom_SA_ana_land

agg_level = TP.ANNUAL_CYCLE
agg_level = TP.ALL_TIME

if agg_level == TP.ALL_TIME:
    serial_time_plt_sels = [None]
elif agg_level == TP.ANNUAL_CYCLE:
    serial_time_plt_sels = []
    for month in range(1,13,1):
        serial_time_plt_sels.append({'month':month})
elif agg_level == TP.DIURNAL_CYCLE:
    serial_time_plt_sels = []
    for hour in range(0,23,3):
        serial_time_plt_sels.append({'hour':hour})
else:
    raise NotImplementedError()

line_along = 'lat'
#line_along = 'lon'

era5 = 'ERA5'
ctrl_3 = 'COSMO_3.3_ctrl'
ctrl_12 = 'COSMO_12_ctrl'
sat = 'CERES_EBAF'
mpi = 'MPI-ESM1-2-HR'
eval = sat

skip_recompute = {
    era5:       1,
    ctrl_3:     0,
    ctrl_12:    0,
    sat:        0,
    mpi:        0,
}

name_dict = {
    plot_domain['key']:line_along,
    'time':agg_level,
}

var_names = ['SWNDTOA', 'LWUTOA', 'RADNDTOA']

colors = {
    var_names[0]:  'orange',
    var_names[1]:   'blue',
    var_names[2]: 'black',
}
linestyles = {
    var_names[0]:  '-',
    var_names[1]:   '-',
    var_names[2]: '-',
}

cfg = {
    'serial_time_plt_sels': serial_time_plt_sels,
    'sub_dir':              'toa_rad_eval',
    'name_dict':            name_dict,
    'figsize':              (10,9),
    'nrows':                4,
    'ncols':                4,
    'subplots_adjust':       '4x4',
    'i_remove_axis_labels': 1,
    'arg_subplots_adjust':  {
                            },
    'all_panels':
        {
            'time_periods': time_periods,
            'agg_level':    agg_level,
            'plot_domain':  plot_domain,
            'use_ax_cbars': False,
            'line_along':   line_along,
            'line_at':      slice(plot_domain['lon'].start+1,
                                  plot_domain['lon'].stop-1),
            'skip_recomp':  1,
        },
    'panels':
    {


        '0,0':
        {
            'skip_recomp':  skip_recompute[era5],
            'ana_number':   4,
            'mem_keys':     [era5],
            'fg_var_names': ['QC', 'QI'],
            'bg_var_name':  'QV',
            'alt_lims':     (0,18000),
        },
        '0,1':
        {
            'skip_recomp':  skip_recompute[ctrl_3],
            'ana_number':   4,
            'mem_keys':     [ctrl_3],
            'fg_var_names': ['QC', 'QI'],
            'bg_var_name':  'QV',
            'alt_lims':     (0,18000),
        },
        '0,2':
        {
            'skip_recomp':  skip_recompute[ctrl_12],
            'ana_number':   4,
            'mem_keys':     [ctrl_12],
            'fg_var_names': ['QC', 'QI'],
            'bg_var_name':  'QV',
            'alt_lims':     (0,18000),
        },


        
        '1,1':
        {
            'ana_number':   4,
            'mem_keys':     [{'diff':[ctrl_3,era5]}],
            'fg_var_names': ['QC', 'QI'],
            'bg_var_name':  'QV',
            'alt_lims':     (0,18000),
        },
        '1,2':
        {
            'ana_number':   4,
            'mem_keys':     [{'diff':[ctrl_12,era5]}],
            'fg_var_names': ['QC', 'QI'],
            'bg_var_name':  'QV',
            'alt_lims':     (0,18000),
        },


        '1,3':
        {
            'skip_recomp':  skip_recompute[sat],
            'ana_number':   15,
            'plot_dict':    {
                            'l1':[{'mem_key':sat,    'var_name':var_names[0],
                                   'color':colors[var_names[0]],
                                   'linestyle':linestyles[var_names[0]]},
                                  {'mem_key':sat,    'var_name':var_names[1],
                                   'color':colors[var_names[1]],
                                   'linestyle':linestyles[var_names[1]]},
                                  {'mem_key':sat,  'var_name':var_names[2],
                                   'color':colors[var_names[2]],
                                   'linestyle':linestyles[var_names[2]]},
                                   ],
                            },
        },



        '2,0':
        {
            'skip_recomp':  skip_recompute[era5],
            'ana_number':   15,
            'plot_dict':    {
                            'l1':[{'mem_key':era5,  'var_name':var_names[0],
                                   'color':colors[var_names[0]],
                                   'linestyle':linestyles[var_names[0]]},
                                  {'mem_key':era5,  'var_name':var_names[1],
                                   'color':colors[var_names[1]],
                                   'linestyle':linestyles[var_names[1]]},
                                  {'mem_key':era5,  'var_name':var_names[2],
                                   'color':colors[var_names[2]],
                                   'linestyle':linestyles[var_names[2]]},
                                   ],
                            },
            'legend_for':   [{'mem_key':era5,  'var_name':var_names[0]},
                             {'mem_key':era5,  'var_name':var_names[1]},
                             {'mem_key':era5,  'var_name':var_names[2]},
                            ],
        },
        '2,1':
        {
            'skip_recomp':  skip_recompute[ctrl_3],
            'ana_number':   15,
            'plot_dict':    {
                            'l1':[{'mem_key':ctrl_3,    'var_name':var_names[0],
                                   'color':colors[var_names[0]],
                                   'linestyle':linestyles[var_names[0]]},
                                  {'mem_key':ctrl_3,    'var_name':var_names[1],
                                   'color':colors[var_names[1]],
                                   'linestyle':linestyles[var_names[1]]},
                                  {'mem_key':ctrl_3,  'var_name':var_names[2],
                                   'color':colors[var_names[2]],
                                   'linestyle':linestyles[var_names[2]]},
                                   ],
                            },
        },
        '2,2':
        {
            'skip_recomp':  skip_recompute[ctrl_12],
            'ana_number':   15,
            'plot_dict':    {
                            'l1':[{'mem_key':ctrl_12,    'var_name':var_names[0],
                                   'color':colors[var_names[0]],
                                   'linestyle':linestyles[var_names[0]]},
                                  {'mem_key':ctrl_12,    'var_name':var_names[1],
                                   'color':colors[var_names[1]],
                                   'linestyle':linestyles[var_names[1]]},
                                  {'mem_key':ctrl_12,  'var_name':var_names[2],
                                   'color':colors[var_names[2]],
                                   'linestyle':linestyles[var_names[2]]},
                                   ],
                            },
        },
        '2,3':
        {
            'skip_recomp':  skip_recompute[mpi],
            'ana_number':   15,
            'plot_dict':    {
                            'l1':[{'mem_key':mpi,    'var_name':var_names[0],
                                   'color':colors[var_names[0]],
                                   'linestyle':linestyles[var_names[0]]},
                                  {'mem_key':mpi,    'var_name':var_names[1],
                                   'color':colors[var_names[1]],
                                   'linestyle':linestyles[var_names[1]]},
                                  {'mem_key':mpi,  'var_name':var_names[2],
                                   'color':colors[var_names[2]],
                                   'linestyle':linestyles[var_names[2]]},
                                   ],
                            },
        },



        '3,0':
        {
            'ana_number':   15,
            'plot_dict':    {
                            'l1':[{'mem_key':{'diff':[era5,eval]},  'var_name':var_names[0],
                                   'color':colors[var_names[0]],
                                   'linestyle':linestyles[var_names[0]]},
                                  {'mem_key':{'diff':[era5,eval]},  'var_name':var_names[1],
                                   'color':colors[var_names[1]],
                                   'linestyle':linestyles[var_names[1]]},
                                  {'mem_key':{'diff':[era5,eval]},  'var_name':var_names[2],
                                   'color':colors[var_names[2]],
                                   'linestyle':linestyles[var_names[2]]},
                                   ],
                            },
        },
        '3,1':
        {
            'ana_number':   15,
            'plot_dict':    {
                            'l1':[{'mem_key':{'diff':[ctrl_3,eval]},  'var_name':var_names[0],
                                   'color':colors[var_names[0]],
                                   'linestyle':linestyles[var_names[0]]},
                                  {'mem_key':{'diff':[ctrl_3,eval]},  'var_name':var_names[1],
                                   'color':colors[var_names[1]],
                                   'linestyle':linestyles[var_names[1]]},
                                  {'mem_key':{'diff':[ctrl_3,eval]},  'var_name':var_names[2],
                                   'color':colors[var_names[2]],
                                   'linestyle':linestyles[var_names[2]]},
                                   ],
                            },
        },
        '3,2':
        {
            'ana_number':   15,
            'plot_dict':    {
                            'l1':[{'mem_key':{'diff':[ctrl_12,eval]},  'var_name':var_names[0],
                                   'color':colors[var_names[0]],
                                   'linestyle':linestyles[var_names[0]]},
                                  {'mem_key':{'diff':[ctrl_12,eval]},  'var_name':var_names[1],
                                   'color':colors[var_names[1]],
                                   'linestyle':linestyles[var_names[1]]},
                                  {'mem_key':{'diff':[ctrl_12,eval]},  'var_name':var_names[2],
                                   'color':colors[var_names[2]],
                                   'linestyle':linestyles[var_names[2]]},
                                   ],
                            },
        },
        '3,3':
        {
            'ana_number':   15,
            'plot_dict':    {
                            'l1':[{'mem_key':{'diff':[mpi,eval]},  'var_name':var_names[0],
                                   'color':colors[var_names[0]],
                                   'linestyle':linestyles[var_names[0]]},
                                  {'mem_key':{'diff':[mpi,eval]},  'var_name':var_names[1],
                                   'color':colors[var_names[1]],
                                   'linestyle':linestyles[var_names[1]]},
                                  {'mem_key':{'diff':[mpi,eval]},  'var_name':var_names[2],
                                   'color':colors[var_names[2]],
                                   'linestyle':linestyles[var_names[2]]},
                                   ],
                            },
        },

    }
}
