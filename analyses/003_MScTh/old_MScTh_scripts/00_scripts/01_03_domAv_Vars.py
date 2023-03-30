#################################
# Calculate domain Average Precipitation
# author: Christoph Heim
# date: 21 10 2017
#################################
import os
os.chdir('00_scripts/')

i_resolutions = 1 # 1 = 4.4, 2 = 4.4 + 2.2, 3 = ...
i_plot = 1 # 0 = no plot, 1 = show plot, 2 = save plot
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
inpPath = '../02_fields/subDomDiur'
others = ['cHSURF', 'nTOT_PREC']
hydrometeors = ['zQC', 'zQI', 'zQV', 'zQR', 'zQS', 'zQG']
TTendencies = ['zATT_MIC', 'zATT_RAD', 'zATT_ADV', 'zATT_ZADV', 'zATT_TURB', 'zATT_TOT']
QVTendencies = ['zAQVT_MIC', 'zAQVT_ADV', 'zAQVT_ZADV', 'zAQVT_TURB', 'zAQVT_TOT']
dynamics = ['zW', 'zU', 'zV', 'zT', 'zP']

fieldNames = ['zAQVT_MIC']
#fieldNames = QVTendencies

altInds = [40,50,60,61,62,63,64]
altInds = [63]

for fieldName in fieldNames:
    print('#######################')
    print(fieldName)
    #####################################################################		

    for altInd in altInds:
        if altInd <= 60:
            altitude = altInd*100
        else:
            altitude = 6000 + (altInd - 60)*1000
        print(altitude)
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

        #startTime = datetime(2006,7,11,0)
        #endTime = datetime(2006,7,12,0)
        #endTime = datetime(2006,7,20,0)
        #subSpaceIndsIN['time'] = (startTime,endTime)
        subSpaceIndsIN['altitude'] = [altInd]
        #####################################################################

        ####################### NAMELIST AGGREGATE #######################
        # Options: MEAN, SUM, DIURNAL
        ag_commnds = {}
        ag_commnds['rlat'] = 'MEAN'
        ag_commnds['rlon'] = 'MEAN'
        #ag_commnds['altitude'] = 'MEAN'
        #####################################################################

        ####################### NAMELIST PLOT #######################
        nDPlot = 1 # How many dimensions should plot have (1 or 2)
        i_diffPlot = 1 # Draw plot showing difference filtered - unfiltered # TODO
        plotOutDir = '../00_plots/01_domAv_Fields/'+fieldName
        import os
        if not os.path.exists(plotOutDir):
            os.makedirs(plotOutDir)
        plotName = 'domAv_'+fieldName+'_alt_'+str(altitude)+'_NEW.png'
        ##### 1D PLOT #########

        ##### 2D Contour ######
        contourTranspose = 0 # Reverse contour dimensions?
        plotContour = 0 # Besides the filled contour, also plot the contour?
        cmapM = 'jet' # colormap for Model output (jet, terrain, inferno, YlOrRd)
        axis = 'equal' # set 'equal' if keep aspect ratio, else 'auto'
        # COLORBAR Models
        autoTicks = 1 # 1 if colorbar should be set automatically
        Mmask = 1 # Mask Model values lower than MThrMinRel of maximum value?
        MThrMinRel = 0.15 # Relative amount of max value to mask (see Mmask)
        Mticks = [0.0001,0.0002,0.0003,0.0004,0.0005]
        Mticks = list(np.arange(0.0002,0.0022,0.0002))
        # COLORBAR Models
        cmapD = 'bwr' # colormap for Difference output (bwr)
        #####################################################################


        an = analysis.analysis(inpPath, [fieldName])

        an.subSpaceInds = subSpaceIndsIN
        an.ag_commnds = ag_commnds
        an.i_info = i_info
        an.i_resolutions = i_resolutions

        # RUN ANALYSIS
        an.run()


        import matplotlib
        if i_plot == 2:
            matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        import math


        if i_plot > 0:
            if i_info >= 3:
                print('plotting')
            #mainVar = an.vars[fieldName]
            mainVar = an.vars[an.varNames[0]]
            someField = next(iter(mainVar.ncos.values())).field
            if i_info >= 1:
                print('NONSINGLETONS: ' + str(someField.nNoneSingleton))
            
                    
            if nDPlot == 1 and someField.nNoneSingleton == 1:
                import ncPlots.ncSubplots1D as ncSubplots
                ncs = ncSubplots.ncSubplots(an, nDPlot, i_diffPlot, 'HOR')
            
                ncs.plotVar(an.vars[fieldName])
                        
                title = 'domain average ' + an.vars[fieldName].label + ' at ' + str(altitude) + ' m'
                ncs.fig.suptitle(title, fontsize=14)
                

            else:
                raise ValueError('ERROR: CANNOT MAKE ' + str(nDPlot) + 'D-PLOT WITH ' +
                str(mainVar.nNoneSingleton) + ' NON-SINGLETON DIMS!')

            
            if i_plot == 1:
                plt.show()
            elif i_plot == 2:
                plotPath = plotOutDir + '/' + plotName
                plt.savefig(plotPath, format='png', bbox_inches='tight')



