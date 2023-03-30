#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    plotting namelist for 14_anim:
author			Christoph Heim
date created    29.07.2021
date changed    24.09.2021
usage			import in another script
"""
###############################################################################
import matplotlib.pyplot as plt
import cartopy
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
###############################################################################
nlp = {}

nlp['geo_plot']     = True

#### PLOT RESOLUTION
nlp['dpi'] = 600

# very important to use pcolormesh for lwp snapshots!!
# takes ages with contourf and looks bad
nlp['2D_type'] = 'pcolormesh'
#nlp['2D_type'] = 'contourf'

plt.rcParams['figure.titlesize'] = 7
plt.rcParams['font.size'] = 10
plt.rcParams['legend.fontsize'] = 6
#plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 6
plt.rcParams['ytick.labelsize'] = 6
plt.rcParams['axes.labelsize'] = 8

# transparent plot background
#nlp['transparent_bg'] = True
#COLOR = 'white'
nlp['transparent_bg'] = False
nlp['black_bg'] = False
COLOR = 'black'
plt.rcParams['xtick.color'] = COLOR
plt.rcParams['axes.labelcolor'] = COLOR
plt.rcParams['ytick.color'] = COLOR
plt.rcParams['text.color'] = COLOR

# COLORMAP SIMPLE
nlp['cmaps'] = {}

### MAP COLORMAPS
#cmap = plt.cm.YlGn
#my_cmap = cmap(np.linspace(0.1, 1.0, cmap.N))
#my_cmap = ListedColormap(my_cmap)
#nlp['cmaps']['land'] = my_cmap

#colors = ['#f0d8af', '#7d5f2f', '#49783e', '#114206']
#colors = ['#f0d8af', '#bea88b', '#706244', '#72734f', '#147a2d', '#0d521e']
#colors = ['#f0d8af', '#bea88b', '#678720', '#147a2d', '#0d521e'] # 3
#colors = ['#f0d8af', '#706244', '#72734f', '#147a2d', '#0d521e']
#colors = ['#f0d8af', '#574726', '#678720', '#147a2d', '#0d521e']
#colors = ['#f0d8af', '#7a6c4d', '#3e7046', '#147a2d', '#0d521e'] # 6
colors = ['#f0d8af', '#9c8c6a', '#607a30', '#276618', '#083613'] # 7
cmap = LinearSegmentedColormap.from_list("land", colors)
my_cmap = cmap(np.linspace(0.0, 1.0, cmap.N))
my_cmap = ListedColormap(my_cmap)
nlp['cmaps']['land'] = my_cmap

cmap = plt.cm.Blues
my_cmap = cmap(np.arange(cmap.N))
my_cmap[:,-1] = np.linspace(0, 1, cmap.N)
my_cmap = ListedColormap(my_cmap)
nlp['cmaps']['ocean'] = my_cmap

# TQC cmap
cmap = plt.cm.binary_r
#my_cmap = cmap(np.arange(cmap.N))
my_cmap = cmap(np.linspace(0.7, 1.0, cmap.N))
my_cmap[:,-1] = np.linspace(0, 1, cmap.N)
my_cmap = ListedColormap(my_cmap)
nlp['cmaps']['TQC'] = my_cmap

# TQV cmap
cmap = plt.cm.inferno_r
my_cmap = cmap(np.linspace(0.0, 0.35, cmap.N))
my_cmap[:,-1] = np.linspace(0.10, 0.28, cmap.N)
my_cmap = ListedColormap(my_cmap)
nlp['cmaps']['TQV'] = my_cmap

## TQI cmap
#cmap = plt.cm.cool
#my_cmap = cmap(np.linspace(0.0, 0.5, cmap.N))
#my_cmap[:,-1] = np.linspace(0.0, 1.0, cmap.N)**(1/1.5)
#my_cmap = ListedColormap(my_cmap)
#nlp['cmaps']['TQI'] = my_cmap
colors = ['#66f5fa', '#ffffff'] # 7
cmap = LinearSegmentedColormap.from_list("tqi", colors)
my_cmap = cmap(np.linspace(0.3, 1.0, cmap.N))
my_cmap[:,-1] = np.linspace(0.0, 1.0, cmap.N)**(1/2)
my_cmap = ListedColormap(my_cmap)
nlp['cmaps']['TQI'] = my_cmap


# PP cmap
#cmap = plt.cm.plasma
cmap = plt.cm.gnuplot2_r
my_cmap = cmap(np.arange(cmap.N))
my_cmap[:,-1] = np.linspace(0.0, 1.0, cmap.N)
my_cmap = ListedColormap(my_cmap)
nlp['cmaps']['PP'] = my_cmap


# QV2M cmap
cmap = plt.cm.inferno
my_cmap = cmap(np.linspace(0.0, 1.00, cmap.N))
#my_cmap[:,-1] = np.linspace(0.10, 0.28, cmap.N)
my_cmap = ListedColormap(my_cmap)
nlp['cmaps']['QV2M'] = my_cmap



nlp['cmaps']['colorful'] = 'nipy_spectral'
#nlp['cmaps']['colorful'] = 'gist_ncar'
nlp['cmaps']['jump'] = 'gist_stern_r'
nlp['cmaps']['terrain'] = 'gist_earth'
nlp['cmaps']['rainbow'] = 'rainbow'
nlp['cmaps']['blue_red'] = 'RdBu_r'
nlp['cmaps']['red_blue'] = 'RdBu'
nlp['cmaps']['cubehelix'] = 'cubehelix'
nlp['cmaps']['reds'] = 'Reds'
nlp['cmaps']['rain'] = 'gnuplot2'
nlp['cmaps']['rain_r'] = 'gnuplot2_r'
# COLORMAP VERSION 1
import matplotlib.pyplot as plt
cmap = plt.get_cmap('RdBu_r')
colors = cmap(np.linspace(0., 0.5, cmap.N // 2))
nlp['cmaps']['clouds'] = LinearSegmentedColormap.from_list('test', colors)

## COLORMAP VERSION 2
#from matplotlib.colors import LinearSegmentedColormap
#nlp['cmap'] = LinearSegmentedColormap.from_list('name', ['blue', 'white', 'brown'])


#### CARTOPY
nlp['map_margin']   = (0,0,0,0) # lon0, lon1, lat0, lat1
nlp['projection']   = cartopy.crs.PlateCarree()
nlp['land_color']           = (0,0.5,0,0.5)
nlp['ocean_color']          = (0,0.3,1,0.5)
nlp['river_color']          = (0,0.2,0.7,0.3)


# panel labels
nlp['i_draw_panel_labels'] = 0
nlp['panel_labels_start_ind'] = 0


# draw analysis/model domains
nlp['lw'] = 1.5

# position of time label
## this is for full animation with black bg
nlp['time_label_xpos'] = 0.87
## this is for domain plots
nlp['time_label_xpos'] = 0.98
### this is for double animation plots with black bg
#nlp['time_label_xpos'] = 0.99

nlp['time_label_color'] = 'black'
#nlp['time_label_color'] = 'white'


# configuration of subplots
nlp['subplts_cfgs'] = {
    '1x1':  {
        'left':0.04,
        'bottom':0.06,
        'right':0.99,
        'top':0.93,
        'wspace':0.02,
        'hspace':0.20,

        #'left':0.00,
        #'bottom':0.00,
        #'right':1.00,
        #'top':1.00,
        #'wspace':0.00,
        #'hspace':0.00,
    },

    '1x2':  {
        'left':0.00,
        'bottom':0.00,
        'right':1.00,
        'top':1.00,
        'wspace':0.01,
        'hspace':0.00,
    },
}
