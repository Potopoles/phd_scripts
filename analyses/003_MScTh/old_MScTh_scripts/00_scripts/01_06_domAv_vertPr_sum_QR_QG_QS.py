#################################
# Calculate domain Average Precipitation
# author: Christoph Heim
# date: 21 10 2017
#################################
import os
os.chdir('00_scripts/')

i_resolutions = 3 # 1 = 4.4, 2 = 4.4 + 2.2, 3 = ...
i_plot = 3 # 0 = no plot, 1 = show plot, 2 = save plot
i_info = 2 # output some information [from 0 (off) to 5 (all you can read)]
import matplotlib
if i_plot > 1:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt


import ncClasses.analysis as analysis
from datetime import datetime
from functions import *
from ncClasses.subdomains import setSSI
####################### NAMELIST INPUTS FILES #######################
# directory of input model folders
inpPath = '../02_fields/diurnal'
fieldNames = ['zQR', 'zQG', 'zQS', 'zPW']

####################### NAMELIST DIMENSIONS #######################
i_subDomain = 1 # 0: full domain, 1: alpine region
ssI, domainName = setSSI(i_subDomain, {'4.4':{}, '2.2':{}, '1.1':{}}) 
#ssI['diurnal'] = list(range(10,20)) 
#ssI['altitude'] = list(range(25,65)) 
# DOMAINS ASSUMING Alpine Region FROM subDomDiur FILES IS REFERENCE!
if i_subDomain == 1: # Alpine Region
    CF_Ticks = list(np.arange(0.001,0.066,0.002))
    C_SumTicks = [0.001, 0.005, 0.01, 0.02, 0.03]
    C_AQVT_MIC_Ticks = [-0.08,-0.04,-0.02,0.02,0.04,0.08]
#if subDomain == 3: # Northern Italy Plains (04_00 DOMAIN 3)
#    subSpaceIndsIN['rlon'] = [48,100]
#    subSpaceIndsIN['rlat'] = [25,56]
#    CF_Ticks = list(np.arange(0.001,0.23,0.02))
#    C_SumTicks = [0.001, 0.005, 0.01, 0.05, 0.1]
#    C_AQVT_MIC_Ticks = [-0.1,-0.05,-0.01,0.01,0.05,0.1]
#####################################################################

####################### NAMELIST AGGREGATE #######################
# Options: MEAN, SUM, DIURNAL
ag_commnds = {}
ag_commnds['rlat'] = 'MEAN'
ag_commnds['rlon'] = 'MEAN'
#####################################################################

####################### NAMELIST PLOT #######################
nDPlot = 2 # How many dimensions should plot have (1 or 2)
i_diffPlot = 0 # Draw plot showing difference filtered - unfiltered # TODO
plotOutDir = '../00_plots/01_domAv_Fields/domain_'+str(domainName)
import os
if not os.path.exists(plotOutDir):
    os.makedirs(plotOutDir)
plotName = 'dA_diurn_sum_QR_QG_QS_dom_'+str(domainName)
##### 1D PLOT #########

##### 2D Contour ######
contourTranspose = 0 # Reverse contour dimensions?
plotContour = 0 # Besides the filled contour, also plot the contour?
cmapM = 'YlGn' # colormap for Model output (jet, terrain, inferno, YlOrRd)
axis = 'auto' # set 'equal' if keep aspect ratio, else 'auto'
# COLORBAR Models
autoTicks = 0 # 1 if colorbar should be set automatically
Mmask = 1 # Mask Model values lower than MThrMinRel of maximum value?
MThrMinRel = 0.15 # Relative amount of max value to mask (see Mmask)
Mticks = CF_Ticks 
# COLORBAR Models
cmapD = 'bwr' # colormap for Difference output (bwr)
#####################################################################


an = analysis.analysis(inpPath, fieldNames)

an.subSpaceInds = ssI
an.ag_commnds = ag_commnds
an.i_info = i_info
an.i_resolutions = i_resolutions

# RUN ANALYSIS
an.run()


#quit()

import matplotlib
if i_plot == 2:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

import math


if i_info >= 3:
    print('plotting')
mainVar = an.vars[an.varNames[0]]
someField = next(iter(mainVar.ncos.values())).field
if i_info >= 1:
    print('NONSINGLETONS: ' + str(someField.nNoneSingleton))

if nDPlot == 2 and someField.nNoneSingleton == 2:
    import ncPlots.ncSubplots2D as ncSubplots
    ncs = ncSubplots.ncSubplots(an, nDPlot, i_diffPlot, 'HOR')

    ncs.contourTranspose = contourTranspose
    ncs.plotContour = plotContour
    ncs.cmapM = cmapM
    ncs.axis = axis
    ncs.autoTicks = autoTicks
    ncs.Mmask = Mmask
    ncs.MThrMinRel = MThrMinRel
    ncs.Mticks = Mticks
    ncs.cmapD = cmapD

    fig, axes, MCB = ncs.plotVar(an.vars['zPW'])
    ncs.Mticks = C_SumTicks 
    QR = ncs.addContour(an.vars['zQR'], 'black', 1, lineWidth=1.5) 
    QG = ncs.addContour(an.vars['zQG'], 'red', 1, lineWidth=1.5)
    QS = ncs.addContour(an.vars['zQS'], 'blue', 1, lineWidth=1.5)
    #ncs.Mticks = C_AQVT_MIC_Ticks
    #MIC = ncs.addContour(an.vars['zAQVT_MIC'], 'blue', 1, lineWidth=1)
    
    ax1 = axes[0,0]
    
    #lines = [QR.collections[0], QG.collections[0], QS.collections[0], MIC.collections[0]]
    lines = [QR.collections[0], QG.collections[0], QS.collections[0]]
    #labels = ['QR', 'QG', 'QS', 'MIC']
    labels = ['$q_{r}$', '$q_{g}$', '$q_{s}$']
    ax1.legend(lines, labels, loc=2)

    #title = 'dA diurn (QR + QG + QS)' 
    #ncs.fig.suptitle(title, fontsize=14)
    MCB.set_label(r'Precipitable Water $[g$ $kg^{-1}]$', fontsize=13*ncs.MAG)
             
elif nDPlot == 1 and someField.nNoneSingleton == 1:
    pass
else:
    raise ValueError('ERROR: CANNOT MAKE ' + str(nDPlot) + 'D-PLOT WITH ' +
    str(someField.nNoneSingleton) + ' NON-SINGLETON DIMS!')


if i_plot == 1:
    plt.show()
elif i_plot == 2:
    plotPath = plotOutDir + '/' + plotName+'.png'
    plt.savefig(plotPath, format='png', bbox_inches='tight')
elif i_plot == 3:
    plotPath = plotOutDir + '/' + plotName+'.pdf'
    plt.savefig(plotPath, format='pdf', bbox_inches='tight')
    plt.close('all')
          


