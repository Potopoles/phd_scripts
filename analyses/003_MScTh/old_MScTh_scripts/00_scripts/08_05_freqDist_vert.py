#################################
# Calculate domain Average Precipitation
# author: Christoph Heim
# date: 21 10 2017
#################################
import os
os.chdir('00_scripts/')
import sys

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
inpPath = '../02_fields/subDomDiur'
inpPath = '../02_fields/topocut'

others = ['cHSURF', 'nTOT_PREC', 'nHPBL']
hydrometeors = ['zQC', 'zQI', 'zQV', 'zQR', 'zQS', 'zQG']
TTendencies = ['zATT_MIC', 'zATT_RAD', 'zATT_ADV', 'zATT_ZADV', 'zATT_TURB', 'zATT_TOT']
QVTendencies = ['zAQVT_MIC', 'zAQVT_ADV', 'zAQVT_ZADV', 'zAQVT_TURB', 'zAQVT_TOT']
dynamics = ['zW', 'zU', 'zV', 'zT']
dynamics = ['zW', 'zU', 'zV', 'zT', 'zP']
#####################################################################		
#varName = 'zQC'
#varName = 'zQI'
#varName = 'zQV'
#varName = 'zQR'
#varName = 'zQS'
#varName = 'zQG'

#varName = 'zW'
#varName = 'zU'
#varName = 'zV'
#varName = 'zT'

#varName = 'zAQVT_TOT'
#varName = 'zAQVT_ADV'
#varName = 'zAQVT_ZADV'
#varName = 'zAQVT_MIC'
#varName = 'zAQVT_TURB'

#varName = 'zATT_TOT'
#varName = 'zATT_ADV'
#varName = 'zATT_ZADV'
#varName = 'zATT_MIC'
#varName = 'zATT_TURB'
#varName = 'zATT_RAD'
nbins = 50
if len(sys.argv) > 1:
    varName = sys.argv[1]
fieldNames = [varName]
altInds = np.asarray(list(range(0,65)))
outPath = '../00_plots/08_cloud_cluster/vertProfs/'
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


startTime = datetime(2006,7,11,00)
endTime = datetime(2006,7,19,23)
#endTime = datetime(2006,7,13,23)
subSpaceInds['time'] = [startTime,endTime] # border values

if varName == 'zQC':
    binMin = 0
    binMax = 0.009
    rangeD = 1.5
elif varName == 'zQI':
    binMin = 0
    binMax = 0.0015
    rangeD = 1
elif varName == 'zQV':
    binMin = 0
    binMax = 0.017
    rangeD = 1.5
elif varName == 'zQR':
    binMin = 0
    binMax = 0.010
    rangeD = 1
elif varName == 'zQS':
    binMin = 0
    binMax = 0.008
    rangeD = 3
elif varName == 'zQG':
    binMin = 0
    binMax = 0.013
    rangeD = 0.5
elif varName == 'zW':
    binMin = -18
    binMax = 42 
    rangeD = 2
elif varName == 'zU':
    binMin = -30
    binMax = 30 
    rangeD = 2
elif varName == 'zV':
    binMin = -30
    binMax = 30 
    rangeD = 2
elif varName == 'zT':
    binMin = -10
    binMax = 15 
    rangeD = 1
elif varName == 'zAQVT_TOT':
    binMin = -0.000005
    binMax = 0.000005 
    rangeD = 1
elif varName == 'zAQVT_ADV':
    binMin = -0.000015
    binMax = 0.000025 
    rangeD = 1.5
elif varName == 'zAQVT_ZADV':
    binMin = -0.00015
    binMax = 0.00008 
    rangeD = 3
elif varName == 'zAQVT_MIC':
    binMin = -0.000025
    binMax = 0.00001 
    rangeD = 2
elif varName == 'zAQVT_TURB':
    binMin = -0.000013
    binMax = 0.000013 
    rangeD = 3

elif varName == 'zATT_TOT':
    binMin = -0.010
    binMax = 0.010 
    rangeD = 1
elif varName == 'zATT_ADV':
    binMin = -0.10
    binMax = 0.06
    rangeD = 2
elif varName == 'zATT_ZADV':
    binMin = -0.15
    binMax = 0.25
    rangeD = 1
elif varName == 'zATT_MIC':
    binMin = -0.03
    binMax = 0.07 
    rangeD = 2
elif varName == 'zATT_TURB':
    binMin = -0.012
    binMax = 0.015 
    rangeD = 1
