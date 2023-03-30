#################################
# Calculate domain Average Precipitation
# author: Christoph Heim
# date: 11 10 2017
#################################
import os
os.chdir('00_scripts/')

i_allResolutions = 0 # = 1: only 4.4 resolution, else all
i_plot = 2
i_info = 0 # output some information
import matplotlib
if i_plot == 2:
	matplotlib.use('Agg')
import matplotlib.pyplot as plt

import ncClasses.analysis as analysis
from datetime import datetime, timedelta
from functions import *
import copy as copy
####################### NAMELIST INPUTS FILES #######################
# directory of input model folders
inpPath = '../02_fields/result' # BOTH

#mode = 'zlev'
#startTime = datetime(2006,7,15,14)
#endTime = datetime(2006,7,15,15)
#startTime = datetime(2006,7,12,00)
#endTime = datetime(2006,7,13,00)

# input file name
#inpFileName = 'constantParams.nc'

# name of field to extract
fldName = 'TOT_PREC'
fldName = 'QC'
#fldName = 'HPBL'


inpFileName = 'TOT_PREC.nc' # OVERWRITES THINGS ABOVE
inpFileName = 'QC.nc' # OVERWRITES THINGS ABOVE
#inpFileName = 'HPBL.nc' # OVERWRITES THINGS ABOVE

useTopo = 1 # use topography background contourf?
#####################################################################		

