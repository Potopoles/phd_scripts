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
altInds = [20,30,40,50,60,61]

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
#endTime = datetime(2006,7,12,23)
subSpaceInds['time'] = [startTime,endTime] # border values
#subSpaceInds['diurnal'] = [10] # list values
#subSpaceInds['diurnal'] = list(range(0,24)) 
for startHght in altInds:
    print('##########################################    ' + str(startHght))
    #startHght = 40
    endHght = startHght 
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
    an = analysis.analysis(inpPath, fieldNames)

    an.subSpaceInds = subSpaceInds
    an.ag_commnds = ag_commnds
    an.i_info = i_info
    an.i_resolutions = i_resolutions

    # RUN ANALYSIS
    an.run()

    if startHght > 60:
        altitude = 6000 + (startHght-60)*1000
    else:
        altitude = startHght*100

    an.vars['zQC'].setValueLimits()
    binMin = 0
    binMax = an.vars['zQC'].max
    nbins = 50
    outPath = '../00_plots/08_cloud_cluster/'

    bins = np.linspace(binMin,binMax,num=nbins)
    #print(bins)
    binsCentred = bins[0:(len(bins)-1)] + np.diff(bins)/2
    #print(binsCentred)
    #quit()
    freqs = []
    nPoints = []
    outRess = []
    outModes = []

    for res in an.resolutions: 
        for mode in an.modes:
            vals = an.vars['zQC'].ncos[str(res)+mode].field.vals
            vals = vals.flatten()
            vals = vals[~np.isnan(vals)] # remove mountains

            # CREATE HISTOGRAMS
            nPoint = np.histogram(vals, bins=bins)
            nPoints.append(nPoint[0]) 
            freq = nPoint[0]/len(vals)
            freqs.append(freq)
            outRess.append(str(res))
            outModes.append(mode)


    ### PLOT ALL RESS TOGETHER
    fig = plt.figure(figsize=(6,7))
    handles = []
    labels = []
    for i in range(0,len(freqs)):
        if outModes[i] == 'f':
            lstyle = '--'
        else:
            lstyle = '-'
        line, = plt.semilogy(binsCentred, freqs[i], lstyle) 
        handles.append(line)
        labels.append(outRess[i]+outModes[i])
    plt.legend(handles, labels)
    plt.xlabel('QC [kg/kg]')
    plt.ylabel('relative frequency')
    plt.xlim((binMin,binMax))
    plt.ylim((1E-8,1E0))
    plt.title('QC Frequency Distribution at Altitude '+str(altitude))
    plt.grid()
    if i_plot == 2:
        outName = 'QC_dist_alt_'+str(altitude)+'.png'
        plt.savefig(outPath + outName)
    elif i_plot == 1:
        plt.show()
    plt.close(fig)



    ### PLOT RES SEPARATELY AND DIFFERENCE BETWEEN MODES
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(11,7))
    for i in range(0,len(an.resolutions)):
        # ABSOLUTE VALUES
        ax = axes[0,i]
        lineRaw, = ax.semilogy(binsCentred, freqs[i*2+1], '-') 
        lineSmoothed, = ax.semilogy(binsCentred, freqs[i*2], '--') 
        ax.legend([lineRaw, lineSmoothed], ['raw','smoothed'])
        ax.set_xlabel('QC [kg/kg]')
        ax.set_ylabel('relative frequency')
        ax.set_xlim((binMin,binMax))
        #ax.set_ylim((1E0,1E5))
        ax.grid()
        ax.set_title(str(an.resolutions[i]))


        # MASKING OF VALUES WITH SMALL NUMBER OF SAMPLES 
        minSamples = 100
        nRaw = nPoints[i*2+1]
        nSmooth = nPoints[i*2]
        mask = np.full(len(nRaw),1)
        mask[nRaw < minSamples] = 0
        mask[nSmooth < minSamples] = 0

        # DIFFERENCE 
        ax = axes[1,i]
        raw = freqs[i*2+1]
        sm = freqs[i*2]
        raw[raw == 0] = np.nan
        sm[sm == 0] = np.nan
        ratio = (raw - sm)/sm
        ratio[mask == 0] = np.nan
        line, = ax.plot(binsCentred, ratio, '-', color='darkgreen') 
        ax.axhline(y=0, color='k', lineWidth=0.5)
        ax.set_xlabel('QC [kg/kg]')
        ax.set_ylabel('(raw-smoothed)/smoothed')
        ax.set_ylim((-1,1))
        ax.set_xlim((binMin,binMax))
        ax.grid()
        ax.set_title(str(an.resolutions[i]))
    plt.suptitle('QC Frequency Distribution at Altitude '+str(altitude))
    plt.subplots_adjust(left=0.07, right=0.95, top=0.92, bottom=0.08, wspace=0.27, hspace=0.33)
    if i_plot == 2:
        outName = 'QC_dist_and_diff_alt_'+str(altitude)+'.png'
        plt.savefig(outPath + outName)
    elif i_plot == 1:
        plt.show()
    plt.close(fig)
