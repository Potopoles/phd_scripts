
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 005_17:
author			Christoph Heim
date created    04.03.2022
date changed    08.03.2022
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
from package.functions import get_comb_mem_key
from nl_mem_src import *
from package.nl_models import models_cmip6, models_cmip6_cldf
###############################################################################
## paths
ana_name        = '005_long'
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name, '17_crf')
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)


ANA_NATIVE_domain = dom_SA_3km_large3
plot_domain = dom_SA_ana_sea # unused here

main_domain = dom_SA_ana_sea
#main_domain = dom_SA_ana_land
#main_domain = dom_SA_ana
#main_domain = dom_trades_east
#main_domain = dom_trades_west
#main_domain = dom_trades_full

overwrite_var_dom_map = {
    'CRERADNDTOA'   :main_domain,
    'CRESWNDTOA'    :main_domain,
    'CRELWDTOA'     :main_domain,
    'CSWNDTOA'      :main_domain,
    'CLWDTOA'       :main_domain,
    'CRADNDTOA'     :main_domain,
    'SWNDTOA'       :main_domain,
    'LWDTOA'        :main_domain,
    'RADNDTOA'      :main_domain,
    'T2M'           :dom_global,
}

scale_var_name = None # for computation (although for i_recompute=1 it is automatically removed)
scale_var_name = 'T2M'

## run settings
i_debug = 1
i_plot = 1
i_skip_missing = 1

agg_level = TP.ALL_TIME
agg_level = TP.YEARLY_SERIES
#agg_level = TP.MONTHLY_SERIES

agg_operators = [TP.MEAN]

pickle_append = ''
plot_append = ''

#time_periods = time_periods_2007
time_periods = time_periods_ana
#start_date = datetime(2006,8,1)
#end_date = datetime(2006,8,31)
#time_periods = [{
#    'first_date':start_date,
#    'last_date':end_date
#}]

#models_cmip6 = models_cmip6[:3]

var_group_cfg = {
    'SWNDTOA':'all-sky',
    'CSWNDTOA':'clear-sky',
    'CRESWNDTOA':'CRE',
}

line_mem_cfg = {
    'COSMO_3.3': {
        'color':    'red',
        'label':    'COSMO',
        'yearly':   True,
    },
    'MPI-ESM1-2-HR': {
        'color':    'green',
        'label':    'MPI-ESM1-2-HR',
        'yearly':   False,
    },
}

mem_cfgs = [
    #'COSMO_3.3_pgw3'
    {
        'mem_oper': 'diff',
        'mem_keys': ['COSMO_3.3_pgw3', 'COSMO_3.3_ctrl'],
        'label':    'COSMO',
    },
]

#models_cmip6 = ['MPI-ESM1-2-HR']
#models_cmip6 = models_cmip6[0:15]
#models_cmip6 = models_cmip6[15:]

models_cmip6 = models_cmip6_cldf
for mod_key in models_cmip6:
    pass
    mem_cfgs.append(
        {
            'mem_oper': 'diff',
            'mem_keys': [
                {
                    'mem_key':      '{}_ssp585'.format(mod_key),
                    'time_periods': time_periods_cmip6_scen,
                },
                {
                    'mem_key':      '{}_historical'.format(mod_key),
                    'time_periods': time_periods_cmip6_hist,
                },
            ],
        }
    )


ref_key = None

dask_chunks = {'lon':50,'lat':50}

#### plot
nrows = 1
ncols = 1
#figsize = (3.5,3)
figsize = (7,3)
pval_regression = 0.05

arg_subplots_adjust = {
    'left':0.10,
    'bottom':0.10,
    'right':0.98,
    'top':0.95,
    'wspace':0.10,
    'hspace':0.30,
}
