
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 004_06_diurnal:
author			Christoph Heim
date created    17.08.2020
date changed    18.08.2020
usage			import in another script
"""
###############################################################################
import os, subprocess, sys
from datetime import datetime, timedelta
from base.nl_global import (plot_glob_base_dir, inp_glob_base_dir,
                               ana_glob_base_dir)
from base.nl_domains import *
from package.var_pp import DERIVE, DIRECT
from nl_plot_06 import nlp
###############################################################################
## paths
ana_name        = '004_dyamond'
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name, '06_diurnal')
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)

## computation
njobs = 1
if len(sys.argv) > 1:
    njobs = int(sys.argv[1])


mlo_sims = {
    #### 12km 
    #######################################################
    #'off'             :{'mkey':'COSMO',       'res':12,
    #                    'case':'SA_MLO_off',
    #                    'label':'no mlo',},
    #'bc'       :{'mkey':'COSMO',       'res':12,
    #                      'case':'SA_MLO_bc',
    #                      'label':'sst bc',},
    #'tau_6_depth_0.5'   :{'mkey':'COSMO',       'res':12,
    #                    'case':'SA_MLO_tau_6_depth_0.5',
    #                    'label':'tau 6h depth 0.5m',},
    #'tau_3_depth_1'   :{'mkey':'COSMO',       'res':12,
    #                    'case':'SA_MLO_tau_3_depth_1',
    #                    'label':'tau 3h depth 1m',},
    #'tau_6_depth_5'   :{'mkey':'COSMO',       'res':12,
    #                    'case':'SA_MLO_tau_6_depth_5',
    #                    'label':'tau 6h depth 5m',},
    #'tau_3_depth_3'   :{'mkey':'COSMO',       'res':12,
    #                    'case':'SA_MLO_tau_3_depth_3',
    #                    'label':'tau 3h depth 3m',},
    #'tau_3_depth_4'   :{'mkey':'COSMO',       'res':12,
    #                    'case':'SA_MLO_tau_3_depth_4',
    #                    'label':'tau 3h depth 4m',},

    #### 2.2km 
    #######################################################
    'C2_noMLO'      :{'mkey':'COSMO',       'res':2.2,
                      'case':'SA_4_2_noMLO',
                      'label':'COSMO 2.2 noMLO',       },
    'C2_MLO'        :{'mkey':'COSMO',       'res':2.2,
                      'case':'SA_4_2_MLO',
                      'label':'COSMO 2.2 MLO',       },
}


## run settings
if len(sys.argv) > 2:
    i_save_fig = int(sys.argv[2])
else:
    i_save_fig = 0
i_debug = 0
i_use_obs = 1
i_plot = 1

first_date = datetime(2016,8,1)
last_date = datetime(2016,8,31)

run_mode = 'mlo_sst'

plot_var = 'SST'

var_src = {
    'SST':     {'load':DERIVE, 'src':os.path.join(inp_base_dir)},
    'TSURF':   {'load':DIRECT, 'src':os.path.join(inp_base_dir)},
}


stretch = 1
run_configs = {
    'mlo_sst':  {
        'use_sims': mlo_sims,
        'domain':   dom_SEA_Sc,
    },
}

cfg = run_configs[run_mode]
cfg['var_name'] = plot_var
