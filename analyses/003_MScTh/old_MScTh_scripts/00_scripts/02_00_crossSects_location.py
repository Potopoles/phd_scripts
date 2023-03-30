#################################
# Calculate domain Average Precipitation
# author: Christoph Heim
# date: 21 10 2017
#################################
import os
os.chdir('00_scripts/')

i_resolutions = 2 # 1 = 4.4, 2 = 4.4 + 2.2, 3 = ...
i_plot = 2 # 0 = no plot, 1 = show plot, 2 = save plot
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

#startTime = datetime(2006,7,11,0)
#endTime = datetime(2006,7,11,23)
#subSpaceIndsIN['time'] = (startTime,endTime)

#subSpaceIndsIN['altitude'] = (60,61)
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
plotOutDir = '../00_plots/02_QC_crossSections'
plotName = 'locations.png'
##### 1D PLOT #########

##### 2D Contour ######
contourTranspose = 0 # Reverse contour dimensions?
plotContour = 0 # Besides the filled contour, also plot the contour?
cmapM = 'terrain' # colormap for Model output (jet, terrain, inferno, YlOrRd)
axis = 'equal' # set 'equal' if keep aspect ratio, else 'auto'
# COLORBAR Models
autoTicks = 1 # 1 if colorbar should be set automatically
Mmask = 0 # Mask Model values lower than MThrMinRel of maximum value?
MThrMinRel = 0.15 # Relative amount of max value to mask (see Mmask)
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
	
		
		for fldName in an.fieldNames:
			ncs.plotVar2D(an.vars[fldName])
			
		
		#####################################################################
		lons = [80, 90, 107, 125, 150, 175, None, None, None, None, None, None, None]
		lats = [None, None, None, None, None, None, 60, 75, 90, 100, 110, 120, 130]
		lons = [None]
		lats = [110]
		counts = range(0,len(lons))
		#counts = [1,2,3,7,8,9]
		
		txtSize = 10
		for count in counts:
			lon44 = lons[count]
			lat44 = lats[count]
			for rowInd,res in enumerate(an.resolutions):
				#res = '4.4'
				if lat44 == None:
					lat = lat44
					if res == '2.2':
						lon = lon44*2
					elif res == '1.1':
						lon = lon44*4
					else:
						lon = lon44
				elif lon44 == None:
					lon = lon44
					if res == '2.2':
						lat = lat44*2
					elif res == '1.1':
						lat = lat44*4
					else:
						lat = lat44
				
				for colInd,mode in enumerate(['U', 'F']):
					#mode = 'U'
					ax = ncs.axes[rowInd,colInd]
					
					var = an.vars['cHSURF']
					nco  = var['modelRes'][res].ncos[mode]
					fld = nco.curFld
					dims = fld.getNoneSingletonDims()			
					dimx, dimy, fld = ncs._prepareDimAndFields(dims, fld)
					
					if lat == None:
						latI = nco.subSpaceInds['rlat']
						y1 = dimy.valsUncut[latI[0]]
						y2 = dimy.valsUncut[latI[1]]
						x = dimx.valsUncut[lon]
						ax.plot([x, x], [y1, y2], '-k')
						txt = str(lon)
						ax.text(x, y1, txt, size=txtSize)
					elif lon == None:
						lonI = nco.subSpaceInds['rlon']
						y = dimy.valsUncut[lat]
						x1 = dimx.valsUncut[lonI[0]]
						x2 = dimx.valsUncut[lonI[1]]
						ax.plot([x1, x2], [y, y], '-k')
						txt = str(lat)
						ax.text(x1, y+5, txt, size=txtSize)
				
		#####################################################################
			
			
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

		  


