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
from datetime import datetime
from functions import *
####################### NAMELIST INPUTS FILES #######################
# directory of input model folders
inpPath = '../02_fields/result'
#fieldNames = ['zQC', 'nHPBL', 'cHSURF']
fieldNames = ['cHSURF', 'zQC']
fieldNames = ['nHPBL', 'cHSURF']
#####################################################################		

####################### NAMELIST DIMENSIONS #######################
subDomain = 1 # 0: full domain, 1: alpine region, 2: zoom in
# SUBSPACE
subSpaceIndsIN = {}
if subDomain == 1: # alpine region
	subSpaceIndsIN['rlon'] = (50,237)
	subSpaceIndsIN['rlat'] = (41,155)
elif subDomain == 2: # zoom in subdomain
	subSpaceIndsIN['rlon'] = (70,100)
	subSpaceIndsIN['rlat'] = (70,100)

startTime = datetime(2006,7,11,0)
endTime = datetime(2006,7,11,23)
subSpaceIndsIN['time'] = (startTime,endTime)

subSpaceIndsIN['altitude'] = (60,61)
#####################################################################

####################### NAMELIST AGGREGATE #######################
# Options: MEAN, SUM, DIURNAL
ag_commnds = {}
#ag_commnds['rlat'] = 'MEAN'
#ag_commnds['rlon'] = 'MEAN'
ag_commnds['time'] = 'DIURNAL'
#ag_commnds['altitude'] = 'MEAN'
#####################################################################

####################### NAMELIST PLOT #######################
nDPlot = 2 # How many dimensions should plot have (1 or 2)
i_diffPlot = 0 # Draw plot showing difference filtered - unfiltered # TODO
plotOutDir = '../00_plots/04_onlyAlps'
plotName = 'summary.png'
##### 1D PLOT #########

##### 2D Contour ######
contourTranspose = 0 # Reverse contour dimensions?
plotContour = 0 # Besides the filled contour, also plot the contour?
cmapM = 'jet' # colormap for Model output (jet, terrain, inferno, YlOrRd)
axis = 'equal' # set 'equal' if keep aspect ratio, else 'auto'
# COLORBAR Models
autoTicks = 1 # 1 if colorbar should be set automatically
Mmask = 0 # Mask Model values lower than MThrMinRel of maximum value?
MThrMinRel = 0.10 # Relative amount of max value to mask (see Mmask)
Mticks = [0.0001,0.0002,0.0003,0.0004,0.0005]
Mticks = list(np.arange(0.0002,0.0022,0.0002))
# COLORBAR Models
cmapD = 'bwr' # colormap for Difference output (bwr)
#####################################################################


an = analysis.analysis(inpPath, fieldNames)

an.subSpaceIndsIN = subSpaceIndsIN
an.ag_commnds = ag_commnds
an.i_info = i_info
an.i_resolutions = i_resolutions

# RUN ANALYSIS
an.run()


# SELECT ONLY CONVECTIVE HOURS
varNames = ['nHPBL']
for varName in varNames:
	#varName = 'zQC'
	for res in an.resolutions:
		mr = an.vars[varName]['modelRes'][res]
		#mr2 = an2.vars[varName]['modelRes'][res]
		for mode in mr.mdNms:
			subSpaceInds = {}
			subSpaceInds['time'] = (12,16)
			nco = mr.ncos[mode]
			nco.extractSubspace(subSpaceInds)
			#nco2 = mr2.ncos[mode]
			#nco2.extractSubspace(subSpaceInds)
			# AGGREGATE AGAIN
			ag_commnds = {}
			ag_commnds['time'] = 'MEAN'
			nco.aggregate(ag_commnds)
			#nco2.aggregate(ag_commnds)
an._setValueLimits()
#an2._setValueLimits()

HPBL = an.vars['nHPBL']
HSURF = an.vars['cHSURF']
res = '4.4'
mode = 'U'
threshold = 2000
plotName = 'summary_thresh_'+str(threshold)+'.png'

fig, axes = plt.subplots(ncols=3, nrows=2, figsize=(14,7))


print('HSURF')
hsurf = HSURF['modelRes'][res].ncos[mode].curFld
hsurf.mask = hsurf.vals > threshold
hsurf.vals[hsurf.mask == 0] = None
meanHSURF = np.nanmean(hsurf.vals)
print(meanHSURF)
cmap = 'terrain'
ax = axes[0,0]
CF = ax.contourf(hsurf.vals.squeeze(), cmap=cmap)
ax.text(10,5,str(int(meanHSURF))+'m',size=15)
fig.colorbar(CF, ax=ax)

