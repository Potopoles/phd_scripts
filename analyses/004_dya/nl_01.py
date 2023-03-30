
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 004_01_spatial:
author			Christoph Heim
date created    18.11.2019
date changed    03.02.2021
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
from nl_plot_01 import nlp
###############################################################################
## paths
ana_name        = '004_dyamond'
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name, '01_spatial')
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)

## computation
njobs = int(sys.argv[1])

## members

stretch = 0.4
obs_src_dict = mem_src['obs']

# TODO
plot_pos = {
    'C12': (0,0),
    'C4.4': (0,0),
}

i_aggreg = 'none'
i_aggreg = 'monthly'
i_aggreg = 'yearly'
i_aggreg = 'all'

## run settings
i_save_fig = 0
if len(sys.argv) > 2:
    i_save_fig = int(sys.argv[2])
i_debug = 1
i_use_obs = 1
ERA5_as_obs = 1
i_plot = 1
i_coarse_grain = 0
#i_coarse_grain = 50

time_periods = [
    {
        'first_date':    datetime(2016,8,6),
        'last_date':     datetime(2016,9,9),
        #'last_date':     datetime(2016,8,31),

        #'first_date':    datetime(2016,8,14),
        #'last_date':     datetime(2016,8,14),
    },
]

#time_periods = [
#    {
#        'first_date':    datetime(2006,8,6),
#        'last_date':     datetime(2006,12,31),
#    },
#]


i_plot_bias = 0

plot_var = 'ALBEDO'
plot_var = 'LWUTOA'
##plot_var = 'TQC'
#plot_var = 'INVHGT'
#plot_var = 'PP'
#plot_var = 'UV10M'
#plot_var = 'CORREFL'
#plot_var = 'SLHFLX'
#plot_var = 'INVSTRV'
#plot_var = 'U10M'
#plot_var = 'V10M'
#plot_var = 'ENTR'
#plot_var = 'TQV'
#plot_var = 'TQI'
#plot_var = 'POTTMBLI'
#plot_var = 'POTTHDIVMBLI'
#plot_var = 'SUBS'
#plot_var = 'LTS'
#plot_var = 'LCL'
##plot_var = 'LCLDBASE'
#plot_var = 'DCLDBASELCL'
#plot_var = 'DCLDTOPINVHGT'
#plot_var = 'DINVHGTLCL'
#plot_var = 'CLCL'
#plot_var = 'CLCL2'
#plot_var = 'NOINVF'
#plot_var = 'WFLXMBLI'
#plot_var = 'CLDBASENORMI'
#plot_var = 'QVFLXZCB'
#plot_var = 'WNORMI'
#plot_var = 'WMBLI'
#plot_var = 'DIABHMINV'

run_mode = 'dya'
#run_mode = 'snapshot'
#run_mode = 'cosmo_clouds'
##run_mode = 'movie'
##run_mode = 'cosmo'
#run_mode = 'sens_extpar'
#run_mode = 'sens_clouds'
#run_mode = 'sensitivity'
#run_mode = 'iav'


### set up var_src
var_src_dict = set_up_var_src_dict(inp_base_dir, ana_base_dir)

