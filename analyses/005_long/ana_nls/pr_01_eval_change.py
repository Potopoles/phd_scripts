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
from package.nl_models import models_cmip6
from nl_plot_org_ana import nlp
###############################################################################

start_year = 2006
end_year = 2006
start_month = 8
end_month = 8
start_day = 1
end_day = 20
#end_day = 1

time_periods = [{'first_date':datetime(start_year,start_month,start_day),
                       'last_date':datetime(end_year,end_month,end_day)}]

time_periods_cmip6 = [{'first_date':datetime(1985,1,1),
                       'last_date':datetime(1985,12,31)},
                       #'last_date':datetime(2014,12,31)},
                       {'first_date':datetime(2070,1,1),
                       'last_date':datetime(2070,12,31)}
                       #'last_date':datetime(2099,12,31)}
                       ]

plot_domain = dom_SA_ana
#plot_domain = dom_SA_ana_sea
plot_domain = dom_ITCZ

agg_level = TP.ALL_TIME

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


nrows = 4
ncols = 4

cosmo           = 'COSMO_3.3_ctrl'
obs             = 'ERA5'


var_name = 'W'
var_name = 'T'
var_name = 'P'
var_name = 'POTT'
#var_name = 'QI'
#var_name = 'QC'
#var_name = 'QV'
#var_name = 'QVFLXZ'
#var_name = 'QS'
#var_name = 'U'
#var_name = 'V'

plot_append = 'compare'

if var_name in ['QI','QC', 'QS', 'U', 'V']:
    models_cmip6 = []
else:
    models_cmip6 = [
        'MPI-ESM1-2-HR',
        #'NorESM2-MM',
        #'GFDL-ESM4',
        #'MIROC6',
        #'NorESM2-LM',
        #'INM-CM5-0',
        #'INM-CM4-8',
    ]

pgw_types = [
    'pgw',
    #'pgwnp',
    #'pgw2',
    #'pgw3',
    'pgw5',
    #'pgw4',
    'pgw6',
]

ctrl_mem_types = [
    '_ref',
    #'_rdheight2',
    '_rdheight2_spubc1',
    #'_rdheight_spubc1',
    #'_nodamp',
    #'_cloudnum',
    '_BC',
]
pgw_mem_types = {
    'pgw':[
        '_ref',
        #'_rdheight2',
        '_rdheight2_spubc1',
        #'_rdheight_spubc1',
        #'_nodamp',
        #'_cloudnum',
        '_BC',
    ],
    #'pgwnp':[
    #    '_ref',
    #    '_rdheight2_spubc1',
    #    '_BC',
    #],
    'pgw2':[
        '_rdheight2',
        '_rdheight2_spubc1',
        '_BC',
    ],
    'pgw3':[
        '_rdheight2',
        '_rdheight2_spubc1',
        '_BC',
    ],
    'pgw5':[
        '_rdheight2',
        '_rdheight2_spubc1',
        '_BC',
    ],
    'pgw4':[
        '_rdheight2',
        '_rdheight2_spubc1',
        '_BC',
    ],
    'pgw6':[
        #'_rdheight2',
        #'_rdheight2_spubc1',
        '_rdheight2_2',
        '_rdheight2_3',
        '_BC',
    ],
}

i_recompute_ctrl    = 0
i_recompute_pgw     = 0
i_recompute_pgw2    = 0
i_recompute_pgw5    = 0
i_recompute_pgw6    = 1

i_recompute_cmip6   = 0



bc_var_names = ['P','T','POTT','QV','U','V']

print(var_name)

name_dict = {}
if plot_domain is not None:
    name_dict[plot_domain['key']] = var_name
else:
    name_dict['None'] = var_name
name_dict[plot_append] = ''

