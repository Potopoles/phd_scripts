
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 005_18:
author			Christoph Heim
date created    31.05.2022
date changed    31.05.2022
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
from package.nl_models import models_cmip6
###############################################################################
## paths
ana_name        = '005_long'
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name, '18_mean')
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)


ANA_NATIVE_domain = dom_SA_3km_large3
plot_domain = dom_SA_ana_sea # unused here

main_domain = dom_ITCZ
main_domain = dom_SA_ana_sea

overwrite_var_dom_map = {
    'PP':           main_domain,
    'T@alt=1000':   main_domain,

    #'T@alt=3000':   main_domain,
    #'T2M':          main_domain,
}

diff_mem_key = '|diff|COSMO_3.3_pgw3#time#20070101-20101231-gap0#+++#COSMO_3.3_ctrl#time#20070101-20101231-gap0|enddiff|'
rel_mem_key = '|rel0.01|COSMO_3.3_pgw3#time#20070101-20101231-gap0#+++#COSMO_3.3_ctrl#time#20070101-20101231-gap0|endrel0.01|'

#diff_mem_key = '#diff#MPI-ESM1-2-HR_ssp585#time#20700101-20991231-gap0#+++#MPI-ESM1-2-HR_historical#time#19850101-20141231-gap0#enddiff#'
#rel_mem_key = '#rel0.01#MPI-ESM1-2-HR_ssp585#time#20700101-20991231-gap0#+++#MPI-ESM1-2-HR_historical#time#19850101-20141231-gap0#endrel0.01#'

diff_var_name = 'T@alt=3000'
diff_var_name = 'T@alt=1000'
#diff_var_name = 'T2M'
rel_var_name = 'PP'

## run settings
i_debug = 2
i_plot = 1
i_skip_missing = 1

agg_level = TP.ALL_TIME
#agg_level = TP.YEARLY_SERIES
#agg_level = TP.MONTHLY_SERIES

agg_operators = [TP.MEAN]

pickle_append = ''
plot_append = ''

time_periods = time_periods_ana
#time_periods = time_periods_2007
#time_periods = get_time_periods_for_month(2007, 2) # lowest LWDTOA feedback

#models_cmip6 = models_cmip6[:3]

mem_cfgs = [
    {
        'mem_oper': 'diff',
        'mem_keys': ['COSMO_3.3_pgw3', 'COSMO_3.3_ctrl'],
    },
    {
        'mem_oper': 'rel0.01',
        'mem_keys': ['COSMO_3.3_pgw3', 'COSMO_3.3_ctrl'],
    },
    #'COSMO_3.3_pgw3'

    #{
    #    'mem_oper': 'diff',
    #    'mem_keys': [
    #        {
    #            'mem_key':      'MPI-ESM1-2-HR_ssp585',
    #            'time_periods': time_periods_cmip_ssp585,
    #        },
    #        {
    #            'mem_key':      'MPI-ESM1-2-HR_historical',
    #            'time_periods': time_periods_cmip_historical,
    #        },
    #    ],
    #},
    #{
    #    'mem_oper': 'rel0.01',
    #    'mem_keys': [
    #        {
    #            'mem_key':      'MPI-ESM1-2-HR_ssp585',
    #            'time_periods': time_periods_cmip_ssp585,
    #        },
    #        {
    #            'mem_key':      'MPI-ESM1-2-HR_historical',
    #            'time_periods': time_periods_cmip_historical,
    #        },
    #    ],
    #},
]


dask_chunks = {'lon':50,'lat':50}

#### plot
nrows = 1
ncols = 1
#figsize = (3.5,3)
figsize = (7,3)
pval_regression = 0.05

arg_subplots_adjust = {
    'left':0.15,
    'bottom':0.20,
    'right':0.98,
    'top':0.90,
    'wspace':0.10,
    'hspace':0.30,
}
