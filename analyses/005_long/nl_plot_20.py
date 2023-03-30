#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    plotting namelist for 005_20_cld3d:
author			Christoph Heim
date changed    13.06.2022
date changed    13.06.2022
usage			import in another script
"""
###############################################################################
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from base.nl_plot_global import nlp, var_plt_cfgs_glob
###############################################################################

nlp['geo_plot']     = False

#### PLOT RESOLUTION
nlp['dpi'] = 600

# font sizes
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['legend.fontsize'] = 8

#nlp['mod_linewidth'] = 1.5
#nlp['obs_linewidth'] = 1.5

# colors
nlp['colors'] = plt.rcParams['axes.prop_cycle'].by_key()['color']


nlp['ref_color'] = '#000000'
#nlp['ref2_color'] = '#616161'
nlp['ref2_color'] = '#000000'

#nlp['ref_color'] = nlp['colors'][0]
#nlp['ref2_color'] = nlp['colors'][0] 

nlp['mem_colors'] = {
    'CTRL':                         nlp['colors'][2],
    'PGW':                          nlp['colors'][1],
}

nlp['ref_linestyle'] = '-'
nlp['ref2_linestyle'] = '--'

nlp['mem_linestyles'] = {
    'COSMO_3.3_ctrl':               '-',
    'COSMO_3.3_pgw':                '--',
    'MPI-ESM1-2-HR_historical':     '-',
    'MPI-ESM1-2-HR_ssp585':         '--',
    'CERES 2007-2009':              '-',
    'CERES 2004-2014':              '--',
    'GPM 2007-2009':                '-',
    'GPM 2001-2014':                '--',
}



nlp['nrows']    = 1
nlp['ncols']    = 1
stretch = 1.1
nlp['figsize']  = (7*stretch,6*stretch) 

nlp['arg_subplots_adjust']  = {
                                'left':0.20,
                                'right':0.94,
                                'bottom':0.16,
                                'top':0.98,
                                #'wspace':0.14,
                                #'hspace':0.00,
                              }

nlp['panel_label_x_left_shift'] = 0.24
nlp['panel_label_y_pos'] = 0.94
nlp['panel_label_size'] = 36


nlp['var_plt_cfgs'] = var_plt_cfgs_glob
#nlp['var_plt_cfgs']['W'] = {
#    'lims': {
#        'abs':  [-0.01,0.01],
#        'diff': [-0.005,0.005],
#    },
#}





nlp['cmaps'] = {
    'cf':{'abs':{},'diff':{},'bias':{},'rel':{}},
    'cl':{'abs':{},'diff':{},'bias':{},'rel':{}},
}
nlp['levels'] = {
    'cf':{'abs':{},'diff':{},'bias':{},'rel':{}},
    'cl':{'abs':{},'diff':{},'bias':{},'rel':{}},
}
nlp['cb_ticks'] = {
    'cf':{'abs':{},'diff':{},'bias':{},'rel':{}},
    'cl':{'abs':{},'diff':{},'bias':{},'rel':{}},
}

######### variable QC
##############################################################################
for var_name in [
        'QC'
    ]:
    #cmap = plt.cm.viridis
    #my_cmap = cmap(np.linspace(0.10, 1.00, cmap.N))
    cmap = plt.cm.Greens
    my_cmap = cmap(np.linspace(0.0, 1.00, cmap.N))
    #my_cmap[:,-1] = np.linspace(0.0, 1.0, cmap.N)**(1./2.)
    my_cmap = ListedColormap(my_cmap)
    nlp['cmaps']['cf']['abs'][var_name] = my_cmap
    nlp['levels']['cf']['abs'][var_name] = np.arange(0, 0.3*1.01, 0.05)
    nlp['cb_ticks']['cf']['abs'][var_name] = nlp['levels']['cf']['abs'][var_name]

    cmap = plt.cm.RdBu_r
    my_cmap = cmap(np.linspace(0.00, 1.00, cmap.N))
    #my_cmap[:,-1] = np.linspace(0.0, 1.0, cmap.N)**(1./2.)
    my_cmap = ListedColormap(my_cmap)
    nlp['cmaps']['cf']['diff'][var_name] = my_cmap
    nlp['levels']['cf']['diff'][var_name] = np.arange(-0.02, 0.02*1.01, 0.005)
    nlp['cb_ticks']['cf']['diff'][var_name] = nlp['levels']['cf']['diff'][var_name]

######### variables QVDIV
##############################################################################
for var_name in [
        'QVDIV','QVHDIV','QVVDIV',
        'QVDIVTURB','QVHDIVTURB','QVVDIVTURB',
    ]:
    cmap = plt.cm.RdBu_r
    my_cmap = cmap(np.linspace(0.0, 1.00, cmap.N))
    #my_cmap[:,-1] = (np.linspace(-1.0, 1.0, cmap.N)**2)**(1/2)
    my_cmap = ListedColormap(my_cmap)
    nlp['cmaps']['cf']['abs'][var_name] = my_cmap
    nlp['levels']['cf']['abs'][var_name] = np.arange(-1.5, 1.5*1.01, 0.3)
    nlp['cb_ticks']['cf']['abs'][var_name] = nlp['levels']['cf']['abs'][var_name]

    nlp['cmaps']['cf']['diff'][var_name] = my_cmap
    nlp['levels']['cf']['diff'][var_name] = np.arange(-0.3, 0.3*1.02, 0.05)
    nlp['cb_ticks']['cf']['diff'][var_name] = nlp['levels']['cf']['diff'][var_name]


######### variables W
##############################################################################
for var_name in [
        'W'
    ]:
    cmap = plt.cm.RdBu_r
    my_cmap = cmap(np.linspace(0.0, 1.00, cmap.N))
    #my_cmap[:,-1] = (np.linspace(-1.0, 1.0, cmap.N)**2)**(1/2)
    my_cmap = ListedColormap(my_cmap)
    nlp['cmaps']['cf']['abs'][var_name] = my_cmap
    nlp['levels']['cf']['abs'][var_name] = np.arange(-0.2, 0.2*1.01, 0.04)
    nlp['cb_ticks']['cf']['abs'][var_name] = nlp['levels']['cf']['abs'][var_name]

    nlp['cmaps']['cf']['diff'][var_name] = my_cmap
    nlp['levels']['cf']['diff'][var_name] = np.arange(-0.02, 0.02*1.02, 0.005)
    nlp['cb_ticks']['cf']['diff'][var_name] = nlp['levels']['cf']['diff'][var_name]
