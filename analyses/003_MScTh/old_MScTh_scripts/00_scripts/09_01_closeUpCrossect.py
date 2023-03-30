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
from ncClasses.subdomains import setSSI
####################### NAMELIST INPUTS FILES #######################
# directory of input model folders
inpPath = '../02_fields/diurnal'
#inpPath = '../02_fields/topocut'

others = ['cHSURF', 'nTOT_PREC', 'nHPBL']
hydrometeors = ['zQC', 'zQI', 'zQV', 'zQR', 'zQS', 'zQG']
TTendencies = ['zATT_MIC', 'zATT_RAD', 'zATT_ADV', 'zATT_ZADV', 'zATT_TURB', 'zATT_TOT']
QVTendencies = ['zAQVT_MIC', 'zAQVT_ADV', 'zAQVT_ZADV', 'zAQVT_TURB', 'zAQVT_TOT']
dynamics = ['zW', 'zU', 'zV', 'zT', 'zP']
#fieldNames = ['zAQVT_ZADV', 'cHSURF']
#fieldNames = ['zU', 'cHSURF']
#####################################################################		

diurnals = list(range(8,24))
diurnals.extend(list(range(0,8)))
#diurnals = [15]
plotVarName = 'zAQVT_MIC'
plotVarName = 'zFQVy'
plotVarName = 'zQV'
#plotVarName = 'zT'
cmapM = 'seismic' 

fieldNames = [plotVarName, 'cHSURF', 'zQC']
if plotVarName == 'zU':
    ticks = list(np.arange(-10,11,1)) # U
    cmapM = 'seismic'
elif plotVarName == 'zV':
    ticks = list(np.arange(-7,8,1)) # U
    cmapM = 'seismic'
#elif plotVarName == 'zQV':
#    ticks = list(np.arange(0,15,1)) # U
#    cmapM = 'jet'
elif plotVarName == 'zW':
    ticks = list(np.arange(-2.5,2.5,0.30)) # U
    cmapM = 'seismic'
elif plotVarName == 'zRH':
    ticks = list(np.arange(10,110,5)) # U
    cmapM = 'jet'
elif plotVarName == 'zT':
    ticks = list(np.arange(250,309,3)) # U
    cmapM = 'jet'
elif plotVarName == 'zAQVT_HADV':
    ticks = list(np.arange(-0.5,0.6,0.1)) # U
    cmapM = 'seismic'
elif plotVarName == 'zFQVy':
    ticks = list(np.arange(-7.5,7.5,0.50))
    cmapM = 'seismic'
elif 'AQVT' in plotVarName:
    #ticks = list(np.arange(-10,11,1)) # U
    ticks = list(np.arange(-0.3,0.3,0.03)) # U
    cmapM = 'seismic'
else:
    ticks = None # autoticks
####################### NAMELIST DIMENSIONS #######################
i_subDomain = 4 # 0: full domain, 1: alpine region
ssI, domainName = setSSI(i_subDomain, {'4.4':{}, '2.2':{}, '1.1':{}}) 
startHght = 0
endHght = 40
altInds = list(range(startHght,endHght+1))
ssI['altitude'] = altInds 
#startTime = datetime(2006,7,12,8)
#endTime = datetime(2006,7,12,9)
#ssI['time'] = [startTime] # border values (one value if only one time step desired)
for i in range(0,len(diurnals)):
    diurn = diurnals[i]
    print(diurn)
    ssI['diurnal'] = [diurn] # list values

    ####################### NAMELIST AGGREGATE #######################
    # Options: MEAN, SUM 
    ag_commnds = {}
    #ag_commnds['rlat'] = 'MEAN'
    ag_commnds['rlon'] = 'SUM'
    #ag_commnds['time'] = 'MEAN'
    #ag_commnds['diurnal'] = 'MEAN'
    #ag_commnds['altitude'] = 'MEAN'
    #####################################################################

    ####################### NAMELIST PLOT #######################
    nDPlot = 2 # How many dimensions should plot have (1 or 2)
    i_diffPlot = 1 # Draw plot showing difference filtered - unfiltered # TODO
    #plotOutDir = '../00_plots/09_closeUp'
    plotOutDir = '../00_plots/11_yz_crossSect'
    plotName = plotVarName+'_'+str(i)+'_hr_'+str(diurn)+'.png' 
    ##### 1D PLOT #########

    ##### 2D Contour ######
    contourTranspose = 0 # Reverse contour dimensions?
    plotContour = 0 # Besides the filled contour, also plot the contour?
    axis = 'auto' # set 'equal' if keep aspect ratio, else 'auto'
    # COLORBAR Models
    if ticks is not None:
        autoTicks = 0
    else:
        autoTicks = 1
    Mticks = ticks
    Mmask = 0 # Mask Model values lower than MThrMinRel of maximum value?
    MThrMinRel = 0.02 # Relative amount of max value to mask (see Mmask)
    # COLORBAR Models
    cmapD = 'bwr' # colormap for Difference output (bwr)
    #####################################################################


    an = analysis.analysis(inpPath, fieldNames)

    #an.subSpaceInds = subSpaceInds
    an.subSpaceInds = ssI
    an.ag_commnds = ag_commnds
    an.i_info = i_info
    an.i_resolutions = i_resolutions

    # RUN ANALYSIS
    an.run()

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
        
            #if 'cHSURF' in an.varNames:
            #    ncs.plotTopo(an.vars['cHSURF'])
            
            ncs.plotVar(an.vars[an.varNames[0]])

            #ncs.addContour(an.vars['zQC'], 'white', 0.8, 1.5, ticks=[0.1])
            #ncs.addContour(an.vars['zQC'], 'white', 0.8, 1.5, ticks=[0.01])
            ncs.addContour(an.vars['zQC'], 'white', 0.8, 1.5, ticks=[1])
                
            title = plotVarName+'_hr_'+str(diurn) 
            ncs.fig.suptitle(title, fontsize=14)

        else:
            raise ValueError('ERROR: CANNOT MAKE ' + str(nDPlot) + 'D-PLOT WITH ' +
            str(someField.nNoneSingleton) + ' NON-SINGLETON DIMS!')

        
        if i_plot == 1:
            plt.show()
        elif i_plot == 2:
            plotPath = plotOutDir + '/' + plotName
            plt.savefig(plotPath, format='png', bbox_inches='tight')
            plt.close('all')

              


