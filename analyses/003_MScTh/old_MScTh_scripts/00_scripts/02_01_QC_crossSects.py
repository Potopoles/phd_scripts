#################################
# Calculate domain Average Precipitation
# author: Christoph Heim
# date: 21 10 2017
#################################
import os
os.chdir('00_scripts/')

i_resolutions = 3 # 1 = 4.4, 2 = 4.4 + 2.2, 3 = ...
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
#fieldNames = ['zQC', 'cHSURF']
#####################################################################		

lons = [80, 90, 107, 125, 150, 175, None, None, None, None, None, None, None]
lats = [None, None, None, None, None, None, 60, 75, 90, 100, 110, 120, 130]
days = range(11,20)
#days = range(11,12)

counts = range(0,len(lons))
#counts = [8]

for count in counts:
	#print(count)
	#count = counts[0]
	lon = lons[count]
	lat = lats[count]
	
	for day in days:
		#day = 11
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

		startTime = datetime(2006,7,day,12)
		endTime = datetime(2006,7,day,16)
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
		ag_commnds['time'] = 'MEAN'
		#ag_commnds['altitude'] = 'MEAN'
		#####################################################################

		####################### NAMELIST PLOT #######################
		nDPlot = 2 # How many dimensions should plot have (1 or 2)
		i_diffPlot = 0 # Draw plot showing difference filtered - unfiltered # TODO
		plotOutDir = '../00_plots/02_QC_crossSections/01_snapshot'
		if lat == None:
			plotName = 'QC_crossSection_hrs_12-15_lon_'+str(lon)+'_day_'+str(day)+'.png'
		elif lon == None:
			plotName = 'QC_crossSection_hrs_12-15_lat_'+str(lat)+'_day_'+str(day)+'.png'
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
		Mticks = list(np.arange(0.0001,0.0015,0.0002))
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



		if i_info >= 3:
			print('plotting')
		mainVar = an.vars[an.fieldNames[0]]
		
		someField = mainVar['modelRes'][list(mainVar['modelRes'].keys())[0]].ncos['U'].curFld
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
			title = 'QC cross-section  hrs: 12-15 day: ' + str(day) + ' lon: ' + str(lon)
		elif lon == None:
			title = 'QC cross-section  hrs: 12-15 day: ' + str(day) + ' lat: ' + str(lat)
		print(title)
		ncs.fig.suptitle(title, fontsize=14)
				


		if i_plot == 1:
			plt.show()
		elif i_plot == 2:
			plotPath = plotOutDir + '/' + plotName
			plt.savefig(plotPath, format='png', bbox_inches='tight')

				  


