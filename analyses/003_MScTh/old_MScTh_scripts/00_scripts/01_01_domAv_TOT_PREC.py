#################################
# Calculate domain Average Precipitation
# author: Christoph Heim
# date: 21 10 2017
#################################
import os
os.chdir('00_scripts/')

i_resolutions = 3 # 1 = 4.4, 2 = 4.4 + 2.2, 3 = ...
i_plot = 2 # 0 = no plot, 1 = show plot, 2 = save plot
i_info = 1 # output some information [from 0 (off) to 5 (all you can read)]
import matplotlib
if i_plot == 2:
	matplotlib.use('Agg')
import matplotlib.pyplot as plt


import ncClasses.analysis as analysis
from ncClasses.subdomains import setSSI
from datetime import datetime
from functions import *
####################### NAMELIST INPUTS FILES #######################
# directory of input model folders
#inpPath = '../02_fields/subDomDiur'
inpPath = '../02_fields/topocut'
inpPath = '../02_fields/diurnal'
fieldNames = ['nTOT_PREC', 'cHSURF']
#####################################################################		

####################### NAMELIST DIMENSIONS #######################
subDomain = 1 # 0: full domain, 1: alpine region, 2: zoom in
# SUBSPACE
#subSpaceIndsIN = {'4.4':{},'2.2':{},'1.1':{}}
#subSpaceIndsIN = setSSI(subDomain, subSpaceIndsIN)
subSpaceIndsIN = {}
if subDomain == 1: # alpine region
	subSpaceIndsIN['rlon'] = [50,237]
	subSpaceIndsIN['rlat'] = [41,155]
elif subDomain == 2: # zoom in subdomain
	subSpaceIndsIN['rlon'] = [95,160]
	subSpaceIndsIN['rlat'] = [60,100]
	
#subSpaceIndsIN['rlat'] = (90,91)
#subSpaceIndsIN['rlon'] = (50,237)

#startTime = datetime(2006,7,11,0)
#endTime = datetime(2006,7,19,23)
#subSpaceIndsIN['time'] = (startTime,endTime)
#startHr = 14
#endHr = 15
#subSpaceIndsIN['diurnal'] = (startHr,endHr)
#subSpaceIndsIN['altitude'] = (60,61)
#subSpaceIndsIN['altitude'] = (60,61)
#####################################################################

####################### NAMELIST AGGREGATE #######################
# Options: MEAN, SUM, DIURNAL
ag_commnds = {}
ag_commnds['rlat'] = 'MEAN'
ag_commnds['rlon'] = 'MEAN'
#ag_commnds['altitude'] = 'MEAN'
#####################################################################

####################### NAMELIST PLOT #######################
nDPlot = 1 # How many dimensions should plot have (1 or 2)
i_diffPlot = 0 # Draw plot showing difference filtered - unfiltered # TODO
plotOutDir = '../00_plots'
plotName = 'domAv_diurnal_TOT_PREC'
#plotName = 'domAv_diurnal_TOT_PREC_Northern_Italy'
##### 1D PLOT #########

##### 2D Contour ######
contourTranspose = 0 # Reverse contour dimensions?
plotContour = 0 # Besides the filled contour, also plot the contour?
cmapM = 'jet' # colormap for Model output (jet, terrain, inferno, YlOrRd)
axis = 'equal' # set 'equal' if keep aspect ratio, else 'auto'
# COLORBAR Models
autoTicks = 1 # 1 if colorbar should be set automatically
Mmask = 1 # Mask Model values lower than MThrMinRel of maximum value?
MThrMinRel = 0.15 # Relative amount of max value to mask (see Mmask)
Mticks = [0.0001,0.0002,0.0003,0.0004,0.0005]
# COLORBAR Models
cmapD = 'bwr' # colormap for Difference output (bwr)
#####################################################################


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



if i_info >= 3:
	print('plotting')
mainVar = an.vars[an.varNames[0]]
someField = next(iter(mainVar.ncos.values())).field
print('NONSINGLETONS: ' + str(someField.nNoneSingleton))

if nDPlot == 2 and someField.nNoneSingleton == 2:
	ncs.contourTranspose = contourTranspose
	ncs.plotContour = plotContour
	ncs.cmapM = cmapM
	ncs.axis = axis
	ncs.autoTicks = autoTicks
	ncs.Mmask = Mmask
	ncs.MThrMinRel = MThrMinRel
	ncs.Mticks = Mticks
	ncs.cmapD = cmapD

	if 'cHSURF' in an.fieldNames:
		ncs.plotTopo(an.vars['cHSURF'])
	
	for fldName in an.fieldNames:
		if fldName != 'cHSURF':
			ncs.plotVar(an.vars[fldName])
			ncs.cmapM = 'terrain'
		
elif nDPlot == 1 and someField.nNoneSingleton == 1:
    import ncPlots.ncSubplots1D as ncSubplots
    ncs = ncSubplots.ncSubplots(an, nDPlot, i_diffPlot, 'HOR')

    for varName in an.varNames:
        if varName != 'cHSURF':
            ncs.plotVar(an.vars[varName])

else:
	raise ValueError('ERROR: CANNOT MAKE ' + str(nDPlot) + 'D-PLOT WITH ' +
	str(someField.nNoneSingleton) + ' NON-SINGLETON DIMS!')

# PRECIP MEAN DAILY SUM
x = 1
yTop = 0.85
dy = 0.12
size = 12
for rowInd,mode in enumerate(an.modes):
    if ncs.orientation == 'VER':
        ax = ncs.axes[rowInd,0]
    elif ncs.orientation == 'HOR':
        ax = ncs.axes[0,rowInd]
    if mode != 'D':
        ax.text(x, yTop+dy, 'Sum:', size=size,
                bbox=dict(boxstyle='square',ec=(1,1,1,0.5),fc=(1,1,1,0.5)))
    # PLOT ADJUSTMENTS
    ax.set_xlabel('Hour',fontsize=12)
    if mode == '':
        #ax.legend_.remove()
        ax.set_ylabel('',fontsize=12)
    else:
        ax.set_ylabel(r'Rain Rate $[mm$ $h^{-1}]$',fontsize=12)
    ax.set_ylim(0,1.7)
    for rI,res in enumerate(ncs.ress):
        # GET VALUES AND DIMENSIONS				
        fld = an.vars['nTOT_PREC'].ncos[str(res+mode)].field
        if mode != 'd':
            sum = str(round(np.sum(fld.vals),1)) + ' mm' 
            ax.text(x, yTop-dy*rI, sum, color=ncs.colrs[rI], size=size,
                    bbox=dict(boxstyle='square',ec=(1,1,1,0.5),fc=(1,1,1,0.5)))
        
	
if i_plot == 1:
	plt.show()
elif i_plot == 2:
    plotPath = plotOutDir + '/' + plotName+'.png'
    plt.savefig(plotPath, format='png', bbox_inches='tight')
    plt.close('all')
elif i_plot == 3:
    plotPath = plotOutDir + '/' + plotName+'.pdf'
    plt.savefig(plotPath, format='pdf', bbox_inches='tight')
    plt.close('all')

		  