var_configs = {
    'ALBEDO':{
        #'min_max'   :(0,'obs'),
        #'min_max'   :(0,None),
        'min_max'   :(0,0.5),
        'min_max_bias':(-0.15,0.15),
        'cmap'      :'cubehelix',
        #'obs'       :None,
        'obs'       :'CM_SAF_MSG_AQUA_TERRA',
        #'obs'       :'CM_SAF_METEOSAT',
        #'obs'       :'ERA5_31',
        #'obs'       :'COSMO_4.4_OBSREF',
        #'obs'       :'COSMO_4.4_CALIB_OBSREF',
    },
    'LWUTOA':{
        'min_max'   :(260,300), # DYAMOND paper
        #'min_max'   :(190,300),
        #'min_max'   :('obs','obs'),
        'min_max_bias':(-40,40),
        'cmap'      :'rain',
        'obs'       :'CM_SAF_MSG_AQUA_TERRA',
        #'obs'       :'CM_SAF_METEOSAT',
        #'obs'       :'ERA5_31',
        #'obs'       :'COSMO_4.4_OBSREF',
        #'obs'       :'COSMO_4.4_CALIB_OBSREF',
    },
    'U10M':{
        'min_max'   :(-5,5),
        'min_max_bias':(-3.0,3.0),
        'cmap'      :'blue_red',
        'obs'       :'ERA5_31',
    },
    'V10M':{
        'min_max'   :(-7,7),
        'min_max_bias':(-1.5,1.5),
        'cmap'      :'blue_red',
        'obs'       :'ERA5_31',
    },
    'UV10M':{
        'min_max'   :(None,None),
        'min_max_bias':(-1.5,1.5),
        'cmap'      :'rain',
        'obs'       :'ERA5_31_OBS',
        #'obs'       :'COSMO_4.4_CALIB_OBSREF',
    },
    'PP':{
        'min_max'   :(0,0.4),
        'min_max_bias':(-0.1,0.1),
        'cmap'      :'rain',
        'obs'       :'ERA5_31_OBS',
        #'obs'       :'COSMO_4.4_CALIB_OBSREF',
    },
    'INVHGT':{
        'min_max'   :(400,2500), # DYAMOND paper
        'min_max_bias':(-500,500),
        'cmap'      :'terrain',
        'obs'       :'ERA5_31_OBS',
        #'obs'       :'COSMO_4.4_CALIB_OBSREF',
    },
    'INVSTRV':{
        'min_max'   :(None,None),
        'min_max_bias':(-5,5),
        'cmap'      :'cubehelix',
        'obs'       :'ERA5_31',
    },
    'ENTR':{
        'min_max'   :(-0.005,0.005),
        'cmap'      :'blue_red',
        'obs'       :'ERA5_31',
    },
    'TQV':{
        'min_max'   :(None,None),
        'cmap'      :'rain',
        'obs'       :'CM_SAF_HTOVS',
        #'obs'       :'ERA5_31',
    },
    'TQI':{
        'min_max'   :(0,0.005),
        'cmap'      :'rain',
        'obs'       :'CM_SAF_MSG',
    },
    'CLCL':{
        'min_max'   :(0,1),
        'cmap'      :'cubehelix',
        'obs'       :'CM_SAF',
    },
    'CLCL2':{
        'min_max'   :(0,1),
        'cmap'      :'cubehelix',
        'obs'       :'CM_SAF',
    },
    'SUBS':{
        'min_max'   :(-0.01,0.00),
        'cmap'      :'rain',
        'obs'       :'ERA5_31',
    },
    'NOINVF':{
        'min_max'   :(0.0,0.1),
        'cmap'      :'cubehelix',
        'obs'       :'ERA5_31',
    },
    'LTS':{
        'min_max'   :(None,None),
        'cmap'      :'cubehelix',
        'obs'       :'ERA5_31',
    },
    'LCL':{
        'min_max'   :(0,1500),
        'cmap'      :'rain',
        'obs'       :'ERA5_31',
    },
    'LCLDBASE':{
        'min_max'   :(0,1500),
        'cmap'      :'rain',
        'obs'       :'ERA5_31',
    },
    'POTTMBLI':{
        'min_max'   :(None,None),
        'cmap'      :'rain',
        'obs'       :'ERA5_31',
    },
    'POTTHDIVMBLI':{
        'min_max'   :(-0.0001,0.0001),
        'cmap'      :'blue_red',
        'obs'       :'ERA5_31',
    },
    'DCLDBASELCL':{
        'min_max'   :(0,600),
        'cmap'      :'rain',
        'obs'       :'ERA5_31',
    },
    'DCLDTOPINVHGT':{
        'min_max'   :(None,None),
        'cmap'      :'rain',
        'obs'       :'ERA5_31',
    },
    'DINVHGTLCL':{
        'min_max'   :(0,1500),
        'cmap'      :'rain',
        'obs'       :'ERA5_31',
    },
    'INVSTRA':{
        'min_max'   :(None,None),
        'cmap'      :'cubehelix',
        'obs'       :'ERA5_31',
    },
    'CLDBASENORMI':{
        'min_max'   :(None,None),
        'cmap'      :'cubehelix',
        'obs'       :'ERA5_31',
    },
    'WMBLI':{
        'min_max'   :(-0.02,0.02),
        'cmap'      :'cubehelix',
        'obs'       :False,
    },
    'WFLXI':{
        'min_max'   :(-0.0075,0.025),
        'cmap'      :'jump',
        'obs'       :False,
    },
    'WFLXMBLI':{
        'min_max'   :(-0.0075,0.0025),
        'cmap'      :'jump',
        'obs'       :False,
    },
    'WFLXBLMIN':{
        'min_max'   :(-0.0150,0.0050),
        'cmap'      :'jump',
        'obs'       :False,
    },
    'DIABHMINV':{
        'min_max'   :(-0.00018, 0.00006),
        'cmap'      :'jump',
        'obs'       :False,
    },
    'tqvbli':{
        'min_max'   :(None,None),
        'cmap'      :'rain',
        'obs'       :False,
    },
    'tqvfti':{
        'min_max'   :(None,None),
        'cmap'      :'rain',
        'obs'       :False,
    },
    'tqv0_5':{
        'min_max'   :(None,None),
        'cmap'      :'rain',
        'obs'       :False,
    },
    'dtqvi':{
        'min_max'   :(None,None),
        'cmap'      :'rain',
        'obs'       :False,
    },
    'QVFLXZCB':{
        'min_max'   :(-0.001,0.001),
        'cmap'      :'blue_red',
        'obs'       :False,
    },
    'CORREFL':{
        'min_max'   :(0,0.10),
        'cmap'      :'clouds',
        'obs'       :'SUOMI_NPP_VIIRS',
    },
    'TQC':{
        'min_max'   :(0,0.25),
        'min_max_bias':(-0.10,0.10),
        'cmap'      :'clouds',
        'obs'       :'ERA5_31_OBS',
    },
    'CLDHGT':{
        'compute_exact':False,
        'min_max'   :(None,2000),
        'cmap'      :'cubehelix',
        'obs'       :False,
    },
    'SLHFLX':{
        'min_max'   :(None,None),
        'cmap'      :'colorful',
        'obs'       :'ERA5_31_OBS',
    },
    'UI':{
        'min_max'   :(-8,8),
        'cmap'      :'blue_red',
        'obs'       :'ERA5_31',
    },
    'VI':{
        'min_max'   :(-8,8),
        'cmap'      :'blue_red',
        'obs'       :'ERA5_31',
    },
    'ENTRV':{
        'min_max'   :(-0.005,0.005),
        'cmap'      :'blue_red',
        'obs'       :'ERA5_31',
    },
    'ENTRH':{
        'min_max'   :(-0.005,0.005),
        'cmap'      :'blue_red',
        'obs'       :'ERA5_31',
    },
}



