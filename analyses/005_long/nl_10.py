
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 005_10_csalttime:
author			Christoph Heim
date crated     06.04.2022
date changed    06.04.2022
usage			import in another script
"""
###############################################################################
import os
from datetime import datetime, timedelta
from base.nl_global import (plot_glob_base_dir, inp_glob_base_dir,
                               ana_glob_base_dir)
from base.nl_domains import *
from package.time_processing import Time_Processing as TP
from package.functions import get_comb_mem_key
from nl_mem_src import *
###############################################################################
## paths
ana_name        = '005_long'
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name, '10_csalttime')
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)


ANA_NATIVE_domain = dom_SA_3km_large3
plot_domain = dom_SA_3km_large3
plot_domain = dom_SA_ana
plot_domain = dom_SA_ana_land
plot_domain = dom_SA_ana_sea
#plot_domain = dom_ITCZ
plot_domain = dom_trades_deep
#plot_domain = dom_trades_shallow
#plot_domain = dom_trades


## run settings
i_debug = 2
i_plot = 1
i_skip_missing = 1

start_year = 2006
end_year = 2007
start_month = 8
end_month = 5
start_day = 1
end_day = 31
time_periods = [{
    'first_date':datetime(start_year,start_month,start_day),
    'last_date':datetime(end_year,end_month,end_day)
}]

start_year = 2006
end_year = 2006
start_month = 8
end_month = 8
start_day = 1
end_day = 31
time_periods_aug2006 = [{
    'first_date':datetime(start_year,start_month,start_day),
    'last_date':datetime(end_year,end_month,end_day)
}]


start_year = 2007
end_year = 2007
start_month = 1
end_month = 12
start_day = 1
end_day = 31
time_periods_cmip = [{
    'first_date':datetime(start_year,start_month,start_day),
    'last_date':datetime(end_year,end_month,end_day)
}]


agg_level = TP.HOURLY_SERIES
agg_level = TP.DIURNAL_CYCLE
agg_level = TP.ANNUAL_CYCLE
#agg_level = TP.MONTHLY_SERIES
#agg_level = TP.DAILY_SERIES

agg_operators = [TP.MEAN]

alt_lims = (0,4000)

pickle_append = ''

plot_append = ''
#plot_append = 'diff'
#plot_append = 'change'

#if plot_append == 'diff':
#elif plot_append == 'change':
#else:

mem_cfgs = [
    {
        'mem_key':      'COSMO_3.3_ctrl', 
        #'time_periods': time_periods_aug2006
    },
    {
        'mem_key':      'COSMO_3.3_pgw', 
        #'time_periods': time_periods_aug2006
    },
    #{
    #    'mem_oper':     'diff',
    #    'mem_keys':     ['COSMO_3.3_pgw', 'COSMO_3.3_ctrl'], 
    #    'time_periods': time_periods_aug2006
    #},
    #{
    #    'mem_oper':     'diff',
    #    'mem_keys':     ['COSMO_3.3_pgw_OLD', 'COSMO_3.3_ctrl'], 
    #    'time_periods': time_periods_aug2006
    #},
    #{
    #    'mem_oper':     'diff',
    #    'mem_keys':     ['COSMO_3.3_pgw_300hPa', 'COSMO_3.3_ctrl'], 
    #    'time_periods': time_periods_aug2006
    #},
]


dask_chunks = {'lon':50,'lat':50}

#### plot
nrows = 1
ncols = 2
figsize = (4,3.5)
figsize = (8,3.5)

arg_subplots_adjust = {
    'left':0.18,
    'bottom':0.13,
    'right':0.98,
    'top':0.95,
    'wspace':0.10,
    'hspace':0.30,
}
