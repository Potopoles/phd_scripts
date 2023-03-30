# Calculate domain Average Precipitation
# author: Christoph Heim
# date: 21 10 2017
#################################
import os
os.chdir('00_scripts/')

i_resolutions = 5 # 1 = 4.4, 2 = 4.4 + 2.2, 3 = ...
i_plot = 2 # 0 = no plot, 1 = show plot, 2 = save plot
i_info = 2 # output some information [from 0 (off) to 5 (all you can read)]

labelsize = 17
timelabelsize = 25
titlesize = 23

import matplotlib
if i_plot == 2:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt


import ncClasses.analysis as analysis
from datetime import datetime
from functions import *
####################### NAMELIST INPUTS FILES #######################
# directory of input model folders
inpPath = '../02_fields/topocut'
#fieldNames = ['cHSURF', 'nTOT_PREC', 'nU_10M', 'nV_10M']
fieldNames = ['cHSURF', 'nTOT_PREC', 'nU_10M']
#####################################################################		
#startDateTime = datetime(2006,7,12,15)
#plotLabel = '12.1500'
startDateTime = datetime(2006,7,12,19)
plotLabel = '12.1900'
nts = 4
import datetime
#dtlist = [startDateTime + datetime.timedelta(hours=x) for x in range(0,nts)]


####################### NAMELIST DIMENSIONS #######################
subDomain = 2 # 0: full domain, 1: alpine region, 2: zoom in
# SUBSPACE
subSpaceIndsIN = {}
if subDomain == 1: # alpine region
    subSpaceIndsIN['rlon'] = [50,237]
    subSpaceIndsIN['rlat'] = [41,155]
elif subDomain == 2: # italy region
    subSpaceIndsIN['rlon'] = [80,180]
    subSpaceIndsIN['rlat'] = [50,120]
#subSpaceIndsIN['altitude'] = (altInd, altInd+1)
startTime = startDateTime
endTime = startTime + datetime.timedelta(hours=nts)
subSpaceIndsIN['time'] = [startTime,endTime]
#####################################################################

####################### NAMELIST AGGREGATE #######################
# Options: MEAN, SUM, DIURNAL
ag_commnds = {}
#ag_commnds['rlat'] = 'MEAN'
#ag_commnds['rlon'] = 'MEAN'
#####################################################################

####################### NAMELIST PLOT #######################
nDPlot = 2 # How many dimensions should plot have (1 or 2)
i_diffPlot = 0 # Draw plot showing difference filtered - unfiltered # TODO
plotOutDir = '../00_plots/04_coldPools/coldPool_evolution'
import os
if not os.path.exists(plotOutDir):
    os.makedirs(plotOutDir)
#hrStr = '{num:02d}'.format(num=hour)
dtStr = format(startTime,'%d_%H') 
plotName = '1.1_timeseries_'+plotLabel


an = analysis.analysis(inpPath, fieldNames)

an.subSpaceInds = subSpaceIndsIN
an.ag_commnds = ag_commnds
an.i_info = i_info
an.i_resolutions = i_resolutions

# RUN ANALYSIS
an.run()



import matplotlib
if i_plot == 2:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

widthStretch = 13.8
heightStretch = 6*nts
fig, axes = plt.subplots(nts, 2, figsize=(widthStretch,heightStretch))

dts = an.vars['nU_10M'].ncos[an.resolutions[0]].dims['time'].vals
for mI,mode in enumerate(an.modes):
    for tI,dt in enumerate(dts):
        ax = axes[tI,mI]
        ax.axis('equal')

        topo = an.vars['cHSURF'].ncos[an.resolutions[0]+mode]
        dimx = topo.dims['rlon']
        dimy = topo.dims['rlat']
        tTicks = np.array([-100,0,100,200,500,1000,1500,2000,2500,3000,3500,4000])
        ax.contourf(dimx.vals, dimy.vals, topo.field.vals, tTicks,
            cmap='binary', alpha=0.7)

        wind = an.vars['nU_10M'].ncos[an.resolutions[0]+mode].field.vals[tI,:,:]
        wind[np.abs(wind) < 2] = np.nan
        Mticks = [-16,-14,-12,-10,-8,-6,-4,-2,2,4,6,8,10,12,14,16.1]
        CF = ax.contourf(dimx.vals, dimy.vals, wind.squeeze(), Mticks,
            cmap='seismic', alpha=0.7)

        rain = an.vars['nTOT_PREC'].ncos[an.resolutions[0]+mode].field.vals[tI,:,:]
        Mticks = [5]
        ax.contour(dimx.vals, dimy.vals, rain.squeeze(), Mticks, linewidths=3,
                    colors=('green'))

        if tI == 0:
            ax.set_title(an.modeNames[mI]+an.resolutions[0],fontsize=titlesize)

        ax.text(700,228,dt.strftime('%H:00'),size=timelabelsize)

        if tI == nts-1:
            ax.set_xlabel('x $[km]$',fontsize=labelsize)
        if mI == 0:
            ax.set_ylabel('y $[km]$',fontsize=labelsize)

        # colorbar
        xPosLeft = 0.10
        cPosBot = 0.05
        width = 0.80
        cHeight = 0.02
        cax = fig.add_axes([xPosLeft, cPosBot, width, cHeight])
        MCB = plt.colorbar(mappable=CF, cax=cax, orientation='horizontal')
        cax.tick_params(labelsize=labelsize)
        MCB.set_label('u wind at 10m $[m$ $s^{-1}]$',fontsize=labelsize)


        fig.subplots_adjust(wspace=0.10, hspace=0.17,
                left=0.07, right=0.96, bottom=0.11, top=0.88)

if i_plot == 1:
    plt.show()
elif i_plot == 2:
    plotPath = plotOutDir + '/' + plotName+'.png'
    plt.savefig(plotPath, format='png', bbox_inches='tight')

          
quit()




    

