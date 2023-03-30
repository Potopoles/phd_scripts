#################################
# Calculate domain Average Precipitation
# author: Christoph Heim
# date: 21 10 2017
#################################
import os
os.chdir('00_scripts/')

i_resolutions = 1 # 1 = 4.4, 2 = 4.4 + 2.2, 3 = ...
i_plot = 2 # 0 = no plot, 1 = show plot, 2 = save plot
i_info = 0 # output some information [from 0 (off) to 5 (all you can read)]
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
fieldNames = ['zQC', 'nHPBL', 'cHSURF']
#####################################################################		

lons = [80, 90, 107, 125, 150, 175, None, None, None, None, None, None]
lats = [None, None, None, None, None, None, 60, 75, 90, 100, 110, 120]

ans = np.zeros((3,4))
ans[:] = None
ans = ans.tolist()

counts = range(0,len(lons))
#counts = [1,8]

for count in counts:
	print(count)
	#count = counts[0]
	lon = lons[count]
	lat = lats[count]
	
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
		
	if lat != None:
		subSpaceIndsIN['rlat'] = (lat,lat+1)
	elif lon != None:
		subSpaceIndsIN['rlon'] = (lon,lon+1)

	startTime = datetime(2006,7,11,0)
	endTime = datetime(2006,7,20,00)
	subSpaceIndsIN['time'] = (startTime,endTime)

	subSpaceIndsIN['altitude'] = (0,62)
	#####################################################################

	####################### NAMELIST AGGREGATE #######################
	# Options: MEAN, SUM, DIURNAL
	ag_commnds = {}
	if lat != None:
		ag_commnds['rlat'] = 'MEAN'
	elif lon != None:
		ag_commnds['rlon'] = 'MEAN'
	ag_commnds['time'] = 'DIURNAL'
	#ag_commnds['altitude'] = 'MEAN'
	#####################################################################

	####################### NAMELIST PLOT #######################
	nDPlot = 2 # How many dimensions should plot have (1 or 2)
	i_diffPlot = 0 # Draw plot showing difference filtered - unfiltered # TODO
	plotOutDir = '../00_plots/02_QC_crossSections'
	plotName = 'QC_crossSection_hrs_12-15_timeAverage_collection.png'
	##### 1D PLOT #########

	##### 2D Contour ######
	contourTranspose = 0 # Reverse contour dimensions?
	plotContour = 0 # Besides the filled contour, also plot the contour?
	cmapM = 'YlOrRd' # colormap for Model output (jet, terrain, inferno, YlOrRd)
	axis = 'auto' # set 'equal' if keep aspect ratio, else 'auto'
	# COLORBAR Models
	autoTicks = 0 # 1 if colorbar should be set automatically
	Mmask = 1 # Mask Model values lower than MThrMinRel of maximum value?
	MThrMinRel = 0.15 # Relative amount of max value to mask (see Mmask)
	Mticks = list(np.arange(0.0001,0.00035,0.00005))
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
	
	#####################################################################
	# SELECT ONLY CONVECTIVE HOURS
	varNames = ['zQC', 'nHPBL']
	for varName in varNames:
		#varName = 'zQC'
		for res in an.resolutions:
			mr = an.vars[varName]['modelRes'][res]
			for mode in mr.mdNms:
				subSpaceInds = {}
				subSpaceInds['time'] = (12,16)
				nco = mr.ncos[mode]
				nco.extractSubspace(subSpaceInds)
				# AGGREGATE AGAIN
				ag_commnds = {}
				ag_commnds['time'] = 'MEAN'
				nco.aggregate(ag_commnds)
        an.vars[varName].setValueLimits()
	#####################################################################
	
	rInd = int((count)/4 - (count)/4 % 1)
	cInd = int(count - 4*rInd)
	ans[rInd][cInd] = an



#####################################################################
import matplotlib
if i_plot == 2:
	matplotlib.use('Agg')
import matplotlib.pyplot as plt
import ncPlots.ncSubplots as ncSubplots

