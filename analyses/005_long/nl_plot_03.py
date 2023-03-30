#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    plotting namelist for 004_09_timeline:
author			Christoph Heim
date created    25.11.2019
date changed    16.11.2021
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

nlp['mem_colors'] = {
    'MPI-ESM1-2-HR': 'orange',
}

nlp['mem_group_colors'] = {
    'CMIP6':'black',
    'COSMO':'red',
}
nlp['regression_mem_groups'] = ['CMIP6']

nlp['ref_color'] = '#000000'


#nlp['xlim'] = {
#    TP.DIURNAL_CYCLE:   (0,24),
#    TP.ANNUAL_CYCLE:    (1,12),
#    TP.DAILY_SERIES:    None,
#    TP.MONTHLY_SERIES:  None,
#}
#
#nlp['time_key'] = {
#    TP.DIURNAL_CYCLE:   'hour',
#    TP.ANNUAL_CYCLE:    'month',
#    TP.DAILY_SERIES:    'time',
#    TP.MONTHLY_SERIES:  'time',
#}
#
#nlp['linewidths'] = {
#    TP.DIURNAL_CYCLE:{
#        TP.MEAN:    1.5,
#    },
#    TP.ANNUAL_CYCLE:{
#        TP.MEAN:    1.5,
#        '2006':     0.5,
#        '2007':     0.5,
#        '2008':     0.5,
#        '2009':     0.5,
#    },
#}

nlp['markersize'] = {
    TP.ALL_TIME:        30.0,
    TP.YEARLY_SERIES:   20.0,
    TP.MONTHLY_SERIES:  10.0,
}

## panel labels
nlp['panel_labels_start_ind'] = 0
nlp['panel_labels_shift_right'] = -0.16
nlp['panel_labels_shift_up'] = 0.02
nlp['panel_labels_fontsize'] = 15


# linear regression
#nlp['regr_color']        = 'black'
nlp['regr_linewidth']    = 1
