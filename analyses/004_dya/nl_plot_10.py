#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    plotting namelist for 004_10_olr_bias.
author			Christoph Heim
date created    14.01.2021
date changed    21.01.2021
usage			import in another script
"""
###############################################################################
import matplotlib.pyplot as plt
from base.nl_plot_global import nlp
###############################################################################

# font sizes
#plt.rcParams['font.size'] = 23
plt.rcParams['font.size'] = 18
#plt.rcParams['axes.labelsize'] = 35
plt.rcParams['axes.labelsize'] = 20

# colors
nlp['colors'] = plt.rcParams['axes.prop_cycle'].by_key()['color']
nlp['mod_col_inds'] = ['COSMO',
    'NICAM', 'GEOS', 'ICON', 'UM', 'MPAS',
    'IFS', 'SAM', 'ARPEGE-NH', 'FV3']

nlp['mod_linewidth'] = 2.0
nlp['obs_linewidth'] = 2.5

nlp['linestyles'] = ['-', '--', ':']

nlp['textx'] = 0.65
nlp['texty'] = 0.92

nlp['nrows']    = 2
nlp['ncols']    = 2
stretch = 1.6
nlp['figsize']  = (7*stretch,6*stretch) 

nlp['arg_subplots_adjust']  = {
                                'left':0.10,
                                'right':0.95,
                                'bottom':0.08,
                                'top':0.98,
                                'wspace':0.25,
                                'hspace':0.20,
                              }

nlp['panel_label_x_left_shift'] = 0.14
nlp['panel_label_y_pos'] = 0.94
