#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    plotting namelist for 004_04_cross_sects:
author			Christoph Heim
date created    16.07.2020
date changed    26.04.2022
usage			import in another script
"""
###############################################################################
import copy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from base.nl_plot_global import cmap_symzero,cmap_diff,cmap_RdBu_r_positive
from package.plot_functions import get_levels_sym_zero
###############################################################################

domain = 'Trades'
domain = 'ITCZ'

nlp = {}

stretch = 1.0

nlp['geo_plot']     = False

#### PLOT RESOLUTION
nlp['dpi'] = 600


# font sizes
plt.rcParams['font.size'] = 10*stretch
plt.rcParams['axes.labelsize'] = 13*stretch
plt.rcParams['axes.titlesize'] = 18*stretch


nlp['panel_label_kwargs'] = {
    'fontsize':     14*stretch,
    'shift_right':  -0.10,
    'shift_up':      0.04,
}


nlp['contour_linewidths'] = {
    #'abs': [0.50, 1.00, 1.25, 1.50],
    #'diff':[1.50, 1.25, 1.00, 0.50, 0.50, 1.00, 1.25, 1.50],
    #'bias':[1.50, 1.25, 1.00, 0.50, 0.50, 1.00, 1.25, 1.50],

    #'abs': [0.50, 1.00],
    #'diff':[1.00, 0.50, 0.50, 1.00],
    #'bias':[1.00, 0.50, 0.50, 1.00],

    'abs': [1.00],
    'diff':[1.00, 1.00],
    'bias':[1.00, 1.00],
}


nlp['linewidths'] = [
    1.5,
    1.5,
    1.5,
]
nlp['colors'] = [
    'red',
    #'orange',
    'white',
    'white',
]
nlp['linestyles'] = [
    '-',
    '--',
    ':',
]


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
nlp['oom'] = {
    'cf':{'abs':{},'diff':{},'bias':{},'rel':{}},
    'cl':{'abs':{},'diff':{},'bias':{},'rel':{}},
}



######### variables QC and QI
##############################################################################
for var_name in ['QC', 'QI', 'QCNORMI', 'CLDW']:
    #nlp['levels']['cl']['abs'][var_name] = [1E-3, 2E-3, 5E-3, 1E-2, 5E-2] 
    nlp['levels']['cl']['abs'][var_name] = [1E-3, 3E-3, 1E-2, 3E-2] 
    nlp['cb_ticks']['cl']['abs'][var_name] = nlp['levels']['cl']['abs'][var_name]

    #nlp['levels']['cl']['diff'][var_name] = [-1E-2, -5E-3, -2E-3, -1E-3, 1E-3, 2E-3, 5E-3, 1E-2] 
    nlp['levels']['cl']['diff'][var_name] = [-3E-2, -1E-2, -3E-3, -1E-3, 1E-3, 3E-3, 1E-2, 3E-2] 
    nlp['cb_ticks']['cl']['diff'][var_name] = nlp['levels']['cl']['diff'][var_name]

#cmap = plt.cm.GnBu
#my_cmap = cmap(np.linspace(0.0, 1.00, cmap.N))
#my_cmap = ListedColormap(my_cmap)


cmap = plt.cm.PiYG
my_cmap = cmap(np.linspace(0.50, 1.00, cmap.N))
my_cmap[:,-1] = np.linspace(0.0, 0.6, cmap.N)
my_cmap = ListedColormap(my_cmap)
var_name = 'QC'
nlp['cmaps']['cf']['abs'][var_name] = my_cmap
nlp['levels']['cf']['abs'][var_name] = np.linspace(1E-4, 1E-2, 100)
nlp['cb_ticks']['cf']['abs'][var_name] = nlp['levels']['cf']['abs'][var_name]

var_name = 'QI'
nlp['cmaps']['cf']['abs'][var_name] = my_cmap
nlp['levels']['cf']['abs'][var_name] = np.linspace(1E-4, 1E-2, 100)
nlp['cb_ticks']['cf']['abs'][var_name] = nlp['levels']['cf']['abs'][var_name]


for var_name in ['QC', 'QI']:
    #cmap = plt.cm.PiYG_r
    ##cmap = plt.cm.BrBG_r
    #my_cmap = cmap(np.linspace(0.00, 1.00, cmap.N))
    #my_cmap[:,-1] = (np.linspace(-1.0, 1.0, cmap.N)**2)**(1/2)
    #my_cmap = ListedColormap(my_cmap)

    cmap = plt.cm.PRGn_r
    my_cmap = cmap(np.linspace(0.0, 1.00, cmap.N))
    my_cmap[:,-1] = (np.linspace(-1.0, 1.0, cmap.N)**2)**(1/2)
    my_cmap = ListedColormap(my_cmap)

    nlp['cmaps']['cf']['diff'][var_name] = my_cmap
    nlp['levels']['cf']['diff'][var_name] = np.linspace(-1E-2, 1E-2, 100)
    nlp['cb_ticks']['cf']['diff'][var_name] = nlp['levels']['cf']['diff'][var_name]

######## variables of cloud fraction
#############################################################################
for var_name in [
    'CLDF', 'CLDFNORMI','CLDMASK',
    'LCLDF1E-3', 'LCLDF5E-4', 'LCLDF2E-4', 'LCLDF1E-4', 'LCLDF5E-5', 'LCLDF2E-5', 'LCLDF1E-5',
    'ICLDF1E-3', 'ICLDF5E-4', 'ICLDF2E-4', 'ICLDF1E-4', 'ICLDF5E-5', 'ICLDF2E-5', 'ICLDF1E-5',
    'LCLDF1E-3NORMI', 'LCLDF5E-4NORMI', 'LCLDF2E-4NORMI', 
    'LCLDF1E-4NORMI', 'LCLDF5E-5NORMI', 'LCLDF2E-5NORMI', 'LCLDF1E-5NORMI',
    'ICLDF1E-3NORMI', 'ICLDF5E-4NORMI', 'ICLDF2E-4NORMI', 
    'ICLDF1E-4NORMI', 'ICLDF5E-5NORMI', 'ICLDF2E-5NORMI', 'ICLDF1E-5NORMI',
    ]:
    #nlp['levels']['cl']['abs'][var_name] = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
    #nlp['levels']['cl']['diff'][var_name] = [-20, -10, -5, -2, 2, 5, 10, 20]
    
    #nlp['levels']['cl']['abs'][var_name] = [3, 15]
    #nlp['levels']['cl']['diff'][var_name] = [-15, -3, 3, 15]

    if domain == 'Trades':
        nlp['levels']['cl']['abs'][var_name] = [2]
        nlp['levels']['cl']['diff'][var_name] = [-0.5, 0.5]
    elif domain == 'ITCZ':
        nlp['levels']['cl']['abs'][var_name] = [5]
        #nlp['levels']['cl']['diff'][var_name] = [-2, 2]
        #nlp['levels']['cl']['bias'][var_name] = [-2, 2]
        nlp['levels']['cl']['diff'][var_name] = [-1, 1]
        nlp['levels']['cl']['bias'][var_name] = [-2, 2]

    cmap = plt.cm.viridis_r
    abs_cmap = cmap(np.linspace(0.00, 1.00, cmap.N))
    abs_cmap[:,-1] = np.linspace(0.0, 1.0, cmap.N)**(1./2.)
    abs_cmap = ListedColormap(abs_cmap)
    nlp['cmaps']['cf']['abs'][var_name] = abs_cmap

    cmap = plt.cm.RdBu_r
    diff_cmap = cmap(np.linspace(0.00, 1.00, cmap.N))
    diff_cmap = ListedColormap(diff_cmap)
    nlp['cmaps']['cf']['diff'][var_name] = diff_cmap

    if domain == 'Trades':
        nlp['levels']['cf']['abs'][var_name] = [0,2,10,20,30,40,50]
        nlp['cb_ticks']['cf']['abs'][var_name] = nlp['levels']['cf']['abs'][var_name]

        range = 6
        delta = 1

        nlp['levels']['cf']['diff'][var_name] = np.arange(-range+delta/2,range,delta)
        #nlp['levels']['cf']['diff'][var_name] = np.arange(-5,5.1,2)
        nlp['cb_ticks']['cf']['diff'][var_name] = nlp['levels']['cf']['diff'][var_name]
    elif domain == 'ITCZ':
        #nlp['levels']['cf']['abs'][var_name] = np.arange(0, 30.1, 3)
        #nlp['levels']['cf']['abs'][var_name] = np.arange(0, 45.1, 5)
        nlp['levels']['cf']['abs'][var_name] = [0,2,5,10,15,20,25,30,35,40,45]
        #nlp['levels']['cf']['abs'][var_name] = [0,2,4,6,8,10,12,14,16,18,20]
        nlp['cb_ticks']['cf']['abs'][var_name] = nlp['levels']['cf']['abs'][var_name]

        #nlp['levels']['cf']['diff'][var_name] = np.arange(-10, 10.1, 2)
        nlp['levels']['cf']['diff'][var_name] = [-9,-7,-5,-3,-1,1,3,5,7,9]
        nlp['cb_ticks']['cf']['diff'][var_name] = nlp['levels']['cf']['diff'][var_name]
    else: raise NotImplementedError()




#cmap = plt.cm.plasma
#my_cmap = cmap(np.linspace(0.0, 1.00, cmap.N))
#my_cmap[:,-1] = np.linspace(0.4, 0.4, cmap.N)
#my_cmap = ListedColormap(my_cmap)
#for var_name in ['QR', 'QG', 'QS']:
#    nlp['cmaps']['abs'][var_name] = my_cmap
#    nlp['levels']['abs'][var_name] = [5E-3, 1E-2, 2E-2, 4E-2, 8E-2] 
#    nlp['cb_ticks']['abs'][var_name] = [5E-3, 1E-2, 2E-2, 4E-2, 8E-2]
#

######## variable T
#############################################################################
for var_name in ['T', 'TNORMI']:
    cmap = plt.cm.cividis
    cmap = plt.cm.plasma
    my_cmap = cmap(np.linspace(0.0, 1.00, cmap.N))
    #my_cmap[:,-1] = np.linspace(0.4, 0.4, cmap.N)
    my_cmap = ListedColormap(my_cmap)
    nlp['cmaps']['cf']['abs'][var_name] = my_cmap

    nlp['cmaps']['cf']['diff'][var_name] = cmap_RdBu_r_positive
    if domain == 'Trades':
        max = 4.5 # low domains
        nlp['levels']['cf']['abs'][var_name] = np.arange(275,295*1.01,0.5)
        nlp['cb_ticks']['cf']['abs'][var_name] = np.arange(275,295*1.01,5)
    elif domain == 'ITCZ':
        max = 10
        nlp['levels']['cf']['abs'][var_name] = np.arange(190,300*1.01,10)
        nlp['cb_ticks']['cf']['abs'][var_name] = nlp['levels']['cf']['abs'][var_name][::2]
    else: raise NotImplementedError()

    nlp['levels']['cf']['diff'][var_name] = np.arange(2,max*1.01,1.0)
    nlp['cb_ticks']['cf']['diff'][var_name] = np.arange(2,max*1.01,2.0)

    nlp['cmaps']['cf']['bias'][var_name] = 'RdBu_r'
    #nlp['levels']['cf']['bias'][var_name] = np.arange(-2,2*1.01,0.5)
    #nlp['cb_ticks']['cf']['bias'][var_name] = np.arange(-2,2*1.01,1.0)
    range = 2.4
    delta = 0.4
    nlp['levels']['cf']['bias'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks']['cf']['bias'][var_name] = nlp['levels']['cf']['bias'][var_name][::2]


######## variable POTT
#############################################################################
for var_name in ['POTT','POTTNORMI']:
    cmap = plt.cm.cividis
    my_cmap = cmap(np.linspace(0.0, 1.00, cmap.N))
    my_cmap = ListedColormap(my_cmap)
    nlp['cmaps']['cf']['abs'][var_name] = my_cmap

    nlp['cmaps']['cf']['diff'][var_name] = 'Reds'
    if domain == 'Trades':
        max = 4.5 # low domains
        nlp['levels']['cf']['abs'][var_name] = np.arange(290,320*1.01,5)
        nlp['cb_ticks']['cf']['abs'][var_name] = nlp['levels']['cf']['abs'][var_name]
    elif domain == 'ITCZ':
        max = 8.0 # NS cs, ITCZ
        nlp['levels']['cf']['abs'][var_name] = np.arange(300,360*1.01,0.5)
        nlp['cb_ticks']['cf']['abs'][var_name] = np.arange(300,360*1.01,5)

    if domain == 'Trades':
        if var_name == 'POTTNORMI':
            nlp['levels']['cf']['diff'][var_name] = np.arange(1.5,3.5*1.01,0.25)
        elif var_name == 'POTT':
            nlp['levels']['cf']['diff'][var_name] = np.arange(2.0,4.5*1.01,0.5) # cp_01
        nlp['cb_ticks']['cf']['diff'][var_name] = nlp['levels']['cf']['diff'][var_name] 
    else:
        nlp['levels']['cf']['diff'][var_name] = np.arange(2,max*1.01,0.1)
        nlp['cb_ticks']['cf']['diff'][var_name] = np.arange(2,max*1.01,0.5)


######### variable QV
##############################################################################
for var_name in ['QV','QVNORMI','NCOLIQV']:
    #cmap = plt.cm.cool
    #my_cmap = cmap(np.linspace(0.4, 1.00, cmap.N))
    cmap = plt.cm.plasma
    my_cmap = cmap(np.linspace(0.0, 1.00, cmap.N))
    my_cmap = ListedColormap(my_cmap)
    nlp['cmaps']['cf']['abs'][var_name] = my_cmap
    nlp['levels']['cf']['abs'][var_name] = np.arange(2,14*1.01,1)
    nlp['cb_ticks']['cf']['abs'][var_name] = np.arange(2,14*1.01,2)

    if domain == 'Trades':
        nlp['cmaps']['cf']['diff'][var_name] = cmap_RdBu_r_positive
        nlp['levels']['cf']['diff'][var_name] = np.arange(0.75,2.5*1.01,0.25)
        nlp['cb_ticks']['cf']['diff'][var_name] = nlp['levels']['cf']['diff'][var_name]
    else:
        nlp['cmaps']['cf']['diff'][var_name] = cmap_RdBu_r_positive
        nlp['levels']['cf']['diff'][var_name] = np.arange(1.0,2.5*1.01,0.3)
        nlp['cb_ticks']['cf']['diff'][var_name] = np.arange(1.0,2.5*1.01,0.6)

    nlp['cmaps']['cf']['bias'][var_name] = cmap_diff
    nlp['levels']['cf']['bias'][var_name] = np.arange(-1,1*1.01,0.2)
    nlp['cb_ticks']['cf']['bias'][var_name] = np.arange(-1,1*1.01,0.5)

    nlp['cmaps']['cf']['rel'][var_name] = cmap_RdBu_r_positive
    nlp['levels']['cf']['rel'][var_name] = np.arange(0,2.4*1.01,0.2)
    nlp['cb_ticks']['cf']['rel'][var_name] = nlp['levels']['cf']['rel'][var_name][::2]


######### variable RH
##############################################################################
for var_name in ['RH', 'RHNORMI']:
    my_cmap = plt.cm.YlGnBu
    my_cmap = plt.cm.plasma
    nlp['cmaps']['cf']['abs'][var_name] = my_cmap
    nlp['levels']['cf']['abs'][var_name] = np.arange(0,100*1.01,10)
    nlp['cb_ticks']['cf']['abs'][var_name] = np.arange(0,100*1.01,10)

    nlp['cmaps']['cf']['diff'][var_name] = 'RdBu_r'
    #nlp['cmaps']['cf']['diff'][var_name] = 'PuOr_r'
    if domain in ['Trades', 'ITCZ_low']:
        range=5
        delta=1
    elif domain in ['ITCZ']:
        range=20
        delta=4
    else: raise NotImplementedError()
    #nlp['levels']['cf']['diff'][var_name] = np.arange(-range,range*1.01,4)
    #nlp['levels']['cf']['diff'][var_name] = [-18,-14,-10,-6,-2,2,6,10,14,18]
    nlp['levels']['cf']['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks']['cf']['diff'][var_name] = nlp['levels']['cf']['diff'][var_name]

    #nlp['levels']['cl']['abs'][var_name] = np.linspace(20,100,10)
    #nlp['levels']['cl']['diff'][var_name] = np.linspace(-12,12,9)

######### variable U
##############################################################################
for var_name in ['U', 'UNORMI']:
    if domain in ['Trades', 'ITCZ_low']:
        range = 10 # ITCZ, trades
    elif domain == 'ITCZ':
        #range = 15
        range = 30
    else: raise NotImplementedError()
    nlp['cmaps']['cf']['abs'][var_name] = 'RdBu_r' 
    nlp['levels']['cf']['abs'][var_name] = np.arange(-range,range*1.01,5)
    nlp['cb_ticks']['cf']['abs'][var_name] = np.arange(-range,range*1.01,10)
    if domain in ['Trades', 'ITCZ_low']:
        range = 1 # trades
    elif domain == 'ITCZ':
        #range = 8
        range = 15
    else: raise NotImplementedError()
    nlp['cmaps']['cf']['diff'][var_name] = 'RdBu_r' 
    nlp['levels']['cf']['diff'][var_name] = np.arange(-range,range*1.01,2.5)
    nlp['cb_ticks']['cf']['diff'][var_name] = np.arange(-range,range*1.01,5)

    #nlp['levels']['cl']['abs'][var_name] = np.linspace(-range,range,13)
    #nlp['levels']['cl']['diff'][var_name] = np.linspace(-range/2-1,range/2-1,16)

######### variable V
##############################################################################
for var_name in ['V', 'VNORMI']:
    #range = 6
    range = 5
    nlp['cmaps']['cf']['abs'][var_name] = 'PRGn_r' 
    #nlp['levels']['cf']['abs'][var_name] = np.arange(-range,range*1.01,0.5)
    #nlp['cb_ticks']['cf']['abs'][var_name] = np.arange(-range,range*1.01,2)
    nlp['levels']['cf']['abs'][var_name] = np.arange(-range+0.5,range,1.)
    nlp['cb_ticks']['cf']['abs'][var_name] = np.arange(-range+0.5,range,1)

    if domain in ['Trades', 'ITCZ_low']:
        range = 1 # trades, ITCZ low
    elif domain == 'ITCZ':
        #range = 3
        range = 2
    else: raise NotImplementedError()
    nlp['cmaps']['cf']['diff'][var_name] = 'RdBu_r' 
    nlp['levels']['cf']['diff'][var_name] = np.arange(-range+0.2,range,0.4)
    nlp['cb_ticks']['cf']['diff'][var_name] = np.arange(-range+0.2,range*1.01,0.4)

    if domain in ['Trades', 'ITCZ_low']:
        range = 1 # trades, ITCZ low
    elif domain == 'ITCZ':
        range = 2.8
    else: raise NotImplementedError()
    nlp['cmaps']['cf']['bias'][var_name] = 'RdBu_r' 
    nlp['levels']['cf']['bias'][var_name] = np.arange(-range+0.2,range,0.4)
    nlp['cb_ticks']['cf']['bias'][var_name] = np.arange(-range+0.2,range*1.01,0.4)


######### variable VFLX
##############################################################################
for var_name in ['VFLX']:
    cmap = plt.cm.PRGn_r
    cmap = plt.cm.PuOr_r
    cmap = plt.cm.PiYG_r
    my_cmap = cmap(np.linspace(0.0, 1.00, cmap.N))
    my_cmap = ListedColormap(my_cmap)
    ## Heim et al 2023 JGR (1)
    #range = 2
    #delta = 0.4
    range = 3.2
    delta = 0.4
    nlp['cmaps'     ]['cf']['abs'][var_name] = my_cmap
    nlp['levels'    ]['cf']['abs'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['cf']['abs'][var_name] = nlp['levels']['cf']['abs'][var_name][::2]
    nlp['oom'       ]['cf']['abs'][var_name] = 0

    cmap = plt.cm.RdBu_r
    my_cmap = cmap(np.linspace(0.0, 1.00, cmap.N))
    my_cmap = ListedColormap(my_cmap)
    ## Heim et al 2023 JGR (1)
    #range = 0.7
    #delta = 0.1
    range = 1.2
    delta = 0.2
    nlp['cmaps'     ]['cf']['diff'][var_name] = my_cmap
    nlp['levels'    ]['cf']['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['cf']['diff'][var_name] = nlp['levels']['cf']['diff'][var_name][::2]
    nlp['oom'       ]['cf']['diff'][var_name] = 0

    range = 1.4
    delta = 0.2
    nlp['cmaps'     ]['cf']['bias'][var_name] = my_cmap
    nlp['levels'    ]['cf']['bias'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['cf']['bias'][var_name] = nlp['levels']['cf']['bias'][var_name][::2]
    nlp['oom'       ]['cf']['bias'][var_name] = 0


######### variable UV
##############################################################################
for var_name in ['UV', 'UVNORMI']:
    range = 10
    nlp['cmaps']['cf']['abs'][var_name] = 'Reds' 
    nlp['levels']['cf']['abs'][var_name] = np.arange(4,range*1.01,0.25)
    nlp['cb_ticks']['cf']['abs'][var_name] = np.arange(4,range*1.01,2)
    range = 2 # ICTZ deep
    range = 1 # trades, ITCZ low
    nlp['cmaps']['cf']['diff'][var_name] = 'RdBu_r' 
    nlp['levels']['cf']['diff'][var_name] = np.arange(-range,range*1.01,0.1)
    nlp['cb_ticks']['cf']['diff'][var_name] = np.arange(-range,range*1.01,1)

    #nlp['levels']['cl']['abs'][var_name] = np.linspace(-range,range,7)
    #nlp['levels']['cl']['diff'][var_name] = np.linspace(-range/2-1,range/2-1,7)

######### variable W
##############################################################################
for var_name in ['W', 'WNORMI']:
    #cmap = plt.cm.PiYG
    cmap = plt.cm.PRGn_r
    my_cmap = cmap(np.linspace(0.0, 1.00, cmap.N))
    #my_cmap[:,-1] = (np.linspace(-1.0, 1.0, cmap.N)**2)**(1/2)
    my_cmap = ListedColormap(my_cmap)
    if domain in ['Trades', 'ITCZ_low']:
        fact = 0.5 # trades
    elif domain == 'ITCZ':
        #fact = 1.0 # NS cs
        fact = 0.6 # NS cs
    else: raise NotImplementedError()
    nlp['cmaps']['cf']['abs'][var_name] = my_cmap
    #nlp['levels']['cf']['abs'][var_name] = np.arange(-0.01*fact,0.01*fact*1.01,0.001)
    #nlp['cb_ticks']['cf']['abs'][var_name] = np.arange(-0.01*fact,0.01*fact,0.002)
    #nlp['levels']['cf']['abs'][var_name] = np.arange(-0.01*fact,0.01*fact,0.001)+0.0005
    #nlp['cb_ticks']['cf']['abs'][var_name] = [-0.0055,-0.0035,-0.0015,0.0,0.0015,0.0035,0.0055]
    #nlp['oom'     ]['cf']['abs'][var_name] = -2

    range = 0.006
    delta = 0.001
    nlp['cmaps'     ]['cf']['abs'][var_name] = my_cmap
    nlp['levels'    ]['cf']['abs'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['cf']['abs'][var_name] = nlp['levels']['cf']['abs'][var_name][::2]
    nlp['oom'       ]['cf']['abs'][var_name] = -3

    cmap = plt.cm.RdBu_r
    my_cmap = cmap(np.linspace(0.0, 1.00, cmap.N))
    #my_cmap[:,-1] = (np.linspace(-1.0, 1.0, cmap.N)**2)**(1/2)
    my_cmap = ListedColormap(my_cmap)
    nlp['cmaps']['cf']['diff'][var_name] = my_cmap
    if domain == 'Trades':
        range = 0.002
        delta = 0.0005
    elif domain == 'ITCZ':
        range = 0.006
        delta = 0.001
    elif domain == 'ITCZ_low':
        range = 0.25 # NS cs
    #nlp['levels']['cf']['diff'][var_name] = np.arange(-0.01*fact,0.01*fact,delta)+delta/2
    #nlp['cb_ticks']['cf']['diff'][var_name] = [-0.0055,-0.0035,-0.0015,0.0,0.0015,0.0035,0.0055]
    #nlp['levels']['cf']['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    #nlp['cb_ticks']['cf']['diff'][var_name] = nlp['levels']['cf']['diff'][var_name]

    range = 0.006
    delta = 0.001
    nlp['cmaps'     ]['cf']['bias'][var_name] = my_cmap
    nlp['levels'    ]['cf']['bias'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['cf']['bias'][var_name] = nlp['levels']['cf']['bias'][var_name][::2]
    nlp['oom'       ]['cf']['bias'][var_name] = -3


    nlp['cmaps']['cf']['bias'][var_name] = my_cmap
    if domain == 'Trades':
        fact = 0.2 # trades
    elif domain == 'ITCZ':
        fact = 0.6 # NS cs
    elif domain == 'ITCZ_low':
        fact = 1.0 # NS cs
    #nlp['levels']['cf']['bias'][var_name] = np.arange(-0.01*fact,0.01*fact*1.01,0.001)
    #nlp['cb_ticks']['cf']['bias'][var_name] = np.arange(-0.01*fact,0.01*fact*1.01,0.002)
    #nlp['levels']['cf']['bias'][var_name] = np.arange(-0.01*fact+0.0005,0.01*fact,0.001)
    #nlp['cb_ticks']['cf']['bias'][var_name] = [-0.0055,-0.0035,-0.0015,0.0,0.0015,0.0035,0.0055]
    #nlp['oom'     ]['cf']['bias'][var_name] = -2

    range = 0.006
    delta = 0.001
    nlp['cmaps'     ]['cf']['diff'][var_name] = my_cmap
    nlp['levels'    ]['cf']['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['cf']['diff'][var_name] = nlp['levels']['cf']['diff'][var_name][::2]
    nlp['oom'       ]['cf']['diff'][var_name] = -3



######### variable WFLX
##############################################################################
for var_name in ['WFLX']:
    cmap = plt.cm.PRGn_r
    cmap = plt.cm.PuOr_r
    cmap = plt.cm.PiYG_r
    my_cmap = cmap(np.linspace(0.0, 1.00, cmap.N))
    my_cmap = ListedColormap(my_cmap)
    ## heim et al 2023 JGR
    #range = 0.0044
    #delta = 0.0008
    range = 0.007
    delta = 0.001
    nlp['cmaps'     ]['cf']['abs'][var_name] = my_cmap
    nlp['levels'    ]['cf']['abs'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['cf']['abs'][var_name] = nlp['levels']['cf']['abs'][var_name][::2]
    nlp['oom'       ]['cf']['abs'][var_name] = -3

    cmap = plt.cm.RdBu_r
    my_cmap = cmap(np.linspace(0.0, 1.00, cmap.N))
    my_cmap = ListedColormap(my_cmap)
    ## heim et al 2023 JGR
    #range = 0.0024
    #delta = 0.0004
    range = 0.0032
    delta = 0.0004
    nlp['cmaps'     ]['cf']['diff'][var_name] = my_cmap
    nlp['levels'    ]['cf']['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks'  ]['cf']['diff'][var_name] = nlp['levels']['cf']['diff'][var_name][::2]
    nlp['oom'       ]['cf']['diff'][var_name] = -3


######### variable POTTDIV
##############################################################################
for var_name in [
        'POTTVDIV','POTTHDIV','DIABH','POTTDIV',
        'POTTDIV4',
        'POTTVDIVMEAN', 'POTTHDIVMEAN', 'POTTDIVMEAN', 
        'POTTVDIVTURB', 'POTTHDIVTURB', 'POTTDIVTURB', 
        'POTTVDIVMEANNORMI', 'POTTHDIVMEANNORMI', 'POTTDIVMEANNORMI', 
        'POTTVDIVTURBNORMI', 'POTTHDIVTURBNORMI', 'POTTDIVTURBNORMI', 
        'POTTVDIVNORMI', 'POTTHDIVNORMI', 'DIABHNORMI', 'POTTDIVNORMI',
        'CLDPOTTDIV','CSPOTTDIV','CLDPOTTDIVNORMI','CSPOTTDIVNORMI',
        'NCOLIPOTTDIV',
    ]:
    if domain in ['ITCZ']:
        range = 3.25
        delta = 0.5
    elif domain == 'Trades':
        range = 7
        delta = 1
    nlp['cmaps']['cf']['abs'][var_name] = cmap_symzero
    nlp['levels']['cf']['abs'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks']['cf']['abs'][var_name] = nlp['levels']['cf']['abs'][var_name][::2]
    if domain in ['ITCZ']:
        range = 2.0
        delta = 0.4
    elif domain == 'Trades':
        range = 0.7
        delta = 0.1
    nlp['cmaps']['cf']['diff'][var_name] = cmap_diff
    nlp['levels']['cf']['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks']['cf']['diff'][var_name] = nlp['levels']['cf']['diff'][var_name][::2]

    if domain in ['ITCZ']:
        range = 2.0
        delta = 0.4
    elif domain == 'Trades':
        range = 0.7
        delta = 0.1
    nlp['levels']['cf']['bias'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks']['cf']['bias'][var_name] = nlp['levels']['cf']['bias'][var_name][::2]


######### variable POTTDIV3
##############################################################################
for var_name in [
        'POTTVDIV3', 'POTTHDIV3', 'POTTDIV3',
        'CLDPOTTVDIV3', 'CLDPOTTHDIV3', 'CLDPOTTDIV3',
        'CSPOTTVDIV3','CSPOTTHDIV3','CSPOTTDIV3',
        'NCOLIPOTTDIV3',
        'POTTDIV3NORMI','CSPOTTDIV3NORMI','CLDPOTTDIV3NORMI',
        'EQPOTTDIV3', 'CLDEQPOTTDIV3', 'CSEQPOTTDIV3',
        'RH0GCSPOTTDIV3','RH1GCSPOTTDIV3','RH2GCSPOTTDIV3',
    ]:
    if domain in ['ITCZ', 'ITCZ_low']:
        range = 3
        delta = 0.5
        #if var_name in ['POTTDIV3','NCOLIPOTTDIV3',]:
        #    range = 3
        #    delta = 0.5
        #else:
        #    range = 5
        #    delta = 1
    elif domain == 'Trades':
        #range = 6
        #delta = 1
        range = 2
        delta = 0.4
    nlp['cmaps']['cf']['abs'][var_name] = cmap_symzero
    nlp['levels']['cf']['abs'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks']['cf']['abs'][var_name] = nlp['levels']['cf']['abs'][var_name] 
    if domain in ['ITCZ', 'ITCZ_low']:
        if var_name in ['POTTDIV3','NCOLIPOTTDIV3',]:
            range = 2
            delta = 0.4
        else:
            range = 4
            delta = 0.5
    elif domain == 'Trades':
        #range = 6
        #delta = 1
        range = 0.5
        delta = 0.1
    nlp['cmaps']['cf']['diff'][var_name] = cmap_diff
    nlp['levels']['cf']['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks']['cf']['diff'][var_name] = nlp['levels']['cf']['diff'][var_name] 

for var_name in [
        'RH0LCSPOTTDIV3', 'RH1LCSPOTTDIV3', 'RH2LCSPOTTDIV3',
    ]:
    range = 0.1
    if domain in ['ITCZ', 'ITCZ_low']:
        range = 30
        delta = 4
    nlp['cmaps']['cf']['abs'][var_name] = cmap_symzero
    nlp['levels']['cf']['abs'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks']['cf']['abs'][var_name] = nlp['levels']['cf']['abs'][var_name] 
    if domain in ['ITCZ', 'ITCZ_low']:
        range = 30
        delta = 4
    nlp['cmaps']['cf']['diff'][var_name] = cmap_diff
    nlp['levels']['cf']['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks']['cf']['diff'][var_name] = nlp['levels']['cf']['diff'][var_name] 


for var_name in [
        'QIDIV3',
    ]:
    if domain in ['ITCZ', 'ITCZ_low']:
        range = 0.02
        delta = 0.002
    nlp['cmaps']['cf']['abs'][var_name] = cmap_symzero
    nlp['levels']['cf']['abs'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks']['cf']['abs'][var_name] = nlp['levels']['cf']['abs'][var_name] 
    if domain in ['ITCZ', 'ITCZ_low']:
        range = 0.01
        delta = 0.002
    nlp['cmaps']['cf']['diff'][var_name] = cmap_diff
    nlp['levels']['cf']['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks']['cf']['diff'][var_name] = nlp['levels']['cf']['diff'][var_name] 


######### variable QVDIV
##############################################################################
for var_name in [
        'QVVDIV', 'QVHDIV', 'QVDIV', 'DIABM',
        'QVVDIVMEAN', 'QVHDIVMEAN', 'QVDIVMEAN', 
        'QVVDIVTURB', 'QVHDIVTURB', 'QVDIVTURB',
        'QVVDIVMEANNORMI', 'QVHDIVMEANNORMI', 'QVDIVMEANNORMI', 
        'QVVDIVTURBNORMI', 'QVHDIVTURBNORMI', 'QVDIVTURBNORMI', 
        'QVVDIVNORMI', 'QVHDIVNORMI', 'QVDIVNORMI', 'DIABMNORMI',
        'CLDQVHDIVTURB', 'CLDQVHDIVTURBNORMI',
        'CLDQVVDIVTURB', 'CLDQVVDIVTURBNORMI',
        'CSQVHDIVTURB', 'CSQVHDIVTURBNORMI',
        'CSQVVDIVTURB', 'CSQVVDIVTURBNORMI',

        'QVVDIV3', 'QVHDIV3', 'QVDIV3', 'DIABM',
        'QVVDIV3MEAN', 'QVHDIV3MEAN', 'QVDIV3MEAN', 
        'QVVDIV3TURB', 'QVHDIV3TURB', 'QVDIV3TURB',
        'QVVDIV3MEANNORMI', 'QVHDIV3MEANNORMI', 'QVDIV3MEANNORMI', 
        'QVVDIV3TURBNORMI', 'QVHDIV3TURBNORMI', 'QVDIV3TURBNORMI', 
        'QVVDIV3NORMI', 'QVHDIV3NORMI', 'QVDIV3NORMI', 'DIABMNORMI',
        'CLDQVHDIV3TURB', 'CLDQVHDIV3TURBNORMI',
        'CLDQVVDIV3TURB', 'CLDQVVDIV3TURBNORMI',
        'CLDQVDIV3TURB', 'CLDQVDIV3TURBNORMI',
        'CSQVHDIV3TURB', 'CSQVHDIV3TURBNORMI',
        'CSQVVDIV3TURB', 'CSQVVDIV3TURBNORMI',
        'CSQVDIV3TURB', 'CSQVDIV3TURBNORMI',
    ]:
    cmap = plt.cm.RdBu_r
    my_cmap = cmap(np.linspace(0.0, 1.00, cmap.N))
    #my_cmap[:,-1] = (np.linspace(-1.0, 1.0, cmap.N)**2)**(1/2)
    my_cmap = ListedColormap(my_cmap)
    if domain in ['ITCZ', 'ITCZ_low']:
        fact = 1 # ITCZ
    elif domain == 'Trades':
        fact = 1.5 # Trades, Trades norm inv
    else: raise NotImplementedError()
    nlp['cmaps']['cf']['abs'][var_name] = cmap_symzero
    nlp['levels']['cf']['abs'][var_name] = np.arange(-0.1*fact+0.01,0.1*fact,0.02)
    nlp['cb_ticks']['cf']['abs'][var_name] = np.arange(-0.1*fact+0.01,0.1*fact,0.02) 
    if domain in ['ITCZ', 'ITCZ_low']:
        fact = 1.5 # ITCZ
    elif domain == 'Trades':
        fact = 1.5 # Trades, Trades norm inv
    else: raise NotImplementedError()
    nlp['cmaps']['cf']['diff'][var_name] = cmap_diff
    nlp['levels']['cf']['diff'][var_name] = np.arange(-0.02*fact+0.0025,0.02*fact,0.005)
    nlp['cb_ticks']['cf']['diff'][var_name] = np.arange(-0.02*fact+0.0025,0.02*fact,0.005) 

    nlp['cmaps']['cf']['rel'][var_name] = cmap_diff
    nlp['levels']['cf']['rel'][var_name] = np.arange(-1000,1000*1.01,100)
    nlp['cb_ticks']['cf']['rel'][var_name] = np.arange(-1000,1000*1.01,100)


for var_name in [
        'QCDIV', 'QCDIVNORMI',
    ]:
    cmap = plt.cm.RdBu_r
    my_cmap = cmap(np.linspace(0.0, 1.00, cmap.N))
    #my_cmap[:,-1] = (np.linspace(-1.0, 1.0, cmap.N)**2)**(1/2)
    my_cmap = ListedColormap(my_cmap)
    if domain in ['ITCZ', 'ITCZ_low']:
        fact = 1 # ITCZ
    elif domain == 'Trades':
        fact = 1.5 # Trades, Trades norm inv
    else: raise NotImplementedError()
    nlp['cmaps']['cf']['abs'][var_name] = my_cmap
    nlp['levels']['cf']['abs'][var_name] = np.arange(-0.05*fact,0.05*fact*1.01,0.005)
    nlp['cb_ticks']['cf']['abs'][var_name] = np.arange(-0.05*fact,0.05*fact*1.01,0.05) 
    nlp['cmaps']['cf']['diff'][var_name] = my_cmap
    nlp['levels']['cf']['diff'][var_name] = np.arange(-0.01*fact,0.01*fact*1.01,0.002)
    nlp['cb_ticks']['cf']['diff'][var_name] = np.arange(-0.01*fact,0.01*fact*1.01,0.02) 


######### variable BVF
##############################################################################
for var_name in ['BVF', 'BVFNORMI']:
    if domain in ['Trades']:
        min = -6E-5
        max = 3E-4
        delta = 3E-5
    elif domain == 'ITCZ':
        #min = -6E-5
        #max = 3E-4
        #delta = 2E-5
        min = -6E-5
        max = 3E-4
        delta = 2E-5
    cmap = plt.cm.rainbow
    my_cmap = cmap(np.linspace(0.0, 1.00, cmap.N))
    my_cmap = ListedColormap(my_cmap)
    nlp['cmaps']['cf']['abs'][var_name] = my_cmap
    nlp['levels']['cf']['abs'][var_name] = np.arange(min+delta/2,max,delta)
    nlp['cb_ticks']['cf']['abs'][var_name] = nlp['levels']['cf']['abs'][var_name][::2]

    nlp['cmaps']['cf']['diff'][var_name] = 'RdBu_r'
    if domain in ['Trades']:
        #range = 5E-5
        #delta = 1E-5
        #nlp['levels']['cf']['diff'][var_name] = np.arange(-range+delta/2,range,delta)
        min = 0
        max = 5.5E-5
        delta = 5E-6
        nlp['levels']['cf']['diff'][var_name] = np.arange(min+delta/2,max,delta)
        nlp['cmaps']['cf']['diff'][var_name] = cmap_RdBu_r_positive
    elif domain == 'ITCZ':
        range = 5E-5
        delta = 1E-5
        nlp['levels']['cf']['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    else: raise NotImplementedError()
    nlp['cb_ticks']['cf']['diff'][var_name] = nlp['levels']['cf']['diff'][var_name]


######### variable UVDIV
##############################################################################
for var_name in ['UVDIV', 'UVDIVNORM', 'CSUVDIV','CLDUVDIV']:
    cmap = plt.cm.RdBu_r
    my_cmap = cmap(np.linspace(0.0, 1.00, cmap.N))
    my_cmap = ListedColormap(my_cmap)
    range = 1E-5
    delta = 2E-6
    nlp['cmaps']['cf']['abs'][var_name] = my_cmap
    nlp['levels']['cf']['abs'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks']['cf']['abs'][var_name] = nlp['levels']['cf']['abs'][var_name]

    range = 5E-6
    delta = 1E-6
    nlp['cmaps']['cf']['diff'][var_name] = my_cmap
    nlp['levels']['cf']['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks']['cf']['diff'][var_name] = nlp['levels']['cf']['diff'][var_name]

#for var_name in ['CLDUVDIV']:
#    cmap = plt.cm.RdBu_r
#    my_cmap = cmap(np.linspace(0.0, 1.00, cmap.N))
#    my_cmap = ListedColormap(my_cmap)
#    base_val = 1E-6
#    abs_fact = 5*6
#    diff_fact = 2*6
#    nlp['cmaps']['cf']['abs'][var_name] = my_cmap
#    nlp['levels']['cf']['abs'][var_name] = np.arange(-base_val*abs_fact,base_val*abs_fact*1.01,base_val/10)
#    nlp['cb_ticks']['cf']['abs'][var_name] = np.arange(-base_val*abs_fact,base_val*abs_fact*1.01,base_val*6) 
#
#    nlp['cmaps']['cf']['diff'][var_name] = my_cmap
#    nlp['levels']['cf']['diff'][var_name] = np.arange(-base_val*diff_fact,base_val*diff_fact*1.01,base_val/20)
#    nlp['cb_ticks']['cf']['diff'][var_name] = np.arange(-base_val*diff_fact,base_val*diff_fact*1.01,base_val/2*6) 


######### variable TKE
##############################################################################
for var_name in ['TKE', 'TKENORMI']:
    cmap = plt.cm.plasma
    my_cmap = cmap(np.linspace(0.0, 1.00, cmap.N))
    my_cmap = ListedColormap(my_cmap)
    base_val = 20
    fact = 1 # Trades norm inv
    nlp['cmaps']['cf']['abs'][var_name] = my_cmap
    nlp['levels']['cf']['abs'][var_name] = np.arange(0,base_val*fact*1.01,5E-1)
    nlp['cb_ticks']['cf']['abs'][var_name] = np.arange(0,base_val*fact*1.01,5) 
    fact = 0.1 # Trades norm inv
    nlp['cmaps']['cf']['diff'][var_name] = 'RdBu_r'
    nlp['levels']['cf']['diff'][var_name] = np.arange(-base_val*fact,base_val*fact*1.01,1E-1)
    nlp['cb_ticks']['cf']['diff'][var_name] = np.arange(-base_val*fact,base_val*fact*1.01,1) 


######### variable BUOYIFLX
##############################################################################
for var_name in ['BUOYIFLX', 'BUOYIFLXNORMI']:
    #if domain in ['ITCZ']:
    range = 0.0005
    delta = 0.0001
    nlp['cmaps']['cf']['abs'][var_name] = cmap_symzero
    nlp['levels']['cf']['abs'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks']['cf']['abs'][var_name] = nlp['levels']['cf']['abs'][var_name] 
    #if domain in ['ITCZ']:
    range = 0.00005
    delta = 0.00001
    nlp['cmaps']['cf']['diff'][var_name] = cmap_diff
    nlp['levels']['cf']['diff'][var_name] = np.arange(-range+delta/2,range,delta)
    nlp['cb_ticks']['cf']['diff'][var_name] = nlp['levels']['cf']['diff'][var_name] 


# default: copy everything from diff to bias
for var_name,val in nlp['cmaps']['cf']['diff'].items():
    if var_name not in nlp['cmaps']['cf']['bias']:
        nlp['cmaps']['cf']['bias'][var_name] = val
for var_name,val in nlp['levels']['cf']['diff'].items():
    if var_name not in nlp['levels']['cf']['bias']:
        nlp['levels']['cf']['bias'][var_name] = val
for var_name,val in nlp['oom']['cf']['diff'].items():
    if var_name not in nlp['oom']['cf']['bias']:
        nlp['oom']['cf']['bias'][var_name] = val
for var_name,val in nlp['cb_ticks']['cf']['diff'].items():
    if var_name not in nlp['cb_ticks']['cf']['bias']:
        nlp['cb_ticks']['cf']['bias'][var_name] = val

for var_name,val in nlp['levels']['cl']['diff'].items():
    if var_name not in nlp['levels']['cl']['bias']:
        nlp['levels']['cl']['bias'][var_name] = val