times = range(0,217)
for ts in times:
	print(ts)
	####################### NAMELIST DIMENSIONS #######################
	subDomain = 1 # 0: full domain, 1: alpine region, 2: zoom in
	
	# SUBSPACE
	subSpaceIndsIN = {}
	if subDomain == 1: # alpine region
		subSpaceIndsIN['4.4'] = dict(rlon=(50,237),rlat=(41,155))
		subSpaceIndsIN['2.2'] = dict(rlon=(100,474),rlat=(82,310))
		subSpaceIndsIN['1.1'] = dict(rlon=(200,948),rlat=(164,620))
	elif subDomain == 2: # zoom in subdomain
		subSpaceIndsIN['4.4'] = dict(rlon=(70,100),rlat=(70,100))
		subSpaceIndsIN['2.2'] = dict(rlon=(140,200),rlat=(140,200))
		subSpaceIndsIN['1.1'] = dict(rlon=(280,400),rlat=(280,400))
		
	lat = None
	lon = 100
	if lat != None:
		subSpaceIndsIN['4.4']['rlat'] = (lat,lat+1)
		subSpaceIndsIN['2.2']['rlat'] = (2*lat,2*lat+2)
		subSpaceIndsIN['1.1']['rlat'] = (4*lat,4*lat+4)
	elif lon != None:
		subSpaceIndsIN['4.4']['rlon'] = (lon,lon+1)
		subSpaceIndsIN['2.2']['rlon'] = (2*lon,2*lon+2)
		subSpaceIndsIN['1.1']['rlon'] = (4*lon,4*lon+4)

	subSpaceIndsIN['time'] = (ts,ts+1)
	subSpaceIndsIN['altitude'] = (0,65)
	#####################################################################

	####################### NAMELIST AGGREGATE #######################
	# Options: MEAN, SUM, DIURNAL
	ag_commnds = {}
	if lat != None:
		ag_commnds['rlat'] = 'MEAN'
	elif lon != None:
		ag_commnds['rlon'] = 'MEAN'

	#ag_commnds['time'] = 'MEAN'
	#ag_commnds['altitude'] = 'SUM'
	# TOPO
	ag_commnds_topo = {}
	if 'rlat' in ag_commnds:
		ag_commnds_topo['rlat'] = ag_commnds['rlat']
	if 'rlon' in ag_commnds:
		ag_commnds_topo['rlon'] = ag_commnds['rlon']
	#####################################################################

	####################### NAMELIST PLOT #######################
	i_diffPlot = 0 # Draw plot showing difference filtered - unfiltered # TODO
	plotOutDir = '../00_plots/02_02_crossSectionsMovie'
	plotName = 'tInd_' + str(subSpaceIndsIN['time'][0]) + '.png'
	##### 1D PLOT #########

	##### 2D Contour ######
	plotContour = 0 # Besides the filled contour, also plot the contour?
	contourTranspose = 0 # Reverse contour dimensions?
	cmapM = 'jet' # colormap for Model output (jet, terrain)
	cmapD = 'bwr' # colormap for Difference output (bwr)
	axis = 'auto' # set 'equal' if keep aspect ratio, else 'auto'
	# COLORBAR Models
	Mauto = 0 # 1 if colorbar should be set automatically
	Mmask = 1 # Mask Model values lower than MThrMinRel of maximum value?
	MThrMinRel = 0.15 # Relative amount of max value to mask (see Mmask)
	#MThrMinAbs = 0
	Mticks = [0.0001,0.0002,0.0003,0.0004,0.0005,0.001]
	# COLORBAR Models
	Dticks = [-0.0001,0,0.0001]
	Dmask = 1 # Mask Difference values lower than MThrMinRel of maximum value?
	#####################################################################


	an = analysis.analysis(inpPath, inpFileName, fldName)

	an.subSpaceIndsIN = subSpaceIndsIN
	an.ag_commnds = ag_commnds
	an.ag_commnds_topo = ag_commnds_topo
	an.i_info = i_info
	an.i_allResolutions = i_allResolutions
	an.useTopo = useTopo


	an2 = analysis.analysis(inpPath, 'HPBL.nc', 'HPBL')

	an2.subSpaceIndsIN = copy.deepcopy(subSpaceIndsIN)
	#
	del an2.subSpaceIndsIN['altitude']
	an2.ag_commnds = copy.deepcopy(ag_commnds)
	an2.ag_commnds_topo = copy.deepcopy(ag_commnds_topo)
	an2.i_info = copy.deepcopy(i_info)
	an2.i_allResolutions = copy.deepcopy(i_allResolutions)
	an2.useTopo = copy.deepcopy(useTopo)
	an2.useTopo = 0


	# RUN ANALYSIS
	an.run()
	an2.run()
	#print(an.modelRes['4.4'].ncos['U'].curFld.vals.shape)



	plotPath = plotOutDir + '/' + plotName

	if i_plot > 0:
		#print('plotting')
		someField = an.modelRes[next(iter(an.modelRes))].ncos['U'].curFld
		if someField.nNoneSingleton == 1:
			import ncPlots.ncPlot1D as ncPlot1D
			ncp = ncPlot1D.ncPlot1D(an)
			ncp.i_diffPlot = i_diffPlot
			ncp.plotPath = plotPath
			ncp.prepare()
			ncp.draw(i_plot)
		elif someField.nNoneSingleton == 2:
			import ncPlots.ncPlot2D as ncPlot2D
			ncp = ncPlot2D.ncPlot2D(an)
			ncp.i_diffPlot = i_diffPlot
			ncp.plotPath = plotPath
			# 2D specific
			ncp.plotContour = plotContour
			ncp.contourTranspose = contourTranspose
			ncp.cmapM = cmapM
			ncp.cmapD = cmapD
			ncp.axis = axis
			ncp.Mauto = Mauto
			ncp.Mmask = Mmask
			ncp.MThrMinRel = MThrMinRel
			ncp.Dmask = Dmask
			ncp.Mticks = Mticks
			ncp.Dticks = Dticks
			ncp.useTopo = useTopo

			#
			ncp.prepare()
			fig, axes = ncp.draw(i_plot)
		else:
			raise ValueError('ERROR: CANNOT PLOT FIELD WITH ' +
			str(someField.nNoneSingleton) + ' NON-SINGLETON DIMS!')

		for rowInd,res in enumerate(an2.resolutions):
			#res = '4.4'
			ax = axes[rowInd, 0]
			fld = an2.modelRes[res].ncos['U'].curFld
			dim = fld.getNoneSingletonDims()[0]
			topo = an.modelRes[res].topo['U'].curFld
			fld.vals = fld.vals + topo.vals
			ax.plot(dim.vals, fld.vals.squeeze(), color='darkgreen')
			
			ax = axes[rowInd, 1]
			fld = an2.modelRes[res].ncos['F'].curFld
			dim = fld.getNoneSingletonDims()[0]
			topo = an.modelRes[res].topo['F'].curFld
			fld.vals = fld.vals + topo.vals
			ax.plot(dim.vals, fld.vals.squeeze(), color='darkgreen')
			
		dt = an.modelRes[res].ncos['U'].ncd.dims['time'].vals[0]
		fig.suptitle(str(dt), fontsize=14)
		
		if i_plot == 1:
			plt.show()
		elif i_plot == 2:
			plt.savefig(ncp.plotPath, format='png', bbox_inches='tight')
			
			
			
			  


