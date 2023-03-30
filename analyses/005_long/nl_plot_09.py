#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    plotting namelist for 004_09_timeline:
author			Christoph Heim
date created    21.11.2020
date changed    13.05.2022
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
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 8

nlp['ylims'] = dict(abs={}, diff={})

nlp['ylims']['abs'] = {
    #### no subtract mean
    #'ALBEDO':   [14,32],
    #'LWUTOA':   [230,290],
    #'PP':       [0,8],
    ### subtract mean
    'ALBEDO':   [-8,8],
    'LWUTOA':   [-20,20],
    'PP':       [-4,4],

    #'LWDTOA':   [-230,-290],
    #'PP':       [0,7],
    'INVHGT':   [1100,1900],
    'LCLDTOP':  [1100,1900],
}


nlp['ylims']['diff'] = {
    #'ALBEDO':   [-8,8],
    #'PP':       [-0.07,0.13],
    #'LWUTOA':   [-25,25],

    'ALBEDO':   [-9,9],
    'PP':       [-3.5,3.5],
    #'LWUTOA':   [-35,35],
    #'LWDTOA':   [-35,35],
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

nlp['mem_colors'] = {
    #'CTRL':                         nlp['colors'][3],
    'PGW':                          nlp['colors'][3],
    'PGW ITCZ$-$CTRL':              nlp['colors'][0],
    'PGW$-$CTRL':                   nlp['colors'][3],
    'PGW2$-$CTRL':                  nlp['colors'][2],
    'PGW3$-$CTRL':                  nlp['colors'][1],
    'MPI-ESM1-2-HR SSP5-8.5':       nlp['colors'][0],
    'MPI-ESM1-2-HR HIST':           nlp['colors'][0],
    'MPI-ESM1-2-HR SSP5-8.5 - HIST':nlp['colors'][0],
    #'CMIP6':                        '#999999',
    #'CMIP6 SSP5-8.5 - HIST':        '#999999',
    #'CM_SAF_MSG_AQUA_TERRA':        '#000000',

    'old pgw':                      nlp['colors'][2],
    '300hPa':                       nlp['colors'][1],
    'rdh2':                         nlp['colors'][0],

    ##### START CONFIG: Heim et al. 2022 Figs.6-8
    'CTRL':                         nlp['colors'][3],
    'ERA5':                         'orange',
    'CMIP6':                        nlp['colors'][0],
    'CERES 07-10':                  '#000000',
    'CERES 04-14':                  '#000000',
    'CM SAF 07-10':                 '#9c9c9c',
    'CM SAF 04-10':                 '#9c9c9c',
    'GPM 07-10':                    '#000000',
    'GPM 01-14':                    '#000000',
    ##### END CONFIG: Heim et al. 2022 Figs.6-8
}

nlp['mem_spread_colors'] = [
    #'#000000',
    #'#000000',

    ##### START CONFIG: Heim et al. 2022 Figs.6-8
    nlp['colors'][0],
    nlp['colors'][0],
    ##### END CONFIG: Heim et al. 2022 Figs.6-8
]

nlp['ref_color'] = '#000000'
#nlp['ref2_color'] = '#616161'
nlp['ref2_color'] = '#000000'

#nlp['ref_color'] = nlp['colors'][0]
#nlp['ref2_color'] = nlp['colors'][0] 

nlp['ref_linestyle'] = '-'
nlp['ref2_linestyle'] = '--'


nlp['mem_linestyles'] = {
    'COSMO_3.3_ctrl':               '-',
    'COSMO_3.3_pgw':                '--',
    'MPI-ESM1-2-HR_historical':     '-',
    'MPI-ESM1-2-HR_ssp585':         '--',
    'CERES 07-10':                  '-',
    'CERES 04-14':                  '--',
    'GPM 07-10':                    '-',
    'GPM 01-14':                    '--',
    'CM SAF 07-10':                 '-',
    'CM SAF 04-10':                 '--',
}




nlp['tick_locator'] = {
    TP.DIURNAL_CYCLE:   ticker.FixedLocator([0,3,6,9,12,15,18,21,24]),
    TP.ANNUAL_CYCLE:    ticker.FixedLocator([1,2,3,4,5,6,7,8,9,10,11,12]),
    TP.DAILY_SERIES:    mdates.AutoDateLocator(),
    TP.MONTHLY_SERIES:  mdates.AutoDateLocator(),
    TP.YEARLY_SERIES:   mdates.AutoDateLocator(),
}

nlp['xlim'] = {
    TP.DIURNAL_CYCLE:   (0,24),
    TP.ANNUAL_CYCLE:    (1,12),
    TP.DAILY_SERIES:    None,
    TP.MONTHLY_SERIES:  None,
    TP.YEARLY_SERIES:   None,
}

nlp['time_key'] = {
    TP.DIURNAL_CYCLE:   'hour',
    TP.ANNUAL_CYCLE:    'month',
    TP.DAILY_SERIES:    'time',
    TP.MONTHLY_SERIES:  'time',
    TP.YEARLY_SERIES:   'time',
}

nlp['linewidths'] = {
    TP.HOURLY_SERIES:{
        TP.MEAN:    1.5,
    },
    TP.DIURNAL_CYCLE:{
        TP.MEAN:    1.5,
    },
    TP.ANNUAL_CYCLE:{
        TP.MEAN:    1.5,
        '2006':     0.5,
        '2007':     0.5,
        '2008':     0.5,
        '2009':     0.5,
        '2010':     0.5,
    },
    TP.DAILY_SERIES:{
        TP.MEAN:    2.0,
    },
    TP.MONTHLY_SERIES:{
        TP.MEAN:    2.0,
    },
    TP.YEARLY_SERIES:{
        TP.MEAN:    2.0,
    },
}


nlp['markersize'] = {
    TP.HOURLY_SERIES:{
        TP.MEAN:    3.0,
    },
    TP.DIURNAL_CYCLE:{
        TP.MEAN:    3.0,
    },
    TP.ANNUAL_CYCLE:{
        #TP.MEAN:    2.5,
        TP.MEAN:    0.0,
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
    TP.YEARLY_SERIES:{
        TP.MEAN:    3.0,
    },
}

nlp['spread'] = {
    #'linewidth':    0.5,
    #'opacity':      '50',
    'linewidth':    0.0,
    'opacity':      '30',
}

nlp['hide_spread_mem_key'] = [
    #'COSMO_3.3_pgw',
    'MPI-ESM1-2-HR_ssp585',
]


## panel labels
#nlp['panel_labels_start_ind'] = 12
nlp['panel_labels_start_ind'] = 0
nlp['panel_labels_shift_right'] = -0.16
nlp['panel_labels_shift_up'] = 0.02
nlp['panel_labels_fontsize'] = 15
