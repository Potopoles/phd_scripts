#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 004_00_compute_fields:
author			Christoph Heim
date created    18.02.2020
date changed    30.05.2022
usage			import in another script
"""
###############################################################################
import os, subprocess, sys, warnings, argparse
from datetime import datetime, timedelta
from base.nl_global import (plot_glob_base_dir, inp_glob_base_dir,
                               ana_glob_base_dir)
from base.nl_domains import *
from base.nl_time_periods import *
from nl_mem_src import *
from nl_var_src import set_up_var_src_dict, set_up_mean_var_src_dict
###############################################################################
## input arguments
parser = argparse.ArgumentParser(description = 'Derive atmospheric variable based on other variables.')
# variable to plot
parser.add_argument('var_name', type=str)
# member to compute
parser.add_argument('mem_key', type=str)
# number of parallel processes
parser.add_argument('-p', '--n_par', type=int, default=1)
args = parser.parse_args()
print(args)
#quit()

## paths
ana_name        = '005_long'
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)




####
i_debug     = 2
# do computation step
i_compute   = 1
# do compression step
i_compress  = 2

time_periods = time_periods_ana
#time_periods = time_periods_2006
time_periods = time_periods_2007
#time_periods = time_periods_2008
#time_periods = time_periods_2009
#time_periods = time_periods_2010
#time_periods = get_time_periods_for_month(2008,2)
#time_periods = time_periods_ana_JJA
#time_periods = time_periods_ana_SON
#time_periods = time_periods_ana_DJF
#time_periods = time_periods_ana_MAM
#time_periods = time_periods_cmip6_hist

time_periods = [{
    'first_date':datetime(2008,1,2),
    'last_date':datetime(2008,1,10)
}]
#
#time_periods = [{
#    'first_date':datetime(2008,2,28),
#    'last_date':datetime(2008,2,28)
#}]

time_mode = 'daily'
#time_mode = 'tmean'


#ANA_NATIVE_domain = dom_trades_shallow
#ANA_NATIVE_domain = dom_SA_ana
ANA_NATIVE_domain = dom_SA_3km_large3
domain = dom_SA_3km_large3
#domain = dom_trades_full
#domain = dom_ERA5_gulf
#domain = dom_ITCZ_feedback


### set up var_src
var_src_dict = set_up_var_src_dict(inp_base_dir, ana_base_dir,
                                    ANA_NATIVE_domain)
mean_var_src_dict = set_up_mean_var_src_dict(inp_base_dir, ana_base_dir,
                                    ANA_NATIVE_domain)