print('diff')
cmap = 'bwr'
hsurf.vals = hsurf.vals - meanHSURF
Max = np.nanmax(hsurf.vals)
Min = np.nanmin(hsurf.vals)
amax = max(abs(Max), abs(Min))
ticks = np.linspace(start=-amax, stop=amax, num=8, endpoint=True)
ax = axes[1,0]
CF = ax.contourf(hsurf.vals.squeeze(), ticks, cmap=cmap)
fig.colorbar(CF, ax=ax)
hsurf.vals = hsurf.vals + meanHSURF



print('HPBL')
hpbl = HPBL['modelRes'][res].ncos[mode].curFld
hpbl.vals[hsurf.mask == 0] = None
meanHPBL = np.nanmean(hpbl.vals)
print(meanHPBL)
cmap = 'jet'
ax = axes[0,1]
CF = ax.contourf(hpbl.vals.squeeze(), cmap=cmap)
ax.text(10,5,str(int(meanHPBL))+'m',size=15)
fig.colorbar(CF, ax=ax)

print('diff')
cmap = 'bwr'
hpbl.vals = hpbl.vals - meanHPBL
Max = np.nanmax(hpbl.vals)
Min = np.nanmin(hpbl.vals)
amax = max(abs(Max), abs(Min))
ticks = np.linspace(start=-amax, stop=amax, num=8, endpoint=True)
ax = axes[1,1]
CF = ax.contourf(hpbl.vals.squeeze(), ticks, cmap=cmap)
fig.colorbar(CF, ax=ax)
hpbl.vals = hpbl.vals + meanHPBL



print('add')
hpbl.add(hsurf)
meanSum = np.nanmean(hpbl.vals)
cmap = 'jet'
ax = axes[0,2]
CF = ax.contourf(hpbl.vals.squeeze(), cmap=cmap)
ax.text(10,5,str(int(meanSum))+'m',size=15)
fig.colorbar(CF, ax=ax)
print(meanSum)

print('diff')
cmap = 'bwr'
hpbl.vals = hpbl.vals - meanSum
Max = np.nanmax(hpbl.vals)
Min = np.nanmin(hpbl.vals)
amax = max(abs(Max), abs(Min))
ticks = np.linspace(start=-amax, stop=amax, num=8, endpoint=True)
ax = axes[1,2]
CF = ax.contourf(hpbl.vals.squeeze(), ticks, cmap=cmap)
fig.colorbar(CF, ax=ax)
hpbl.vals = hpbl.vals + meanSum

fig.tight_layout()

#title = 'domain average ' + fieldNames[0] + ' at ' + str(altInd*100) + ' m'
#fig.suptitle(title, fontsize=14)


if i_plot == 1:
	plt.show()
elif i_plot == 2:
	plotPath = plotOutDir + '/' + plotName
	plt.savefig(plotPath, format='png', bbox_inches='tight')

#for mode in ['U', 'F']:
#	hpbl = HPBL['modelRes'][res].ncos[mode].curFld
#	hsurf = HSURF['modelRes'][res].ncos[mode].curFld
#	
#	hpbl.mean = np.mean(hpbl.vals)
#	hsurf.mean = np.mean(hsurf.vals)
#	print(hpbl.mean)
#	print(hsurf.mean)


import matplotlib
if i_plot == 2:
	matplotlib.use('Agg')
import matplotlib.pyplot as plt




quit()


if i_plot > 0:
	if i_info >= 3:
		print('plotting')
	mainVar = an.vars[an.fieldNames[0]]
	someField = mainVar['modelRes']['4.4'].ncos['U'].curFld
	if i_info >= 1:
		print('NONSINGLETONS: ' + str(someField.nNoneSingleton))
	import ncPlots.ncSubplots as ncSubplots
	ncs = ncSubplots.ncSubplots(an, nDPlot, i_diffPlot)
	
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

		
		fldName = 'nHPBL'
		fldName = 'cHSURF'
		ncs.plotVar2D(an.vars[fldName])
			
	elif nDPlot == 1 and someField.nNoneSingleton == 1:
	
		for fldName in an.fieldNames:
			if fldName != 'cHSURF':
				ncs.plotVar1D(an.vars[fldName])

	else:
		raise ValueError('ERROR: CANNOT MAKE ' + str(nDPlot) + 'D-PLOT WITH ' +
		str(someField.nNoneSingleton) + ' NON-SINGLETON DIMS!')

	
	if i_plot == 1:
		plt.show()
	elif i_plot == 2:
		plotPath = plotOutDir + '/' + plotName
		plt.savefig(plotPath, format='png', bbox_inches='tight')

		  


