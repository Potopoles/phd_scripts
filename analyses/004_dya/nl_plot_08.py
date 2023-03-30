#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    plotting namelist for 004_03_corr:
author			Christoph Heim
date created    25.11.2019
date changed    29.09.2020
usage			import in another script
"""
###############################################################################
import cartopy
import numpy as np
import matplotlib.pyplot as plt
from base.nl_plot_global import nlp
###############################################################################
# font sizes
plt.rcParams['font.size'] = 13.0
plt.rcParams['axes.labelsize'] = 22

# transparent plot background
#nlp['transparent_bg'] = True
#COLOR = 'white'
nlp['transparent_bg'] = False
COLOR = 'black'
plt.rcParams['xtick.color'] = COLOR
plt.rcParams['axes.labelcolor'] = COLOR
plt.rcParams['ytick.color'] = COLOR
plt.rcParams['text.color'] = COLOR
if nlp['transparent_bg']:
    plt.rcParams['grid.color'] = 'black'
    plt.rcParams['legend.facecolor'] = 'dimgrey'
    nlp['OBS_color'] = 'white'
else:
    nlp['OBS_color'] = 'black'

# colors
nlp['colors'] = plt.rcParams['axes.prop_cycle'].by_key()['color']
nlp['mod_col_inds'] = ['COSMO',
    'NICAM', 'GEOS', 'ICON', 'UM', 'MPAS',
    'IFS', 'SAM', 'ARPEGE-NH', 'FV3']

# markers
nlp['markers_aggreg'] = ['o', 'p', 'd', 'X', '*']
nlp['markers_daily'] = ['o', '*', 'd', 'X', '*']
nlp['marker_size_aggreg'] = 260
nlp['marker_linewidths_aggreg'] = 3
nlp['marker_size_daily'] =  50
nlp['marker_linewidths_daily'] = 2

# opacity for secondary models
nlp['alpha_secondary_models'] = 0.40


nlp['plot_order'] = [
    'OBS',
    'COSMO_12', 'COSMO_4.4', 'COSMO_2.2', 'COSMO_1.1', 'COSMO_0.5',
    'NICAM_7', 'NICAM_3.5',
    'SAM_4',
    'ICON_10', 'ICON_2.5',
    'UM_5',
    'MPAS_7.5', 'MPAS_3.75',
    'IFS_9', 'IFS_4',    
    'GEOS_3', 
    'ARPEGE-NH_2.5',
    'FV3_3.25',
]


# specific axis limits for aggreg_days
nlp['axis_limits'] = {
    'WFLXMBLI':0.009,
    'WFLXI':0.010,
}


# legend position
nlp['leg_pos'] = {
    str(['LWUTOA', 'SWUTOA']):      {'loc':'upper right', 'shift_right':0.13},
    #str(['WFLXMBLI', 'INVHGT']):   {'loc':'lower left', 'shift_left':0.10},
}


nlp['nrows']    = 1
nlp['ncols']    = 1
stretch = 1.3
nlp['figsize']  = (7*stretch,6*stretch) 

nlp['arg_subplots_adjust']  = {
                                'left':0.15,
                                'right':0.97,
                                'bottom':0.12,
                                'top':0.98,
                                #'wspace':0.14,
                                #'hspace':0.00,
                              }

nlp['panel_label_x_left_shift'] = 0.13
nlp['panel_label_y_pos'] = 0.95

