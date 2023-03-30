#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    Plotting namelist for 000_01_draw_map
author			Christoph Heim
date created    20.04.2019
date changed    20.09.2021
usage			no args
"""
##############################################################################
from base.nl_plot_global import nlp
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy
##############################################################################

#### PLOT RESOLUTION
nlp['dpi'] = 600

#### PLOT TYPE
# transparent_background
nlp['transparent_bg'] = False
COLOR = 'black'

#nlp['transparent_bg'] = True
#COLOR = 'white'


##### PLOT DESIGN
nlp['cmap'] = 'jet'
nlp['lw'] = 2


#fact = 0.7 # DYAMOND paper
fact = 1.1 

plt.rcParams['font.size']   = 22 * fact
plt.rcParams['axes.labelsize'] = 22 * fact
plt.rcParams['xtick.color'] = COLOR
plt.rcParams['axes.labelcolor'] = COLOR
plt.rcParams['ytick.color'] = COLOR
plt.rcParams['xtick.labelsize'] = 18 * fact
plt.rcParams['ytick.labelsize'] = 18 * fact
plt.rcParams['legend.fontsize']   = 17 * fact

# dom_plot_map
nlp['arg_subplots_adjust']  = {
                                'left':0.16,
                                'right':0.98,
                                'bottom':0.12,
                                'top':0.99,
                              }
## dom_4km_dya
#nlp['arg_subplots_adjust']  = {
#                                'left':0.01,
#                                'right':0.99,
#                                'bottom':0.12,
#                                'top':0.99,
#                              }

#nlp['figsize_inches'] = (8*fact,5.0*fact) # DYAMOND paper
nlp['figsize_inches'] = (8*1.3,5.5*1.3)

##### CARTOPY
nlp['projection']   = cartopy.crs.PlateCarree()
#nlp['map_margin'] = (12,12,12,12) # lon0, lon1, lat0, lat1
nlp['map_margin'] = (2,2,2,2) # lon0, lon1, lat0, lat1
nlp['map_margin'] = (0,0,0,0) # lon0, lon1, lat0, lat1


