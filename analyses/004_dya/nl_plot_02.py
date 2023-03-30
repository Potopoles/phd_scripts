#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    plotting namelist for 004_02_profiles:
author			Christoph Heim
date created    04.12.2019
date changed    03.02.2021
usage			import in another script
"""
###############################################################################
import matplotlib
import matplotlib.pyplot as plt
from base.nl_plot_global import nlp
###############################################################################

# font sizes

#plt.rcParams['font.size'] = 23
#plt.rcParams['axes.labelsize'] = 35
#plt.rcParams['legend.fontsize'] = 20
#nlp['mod_linewidth'] = 3.5
#nlp['obs_linewidth'] = 4.5

#fact = 1/4.11
fact = 1/2
plt.rcParams['font.size'] = 23 * fact
plt.rcParams['axes.labelsize'] = 35 * fact
plt.rcParams['legend.fontsize'] = 20 * fact * 0.9
nlp['mod_linewidth'] = 3.5 * fact
nlp['obs_linewidth'] = 4.5 * fact


# colors
nlp['colors'] = plt.rcParams['axes.prop_cycle'].by_key()['color']
nlp['mod_col_inds'] = ['COSMO',
    'NICAM', 'GEOS', 'ICON', 'UM', 'MPAS',
    'IFS', 'SAM', 'ARPEGE-NH', 'FV3']

nlp['linestyles'] = ['-', '--', ':', '-.']

cmap = matplotlib.cm.get_cmap('viridis')

cosmo_rgb = (0/256, 106/256, 190/256)

nlp['specific_mem_colors'] = {
    #### for cosmo set
    #'COSMO_12':     cmap(0/4),
    #'COSMO_4.4':    cmap(1/4),
    #'COSMO_2.2':    cmap(2/4),
    #'COSMO_1.1':    cmap(3/4),
    #'COSMO_0.5':    cmap(4/4),
    #'COSMO_4.4_calib_7':  cmap(1/4),
    #'COSMO_4.4_calib_8':  cmap(1/4),

    ### for dya_main set
    #'COSMO_4.4':    cosmo_rgb,

}

nlp['unique_colors'] = False
#nlp['unique_colors'] = True

nlp['specific_mem_linestyles'] = {
    'COSMO_12':     '-',
    'COSMO_4.4':    '-',
    'COSMO_4.4_calib_2':    ':',
    'COSMO_4.4_calib_3':    '--',
    'COSMO_4.4_calib_4':    '-.',
    'COSMO_4.4_calib_5':    '-',
    'COSMO_4.4_calib_6':    '--',
    'COSMO_4.4_calib_7':    ':',
    'COSMO_4.4_calib_8':    '-.',
    'COSMO_2.2':    '-',
    'COSMO_1.1':    '-',
    'COSMO_0.5':    '-',
}


nlp['nrows']    = 1
nlp['ncols']    = 1
stretch = 1.0
nlp['figsize']  = (3.5*stretch,3.1*stretch) 

#nlp['arg_subplots_adjust']  = {
#                                'left':0.20,
#                                'right':0.94,
#                                'bottom':0.16,
#                                'top':0.98,
#                              }
nlp['arg_subplots_adjust']  = {
                                'left':0.23,
                                'right':0.93,
                                'bottom':0.19,
                                #'top':0.97,
                                'top':0.92,
                              }

#nlp['panel_label_x_left_shift'] = 0.24
nlp['panel_label_x_left_shift'] = 0.33
#nlp['panel_label_y_pos'] = 0.94
nlp['panel_label_y_pos'] = 1.02
nlp['panel_label_size'] = 36 * fact
