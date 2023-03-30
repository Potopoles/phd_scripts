#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 005_04:
author			Christoph Heim
date created    29.01.2021
date changed    01.06.2022
usage			import in another script
"""
###############################################################################
import os
from datetime import datetime, timedelta
from base.nl_global import (plot_glob_base_dir, inp_glob_base_dir,
                               ana_glob_base_dir)
from package.time_processing import Time_Processing as TP
from base.nl_domains import *
from base.nl_time_periods import *
from nl_mem_src import *
from nl_var_src import set_up_var_src_dict
from package.nl_models import models_cmip6, models_cmip6_cldf
from ana_nls.glob_cfgs import *
###############################################################################
## paths
ana_name        = '005_long'
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name, '04_cross_sects')
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)


ANA_NATIVE_domain = dom_SA_3km_large3
#plot_domain = dom_SA_ana_sea
#plot_domain = dom_SA_ana_land
#plot_domain = dom_trades_shallow
#plot_domain = dom_trades_deep
#plot_domain = dom_ITCZ
#plot_domain = dom_trades_extended

plot_domain = dom_SA_ana_merid_cs_afr
plot_domain = dom_SA_ana_merid_cs
#plot_domain = dom_SA_ana_merid_cs_2
#plot_domain = dom_trades_full
#plot_domain = dom_trades_NA
#plot_domain = dom_trades_merid

#line_at = plot_domain['lat']
#line_at = (0,1)
#line_at = slice(-25,-20)

line_along = 'lat'
#line_at = slice(plot_domain['lon'].start+1,plot_domain['lon'].stop-1)
line_at = None

#line_along = 'lon'
#line_at = None

# not implemented anymore
#min_dlonlat = 5

norm_inv = 0

## run settings
i_debug = 1
i_plot = 1
i_skip_missing = 1

# plotting settings
i_force_axis_limits = 1
i_show_title = 1

if plot_domain['key'] in ['dom_trades_deep','dom_trades_shallow','dom_trades','dom_trades_full','dom_trades_extended']:
    alt_lims = (0,4000) 
elif plot_domain['key'] in ['dom_ITCZ','dom_NS_cs','dom_NS_cs_afr']:
    alt_lims = (0,18000) 
    #alt_lims = (0,6000) 
else:
    alt_lims = (0,4000) 
    #raise NotImplementedError()

vertical_line = None
#vertical_line = 8

title = None

agg_level = TP.ALL_TIME
#agg_level = TP.ANNUAL_CYCLE

agg_operators = [TP.MEAN]

#use_time_periods = time_periods_2007
#use_time_periods = time_periods_2008
#use_time_periods = get_time_periods_for_month(2007, 12)
use_time_periods = time_periods_ana
#use_time_periods = time_periods_ana_FMA
#use_time_periods = time_periods_ana_MAM
#use_time_periods = time_periods_ana_MJJ
#use_time_periods = time_periods_ana_MJ
#use_time_periods = time_periods_ana_JJA
#use_time_periods = time_periods_ana_JAS
#use_time_periods = time_periods_ana_ASO
#use_time_periods = time_periods_ana_SON
#use_time_periods = time_periods_ana_ONDJ
#use_time_periods = time_periods_ana_NDJ
#use_time_periods = time_periods_ana_DJF

use_time_periods = time_periods_ana_JFM
#use_time_periods = time_periods_ana_AMJ
#use_time_periods = time_periods_ana_JAS
use_time_periods = time_periods_ana_OND

#use_time_periods = [{
#    'first_date':datetime(2010,12,31),
#    'last_date':datetime(2010,12,31)
#}]


plot_append = 'change'
plot_append = 'MPI-ESM1-2-HR'


models_cmip6 = models_cmip6_cldf
#models_cmip6 = models_cmip6_cldf[0:2]
#models_cmip6 = models_cmip6_cldf[2:]
#print(models_cmip6)
#quit()
mem_keys_cmip6_hist = ['{}_historical'.format(model) for model in models_cmip6]
mem_keys_cmip6_scen = ['{}_ssp585'.format(model) for model in models_cmip6]
from package.nl_models import models_cmip6

if plot_append in ['change', 'SON', 'aug']:
    mem_cfgs = [
        #{
        #    'mem_key':      'GPM_IMERG', 
        #    'time_periods': use_time_periods,
        #},
        {
            'mem_key':      'ERA5', 
            'time_periods': use_time_periods,
        },
        {
            'mem_key':      'COSMO_3.3_ctrl', 
            'time_periods': use_time_periods,
        },
        {
            'mem_key':      'COSMO_3.3_pgw3', 
            'time_periods': use_time_periods,
        },
    ]
elif plot_append in models_cmip6:
    mem_cfgs = [
        #mpi_change_JAS,
        #mpi_change_JFM,
        {
            'mem_oper':     'mean',
            'mem_keys':     mem_keys_cmip6_hist,
            'time_periods': time_periods_cmip6_hist,
            'time_periods': time_periods_cmip6_hist_JFM,
            'time_periods': time_periods_cmip6_hist_AMJ,
            'time_periods': time_periods_cmip6_hist_JAS,
            'time_periods': time_periods_cmip6_hist_OND,
        },
        {
            'mem_oper':     'mean',
            'mem_keys':     mem_keys_cmip6_scen,
            'time_periods': time_periods_cmip6_scen,
            'time_periods': time_periods_cmip6_scen_JFM,
            'time_periods': time_periods_cmip6_scen_AMJ,
            'time_periods': time_periods_cmip6_scen_JAS,
            'time_periods': time_periods_cmip6_scen_OND,
        },
    ]

else:
    raise ValueError()

dask_chunks = {'lon':50,'lat':50}

norm_var_cfg = {
    #'QV':   'T',
}

### set up var_src
var_src_dict = set_up_var_src_dict(inp_base_dir, ana_base_dir,
                                    ANA_NATIVE_domain)


#### plot
nrows = 1
ncols = 3
figsize = (13,3.0)

#jnrows = 1
#jncols = 4
#jfigsize = (16,3.0)

#nrows = 2
#ncols = 3
#figsize = (13,6.0)

#nrows = 2
#ncols = 4
#figsize = (16,7.0)

#nrows = 2
#ncols = 2
#figsize = (9,7.0)

#nrows = 5
#ncols = 3
#figsize = (12,16.0)

i_plot_cbar = 1
#pan_cbar_pos = 'center right'
#pan_cbar_pad = -2
pan_cbar_pos = 'lower center'
pan_cbar_pad = -5
cbar_label_mode = 'both'
#cbar_label_mode = 'var_units'
#cbar_label_mode = 'var_name'
#cbar_label_mode = 'neither'

#plot_glob_cbar = 0
#

arg_subplots_adjust = {
    # 1x3
    'left':0.05,
    'bottom':0.18,
    'right':0.97,
    'top':0.90,
    'wspace':0.20,
    'hspace':0.30,
}
colorbar_pos = [0.10, 0.12, 0.52, 0.03]
