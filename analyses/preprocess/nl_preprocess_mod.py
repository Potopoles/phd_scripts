#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for preprocess_mod
author			Christoph Heim
date created    02.12.2020
date changed    26.04.2022
usage			import in another script
"""
###############################################################################
import os, subprocess, sys, argparse
from datetime import datetime, timedelta
from base.nl_global import (plot_glob_base_dir, inp_glob_base_dir,
                               ana_glob_base_dir)
from nl_mem_src import *
from nl_var_src import set_up_var_src_dict, set_up_mean_var_src_dict
from base.nl_domains import *
from package.nl_models import models_cmip6
###############################################################################
## input arguments
parser = argparse.ArgumentParser(description = 'Preprocess observational data.')
# var_name
parser.add_argument('var_name', type=str)
# number of parallel processes
parser.add_argument('-p', '--n_par', type=int, default=1)
# cmip6 scenario
parser.add_argument('-m', '--mem_key', type=str, default=None)
args = parser.parse_args()

base_dir_cmip6 = os.path.join('/net','atmos','data','cmip6')

ANA_NATIVE_domain = dom_SA_3km_large3

## paths
#ana_name        = '004_dyamond'
ana_name        = '005_long'
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)


mem_key = 'IFS_9' # P,ALT
mem_key = 'IFS_4' # P,ALT
mem_key = 'ARPEGE-NH_2.5' # P  # at most 2 parallel tasks
mem_key = 'ERA5' # P,ALT
#mem_key = 'FV3_3.25' # P, ALT (for full levels)
#mem_key = 'CERES_EBAF' # 


if args.mem_key is not None:
    mem_key = args.mem_key

var_name = args.var_name

domain = dom_SA_3km_large3 

i_compute = 1
i_compress = 1


start_year = 2006
end_year = 2006
if 'hist' in mem_key:
    start_year = 1985
    end_year = 2014
elif ('ssp585' in mem_key) or ('ssp245' in mem_key):
    start_year = 2070
    end_year = 2099

first_date = datetime(start_year,1,1)
last_date = datetime(end_year,12,31)

first_date = datetime(1985,1,1)
last_date = datetime(2014,12,31)

first_date = datetime(2070,1,1)
last_date = datetime(2099,12,31)
#
#first_date = datetime(2011,1,1)
#last_date = datetime(2014,12,31)

#first_date = datetime(2006,8,1)
#last_date = datetime(2006,12,31)
#first_date = datetime(2006,8,1)
#last_date = datetime(2009,12,31)

amon = 'Amon'
emon = 'Emon'
cmip6_var_src = {
    'CLDF':     amon,
    'U':        amon,
    'V':        amon,
    'W':        amon,
    'ALT':      amon,
    'T':        amon,
    #'QV':       emon,
    'QV':       amon,
    'RH':       amon,
    'PP':       amon,
    'SLHFLX':   amon,
    'T2M':      amon,
    'LWUTOA':   amon,
    'CLWUTOA':  amon,
    'SWDTOA':   amon,
    'TSURF':    amon,
}


i_debug = 2

### set up mem_src_dict
mem_dict = mem_src[mem_key]

### set up var_src
var_src_dict = set_up_var_src_dict(inp_base_dir, ana_base_dir,
                                    ANA_NATIVE_domain)
mean_var_src_dict = set_up_mean_var_src_dict(inp_base_dir, ana_base_dir,
                                    ANA_NATIVE_domain)

