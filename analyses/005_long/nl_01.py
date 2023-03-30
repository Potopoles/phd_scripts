#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 005_01:
author			Christoph Heim
date created    18.11.2019
date changed    31.03.2022
usage			import in another script
"""
###############################################################################
import os
from datetime import datetime, timedelta
from base.nl_global import (plot_glob_base_dir, inp_glob_base_dir,
                               ana_glob_base_dir)
from base.nl_domains import *
from base.nl_time_periods import *
from package.time_processing import Time_Processing as TP
from package.nl_models import models_cmip6, models_cmip6_cldf
from nl_mem_src import *
from nl_plot_01 import nlp
from ana_nls.glob_cfgs import (
    cmip6_change,
    cmip6_change_FMA,
    cmip6_change_MJJ,
    cmip6_change_ASO,
    cmip6_change_NDJ,
    
    mpi_change,
    mpi_change_FMA,
    mpi_change_MJJ,
    mpi_change_ASO,
    mpi_change_NDJ,
)
###############################################################################

## paths
ana_name        = '005_long'
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name, '01_spatial')
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)

ANA_NATIVE_domain = dom_SA_3km_large3
#plot_domain = dom_gulf_2
#plot_domain = dom_SA_3km_large3
plot_domain = dom_SA_ana
#plot_domain = dom_SA_ana_sea
#plot_domain = dom_SA_ana_land
#plot_domain = dom_SA_ana_sea_2
#plot_domain = dom_macronesia

#plot_domain = dom_ITCZ
#plot_domain = dom_ITCZ_feedback
#plot_domain = dom_trades_deep
#plot_domain = dom_trades_shallow
#plot_domain = dom_trades

#plot_domain = dom_trades_east
#plot_domain = dom_trades_west
#plot_domain = dom_trades_full

#plot_domain = dom_SA_ana_merid_cs

#plot_domain = dom_tuning

## run settings
i_debug = 1
i_plot = 1
i_skip_missing = 1
i_coarse_grain = 0
#i_coarse_grain = 50
#i_coarse_grain = 100


#agg_level = TP.NONE
agg_level = TP.ALL_TIME
#agg_level = TP.DIURNAL_CYCLE
#agg_level = TP.ANNUAL_CYCLE
#agg_level = TP.SEASONAL_CYCLE
#agg_level = TP.MONTHLY_SERIES

agg_operators = [TP.MEAN]

pickle_append = ''
#pickle_append = 'cg50'
#pickle_append = 'cg100'

plot_append = ''

time_periods = time_periods_ana
#time_periods = get_time_periods_for_month(2007, 8) # highest LDWTOA feedback
#time_periods = get_time_periods_for_month(2010, 5) # highest LDWTOA feedback
#time_periods = get_time_periods_for_month(2008, 2) # lowest LWDTOA feedback
#time_periods = get_time_periods_for_month(None, 5) # highest LDWTOA feedback
#time_periods = get_time_periods_for_month(None, 2) # lowest LWDTOA feedback
#time_periods = get_time_periods_for_month(None, 2)
time_periods = time_periods_2007
#time_periods = time_periods_ceres_ebaf
#time_periods = time_periods_ana_DJF
#time_periods = time_periods_ana_MAM
#time_periods = time_periods_ana_JJA
#time_periods = time_periods_ana_SON

#time_periods = time_periods_ana_FMA
#time_periods = time_periods_ana_MJJ
#time_periods = time_periods_ana_ASO
#time_periods = time_periods_ana_NDJ

#time_periods = time_periods_ana_JFM
#time_periods = time_periods_ana_AMJ
#time_periods = time_periods_ana_JAS
#time_periods = time_periods_ana_OND

#time_periods = time_periods_ana_DJF

#time_periods = time_periods_tuning
#time_periods = get_time_periods_for_month(2006, 8)

#start_date = datetime(2007,8,1)
#end_date = datetime(2007,8,31)
#time_periods = [{
#    'first_date':start_date,
#    'last_date':end_date
#}]



models_cmip6 = models_cmip6_cldf#[2:]
mem_keys_cmip6_hist = ['{}_historical'.format(model) for model in models_cmip6]
mem_keys_cmip6_scen = ['{}_ssp585'.format(model) for model in models_cmip6]

obs_key = 'ERA5'
#obs_key = 'GPM_IMERG'
#obs_key = 'CM_SAF_MSG_AQUA_TERRA'
obs_key = 'CERES_EBAF'

mem_cfgs = [

    #cmip6_change_FMA,
    #cmip6_change_MJJ,
    #cmip6_change_ASO,
    #cmip6_change_NDJ

    #'COSMO_4.4_test_01',
    #'CM_SAF_MSG_AQUA_TERRA_DAILY',

    'COSMO_3.3_ctrl',
    'COSMO_3.3_pgw3',
    {
        'mem_oper':     'diff',
        'mem_keys':     ['COSMO_3.3_pgw3', 'COSMO_3.3_ctrl'], 
        'label':        'PGW3$-$CTRL',
    },
    #{
    #    'mem_oper':     'bias',
    #    'mem_keys':     ['COSMO_3.3_pgw3', 'COSMO_3.3_pgw'], 
    #    'label':        'PGW3$-$PGW',
    #},


    #mpi_change,
    #mpi_change_FMA,
    #mpi_change_MJJ,
    #mpi_change_ASO,
    #mpi_change_NDJ,
    #{
    #    'mem_oper':     'diff',
    #    'mem_keys':     [
    #        {
    #            'time_periods': time_periods_cmip6_scen,
    #            'mem_key': 'MPI-ESM1-2-HR_ssp585',
    #        },
    #        {
    #            'time_periods': time_periods_cmip6_hist,
    #            'mem_key': 'MPI-ESM1-2-HR_historical',
    #        },
    #    ],
    #    'label':        'MPI-ESM1-2HR SCEN$-$HIST',
    #},

    #{
    #    'mem_oper':     'diff',
    #    'mem_keys':     ['COSMO_3.3_itcz_pgw', 'COSMO_3.3_ctrl'], 
    #    'label':        'PGW ITCZ$-$CTRL',
    #},
    #{
    #    'mem_oper':     'diff',
    #    'mem_keys':     ['COSMO_3.3_pgw2', 'COSMO_3.3_ctrl'], 
    #    'label':        'PGW2$-$CTRL',
    #},
    #{
    #    'mem_oper':     'diff',
    #    'mem_keys':     ['COSMO_3.3_itcz_pgw', 'COSMO_3.3_pgw'], 
    #    'label':        'PGW ITCZ$-$PGW',
    #},
    #{
    #    'mem_oper':     'diff',
    #    'mem_keys':     ['COSMO_3.3_pgw2', 'COSMO_3.3_pgw'], 
    #    'label':        'PGW2$-$PGW',
    #},
    #{
    #    'mem_oper':     'diff',
    #    'mem_keys':     ['COSMO_3.3_pgw3', 'COSMO_3.3_pgw2'], 
    #    'label':        'PGW3$-$PGW2',
    #},

    #'COSMO_3.3_ctrl',
    ##'ERA5',
    #'COSMO_3.3_pgw',
    #{
    #    'mem_oper':     'diff',
    #    'mem_keys':     ['COSMO_3.3_pgw', 'COSMO_3.3_ctrl'], 
    #},


    #{
    #    'time_periods': time_periods_cmip6_hist,
    #    'mem_key': 'MPI-ESM1-2-HR_historical',
    #},
    #{
    #    'time_periods': time_periods_cmip6_scen,
    #    'mem_key': 'MPI-ESM1-2-HR_ssp585',
    #},

    #{
    #    'mem_oper':     'bias',
    #    'mem_keys':     [
    #        {
    #            'mem_oper':     'diff',
    #            'mem_keys':     ['COSMO_3.3_pgw', 'COSMO_3.3_ctrl'], 
    #        },
    #        {
    #            'mem_oper':     'diff',
    #            'mem_keys':     [
    #                {
    #                    'time_periods': time_periods_cmip6_scen,
    #                    'mem_key': 'MPI-ESM1-2-HR_ssp585',
    #                },
    #                {
    #                    'time_periods': time_periods_cmip6_hist,
    #                    'mem_key': 'MPI-ESM1-2-HR_historical',
    #                },
    #            ],
    #        },
    #    ],
    #    'label':        '(PGW$-$CTRL)$-$(SCEN$-$HIST)',
    #},



    #{
    #    'mem_oper':     'diff',
    #    'mem_keys':     [
    #        {
    #            'mem_oper':     'mean',
    #            'mem_keys':     mem_keys_cmip6_scen,
    #            'time_periods': time_periods_cmip6_scen,
    #        },
    #        {
    #            'mem_oper':     'mean',
    #            'mem_keys':     mem_keys_cmip6_hist,
    #            'time_periods': time_periods_cmip6_hist,
    #        },
    #    ], 
    #    'label':        'CMIP6 SSP5-8.5 - HIST'
    #},





    #{
    #    'time_periods': time_periods_cmip_historical,
    #    'mem_key': 'E3SM-1-1_historical',
    #},
    #{
    #    'time_periods': time_periods_cmip_ssp585,
    #    'mem_key': 'E3SM-1-1_ssp585',
    #},

    #obs_key,
    #{
    #    'mem_oper':     'diff',
    #    'mem_keys':     ['COSMO_3.3_ctrl', obs_key], 
    #},
    #'COSMO_3.3_pgw',
    #'ERA5',
    #'COSMO_3.3_pgw_Amon',
    #{
    #    'mem_oper':     'diff',
    #    'mem_keys':     ['COSMO_3.3_pgw_Amon', 'COSMO_3.3_ctrl'], 
    #},
    #{
    #    'mem_oper':     'bias',
    #    'mem_keys':     ['COSMO_3.3_ctrl', 'ERA5'], 
    #},
    #{
    #    'mem_oper':     'bias',
    #    'mem_keys':     ['COSMO_3.3_ctrl', 'CM_SAF_MSG_AQUA_TERRA'], 
    #},

    #{
    #    'mem_oper':     'mean',
    #    'mem_keys':     mem_keys_cmip6_historical,
    #    'time_periods': time_periods_cmip_historical,
    #    'label':        'CMIP6'
    #},
    #{
    #    'mem_oper':     'mean',
    #    'mem_keys':     mem_keys_cmip6_ssp585,
    #    'time_periods': time_periods_cmip_ssp585,
    #    'label':        'CMIP6'
    #},
    #{
    #    'mem_oper':     'diff',
    #    'mem_keys':     [
    #        {
    #            'mem_oper':     'mean',
    #            'mem_keys':     mem_keys_cmip6_historical,
    #            'time_periods': time_periods_cmip_historical,
    #            'label':        'CMIP6'
    #        },
    #        {
    #            'time_periods': time_periods_gpm,
    #            'mem_key': obs_key,
    #        },
    #    ], 
    #},

    #'COSMO_3.3_ctrl',
    #'COSMO_3.3_ctrl_rdheight2',
    #{
    #    'mem_oper':     'diff',
    #    'mem_keys':     ['COSMO_3.3_pgw', 'COSMO_3.3_ctrl'], 
    #},
    #{
    #    'mem_oper':     'diff',
    #    'mem_keys':     ['COSMO_3.3_pgw_OLD', 'COSMO_3.3_ctrl'], 
    #},
    ##{
    ##    'mem_oper':     'diff',
    ##    'mem_keys':     ['COSMO_3.3_pgw_300hPa', 'COSMO_3.3_ctrl'], 
    ##},
    #{
    #    'mem_oper':     'diff',
    #    'mem_keys':     ['COSMO_3.3_pgw_rdheight2', 'COSMO_3.3_ctrl_rdheight2'], 
    #},
]


dask_chunks = {'lon':50,'lat':50}

#### plot
nrows = 2
ncols = 3
figsize = (14,6)

#nrows = 3
#ncols = 3
#figsize = (14,9)

nrows = 1
ncols = 3
figsize = (14,3)

#nrows = 1
#ncols = 2
#figsize = (10,5)

#nrows = 1
#ncols = 4
#figsize = (18,3)

#nrows = 2
#ncols = 4
#figsize = (18,6)

#nrows = 3
#ncols = 4
#figsize = (18,9)
#
#nrows = 1
#ncols = 1
#figsize = (4,3)

i_plot_cbar = 1
pan_cbar_pos = 'center right'
pan_cbar_pad = -1
#pan_cbar_pos = 'lower center'
#pan_cbar_pad = -5
cbar_label_mode = 'both'
#cbar_label_mode = 'var_units'
#cbar_label_mode = 'var_name'
#cbar_label_mode = 'neither'

add_bias_labels = 1

plot_glob_cbar = 0

arg_subplots_adjust = nlp['subplts_cfgs']['{}x{}'.format(nrows,ncols)]
glob_cbar_pos = [0.20, 0.12, 0.73, 0.03]

title = None # take automatic title
#title = '' # manually set title