ncs = ncSubplots.ncSubplots(an, nDPlot, i_diffPlot)
plt.close()
ncs.contourTranspose = contourTranspose
#ncs.plotContour = plotContour
ncs.cmapM = cmapM
#ncs.axis = axis
#ncs.autoTicks = autoTicks
#ncs.Mmask = Mmask
#ncs.MThrMinRel = MThrMinRel
ncs.Mticks = Mticks
#ncs.cmapD = cmapD

fig, axes = plt.subplots(ncols=4, nrows=3,
									figsize=(18,10))
									

for count in counts:
	#count = 8
	rInd = int((count)/4 - (count)/4 % 1)
	cInd = int(count - 4*rInd)
	an = ans[rInd][cInd]
	ax = axes[rInd,cInd]

	var = an.vars['zQC']
	qc = var['modelRes']['4.4'].ncos['U'].curFld
	dims = qc.getNoneSingletonDims()			
	dimx, dimy, qc = ncs._prepareDimAndFields(dims, qc)

	cmap = ncs.cmapM
	ticks = ncs.Mticks
	CF = ax.contourf(dimx.vals, dimy.vals,
							qc.vals.squeeze(), ticks,
							cmap=cmap)
							
							
	var = an.vars['cHSURF']
	topo = var['modelRes']['4.4'].ncos['U'].curFld
	tdims = topo.getNoneSingletonDims()

	topo.vals[topo.vals < 0] = 0 # for plotting: make ground always zero.
	ax.fill_between(tdims[0].vals, 0, topo.vals.squeeze(), color='k')


	var = an.vars['nHPBL']
	hpbl = var['modelRes']['4.4'].ncos['U'].curFld
	dim = hpbl.getNoneSingletonDims()[0]	


	hpbl.vals = hpbl.vals + topo.vals
	ax.plot(dim.vals, hpbl.vals.squeeze(), color='darkgreen')
	ax.axhline(y=np.mean(hpbl.vals), linestyle='--', linewidth=1, color = 'darkgreen')
	ax.axhline(y=np.mean(topo.vals), linestyle='--', linewidth=1, color = 'black')
	
	lon = lons[count]
	lat = lats[count]
	
	txtSize = 10
	if lon == None:
		txt = 'lat ' + str(lat)
		x = 850
	elif lat == None:
		txt = 'lon ' + str(lon)
		x = 550
	ax.text(x, 6200, txt, size=txtSize)




if i_plot == 1:
	plt.show()
elif i_plot == 2:
	plotPath = plotOutDir + '/' + plotName
	plt.savefig(plotPath, format='png', bbox_inches='tight')
	
	
quit()




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

	if 'cHSURF' in an.fieldNames:
		ncs.plotTopo(an.vars['cHSURF'])
		
	ncs.plotVar2D(an.vars['zQC'])
	
elif nDPlot == 1 and someField.nNoneSingleton == 1:

	for fldName in an.fieldNames:
		if fldName != 'cHSURF':
			ncs.plotVar1D(an.vars[fldName])

else:
	raise ValueError('ERROR: CANNOT MAKE ' + str(nDPlot) + 'D-PLOT WITH ' +
	str(someField.nNoneSingleton) + ' NON-SINGLETON DIMS!')

# PBL Height
for colInd,mode in enumerate(ncs.modes):
	for rowInd,res in enumerate(ncs.ress):
		#print(rowInd)
		ax = ncs.axes[rowInd,colInd]

		# GET VALUES AND DIMENSIONS				
		fld = an.vars['nHPBL']['modelRes'][res].ncos[mode].curFld
		dim = fld.getNoneSingletonDims()[0]	

		topo = an.vars['cHSURF']['modelRes'][res].ncos[mode].curFld
		
		fld.vals = fld.vals + topo.vals
		ax.plot(dim.vals, fld.vals.squeeze(), color='darkgreen')
		ax.axhline(y=np.mean(fld.vals), linestyle='--', linewidth=1, color = 'darkgreen')
		ax.axhline(y=np.mean(topo.vals), linestyle='--', linewidth=1, color = 'black')
	
if lat == None:
	title = 'QC cross-section  hrs: 12-15 time average lon: ' + str(lon)
elif lon == None:
	title = 'QC cross-section  hrs: 12-15 time average lat: ' + str(lat)
print(title)
ncs.fig.suptitle(title, fontsize=14)
		




		  


