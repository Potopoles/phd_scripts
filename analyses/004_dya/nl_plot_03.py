#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    plotting namelist for 004_03_corr:
author			Christoph Heim
date created    25.11.2019
date changed    10.03.2021
usage			import in another script
"""
###############################################################################
import cartopy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm
from base.nl_plot_global import nlp
###############################################################################
fact = 1/3

# font sizes
plt.rcParams['font.size'] = 21 * fact 
plt.rcParams['axes.labelsize'] = 32 * fact
plt.rcParams['axes.titlesize'] = 36 * fact


### DYA paper
nlp['legend_fontsize'] = 16.3 * fact * 0.88
nlp['legend_markerscale'] = 0.45
### huge amount
#nlp['legend_fontsize'] = 12.3
#nlp['legend_markerscale'] = 0.45


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

col_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
viridis = matplotlib.cm.get_cmap('viridis')
crgb1 = 0/256
crgb2 = 106/256
crgb3 = 190/256

nlp['plt_mem_cfg'] = {
    #### main sims
    'COSMO_2.2':{
        'col':          (crgb1,crgb2,crgb3),
        'marker':       'o',
        'linestyle':    '-',
    },
    'NICAM_3.5':{
        'col':          col_cycle[1],
        'marker':       'o',
        'linestyle':    '-',
    },
    'SAM_4':{
        'col':          col_cycle[7],
        'marker':       'o',
        'linestyle':    '-',
    },
    'ICON_2.5':{
        'col':          col_cycle[3],
        'marker':       'o',
        'linestyle':    '-',
    },
    'UM_5':{
        'col':          col_cycle[4],
        'marker':       'o',
        'linestyle':    '-',
    },
    'MPAS_3.75':{
        'col':          col_cycle[5],
        'marker':       'o',
        'linestyle':    '-',
    },
    'IFS_4':{
        'col':          col_cycle[6],
        'marker':       'o',
        'linestyle':    '-',
    },
    'GEOS_3':{
        'col':          col_cycle[2],
        'marker':       'o',
        'linestyle':    '-',
    },
    'ARPEGE-NH_2.5':{
        'col':          col_cycle[8],
        'marker':       'o',
        'linestyle':    '-',
    },
    'FV3_3.25':{
        'col':          col_cycle[9],
        'marker':       'o',
        'linestyle':    '-',
    },
    'ERA5_31':{
        'col':          'black',
        'marker':       'o',
        'linestyle':    '-',
    },

    #### all others
    'COSMO_12':{
        'col':          (crgb1,crgb2,crgb3),
        'marker':       'o',
        'linestyle':    '-',
    },
    'COSMO_4.4':{
        'col':          (crgb1,crgb2,crgb3),
        'marker':       'o',
        'linestyle':    '-',
    },
    'COSMO_4.4_calib_7':{
        'col':          (78/256,153/256,218/256),
        'marker':       'o',
        'linestyle':    '-',
    },
    'COSMO_4.4_calib_8':{
        'col':          (144/256,197/256,243/256),
        'marker':       'o',
        'linestyle':    '-',
    },
    'COSMO_1.1':{
        'col':          (crgb1,crgb2,crgb3),
        'marker':       'o',
        'linestyle':    '-',
    },
    'COSMO_0.5':{
        'col':          (crgb1,crgb2,crgb3),
        'marker':       'o',
        'linestyle':    '-',
    },
    'NICAM_7':{
        'col':          col_cycle[1],
        'marker':       'o',
        'linestyle':    '-',
    },
    'ICON_10':{
        'col':          col_cycle[3],
        'marker':       'o',
        'linestyle':    '-',
    },
    'MPAS_7.5':{
        'col':          col_cycle[5],
        'marker':       'o',
        'linestyle':    '-',
    },
    'IFS_9':{
        'col':          col_cycle[6],
        'marker':       'o',
        'linestyle':    '-',
    },
}


# markers
nlp['markers_aggreg'] = {
    'all':['o', '*', 'd', 'X', '>'],
    'yearly':['o', 'p', 'd', 'X', '*'],
    'monthly':['o', 'p', 'd', 'X', '*'],
    'none':['o', '*', 'd', 'X', '*'],
}
nlp['marker_size_aggreg'] = {
    #'all':260,
    'all':500*fact*0.25,
    'yearly':500*fact*0.25,
    'monthly':500*fact*0.25,
    'none':70*fact*0.25,
}
nlp['marker_linewidths_aggreg'] = {
    'all':3*fact,
    'yearly':3*fact,
    'monthly':3*fact,
    'none':2*fact,
}
nlp['percentile_linewidth'] = 0.7
nlp['regression_linewidth'] = 0.7

# opacity for secondary models
#nlp['alpha_secondary_models'] = 0.40
nlp['alpha_secondary_models'] = 1.00

nlp['unique_colors'] = False
#nlp['unique_colors'] = True


nlp['plot_order'] = [
    'NICAM_7', 'NICAM_3.5',
    'SAM_4',
    'ICON_10', 'ICON_2.5',
    'UM_5',
    'MPAS_7.5', 'MPAS_3.75',
    'IFS_9', 'IFS_4',    
    'GEOS_3', 
    'ARPEGE-NH_2.5',
    'FV3_3.25',
    'COSMO_12', 'COSMO_4.4', 'COSMO_4.4_calib_7', 'COSMO_4.4_calib_8',
    'COSMO_2.2', 'COSMO_1.1', 'COSMO_0.5',
    'OBS',
]


# specific axis limits for aggreg_days
nlp['axis_max_agg_all'] = {
    #'WFLXI':0.010,
}


## legend position
nlp['legend_hidden'] = [
    'none', # aggregation

    ##str(['CLCL2',       'TQC']),
    ##str(['CLCL2',       'ALBEDO']),
    str(['TQC',         'ALBEDO']),

    str(['TQV',         'LWUTOA']),
    str(['TQI',         'LWUTOA']),

    str(['INVSTR',      'ALBEDO']),
    str(['INVSTRV',     'ALBEDO']),
    str(['SUBS',        'ALBEDO']),

    str(['ENTR',        'SLHFLX']),
    str(['ENTR',        'ALBEDO']),
]

## title hidden
nlp['title_hidden'] = [
    str(['CLCL2',       'ALBEDO']),

    str(['TQV',         'LWUTOA']),

    str(['INVSTR',      'ALBEDO']),
    str(['INVSTRV',     'ALBEDO']),
    str(['SUBS',        'ALBEDO']),

    str(['ENTR',        'SLHFLX']),
    str(['ENTR',        'ALBEDO']),
]

nlp['nrows']    = 1
nlp['ncols']    = 1


#stretch = 1.3
#nlp['figsize']  = (7*stretch,6*stretch) 
#nlp['arg_subplots_adjust']  = {
#                                'left':0.19,
#                                'right':0.97,
#                                'bottom':0.14,
#                                'top':0.98,
#                              }

stretch = 1.0
nlp['figsize']  = (3.0*stretch,2.2*stretch) 
nlp['arg_subplots_adjust']  = {
                                'left':0.19,
                                'right':0.70,
                                'bottom':0.21,
                                'top':0.88,
                              }

#nlp['panel_label_x_left_shift'] = 0.23
#nlp['panel_label_y_pos'] = 0.97

nlp['panel_label_x_left_shift'] = 0.32
nlp['panel_label_y_pos'] = 1.08

nlp['panel_label_size'] = 38 * fact

