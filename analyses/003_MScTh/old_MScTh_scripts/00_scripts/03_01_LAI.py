#################################
# Calculate domain Average Precipitation
# author: Christoph Heim
# date: 21 10 2017
#################################
import os
os.chdir('00_scripts/')

i_resolutions = 3 # 1 = 4.4, 2 = 4.4 + 2.2, 3 = ...
i_plot = 2 # 0 = no plot, 1 = show plot, 2 = save plot
i_info = 5 # output some information [from 0 (off) to 5 (all you can read)]
import matplotlib
if i_plot == 2:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt


import ncClasses.analysis as analysis
from datetime import datetime
from functions import *
####################### NAMELIST INPUTS FILES #######################
# directory of input model folders
inpPath = '../02_fields/result'
fieldNames = ['cLAI']
#####################################################################		

####################### NAMELIST DIMENSIONS #######################
subDomain = 0 # 0: full domain, 1: alpine region, 2: zoom in
# SUBSPACE
subSpaceIndsIN = {}
if subDomain == 1: # alpine region
    subSpaceIndsIN['rlon'] = (50,237)
    subSpaceIndsIN['rlat'] = (41,155)
elif subDomain == 2: # zoom in subdomain
    subSpaceIndsIN['rlon'] = (70,100)
    subSpaceIndsIN['rlat'] = (70,100)

#####################################################################

####################### NAMELIST AGGREGATE #######################
# Options: MEAN, SUM 
ag_commnds = {}
#ag_commnds['rlat'] = 'MEAN'
#ag_commnds['rlon'] = 'MEAN'
#ag_commnds['time'] = 'MEAN'
#ag_commnds['diurnal'] = 'MEAN'
#ag_commnds['altitude'] = 'MEAN'
#####################################################################

####################### NAMELIST PLOT #######################
nDPlot = 2 # How many dimensions should plot have (1 or 2)
i_diffPlot = 0 # Draw plot showing difference filtered - unfiltered # TODO
plotOutDir = '../00_plots'
plotName = 'lai.pdf'
##### 1D PLOT #########

##### 2D Contour ######
contourTranspose = 0 # Reverse contour dimensions?
plotContour = 0 # Besides the filled contour, also plot the contour?
cmapM = 'jet' # colormap for Model output (jet, terrain, inferno, YlOrRd)
axis = 'equal' # set 'equal' if keep aspect ratio, else 'auto'
# COLORBAR Models
autoTicks = 1 # 1 if colorbar should be set automatically
Mmask = 0 # Mask Model values lower than MThrMinRel of maximum value?
MThrMinRel = 0.15 # Relative amount of max value to mask (see Mmask)
Mticks = [0.0001,0.0002,0.0003,0.0004,0.0005]
Mticks = list(np.arange(0.0002,0.0022,0.0002))
# COLORBAR Models
cmapD = 'bwr' # colormap for Difference output (bwr)
#####################################################################


an = analysis.analysis(inpPath, fieldNames)

an.subSpaceIndsIN = subSpaceIndsIN
an.ag_commnds = ag_commnds
an.i_info = i_info
an.i_resolutions = i_resolutions

# RUN ANALYSIS
an.run()


import matplotlib
if i_plot == 2:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt



if i_plot > 0:
    if i_info >= 3:
        print('plotting')
    mainVar = an.vars[an.fieldNames[0]]
    someField = mainVar.modelRes['4.4'].ncos['U'].curFld
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
    
        if 'cHSURF' in an.fieldNames:
            ncs.plotTopo(an.vars['cHSURF'])
        
        if 'cHSURF' in an.fieldNames:
            ncs.plotVar(an.vars[an.fieldNames[1]])
        else:
            ncs.plotVar(an.vars[an.fieldNames[0]])
            
        title = 'title' 
        ncs.fig.suptitle(title, fontsize=14)

    elif nDPlot == 1 and someField.nNoneSingleton == 1:
        import ncPlots.ncSubplots1D as ncSubplots
        ncs = ncSubplots.ncSubplots(an, nDPlot, i_diffPlot, 'HOR')
    
        for fldName in an.fieldNames:
            if fldName != 'cHSURF':
                ncs.plotVar(an.vars[fldName])

        title = 'title' 
        ncs.fig.suptitle(title, fontsize=14)

    else:
        raise ValueError('ERROR: CANNOT MAKE ' + str(nDPlot) + 'D-PLOT WITH ' +
        str(someField.nNoneSingleton) + ' NON-SINGLETON DIMS!')

    
    if i_plot == 1:
        plt.show()
    elif i_plot == 2:
        plotPath = plotOutDir + '/' + plotName
        #plt.savefig(plotPath, format='png', bbox_inches='tight')
        plt.savefig(plotPath, format='pdf', bbox_inches='tight')

          


