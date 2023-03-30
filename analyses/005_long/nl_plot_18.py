#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    plotting namelist for 005_17:
author			Christoph Heim
date created    04.03.2022
date changed    04.03.2022
usage			import in another script
"""
###############################################################################
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import cartopy
import numpy as np
from package.time_processing import Time_Processing as TP
###############################################################################
nlp = {}

nlp['geo_plot']     = False

#### PLOT RESOLUTION
nlp['dpi'] = 600

plt.rcParams['axes.titlesize'] = 14
plt.rcParams['font.size'] = 13
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['legend.fontsize'] = 5

nlp['axlims'] = {
    #'INVHGT': [1100,1900],
    #'LCLDTOP': [1100,1900],
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


# colors
nlp['colors'] = plt.rcParams['axes.prop_cycle'].by_key()['color']
#nlp['mod_col_inds'] = ['COSMO', 'ERA5',
#                       ]
nlp['mem_col_inds'] = ['COSMO_3.3_pgw',  
                       'MPI-ESM1-2-HR']


## panel labels
nlp['panel_labels_start_ind'] = 0
nlp['panel_labels_shift_right'] = -0.16
nlp['panel_labels_shift_up'] = 0.02
nlp['panel_labels_fontsize'] = 15


# linear regression
#nlp['regr_color']        = 'black'
nlp['regr_linewidth']    = 1
