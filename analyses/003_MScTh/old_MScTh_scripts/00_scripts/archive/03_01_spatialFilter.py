#################################
# Calculate domain Average Precipitation
# author: Christoph Heim
# date: 21 10 2017
#################################
import os
os.chdir('00_scripts/')

i_resolutions =1 # 1 = 4.4, 2 = 4.4 + 2.2, 3 = ...
i_plot = 1 # 0 = no plot, 1 = show plot, 2 = save plot
i_info = 2 # output some information [from 0 (off) to 5 (all you can read)]
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
fieldNames = ['cHSURF']
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
#ag_commnds['time'] = 'DIURNAL'
#ag_commnds['altitude'] = 'MEAN'
#####################################################################

####################### NAMELIST PLOT #######################
nDPlot = 2 # How many dimensions should plot have (1 or 2)
i_diffPlot = 0 # Draw plot showing difference filtered - unfiltered # TODO
plotOutDir = '../00_plots'
plotName = 'test.png'
##### 1D PLOT #########

##### 2D Contour ######
contourTranspose = 0 # Reverse contour dimensions?
plotContour = 0 # 0: filled contour | 1: contour | 2: both
cmapM = 'bwr' # colormap for Model output (jet, terrain, inferno, YlOrRd)
axis = 'equal' # set 'equal' if keep aspect ratio, else 'auto'
# COLORBAR Models
autoTicks = 0 # 1 if colorbar should be set automatically
Mmask = 0 # Mask Model values lower than MThrMinRel of maximum value?
MThrMinRel = 0.1 # Relative amount of max value to mask (see Mmask)
Mticks = list(np.arange(-2000,2500,500))
# COLORBAR Models
cmapD = 'bwr' # colormap for Difference output (bwr)
#####################################################################

# FILTERED AND TIMEMEAN
an = analysis.analysis(inpPath, fieldNames)
an.subSpaceIndsIN = subSpaceIndsIN
an.ag_commnds = ag_commnds
an.i_info = i_info
an.i_resolutions = i_resolutions

# NONFILTER AND TIMEMEAN
an2 = analysis.analysis(inpPath, fieldNames)
an2.subSpaceIndsIN = subSpaceIndsIN
an2.ag_commnds = ag_commnds
an2.i_info = i_info
an2.i_resolutions = i_resolutions


# RUN ANALYSIS
an.run()
an2.run()


#####################################################################
# SELECT ONLY CONVECTIVE HOURS
varNames = ['nHPBL']
for varName in varNames:
	#varName = 'zQC'
	for res in an.resolutions:
		mr = an.vars[varName]['modelRes'][res]
		mr2 = an2.vars[varName]['modelRes'][res]
		for mode in mr.mdNms:
			subSpaceInds = {}
			subSpaceInds['time'] = (12,16)
			nco = mr.ncos[mode]
			nco.extractSubspace(subSpaceInds)
			nco2 = mr2.ncos[mode]
			nco2.extractSubspace(subSpaceInds)
			# AGGREGATE AGAIN
			ag_commnds = {}
			ag_commnds['time'] = 'MEAN'
			nco.aggregate(ag_commnds)
			nco2.aggregate(ag_commnds)
an._setValueLimits()
an2._setValueLimits()
#####################################################################


import matplotlib
if i_plot == 2:
	matplotlib.use('Agg')
import matplotlib.pyplot as plt


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
		
		# SEPARATE FIELDS
		# FILTER FIELDS
		fHPBL = an.vars['nHPBL']
		fHSURF = an.vars['cHSURF']
		# NONFILTER FIELDS
		HPBL = an2.vars['nHPBL']
		HSURF = an2.vars['cHSURF']
		
		#for fldName in ['nHPBL', 'cHSURF']:
		#	var = an.vars[fldName]
		#	for res in an.resolutions:
		#		for mode in ['U', 'F']:
		res = '4.4'
		for mode in ['U', 'F']:
			#mode = 'U'
			
			fhpbl = fHPBL['modelRes'][res].ncos[mode].curFld
			fhsurf = fHSURF['modelRes'][res].ncos[mode].curFld
			
			hpbl = an2.vars['nHPBL']['modelRes'][res].ncos[mode].curFld
			hsurf = an2.vars['cHSURF']['modelRes'][res].ncos[mode].curFld
			
			if mode == 'U':
				# FILTER
				from scipy.ndimage import gaussian_filter
				sigma = 5
				fhpbl.vals = gaussian_filter(fhpbl.vals, sigma=sigma)
				fhsurf.vals = gaussian_filter(fhsurf.vals, sigma=sigma)
			
			
			# Add HSURF to HPBL
			hpbl.add(hsurf)
			fhpbl.add(fhsurf)
			
		fHPBL['modelRes'][res].ncos['F'].curFld.subtract(fHPBL['modelRes'][res].ncos['U'].curFld)
		fHPBL['modelRes'][res].ncos['U'].curFld = fHPBL['modelRes'][res].ncos['F'].curFld
		an._setValueLimits()
		an2._setValueLimits()
		
		ncs.plotVar2D(fHPBL)
		#ncs.addContour(an.vars['cHSURF'], col='k', alpha=1)
		
			
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

		  


