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
from base.nl_plot_global import nlp, var_plt_cfgs_glob
###############################################################################

domain = 'trades'
domain = 'ITCZ'

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
    'EQPOTTDIV', 'EQPOTTDIVNORMI',
    'LATH', 'LATHNORMI',
    'POTT','POTTNORMI',
    'POTTDIV', 'POTTDIVNORMI',
    'POTTDIVMEAN', 'POTTDIVMEANNORMI',
    'POTTHDIVMEAN', 'POTTHDIVMEANNORMI',
    'POTTVDIVMEAN', 'POTTVDIVMEANNORMI',
    'POTTDIVTURB', 'POTTDIVTURBNORMI',
    'POTTHDIVTURB', 'POTTHDIVTURBNORMI',
    'POTTVDIVTURB', 'POTTVDIVTURBNORMI',

    'POTTDIV2', 'POTTDIV2NORMI',

    'POTTDIV3', 'POTTDIV3NORMI',

    'QVDIV', 'QVDIVNORMI',
    'QVDIVMEAN', 'QVDIVMEANNORMI',
    'QVHDIVMEAN', 'QVHDIVMEANNORMI',
    'QVVDIVMEAN', 'QVVDIVMEANNORMI',
    'QVDIVTURB', 'QVDIVTURBNORMI',
    'QVHDIVTURB', 'QVHDIVTURBNORMI',
    'QVVDIVTURB', 'QVVDIVTURBNORMI',
    'QVUVDIVTURB', 'QVUVDIVTURBNORMI',
    'QVDVDIVTURB', 'QVDVDIVTURBNORMI',

    'QVDIV2', 'QVDIV2NORMI',
    'QVDIV2MEAN', 'QVDIV2MEANNORMI',
    'QVHDIV2MEAN', 'QVHDIV2MEANNORMI',
    'QVVDIV2MEAN', 'QVVDIV2MEANNORMI',
    'QVDIV2TURB', 'QVDIV2TURBNORMI',
    'QVHDIV2TURB', 'QVHDIV2TURBNORMI',
    'QVVDIV2TURB', 'QVVDIV2TURBNORMI',

    'QVDIV3', 'QVDIV3NORMI',
    'QVDIV3MEAN', 'QVDIV3MEANNORMI',
    'QVHDIV3MEAN', 'QVHDIV3MEANNORMI',
    'QVVDIV3MEAN', 'QVVDIV3MEANNORMI',
    'QVDIV3TURB', 'QVDIV3TURBNORMI',
    'QVHDIV3TURB', 'QVHDIV3TURBNORMI',
    'QVVDIV3TURB', 'QVVDIV3TURBNORMI',

    'QV','QVNORMI',
    'QVSATDEF','QVSATDEFNORMI',
    'W','WNORMI',
    'TKEV','TKEVNORMI',
    'RH','RHNORMI',
    'BVF',
    ]:
    nlp['var_colors'][var_name] = '#000000'
for var_name in [
    'CLDEQPOTTDIV', 'CLDEQPOTTDIVNORMI',
    'CLDLATH', 'CLDLATHNORMI',
    'CLDPOTTDIV', 'CLDPOTTDIVNORMI',
    'CLDPOTTHDIV', 'CLDPOTTHDIVNORMI',
    'CLDPOTTVDIV', 'CLDPOTTVDIVNORMI',
    'CLDPOTTDIVTURB', 'CLDPOTTDIVTURBNORMI',
    'CLDPOTTHDIVTURB', 'CLDPOTTHDIVTURBNORMI',
    'CLDPOTTVDIVTURB', 'CLDPOTTVDIVTURBNORMI',

    'CLDPOTTDIV2', 'CLDPOTTDIV2NORMI',
    'CLDPOTTHDIV2', 'CLDPOTTHDIV2NORMI',
    'CLDPOTTVDIV2', 'CLDPOTTVDIV2NORMI',

    'CLDPOTTDIV3', 'CLDPOTTDIV3NORMI',
    'CLDPOTTHDIV3', 'CLDPOTTHDIV3NORMI',
    'CLDPOTTVDIV3', 'CLDPOTTVDIV3NORMI',

    'CLDQVDIV', 'CLDQVDIVNORMI',
    'CLDQVHDIV', 'CLDQVHDIVNORMI',
    'CLDQVVDIV', 'CLDQVVDIVNORMI',
    'CLDQVDIVTURB', 'CLDQVDIVTURBNORMI',
    'CLDQVHDIVTURB', 'CLDQVHDIVTURBNORMI',
    'CLDQVVDIVTURB', 'CLDQVVDIVTURBNORMI',
    'CLDQVUVDIVTURB', 'CLDQVUVDIVTURBNORMI',
    'CLDQVDVDIVTURB', 'CLDQVDVDIVTURBNORMI',

    'CLDQVDIV2', 'CLDQVDIV2NORMI',
    'CLDQVHDIV2', 'CLDQVHDIV2NORMI',
    'CLDQVVDIV2', 'CLDQVVDIV2NORMI',
    'CLDQVDIV2TURB', 'CLDQVDIV2TURBNORMI',
    'CLDQVHDIV2TURB', 'CLDQVHDIV2TURBNORMI',
    'CLDQVVDIV2TURB', 'CLDQVVDIV2TURBNORMI',

    'CLDQVDIV3', 'CLDQVDIV3NORMI',
    'CLDQVHDIV3', 'CLDQVHDIV3NORMI',
    'CLDQVVDIV3', 'CLDQVVDIV3NORMI',
    'CLDQVDIV3TURB', 'CLDQVDIV3TURBNORMI',
    'CLDQVHDIV3TURB', 'CLDQVHDIV3TURBNORMI',
    'CLDQVVDIV3TURB', 'CLDQVVDIV3TURBNORMI',

    'CLDQV','CLDQVNORMI',
    'CLDQVSATDEF','CLDQVSATDEFNORMI',
    'CLDW','CLDWNORMI',
    'CLDTKEV','CLDTKEVNORMI',
    'CLDRH','CLDRHNORMI',
    'CLDBVF',
    ]:
    nlp['var_colors'][var_name] = nlp['colors'][1] 