cfg = {
    'serial_time_plt_sels': serial_time_plt_sels,
    'sub_dir':              'pr_eval_change',
    'name_dict':            name_dict,
    'figsize':              (nlp['figsize_lineplot']['{}x{}'.format(
                                    nrows,ncols).format(nrows,ncols)][0],
                             nlp['figsize_lineplot']['{}x{}'.format(
                                    nrows,ncols).format(nrows,ncols)][1]),
    'nrows':                nrows,
    'ncols':                ncols,
    'subplots_adjust_lineplot': 
                            '{}x{}'.format(nrows,ncols),
    'i_remove_axis_labels': 1,
    'i_add_panel_labels':   0,
    'arg_subplots_adjust':  {
                            },
    'all_panels':
        {
            'plot_append':  plot_append,
            'ana_number':   2,
            'var_names':    [var_name],
            'time_periods': time_periods,
            'agg_level':    agg_level,
            'plot_domain':  plot_domain,
            'i_recompute':  0,
        },
    'panels':
    {
        #'0,0':
        #{
        #    'i_recompute':  1,
        #    'mem_keys':     [
        #        #'COSMO_3.3_ctrl_BC',
        #        #'COSMO_3.3_pgw_BC',
        #        'COSMO_3.3_pgwnp_BC',
        #    ],
        #},

        #'1,0':
        #{
        #    'title':        'CMIP6',
        #    'time_periods' : time_periods_cmip6,
        #    'i_recompute':  i_recompute_cmip6,
        #    'mem_keys':     [
        #        #'MPI-ESM1-2-HR_historical',
        #        #'MPI-ESM1-2-HR_ssp585',
        #    ],
        #},
        #'2,0':
        #{
        #    'title':        'CMIP6 SSP585 - HIST',
        #    'time_periods' : time_periods_cmip6,
        #    'mem_keys':     [
        #        {'diff':['MPI-ESM1-2-HR_ssp585',
        #                 'MPI-ESM1-2-HR_historical',],
        #                 'label':'MPI-ESM1-2-HR'},
        #    ],
        #    #'i_plot_legend':False,
        #},

        '0,0':
        {
            'title':        'CTRL',
            'i_recompute':  i_recompute_ctrl,
            'mem_keys':     [
            ],
            'i_plot_legend':False,
        },
        '0,1':
        {
            'title':        'PGW',
            'mem_keys':     [
            ],
            'i_recompute':  i_recompute_pgw,
        },
        '0,2':
        {
            #'i_recompute':  1,
            'title':        '$\Delta_{Model}$ (= PGW - CTRL)',
            'mem_keys':     [
            ],
            'i_plot_legend':False,
        },
        '0,3':
        {
            'title':        '$\Delta_{Model}$ - $\Delta_{BC}$',
            'mem_keys':     [
            ],
            'i_plot_legend':False,
        },

        #'1,0':
        #{
        #    'title':        'CTRL',
        #    #'i_recompute':  i_recompute_ctrl,
        #    'mem_keys':     [
        #    ],
        #    'i_plot_legend':False,
        #},
        #'1,1':
        #{
        #    'title':        'PGW2',
        #    'mem_keys':     [
        #    ],
        #    #'i_recompute':  i_recompute_pgwnp,
        #    'i_recompute':  i_recompute_pgw2,
        #},
        #'1,2':
        #{
        #    #'i_recompute':  1,
        #    'title':        '$\Delta_{Model}$ (= PGW2 - CTRL)',
        #    'mem_keys':     [
        #    ],
        #    'i_plot_legend':False,
        #},
        #'1,3':
        #{
        #    'title':        '$\Delta_{Model}$ - $\Delta_{BC}$',
        #    'mem_keys':     [
        #    ],
        #    'i_plot_legend':False,
        #},


        '1,0':
        {
            'title':        'CTRL',
            #'i_recompute':  i_recompute_ctrl,
            'mem_keys':     [
            ],
            'i_plot_legend':False,
        },
        '1,1':
        {
            'title':        'PGW5',
            'mem_keys':     [
            ],
            'i_recompute':  i_recompute_pgw5,
        },
        '1,2':
        {
            #'i_recompute':  1,
            'title':        '$\Delta_{Model}$ (= PGW5 - CTRL)',
            'mem_keys':     [
            ],
            'i_plot_legend':False,
        },
        '1,3':
        {
            'title':        '$\Delta_{Model}$ - $\Delta_{BC}$',
            'mem_keys':     [
            ],
            'i_plot_legend':False,
        },




        '2,0':
        {
            'title':        'CTRL',
            #'i_recompute':  i_recompute_ctrl,
            'mem_keys':     [
            ],
            'i_plot_legend':False,
        },
        '2,1':
        {
            'title':        'PGW6',
            'mem_keys':     [
            ],
            'i_recompute':  i_recompute_pgw6,
        },
        '2,2':
        {
            #'i_recompute':  1,
            'title':        '$\Delta_{Model}$ (= PGW6 - CTRL)',
            'mem_keys':     [
            ],
            'i_plot_legend':False,
        },
        '2,3':
        {
            'title':        '$\Delta_{Model}$ - $\Delta_{BC}$',
            'mem_keys':     [
            ],
            'i_plot_legend':False,
        },



        '3,0':
        {
            'title':        'CMIP6 HIST',
            'mem_keys':     [
            ],
            'time_periods' : time_periods_cmip6,
            'i_recompute':  i_recompute_cmip6,
        },
        '3,1':
        {
            'title':        'CMIP6 SSP5-85',
            'mem_keys':     [
            ],
            'time_periods' : time_periods_cmip6,
            'i_recompute':  i_recompute_cmip6,
            'i_plot_legend':False,
        },
        '3,2':
        {
            'title':        'CMIP6 SSP5-85 - HIST',
            'mem_keys':     [
            ],
            'time_periods' : time_periods_cmip6,
            'i_plot_legend':False,
        },
        '3,3':
        {
            'title':        '',
            'mem_keys':     [
            ],
            'time_periods' : time_periods_cmip6,
            'i_plot_legend':False,
        },
    }
}

