#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    plotting namelist for 004_04_cross_sects:
author			Christoph Heim
date created    16.07.2020
date changed    16.07.2020
usage			import in another script
"""
###############################################################################
import numpy as np
import matplotlib.pyplot as plt
from base.nl_plot_global import nlp
###############################################################################

stretch = 0.5

# font sizes
plt.rcParams['font.size'] = 15*stretch
plt.rcParams['axes.labelsize'] = 18*stretch
plt.rcParams['axes.titlesize'] = 18*stretch
plt.rcParams['figure.titlesize'] = 21*stretch

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

# colors
#nlp['colors'] = plt.rcParams['axes.prop_cycle'].by_key()['color']
nlp['colors'] = ['black', 'black']

nlp['linewidths'] = [2, 2]

nlp['linestyles'] = ['-', '--']

#nlp['cl_cmap'] = nlp['cmaps']['rain']
nlp['cfqc_cmap'] = 'YlGn'
nlp['cfqc_cmap'] = 'viridis'

nlp['cfw_cmap'] = nlp['cmaps']['blue_red']

nlp['cfqc_levels'] = [1E-2, 1E-1, 2E-1, 3E-1, 4E-1, 5E-1]
nlp['cfqc_cb_ticks'] = [1E-2, 1E-1, 2E-1, 3E-1, 4E-1, 5E-1]
#nlp['cfqc_levels'] = [1E-1, 2E-1, 3E-1, 4E-1, 5E-1]
#nlp['cfqc_cb_ticks'] = [1E-1, 2E-1, 3E-1, 4E-1, 5E-1]
#nlp['cfqc_levels'] = [5E-2, 1E-1, 2E-1, 3E-1, 4E-1, 5E-1]
#nlp['cfqc_cb_ticks'] = [5E-2, 1E-1, 2E-1, 3E-1, 4E-1, 5E-1]

nlp['cfw_levels'] = np.linspace(-1E1,1E1,11)
nlp['cfw_cb_ticks'] = [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10]
#quit()

nlp['cfw_colorbar'] = 'ICON_2.5'
nlp['cfqc_colorbar'] = 'COSMO_2.2'


nlp['nrows']    = 1
nlp['ncols']    = 2
nlp['figsize']  = (6.0*stretch,3.8*stretch) 


nlp['arg_subplots_adjust']  = {
            'left':0.20,
            'bottom':0.53,
            'right':0.98,
            'top':0.85,
            'wspace':0.05,
            #'hspace':0.40,
                              }

nlp['colorbar_pos']  = [0.20, 0.24, 0.73, 0.05]

nlp['panel_label_size'] = 24 * stretch
nlp['panel_label_x_left_shift'] = 0.42
nlp['panel_label_y_pos'] = 1.18
nlp['panel_labels'] = ['a.','b.','c.','d.','e.','f.','g.','h.','i.','j.']