for var_name in [
    'CSEQPOTTDIV', 'CSEQPOTTDIVNORMI',
    'CSLATH', 'CSLATHNORMI',
    'CSPOTTDIV', 'CSPOTTDIVNORMI',
    'CSPOTTHDIV', 'CSPOTTHDIVNORMI',
    'CSPOTTVDIV', 'CSPOTTVDIVNORMI',
    'CSPOTTDIVTURB', 'CSPOTTDIVTURBNORMI',
    'CSPOTTHDIVTURB', 'CSPOTTHDIVTURBNORMI',
    'CSPOTTVDIVTURB', 'CSPOTTVDIVTURBNORMI',

    'CSPOTTDIV2', 'CSPOTTDIV2NORMI',
    'CSPOTTHDIV2', 'CSPOTTHDIV2NORMI',
    'CSPOTTVDIV2', 'CSPOTTVDIV2NORMI',

    'CSPOTTDIV3', 'CSPOTTDIV3NORMI',
    'CSPOTTHDIV3', 'CSPOTTHDIV3NORMI',
    'CSPOTTVDIV3', 'CSPOTTVDIV3NORMI',

    'CSQVDIV', 'CSQVDIVNORMI',
    'CSQVHDIV', 'CSQVHDIVNORMI',
    'CSQVVDIV', 'CSQVVDIVNORMI',
    'CSQVDIVTURB', 'CSQVDIVTURBNORMI',
    'CSQVHDIVTURB', 'CSQVHDIVTURBNORMI',
    'CSQVVDIVTURB', 'CSQVVDIVTURBNORMI',
    'CSQVUVDIVTURB', 'CSQVUVDIVTURBNORMI',
    'CSQVDVDIVTURB', 'CSQVDVDIVTURBNORMI',

    'CSQVDIV2', 'CSQVDIV2NORMI',
    'CSQVHDIV2', 'CSQVHDIV2NORMI',
    'CSQVVDIV2', 'CSQVVDIV2NORMI',
    'CSQVDIV2TURB', 'CSQVDIV2TURBNORMI',
    'CSQVHDIV2TURB', 'CSQVHDIV2TURBNORMI',
    'CSQVVDIV2TURB', 'CSQVVDIV2TURBNORMI',

    'CSQVDIV3', 'CSQVDIV3NORMI',
    'CSQVHDIV3', 'CSQVHDIV3NORMI',
    'CSQVVDIV3', 'CSQVVDIV3NORMI',
    'CSQVDIV3TURB', 'CSQVDIV3TURBNORMI',
    'CSQVHDIV3TURB', 'CSQVHDIV3TURBNORMI',
    'CSQVVDIV3TURB', 'CSQVVDIV3TURBNORMI',

    'CSQV','CSQVNORMI',
    'CSQVSATDEF','CSQVSATDEFNORMI',
    'CSW','CSWNORMI',
    'CSTKEV','CSTKEVNORMI',
    'CSRH','CSRHNORMI',
    'CSBVF',
    ]:
    nlp['var_colors'][var_name] = nlp['colors'][0] 

