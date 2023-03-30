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

time_periods = []
start_year = 2007
end_year = 2009
start_month = 1
end_month = 12
start_day = 1
end_day = 31

#start_year = 2006
#end_year = 2006
#start_month = 8
#end_month = 8
#start_day = 1
#end_day = 10
time_periods_cosmo = [{'first_date':datetime(start_year,start_month,start_day),
                       'last_date':datetime(end_year,end_month,end_day)}]

time_periods_cmip6 = [{'first_date':datetime(1985,1,1),
                       'last_date':datetime(2014,12,31)},
                      {'first_date':datetime(2070,1,1),
                       'last_date':datetime(2099,12,31)},
                       ]

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

#ctrl_12 = 'COSMO_12_ctrl'
#pgw_12 = 'COSMO_12_pgw'
cmip6 = 'cmip6'
ctrl_3 = 'COSMO_3.3_ctrl'
pgw_3 = 'COSMO_3.3_pgw'


i_recompute = {
    ctrl_3:     1,
    pgw_3:      1,
    cmip6:      0,
    #ctrl_12:    1,
    #pgw_12:     1,
}

var_name = 'LWUTOA'
#var_name = 'SWNDTOA'
#var_name = 'RADNDTOA'
#var_name = 'CRELWUTOA'
#var_name = 'CRESWNDTOA'
#var_name = 'CRERADNDTOA'
#var_name = 'CLCT'
#var_name = 'CLCL'
#var_name = 'CLCM'
#var_name = 'CLCH'
#var_name = 'ALBEDO'
#var_name = 'SUBS'
#var_name = 'INVHGT'
#var_name = 'INVF'
#var_name = 'ENTR'

ANA_NATIVE_domain = dom_SA_3km_large3
if var_name in ['INVHGT', 'INVF', 'ENTR']:
    ANA_NATIVE_domain = dom_SA_ana

#models_cmip6 = models_cmip6[0:2]
mem_keys_cmip6_hist = ['{}_historical'.format(model) for model in models_cmip6]
mem_keys_cmip6_ssp585 = ['{}_ssp585'.format(model) for model in models_cmip6]

name_dict = {
    plot_domain['key']:var_name,
    'time':agg_level,
}

#nrows = 2
nrows = 1
ncols = 3

cfg = {
    'serial_time_plt_sels': serial_time_plt_sels,
    'sub_dir':              'sp_change',
    'name_dict':            name_dict,
    'figsize':              (nlp['figsize_spatial']['{}x{}'.format(
                                    nrows,ncols).format(nrows,ncols)][0],
                             nlp['figsize_spatial']['{}x{}'.format(
                                    nrows,ncols).format(nrows,ncols)][1]),
    'nrows':                nrows,
    'ncols':                ncols,
    'subplots_adjust':      '{}x{}'.format(nrows,ncols),
    'i_remove_axis_labels': 1,
    'args_subplots_adjust':  {
        ## only for nrows = 1
        'wspace':0.25,
                            },
    'all_panels':
        {
            'ana_number':   1,
            'var_names':    [var_name],
            'agg_level':    agg_level,
            'plot_domain':  plot_domain,
            'plot_ax_cbars':{
                                'abs':  1,
                                'diff': 1,
                            },
            'i_recompute':  0,
            'ANA_NATIVE_domain':
                            ANA_NATIVE_domain,
        },
    'panels':
    {
        '0,0':
        {
            'time_periods': time_periods_cosmo,
            'i_recompute':  i_recompute[ctrl_3],
            'mem_keys':     [ctrl_3],
        },
        '0,1':
        {
            'time_periods': time_periods_cosmo,
            'i_recompute':  i_recompute[pgw_3],
            'mem_keys':     [pgw_3],
        },
        '0,2':
        {
            'time_periods': time_periods_cosmo,
            'mem_keys':     [{'diff':[pgw_3,ctrl_3], 'label':'PGW - CTRL'}],
        },

        #'1,0':
        #{
        #    'time_periods': time_periods_cmip6,
        #    'i_recompute':  i_recompute[cmip6],
        #    'mem_keys':     [{'mean':mem_keys_cmip6_hist, 'label':'CMIP6 HIST'}],
        #},
        #'1,1':
        #{
        #    'time_periods': time_periods_cmip6,
        #    'i_recompute':  i_recompute[cmip6],
        #    'mem_keys':     [pgw_12],
        #    'mem_keys':     [{'mean':mem_keys_cmip6_ssp585, 'label':'CMIP6 SSP5-85'}],
        #},
        #'1,2':
        #{
        #    'time_periods': time_periods_cmip6,
        #    'mem_keys':     [{'diff':[pgw_12,ctrl_12]}],
        #    'mem_keys':     [{'diff':[{'mean':mem_keys_cmip6_ssp585},
        #                              {'mean':mem_keys_cmip6_hist}],
        #                      'label':'CMIP6 change'}],
        #},

        #'1,0':
        #{
        #    'i_recompute':  i_recomputeute[ctrl_12],
        #    'mem_keys':     [ctrl_12],
        #},
        #'1,1':
        #{
        #    'i_recompute':  i_recomputeute[pgw_12],
        #    'mem_keys':     [pgw_12],
        #},
        #'1,2':
        #{
        #    'mem_keys':     [{'diff':[pgw_12,ctrl_12]}],
        #},
    }
}
