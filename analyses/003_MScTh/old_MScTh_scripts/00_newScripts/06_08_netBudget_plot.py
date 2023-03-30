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
wallAlts = '0_2500'
slab2Alt = '2500'

#region = 'Alpine_Region'
#wallAlts = '2500_6000'
#slab1Alt = '2500'
#slab2Alt = '6000'

#region = 'Alpine_Region'
#wallAlts = '4500_6000'
#slab1Alt = '4500'
#slab2Alt = '6000'

#region = 'Northern_Italy'
#wallAlts = '0_2500'
#slab2Alt = '2500'

plotOutDir = '../00_plots/06_bulk'

# WALL
path = 'alts_'+wallAlts+'_'+region
wallFolder = '../06_bulk/vertSlab/' + path

plotName = 'netBudget_'+path+'.png'

# HORIZONTAL SLAB BELOW
if 'slab1Alt' in locals():
    path = 'alt_'+slab1Alt+'_'+region
    slab1Folder = '../06_bulk/horSlab/' + path
    print('slab1')

# HORIZONTAL SLAB ABOVE
if 'slab2Alt' in locals():
    path = 'alt_'+slab2Alt+'_'+region
    slab2Folder = '../06_bulk/horSlab/' + path
    print('slab2')

modeNames = ['smoothed', 'raw', 'raw - smoothed']

i_walls = ['left', 'right', 'top', 'bottom']

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

        # VERTICAL WALL
        vertVals = None
        for i_wall in i_walls:
            name = var+'_'+i_wall+'_'+res+mode
            obj = loadObj(wallFolder,name)  
            if vertVals is None:
                vertVals = obj[var]/1E9*3600
            else:
                vertVals = vertVals + obj[var]/1E9*3600

        vals = vertVals

        # HORIZONTAL SLAB BELOW
        if 'slab1Folder' in locals():
            name = var+'_'+res+mode
            obj = loadObj(slab1Folder,name)  
            horVals = obj[var]/1E9*3600
            vals = vals + horVals


        # HORIZONTAL SLAB ABOVE
        if 'slab2Folder' in locals():
            name = var+'_'+res+mode
            obj = loadObj(slab2Folder,name)  
            horVals = obj[var]/1E9*3600
            vals = vals - horVals


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


fig.suptitle(titleVar + ' net balance in ' + obj['domainName'] +' between ' + wallAlts + ' m.')
fig.subplots_adjust(wspace=0.4,
        left=0.10, right=0.95, bottom=0.15, top=0.85)

if i_plot == 1:
    plt.show()
    plt.close(fig)
elif i_plot == 2:
    plotPath = plotOutDir + '/' + plotName
    plt.savefig(plotPath, format='png', bbox_inches='tight')
    plt.close(fig)

    