for var_name in [
    'EQPOTT',    
    'POTTHDIV', 'POTTHDIVNORMI',
    'POTTHDIV3', 'POTTHDIVNORMI3',
    'QVHDIV', 'QVHDIVNORMI',
    'QVHDIV2', 'QVHDIV2NORMI',
    'QVHDIV3', 'QVHDIV3NORMI',
    ]:
    nlp['var_colors'][var_name] = nlp['colors'][3] 

for var_name in [
    'POTTVDIV', 'POTTVDIVNORMI',
    'POTTVDIV3', 'POTTVDIVNORMI3',
    'QVVDIV', 'QVVDIVNORMI',
    'QVVDIV2', 'QVVDIV2NORMI',
    'QVVDIV3', 'QVVDIV3NORMI',
    ]:
    nlp['var_colors'][var_name] = nlp['colors'][4] 

#for var_name in [
#    'QVDVDIVTURB', 'QVDVDIVTURBNORMI',
#    ]:
#    nlp['var_colors'][var_name] = nlp['colors'][2]
#for var_name in [
#    'CLDQVDVDIVTURB', 'CLDQVVDIVTURBNORMI',
#    ]:
#    nlp['var_colors'][var_name] = nlp['colors'][3] 
#for var_name in [
#    ]:
#    nlp['var_colors'][var_name] = nlp['colors'][4] 

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


nlp['var_plt_cfgs'] = var_plt_cfgs_glob
nlp['var_plt_cfgs']['W'] = {
    'lims': {
        'abs':  [-0.008,0.008],
        'diff': [-0.008,0.008],
        #'abs':  [-20,10],
        #'diff': [-10,10],
    },
}
for var_name in ['WNORMI','CSWNORMI']:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            'abs':  [-0.015,0.015],
            'diff': [-0.002,0.002],
        },
    }
for var_name in ['TKEVNORMI']:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            'abs':  [-0.003,0.003],
            'diff': [-0.0003,0.0003],
        },
    }
for var_name in ['BVFNORMI']:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            'abs':  [-0.0001,0.001],
            'diff': [-0.0001,0.0001],
        },
    }
for var_name in ['CLDTKEVNORMI']:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            'abs':  [-0.06,0.06],
            'diff': [-0.02,0.02],
        },
    }
nlp['var_plt_cfgs']['CLDWNORMI'] = {
    'lims': {
        'abs':  [-0.30,0.30],
        'diff': [-0.03,0.03],
    },
}
nlp['var_plt_cfgs']['CLDF'] = {
    'lims': {
        'abs':  [0,60],
        'diff': [-10,10],
    },
}
nlp['var_plt_cfgs']['CLDFNORMI'] = {
    'lims': {
        'abs':  [0,50], # cp_01
        'diff': [-8,8], # cp_01
    },
}
nlp['var_plt_cfgs']['T'] = {
    'lims': {
        'abs':  [190,300],
        'diff': [-10,10],
    },
}
nlp['var_plt_cfgs']['P'] = {
    'lims': {
        'abs':  [0,101300],
        #'diff': [-2200,2200],
        'diff': [-650,650],
        #'diff': [-50,50],
    },
}
for var_name in ['POTT','EQPOTT']:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            'abs':  [290,400],
            'diff': [-10,10],
        },
    }
nlp['var_plt_cfgs']['POTTNORMI'] = {
    'lims': {
        'abs':  [290,320],
        'diff': [1,4],
        #'diff': [1.7,3.2], # cp_01
    },
}
nlp['var_plt_cfgs']['QI'] = {
    'lims': {
        'abs':  [0,0.015],
        'diff': [-0.002,0.01],
    },
}
nlp['var_plt_cfgs']['QC'] = {
    'lims': {
        'abs':  [0,0.03],
        'diff': [-0.002,0.006],
    },
}
for var_name in [
    'QV',
    'CLDQV', 'CLDQVNORMI','CSQV', 'CSQVNORMI',
    'QVSATDEF','QVSATDEFNORMI',
    'CLDQVSATDEF','CLDQVSATDEFNORMI','CSQVSATDEF','CSQVSATDEFNORMI',
    ]:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            #'abs':  [0,20],
            #'diff': [-1,4],
            'abs':  [0,2],
            'diff': [-0.4,0.4],
        },
    }
