#################################
# Calculate domain Average Precipitation
# author: Christoph Heim
# date: 21 10 2017
#################################
import os
os.chdir('00_scripts/')

i_resolutions = 3 # 1 = 4.4, 2 = 4.4 + 2.2, 3 = ...
i_plot = 1 # 0 = no plot, 1 = show plot, 2 = save plot
i_info = 2 # output some information [from 0 (off) to 5 (all you can read)]
altInd = 63

import matplotlib
if i_plot > 1:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt


import ncClasses.analysis as analysis
from datetime import datetime
from functions import *
####################### NAMELIST INPUTS FILES #######################
# directory of input model folders
inpPath = '../02_fields/topocut'

others = ['cHSURF', 'nTOT_PREC', 'nHPBL']
hydrometeors = ['zQC', 'zQI', 'zQV', 'zQR', 'zQS', 'zQG']
TTendencies = ['zATT_MIC', 'zATT_RAD', 'zATT_ADV', 'zATT_ZADV', 'zATT_TURB', 'zATT_TOT']
QVTendencies = ['zAQVT_MIC', 'zAQVT_ADV', 'zAQVT_ZADV', 'zAQVT_TURB', 'zAQVT_TOT']
dynamics = ['zW', 'zU', 'zV', 'zT', 'zP']
fieldNames = ['zQC']
#####################################################################		

####################### NAMELIST DIMENSIONS #######################
subDomain = 1 # 0: full domain, 1: alpine region
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


startTime = datetime(2006,7,11,0)
startTime = datetime(2006,7,12,12)
endTime = datetime(2006,7,19,23)
endTime = datetime(2006,7,12,23)
subSpaceInds['time'] = [startTime,endTime] # border values
subSpaceInds['altitude'] = list(range(altInd,altInd+1))
#####################################################################

ag_commnds = {}
an = analysis.analysis(inpPath, fieldNames)

an.subSpaceInds = subSpaceInds
an.ag_commnds = ag_commnds
an.i_info = i_info
an.i_resolutions = i_resolutions

# RUN ANALYSIS
an.run()

altitude = 6000 + (altInd-60)*1000
altitude = altInd*100

outPath = '../00_plots/08_cloud_cluster/'

an.vars[fieldNames[0]].setValueLimits()
if fieldNames[0] == 'zW':
    binMax = np.ceil(an.vars[fieldNames[0]].max)
    binMax = binMax + 0.5
    binMin = np.floor(an.vars[fieldNames[0]].min)
    binMin = binMin - 0.5
    nbins2 = int((binMax - binMin)/2)
    dbin = 1
    bins = np.arange(binMin,binMax,dbin)
elif fieldNames[0] == 'zQC':
    binMin = 0
    binMax = np.max(an.vars[fieldNames[0]].max)
    bins = np.linspace(binMin,binMax,num=30)
binsCentred = bins[0:(len(bins)-1)] + np.diff(bins)/2

freqs = {}
nPoints = {}
outRess = []
outModes = []

for res in an.resolutions: 
    for mode in an.modes:
        simLabel = str(res)+mode
        print(simLabel)
        vals = an.vars[fieldNames[0]].ncos[str(res)+mode].field.vals
        vals = vals.flatten()
        vals = vals[~np.isnan(vals)] # remove mountains

        # CREATE HISTOGRAMS
        nPoint = np.histogram(vals, bins=bins)[0]
        #nPoints.append(nPoint[0]) 
        nPoints[simLabel] = nPoint
        freq = nPoint/len(vals)
        #freqs.append(freq)
        freqs[simLabel] = freq
        outRess.append(str(res))
        outModes.append(mode)

        val = 0.001
        #print(binsCentred[binsCentred > val])
        #print(nPoint[binsCentred > val])
        print(np.sum(nPoint[binsCentred > val]))

