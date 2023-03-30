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
#dynamics = ['zW', 'zU', 'zV', 'zT', 'zP', 'zRH']
dynamics = ['zW', 'zU', 'zV', 'zT', 'zRH']

fieldNames = TTendencies
fieldNames = QVTendencies
#fieldNames = hydrometeors
#fieldNames = dynamics
fieldNames = ['zQV']

diurnals = list(range(6,24))
diurnals.extend(list(range(0,6)))

xlims = {}
xlims['zW'] = (-0.015,0.015)
xlims['zU'] = (-5,1)
xlims['zV'] = (-7,0)
xlims['zT'] = (-5,3)
xlims['zRH'] = (20,70)

xlims['zQC'] = (0,0.012)
xlims['zQI'] = (0,0.01)
xlims['zQV'] = (0,11)
xlims['zQR'] = (0,0.013)
xlims['zQS'] = (0,0.04)
xlims['zQG'] = (0,0.026)

xlims['zAQVT_MIC'] = (-0.09,0.04)
xlims['zAQVT_ADV'] = (-0.6,0.2)
xlims['zAQVT_ZADV'] = (-0.6,0.2)
xlims['zAQVT_HADV'] = (-0.5,0.6)
xlims['zAQVT_TURB'] = (-0.1,0.4)
xlims['zAQVT_TOT'] = (-0.3,0.2)
#for var in QVTendencies:
#    xlims[var] = (-1.0,1.0)

xlims['zATT_MIC'] = (-0.2,0.3)
xlims['zATT_ADV'] = (-1.0,0.3)
xlims['zATT_ZADV'] = (-0.2,1.0)
xlims['zATT_HADV'] = (-1.4,0.0)
xlims['zATT_TURB'] = (-0.4,1.4)
xlims['zATT_TOT'] = (-0.7,1.0)
xlims['zATT_RAD'] = (-0.2,0.2)
#for var in TTendencies:
#    xlims[var] = (-1.0,1.3)

for fieldName in fieldNames:
    print('#######################')
    print(fieldName)
    ####################### NAMELIST DIMENSIONS #######################
    i_subDomain = 1 # 0: full domain, 1: alpine region
    ssI, domainName = setSSI(i_subDomain, {'4.4':{}, '2.2':{}, '1.1':{}}) 
    startHght = 2 
    endHght = 64 
    altInds = list(range(startHght,endHght+1))
    for i in range(0,len(diurnals)):
        print(diurnals[i])
        ssI['altitude'] = altInds 
        ssI['diurnal'] = [diurnals[i]]
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
        plotOutDir = '../00_plots/01_domAv_Fields/domain_'+str(domainName)+'/diurnal/'+fieldName
        import os
        if not os.path.exists(plotOutDir):
            os.makedirs(plotOutDir)
        plotName = 'dA_'+fieldName+'_dom_'+str(domainName)+'_'+str(i)+'_hr_'+str(diurnals[i])+'.png'
        #print(plotName)
        ##### 1D PLOT #########


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

                title = 'dA ' + an.vars[fieldName].label + ' hr ' + str(diurnals[i])
                ncs.fig.suptitle(title, fontsize=14)

                if fieldName in xlims:
                    for mI,mode in enumerate(an.modes):
                        ax = ncs.axes[0,mI]
                        ax.set_xlim(xlims[fieldName])
                    
                        
            else:
                raise ValueError('ERROR: CANNOT MAKE ' + str(nDPlot) + 'D-PLOT WITH ' +
                str(someField.nNoneSingleton) + ' NON-SINGLETON DIMS!')

            
            if i_plot == 1:
                plt.show()
            elif i_plot == 2:
                plotPath = plotOutDir + '/' + plotName
                plt.savefig(plotPath, format='png', bbox_inches='tight')



