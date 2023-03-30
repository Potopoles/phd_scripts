#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    plotting namelist for 004_11_bulk.
author			Christoph Heim
date created    22.01.2021
date changed    02.02.2021
usage			import in another script
"""
###############################################################################
import matplotlib.pyplot as plt
from base.nl_plot_global import nlp
###############################################################################

# font sizes
plt.rcParams['font.size'] = 15
plt.rcParams['axes.titlesize'] = 24
plt.rcParams['axes.labelsize'] = 24

# colors
nlp['colors'] = plt.rcParams['axes.prop_cycle'].by_key()['color']
nlp['mod_col_inds'] = ['COSMO',
    'NICAM', 'GEOS', 'ICON', 'UM', 'MPAS',
    'IFS', 'SAM', 'ARPEGE-NH', 'FV3']

nlp['mod_linewidth'] = 2.0
nlp['obs_linewidth'] = 2.5

nlp['linestyles'] = ['-', '--', ':']


config = 4
plot_type = 'box'
#plot_type = 'line'

if plot_type == 'box':
    nlp['i_aggreg_daily'] = 0
if plot_type == 'line':
    nlp['i_aggreg_daily'] = 1

#############################################################################
#############################################################################
if config == 1:
    nlp['plot_type'] = plot_type
    nlp['computation'] = 'tend'
    nlp['nrows']    = 3
    nlp['ncols']    = 4
    nlp['axes'] = {
        #(0,0)   :{
        #    'var':'edge S',
        #},
        #(0,1)   :{
        #    'var':'edge N',
        #},
        #(0,2)   :{
        #    'var':'edge W',
        #},
        #(0,3)   :{
        #    'var':'edge E',
        #},

        (0,0)   :{
            'var':'residual',
        },

        (0,1)   :{
            'var':'inv tot',
        },
        (0,2)   :{
            'var':'inv hori',
        },
        (0,3)   :{
            'var':'inv vert',
        },

        (1,0)   :{
            'var':'edge T',
        },
        (1,1)   :{
            'var':'edge tot',
        },
        (1,2)   :{
            'var':'edge hori',
        },
        (1,3)   :{
            'var':'edge vert',
        },
        (2,0)   :{
            #'var':'edge B',
            'var':'edge SFC',
        },
        (2,1)   :{
            'var':'vol tot',
        },

        #(2,2)   :{
        #    'var':'vol hori',
        #},
        #(2,3)   :{
        #    'var':'vol vert',
        #},

        (2,2)   :{
            'var':'adv + sfc tot',
        },
        (2,3)   :{
            'var':'tot',
        },
    }
    if plot_type == 'box':
        fact = 0.2
    if plot_type == 'line':
        fact = 1.0
    #nlp['ylim'] = {}
    #nlp['ylim']['QV'] = {}
    #nlp['ylim']['QC'] = {}
    #nlp['ylim']['POTT'] = {}
    #nlp['ylim']['QV']['total'] = (-1.0E-4*fact,1.0E-4*fact)
    #nlp['ylim']['QV']['above'] = (-1.0E-4*fact,1.0E-4*fact)
    #nlp['ylim']['QV']['below'] = (-4.0E-4*fact,4.0E-4*fact)
    #nlp['ylim']['POTT']['total'] = (-1.5*fact,1.5*fact)
    #nlp['ylim']['POTT']['above'] = (-3.0*fact,3.0*fact)
    #nlp['ylim']['POTT']['below'] = (-9.0*fact,9.0*fact)
    #nlp['ylim']['QC'] = nlp['ylim']['QV']

    stretch = 1.8
    nlp['figsize']  = (11*stretch,8*stretch) 
    nlp['arg_subplots_adjust']  = {
                                    'left':0.10,
                                    'right':0.98,
                                    'bottom':0.15,
                                    'top':0.96,
                                    'wspace':0.35,
                                    'hspace':0.85,
                                  }

#############################################################################
#############################################################################
elif config == 2:
    nlp['plot_type'] = plot_type
    nlp['computation'] = 'mean'
    nlp['nrows']    = 1
    nlp['ncols']    = 1
    nlp['axes'] = {
        (0,0)   :{
            'var':'mean',
        },
    }

    stretch = 1.0
    nlp['figsize']  = (8*stretch,6*stretch) 
    nlp['arg_subplots_adjust']  = {
                                    'left':0.20,
                                    'right':0.98,
                                    'bottom':0.25,
                                    'top':0.94,
                                    'wspace':0.35,
                                    'hspace':0.50,
                                  }


#############################################################################
#############################################################################
elif config == 3:
    raise NotImplementedError()
    nlp['plot_type'] = 'box'
    #nlp['plot_type'] = 'line'

    nlp['nrows']    = 2
    nlp['ncols']    = 3
    nlp['axes'] = {
        (0,0)   :{
            'var':'vol hori',
        },
        (0,1)   :{
            'var':'vol vert',
        },
        (0,2)   :{
            'var':'vol tot',
        },
        (1,0)   :{
            'var':'inv hori',
        },
        (1,1)   :{
            'var':'inv vert',
        },
        (1,2)   :{
            'var':'inv tot',
        },
    }
    nlp['ylim'] = {}
    nlp['ylim']['QV'] = {}
    nlp['ylim']['POTT'] = {}
    nlp['ylim']['QV']['below'] = (-7E-8,7E-8)
    nlp['ylim']['QV']['above'] = (-2E-8,2E-8)
    nlp['ylim']['QV']['total'] = (-2E-8,2E-8)
    nlp['ylim']['POTT']['below'] = (-0.0025,0.0025)
    nlp['ylim']['POTT']['above'] = (-0.0010,0.0010)
    nlp['ylim']['POTT']['total'] = (-0.0005,0.0005)


    stretch = 1.8
    nlp['figsize']  = (11*stretch,7*stretch) 
    nlp['arg_subplots_adjust']  = {
                                    'left':0.05,
                                    'right':0.98,
                                    'bottom':0.15,
                                    'top':0.95,
                                    'wspace':0.35,
                                    'hspace':0.50,
                                  }

if config == 4:
    nlp['plot_type'] = plot_type
    nlp['computation'] = 'tend'
    nlp['nrows']    = 2
    nlp['ncols']    = 3
    nlp['axes'] = {
        (1,1)   :{
            'var':'edge S',
        },
        (0,1)   :{
            'var':'edge N',
        },
        (0,0)   :{
            'var':'edge W',
        },
        (0,2)   :{
            'var':'edge E',
        },

        (1,2)   :{
            'var':'edge hori',
        },
    }
    #if plot_type == 'box':
    #    fact = 0.2
    #if plot_type == 'line':
    #    fact = 1.0
    #nlp['ylim'] = {}
    #nlp['ylim']['QV'] = {}
    #nlp['ylim']['QC'] = {}
    #nlp['ylim']['POTT'] = {}
    #nlp['ylim']['QV']['total'] = (-1.0E-4*fact,1.0E-4*fact)
    #nlp['ylim']['QV']['above'] = (-1.0E-4*fact,1.0E-4*fact)
    #nlp['ylim']['QV']['below'] = (-4.0E-4*fact,4.0E-4*fact)
    #nlp['ylim']['POTT']['total'] = (-1.5*fact,1.5*fact)
    #nlp['ylim']['POTT']['above'] = (-3.0*fact,3.0*fact)
    #nlp['ylim']['POTT']['below'] = (-9.0*fact,9.0*fact)
    #nlp['ylim']['QC'] = nlp['ylim']['QV']

    stretch = 1.4
    nlp['figsize']  = (11*stretch,8*stretch) 
    nlp['arg_subplots_adjust']  = {
                                    'left':0.10,
                                    'right':0.98,
                                    'bottom':0.15,
                                    'top':0.96,
                                    'wspace':0.35,
                                    'hspace':0.85,
                                  }

else: raise ValueError()






nlp['panel_label_x_left_shift'] = 0.14
nlp['panel_label_y_pos'] = 0.94
