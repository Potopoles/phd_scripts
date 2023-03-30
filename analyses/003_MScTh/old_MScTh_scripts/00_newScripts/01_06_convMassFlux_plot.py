from datetime import datetime, timedelta
import numpy as np
import os
os.chdir('00_newScripts/')

from functions import loadObj 

ress = ['4.4', '2.2', '1.1']
modes = ['f', '']
i_plot = 3

plotOutDir = '../00_plots/01_domAv_Fields/domain_Alpine_Region/'
#plotOutDir = '../00_plots/01_domAv_Fields/domain_Northern_Italy/'
plotName = 'mass_flux'
#plotName = 'mass_flux_NI'
if not os.path.exists(plotOutDir):
    os.mkdir(plotOutDir)
modeNames = ['SM','RAW']


import matplotlib
if i_plot == 2:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt


folder = '../06_bulk'
#name = 'convective_mass_flux_Alpine_Region'
name = 'convective_mass_flux_Alpine_Region_1ms_threshold'
#name = 'convective_mass_flux_Northern_Italy'
#levels = np.arange(0.001,0.0360,0.002)
levels = np.arange(0.001,0.0145,0.0005)
obj = loadObj(folder,name)


out = {}
out['hrs'] = np.arange(0,25)
hrs = np.arange(0,24)
for res in ress:
    for mode in modes[0:2]:
        hrVals = np.full((65,25), np.nan)
        for hr in hrs:
            inds = [i for i in range(0,len(obj['times'])) if obj['times'][i].hour == hr]
            hrVals[:,hr] = np.mean(obj[res+mode][:,inds],1)
        hrVals[:,24] = hrVals[:,0] 
        out[res+mode] = hrVals

hrs = np.arange(0,25)
alts = list(range(0,6001,100))
alts.extend(list(range(7000,10001,1000)))

# PLOT
MAG = 1.
ncols = 3
nrows = 2
stretchCol = 5*MAG
stretchRow = 4.1*MAG
fig, axes = plt.subplots(ncols=ncols, nrows=nrows,
                                figsize=(ncols*stretchCol,nrows*stretchRow))


for rI,mode in enumerate(modes):
    for cI,res in enumerate(ress):
        ax = axes[rI,cI]
        vals = out[res+mode]
        CF = ax.contourf(hrs, alts,vals, levels=levels,
                                cmap='YlOrRd')
        ax.grid()
        if rI == 1:
            ax.set_xlabel('hour')
        if cI == 0:
            ax.set_ylabel('altitude [m]')
        ax.set_xticks([0,6,12,18,24])
        ax.set_title(modeNames[rI]+str(res))


# COLORBAR
cPosBot = 0.08
cHeight = 0.03
xPosLeft = 0.25
width = 0.5
cax = fig.add_axes([xPosLeft, cPosBot, width, cHeight])
MCB = plt.colorbar(mappable=CF, cax=cax,
            orientation='horizontal')
cax.tick_params(labelsize=9*MAG)
MCB.set_label('Convective Mass Flux $[kg$ $m^{-2}$ $s^{-1}]$')
fig.subplots_adjust(wspace=0.15, hspace=0.3,
        left=0.07, right=0.96, bottom=0.20, top=0.90)

if i_plot == 1:
    plt.show()
    plt.close(fig)
elif i_plot == 2:
    plotPath = plotOutDir + '/' + plotName + '.png'
    plt.savefig(plotPath, format='png', bbox_inches='tight')
    plt.close(fig)
elif i_plot == 3:
    plotPath = plotOutDir + '/' + plotName + '.pdf'
    plt.savefig(plotPath, format='pdf', bbox_inches='tight')
    plt.close(fig)

    
