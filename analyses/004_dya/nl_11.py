#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 004_11_bulk:
author			Christoph Heim
date created    22.01.2021
date changed    02.02.2021
usage			import in another script
"""
###############################################################################
import os, sys
import numpy as np
from datetime import datetime, timedelta
from base.nl_global import (plot_glob_base_dir, inp_glob_base_dir,
                               ana_glob_base_dir)
from nl_plot_11 import nlp
from base.nl_domains import *
from nl_mem_src import *
from nl_var_src import set_up_var_src_dict
###############################################################################
## paths
ana_name        = '004_dyamond'
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name, '11_bulk')
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)
pickle_dir      = os.path.join(ana_base_dir, '11')

if len(sys.argv) <= 8:
    raise ValueError('Not 8 arguments given')

## computation
njobs = int(sys.argv[1])

## analysis members
obs_src_dict = mem_src['obs']
sim_group = 'all_members'
#sim_group = 'sensitivity'
#sim_group = 'debug'
#sim_group = 'iav'
sim_src_dict_tmp = mem_src[sim_group]
# select members in sim_src_dict based on user input
mem_keys = sys.argv[6].split(',')
sim_src_dict = {}
for mem_key in mem_keys:
    print(mem_key)
    if mem_key in sim_src_dict_tmp:
        sim_src_dict[mem_key] = sim_src_dict_tmp[mem_key]
    else: raise ValueError('mem_key {} not in sim_src_dict'.format(mem_key))
## add OBS
#sim_src_dict['OBS'] = {}

obs_key='ERA5_31'

# var_names
main_var_name = sys.argv[2]

## run settings
#computation = 'tend'
#computation = 'mean'
#bulk_mode = 'edge'
#bulk_mode = 'vol'
computation = sys.argv[8].split('_')[0]
bulk_mode = sys.argv[8].split('_')[1]
print(computation)
print(bulk_mode)
print(main_var_name)
i_save_fig = 3
i_debug = 1
i_aggreg_days = 0
i_skip_missing = 1
i_plot = 1
i_recompute = int(sys.argv[3])
if i_recompute: i_plot = 0;
panel_label = sys.argv[4]


if not i_recompute:
    computation = nlp['computation']

optional_var_names = []
if computation == 'tend':
    if bulk_mode == 'edge':
        input_var_names = [main_var_name, 'RHO', 'INVHGT', 'U', 'V', 'W']
        if main_var_name == 'QV':
            input_var_names.append('SLHFLX')
            optional_var_names.append('SLHFLX')
        elif main_var_name == 'POTT':
            input_var_names.append('SSHFLX')
            optional_var_names.append('SSHFLX')
    elif bulk_mode == 'vol':
        input_var_names = [main_var_name, 'RHO', 'INVHGT', 'U', 'V', 'W']
elif computation == 'mean':
    input_var_names = [main_var_name, 'RHO', 'INVHGT']
    bulk_mode = 'vol'


integ_dims = ['lon','lat','alt']
#integ_dims = ['lon','lat']
#integ_dims = ['alt']
#integ_dims = ['alt','lat']

#integration_volumes = ['total', 'above', 'below']
integration_volumes = sys.argv[7].split(',')
#print(integration_volumes)
#quit()

### time
time_periods = [
    {
        'first_date':    datetime(2016,8,1),
        'last_date':     datetime(2016,9,9),
        #'first_date':    datetime(2016,8,6),
        #'last_date':     datetime(2016,8,6),
    },
]
# change to 02.08. because some models (e.g. IFS) need last day
# to compute surface fluxes (due to accumulation.. (why would you?))
if computation == 'tend':
    time_periods[0]['first_date'] = datetime(2016,8,2)

edges = {
    'W'     :{'dim':'lon', 'orient': 1,  'pos':'start'},
    'E'     :{'dim':'lon', 'orient':-1,  'pos':'stop'},
    'S'     :{'dim':'lat', 'orient': 1,  'pos':'start'},
    'N'     :{'dim':'lat', 'orient':-1,  'pos':'stop'},
    'B'     :{'dim':'alt', 'orient': 1,  'pos':'start'},
    'SFC'   :{'dim':'alt', 'orient': 1,  'pos':None},
    'T'     :{'dim':'alt', 'orient':-1,  'pos':'stop'},
}

aggregs = {
    'edge S'   :{
        'vars':{'S':1,},
    },
    'edge N'   :{
        'vars':{'N':1,},
    },
    'edge W'   :{
        'vars':{'W':1,},
    },
    'edge E'   :{
        'vars':{'E':1,},
    },
    'edge T'   :{
        'vars':{'T':1,},
    },
    'edge B'   :{
        'vars':{'B':1,},
    },
    'edge SFC'   :{
        'vars':{'SFC':1,},
    },
    'edge hori'   :{
        'vars':{'N':1, 'S':1, 'W':1, 'E':1,},
    },
    'edge vert'   :{
        'vars':{'T':1, 'B':1,},
        #'vars':{'T':1, 'SFC':1,},
    },
    'edge tot'   :{
        #'vars':{'N':1, 'S':1, 'W':1, 'E':1, 'T':1, 'B':1,},
        'vars':{'N':1, 'S':1, 'W':1, 'E':1, 'T':1, 'SFC':1,},
    },
    'vol tot'   :{
        'vars':{'HORI':1, 'VERT':1,},
    },
    'vol hori'   :{
        'vars':{'HORI':1,},
    },
    'vol vert'   :{
        'vars':{'VERT':1,},
    },

    'inv tot'   :{
        'vars':{'HORI':1, 'N':-1, 'S':-1, 'W':-1, 'E':-1,
                'VERT':1, 'T':-1, 'B':-1},
    },
    'inv hori'   :{
        'vars':{'HORI':1, 'N':-1, 'S':-1, 'W':-1, 'E':-1,},
    },
    'inv vert'   :{
        'vars':{'VERT':1, 'T':-1, 'B':-1},
    },

    'adv + sfc tot'   :{
        'vars':{'HORI':1, 'VERT':1, 'SFC':1},
    },
    'tot'   :{
        'vars':{'TOT':1},
    },
    'residual'   :{
        'vars':{'TOT':1, 'HORI':-1, 'VERT':-1, 'SFC':-1},
    },

    'mean'   :{
        'vars':{'TOT':1},
    },
}



#cumulative_edges = {
#    'HORI':['W', 'E', 'S', 'N'],
#    'VERT':['B', 'T'],
#    'TOT': ['W', 'E', 'S', 'N', 'B', 'T'],
#}


# set up names of target variables to be computed
# only used for plotting
target_var_names = []
for vol_key in integration_volumes:
    if nlp['computation'] == 'tend':
        for edge_key,edge in edges.items():
            var_name = 'bulk_{}_{}_{}_{}_{}'.format(nlp['computation'],
                            'edge', main_var_name, vol_key, edge_key)
            target_var_names.append(var_name)
        var_name = 'bulk_{}_{}_{}_{}_{}'.format(nlp['computation'],
                            'vol', main_var_name, vol_key, 'HORI')
        target_var_names.append(var_name)
        var_name = 'bulk_{}_{}_{}_{}_{}'.format(nlp['computation'],
                            'vol', main_var_name, vol_key, 'VERT')
        target_var_names.append(var_name)
        var_name = 'bulk_{}_{}_{}_{}_{}'.format(nlp['computation'],
                            'vol', main_var_name, vol_key, 'TOT')
        target_var_names.append(var_name)
    elif nlp['computation'] == 'mean':
        var_name = 'bulk_{}_{}_{}_{}_{}'.format(nlp['computation'],
                            'vol', main_var_name, vol_key, 'MEAN')
        target_var_names.append(var_name)



cfg = {}
if len(sys.argv) > 5:
    dom_key = sys.argv[5]
    if dom_key == 'full':
        cfg['domain']       = dom_SEA_Sc
    elif dom_key == 'Cu':
        cfg['domain']       = dom_SEA_Sc_sub_Cu
    elif dom_key == 'Sc':
        cfg['domain']       = dom_SEA_Sc_sub_Sc
    elif dom_key == 'St':
        cfg['domain']       = dom_SEA_Sc_sub_St
    else:
        raise NotImplementedError()
else:
    cfg['domain']       = dom_SEA_Sc
# altitude limits
cfg['domain']['alt'] = slice(0,6000)
print('run on domain {}'.format(cfg['domain']['label']))


### set up var_src
var_src_dict = set_up_var_src_dict(inp_base_dir, ana_base_dir)
