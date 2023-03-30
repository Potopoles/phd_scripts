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
#end_year = 2007
#start_month = 8
#end_month = 12
#start_day = 1
#end_day = 31
time_periods = [{'first_date':datetime(start_year,start_month,start_day),
                 'last_date':datetime(end_year,end_month,end_day)}]

plot_domain = dom_SA_ana_sea
#plot_domain = dom_SA_ana_land

agg_level = TP.ANNUAL_CYCLE
agg_level = TP.ALL_TIME
#agg_level = TP.SEASONAL_CYCLE

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

era5 = 'ERA5'
ctrl_3 = 'COSMO_3.3_ctrl'
ctrl_12 = 'COSMO_12_ctrl'
mpi = 'MPI-ESM1-2-HR'
cmip6 = 'cmip6'
ceres = 'CERES_EBAF'
cmsaf = 'CM_SAF_MSG_AQUA_TERRA'

i_recompute = {
    era5:       1,
    ctrl_3:     1,
    cmip6:      1,
    ceres:      1,
    cmsaf:      1,
    #ctrl_12:    0,
}

var_name = 'LWUTOA'
#var_name = 'SWNDTOA'
#var_name = 'RADNDTOA'
#var_name = 'ALBEDO'

#models_cmip6 = models_cmip6[0:2]
mem_keys_cmip6 = ['{}_historical'.format(model) for model in models_cmip6]

name_dict = {
    plot_domain['key']:var_name,
    'time':agg_level,
}

nrows = 3
ncols = 4

cfg = {
    'serial_time_plt_sels': serial_time_plt_sels,
    'sub_dir':              'sp_eval',
    'name_dict':            name_dict,
    'figsize':              (nlp['figsize_spatial']['{}x{}'.format(
                                    nrows,ncols).format(nrows,ncols)][0],
                             nlp['figsize_spatial']['{}x{}'.format(
                                    nrows,ncols).format(nrows,ncols)][1]),
    'nrows':                nrows,
    'ncols':                ncols,
    'subplots_adjust':      '{}x{}'.format(nrows,ncols),
    'i_remove_axis_labels': 2,
    'arg_subplots_adjust':  {
                            },
    'all_panels':
        {
            'ana_number':   1,
            'var_names':    [var_name],
            'time_periods': time_periods,
            'agg_level':    agg_level,
            'plot_domain':  plot_domain,
            'plot_ax_cbars':{
                                'abs':  1,
                                'diff': 1,
                            },
            'i_recompute':  0,
        },
    'panels':
    {
        '0,1':
        {
            'i_recompute':  i_recompute[ctrl_3],
            'mem_keys':     [ctrl_3],
        },
        '0,2':
        {
            'i_recompute':  i_recompute[cmip6],
            #'mem_keys':     [mpi],
            'mem_keys':     [{'mean':mem_keys_cmip6, 'label':'CMIP6'}],
        },
        '0,3':
        {
            'i_recompute':  i_recompute[era5],
            'mem_keys':     [era5],
        },
        #'0,4':
        #{
        #    'skip_recomp':  skip_recompute[ctrl_12],
        #    'mem_keys':     [ctrl_12],
        #},


        '1,0':
        {
            'i_recompute':  i_recompute[cmsaf],
            'mem_keys':     [cmsaf],
        },
        '1,1':
        {
            'mem_keys':     [{'diff':[ctrl_3,cmsaf]}],
        },
        '1,2':
        {
            #'mem_keys':     [{'diff':[mpi,cmsaf]}],
            'mem_keys':     [{'diff':[{'mean':mem_keys_cmip6},cmsaf],
                              'label':'CMIP6 - CM SAF'}],
        },
        '1,3':
        {
            'mem_keys':     [{'diff':[era5,cmsaf]}],
        },
        #'1,4':
        #{
        #    'mem_keys':     [{'diff':[ctrl_12,cmsaf]}],
        #},


        '2,0':
        {
            'i_recompute':  i_recompute[ceres],
            'mem_keys':     [ceres],
        },
        '2,1':
        {
            'mem_keys':     [{'diff':[ctrl_3,ceres]}],
        },
        '2,2':
        {
            #'mem_keys':     [{'diff':[mpi,ceres]}],
            'mem_keys':     [{'diff':[{'mean':mem_keys_cmip6},ceres],
                              'label':'CMIP6 - CERES'}],
        },
        '2,3':
        {
            'mem_keys':     [{'diff':[era5,ceres]}],
        },
        #'2,4':
        #{
        #    'mem_keys':     [{'diff':[ctrl_12,ceres]}],
        #},

    }
}

