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
addLabel = '_HOR'
#addLabel = ''

#region = 'Alpine_Region'
#wallAlts = '2500_6000'
#slab1Alt = '2500'
#slab2Alt = '6000'

#region = 'Alpine_Region'
#wallAlts = '0_2500'
#slab2Alt = '2500'

#region = 'Alpine_Region'
#wallAlts = '4500_6000'
#slab1Alt = '4500'
#slab2Alt = '6000'

#region = 'South_Western_Alps'
#wallAlts = '0_2500'
#slab2Alt = '2500'

#region = 'South_Western_Alps'
#wallAlts = '3000_4000'
#slab1Alt = '3000'
#slab2Alt = '4000'

region = 'Alpine_Region'
#region = 'Northern_Italy'
#wallAlts = '2500_8000'
#wallAlts = '0_2000'
wallAlts = '0_2500'

# WALL
path = 'alts_'+wallAlts+'_'+region
wallFolder = '../06_bulk/vertSlab/' + path
plotName = 'fluxes_summary_'+path+addLabel+'.png'

# HORIZONTAL SLAB BELOW
if 'slab1Alt' in locals():
    path = 'alt_'+slab1Alt+'_'+region
    slab1Folder = '../06_bulk/horSlab/' + path

# HORIZONTAL SLAB ABOVE
if 'slab2Alt' in locals():
    path = 'alt_'+slab2Alt+'_'+region
    slab2Folder = '../06_bulk/horSlab/' + path

modeNames = ['smoothed', 'raw', 'raw - smoothed']
i_walls = ['left', 'right', 'top', 'bottom']

if 'slab1Alt' in locals():
    if 'slab2Alt' in locals():
        allKeys = ['left', 'right', 'top', 'bottom', 'HOR', 'slab1', 'slab2', 'NET']
    else:
        allKeys = ['left', 'right', 'top', 'bottom', 'HOR', 'slab1', 'NET']
else:
    if 'slab2Alt' in locals():
        allKeys = ['left', 'right', 'top', 'bottom', 'HOR', 'slab2', 'NET']
    else:
        allKeys = ['left', 'right', 'top', 'bottom', 'HOR']




import matplotlib
if i_plot == 2:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

var = 'Fqv' 
titleVar = 'WV Flux'
#unit = 'Fqv [1E9*kg/h]'
unit = 'Fqv $[mm$ $h^{-1}]$'

Area = None


# PREAPRE DATA FOR PLOTTING
out = {}
out['hrs'] = np.arange(0,25)
max = -np.Inf
min = np.Inf
maxd = -np.Inf
mind = np.Inf
for res in ress:
    for mode in modes[0:2]:
        all = {}
        for i_wall in i_walls:
            name = var+'_'+i_wall+'_'+res+mode
            obj = loadObj(wallFolder,name)  

            if res == '4.4' and Area is None:
                Area = obj['Area']*1E6

            #all[i_wall] = obj[var]/1E9*3600
            all[i_wall] = obj[var]/Area*3600
        all['HOR'] = all['left'] + all['right'] + all['top'] + all['bottom']
        
        # HORIZONTAL SLAB BELOW
        if 'slab1Folder' in locals():
            name = var+'_'+res+mode
            obj = loadObj(slab1Folder,name)  
            #horVals = obj[var]/1E9*3600
            horVals = obj[var]/Area*3600
            all['slab1'] = horVals


        # HORIZONTAL SLAB ABOVE
        if 'slab2Folder' in locals():
            name = var+'_'+res+mode
            obj = loadObj(slab2Folder,name)  
            #horVals = obj[var]/1E9*3600
            horVals = obj[var]/Area*3600
            all['slab2'] = -horVals

        if 'NET' in allKeys:
            all['NET'] = all['HOR'] 
            if 'slab1Folder' in locals():
                all['NET'] =all['NET'] + all['slab1'] 
            if 'slab2Folder' in locals():
                all['NET'] =all['NET'] + all['slab2'] 




        dates = obj['time'].astype(datetime)

        # MEAN DIURNAL
        #vals = obj[var]
        hrs = np.arange(0,24)
        for key,vals in all.items():
            hrVals = np.full(len(hrs), np.nan)
            for hr in hrs:
                inds = [i for i in range(0,len(dates)) if dates[i].hour == hr]
                hrVals[hr] = np.mean(vals[inds])

            hrVals = np.append(hrVals, hrVals[0])
            out[key+'_'+res+mode] = hrVals
            max = np.max(hrVals) if np.max(hrVals) > max else max
            min = np.min(hrVals) if np.min(hrVals) < min else min


    # CALCUALTE DIFFERENCE
    for key in allKeys:
        out[key+'_'+res+'d'] = out[key+'_'+res+''] - out[key+'_'+res+'f']
        maxd = np.max(out[key+'_'+res+'d']) if np.max(
                            out[key+'_'+res+'d']) > maxd else maxd
        mind = np.min(out[key+'_'+res+'d']) if np.min(
                            out[key+'_'+res+'d']) < mind else mind
        max = np.max(key+'_'+out[res+'d']) if np.max(
                            out[key+'_'+res+'d']) > max else max
        min = np.min(key+'_'+out[res+'d']) if np.min(
                            out[key+'_'+res+'d']) < min else min


# PLOT
cols = {}
cols['left'] = 'orange'
cols['right'] = 'red'
cols['top'] = 'blue'
cols['bottom'] = 'green'
cols['HOR'] = 'purple'
cols['slab1'] = 'brown'
cols['slab2'] = 'grey'
cols['NET'] = 'black'
plotKeys = allKeys 
#plotKeys = ['SUM']
fig,axes = plt.subplots(3,3, figsize=(12,10))
for rowI,res in enumerate(ress):
    for colI,mode in enumerate(modes):
        ax = axes[rowI, colI]
        lines = []
        for kI,key in enumerate(plotKeys):
            line, = ax.plot(out['hrs'], out[key+'_'+res+mode], color=cols[key])
            lines.append(line)

        if res+mode == '4.4f':
            ax.legend(lines, labels=plotKeys)
        ax.axhline(y=0, color='k', lineWidth=1)
        ax.set_xticks([0,6,12,18,24])
        ax.set_xlim((0,24))
        ax.set_ylabel(unit)
        if mode != 'd':
            ax.set_ylim((min,max))
        else:
            #centre = (max + min)*0.5
            #centred = (maxd + mind)*0.5
            #d = centred - centre
            #ax.set_ylim((min+d, max+d))
            ax.set_ylim((mind,maxd))
        ax.grid()
        ax.set_title(modeNames[colI])


    fig.suptitle(titleVar + ' into '+ obj['domainName'] + ' through all edges between ' + wallAlts + ' m.')
fig.subplots_adjust(wspace=0.3,
        left=0.08, right=0.98, bottom=0.05, top=0.9)

if i_plot == 1:
    plt.show()
    plt.close(fig)
elif i_plot == 2:
    print('save plot')
    print(plotName)
    plotOutDir = '../00_plots/06_bulk'
    plotPath = plotOutDir + '/' + plotName
    plt.savefig(plotPath, format='png', bbox_inches='tight')
    plt.close(fig)

    