### CTRL PANELS
for mem_type in ctrl_mem_types:

    # skip BC if var_name not contained
    if (var_name not in bc_var_names) and ('BC' in mem_type):
        continue

    ## CTRL
    mem_key = 'COSMO_3.3_ctrl{}'.format(mem_type)
    for c,pgw_type in enumerate(pgw_types):
        cfg['panels']['{},0'.format(c)]['mem_keys'].append(
           mem_key 
        )

### PGW PANELS
c = 0
for pgw_type in pgw_types:
    for mem_type in pgw_mem_types[pgw_type]:

        # skip BC if var_name not contained
        if (var_name not in bc_var_names) and ('BC' in mem_type):
            continue

        ## PGW
        mem_key = 'COSMO_3.3_{}{}'.format(pgw_type, mem_type)
        cfg['panels']['{},1'.format(c)]['mem_keys'].append(
           mem_key 
        )
        ## PGW - CTRL
        if mem_type in ctrl_mem_types:
            mem_key_ctrl = 'COSMO_3.3_ctrl{}'.format(mem_type)
        else:
            mem_key_ctrl = 'COSMO_3.3_ctrl{}'.format('_ref')
        mem_key_pgw = 'COSMO_3.3_{}{}'.format(pgw_type, mem_type)
        cfg['panels']['{},2'.format(c)]['mem_keys'].append(
            {'diff':[mem_key_pgw,mem_key_ctrl],},
        )

        if var_name in bc_var_names:
            if 'BC' not in mem_type:
                ## (PGW - CTRL) - (BC PGW - BC CTRL)
                #mem_key_ctrl = 'COSMO_3.3_ctrl{}'.format(mem_type)
                #mem_key_pgw = 'COSMO_3.3_{}{}'.format(pgw_type, mem_type)
                cfg['panels']['{},3'.format(c)]['mem_keys'].append(
                    {'diff':[
                        {'diff':[mem_key_pgw, mem_key_ctrl],},
                        {'diff':['COSMO_3.3_{}_BC'.format(pgw_type), 'COSMO_3.3_ctrl_BC'],},
                    ],},
                )
    c += 1



### CMIP6
#c = 2
for mod_key in models_cmip6:
    cfg['panels']['{},0'.format(c)]['mem_keys'].append(
        '{}_historical'.format(mod_key)
    )
    cfg['panels']['{},1'.format(c)]['mem_keys'].append(
        '{}_ssp585'.format(mod_key)
    )
    cfg['panels']['{},2'.format(c)]['mem_keys'].append(
        {'diff':['{}_ssp585'.format(mod_key),
                     '{}_historical'.format(mod_key)],
        },
    )
    #cfg['panels']['{},3'.format(c)]['mem_keys'].append(
    #    {'diff':[
    #        {'diff':['{}_ssp585'.format(mod_key),
    #                     '{}_historical'.format(mod_key)],
    #        },
    #        {'diff':['COSMO_3.3_{}_BC'.format(pgw_types[3]), 'COSMO_3.3_ctrl_BC'],},
    #    ],},
    #)
    


#print(cfg['panels']['2,3'])
#quit()