nlp['var_plt_cfgs']['QVNORMI'] = {
    'lims': {
        'abs':  [2,16],
        'diff': [0,3], # cp_01
        #'diff': [0.7,2.1], # cp_01
    },
}
nlp['var_plt_cfgs']['RHNORMI'] = {
    'lims': {
        'abs':  [0,100],
        'diff': [-4,4], # cp_01
    },
}
nlp['var_plt_cfgs'][var_name] = {
    'lims': {
        'abs':  [0,20],
        'diff': [1,2.5], # cp_01
    },
}
nlp['var_plt_cfgs']['QVFLXZ'] = {
    'lims': {
        'abs':  [0,0.06],
        'diff': [0,0.03],
    },
}
nlp['var_plt_cfgs']['QS'] = {
    'lims': {
        'abs':  [0,3e-5],
        'diff': [-5e-6,2e-5],
    },
}
nlp['var_plt_cfgs']['U'] = {
    'lims': {
        'abs':  [-10,15],
        'diff': [-10,10],
    },
}
nlp['var_plt_cfgs']['V'] = {
    'lims': {
        'abs':  [-2,2],
        'diff': [-4,4],
    },
}
for var_name in [
    'POTTDIV', 'CSPOTTDIV', 'CLDPOTTDIV',
    'POTTHDIV', 'CSPOTTHDIV', 'CLDPOTTHDIV',
    'POTTVDIV', 'CSPOTTVDIV', 'CLDPOTTVDIV',
    'EQPOTTDIV', 'CSEQPOTTDIV', 'CLDEQPOTTDIV',
    'LATH', 'CSLATH', 'CLDLATH',

    'POTTDIV2', 'CSPOTTDIV2', 'CLDPOTTDIV2',
    'POTTHDIV2', 'CSPOTTHDIV2', 'CLDPOTTHDIV2',
    'POTTVDIV2', 'CSPOTTVDIV2', 'CLDPOTTVDIV2',

    'POTTDIV3', 'CSPOTTDIV3', 'CLDPOTTDIV3',
    'POTTHDIV3', 'CSPOTTHDIV3', 'CLDPOTTHDIV3',
    'POTTVDIV3', 'CSPOTTVDIV3', 'CLDPOTTVDIV3',
    ]:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            'abs':  [-2.00,2.00],
            'diff': [-0.50,0.50],
        },
    }
