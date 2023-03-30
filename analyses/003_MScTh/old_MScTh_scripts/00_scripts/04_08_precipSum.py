################################
# Calculate domain Average Precipitation
# author: Christoph Heim
# date: 21 10 2017
#################################
import os
os.chdir('00_scripts/')

i_resolutions = 3 # 1 = 4.4, 2 = 4.4 + 2.2, 3 = ...
i_plot = 2 # 0 = no plot, 1 = show plot, 2 = save plot
i_info = 2 # output some information [from 0 (off) to 5 (all you can read)]
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
inpPath = '../02_fields/subDomDiur'
inpPath = '../02_fields/diurnal'
#inpPath = '../02_fields/topocut'

others = ['cHSURF', 'nTOT_PREC', 'nHPBL']
hydrometeors = ['zQC', 'zQI', 'zQV', 'zQR', 'zQS', 'zQG']
TTendencies = ['zATT_MIC', 'zATT_RAD', 'zATT_ADV', 'zATT_ZADV', 'zATT_TURB', 'zATT_TOT']
QVTendencies = ['zAQVT_MIC', 'zAQVT_ADV', 'zAQVT_ZADV', 'zAQVT_TURB', 'zAQVT_TOT']
dynamics = ['zW', 'zU', 'zV', 'zT', 'zP']
fieldNames = ['zU', 'cHSURF']
fieldNames = ['nTOT_PREC', 'cHSURF']
#fieldNames = ['zAQVT_ZADV']
#####################################################################		

####################### NAMELIST DIMENSIONS #######################
i_subDomain = 1 # 0: full domain, 1: alpine region
ssI, domainName = setSSI(i_subDomain, {'4.4':{}, '2.2':{}, '1.1':{}}) 
#startHght = 25 
#endHght = 60 
#altInds = list(range(startHght,endHght+1))
#ssI['altitude'] = altInds 
#startTime = datetime(2006,7,11,00)
#endTime = datetime(2006,7,11,23)
#ssI['time'] = [startTime,endTime] # border values (one value if only one time step desired)

ssI['diurnal'] = [20,21,22,23,0,1,2,3,4,5,6,7] # list values
#ssI['diurnal'] = [8,9,10,11,12,13,14,15,16,17,18,19] # list values

#ssI['diurnal'] = [12,13,14,15,16,17] # list values
#ssI['diurnal'] = [18,19,20,21,22,23] # list values
#ssI['diurnal'] = [0 ,1 ,2 ,3 ,4 ,5 ] # list values
#ssI['diurnal'] = [6 ,7 ,8 ,9 ,10,11] # list values

####################### NAMELIST AGGREGATE #######################
# Options: MEAN, SUM 
ag_commnds = {}
#ag_commnds['rlat'] = 'MEAN'
#ag_commnds['rlon'] = 'MEAN'
#ag_commnds['time'] = 'SUM'
ag_commnds['diurnal'] = 'SUM'
#ag_commnds['altitude'] = 'MEAN'
#####################################################################

####################### NAMELIST PLOT #######################
nDPlot = 2 # How many dimensions should plot have (1 or 2)
i_diffPlot = 0 # Draw plot showing difference filtered - unfiltered # TODO
plotOutDir = '../00_plots/04_coldPools'
plotName = 'Accum_Precip_'+str(ssI['diurnal'][0])+'-'+str(ssI['diurnal'][-1]+1)
##### 1D PLOT #########

##### 2D Contour ######
contourTranspose = 0 # Reverse contour dimensions?
plotContour = 0 # Besides the filled contour, also plot the contour?
cmapM = 'jet' # colormap for Model output (jet, terrain, inferno, YlOrRd)
axis = 'equal' # set 'equal' if keep aspect ratio, else 'auto'
# COLORBAR Models
autoTicks = 0 # 1 if colorbar should be set automatically
Mmask = 1 # Mask Model values lower than MThrMinRel of maximum value?
MThrMinRel = 0.02 # Relative amount of max value to mask (see Mmask)
Mticks = list(np.arange(10,125,10))
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
        
        (fig,axes,MCB) = ncs.plotVar(an.vars[an.varNames[0]])

        MCB.set_label(r'Total Accumulated Precipitation $[mm]$', fontsize=19*ncs.MAG)
            
        #title = 'Accum. Precip. '+str(ssI['diurnal'][0])+'-'+str(ssI['diurnal'][-1]+1)
        #ncs.fig.suptitle(title, fontsize=14)

        

        for rowInd,mode in enumerate(an.modes):
            if ncs.orientation == 'VER':
                ax = ncs.axes[rowInd,0]
            elif ncs.orientation == 'HOR':
                ax = ncs.axes[0,rowInd]

            ## PLOT ADJUSTMENTS
            #ax.set_xlabel('Latitude',fontsize=12)
            #if mode == '':
            #    ax.legend_.remove()
            #    ax.set_ylabel('',fontsize=12)
            #else:
            #    ax.set_ylabel(r'Rain Rate $[mm h^{-1}]$',fontsize=12)
            #ax.set_ylim(0,1.7)



    elif nDPlot == 1 and someField.nNoneSingleton == 1:
        import ncPlots.ncSubplots1D as ncSubplots
        ncs = ncSubplots.ncSubplots(an, nDPlot, i_diffPlot, 'HOR')
    
        for varName in an.varNames:
            if varName != 'cHSURF':
                ncs.plotVar(an.vars[varName])

        title = 'title' 
        ncs.fig.suptitle(title, fontsize=14)

    else:
        raise ValueError('ERROR: CANNOT MAKE ' + str(nDPlot) + 'D-PLOT WITH ' +
        str(someField.nNoneSingleton) + ' NON-SINGLETON DIMS!')

    
    if i_plot == 1:
        plt.show()
    elif i_plot == 2:
        plotPath = plotOutDir + '/' + plotName + '.png'
        plt.savefig(plotPath, format='png', bbox_inches='tight')
        plt.close('all')
    elif i_plot == 3:
        plotPath = plotOutDir + '/' + plotName+'.pdf'
        plt.savefig(plotPath, format='pdf', bbox_inches='tight')
        plt.close('all')

          


