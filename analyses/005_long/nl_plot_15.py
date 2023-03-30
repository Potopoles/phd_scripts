#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    plotting namelist for 004_04_latlon_sects:
author			Christoph Heim
date created    16.07.2020
date changed    20.09.2022
usage			import in another script
"""
###############################################################################
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
###############################################################################
nlp = {}

stretch = 1.0

nlp['geo_plot']     = False

#### PLOT RESOLUTION
nlp['dpi'] = 600


# font sizes
plt.rcParams['font.size'] = 10*stretch
plt.rcParams['axes.labelsize'] = 10*stretch
plt.rcParams['axes.titlesize'] = 14*stretch
plt.rcParams['figure.titlesize'] = 15*stretch

# colors
nlp['colors'] = {'abs':{},'diff':{}}
nlp['linewidths'] = {'abs':{},'diff':{}}
nlp['linestyles'] = {'abs':{},'diff':{}}
nlp['ylims'] = {'abs':{},'diff':{}}

nlp['line_axes_colors'] = {
    'l1':['#000000','#8585ad','#d1d1e0'],
    'r1':['#cc3300','#ff9900','#e6e600'],
    'r2':['#3333ff','#0099cc','#00cc99'],
}

nlp['linestyles'] = ['-', '--', ':']
#nlp['linestyles'] = ['-', '-', '-']


nlp['panel_label_size'] = 24 * stretch
nlp['panel_label_x_left_shift'] = 0.42
nlp['panel_label_y_pos'] = 1.18
nlp['panel_labels'] = ['a.','b.','c.','d.','e.','f.','g.','h.','i.','j.']



### VARIABLE PLOT CONFIGURATIONS
##############################################################################
nlp['var_plt_cfgs'] = {}

for var_name in [
    'CLCL','CLCM','CLCH',
    ]:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            'abs':  [0,80],
            'diff': [-9,9],
            'rel':  [-0.2,0.2],
        },
    }

for var_name in [
    'RH@alt=3000',
    ]:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            'abs':  [0,100],
            'diff': [-3,7],
            'rel':  [-0.2,0.2],
        },
    }

for var_name in [
    'RH',
    ]:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            'abs':  [0,100],
            'diff': [-10,10],
            'rel':  [-0.2,0.2],
        },
    }

for var_name in [
    'LWDTOA','SWNDTOA','RADNDTOA',
    'CLWDTOA','CSWNDTOA','CRADNDTOA',
    'CRELWDTOA','CRESWNDTOA','CRERADNDTOA',
    ]:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            #'abs':  [-350,350],
            'abs':  [-120,0],
            #'diff': [-15,15],
            'diff': [-20,20],
        },
    }
for var_name in [
    'ALBEDO',
    ]:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            'abs':  [0,0.4],
            'diff': [-0.1,0.1],
            'rel': [-0.2,0.2],
        },
    }

nlp['var_plt_cfgs']['CLDF'] = {
    'lims': {
        'abs':  [0,30],
        'diff': [-10,10],
    },
}
for var_name in [
    #'SLHFLX',
    'WVPHCONV','QVWFLX',
    'PP','ENTRDRY',
    ]:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            'abs':  [0,10],
            #'diff': [-3,3],
            #'abs':  [-5,10], # cp_01
            'diff': [-1,1], # cp_01
            'rel': [-0.4,0.4], # cp_01
        },
    }
for var_name in [
    'SLHFLX'
    ]:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            'abs':  [-300,300],
            'diff': [-20,20],
        },
    }
#for var_name in [
#    'PP',
#    ]:
#    nlp['var_plt_cfgs'][var_name] = {
#        'lims': {
#            'abs':  [0,3],
#            #'diff': [-3,3],
#            #'abs':  [-5,10], # cp_01
#            'diff': [-0.5,0.5], # cp_01
#        },
#    }
#for var_name in [
#    'ENTRDRY',
#    ]:
#    nlp['var_plt_cfgs'][var_name] = {
#        'lims': {
#            'abs':  [0,0.1],
#            'diff': [-0.025,0.025],
#        },
#    }
#for var_name in [
#    'BUOYIFLX',
#    ]:
#    nlp['var_plt_cfgs'][var_name] = {
#        'lims': {
#            'abs':  [0,1E-4],
#            'diff': [-2.5E-5,2.5E-5],
#            'rel': [-0.3,0.3],
#        },
#    }
for var_name in [
    'IWPHCONV',
    ]:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            'abs':  [-0.01,0.01],
            'diff': [-0.01,0.01],
        },
    }


for var_name in [
    'T2M','T',
    ]:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            'abs':  [280,305],
            #'diff': [1,3],
            'diff': [1,3.5],
        },
    }
for var_name in [
    'TSURF','SST',
    ]:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            #'abs':  [287,302],
            'abs':  [292.5,302.5],
            'diff': [1.0,3.5],
        },
    }
for var_name in [
    'DQVINV',
    ]:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            'abs':  [5,10],
            'diff': [0.4,1.9],
        },
    }
for var_name in [
    'QVHDIV','QVVDIV','QVXDIV','QVYDIV',
    'dQVdt_MBL_LH',
    ]:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            'abs':  [-0.15,0.15],
            'diff': [-0.02,0.02],
        },
    }
for var_name in [
    'T@alt=3000',
    ]:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            'abs':  [280,290],
            'diff': [2.5,5.0],
        },
    }
for var_name in [
    'T@alt=300',
    ]:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            'abs':  [280,305],
            'diff': [1,4],
        },
    }
nlp['var_plt_cfgs']['QVSATDEF'] = {
    'lims': {
        'abs':  [0,15],
        'diff': [0,2],
    },
}

for var_name in ['LTS','EIS']:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            'abs':  [15,25],
            'diff': [0.0,2.5],
            'rel': [-0.2,0.2],
        },
    }
for var_name in ['INVSTRV']:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            'abs':  [2,17],
            'diff': [0.0,2.5],
            'rel': [-0.2,0.2],
        },
    }
for var_name in [
    'ENTR','ENTRH','ENTRV',
    'ENTRSCL','ENTRHSCL','ENTRVSCL',
    ]:
    nlp['var_plt_cfgs'][var_name] = {
    'lims': {
        # m/s
        'abs': [0.0,0.01],
        'diff': [-0.001,0.001],
        'rel': [-0.1,0.1],
        #### hPa/d
        #'abs': [-3,3],
        #'diff': [-10,10],
    },
}

for var_name in [
    'POTTHDIV3',
    'POTTHDIV',
    'POTTXDIV',
    'POTTYDIV',
    'POTTVDIV',
    'dTdt_MBL_SH',
    ]:
    nlp['var_plt_cfgs'][var_name] = {
    'lims': {
        'abs': [-3.0,3.0],
        'diff': [-0.3,0.3],
    },
}

for var_name in [
    'dRHdt',
    'dRHdt_MBL_FLX',
    ]:
    nlp['var_plt_cfgs'][var_name] = {
    'lims': {
        'abs':  [- 1.0, 1.0],
        'diff': [- 0.1, 0.1],
    },
}

for var_name in [
    'W',
    ]:
    nlp['var_plt_cfgs'][var_name] = {
    'lims': {
        ## m/s
        #'abs': [-0.007,0.007],
        #'diff': [-0.0005,0.0005],
        ### hPa/d
        'abs': [0,50],
        'diff': [-5,5],
        'rel': [-0.2,0.2],
    },
}

#nlp['var_plt_cfgs']['QV'] = {
#    'lims': {
#        #'abs':  [0,18],
#        'diff': [0.5,2.5],
#        #'diff': [1.5,2.5], # cp_01
#    },
#}
for var_name in [
    'QV@alt=3000',
    ]:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            'abs':  [0,18],
            'diff': [0.0,2.0],
        },
    }
for var_name in [
    'QV@alt=16000',
    'QV@alt=15000',
    'QV@alt=14000',
    'QV@alt=13000',
    'QV@alt=12000',
    ]:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            'abs':  [0,1E-1],
            'diff': [0,1E-1],
            'rel':  [0,2],
        },
    }
for var_name in [
    'T@alt=16000',
    'T@alt=15000',
    'T@alt=14000',
    'T@alt=13000',
    'T@alt=12000',
    ]:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            'abs':  [190,240],
            'diff': [2,10],
            'rel':  [-0.05,0.05],
        },
    }
for var_name in [
    'DINVHGTLCL','DINVHGTLOWCLDBASE'
    ]:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            'abs': [0,2500],
            'diff': [-200,200],
        },
    }
for var_name in [
    'INVHGT',#'LOWCLDBASE','LCL'
    ]:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            #'abs': [0,2500],
            #'diff': [-200,200],
            'abs': [500,2500],
            'diff': [-150,150],
        },
    }
for var_name in [
    'LOWCLDBASE','LCL'
    ]:
    nlp['var_plt_cfgs'][var_name] = {
        'lims': {
            'abs': [300,700],
            'diff': [-50,50],
        },
    }
nlp['var_plt_cfgs']['UV10M'] = {
    'lims': {
        'abs':  [0,8],
        'diff': [-0.5,0.5],
        #'diff': [1.5,2.5], # cp_01
    },
}
nlp['var_plt_cfgs']['SSHFLX'] = {
    'lims': {
        'abs':  [0,30],
        'diff': [-5,5],
        #'diff': [1.5,2.5], # cp_01
    },
}