elif varName == 'zATT_RAD':
    binMin = -0.003
    binMax = 0.0015 
    rangeD = 1

# for all!
rangeD = 1

bins = np.linspace(binMin,binMax,num=nbins+1)
binsCentred = bins[0:(len(bins)-1)] + np.diff(bins)/2

an = analysis.analysis(inpPath, fieldNames)
an.i_resolutions = i_resolutions
an.set_resolutions()
out = {}
for res in an.resolutions:
    out[res] = {}
    out[res]['mask'] = np.full((len(altInds),nbins),1) 
    for mode in an.modes:
        out[res][mode] = np.full((len(altInds),nbins),np.nan) 


altitudes = np.full(len(altInds),np.nan)
altitudes[altInds <= 60] = altInds[altInds <= 60]*100
altitudes[altInds > 60] = (altInds[altInds > 60]-60)*1000+6000

for i in range(0,len(altInds)):
    if i % 10 == 0:
        print('    ' + str(altInds[i]))
    subSpaceInds['altitude'] = list(range(altInds[i],altInds[i]+1))
    #####################################################################
    an = analysis.analysis(inpPath, fieldNames)
    an.subSpaceInds = subSpaceInds
    an.ag_commnds = {}
    an.i_info = i_info
    an.i_resolutions = i_resolutions
    # RUN ANALYSIS
    an.run()

    for res in an.resolutions: 
        for mode in an.modes:
            vals = an.vars[varName].ncos[str(res)+mode].field.vals
            vals = vals.flatten()
            vals = vals[~np.isnan(vals)] # remove mountains

            # for Temperature create anomalies
            if varName == 'zT':
                vals = vals - 300 + 0.0065*altitudes[i]

            # CREATE HISTOGRAMS
            nPoint = np.histogram(vals, bins=bins)
            freq = nPoint[0]/len(vals)
            freq[freq == 0] = np.nan
            out[res][mode][i,:] = freq
            out[res]['mask'][i,:][nPoint[0] < 10] = 0


# Difference
for res in an.resolutions: 
    raw = out[res]['']
    smo = out[res]['f']
    diff = (raw - smo)/smo
    diff[diff <= - rangeD] = - rangeD
    diff[diff >= rangeD] = rangeD
    diff[out[res]['mask'] == 0] = np.nan 
    out[res]['d'] = diff


# get unit
units = an.vars[fieldNames[0]].ncos['4.4f'].field.units

## PLOT
from matplotlib import ticker
from matplotlib import colors
lev_exp = np.arange(-8,0.01,0.2)
levels = np.power(10, lev_exp)
levelsDiff = ticker.MaxNLocator(nbins=30).tick_values(-rangeD, rangeD)
fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(10,10))
modeNames = ['smoothed', 'raw', '(raw-smoth.)/smoth.']
for modeInd,mode in enumerate(['f','','d']):
    for resInd,res in enumerate(an.resolutions):
        # ABSOLUTE VALUES
        ax = axes[modeInd,resInd]
        if mode in ['', 'f']:
            CF = ax.contourf(binsCentred, altitudes, out[res][mode],
                            levels=levels, norm=colors.LogNorm(), cmap='jet')
        else:
            CFD = ax.contourf(binsCentred, altitudes, out[res][mode],
                            levels=levelsDiff, cmap='seismic')

        title = ''
        if modeInd == 2:
            ax.set_xlabel(varName[1:]+' '+units)
        elif modeInd == 0:
            title = title + ' ' + res
        if resInd == 0:
            ax.set_ylabel('altitude [m]')
            title = title + ' ' + modeNames[modeInd]
        ax.set_title(title)
        #ax.set_xlim((binMin,binMax))
        ##ax.set_ylim((1E0,1E5))
        #ax.grid()

# COLORBARS
cax = fig.add_axes([0.9, 0.38, 0.03, 0.55]) # left, bot, width, height
caxD = fig.add_axes([0.9, 0.08, 0.03, 0.22]) # left, bot, width, height
CB = plt.colorbar(mappable=CF, cax=cax,
            orientation='vertical')
CBD = plt.colorbar(mappable=CFD, cax=caxD,
            orientation='vertical')

plt.suptitle(varName[1:]+' Frequency Distribution')
plt.subplots_adjust(left=0.07, right=0.88, top=0.92, bottom=0.08, wspace=0.27, hspace=0.33)
if i_plot == 2:
    outName = varName[1:]+'_freqDist_vProf.png'
    plt.savefig(outPath + outName)
elif i_plot == 1:
    plt.show()
plt.close(fig)
