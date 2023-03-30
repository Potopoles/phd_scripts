
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 004_09_timeline:
author			Christoph Heim
date created    21.11.2020
date changed    23.11.2020
usage			import in another script
"""
###############################################################################
import os, subprocess, sys
import numpy as np
from datetime import datetime, timedelta
from base.nl_global import (plot_glob_base_dir, inp_glob_base_dir,
                               ana_glob_base_dir)
from base.nl_domains import *
from nl_mem_src import *
from nl_var_src import set_up_var_src_dict
from nl_plot_09 import nlp
###############################################################################
## paths
ana_name        = '004_dyamond'
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name, '09_timeline')
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)

## computation
njobs = int(sys.argv[1])

## members
sim_group = 'dya_all'
sim_group = 'dya_main'
#sim_group = 'sensitivity'
#sim_group = 'debug'
#sim_group = 'iav'
sim_src_dict = mem_src[sim_group]
obs_src_dict = mem_src['obs']


i_aggreg = 'none'
i_aggreg = 'daily'
#i_aggreg = 'yearly'
#i_aggreg = 'monthly'
#i_aggreg = 'all'

i_plot_trend_line = False

## run settings
i_save_fig = 0
if len(sys.argv) > 2:
    i_save_fig = int(sys.argv[2])
i_debug = 2
#i_use_obs = 1
i_plot = 1

var_name = 'ALBEDO'
#var_name = 'LWUTOA'
#var_name = 'POTTBL'
#var_name = 'POTTFT'
#var_name = 'QVFT'
#var_name = 'ENTR'
#var_name = 'INVHGT'
var_name = 'SUBS'

obs_key = 'CM_SAF_MSG_AQUA_TERRA'

domain = dom_SEA_Sc
#domain = dom_iav_trades
#domain = dom_iav_ITCZ

#years = np.arange(1983,2019+1)
#years = np.arange(2006,2014+1)
years = [2016]
time_periods = []
for year in years:
    time_periods.append(
        {
            'first_date':    datetime(year,8,1),
            #'first_date':    datetime(year,8,2),
            'last_date':     datetime(year,9,9),
        }
    )


#time_periods = [
#    {
#        'first_date':    datetime(2006,8,6),
#        'last_date':     datetime(2006,12,31),
#    },
#]

### set up var_src
var_src_dict = set_up_var_src_dict(inp_base_dir, ana_base_dir)

#cfg = run_configs[run_mode]
#cfg.update(var_configs[plot_var])
#var_name = plot_var
## update nlp
#nlp['plot_order']  = cfg['plot_order'] 
#nlp['figsize']  = cfg['figsize'] 
#nlp['cmap']     = nlp['cmaps'][cfg['cmap']] 
#nlp['nrows']    = cfg['nrows'] 
#nlp['ncols']    = cfg['ncols'] 
