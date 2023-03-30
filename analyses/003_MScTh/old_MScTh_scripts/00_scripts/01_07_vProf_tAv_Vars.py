#################################
# Calculate domain Average Precipitation
# author: Christoph Heim
# date: 21 10 2017
#################################
import os
os.chdir('00_scripts/')

i_resolutions = 1 # 1 = 4.4, 2 = 4.4 + 2.2, 3 = ...
i_plot = 1 # 0 = no plot, 1 = show plot, 2 = save plot
i_info = 2 # output some information [from 0 (off) to 5 (all you can read)]
i_diffPlot = 1
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
others = ['cHSURF', 'nTOT_PREC']
hydrometeors = ['zQC', 'zQI', 'zQV', 'zQR', 'zQS', 'zQG']
TTendencies=['zATT_MIC','zATT_RAD','zATT_ADV','zATT_ZADV','zATT_TURB','zATT_TOT','zATT_HADV']
QVTendencies=['zAQVT_MIC','zAQVT_ADV','zAQVT_ZADV','zAQVT_TURB','zAQVT_TOT','zAQVT_HADV']
dynamics = ['zW', 'zU', 'zV', 'zT', 'zP', 'zRH']

fieldNames = TTendencies
fieldNames = QVTendencies
fieldNames = hydrometeors
fieldNames = dynamics
fieldNames = ['zPOTT']

for fieldName in fieldNames:
    print('#######################')
    print(fieldName)
    ####################### NAMELIST DIMENSIONS #######################
    i_subDomain = 1 # 0: full domain, 1: alpine region
    ssI, domainName = setSSI(i_subDomain, {'4.4':{}, '2.2':{}, '1.1':{}}) 
    startHght = 2 
    endHght = 64 
    altInds = list(range(startHght,endHght+1))
    ssI['altitude'] = altInds 
    #ssI['diurnal'] = [7,8,9]
    #####################################################################

    ####################### NAMELIST AGGREGATE #######################
    # Options: MEAN, SUM, DIURNAL
    ag_commnds = {}
    ag_commnds['rlat'] = 'MEAN'
    ag_commnds['rlon'] = 'MEAN'
    ag_commnds['diurnal'] = 'MEAN'
    #ag_commnds['altitude'] = 'MEAN'
    #####################################################################

    ####################### NAMELIST PLOT #######################
    nDPlot = 1 # How many dimensions should plot have (1 or 2)
    plotOutDir = '../00_plots/01_domAv_Fields/domain_'+str(domainName)+'/timeAv'
    #plotOutDir = '../00_plots/01_domAv_Fields/domain_'+str(domainName)+'/timeAv_6_12'
    #plotOutDir = '../00_plots/01_domAv_Fields/domain_'+str(domainName)+'/timeAv_7_10'
    import os
    if not os.path.exists(plotOutDir):
        os.makedirs(plotOutDir)
    if i_diffPlot == 1:
        plotName = 'dA_tA_'+fieldName+'_dom_'+str(domainName)+'_diff.png'
    else:
        plotName = 'dA_tA_'+fieldName+'_dom_'+str(domainName)+'.png'
    ##### 1D PLOT #########

    ##### 2D Contour ######
    contourTranspose = 0 # Reverse contour dimensions?
    plotContour = 0 # Besides the filled contour, also plot the contour?
    axis = 'auto' # set 'equal' if keep aspect ratio, else 'auto'
    # COLORBAR Models
    cmapM = 'jet'
    Mmask = 0
    autoTicks = 0
    Mticks = None
    if fieldName in TTendencies:
        cmapM = 'seismic'
        absMax = 0.4
        step = 0.02
        Mticks = list(np.arange(-absMax,absMax+0.001,step))
    elif fieldName in QVTendencies:
        cmapM = 'seismic'
        absMax = 0.2
        step = 0.01
        Mticks = list(np.arange(-absMax,absMax+0.001,step))
    elif fieldName == 'zW':
        Mticks = list(np.arange(0.001,0.0140,0.0005)) 
    elif fieldName in hydrometeors:
        step = 0.001
        absMin = 0.001
        if fieldName == 'zQC':
            absMax = 0.013
        elif fieldName == 'zQG':
            absMax = 0.027
        elif fieldName == 'zQS':
            absMax = 0.042
        elif fieldName == 'zQI':
            absMax = 0.010
        elif fieldName == 'zQR':
            absMax = 0.013
        elif fieldName == 'zQV':
            absMin = 0
            absMax = 14
            step = 0.7
        Mticks = list(np.arange(absMin,absMax+0.001,step))
    elif fieldName in ['zT', 'zU', 'zV']:
        autoTicks = 1
        cmapM = 'seismic'
    else:
        autoTicks = 1 
    MThrMinRel = 0.15 # Relative amount of max value to mask (see Mmask)
    # COLORBAR Models
    cmapD = 'bwr' # colormap for Difference output (bwr)
    #####################################################################


    an = analysis.analysis(inpPath, [fieldName])

    an.subSpaceInds = ssI
    an.ag_commnds = ag_commnds
    an.i_info = i_info
    an.i_resolutions = i_resolutions

    # RUN ANALYSIS
    an.run()

            

    # If temperature remove lapse rate
    if fieldName == 'zT':
        for res in an.resolutions:
            for mode in an.modes:
                field = an.vars['zT'].ncos[res+mode].field
                alts = field.dims['altitude'].vals
                field.vals[:,:,0,0] = field.vals[:,:,0,0] - 300 + 0.0065*alts

    import matplotlib
    if i_plot == 2:
        matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    import math


    if i_plot > 0:
        if i_info >= 3:
            print('plotting')
        mainVar = an.vars[an.varNames[0]]
        someField = next(iter(mainVar.ncos.values())).field
        if i_info >= 1:
            print('NONSINGLETONS: ' + str(someField.nNoneSingleton))
                
        if nDPlot == 1 and someField.nNoneSingleton == 1:
            import ncPlots.ncSubplots1D as ncSubplots
            ncs = ncSubplots.ncSubplots(an, nDPlot, i_diffPlot, 'HOR')
        
            for varName in an.varNames:
                if varName != 'cHSURF':
                    ncs.plotVar(an.vars[varName])

            title = 'dA tA ' + an.vars[fieldName].label
            ncs.fig.suptitle(title, fontsize=14)
        else:
            raise ValueError('ERROR: CANNOT MAKE ' + str(nDPlot) + 'D-PLOT WITH ' +
            str(someField.nNoneSingleton) + ' NON-SINGLETON DIMS!')

        
        if i_plot == 1:
            plt.show()
        elif i_plot == 2:
            plotPath = plotOutDir + '/' + plotName
            plt.savefig(plotPath, format='png', bbox_inches='tight')



