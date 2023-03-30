#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 004_00_pp_obs:
author			Christoph Heim
date created    10.02.2020
date changed    04.07.2022
usage			import in another script
"""
###############################################################################
import os, subprocess, sys, argparse
from datetime import datetime, timedelta
from base.nl_global import (inp_glob_base_dir, ana_glob_base_dir)
from base.nl_domains import *
###############################################################################
## input arguments
parser = argparse.ArgumentParser(description = 'Preprocess observational data.')
# variable to plot
parser.add_argument('var_name', type=str)
# number of parallel processes
parser.add_argument('-p', '--n_par', type=int, default=1)
args = parser.parse_args()


## paths
inp_base_dir    = inp_glob_base_dir

year = 2006
month = 12
last_day = 13
time_periods = [
    {
        #'first_date':    datetime(year,1,1),
        #'first_date':    datetime(year,8,1),
        #'last_date':     datetime(year,8,31),

        'first_date':    datetime(2004,2,1),
        'last_date':     datetime(2011,1,31),
        #'first_date':    datetime(2009,12,1),
        #'last_date':     datetime(2009,12,31),

        'first_date':    datetime(2016,8,1),
        'last_date':     datetime(2016,8,20),

        #'first_date':    datetime(year,month,1),
        #'last_date':     datetime(year,month,last_day),
    },
]
#domain = dom_SEA_Sc
domain = dom_trades
domain = dom_SA_3km_large3
#domain = dom_SA_ana

## observations
use_obs = {
    'LWUTOA':{
        'obs':'CM_SAF_MSG_AQUA_TERRA',
        #'obs_dir':'/net/o3/hymet_nobackup/heimc/data/input/CM_SAF_MSG_AQUA_TERRA',
        #'raw_dir':'/net/o3/hymet_nobackup/heimc/data/input/CM_SAF_MSG_AQUA_TERRA/raw_data/LWUTOA',
        'obs_dir':'/net/o3/hymet_nobackup/heimc/data/input/CM_SAF_MSG_AQUA_TERRA',
        'raw_dir':'/net/o3/hymet_nobackup/heimc/data/input/CM_SAF_MSG_AQUA_TERRA/MSG/dom_meteosat_disk/monthly/raw_data/LWUTOA/data'
    },
    'SWUTOA':{
        'obs':'CM_SAF_MSG_AQUA_TERRA',
        #'obs_dir':'/net/o3/hymet_nobackup/heimc/data/input/CM_SAF_MSG_AQUA_TERRA',
        #'raw_dir':'/net/o3/hymet_nobackup/heimc/data/input/CM_SAF_MSG_AQUA_TERRA/raw_data/SWUTOA',
        'obs_dir':'/net/o3/hymet_nobackup/heimc/data/input/CM_SAF_MSG_AQUA_TERRA',
        'raw_dir':'/net/o3/hymet_nobackup/heimc/data/input/CM_SAF_MSG_AQUA_TERRA/MSG/dom_meteosat_disk/monthly/raw_data/SWUTOA/data'
    },
    'SWDTOA':{
        #'obs':'COSMO_3.3',
        #'obs_dir':'/net/o3/hymet_nobackup/heimc/data/input/CM_SAF_MSG_AQUA_TERRA',
        #'raw_dir':'/net/o3/hymet_nobackup/heimc/data/input/COSMO_3.3/SA_3_ctrl/dom_native/daily/SWDTOA',
        'obs':'COSMO_4.4',
        'obs_dir':'/net/o3/hymet_nobackup/heimc/data/input/CM_SAF_MSG_AQUA_TERRA',
        'raw_dir':'/net/o3/hymet_nobackup/heimc/data/input/COSMO_4.4/test_01/dom_native/daily/SWDTOA',

        #'obs':'CERES_EBAF',
        #'obs_dir':'/net/o3/hymet_nobackup/heimc/data/input/CM_SAF_MSG_AQUA_TERRA',
        #'raw_dir':'/net/o3/hymet_nobackup/heimc/data/input/CERES_EBAF/ed4_1/SA/monthly/SWDTOA',
    },
    'CLDMASK':{
        'obs':'DARDAR_CLOUD',
        'obs_dir':'/net/o3/hymet_nobackup/heimc/data/input/DARDAR_CLOUD',
        'raw_dir':'/net/n2o/wolke_scratch/nedavid/DARDAR_CLOUD/',
    },
    'T':{
        'obs':'DARDAR_CLOUD',
        'obs_dir':'/net/o3/hymet_nobackup/heimc/data/input/DARDAR_CLOUD',
        'raw_dir':'/net/n2o/wolke_scratch/nedavid/DARDAR_CLOUD/',
    },
    'CORREFL':{
        'obs':'SUOMI_NPP_VIIRS',
    },
    #'T':{
    #    'obs':'RADIO_SOUNDING',
    #},
    'RH':{
        'obs':'RADIO_SOUNDING',
    },
    'PP':{
        'obs':'CMORPH',
        'obs_dir':'/net/o3/hymet_nobackup/heimc/data/input/CMORPH/daily/SA/daily/PP',
        'raw_dir':'/net/o3/hymet_nobackup/heimc/data/input/CMORPH/raw_data/daily/www.ncei.noaa.gov/data/cmorph-high-resolution-global-precipitation-estimates/access/daily/0.25deg',
    },
}