run_configs = {
    'dya':  {
        #'subplts':  {'left':0.08,  'bottom':0.21,
        #             'right':0.98, 'top':0.95,
        #             'wspace':0.03,'hspace':0.19},
        'subplts':  {'left':0.10,  'bottom':0.28,
                     'right':0.98, 'top':0.92,
                     'wspace':0.03,'hspace':0.40},
        'use_sims': mem_src['dya_main'],
        #'use_sims': debug_sims,
        'domain':   dom_SEA_Sc,
        #'domain':   dom_SEA_Sc_sub_Cu,
        #'domain':   dom_SEA_Sc_sub_Sc,
        #'domain':   dom_SEA_Sc_sub_St,
        'panel_labels_start_ind': 0,
        #'panel_labels_start_ind': 12,
        'panel_labels_shift_right': -0.1,
        'plot_order':'resolution',
        #'figsize':  (13.9*stretch,8.0*stretch),
        'figsize':  (14.4*stretch,9.5*stretch),
        'nrows':    3,
        'ncols':    4,
        'snapshots':{'on':0},
    },

    'snapshot':  {
        'subplts':  {'left':0.10,  'bottom':0.28,
                     'right':0.98, 'top':0.92,
                     'wspace':0.03,'hspace':0.40},
        'use_sims': mem_src['dya_main'],
        'domain':   dom_SEA_Sc,
        'panel_labels_start_ind': 0,
        'panel_labels_shift_right': -0.1,
        'plot_order':'resolution',
        'figsize':  (14.4*stretch,9.5*stretch),
        'nrows':    3,
        'ncols':    4,
        'snapshots':{'on':1,
                     'freq':timedelta(minutes=180),
                     'max_back':timedelta(days=1),},
    },

    'movie':  {
        'subplts':  {'left':0.05,  'bottom':0.04,
                     'right':0.99, 'top':0.90,
                     'wspace':0.01,'hspace':0.17},
        'use_sims': mem_src['dya_main'],
        'domain':   dom_SEA_Sc_anim,
        'plot_order':'resolution',
        # this is pptx wide screen resolution
        'figsize':  (14.22*stretch,8.0*stretch),
        'nrows':    3,
        'ncols':    4,
        'snapshots':{'on':1,
                     'freq':timedelta(minutes=30),
                     'max_back':timedelta(days=1),},
        'hide_colorbar':True,
    },

    'cosmo':  {
        'subplts':  {'left':0.08,  'bottom':0.21,
                     'right':0.98, 'top':0.95,
                     'wspace':0.03,'hspace':0.20},
        'use_sims': mem_src['cosmo'],
        'domain':   dom_SEA_Sc,
        #'plot_order':'position',
        'plot_order':'resolution',
        'figsize':  (13.9*stretch,7.0*stretch),
        'nrows':    3,
        'ncols':    5,
        'snapshots':{'on':0},
    },

    'cosmo_clouds':  {
        'subplts':  {'left':0.10,  'bottom':0.28,
                     'right':0.98, 'top':0.80,
                     'wspace':0.03,'hspace':0.40},
        'use_sims': mem_src['cosmo_snapshot'],
        'domain':   dom_Sc_zoom,
        #'domain':   dom_SEA_Sc_sub_Sc,
        'panel_labels_start_ind': 11,
        'panel_labels_shift_right': -0.2,
        'plot_order':'resolution',
        # this is pptx wide screen resolution
        'figsize':  (14.22*stretch,4.0*stretch),
        'nrows':    1,
        'ncols':    5,
        'snapshots':{'on':1,
                     'freq':timedelta(minutes=180),
                     'max_back':timedelta(days=1),},
        'hide_colorbar':True,
    },

    'sens_extpar':  {
        'subplts':  {'left':0.08,  'bottom':0.21,
                     'right':0.98, 'top':0.95,
                     'wspace':0.10,'hspace':0.20},
        'use_sims': mem_src['sens_extpar'],
        'plot_order':'resolution',
        'nrows':    2,
        'ncols':    3,
        'domain':   dom_iav_trades,
        'figsize':  (13.0*stretch,9.0*stretch),

        'domain':   dom_DYA_4km,
        'figsize':  (13.0*stretch,10.0*stretch),
        'snapshots':{'on':0},
    },


    'sens_clouds':  {
        'subplts':  {'left':0.08,  'bottom':0.07,
                     'right':0.99, 'top':0.90,
                     'wspace':0.02,'hspace':0.17},
        'use_sims': mem_src['sens_clouds'],
        #'use_sims': mem_src['sensitivity'],
        #'domain':   dom_iav_ITCZ,
        'domain':   dom_SEA_Sc_sub_Sc,
        'domain':   dom_iav_trades,
        'domain':   dom_DYA_4km,
        'plot_order':'resolution',
        # this is pptx wide screen resolution
        'figsize':  (11.00*stretch,7.0*stretch),
        'nrows':    2,
        'ncols':    3,
        'snapshots':{'on':1,
                     'freq':timedelta(minutes=60),
                     'max_back':timedelta(days=1),},
        'hide_colorbar':True,



        #'nrows':    3,
        #'ncols':    4,
        #'domain':   dom_iav_trades,
        #'figsize':  (13.0*stretch,9.0*stretch),
        #'domain':   dom_DYA_4km,
        #'figsize':  (13.0*stretch,10.0*stretch),

    },

    'sensitivity':  {
        'subplts':  {'left':0.08,  'bottom':0.21,
                     'right':0.98, 'top':0.95,
                     'wspace':0.10,'hspace':0.20},
        'use_sims': mem_src['sensitivity'],
        #'domain':   dom_SEA_Sc,
        #'domain':   dom_iav_ITCZ,
        'plot_order':'resolution',
        'nrows':    3,
        'ncols':    4,
        'domain':   dom_iav_trades,
        'figsize':  (13.0*stretch,9.0*stretch),

        'domain':   dom_SA_3km,
        'figsize':  (13.0*stretch,10.0*stretch),
        'snapshots':{'on':0},
    },

    'iav':  {
        #'subplts':  {'left':0.08,  'bottom':0.25,
        #             'right':0.98, 'top':0.96,
        #             'wspace':0.02,'hspace':0.20},
        'subplts':  {'left':0.08,  'bottom':0.21,
                     'right':0.98, 'top':0.96,
                     'wspace':0.02,'hspace':0.20},
        'use_sims': mem_src['iav'],
        #'use_sims': {},
        #'domain':   dom_iav_trades,
        'domain':   dom_SA_3km,
        'plot_order':'time',
        #'plot_order':'resolution',
        #'figsize':  (13.9*stretch,7.0*stretch),
        'figsize':  (14*stretch,9.5*stretch),
        'nrows':    3,
        'ncols':    5,
        #'nrows':    3,
        #'ncols':    5,
        'snapshots':{'on':0},
    },

}

cfg = run_configs[run_mode]
cfg.update(var_configs[plot_var])
var_name = plot_var
# update nlp
nlp['panel_labels_start_ind'] = cfg['panel_labels_start_ind']
nlp['panel_labels_shift_right'] = cfg['panel_labels_shift_right']
nlp['plot_order']  = cfg['plot_order'] 
nlp['figsize']  = cfg['figsize'] 
nlp['cmap']     = nlp['cmaps'][cfg['cmap']] 
nlp['nrows']    = cfg['nrows'] 
nlp['ncols']    = cfg['ncols'] 
