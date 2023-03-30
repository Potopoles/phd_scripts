#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    plotting namelist for 004_01_spatial:
author			Christoph Heim
date created    18.11.2019
date changed    15.09.2020
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

# very important to use pcolormesh for lwp snapshots!!
# takes ages with contourf and looks bad
nlp['2D_type'] = 'pcolormesh'
nlp['2D_type'] = 'contourf'

fact = 1
plt.rcParams['font.size'] = 8 * fact
plt.rcParams['axes.labelsize'] = 10 * fact
plt.rcParams['legend.fontsize'] = 10 * fact
plt.rcParams['axes.titlesize'] = 9 * fact

nlp['bias_labels_fontsize'] = 6 * fact

nlp['snapshots_plot_time'] = 0

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


nlp['projection']   = cartopy.crs.PlateCarree()
nlp['map_margin']   = (0,0,0,0) # lon0, lon1, lat0, lat1




## panel labels
nlp['i_draw_panel_labels'] = 1

## this is now set in config
#nlp['panel_labels_start_ind'] = 12
##nlp['panel_labels_start_ind'] = 11
##nlp['panel_labels_start_ind'] = 0


# labels showing the bias MOD - OBS as spatial mean
nlp['add_bias_labels'] = False
nlp['add_bias_labels'] = True
