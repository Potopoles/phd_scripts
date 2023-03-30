from datetime import datetime, timedelta
import numpy as np
import os
os.chdir('00_newScripts/')

from functions import loadObj 

ress = ['4.4', '2.2', '1.1']
#ress = ['4.4', '2.2']
#ress = ['4.4']
modes = ['f', '', 'd']

i_plot = 1

hydrometeors = ['zQC', 'zQI', 'zQV', 'zQR', 'zQS', 'zQG']
TTendencies=['zATT_MIC','zATT_RAD','zATT_ADV','zATT_ZADV','zATT_TURB','zATT_TOT','zATT_HADV']
QVTendencies=['zAQVT_MIC','zAQVT_ADV','zAQVT_ZADV','zAQVT_TURB','zAQVT_TOT','zAQVT_HADV']
dynamics = ['zW', 'zU', 'zV', 'zT', 'zP', 'zRH']

fieldNames = ['zATT_MIC', 'zQI', 'zW']
fieldNames = ['zW', 'zQC']
fieldNames =['zQV', 'zQS', 'zQG']
 
region = 'Alpine_Region'
alt0 = '8000'
#alt0 = '1000'
alt1 = '10000'
#alt1 = '1900'

path = 'alts_'+alt0+'_'+alt1+'_'+region
folder = '../06_bulk/' + path
plotOutDir = '../00_plots/06_bulk/'+path
if not os.path.exists(plotOutDir):
    os.mkdir(plotOutDir)
modeNames = ['SM', 'RAW', 'RAW - SM']

import matplotlib
if i_plot == 2:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

for fieldName in fieldNames:
    print('######## '+fieldName+' ########')

    plotName = fieldName + '.png'

    # PREAPRE DATA FOR PLOTTING
    out = {}
    out['hrs'] = np.arange(0,25)
    max = -np.Inf
    min = np.Inf
    for res in ress:
        for mode in modes[0:2]:
            name = fieldName
            obj = loadObj(folder,name)  

            dates = obj['time'].astype(datetime)

            # MEAN DIURNAL
            vals = obj[res+mode]
            hrs = np.arange(0,24)
            hrVals = np.full(len(hrs), np.nan)
            for hr in hrs:
                inds = [i for i in range(0,len(dates)) if dates[i].hour == hr]
                hrVals[hr] = np.mean(vals[inds])
            hrVals = np.append(hrVals, hrVals[0])
            out[res+mode] = hrVals

            # calc max min
            vals = out[res+mode]
            max = np.max(vals) if np.max(vals) > max else max
            min = np.min(vals) if np.min(vals) < min else min

        
        # CALCUALTE DIFFERENCE
        out[res+'d'] = out[res+''] - out[res+'f']
        maxd = np.max(out[res+'d'])
        mind = np.min(out[res+'d'])
        max = np.max(out[res+'d']) if np.max(out[res+'d']) > max else max
        min = np.min(out[res+'d']) if np.min(out[res+'d']) < min else min



    # PLOT
    fig,axes = plt.subplots(1,3, figsize=(12,5))
    for axI,mode in enumerate(modes):
        ax = axes[axI]
        lines = []
        for resI,res in enumerate(ress):
            line, = ax.plot(out['hrs'], out[res+mode])
            lines.append(line)

        ax.legend(lines, labels=ress)
        ax.axhline(y=0, color='k', lineWidth=1)
        ax.set_xticks([0,6,12,18,24])
        ax.set_xlim((0,24))

        unit = obj['units']
        ax.set_ylabel(unit)
        if mode != 'd':
            ax.set_ylim((min,max))
        else:
            centre = (max + min)*0.5
            centred = (maxd + mind)*0.5
            d = centred - centre
            ax.set_ylim((min+d, max+d))
        #ax.set_ylim((min,max))
        ax.grid()
        ax.set_title(modeNames[axI])


    fig.suptitle(fieldName[1:] + ' ' + path)
    fig.subplots_adjust(wspace=0.4,
            left=0.10, right=0.95, bottom=0.15, top=0.85)

    if i_plot == 1:
        plt.show()
        plt.close(fig)
    elif i_plot == 2:
        plotPath = plotOutDir + '/' + plotName
        plt.savefig(plotPath, format='png', bbox_inches='tight')
        plt.close(fig)

        
