#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    plotting namelist for 004_09_timeline:
author			Christoph Heim
date created    21.11.2020
date changed    21.11.2020
usage			import in another script
"""
###############################################################################
from base.nl_plot_global import nlp
import matplotlib.pyplot as plt
import cartopy
import numpy as np
###############################################################################
#rckeys = plt.rcParams.keys()
#for rckey in rckeys:
#    if 'title' in rckey:
#        print(rckey)
#quit()

#plt.rcParams['axes.titlesize'] = 14

# transparent plot background
#nlp['transparent_bg'] = True
#COLOR = 'white'
nlp['transparent_bg'] = False
COLOR = 'black'
plt.rcParams['xtick.color'] = COLOR
plt.rcParams['axes.labelcolor'] = COLOR
plt.rcParams['ytick.color'] = COLOR
plt.rcParams['text.color'] = COLOR

# COLORMAP SIMPLE
nlp['cmaps'] = {}
nlp['cmaps']['colorful'] = 'nipy_spectral'
#nlp['cmaps']['colorful'] = 'gist_ncar'
nlp['cmaps']['jump'] = 'gist_stern_r'
nlp['cmaps']['terrain'] = 'gist_earth'
nlp['cmaps']['rainbow'] = 'rainbow'
nlp['cmaps']['blue_red'] = 'RdBu_r'
nlp['cmaps']['cubehelix'] = 'cubehelix'
nlp['cmaps']['reds'] = 'Reds'
nlp['cmaps']['rain'] = 'gnuplot2'
# COLORMAP VERSION 1
import matplotlib.pyplot as plt
cmap = plt.get_cmap('RdBu_r')
colors = cmap(np.linspace(0., 0.5, cmap.N // 2))
from matplotlib.colors import LinearSegmentedColormap
nlp['cmaps']['clouds'] = LinearSegmentedColormap.from_list('test', colors)

## COLORMAP VERSION 2
#from matplotlib.colors import LinearSegmentedColormap
#nlp['cmap'] = LinearSegmentedColormap.from_list('name', ['blue', 'white', 'brown'])

# colors
nlp['colors'] = plt.rcParams['axes.prop_cycle'].by_key()['color']
nlp['mod_col_inds'] = ['COSMO',
    'NICAM', 'GEOS', 'ICON', 'UM', 'MPAS',
    'IFS', 'SAM', 'ARPEGE-NH', 'FV3']
nlp['OBS_color'] = 'black'


nlp['nrows'] = 1
nlp['ncols'] = 1
stretch = 1
nlp['figsize'] = (10*stretch,6*stretch)
nlp['subplts'] = {
    'left':0.15,  'bottom':0.21,
    'right':0.98, 'top':0.96,
    'wspace':0.02,'hspace':0.20
}



## panel labels
#nlp['panel_labels_start_ind'] = 12
nlp['panel_labels_start_ind'] = 0
#
#
## labels showing the bias MOD - OBS as spatial mean
#nlp['add_bias_labels'] = False
