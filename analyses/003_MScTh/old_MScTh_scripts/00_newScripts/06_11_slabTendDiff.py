from datetime import datetime, timedelta
import numpy as np
import os
os.chdir('00_newScripts/')

from functions import loadObj 

ress = ['4.4', '2.2', '1.1']
#ress = ['4.4', '2.2']
#ress = ['4.4']
#modes = ['f', '', 'd']
modes = ['f']
#i_variables = 'QV' # 'QV' or 'T'
#i_variables = 'T' # 'QV' or 'T'
i_plot = 1

region = 'Alpine_Region'
alt1 = '2500'
alt2 = '6000'

region = 'Alpine_Region'
alt1 = '4000'
#alt2 = '6000'

inpPath1 = 'alt_'+alt1+'_'+region
inpPath2 = 'alt_'+alt2+'_'+region
folder1 = '../06_bulk/horSlab/' + inpPath1
folder2 = '../06_bulk/horSlab/' + inpPath2
plotOutDir = '../00_plots/06_bulk'
if not os.path.exists(plotOutDir):
    os.mkdir(plotOutDir)
plotName = 'horSlab_diff_'+alt2+'_'+alt1+'_'+region+'.png'

modeNames = ['smoothed', 'raw', 'raw - smoothed']


import matplotlib
if i_plot == 2:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

var = 'Fqv' 
titleVar = 'WV Flux'
unit = 'Fqv [1E9*kg/h]'


# PREAPRE DATA FOR PLOTTING
out = {}
out['hrs'] = np.arange(0,25)
max = -np.Inf
min = np.Inf
for res in ress:
    for mode in modes[0:2]:
        name = var+'_'+res+mode
        obj = loadObj(folder1,name)  
        vals1 = obj[var]/1E9*3600
        name = var+'_'+res+mode
        obj = loadObj(folder2,name)  
        vals2 = obj[var]/1E9*3600

        vals = vals1 - vals2

        dates = obj['time'].astype(datetime)

        # MEAN DIURNAL
        hrs = np.arange(0,24)
        hrVals = np.full(len(hrs), np.nan)
        for hr in hrs:
            inds = [i for i in range(0,len(dates)) if dates[i].hour == hr]
            hrVals[hr] = np.mean(vals[inds])

        hrVals = np.append(hrVals, hrVals[0])
        out[res+mode] = hrVals
        max = np.max(hrVals) if np.max(hrVals) > max else max
        min = np.min(hrVals) if np.min(hrVals) < min else min
    
    # CALCUALTE DIFFERENCE
    out[res+'d'] = out[res+''] - out[res+'f']
    maxd = np.max(out[res+'d'])
    mind = np.min(out[res+'d'])
    max = np.max(out[res+'d']) if np.max(out[res+'d']) > max else max
    min = np.min(out[res+'d']) if np.min(out[res+'d']) < min else min


# PLOT
fig,axes = plt.subplots(1,3, figsize=(14,5))
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

    #xtxt = 18
    #ytxt = max - 0.2*(max-min) 
    #ax.text(xtxt, ytxt, 'yolo')


fig.suptitle(titleVar + 'vertical budget between slabs at '+alt1+' and '+alt2 + 'm over ' +  obj['domainName'])
fig.subplots_adjust(wspace=0.4,
        left=0.10, right=0.95, bottom=0.15, top=0.85)

if i_plot == 1:
    plt.show()
    plt.close(fig)
elif i_plot == 2:
    plotPath = plotOutDir + '/' + plotName
    plt.savefig(plotPath, format='png', bbox_inches='tight')
    plt.close(fig)

    
