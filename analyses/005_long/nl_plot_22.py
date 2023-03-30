#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    plotting namelist for 004_01_spatial:
author			Christoph Heim
date created    18.11.2019
date changed    26.11.2021
usage			import in another script
"""
###############################################################################
import matplotlib.pyplot as plt
import cartopy
import numpy as np
from base.nl_plot_global import cmap_RdBu_r_positive
###############################################################################
nlp = {}

nlp['geo_plot']     = True
#nlp['geo_plot']     = False

#### PLOT RESOLUTION
nlp['dpi'] = 600

# very important to use pcolormesh for lwp snapshots!!
# takes ages with contourf and looks bad
nlp['2D_type'] = 'pcolormesh'
#nlp['2D_type'] = 'contourf'

plt.rcParams['axes.titlesize'] = 13
plt.rcParams['font.size'] = 13
plt.rcParams['xtick.labelsize'] = 11
plt.rcParams['ytick.labelsize'] = 11

# transparent plot background
#nlp['transparent_bg'] = True
#COLOR = 'white'
nlp['transparent_bg'] = False
COLOR = 'black'
plt.rcParams['xtick.color'] = COLOR
plt.rcParams['axes.labelcolor'] = COLOR
plt.rcParams['ytick.color'] = COLOR
plt.rcParams['text.color'] = COLOR


#### CARTOPY
nlp['projection']   = cartopy.crs.PlateCarree()
nlp['map_margin']   = (0,0,0,0) # lon0, lon1, lat0, lat1
nlp['land_color']           = (0.6,0.6,0.6)
nlp['ocean_color']          = (0,0.3,1,0.5)
nlp['river_color']          = (0,0.2,0.7,0.3)




# panel labels
nlp['i_draw_panel_labels'] = 0
nlp['panel_labels_fontsize'] = 14
nlp['panel_labels_start_ind'] = 12
nlp['panel_labels_start_ind'] = 11
nlp['panel_labels_start_ind'] = 0






# configuration of subplots
nlp['subplts_cfgs'] = {
    '1x1':  {
        'left':0.20,
        'bottom':0.10,
        'right':0.95,
        'top':0.95,
        'wspace':0.02,
        'hspace':0.20
    },
    '1x2':  {
        'left':0.07,
        'bottom':0.16,
        'right':0.99,
        'top':0.98,
        'wspace':0.04,
        'hspace':0.20
    },
    '1x3':  {
        'left':0.06,
        'bottom':0.20,
        'right':0.99,
        'top':0.90,
        'wspace':0.05,
        'hspace':0.10
    },
    '1x4':  {
        'left':0.06,
        'bottom':0.20,
        'right':0.99,
        'top':0.90,
        'wspace':0.05,
        'hspace':0.10
    },
    '2x2':  {
        'left':0.13,
        'bottom':0.25,
        'right':0.98,
        'top':0.95,
        'wspace':0.02,
        'hspace':0.20
    },
    '2x3':  {
        'left':0.07,
        'bottom':0.10,
        'right':0.91,
        'top':0.95,
        'wspace':0.60,
        'hspace':0.40
    },
    '2x4':  {
        'left':0.06,
        'bottom':0.20,
        'right':0.99,
        'top':0.90,
        'wspace':0.05,
        'hspace':0.20
    },
    '2x6':  {
        'left':0.08,
        'bottom':0.21,
        'right':0.98,
        'top':0.96,
        'wspace':0.02,
        'hspace':0.20
    },
    '3x3':  {
        'left':0.06,
        'bottom':0.05,
        'right':0.98,
        'top':0.96,
        'wspace':0.20,
        'hspace':0.30
    },
    '3x4':  {
        'left':0.08,
        'bottom':0.21,
        'right':0.98,
        'top':0.96,
        'wspace':0.02,
        'hspace':0.20
    },
    '4x6':  {
        'left':0.08,
        'bottom':0.21,
        'right':0.98,
        'top':0.96,
        'wspace':0.02,
        'hspace':0.20
    },
    '6x5':  {
        'left':0.08,
        'bottom':0.06,
        'right':0.98,
        'top':0.96,
        'wspace':0.02,
        'hspace':0.20
    },

}


### VARIABLE PLOT CONFIGURATIONS
##############################################################################
from nl_plot_01 import nlp as nlp_01
nlp['cmaps'] = nlp_01['cmaps']
nlp['levels'] = nlp_01['levels']
nlp['cb_ticks'] = nlp_01['cb_ticks']
nlp['oom'] = nlp_01['oom']
#nlp['cmaps'] = {
#    'abs':{},'diff':{},'bias':{},'rel':{},
#}
#nlp['levels'] = {
#    'abs':{},'diff':{},'bias':{},'rel':{},
#}
#nlp['cb_ticks'] = {
#    'abs':{},'diff':{},'bias':{},'rel':{},
#}
#nlp['oom'] = {
#    'abs':{},'diff':{},'bias':{},'rel':{},
#}


##############################################################################
for var_name in ['U']:
    range = 30
    delta = 5
    nlp['cmaps'     ]['abs' ][var_name] = 'RdBu_r' 
    nlp['levels'    ]['abs' ][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['abs' ][var_name] = nlp['levels']['abs'][var_name][::2]
    range = 7
    delta = 1
    nlp['cmaps'     ]['diff'][var_name] = 'RdBu_r' 
    nlp['levels'    ]['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['diff'][var_name] = nlp['levels']['diff'][var_name][::2]

##############################################################################
for var_name in ['V']:
    range = 10
    delta = 2
    nlp['cmaps'     ]['abs' ][var_name] = 'RdBu_r' 
    nlp['levels'    ]['abs' ][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['abs' ][var_name] = nlp['levels']['abs'][var_name][::2]
    range = 2.5
    delta = 0.5
    nlp['cmaps'     ]['diff'][var_name] = 'RdBu_r' 
    nlp['levels'    ]['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['diff'][var_name] = nlp['levels']['diff'][var_name][::2]

##############################################################################
for var_name in ['T']:
    range = 10
    delta = 2
    nlp['cmaps'     ]['abs' ][var_name] = 'Reds' 
    nlp['levels'    ]['abs' ][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['abs' ][var_name] = nlp['levels']['abs'][var_name][::2]
    range = 7
    delta = 1
    nlp['cmaps'     ]['diff'][var_name] = cmap_RdBu_r_positive 
    nlp['levels'    ]['diff'][var_name] = np.arange(0,range+delta,delta)
    nlp['cb_ticks'  ]['diff'][var_name] = nlp['levels']['diff'][var_name]

##############################################################################
for var_name in ['RH']:
    range = 10
    delta = 2
    nlp['cmaps'     ]['abs' ][var_name] = 'RdBu_r' 
    nlp['levels'    ]['abs' ][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['abs' ][var_name] = nlp['levels']['abs'][var_name][::2]
    range = 16
    delta = 4
    nlp['cmaps'     ]['diff'][var_name] = 'RdBu_r' 
    nlp['levels'    ]['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['diff'][var_name] = nlp['levels']['diff'][var_name][::2]

##############################################################################
for var_name in ['ALBEDO']:
    #min = 0.15
    #max = 0.40
    #delta = 0.025
    min = 15
    max = 40
    delta = 2.5
    nlp['cmaps'     ]['abs' ][var_name] = 'cubehelix' 
    nlp['levels'    ]['abs' ][var_name] = np.arange(min,max+delta,delta)
    nlp['cb_ticks'  ]['abs' ][var_name] = nlp['levels']['abs'][var_name][::2]
    #range = 0.05
    #delta = 0.01
    range = 5
    delta = 1
    nlp['cmaps'     ]['diff'][var_name] = 'RdBu_r' 
    nlp['levels'    ]['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['diff'][var_name] = nlp['levels']['diff'][var_name][::2]
    #range = 10
    #delta = 2
    range = 30
    delta = 6
    nlp['cmaps'     ]['bias'][var_name] = 'RdBu_r' 
    nlp['levels'    ]['bias'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['bias'][var_name] = nlp['levels']['bias'][var_name][::2]

##############################################################################
for var_name in ['LWUTOA']:
    min = 210
    max = 290
    delta = 10
    nlp['cmaps'     ]['abs' ][var_name] = 'gnuplot2' 
    nlp['levels'    ]['abs' ][var_name] = np.arange(min,max+delta,delta)
    nlp['cb_ticks'  ]['abs' ][var_name] = nlp['levels']['abs'][var_name][::2]
    range = 36
    delta = 5
    nlp['cmaps'     ]['diff'][var_name] = 'RdBu_r' 
    nlp['levels'    ]['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['diff'][var_name] = nlp['levels']['diff'][var_name][::2]
    range = 36
    delta = 6
    nlp['cmaps'     ]['bias'][var_name] = 'RdBu_r' 
    nlp['levels'    ]['bias'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['bias'][var_name] = nlp['levels']['bias'][var_name][::2]

##############################################################################
for var_name in ['PP']:
    min = 0
    max = 10
    delta = 2
    nlp['cmaps'     ]['abs' ][var_name] = 'plasma' 
    nlp['levels'    ]['abs' ][var_name] = np.arange(min,max+delta,delta)
    nlp['cb_ticks'  ]['abs' ][var_name] = nlp['levels']['abs'][var_name][::2]
    range = 3
    delta = 0.6
    nlp['cmaps'     ]['diff'][var_name] = 'RdBu_r' 
    nlp['levels'    ]['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['diff'][var_name] = nlp['levels']['diff'][var_name][::2]
    range = 4
    delta = 0.8
    nlp['cmaps'     ]['bias'][var_name] = 'RdBu_r' 
    nlp['levels'    ]['bias'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['bias'][var_name] = nlp['levels']['bias'][var_name][::2]
    range = 50
    delta = 10
    nlp['cmaps'     ]['rel'][var_name] = 'RdBu_r' 
    nlp['levels'    ]['rel'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['rel'][var_name] = nlp['levels']['rel'][var_name][::2]

##############################################################################
for var_name in ['CLCH','CLCM','CLCL']:
    min = 10
    max = 70
    delta = 5
    nlp['cmaps'     ]['abs' ][var_name] = 'cubehelix' 
    nlp['levels'    ]['abs' ][var_name] = np.arange(min,max+delta,delta)
    nlp['cb_ticks'  ]['abs' ][var_name] = nlp['levels']['abs'][var_name][::2]
    range = 10
    delta = 2
    nlp['cmaps'     ]['diff'][var_name] = 'RdBu_r' 
    nlp['levels'    ]['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['diff'][var_name] = nlp['levels']['diff'][var_name][::2]
    #range = 4
    #delta = 0.8
    #nlp['cmaps'     ]['bias'][var_name] = 'RdBu_r' 
    #nlp['levels'    ]['bias'][var_name] = np.arange(-range+delta/2,range,delta)
    #nlp['cb_ticks'  ]['bias'][var_name] = nlp['levels']['bias'][var_name][::2]

##############################################################################
for var_name in ['SWNDTOA']:
    min = 250
    max = 360
    delta = 10
    nlp['cmaps'     ]['abs' ][var_name] = 'gnuplot2' 
    nlp['levels'    ]['abs' ][var_name] = np.arange(min,max+delta,delta)
    nlp['cb_ticks'  ]['abs' ][var_name] = nlp['levels']['abs'][var_name][::2]
    range = 20
    delta = 4
    nlp['cmaps'     ]['diff'][var_name] = 'RdBu_r' 
    nlp['levels'    ]['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['diff'][var_name] = nlp['levels']['diff'][var_name][::2]

##############################################################################
for var_name in ['CSWNDTOA']:
    min = 320
    max = 380
    delta = 10
    nlp['cmaps'     ]['abs' ][var_name] = 'gnuplot2' 
    nlp['levels'    ]['abs' ][var_name] = np.arange(min,max+delta,delta)
    nlp['cb_ticks'  ]['abs' ][var_name] = nlp['levels']['abs'][var_name][::2]
    range = 5
    delta = 1
    nlp['cmaps'     ]['diff'][var_name] = 'RdBu_r' 
    nlp['levels'    ]['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['diff'][var_name] = nlp['levels']['diff'][var_name][::2]

##############################################################################
for var_name in ['CRESWNDTOA']:
    min = 250
    max = 360
    delta = 10
    nlp['cmaps'     ]['abs' ][var_name] = 'gnuplot2' 
    nlp['levels'    ]['abs' ][var_name] = np.arange(min,max+delta,delta)
    nlp['cb_ticks'  ]['abs' ][var_name] = nlp['levels']['abs'][var_name][::2]
    range = 20
    delta = 4
    #range = 24
    #delta = 4
    nlp['cmaps'     ]['diff'][var_name] = 'RdBu_r' 
    nlp['levels'    ]['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['diff'][var_name] = nlp['levels']['diff'][var_name][::2]

##############################################################################
for var_name in ['LWDTOA']:
    min = -290
    max = -210
    delta = 10
    nlp['cmaps'     ]['abs' ][var_name] = 'gnuplot2' 
    nlp['levels'    ]['abs' ][var_name] = np.arange(min,max+delta,delta)
    nlp['cb_ticks'  ]['abs' ][var_name] = nlp['levels']['abs'][var_name][::2]
    range = 12
    delta = 2
    nlp['cmaps'     ]['diff'][var_name] = 'RdBu_r' 
    nlp['levels'    ]['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['diff'][var_name] = nlp['levels']['diff'][var_name][::2]

##############################################################################
for var_name in ['CLWDTOA']:
    min = -305
    max = -270
    delta = 5
    nlp['cmaps'     ]['abs' ][var_name] = 'gnuplot2' 
    nlp['levels'    ]['abs' ][var_name] = np.arange(min,max+delta,delta)
    nlp['cb_ticks'  ]['abs' ][var_name] = nlp['levels']['abs'][var_name][::2]
    range = 5
    delta = 1
    nlp['cmaps'     ]['diff'][var_name] = 'RdBu_r' 
    nlp['levels'    ]['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['diff'][var_name] = nlp['levels']['diff'][var_name][::2]

##############################################################################
for var_name in ['CRELWDTOA']:
    min = -290
    max = -210
    delta = 10
    nlp['cmaps'     ]['abs' ][var_name] = 'gnuplot2' 
    nlp['levels'    ]['abs' ][var_name] = np.arange(min,max+delta,delta)
    nlp['cb_ticks'  ]['abs' ][var_name] = nlp['levels']['abs'][var_name][::2]
    range = 12
    delta = 2
    range = 24
    delta = 4
    nlp['cmaps'     ]['diff'][var_name] = 'RdBu_r' 
    nlp['levels'    ]['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['diff'][var_name] = nlp['levels']['diff'][var_name][::2]

##############################################################################
for var_name in ['TSURF']:
    min = 270
    max = 320
    delta = 10
    nlp['cmaps'     ]['abs' ][var_name] = 'gnuplot2' 
    nlp['levels'    ]['abs' ][var_name] = np.arange(min,max+delta,delta)
    nlp['cb_ticks'  ]['abs' ][var_name] = nlp['levels']['abs'][var_name][::2]
    range = 6
    delta = 1
    nlp['cmaps'     ]['diff'][var_name] = 'RdBu_r' 
    nlp['levels'    ]['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['diff'][var_name] = nlp['levels']['diff'][var_name][::2]
    range = 1
    delta = 0.25
    nlp['cmaps'     ]['bias'][var_name] = 'RdBu_r' 
    nlp['levels'    ]['bias'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['bias'][var_name] = nlp['levels']['bias'][var_name][::2]


##############################################################################
for var_name in ['LTS']:
    min = 15
    max = 25
    delta = 2
    nlp['cmaps'     ]['abs' ][var_name] = 'gnuplot2' 
    nlp['levels'    ]['abs' ][var_name] = np.arange(min,max+delta,delta)
    nlp['cb_ticks'  ]['abs' ][var_name] = nlp['levels']['abs'][var_name][::2]
    range = 3
    delta = 0.5
    nlp['cmaps'     ]['diff'][var_name] = 'RdBu_r' 
    nlp['levels'    ]['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['diff'][var_name] = nlp['levels']['diff'][var_name][::2]


##############################################################################
for var_name in ['W']:
    min = 15
    max = 25
    delta = 2
    nlp['cmaps'     ]['abs' ][var_name] = 'gnuplot2' 
    nlp['levels'    ]['abs' ][var_name] = np.arange(min,max+delta,delta)
    nlp['cb_ticks'  ]['abs' ][var_name] = nlp['levels']['abs'][var_name][::2]
    range = 20
    delta = 4
    nlp['cmaps'     ]['diff'][var_name] = 'RdBu_r' 
    nlp['levels'    ]['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['diff'][var_name] = nlp['levels']['diff'][var_name][::2]


##############################################################################
for var_name in ['RH']:
    min = 0
    max = 100
    delta = 10
    nlp['cmaps'     ]['abs' ][var_name] = 'gnuplot2' 
    nlp['levels'    ]['abs' ][var_name] = np.arange(min,max+delta,delta)
    nlp['cb_ticks'  ]['abs' ][var_name] = nlp['levels']['abs'][var_name][::2]
    range = 8
    delta = 2
    nlp['cmaps'     ]['diff'][var_name] = 'RdBu_r' 
    nlp['levels'    ]['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['diff'][var_name] = nlp['levels']['diff'][var_name][::2]


##############################################################################
for var_name in ['UV10M']:
    range = 10
    delta = 2
    nlp['cmaps'     ]['abs' ][var_name] = 'gnuplot2' 
    nlp['levels'    ]['abs' ][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['abs' ][var_name] = nlp['levels']['abs'][var_name][::2]
    range = 1
    delta = 0.2
    nlp['cmaps'     ]['diff'][var_name] = 'RdBu_r' 
    nlp['levels'    ]['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['diff'][var_name] = nlp['levels']['diff'][var_name][::2]


##############################################################################
for var_name in ['SST']:
    min = 270
    max = 310
    delta = 5
    nlp['cmaps'     ]['abs' ][var_name] = 'gnuplot2' 
    nlp['levels'    ]['abs' ][var_name] = np.arange(min,max+delta,delta)
    nlp['cb_ticks'  ]['abs' ][var_name] = nlp['levels']['abs'][var_name][::2]
    range = 4
    delta = 0.5
    nlp['cmaps'     ]['diff'][var_name] = 'RdBu_r' 
    nlp['levels'    ]['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['diff'][var_name] = nlp['levels']['diff'][var_name][::2]


##############################################################################
for var_name in ['SLHFLX']:
    min = 100
    max = 200
    delta = 10
    nlp['cmaps'     ]['abs' ][var_name] = 'gnuplot2' 
    nlp['levels'    ]['abs' ][var_name] = np.arange(min,max+delta,delta)
    nlp['cb_ticks'  ]['abs' ][var_name] = nlp['levels']['abs'][var_name][::2]
    range = 30
    delta = 6
    nlp['cmaps'     ]['diff'][var_name] = 'RdBu_r' 
    nlp['levels'    ]['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['diff'][var_name] = nlp['levels']['diff'][var_name][::2]


##############################################################################
for var_name in ['ENTR']:
    min = 0.0
    max = 0.01
    delta = 0.001
    nlp['cmaps'     ]['abs' ][var_name] = 'gnuplot2' 
    nlp['levels'    ]['abs' ][var_name] = np.arange(min,max+delta,delta)
    nlp['cb_ticks'  ]['abs' ][var_name] = nlp['levels']['abs'][var_name][::2]
    range = 0.005
    delta = 0.001
    nlp['cmaps'     ]['diff'][var_name] = 'RdBu_r' 
    nlp['levels'    ]['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['diff'][var_name] = nlp['levels']['diff'][var_name][::2]


##############################################################################
for var_name in ['INVHGT']:
    min = 0
    max = 1000
    delta = 100
    nlp['cmaps'     ]['abs' ][var_name] = 'gnuplot2' 
    nlp['levels'    ]['abs' ][var_name] = np.arange(min,max+delta,delta)
    nlp['cb_ticks'  ]['abs' ][var_name] = nlp['levels']['abs'][var_name][::2]
    range = 240
    delta = 40
    nlp['cmaps'     ]['diff'][var_name] = 'RdBu_r' 
    nlp['levels'    ]['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['diff'][var_name] = nlp['levels']['diff'][var_name][::2]











#### Copy as default bias = diff
for var_name in list(nlp['cmaps']['abs'].keys()):
    if var_name not in nlp['cmaps']['bias']:
        nlp['cmaps'     ]['bias'][var_name] = nlp['cmaps'     ]['diff'][var_name]
        nlp['levels'    ]['bias'][var_name] = nlp['levels'    ]['diff'][var_name]
        nlp['cb_ticks'  ]['bias'][var_name] = nlp['cb_ticks'  ]['diff'][var_name]
     

#nlp['var_plt_cfgs'] = {
#    'CLWUTOA': {
#        'lims': {
#            'abs':  [260,300],
#            'bias': [-5,5],
#            'diff': [-5,5],
#        },
#        'cmap':     {
#            'abs':  'gnuplot2',
#            'diff': 'RdBu_r',
#            'bias': 'RdBu_r',
#        },
#        'dlevcf': {
#            'abs':  3,
#            'diff': 1,
#            'bias': 1,
#        },
#        #'levelscf': {
#        #    'bias': np.arange(-36+3,36.1,6),
#        #},
#    },
#    'CRELWDTOA':{
#        'lims': {
#            'abs':  [0,80],
#            'diff': [-15,15], # change
#        },
#        'cmap':     {
#            'abs':  'OrRd',
#            'diff': 'RdBu_r',
#        },
#        'dlevcf': {
#            'diff': 3,
#        },
#    },
#    'TQC':{
#        'lims': {
#            'abs':  [0,80],
#            'diff': [-20,20],
#        },
#        'cmap':     {
#            'abs':  'cividis',
#            'diff': 'RdBu_r',
#        },
#    },
#    'SUBS':{
#        'lims': {
#            #'abs':  [-20,20],
#            #'diff': [-20,20], 
#            'abs':  [-60,60],
#            'diff': [-60,60],
#        },
#        'cmap':     {
#            'abs':  'RdBu_r',
#            'diff': 'RdBu_r',
#        },
#    },
#    'SUBSOMEGA':{
#        'lims': {
#            'abs':  [-2,2],
#            'diff': [-1,1],  # change
#            'diff': [-2,2],  # eval
#        },
#        'cmap':     {
#            'abs':  'RdBu_r',
#            'diff': 'RdBu_r',
#        },
#    },
#    'CLDWFLXLOWCLDBASE':{
#        'lims': {
#            'abs':  [-0.01,0.01],
#            'diff': [-0.01,0.01],
#        },
#        'cmap':     {
#            'abs':  'RdBu_r',
#            'diff': 'RdBu_r',
#        },
#    },
#    'CSWFLXLOWCLDBASE':{
#        'lims': {
#            'abs':  [-0.01,0.01],
#            'diff': [-0.01,0.01],
#        },
#        'cmap':     {
#            'abs':  'RdBu_r',
#            'diff': 'RdBu_r',
#        },
#    },
#    'LCL':{
#        'lims': {
#            'abs':  [400,700],
#            'diff': [-50,50],
#        },
#        'cmap':     {
#            'abs':  'terrain',
#            'diff': 'RdBu_r',
#        },
#    },
#    'LOWCLDBASE':{
#        'lims': {
#            'abs':  [200,1600],
#            'diff': [-200,200],
#        },
#        'cmap':     {
#            'abs':  'terrain',
#            'diff': 'RdBu_r',
#        },
#    },
#    'INVF':{
#        'lims': {
#            'abs':  [0.0,1.0],
#            'diff': [-0.2,0.2],
#        },
#        'cmap':     {
#            'abs':  'cubehelix',
#            'diff': 'RdBu_r',
#        },
#    },
#    'T2M':{
#        'lims': {
#            'abs':  [290,300],
#            #'diff': [-4,4],
#            'diff': [1,5],
#            'bias': [-3,3], # eval
#            #'diff': [-1.5,1.5], # change anomaly
#        },
#        'cmap':     {
#            'abs':  'viridis',
#            #'diff': 'RdBu_r',
#            'diff': 'Reds',
#            'bias': 'RdBu_r',
#        },
#    },
#    'TSURF':{
#        'lims': {
#            'abs':  [290,300],
#            #'diff': [1,5], # abs diff
#            'diff': [-1.5,1.5], # abs diff - ITCZ change
#            'bias': [-3,3], # eval
#        },
#        'cmap':     {
#            'abs':  'viridis',
#            #'diff': 'Reds',
#            'diff': 'RdBu_r',
#            'bias': 'RdBu_r',
#        },
#        'dlevcf': {
#            'abs':  2,
#            'diff': 0.2,
#            'bias': 0.5       
#        },
#    },
#    'LTS':{
#        'lims': {
#            'abs':  [15,25],
#            'diff': [-3,3],
#            'bias': [-3,3],
#        },
#        'cmap':     {
#            'abs':  'viridis',
#            'diff': 'RdBu_r',
#            'bias': 'RdBu_r',
#        },
#    },
#    'UV':{
#        'lims': {
#            'abs':  [2,12],
#            'diff': [-0.8,0.8],
#            'bias': [-2,2],
#        },
#        'cmap':     {
#            #'abs':  'plasma',
#            'abs':  'BuGn',
#            'diff': 'RdBu_r',
#            'bias': 'RdBu_r',
#        },
#        'dlevcf': {
#            'abs':  1.0,
#            'diff': 0.2,
#            'bias': 0.5,
#        },
#    },
#    'UV10M':{
#        'lims': {
#            'abs':  [2,9],
#            'diff': [-1,1], # change
#            'diff': [-5,5], # eval
#        },
#        'cmap':     {
#            'abs':  'nipy_spectral',
#            'diff': 'RdBu_r',
#        },
#    },
#    'CAPE':{
#        'lims': {
#            'abs':  [0,1200],
#            'diff': [-300,300],
#        },
#        'cmap':     {
#            'abs':  'viridis',
#            'diff': 'RdBu_r',
#        },
#    },
#    'CIN':{
#        'lims': {
#            'abs':  [0,100],
#            'diff': [-50,50],
#        },
#        'cmap':     {
#            'abs':  'viridis',
#            'diff': 'RdBu_r',
#        },
#    },
#    'T':{
#        'lims': {
#            #'abs':  [264,271],
#            #'diff': [3.5,6],
#            ## @alt=300
#            'abs':  [290,300],
#            'diff': [1.5,3],
#            'bias': [-1.5,1.5],
#            ## @alt=3000
#            'abs':  [280,290],
#            'diff': [2.5,4.5],
#            'bias': [-1.5,1.5],
#            ## @alt=13000
#            'abs':  [210,223],
#            'diff': [4,7.5],
#            'bias': [-1.5,1.5],
#        },
#        'cmap':     {
#            #'abs':  'plasma',
#            'abs':  'PuRd',
#            'diff': 'RdBu_r',
#            'bias': 'RdBu_r',
#        },
#        'dlevcf': {
#            'abs':  1.0,
#            'diff': 0.25,
#            'bias': 0.25,
#        },
#    },
#    'U':{
#        'lims': {
#            'abs':  [-30,30],
#            'diff': [-6,6],
#        },
#        'cmap':     {
#            'abs':  'RdBu_r',
#            'diff': 'RdBu_r',
#        },
#        'dlevcf': {
#            'abs':  10,
#            #'bias': 5,
#            'diff': 1,
#        },
#    },
#    'V':{
#        'lims': {
#            'abs':  [-10,10],
#            'diff': [-2,2],
#            'bias': [-2,2],
#        },
#        'cmap':     {
#            'abs':  'RdBu_r',
#            'diff': 'RdBu_r',
#            'bias': 'RdBu_r',
#        },
#        'dlevcf': {
#            'abs':  2,
#            'diff': 0.5,
#            'bias': 0.5,
#        },
#    },
#    'UVDIV':{
#        'lims': {
#            'abs':  [-1E-5,1E-5],
#            'diff': [-1E-5,1E-5],
#        },
#        'cmap':     {
#            'abs':  'RdBu_r',
#            'diff': 'RdBu_r',
#        },
#    },
#    'RH':{
#        'lims': {
#            'abs':  [0,100],
#            'diff': [-16,16],
#            'bias': [-16,16],
#        },
#        'cmap':     {
#            'abs':  'PuRd',
#            'diff': 'RdBu_r',
#            'bias': 'RdBu_r',
#        },
#        'dlevcf': {
#            'abs':  10,
#            'diff': 4,
#            'bias': 4,
#        },
#    },
#    'CLDF':{
#        'lims': {
#            'abs':  [0,20],
#            'diff': [-20,20],
#            #'bias': [-20,20],
#        },
#        'cmap':     {
#            'abs':  'nipy_spectral',
#            'diff': 'RdBu_r',
#            #'bias': 'RdBu_r',
#        },
#        'dlevcf': {
#            'abs':  4,
#            #'bias': 2,
#            'diff': 4,
#        },
#    },
#    'QV':{
#        'lims': {
#            'abs':  [0,10],
#            'diff': [-2,2],
#            'bias': [-2,2],
#        },
#        'cmap':     {
#            'abs':  'nipy_spectral',
#            'diff': 'RdBu_r',
#            'bias': 'RdBu_r',
#        },
#        'dlevcf': {
#            'abs':  1,
#            'diff': 0.25,
#            'bias': 0.25,
#        },
#    },
#    'QVFT':{
#        'lims': {
#            'abs':  [0,4],
#            'diff': [-2,2],
#        },
#        'cmap':     {
#            'abs':  'nipy_spectral',
#            'diff': 'RdBu_r',
#        },
#    },
#    'TQI':{
#        'lims': {
#            'abs':  [0,30],
#            'diff': [-20,20],
#        },
#        'cmap':     {
#            'abs':  'cividis',
#            'diff': 'RdBu_r',
#        },
#    },
#    'QV2M':{
#        'lims': {
#            'abs':  [0,30],
#            'diff': [-3,3],
#        },
#        'cmap':     {
#            'abs':  'inferno',
#            'diff': 'RdBu_r',
#        },
#    },
#    'TQV':{
#        'lims': {
#            'abs':  [0,60],
#            'diff': [-20,20],
#        },
#        'cmap':     {
#            'abs':  'gnuplot2',
#            'diff': 'RdBu_r',
#        },
#    },
#    'INVSTRV':{
#        'min_max'   :(None,None),
#        'min_max_bias':(-5,5),
#        'cmap'      :'cubehelix',
#    },
#    'CLCL2':{
#        'min_max'   :(0,1),
#        'cmap'      :'cubehelix',
#    },
#    'INVSTRA':{
#        'min_max'   :(None,None),
#        'cmap'      :'cubehelix',
#    },
#    'CORREFL':{
#        'min_max'   :(0,0.10),
#        'cmap'      :'clouds',
#    },
#}
#
#
#
#var_grp_plt_cfgs = {
#    'SW_down':{
#        'var_names':    [
#                        'SWNDTOA', 
#                        'SWDTOA', 
#                        'CSWNDTOA', 
#                        ],
#        'lims': {
#            'abs':  [250,360],
#            'diff': [-30,30],
#            #'diff': [-20,20], # change
#        },
#        'cmap':     {
#            'abs':  'gnuplot2',
#            'diff': 'RdBu_r',
#        },
#        'dlevcf':     {
#            'abs':  10,
#            'diff': 5,
#        },
#    },
#    'LW_down':{
#        'var_names':    [
#                        'LWDTOA', 'CLWDTOA', 
#                        'LWNDSFC', 'CLWNDSFC',
#                        ],
#        'lims': {
#            'abs':  [-290,-210],
#            'diff': [-15,15],
#        },
#        'cmap':     {
#            'abs':  'gnuplot2',
#            'diff': 'RdBu_r',
#            'bias': 'RdBu_r',
#        },
#        'dlevcf': {
#            'abs':  10,
#            #'bias': 5,
#            'diff': 3,
#        },
#        'levelscf': {
#            'bias': np.arange(-36+3,36,6),
#        },
#    },
#    'rad_flux_up':{
#        'var_names':    [
#                        'LWUTOA',
#                        #'CLWUTOA',
#                        'SWUTOA', 'CSWUTOA',
#                        'SWNUSFC',
#                        'LWNUSFC',],
#        'lims': {
#            'abs':  [210,290],
#            'bias': [-36,36],
#            'diff': [-20,20],
#        },
#        'cmap':     {
#            'abs':  'gnuplot2',
#            'diff': 'RdBu_r',
#            'bias': 'RdBu_r',
#        },
#        'dlevcf': {
#            'abs':  10,
#            'diff': 5,
#            'bias': 8,
#        },
#        #'levelscf': {
#        #    'bias': np.arange(-36+3,36.1,6),
#        #},
#    },
#    'net_rad_flux_down':{
#        'var_names':    [
#                        'RADNDTOA', 'CRADNDTOA', 
#                        ],
#        'lims': {
#            'abs':  [0,80],
#            'diff': [-30,30],
#            #'diff': [-20,20], # change
#        },
#        'cmap':     {
#            'abs':  'gnuplot2',
#            'diff': 'RdBu_r',
#        },
#    },
#    'CREdown':{
#        'var_names':    [
#                        #'SWNDTOA',
#                        'CRESWNDTOA', 'CRERADNDTOA',],
#        'lims': {
#            'abs':  [-100,0],
#            'diff': [-40,40],
#            'diff': [-15,15], # change
#        },
#        'cmap':     {
#            'abs':  'RdBu_r',
#            'abs':  'GnBu_r',
#            'diff': 'RdBu_r',
#        },
#        'dlevcf': {
#            'diff': 3,
#        },
#    },
#    'sfc_fluxes':{
#        'var_names':    ['SLHFLX', 'SSHFLX', 'ENFLXNUSFC'],
#        'lims': {
#            'abs':  [0,200],
#            'diff': [-30,30],
#        },
#        'cmap':     {
#            'abs':  'gnuplot2',
#            'diff': 'RdBu_r',
#        },
#    },
#    'TQX':{
#        'var_names':    [
#                        'TQR', 'TQS', 'TQG'],
#        'lims': {
#            'abs':  [0,400],
#            'diff': [-200,200],
#        },
#        'cmap':     {
#            'abs':  'gnuplot2_r',
#            'diff': 'RdBu_r',
#        },
#    },
#}
#for grp_key,grp in var_grp_plt_cfgs.items():
#    for var_name in grp['var_names']:
#        nlp['var_plt_cfgs'][var_name] = {
#            'lims':     grp['lims'],
#            'cmap':     grp['cmap'],
#        }
#        if 'dlevcf' in grp:
#            nlp['var_plt_cfgs'][var_name]['dlevcf'] = grp['dlevcf']
#        if 'levelscf' in grp:
#            nlp['var_plt_cfgs'][var_name]['levelscf'] = grp['levelscf']
#            
#
#for var_name in ['POTTDIV3','CSPOTTDIV3','NCOLIPOTTDIV3']:
#    nlp['var_plt_cfgs'][var_name] = \
#    {
#        'lims': {
#            'abs':  [-4,4],
#            'diff': [-4,4],
#        },
#        'cmap':     {
#            'abs':  'PRGn_r',
#            'diff': 'RdBu_r',
#        },
#        'dlevcf':     {
#            'abs':  0.5,
#            'diff': 0.5,
#        },
#    }
#nlp['var_plt_cfgs']['QI'] = \
#{
#    'lims': {
#        #'abs':  [ 0.00,0.01],
#        #'diff': [-0.01,0.01],
#        'abs':  [ 0.00,0.03],
#        'diff': [-0.03,0.03],
#    },
#    'cmap':     {
#        'abs':  'gnuplot2',
#        'diff': 'RdBu_r',
#    },
#    'dlevcf':     {
#        #'abs':  0.001,
#        #'diff': 0.001,
#        'abs':  0.005,
#        'diff': 0.005,
#    },
#}
#nlp['var_plt_cfgs']['RADNDTOA'] = \
#{
#    'lims': {
#        'abs':  [-100,100],
#        'diff': [-40,40],
#    },
#    'cmap':     {
#        'abs':  'RdBu_r',
#        'diff': 'RdBu_r',
#    },
#}
