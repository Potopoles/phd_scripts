
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 004_08_distr:
author			Christoph Heim
date created    02.10.2020
date changed    02.10.2020
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
from nl_plot_08 import nlp
###############################################################################
## paths
ana_name        = '004_dyamond'
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name, '08_distr')
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)

## computation
njobs = int(sys.argv[1])

obs_src_dict = all_obs

## run settings
i_save_fig = 0
if len(sys.argv) > 2:
    i_save_fig = int(sys.argv[2])
i_debug = 0
i_use_obs = 1
i_plot = 1

first_date = datetime(2016,8,6)
last_date = datetime(2016,9,9)

var_name = 'LCLDDEPTH'

domain = dom_SEA_Sc

use_sims = dyamond_main_sims
#use_sims = debug_sims

### set up var_src
var_src_dict = set_up_var_src_dict(inp_base_dir, ana_base_dir)

