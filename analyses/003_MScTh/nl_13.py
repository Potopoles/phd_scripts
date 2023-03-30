#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 003_13_eval_radar:
author			Christoph Heim
date created    08.11.2019
date changed    28.02.2020
usage			import in main script
"""
###############################################################################
import os, subprocess, sys
from datetime import datetime, timedelta
from package.domains import *
###############################################################################
## paths
plot_base_dir   = '/net/o3/hymet_nobackup/heimc/plots/003_MScTh/eval_radar' 
sim_base_dir    = '/net/o3/hymet_nobackup/heimc/MScTh/02_fields/topocut'

## computation
njobs = 1
if len(sys.argv) > 1:
    njobs = int(sys.argv[1])

## run settings
i_save_fig = 0
i_verbosity = 0

## time (have to be chosen from start with hour 0 to end with hour 1
time_sel = slice(datetime(2006,7,11,0), datetime(2006,7,20,1))
#time_sel = slice(datetime(2006,7,11,0), datetime(2006,7,12,1))
time_dt = timedelta(hours=1)

ress = ['4', '2', '1']
#ress = ['4', '2']
#ress = ['4']
model_types = ['RAW', 'SM']
model_keys = ['SM4', 'RAW4', 'SM2', 'RAW2', 'SM1', 'RAW1']
#obs_keys = ['OBS4', 'OBS2', 'OBS1']

domain = dom_alpine_region

percentiles = [15, 85]
#percentiles = [0, 100]

diff_lims = (-0.20,0.20)
label_size = 20

plot_dict = {
    'top_left':{
        'data':{
            'SM4'   :{'col':'black'},
            'SM2'   :{'col':'blue' },
            'SM1'   :{'col':'red'  },
        },
        'meta':{
            'src'       :'full',
            'ax_inds'   :(0,0),
            'ax_title'  :'SM',
            'ax_xlim'  :(0,24),
            'ax_ylim'  :(0,0.30),
            'ax_xlabel':None,
            'ax_ylabel':'Rain Rate [$mm$ $h^{-1}$]',
            'legend'    :True,
        },
    },
    'top_right':{
        'data':{
            'RAW4'  :{'col':'black'},
            'RAW2'  :{'col':'blue' },
            'RAW1'  :{'col':'red'  },
        },
        'meta':{
            'src'       :'full',
            'ax_inds'   :(0,1),
            'ax_title'  :'RAW',
            'ax_xlim'  :(0,24),
            'ax_ylim'  :(0,0.30),
            'ax_xlabel':None,
            'ax_ylabel':None,
            'legend'    :True,
        },
    },
    'top_diff':{
        'data':{
            'DIFF4'  :{'col':'black'},
            'DIFF2'  :{'col':'blue' },
            'DIFF1'  :{'col':'red'  },
        },
        'meta':{
            'src'       :'full',
            'ax_inds'   :(0,2),
            'ax_title'  :'RAW - SM',
            'ax_xlim'  :(0,24),
            'ax_ylim'  :diff_lims,
            'ax_xlabel':None,
            'ax_ylabel':None,
            'legend'    :False,
        },
    },

    'mid_left':{
        'data':{
            'SM4'   :{'col':'black'},
            'SM2'   :{'col':'blue' },
            'SM1'   :{'col':'red'  },
            'OBS4'  :{'col':'grey' },
        },
        'meta':{
            'src'       :'radar',
            'ax_inds'   :(1,0),
            'ax_title'  :None,
            'ax_xlim'  :(0,24),
            'ax_ylim'  :(0,0.30),
            'ax_xlabel':None,
            'ax_ylabel':'Rain Rate [$mm$ $h^{-1}$]',
            'legend'    :True,
        },
    },
    'mid_right':{
        'data':{
            'RAW4'  :{'col':'black'},
            'RAW2'  :{'col':'blue' },
            'RAW1'  :{'col':'red'  },
            'OBS4'  :{'col':'grey' },
        },
        'meta':{
            'src'       :'radar',
            'ax_inds'   :(1,1),
            'ax_title'  :None,
            'ax_xlim'  :(0,24),
            'ax_ylim'  :(0,0.30),
            'ax_xlabel':None,
            'ax_ylabel':None,
            'legend'    :True,
        },
    },
    'mid_diff':{
        'data':{
            'DIFF4'  :{'col':'black'},
            'DIFF2'  :{'col':'blue' },
            'DIFF1'  :{'col':'red'  },
        },
        'meta':{
            'src'       :'radar',
            'ax_inds'   :(1,2),
            'ax_title'  :None,
            'ax_xlim'  :(0,24),
            'ax_ylim'  :diff_lims,
            'ax_xlabel':None,
            'ax_ylabel':None,
            'legend'    :False,
        },
    },



    'low_left':{
        'data':{
            'SM4'   :{'col':'black'},
            'SM2'   :{'col':'blue' },
            'SM1'   :{'col':'red'  },
            'OBS'  :{'col':'grey' },
        },
        'meta':{
            'src'       :'stat',
            'ax_inds'   :(2,0),
            'ax_title'  :None,
            'ax_xlim'  :(0,24),
            'ax_ylim'  :(0,0.30),
            'ax_xlabel':'Time (UTC)',
            'ax_ylabel':'Rain Rate [$mm$ $h^{-1}$]',
            'legend'    :True,
        },
    },
    'low_right':{
        'data':{
            'RAW4'  :{'col':'black'},
            'RAW2'  :{'col':'blue' },
            'RAW1'  :{'col':'red'  },
            'OBS'  :{'col':'grey' },
        },
        'meta':{
            'src'       :'stat',
            'ax_inds'   :(2,1),
            'ax_title'  :None,
            'ax_xlim'   :(0,24),
            'ax_ylim'   :(0,0.30),
            'ax_xlabel' :'Time (UTC)',
            'ax_ylabel' :None,
            'legend'    :True,
        },
    },
    'low_diff':{
        'data':{
            'DIFF4'  :{'col':'black'},
            'DIFF2'  :{'col':'blue' },
            'DIFF1'  :{'col':'red'  },
        },
        'meta':{
            'src'       :'stat',
            'ax_inds'   :(2,2),
            'ax_title'  :None,
            'ax_xlim'   :(0,24),
            'ax_ylim'   :diff_lims,
            'ax_xlabel' :'Time (UTC)',
            'ax_ylabel' :None,
            'legend'    :False,
        },
    },
}

