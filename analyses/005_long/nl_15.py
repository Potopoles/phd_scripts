#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 005_04_latlon_sects:
author			Christoph Heim
date created    29.01.2021
date changed    10.07.2022
usage			import in another script
"""
###############################################################################
import os
from datetime import datetime, timedelta
from base.nl_global import (plot_glob_base_dir, inp_glob_base_dir,
                               ana_glob_base_dir)
from package.time_processing import Time_Processing as TP
from base.nl_domains import *
from package.nl_models import models_cmip6, models_cmip6_cldf
from base.nl_time_periods import *
from nl_mem_src import *
###############################################################################
## paths
ana_name        = '005_long'
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name, '15_latlonline')
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)


models_cmip6 = models_cmip6_cldf
#models_cmip6 = models_cmip6_cldf[0:2]
#models_cmip6 = models_cmip6_cldf[2:10]
#models_cmip6 = models_cmip6_cldf[10:]
mem_keys_cmip6_hist = ['{}_historical'.format(model) for model in models_cmip6]
mem_keys_cmip6_scen = ['{}_ssp585'.format(model) for model in models_cmip6]
mem_keys_cmip6_change = []
for model in models_cmip6:
    mem_keys_cmip6_change.append(
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
cmip6_change = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_change,
}
cosmo_change = {
    'mem_oper':     'diff',
    'mem_keys':     ['COSMO_3.3_pgw3', 'COSMO_3.3_ctrl'],
}
mpi_hist = {
    'mem_key':      'MPI-ESM1-2-HR_historical', 
    'time_periods': time_periods_cmip6_hist,
}
mpi_scen = {
    'mem_key':      'MPI-ESM1-2-HR_ssp585', 
    'time_periods': time_periods_cmip6_scen,
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


ANA_NATIVE_domain = dom_SA_3km_large3
plot_domain = dom_SA_ana_merid_cs 
plot_domain = dom_trades_full
#plot_domain = dom_trades_NA

#plot_domain = dom_trades_merid

#plot_domain = dom_trades_east

line_along = 'lat'
line_along = 'lon'

if line_along == 'lat':
    line_at = slice(plot_domain['lon'].start,plot_domain['lon'].stop)
elif line_along == 'lon':
    line_at = slice(plot_domain['lat'].start,plot_domain['lat'].stop)
else:
    raise ValueError()


agg_level = TP.ALL_TIME
#agg_level = TP.ANNUAL_CYCLE
#agg_level = TP.DAILY_SERIES

agg_operators = [TP.MEAN]

time_periods = time_periods_ana
#time_periods = time_periods_2007
#time_periods = get_time_periods_for_month(2007, 8) 
#time_periods = [dict(first_date=datetime(2008,2,27),last_date=datetime(2008,2,27))]
#time_periods = time_periods_ana_JJA
#time_periods = time_periods_ana_SON
#time_periods = time_periods_ana_DJF
#time_periods = time_periods_ana_MAM

#time_periods = time_periods_ana_FMA
#time_periods = time_periods_ana_MJJ
#time_periods = time_periods_ana_ASO
#time_periods = time_periods_ana_NDJ

time_periods = time_periods_ana_JFM
time_periods = time_periods_ana_AMJ
time_periods = time_periods_ana_JAS
#time_periods = time_periods_ana_OND

mem_cfgs = [
    'COSMO_3.3_ctrl', 
    'COSMO_3.3_pgw3', 
    #{
    #    'mem_oper':     'diff',
    #    'mem_keys':     ['COSMO_3.3_pgw3','COSMO_3.3_ctrl'],
    #},
   
    #cmip6_hist,
    #cmip6_scen,

    #{
    #    'mem_key':      '{}_ssp585'.format('CMCC-ESM2'),
    #    'time_periods': time_periods_cmip6_scen,
    #},
    #{
    #    'mem_key':      '{}_historical'.format('CMCC-ESM2'),
    #    'time_periods': time_periods_cmip6_hist,
    #},

    #cmip6_change,
    #mpi_change,
    #cosmo_change
]


plot_dict = {
    #'l1':['QVHDIV@alt=3000'],
    #'r1':['POTTHDIV@alt=100'],
    #'l1':['POTTVDIV@alt=100'],
    #'l1':['T@alt=100'],
    #'l1':['QVXDIV@alt=100'],
    'l1':['dRHdt@alt=100'],
    #'l1':['dRHdt_MBL_FLX@alt=100'],
    #'l1':['SLHFLX'],
    #'l1':['dQVdt_MBL_LH'],
    #'l1':['dTdt_MBL_SH'],
    #'l1':['QVXDIV@alt=100','QVYDIV@alt=100'],
    #'r1':['POTTXDIV@alt=100','POTTYDIV@alt=100'],
    #'l1':['QVHDIV@alt=100'],
    #'l1':['QVVDIV@alt=100'],
    #'r1':['QV@alt=100'],
    #'l1':['CLCL'],
    #'l1':['RH@alt=3000','SST','T@alt=3000','W@alt=3000','UV10M'],
    #'l1':['CRESWNDTOA','DQVINV','LTS'],
    #'l1':['RH@alt=3000','SST','T@alt=3000','W@alt=3000','UV10M','CLCL','CRESWNDTOA','DQVINV','LTS'],
    #'r1':['RH@alt=3000'],
    #'r1':['LCL'],
    #'l1':['EIS','TSURF'],
    #'l1':['CRESWNDTOA'],
    #'l1':['SST'],
    #'l1':['QVVFLX@alt=14000'],
    #'l1':['QV@alt=12000','T@alt=12000'],
    #'l1':['QV@alt=13000','T@alt=13000'],
    #'l1':['QV@alt=14000','T@alt=14000'],
    #'l1':['QV@alt=15000','T@alt=15000'],
    #'l1':['QV@alt=16000','T@alt=16000'],
    #'l1':['QV@alt=15000'],
    #'l1':['QV@alt=13000'],
    #'l1':['LWDTOA','CLWDTOA','ALBEDO'],
    #'l1':['ALBEDO'],
    #'l1':['ENTR'],
    #'r1':['UV10M'],
    #'r1':['T2M','PP'],
    #'r1':['T@alt=300'],
    #'r1':['T@alt=3000'],
    #'l1':['W@alt=3000'],
    #'r1':['LTS','LCL','INVHGT','INVSTRV'],
    #'l1':['INVHGT'],
    #'r1':['DINVHGTLCL','DINVHGTLOWCLDBASE'],
    #'r1':['LTS'],
    #'r1':['SSHFLX','SLHFLX','UV10M'],
    #'r1':['QVWFLXINV'],
    #'r1':['QV@alt=20'],
    #'r1':['QVSATDEF@alt=20'],

    #'r1':['QVVDIV3@alt=0:3000'],
    #'r1':['QVHDIV3@alt=0:3000','QVVDIV3@alt=0:3000'],
    #'r2':['CLDF@alt=10000:15000'],
    #'r1':['QVSATDEF@alt=20'],
    #'r1':['PP'],

    #'r1':['WVPHCONV','PP'],
    #'r1':['IWPHCONV'],
    #'r1':['QVWFLX@alt=8000'],
    #'r1':['QVWFLX@alt=5000'],
}


coarse_grain = {
    'W':200,
    'ENTR':200,
    'ENTRH':200,
    'ENTRV':200,
    'ENTRSCL':200,
    'ENTRHSCL':200,
    'ENTRVSCL':200,
    'IWPHCONV':200,
    'BUOYIFLX':200,
    'LOWCLDBASE':200,
    'DINVHGTLCL':200,
    'DINVHGTLOWCLDBASE':200,
    'INVHGT':200,
    'ENTRDRY':200,
    'PP':200,
    'DQVINV':200,
    'POTTHDIV3':200,
    'INVSTRV':200,
    'QVHDIV':200,
    'QVXDIV':200,
    'QVYDIV':200,
    'QVVDIV':200,
    'QV':200,
    'POTTHDIV':200,
    'POTTVDIV':200,
    'POTTXDIV':200,
    'POTTYDIV':200,
    'T':200,
    'dRHdt':200,
    'dRHdt_MBL_FLX':200,
    'dQVdt_MBL_LH':200,
    'dTdt_MBL_SH':200,
}

dask_chunks = {'lon':50,'lat':50}

## run settings
i_debug = 2
i_plot = 1
i_skip_missing = 1

# plotting settings
i_force_axis_limits = 1

## analysis members
sim_group = 'ctrl'

#### plot
nrows = 1
ncols = 1
figsize = (6,4)

i_plot_legend = 0
title = None

arg_subplots_adjust = {
    'left':0.11,
    'bottom':0.15,
    'right':0.75,
    'top':0.93,
    'wspace':0.10,
    'hspace':0.30,
}
colorbar_pos = [0.20, 0.12, 0.73, 0.03]
