#################################
# Calculate domain Average Precipitation
# author: Christoph Heim
# date: 21 10 2017
#################################
import os
os.chdir('00_scripts/')

i_resolutions = 3 # 1 = 4.4, 2 = 4.4 + 2.2, 3 = ...
i_plot = 2 # 0 = no plot, 1 = show plot, 2 = save plot
i_info = 0 # output some information [from 0 (off) to 5 (all you can read)]
import matplotlib
if i_plot == 2:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt


import ncClasses.analysis as analysis
from datetime import datetime
from functions import *
####################### NAMELIST INPUTS FILES #######################
# directory of input model folders
inpPath = '../02_fields/topocut'
inpPath = '../02_fields/diurnal'

others = ['cHSURF', 'nTOT_PREC', 'nHPBL']
hydrometeors = ['zQC', 'zQI', 'zQV', 'zQR', 'zQS', 'zQG']
TTendencies = ['zATT_MIC', 'zATT_RAD', 'zATT_ADV', 'zATT_ZADV', 'zATT_TURB', 'zATT_TOT']
QVTendencies = ['zAQVT_MIC', 'zAQVT_ADV', 'zAQVT_ZADV', 'zAQVT_TURB', 'zAQVT_TOT']
LWP = ['zALL', 'zHYD', 'zIWP', 'zLWP', 'zWVP']
clouds = ['zCB', 'zCT', 'zMF', 'zWM']
dynamics = ['zW', 'zU', 'zV', 'zT', 'zP']
fieldNames = ['zALL', 'cHSURF']
fieldNames = ['zHYD']
#####################################################################		

fieldNameGroup = clouds

for fieldNames in fieldNameGroup:
    print(fieldNames)
    fieldNames = [fieldNames]
    #fieldNames = ['zALL']
    fieldNames.append('cHSURF')

    ####################### NAMELIST DIMENSIONS #######################
    subDomain = 1 # 0: full domain, 1: alpine region
    # SUBSPACE
    subSpaceInds = {}
    if subDomain == 1: # alpine region
        subSpaceInds['rlon'] = [50,237]
        subSpaceInds['rlat'] = [41,155]
    if subDomain == 2: # small Debug domain
        subSpaceInds['rlon'] = [60,90]
        subSpaceInds['rlat'] = [70,90]

    #startTime = datetime(2006,7,12,00)
    #endTime = datetime(2006,7,19,23)
    #subSpaceInds['time'] = [startTime,endTime] # border values
    #subSpaceInds['diurnal'] = [10] # list values
    #subSpaceInds['diurnal'] = list(range(0,24)) 
    #startHght = 20
    #endHght = 50
    #subSpaceInds['altitude'] = list(range(startHght,endHght+1))
    #####################################################################

    ####################### NAMELIST AGGREGATE #######################
    # Options: MEAN, SUM 
    ag_commnds = {}
    #ag_commnds['rlat'] = 'MEAN'
    #ag_commnds['rlon'] = 'MEAN'
    #ag_commnds['time'] = 'MEAN'
    ag_commnds['diurnal'] = 'MEAN'
    #ag_commnds['altitude'] = 'MEAN'
    #####################################################################

    ####################### NAMELIST PLOT #######################
    nDPlot = 2 # How many dimensions should plot have (1 or 2)
    i_diffPlot = 1 # Draw plot showing difference filtered - unfiltered # TODO
    plotOutDir = '../00_plots/07_lwp'
    plotName = 'diurnal_'+fieldNames[0][1:]+'.png'
    plotName = fieldNames[0][1:]+'_2D_tA.png'
    #plotName = fieldNames[0][1:]+'_1D_dA.png'
    ##### 1D PLOT #########

    ##### 2D Contour ######
    contourTranspose = 0 # Reverse contour dimensions?
    plotContour = 0 # Besides the filled contour, also plot the contour?
    cmapM = 'jet' # colormap for Model output (jet, terrain, inferno, YlOrRd)
    axis = 'auto' # set 'equal' if keep aspect ratio, else 'auto'
    # COLORBAR Models
    autoTicks = 1 # 1 if colorbar should be set automatically
    Mmask = 0 # Mask Model values lower than MThrMinRel of maximum value?
    MThrMinRel = 0.15 # Relative amount of max value to mask (see Mmask)
    Mticks = list(np.arange(2000,6500,500)) # cloud base
    #Mticks = list(np.arange(4000,10500,500)) # cloud top
    # COLORBAR Models
    cmapD = 'bwr' # colormap for Difference output (bwr)
    #####################################################################


    an = analysis.analysis(inpPath, fieldNames)

    an.subSpaceInds = subSpaceInds
    an.ag_commnds = ag_commnds
    an.i_info = i_info
    an.i_resolutions = i_resolutions

    # RUN ANALYSIS
    an.run()


    import matplotlib
    if i_plot == 2:
        matplotlib.use('Agg')
    import matplotlib.pyplot as plt


    #quit()

    if i_plot > 0:
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
        
            if 'cHSURF' in an.varNames:
                ncs.plotTopo(an.vars['cHSURF'])
            
            ncs.plotVar(an.vars[an.varNames[0]])
                
            title = fieldNames[0][1:]
            ncs.fig.suptitle(title, fontsize=14)

        elif nDPlot == 1 and someField.nNoneSingleton == 1:
            import ncPlots.ncSubplots1D as ncSubplots
            ncs = ncSubplots.ncSubplots(an, nDPlot, i_diffPlot, 'HOR')
        
            for varName in an.varNames:
                if varName != 'cHSURF':
                    ncs.plotVar(an.vars[varName])

            title = fieldNames[0][1:]
            ncs.fig.suptitle(title, fontsize=14)

        else:
            raise ValueError('ERROR: CANNOT MAKE ' + str(nDPlot) + 'D-PLOT WITH ' +
            str(someField.nNoneSingleton) + ' NON-SINGLETON DIMS!')

        
        if i_plot == 1:
            plt.show()
        elif i_plot == 2:
            plotPath = plotOutDir + '/' + plotName
            plt.savefig(plotPath, format='png', bbox_inches='tight')

              


