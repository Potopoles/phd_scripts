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
inpPath = '../02_fields/diurnal'
inpPath = '../02_fields/subDomDiur'
others = ['cHSURF', 'nTOT_PREC', 'nHPBL']
hydrometeors = ['zQC', 'zQI', 'zQV', 'zQR', 'zQS', 'zQG']
TTendencies = ['zATT_MIC', 'zATT_RAD', 'zATT_ADV', 'zATT_ZADV', 'zATT_TURB', 'zATT_TOT']
QVTendencies = ['zAQVT_MIC', 'zAQVT_ADV', 'zAQVT_ZADV', 'zAQVT_TURB', 'zAQVT_TOT']
dynamics = ['zW', 'zU', 'zV', 'zT', 'zP']
fieldNames = ['cHSURF', 'zU']
fieldNames = ['zU']
#####################################################################		
aggs = ['lat', 'lon']
hours = np.arange(0,24)
#hours = 14
####################### NAMELIST DIMENSIONS #######################
subDomain = 2 # 0: full domain, 1: alpine region, 2: zoom in
# SUBSPACE
subSpaceIndsIN = {}
if subDomain == 1: # alpine region
    subSpaceIndsIN['rlon'] = (61,88)
    subSpaceIndsIN['rlat'] = (48,71)
elif subDomain == 2: # zoom in subdomain
    subSpaceIndsIN['rlon'] = (42,112)
    subSpaceIndsIN['rlat'] = (12,69)

for agg in aggs:
    print(agg)
    for hour in hours:
        print('\t'+str(hour))
        startHr = hour
        endHr = hour+1
        subSpaceIndsIN['diurnal'] = (startHr,endHr)
        #subSpaceIndsIN['altitude'] = (30,31)
        #####################################################################

        ####################### NAMELIST AGGREGATE #######################
        # Options: MEAN, SUM 
        ag_commnds = {}
        #ag_commnds['rlat'] = 'MEAN'
        if agg == 'lon':
            ag_commnds['rlon'] = 'MEAN'
        elif agg == 'lat':
            ag_commnds['rlat'] = 'MEAN'
        #ag_commnds['time'] = 'MEAN'
        #ag_commnds['diurnal'] = 'MEAN'
        #ag_commnds['altitude'] = 'MEAN'
        #####################################################################

        ####################### NAMELIST PLOT #######################
        nDPlot = 2 # How many dimensions should plot have (1 or 2)
        i_diffPlot = 0 # Draw plot showing difference filtered - unfiltered # TODO
        plotOutDir = '../00_plots/04_coldPools/domain'+str(subDomain)+'_'+fieldNames[0]+'_agg_'+agg
        import os
        if not os.path.exists(plotOutDir):
            os.makedirs(plotOutDir)
        hrStr = '{num:02d}'.format(num=hour)
        plotName = fieldNames[0]+'_hr_'+hrStr+'.png'
        ##### 1D PLOT #########

        ##### 2D Contour ######
        contourTranspose = 0 # Reverse contour dimensions?
        plotContour = 0 # Besides the filled contour, also plot the contour?
        cmapM = 'seismic' # colormap for Model output (jet, terrain, inferno, YlOrRd)
        axis = 'auto' # set 'equal' if keep aspect ratio, else 'auto'
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
            
                
                ncs.plotVar(an.vars[fieldNames[0]])
                #ncs.addContour(an.vars['zU'], 'black', 0.5, 2)
                    
                title = 'hr: ' + str(hour) 
                ncs.fig.suptitle(title, fontsize=14)


            else:
                raise ValueError('ERROR: CANNOT MAKE ' + str(nDPlot) + 'D-PLOT WITH ' +
                str(someField.nNoneSingleton) + ' NON-SINGLETON DIMS!')

            
            if i_plot == 1:
                plt.show()
            elif i_plot == 2:
                plotPath = plotOutDir + '/' + plotName
                plt.savefig(plotPath, format='png', bbox_inches='tight')

                  


