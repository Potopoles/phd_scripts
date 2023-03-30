#################################
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
####################### NAMELIST INPUTS FILES #######################
# directory of input model folders
inpPath = '../02_fields/subDomDiur'
#inpPath = '../02_fields/topocut'

others = ['cHSURF', 'nTOT_PREC', 'nHPBL']
hydrometeors = ['zQC', 'zQI', 'zQV', 'zQR', 'zQS', 'zQG']
TTendencies = ['zATT_MIC', 'zATT_RAD', 'zATT_ADV', 'zATT_ZADV', 'zATT_TURB', 'zATT_TOT']
QVTendencies = ['zAQVT_MIC', 'zAQVT_ADV', 'zAQVT_ZADV', 'zAQVT_TURB', 'zAQVT_TOT']
dynamics = ['zW', 'zU', 'zV', 'zT', 'zP']
fieldNames = ['zW', 'cHSURF']
fieldNames = ['nATHB_T', 'cHSURF']
fieldNames = ['nATHB_T']
#fieldNames = ['nCIN_ML', 'cHSURF']
#####################################################################		

####################### NAMELIST DIMENSIONS #######################
subDomain = 4 # 0: full domain, 1: alpine region
subSpaceInds = {}
if subDomain == 0: # (use topocut) 
    domainName = 'Whole_Domain'
if subDomain == 1: 
    domainName = 'Alpine_Region'
    if inpPath == '../02_fields/topocut': # (in case of topocut)
        subSpaceInds['rlon'] = [50,237]
        subSpaceInds['rlat'] = [41,155]
    else: # (in case of subDomDiur) 
        pass
if subDomain == 2: # small Debug domain (use topocut)
    subSpaceInds['rlon'] = [60,90]
    subSpaceInds['rlat'] = [70,90]
if subDomain == 3: # Northern Italy plains (use subDomDiur)
    domainName = 'Northern_Italy_Plains'
    subSpaceInds['rlon'] = [48,100]
    subSpaceInds['rlat'] = [25,56]
if subDomain == 4: # Greater Northern Italy plains (use subDomDiur)
    domainName = 'Greater_Northern_Italy_Plains'
    subSpaceInds['rlon'] = [45,118]
    subSpaceInds['rlat'] = [12,62]


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
ag_commnds['rlat'] = 'MEAN'
ag_commnds['rlon'] = 'MEAN'
#ag_commnds['time'] = 'MEAN'
#ag_commnds['diurnal'] = 'MEAN'
#ag_commnds['altitude'] = 'MEAN'
#####################################################################

####################### NAMELIST PLOT #######################
nDPlot = 1 # How many dimensions should plot have (1 or 2)
i_diffPlot = 1 # Draw plot showing difference filtered - unfiltered # TODO
plotOutDir = '../00_plots/04_coldPools'
plotName = 'ATHB_T_dA_'+domainName+'.png'
#plotName = 'CIN_tA_'+domainName+'.png'
##### 1D PLOT #########

##### 2D Contour ######
contourTranspose = 0 # Reverse contour dimensions?
cmapM = 'jet' # colormap for Model output (jet, terrain, inferno, YlOrRd)
axis = 'auto' # set 'equal' if keep aspect ratio, else 'auto'
# COLORBAR Models
autoTicks = 0 # 1 if colorbar should be set automatically
Mmask = 0 # Mask Model values lower than MThrMinRel of maximum value?
MThrMinRel = 0.25 # Relative amount of max value to mask (see Mmask)
Mticks = [0.0001,0.0002,0.0003,0.0004,0.0005]
Mticks = list(np.arange(200,300,5))
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

for res in an.resolutions:
    for mode in an.modes:
        field = an.vars['nATHB_T'].ncos[res+mode].field
        field.vals = -field.vals
        field._calcMaxMin()


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
            
        title = 'ATHB_T tA '+domainName 
        #title = 'CIN tA '+domainName 
        ncs.fig.suptitle(title, fontsize=14)

    elif nDPlot == 1 and someField.nNoneSingleton == 1:
        import ncPlots.ncSubplots1D as ncSubplots
        ncs = ncSubplots.ncSubplots(an, nDPlot, i_diffPlot, 'HOR')
    
        for varName in an.varNames:
            if varName != 'cHSURF':
                ncs.plotVar(an.vars[varName])

        title = 'ATHB_T dA '+domainName 
        #title = 'CIN tA '+domainName 
        ncs.fig.suptitle(title, fontsize=14)

    else:
        raise ValueError('ERROR: CANNOT MAKE ' + str(nDPlot) + 'D-PLOT WITH ' +
        str(someField.nNoneSingleton) + ' NON-SINGLETON DIMS!')

    
    if i_plot == 1:
        plt.show()
    elif i_plot == 2:
        plotPath = plotOutDir + '/' + plotName
        plt.savefig(plotPath, format='png', bbox_inches='tight')

          


