#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    plotting namelist for 005_02_profiles:
author			Christoph Heim
date created    04.12.2019
date changed    11.11.2021
usage			import in another script
"""
###############################################################################
import matplotlib
import matplotlib.pyplot as plt
from base.nl_plot_global import nlp#, var_plt_cfgs_glob
###############################################################################

nlp['geo_plot']     = False

#### PLOT RESOLUTION
nlp['dpi'] = 600

# font sizes
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 15
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
    'CTRL':                         nlp['colors'][3],
    'PGW':                          nlp['colors'][3],
    'PGW - CTRL':                   nlp['colors'][3],
    'MPI-ESM1-2-HR SSP5-8.5':       nlp['colors'][0],
    'MPI-ESM1-2-HR HIST':           nlp['colors'][0],
    'MPI-ESM1-2-HR SSP5-8.5 - HIST':nlp['colors'][0],
    'ERA5':                         nlp['colors'][1],
    #'CMIP6':                        '#616161',
    'CMIP6':                        '#999999',
    'CMIP6 SSP5-8.5 - HIST':        '#999999',
    'CERES 2007-2009':              '#000000',
    'CERES 2004-2014':              '#000000',
    'GPM 2007-2009':                '#000000',
    'GPM 2001-2014':                '#000000',
}

nlp['var_colors'] = {
    #'TKEV':                         nlp['colors'][2],
    #'TKEVNORMI':                    nlp['colors'][2],
    #'QVSATDEF':                     nlp['colors'][2],
    #'QVSATDEFNORMI':                nlp['colors'][2],

    #'CLDQV':                        nlp['colors'][4],
    #'CLDQVNORMI':                   nlp['colors'][4],
    #'CSQV':                         nlp['colors'][5],
    #'CSQVNORMI':                    nlp['colors'][5],

}

for var_name in [
    'TV','T',
    ]:
    nlp['var_colors'][var_name] = '#000000'
for var_name in [
    'UPDTV','UPDBUOYI',
    ]:
    nlp['var_colors'][var_name] = nlp['colors'][3] 
for var_name in [
    'PARCTV','PARCT','PARCBUOYI',
    ]:
    nlp['var_colors'][var_name] = nlp['colors'][2] 


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
    'CMIP6 HIST':                   '-',
    'CMIP6 SCEN':                   '--',
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



nlp['var_plt_cfgs'] = {}

for var_name in [
    'UPDBUOYI','PARCBUOYI',
    ]:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            'abs':  [-0.5,0.5],
            'diff': [-0.3,0.3],
        },
    }
#print(nlp['var_plt_cfgs'])
#quit()
