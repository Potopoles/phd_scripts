from datetime import datetime, timedelta
import numpy as np
import os
os.chdir('00_newScripts/')

from functions import loadObj 

ress = ['4.4', '2.2', '1.1']
#ress = ['4.4', '2.2']
#ress = ['4.4']
modes = ['f', '', 'd']
#i_variables = 'QV' # 'QV' or 'T'
#i_variables = 'T' # 'QV' or 'T'
i_plot = 1

region = 'Alpine_Region'
#region = 'Northern_Italy'
altitudes = '0_2500'
#altitudes = '0_1000'
#altitudes = '2500_8000'
#altitudes = '2500_6000'
path = 'alts_'+altitudes+'_'+region
folder = '../06_bulk/vertSlab/' + path
plotOutDir = '../00_plots/06_bulk'
if not os.path.exists(plotOutDir):
    os.mkdir(plotOutDir)

modeNames = ['SM', 'RAW', 'RAW - SM']

i_walls = ['left', 'right', 'top', 'bottom']
i_walls = ['bottom', 'top']
i_MODE = 'SUM'
#i_MODE = 'left'

if i_MODE == 'SUM':
    plotName = 'vertSlab_'+path+'_all'
else:
    plotName = 'vertSlab_'+path+'_'+i_MODE

import matplotlib
if i_plot == 2:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

var = 'Fqv' 
titleVar = 'WV Flux'
#unit = r'Vapor Flux $[10^6$ $kg$ $s^{-1}]$'
unit = r'Vapor Flux $[mm$ $h^{-1}]$'

colrs = [(0,0,0), (0,0,1), (1,0,0)]
labelsize = 12
titlesize = 14

Area = None

# PREAPRE DATA FOR PLOTTING
out = {}
out['hrs'] = np.arange(0,25)
max = -np.Inf
min = np.Inf
for res in ress:
    for mode in modes[0:2]:
        if i_MODE == 'SUM':
            vals = None
            for i_wall in i_walls:
                name = var+'_'+i_wall+'_'+res+mode
                obj = loadObj(folder,name)  
                if res == '4.4' and Area is None:
                    #print(obj)
                    Area = obj['Area']*1E6
                if vals is None:
                    #vals = obj[var]/1E6
                    vals = obj[var]/Area*3600
                else:
                    #vals = vals + obj[var]/1E6
                    #if (i_wall == 'top') or (i_wall == 'bottom'):
                    #    vals = vals + obj[var]/Area*3600
                    #else:
                    vals = vals + obj[var]/Area*3600
        else:
            name = var+'_'+i_MODE+'_'+res+mode
            obj = loadObj(folder,name)  
            vals = obj[var]/1E6

        dates = obj['time'].astype(datetime)

        # MEAN DIURNAL
        #vals = obj[var]
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
    increase = np.abs(max-min)*0.03
    max = max+increase
    min = min-increase
    out[res+'d'] = out[res+''] - out[res+'f']
    maxd = np.max(out[res+'d'])
    mind = np.min(out[res+'d'])
    max = np.max(out[res+'d']) if np.max(out[res+'d']) > max else max
    min = np.min(out[res+'d']) if np.min(out[res+'d']) < min else min
    #min = -40
    #max = 30
    min = -0.4
    max = 0.3


# PLOT
fig,axes = plt.subplots(1,3, figsize=(11,4))
for axI,mode in enumerate(modes):
    ax = axes[axI]
    lines = []
    for resI,res in enumerate(ress):
        line, = ax.plot(out['hrs'], out[res+mode], color=colrs[resI])
        lines.append(line)

    if axI == 0:
        ax.legend(lines, labels=ress)
    ax.axhline(y=0, color='k', lineWidth=1)
    ax.set_xticks([0,6,12,18,24])
    ax.set_xlim((0,24))
    ax.set_xlabel('Hour',fontsize=labelsize)
    if axI == 0:
        ax.set_ylabel(unit,fontsize=labelsize)
    if mode != 'd':
        ax.set_ylim((min,max))
    else:
        #centre = (max + min)*0.5
        #centred = (maxd + mind)*0.5
        #d = centred - centre
        #ax.set_ylim((min+d, max+d))
        ax.set_ylim((min,max))
    ax.grid()
    ax.set_title(modeNames[axI],fontsize=titlesize)


#if i_MODE == 'SUM':
#    fig.suptitle(titleVar + ' into '+ obj['domainName'] + ' through all sidewalls between ' + altitudes + ' m.')
#else:
#    fig.suptitle(titleVar + ' into '+ obj['domainName'] + ' through '+i_MODE+' sidewall between ' + altitudes + ' m.')
fig.subplots_adjust(wspace=0.23,
        left=0.07, right=0.95, bottom=0.15, top=0.85)

if i_plot == 1:
    plt.show()
    plt.close(fig)
elif i_plot == 2:
    plotPath = plotOutDir + '/' + plotName+'.png'
    plt.savefig(plotPath, format='png', bbox_inches='tight')
    plt.close(fig)
elif i_plot == 3:
    plotPath = plotOutDir + '/' + plotName+'.pdf'
    plt.savefig(plotPath, format='pdf', bbox_inches='tight')
    plt.close('all')

    