#for var_name in [
#    'POTTDIV3', 'CSPOTTDIV3', 'CLDPOTTDIV3',
#    'POTTHDIV3', 'CSPOTTHDIV3', 'CLDPOTTHDIV3',
#    'POTTVDIV3', 'CSPOTTVDIV3', 'CLDPOTTVDIV3',
#    ]:
#    nlp['var_plt_cfgs'][var_name] = {
#        'lims': {
#            'abs':  [-7.00,7.00],
#            'diff': [-7.00,7.00],
#        },
#    }
for var_name in [
    'QVDIV', 'QVDIVNORMI',
    'QVHDIV', 'QVHDIVNORMI',
    'QVVDIV', 'QVVDIVNORMI',
    'QVDIVMEAN', 'QVDIVMEANNORMI',
    'QVHDIVMEAN', 'QVHDIVMEANNORMI',
    'QVVDIVMEAN', 'QVVDIVMEANNORMI',
    'QVDIVTURB', 'QVDIVTURBNORMI',
    'QVHDIVTURB', 'QVHDIVTURBNORMI',
    'QVVDIVTURB', 'QVVDIVTURBNORMI',

    'QVDIV2', 'QVDIV2NORMI',
    'QVHDIV2', 'QVHDIV2NORMI',
    'QVVDIV2', 'QVVDIV2NORMI',
    'QVDIV2MEAN', 'QVDIV2MEANNORMI',
    'QVHDIV2MEAN', 'QVHDIV2MEANNORMI',
    'QVVDIV2MEAN', 'QVVDIV2MEANNORMI',
    'QVDIV2TURB', 'QVDIV2TURBNORMI',
    'QVHDIV2TURB', 'QVHDIV2TURBNORMI',
    'QVVDIV2TURB', 'QVVDIV2TURBNORMI',

    'QVDIV3', 'QVDIV3NORMI',
    'QVDIV3MEAN', 'QVDIV3MEANNORMI',
    'QVHDIV3MEAN', 'QVHDIV3MEANNORMI',
    'QVVDIV3MEAN', 'QVVDIV3MEANNORMI',
    'QVDIV3TURB', 'QVDIV3TURBNORMI',

    'CSQVDIV', 'CSQVDIVNORMI',
    'CSQVHDIV', 'CSQVHDIVNORMI',
    'CSQVVDIV', 'CSQVVDIVNORMI',
    'CSQVDIVTURB', 'CSQVDIVTURBNORMI',
    'CSQVHDIVTURB', 'CSQVHDIVTURBNORMI',
    'CSQVVDIVTURB', 'CSQVVDIVTURBNORMI',

    'CSQVDIV2', 'CSQVDIV2NORMI',
    'CSQVHDIV2', 'CSQVHDIV2NORMI',
    'CSQVVDIV2', 'CSQVVDIV2NORMI',
    'CSQVDIV2TURB', 'CSQVDIV2TURBNORMI',
    'CSQVHDIV2TURB', 'CSQVHDIV2TURBNORMI',
    'CSQVVDIV2TURB', 'CSQVVDIV2TURBNORMI',

    'CSQVDIV3', 'CSQVDIV3NORMI',
    'CSQVDIV3TURB', 'CSQVDIV3TURBNORMI',

    'CLDQVDIV', 'CLDQVDIVNORMI',
    'CLDQVHDIV', 'CLDQVHDIVNORMI',
    'CLDQVVDIV', 'CLDQVVDIVNORMI',
    'CLDQVDIVTURB', 'CLDQVDIVTURBNORMI',
    'CLDQVHDIVTURB', 'CLDQVHDIVTURBNORMI',
    'CLDQVVDIVTURB', 'CLDQVVDIVTURBNORMI',

    'CLDQVDIV2', 'CLDQVDIV2NORMI',
    'CLDQVHDIV2', 'CLDQVHDIV2NORMI',
    'CLDQVVDIV2', 'CLDQVVDIV2NORMI',
    'CLDQVDIV2TURB', 'CLDQVDIV2TURBNORMI',
    'CLDQVHDIV2TURB', 'CLDQVHDIV2TURBNORMI',
    'CLDQVVDIV2TURB', 'CLDQVVDIV2TURBNORMI',

    'CLDQVDIV3', 'CLDQVDIV3NORMI',
    'CLDQVDIV3TURB', 'CLDQVDIV3TURBNORMI',
    ]:
    if domain == 'trades':
        nlp['var_plt_cfgs'][var_name] = {
            'lims': {
                #'abs':  [-0.15,0.15],
                #'diff': [-0.025,0.025],
                'abs':  [-0.20,0.20],
                'diff': [-0.040,0.040],
                'rel':  [-0.5,0.5],
            },
        }
    elif domain == 'ITCZ':
        nlp['var_plt_cfgs'][var_name] = {
            'lims': {
                'abs':  [-0.1,0.2],
                'diff': [-0.05,0.05],
                'rel':  [-0.5,0.5],
            },
        }
for var_name in [
    'QVUVDIVTURB', 'QVUVDIVTURBNORMI',
    'QVDVDIVTURB', 'QVDVDIVTURBNORMI',

    'CSQVUVDIVTURB', 'CSQVUVDIVTURBNORMI',
    'CSQVDVDIVTURB', 'CSQVDVDIVTURBNORMI',

    'CLDQVUVDIV', 'CLDQVUVDIVNORMI',
    'CLDQVDVDIV', 'CLDQVDVDIVNORMI',

    'QVHDIV3', 'QVHDIV3NORMI',
    'QVVDIV3', 'QVVDIV3NORMI',
    'QVHDIV3TURB', 'QVHDIV3TURBNORMI',
    'QVVDIV3TURB', 'QVVDIV3TURBNORMI',

    'CSQVHDIV3', 'CSQVHDIV3NORMI',
    'CSQVVDIV3', 'CSQVVDIV3NORMI',
    'CSQVHDIV3TURB', 'CSQVHDIV3TURBNORMI',
    'CSQVVDIV3TURB', 'CSQVVDIV3TURBNORMI',

    'CLDQVHDIV3', 'CLDQVHDIV3NORMI',
    'CLDQVVDIV3', 'CLDQVVDIV3NORMI',
    'CLDQVHDIV3TURB', 'CLDQVHDIV3TURBNORMI',
    'CLDQVVDIV3TURB', 'CLDQVVDIV3TURBNORMI',
    ]:
    if domain == 'trades':
        nlp['var_plt_cfgs'][var_name] = {
            'lims': {
                'abs':  [-0.5,0.5],
                'diff': [-0.1,0.1],
            },
        }
    elif domain == 'ITCZ':
        nlp['var_plt_cfgs'][var_name] = {
            'lims': {
                'abs':  [-0.1,0.2],
                'diff': [-0.05,0.05],
                'rel':  [-5,5],
            },
        }
#print(nlp['var_plt_cfgs'])
#quit()
