#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    plotting namelist for 004_06_diurnal:
author			Christoph Heim
date created    17.08.2020
date changed    17.08.2020
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


nlp['projection']   = cartopy.crs.PlateCarree()
nlp['map_margin']   = (0,0,0,0) # lon0, lon1, lat0, lat1

nlp['nrows']    = 1
nlp['ncols']    = 1
stretch = 0.9
nlp['figsize']  = (8*stretch,6*stretch) 

nlp['arg_subplots_adjust']  = {
                                'left':0.20,
                                'right':0.98,
                                'bottom':0.10,
                                'top':0.95,
                                #'wspace':0.14,
                                #'hspace':0.00,
                              }


