#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Global plotting namelist that is important within each anlysis
                in the specific plot namelists.
author			Christoph Heim
date created    22.06.2019
date changed    29.11.2021
usage           no args
"""
###############################################################################
import cartopy
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, ListedColormap

#print(plt.rcParams.keys())
nlp = {}

nlp['dpi'] = 600

#### PLOT TYPE
#nlp['2D_type'] = 'contourf'
nlp['2D_type'] = 'pcolormesh'

# transparent_background
nlp['transparent_bg'] = False

#### PLOT DESIGN
# TODO I think those are not used anymore from here..
##plt.rcParams['figure.titlesize'] = 14
##plt.rcParams['axes.titlesize'] = 12
##plt.rcParams['axes.labelsize'] = 12
##plt.rcParams['xtick.labelsize'] = 8
##plt.rcParams['ytick.labelsize'] = 8
##plt.rcParams['legend.fontsize'] = 10
### generic text labels (from plt.text function)
##plt.rcParams['font.size'] = 13


#nlp['cmap']                 = 'jet'
#nlp['arg_subplots_adjust']  = {
#                                'left':0.15,
#                                'right':0.98,
#                                'bottom':0.15,
#                                'top':0.95,
#                                'wspace':0.15,
#                                'hspace':0.15,
#                              }
# shared colorbar
cax_x0                      = 0.05
cax_y0                      = 0.05
cax_dx                      = 0.90
cax_dy                      = 0.05
nlp['cax_pos']              = [cax_x0, cax_y0, cax_dx, cax_dy]

#### CARTOPY
#nlp['projection']           = cartopy.crs.PlateCarree()
nlp['map_margin']           = (3,3,3,3) # lon0, lon1, lat0, lat1
nlp['land_color']           = (0,0.5,0,0.5)
nlp['ocean_color']          = (0,0.3,1,0.5)
nlp['river_color']          = (0,0.2,0.7,0.3)







### CMAPS
##############################################################################
## PP cmap
#cmap = plt.cm.gnuplot2_r
#my_cmap = cmap(np.arange(cmap.N))
##my_cmap[:,-1] = np.linspace(0.0, 1.0, cmap.N)#**(1/2)
#my_cmap = ListedColormap(my_cmap)
#cmap_precip = my_cmap

## RdBu_r positive cmap
cmap = plt.cm.RdBu_r
my_cmap = cmap(np.linspace(0.5, 1.00, cmap.N))
my_cmap = ListedColormap(my_cmap)
cmap_RdBu_r_positive = my_cmap


cmap = plt.cm.PRGn_r
my_cmap = cmap(np.linspace(0.0, 1.00, cmap.N))
#alpha = np.concatenate([
#    np.repeat(1, int(cmap.N*4/9)),
#    (np.linspace(-1.0, 1.0, int(cmap.N*1/9)+2)**2),#**(1/2),
#    np.repeat(1, int(cmap.N*4/9))
#    ])
#my_cmap[:,-1] = alpha
my_cmap = ListedColormap(my_cmap)
cmap_symzero = my_cmap


cmap = plt.cm.RdBu_r
my_cmap = cmap(np.linspace(0.0, 1.00, cmap.N))
#alpha = np.concatenate([
#    np.repeat(1, int(cmap.N*4/9)),
#    (np.linspace(-1.0, 1.0, int(cmap.N*1/9)+2)**2),#**(1/2),
#    np.repeat(1, int(cmap.N*4/9))
#    ])
#my_cmap[:,-1] = alpha
my_cmap = ListedColormap(my_cmap)
cmap_diff = my_cmap


