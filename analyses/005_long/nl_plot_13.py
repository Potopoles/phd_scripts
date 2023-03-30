#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    plotting namelist for 005_13_rad:
author			Christoph Heim
date created    02.07.2021
date changed    02.07.2021
usage			import in another script
"""
###############################################################################
from base.nl_plot_global import nlp
import matplotlib.pyplot as plt
import cartopy
import numpy as np
###############################################################################

#plt.rcParams['axes.titlesize'] = 12
#plt.rcParams['font.size'] = 13
##plt.rcParams['xtick.labelsize'] = 10
##plt.rcParams['ytick.labelsize'] = 10
#plt.rcParams['axes.labelsize'] = 12
##plt.rcParams['legend.fontsize'] = 10

# transparent plot background
#nlp['transparent_bg'] = True
#COLOR = 'white'
nlp['transparent_bg'] = False
COLOR = 'black'
plt.rcParams['xtick.color'] = COLOR
plt.rcParams['axes.labelcolor'] = COLOR
plt.rcParams['ytick.color'] = COLOR
plt.rcParams['text.color'] = COLOR

# panel labels
nlp['i_draw_panel_labels'] = 0
nlp['panel_labels_start_ind'] = 0


stretch = 1.0
nlp['figsize']  = (5*stretch,4*stretch) 
nlp['nrows']    = 1
nlp['ncols']    = 1

nlp['arg_subplots_adjust']  = {
                                'left':0.17,
                                'right':0.98,
                                'bottom':0.15,
                                'top':0.95,
                                'wspace':0.15,
                                'hspace':0.15,
                              }

#nlp['mem_hatch'] = {'COSMO_3.3':        '',
#                    'COSMO_3.3_pgw':    '...',
#                    'COSMO_3.3_pgw_co2':'///',
#                    'COSMO_3.3_pgw_sst':'+++'}
#nlp['var_col'] = {'SWDTOA':     'orange',
#                  'SWUTOA':     'blue',
#                  'SWNDTOA':    'red',
#                  }


nlp['colors'] = plt.rcParams['axes.prop_cycle'].by_key()['color']
nlp['mem_col_inds'] = ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw',
                       'COSMO_3.3_pgw_co2', 'COSMO_3.3_pgw_sst']
