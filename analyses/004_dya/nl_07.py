#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 004_07_reynolds:
author			Christoph Heim
date created    02.09.2020
date changed    16.12.2020
usage			import in another script
"""
###############################################################################
import os, subprocess, sys
from datetime import datetime, timedelta
from base.nl_global import (plot_glob_base_dir, inp_glob_base_dir,
                               ana_glob_base_dir)
from base.nl_domains import *
from nl_mem_src import *
from nl_var_src import set_up_var_src_dict
###############################################################################
## paths
ana_name        = '004_dyamond'
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)

## computation
njobs = 1
if len(sys.argv) > 1:
    njobs = int(sys.argv[1])

## analysis members
obs_src_dict = mem_src['obs']
sim_group = 'dya_all'
sim_group = 'dya_main'
#sim_group = 'cosmo'
#sim_group = 'sensitivity'
#sim_group = 'debug'
#sim_group = 'iav'
sim_src_dict = mem_src[sim_group]

#mem_key = 'IFS_9'
##mem_key = 'GEOS_3'
#mem_key = 'COSMO_12'
#sim_src_dict = {mem_key:sim_src_dict[mem_key]}
#print(sim_src_dict)
#quit()

if len(sys.argv) > 2:
    use_sim_key = sys.argv[2]
    sim_src_dict = {use_sim_key:sim_src_dict[use_sim_key]}

i_debug     = 3
i_compress  = 2

### time
#first_date = datetime(2016,8,4)
first_date = datetime(2016,8,6)
last_date = datetime(2016,9,9)
#first_date = datetime(2016,8,1)
#last_date = datetime(2016,8,31)

#first_date = datetime(2016,8,22)
#last_date = datetime(2016,8,24)


domain = dom_SEA_Sc
#domain = dom_SEA_Sc_low
#domain = dom_SEA_Sc_high
#domain = dom_test

### set up var_src
var_src_dict = set_up_var_src_dict(inp_base_dir, ana_base_dir)

