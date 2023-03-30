#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 003_12_eval_stat_prec:
author			Christoph Heim
date created    07.11.2019
date changed    28.02.2020
usage			import in main script
"""
###############################################################################
import os, subprocess, sys
from datetime import datetime, timedelta
from package.domains import *
###############################################################################
## paths
plot_base_dir   = '/net/o3/hymet_nobackup/heimc/plots/003_MScTh/eval_stat_prec' 
sim_base_dir    = '/net/o3/hymet_nobackup/heimc/MScTh/02_fields/topocut'
obs_base_dir    = '/net/o3/hymet_nobackup/heimc/data/obs/prec_stat_idaweb'

# station data
stat_meta_name = 'stat_meta.txt'
stat_data_name = 'stat_data.txt'

### computation
#njobs = 1
#if len(sys.argv) > 1:
#    njobs = int(sys.argv[1])

## run settings
i_save_fig = 0

## time
time_sel = slice(datetime(2006,7,11,1), datetime(2006,7,20,0))
time_dt = timedelta(hours=1)


## simulations
model_keys = ['SM4', 'RAW4', 'SM2', 'RAW2', 'SM1', 'RAW1']


plot_dict = {
    'left':{
        'data':{
            'SM4'   :{'col':'black'},
            'SM2'   :{'col':'blue' },
            'SM1'   :{'col':'red'  },
            'OBS'   :{'col':'grey' },
        },
        'meta':{
            'ax_inds'   :(0,0),
            'ax_title'  :'SM',
            'ax_xlim'  :(0,24),
            'ax_ylim'  :(0,0.30),
            'ax_xlabel':'Time (UTC)',
            'ax_ylabel':'Rain Rate [$mm$ $h^{-1}$]',
        },
    },
    'right':{
        'data':{
            'RAW4'  :{'col':'black'},
            'RAW2'  :{'col':'blue' },
            'RAW1'  :{'col':'red'  },
            'OBS'   :{'col':'grey' },
        },
        'meta':{
            'ax_inds'   :(0,1),
            'ax_title'  :'RAW',
            'ax_xlim'  :(0,24),
            'ax_ylim'  :(0,0.30),
            'ax_xlabel':'Time (UTC)',
            'ax_ylabel':'Rain Rate [$mm$ $h^{-1}$]',
        },
    }
}



## script specific run configs
configs = {
    'test':{
        'nrows':1, 'ncols':3,
    },
}
run_mode = 'test'

## implement run config
cfg = configs[run_mode]
