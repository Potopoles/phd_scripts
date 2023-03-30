#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    plotting namelist for 005_10_csalttime:
author			Christoph Heim
date crated     06.04.2022
date changed    06.04.2022
usage			import in another script
"""
###############################################################################
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import cartopy
import numpy as np
from package.time_processing import Time_Processing as TP
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
###############################################################################
nlp = {}

nlp['geo_plot']     = False

#### PLOT RESOLUTION
nlp['dpi'] = 600

plt.rcParams['axes.titlesize'] = 14
plt.rcParams['font.size'] = 13
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
#plt.rcParams['axes.labelsize'] = 12 # does not work from here
plt.rcParams['legend.fontsize'] = 10


nlp['ylims'] = {
    'ALBEDO': [0.14,0.32],
    #'LWUTOA': [230,290],
    'INVHGT': [1100,1900],
    'LCLDTOP': [1100,1900],
}

# transparent plot background
#nlp['transparent_bg'] = True
#COLOR = 'white'
nlp['transparent_bg'] = False
COLOR = 'black'
plt.rcParams['xtick.color'] = COLOR
plt.rcParams['axes.labelcolor'] = COLOR
plt.rcParams['ytick.color'] = COLOR
plt.rcParams['text.color'] = COLOR



nlp['cmaps'] = {
    'cf':{'abs':{},'diff':{}},
}
nlp['levels'] = {
    'cf':{'abs':{},'diff':{}},
}
nlp['cb_ticks'] = {
    'cf':{'abs':{},'diff':{}},
}


######### variable CLDMASK
##############################################################################

cmap = plt.cm.PiYG
my_cmap = cmap(np.linspace(0.50, 1.00, cmap.N))
my_cmap[:,-1] = np.linspace(0.5, 1.0, cmap.N)
my_cmap = ListedColormap(my_cmap)
var_name = 'CLDMASK'
nlp['cmaps']['cf']['abs'][var_name] = my_cmap
nlp['levels']['cf']['abs'][var_name] = np.linspace(0, 30, 10)
nlp['cb_ticks']['cf']['abs'][var_name] = nlp['levels']['cf']['abs'][var_name]

cmap = plt.cm.PiYG_r
#cmap = plt.cm.BrBG_r
my_cmap = cmap(np.linspace(0.00, 1.00, cmap.N))
#my_cmap[:,-1] = np.linspace(0.0, 0.6, cmap.N)
my_cmap[:,-1] = (np.linspace(-1.0, 1.0, cmap.N)**2)**(1/2)
my_cmap = ListedColormap(my_cmap)
nlp['cmaps']['cf']['diff'][var_name] = my_cmap
nlp['levels']['cf']['diff'][var_name] = np.linspace(-1E-2, 1E-2, 100)
nlp['cb_ticks']['cf']['diff'][var_name] = nlp['levels']['cf']['diff'][var_name]



nlp['tick_locator'] = {
    TP.DIURNAL_CYCLE:   ticker.FixedLocator([0,3,6,9,12,15,18,21,24]),
    TP.ANNUAL_CYCLE:    ticker.FixedLocator([1,2,3,4,5,6,7,8,9,10,11,12]),
    TP.DAILY_SERIES:    mdates.AutoDateLocator(),
    TP.MONTHLY_SERIES:  mdates.AutoDateLocator(),
}

nlp['xlim'] = {
    TP.DIURNAL_CYCLE:   (0,24),
    TP.ANNUAL_CYCLE:    (1,12),
    TP.DAILY_SERIES:    None,
    TP.MONTHLY_SERIES:  None,
}

nlp['time_key'] = {
    TP.DIURNAL_CYCLE:   'hour',
    TP.ANNUAL_CYCLE:    'month',
    TP.DAILY_SERIES:    'time',
    TP.MONTHLY_SERIES:  'time',
}

nlp['linewidths'] = {
    TP.DIURNAL_CYCLE:{
        TP.MEAN:    1.5,
    },
    TP.ANNUAL_CYCLE:{
        TP.MEAN:    1.5,
        '2006':     0.5,
        '2007':     0.5,
        '2008':     0.5,
        '2009':     0.5,
    },
    TP.DAILY_SERIES:{
        TP.MEAN:    2.0,
    },
    TP.MONTHLY_SERIES:{
        TP.MEAN:    2.0,
    },
}


nlp['markersize'] = {
    TP.DIURNAL_CYCLE:{
        TP.MEAN:    3.0,
    },
    TP.ANNUAL_CYCLE:{
        TP.MEAN:    2.5,
        '2006':     0.0,
        '2007':     0.0,
        '2008':     0.0,
        '2009':     0.0,
    },
    TP.DAILY_SERIES:{
        TP.MEAN:    3.0,
    },
    TP.MONTHLY_SERIES:{
        TP.MEAN:    3.0,
    },
}

nlp['spread'] = {
    'linewidth':    0.5,
    'opacity':      '50',
}

## panel labels
#nlp['panel_labels_start_ind'] = 12
nlp['panel_labels_start_ind'] = 0
nlp['panel_labels_shift_right'] = -0.16
nlp['panel_labels_shift_up'] = 0.02
nlp['panel_labels_fontsize'] = 15
#
#
## labels showing the bias MOD - OBS as spatial mean
#nlp['add_bias_labels'] = False
