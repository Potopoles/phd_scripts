#################################
# Calculate domain Average Precipitation
# author: Christoph Heim
# date: 21 10 2017
#################################
import os
os.chdir('00_scripts/')

i_resolutions = 5 # 1 = 4.4, 2 = 4.4 + 2.2, 3 = ...
i_plot = 2 # 0 = no plot, 1 = show plot, 2 = save plot
i_info = 2 # output some information [from 0 (off) to 5 (all you can read)]
import matplotlib
if i_plot == 2:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt


import ncClasses.analysis as analysis
import ncClasses.variable as variable
from datetime import datetime, timedelta
from functions import *
####################### NAMELIST INPUTS FILES #######################
# directory of input model folders
#inpPath = '../02_fields/subDomDiur'
inpPath = '../02_fields/topocut'
outPath = '../02_fields/topocut'

others = ['cHSURF', 'nTOT_PREC', 'nHPBL']
hydrometeors = ['zQC', 'zQI', 'zQV', 'zQR', 'zQS', 'zQG']
TTendencies = ['zATT_MIC', 'zATT_RAD', 'zATT_ADV', 'zATT_ZADV', 'zATT_TURB', 'zATT_TOT']
QVTendencies = ['zAQVT_MIC', 'zAQVT_ADV', 'zAQVT_ZADV', 'zAQVT_TURB', 'zAQVT_TOT']
dynamics = ['zW', 'zU', 'zV', 'zT', 'zP']
fieldNames = ['zP', 'zQV', 'zT']
#####################################################################		

####################### NAMELIST DIMENSIONS #######################
subDomain = 0 # 0: full domain, 1: alpine region
# SUBSPACE
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
elif subDomain == 5: # zoom in subdomain
    subSpaceInds['rlon'] = [80,180]
    subSpaceInds['rlat'] = [50,120]


startTime = datetime(2006,7,11,0)
endTime = datetime(2006,7,20,0)
subSpaceInds['time'] = [startTime, endTime] # border values
#subSpaceInds['diurnal'] = [10] # list values
#subSpaceInds['diurnal'] = list(range(0,24)) 
startHght = 0
endHght = 40 
subSpaceInds['altitude'] = list(range(startHght,endHght+1))
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
i_diffPlot = 1 # Draw plot showing difference filtered - unfiltered # TODO
plotOutDir = '../00_plots/04_coldPools/'
plotName = 'RHtest.png'
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
Mticks = [0.0001,0.0002,0.0003,0.0004,0.0005]
Mticks = list(np.arange(0,110,5))
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

varRH = an.vars['zP']._copy()	
varRH.varName = 'zRH' 
for res in an.resolutions:
    for mode in an.modes:
        p = an.vars['zP'].ncos[res+mode].field.vals
        qv = an.vars['zQV'].ncos[res+mode].field.vals
        T = an.vars['zT'].ncos[res+mode].field.vals
        TC = T - 273.15 # Temperature in Celsius

        eps = 0.622
        e = p*qv/(eps+qv) # vapor pressure
        es = 611*np.exp(17.27*TC/(273.3+TC)) # saturation vapor pressure
        RH = e/es*100
        varRH.ncos[res+mode].field.vals = RH
        varRH.ncos[res+mode].fieldName = 'RH'
        varRH.ncos[res+mode].field.name = 'RH'
        outNCPath = outPath + '/'+ res+mode + '/zRH.nc'
        varRH.ncos[res+mode].saveToNewNC(outNCPath)


