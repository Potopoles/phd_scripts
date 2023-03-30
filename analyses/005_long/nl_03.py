
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 005_03_corr:
author			Christoph Heim
date created    25.11.2019
date changed    17.11.2021
usage			import in another script
"""
###############################################################################
import os
from datetime import datetime, timedelta
from base.nl_global import (plot_glob_base_dir, inp_glob_base_dir,
                               ana_glob_base_dir)
from base.nl_domains import *
from package.time_processing import Time_Processing as TP
from package.functions import get_comb_mem_key
from nl_mem_src import *
from package.nl_models import models_cmip6, models_cmip6_cldf
from ana_nls.glob_cfgs import *
###############################################################################
## paths
ana_name        = '005_long'
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name, '03_corr')
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)

# call with python an_03.py -p 12 CRERADNDTOA,T2M -r 0


ANA_NATIVE_domain = dom_SA_3km_large3

plot_domain = dom_SA_ana_sea
#plot_domain = dom_trades

overwrite_var_dom_map = {
    'CRERADNDTOA'   :dom_SA_ana_sea,
    'CRESWNDTOA'    :dom_SA_ana_sea,
    'CRELWUTOA'     :dom_SA_ana_sea,
    'CRELWDTOA'     :dom_SA_ana_sea,
    'T2M'           :dom_global,
}



## run settings
i_debug = 1
i_plot = 1
i_skip_missing = 1

time_periods = []
start_year = 2006
start_month = 8
start_day = 1
end_year = 2006
end_month = 8
end_day = 31
time_periods = [{'first_date':datetime(start_year,start_month,start_day),
                 'last_date':datetime(end_year,end_month,end_day)}]

time_periods_cmip6 = [{'first_date':datetime(1985,1,1),
                       #'last_date':datetime(1985,12,31)},
                       'last_date':datetime(2014,12,31)},
                       {'first_date':datetime(2070,1,1),
                       #'last_date':datetime(2070,12,31)}
                       'last_date':datetime(2099,12,31)}
                       ]

#time_periods_cmip6 = [{'first_date':datetime(2007,1,1),
#                       'last_date':datetime(2007,1,2)},
#                       {'first_date':datetime(2092,1,1),
#                       'last_date':datetime(2092,1,2)}
#                       ]

#time_periods = time_periods_cmip6
time_periods = time_periods_ana
#time_periods = get_time_periods_for_month(2007,1)

agg_level = TP.ALL_TIME
#agg_level = TP.YEARLY_SERIES
#agg_level = TP.MONTHLY_SERIES

agg_operators = [TP.MEAN]

pickle_append = ''
plot_append = ''


#plot_lines = {
#    TP.DIURNAL_CYCLE:   [TP.MEAN],
#    TP.ANNUAL_CYCLE:    [TP.MEAN],
#    TP.DAILY_SERIES:    [TP.MEAN],
#    TP.MONTHLY_SERIES:  [TP.MEAN],
#}
## spread interval limits
#plot_spread = {
#    TP.ANNUAL_CYCLE:    [TP.MIN,TP.MAX], 
#    TP.DIURNAL_CYCLE:   [TP.P25,TP.P75], 
#}



#mem_keys=['COSMO_12_ctrl', 'COSMO_12_pgw', 
#          {'diff':['COSMO_12_pgw','COSMO_12_ctrl']}]
##mem_keys=['COSMO_12_ctrl', 'COSMO_3.3_ctrl', 
##          {'diff':['COSMO_3.3_ctrl','COSMO_12_ctrl']}]
#mem_keys=['COSMO_3.3_ctrl', 'COSMO_3.3_pgw']
##mem_keys=[]
#mem_keys=['COSMO_3.3_ctrl']
##mem_keys=['CERES_EBAF']
#mem_keys=['CM_SAF_MSG_AQUA_TERRA']
##mem_keys=['COSMO_12_ctrl']

ecs = {
    'ACCESS-CM2':       4.72,
    'ACCESS-ESM1-5':    3.87,

    'CAMS-CSM1-0':      2.29,
    'CanESM5':          5.62,
    'CESM2':            5.16,
    'CESM2-WACCM':      4.75,
    'CMCC-CM2-SR5':     3.52,
    #'CMCC-ESM2',
    'CNRM-CM6-1':       4.83,
    'CNRM-ESM2-1':      4.76,
    'E3SM-1-1':         5.32, # this one had a different version number
    'FGOALS-f3-L':      3.00,
    'FGOALS-g3':        2.88,
    #'GFDL-CM4',
    #'GFDL-ESM4',
    'GISS-E2-1-G':      2.72,
    'HadGEM3-GC31-LL':  5.55,
    'MIROC6':           2.61,
    'MIROC-ES2L':       2.68,
    'MPI-ESM1-2-HR':    2.98,
    'MPI-ESM1-2-LR':    3.00,
    'MRI-ESM2-0':       3.15,
    'NorESM2-LM':       2.54,
    'NorESM2-MM':       2.50,
    'TaiESM1':          4.31,
    'UKESM1-0-LL':      5.34,
}


#models_cmip6_pgw = [
#    'CESM2-WACCM',
#    'GFDL-CM4',
#    'IPSL-CM6A-LR',
#    'MIROC6',
#    'MPI-ESM1-2-HR',
#    'MPI-ESM1-2-LR',
#    'MRI-ESM2-0',
#    'NorESM2-LM',       
#    'NorESM2-MM',
#    'TaiESM1',
#]

models_cmip6 = models_cmip6_cldf
#models_cmip6 = models_cmip6_cldf[0:5]
#models_cmip6 = models_cmip6_cldf[10:]

line_member = 'COSMO'
line_member_mem_cfg = {
    'mem_oper': 'diff', 
    'mem_keys': [{'mem_key': 'COSMO_3.3_pgw3'}, {'mem_key': 'COSMO_3.3_ctrl'}],
    'label':    'COSMO',
}

uncertainty_range_xvals = [-0.385,-0.193]

mem_cfgs = []

#mem_cfgs.append(cosmo_change)
mem_cfgs.append(line_member_mem_cfg)
#mem_cfgs.append(mpi_change)

for mod_key in models_cmip6:
    mem_cfgs.append({
        'mem_oper':'diff',
        'mem_keys':[
            {
                'mem_key':'{}_ssp585'.format(mod_key),
                'time_periods':time_periods_cmip6_scen,
            },
            {
                'mem_key':'{}_historical'.format(mod_key),
                'time_periods':time_periods_cmip6_hist,
            },
        ],
        'label':mod_key,
    })
#print(mem_cfgs)
#quit()

ref_key = None

mem_groups = {}
mem_groups['COSMO'] = ['COSMO']
mem_groups['CMIP6'] = []
for mod_key in models_cmip6:
    mem_groups['CMIP6'].append(mod_key)

#no_legend_mem_keys = []
no_legend_mem_keys = copy.deepcopy(mem_groups['CMIP6'])
no_legend_mem_keys.remove('MPI-ESM1-2-HR')
#
#### delete specific models
#mod_keys = [
#   'MPI-ESM1-2-HR',
#   #'MPI-ESM1-2-LR',
#   #'NorESM2-LM',
#   #'NorESM2-MM',
#   #'TaiESM1',
#   ##'NESM3',
#   #'MRI-ESM2-0',
#   #'CMCC-CM2-SR5',
#   #'CMCC-ESM2',
#   #'IPSL-CM6A-LR',
#]
#for mod_key in mod_keys:
#    no_legend_mem_keys.remove(get_comb_mem_key(
#            {'diff':[
#                '{}_ssp585'.format(mod_key),
#                '{}_historical'.format(mod_key)]
#            }))

dask_chunks = {'lon':50,'lat':50}

#### plot
nrows = 1
ncols = 1
figsize = (3.1,3)
pval_regression = 0.05

arg_subplots_adjust = {
    'left':0.20,
    'bottom':0.20,
    'right':0.96,
    'top':0.96,
    'wspace':0.10,
    'hspace':0.30,
}
