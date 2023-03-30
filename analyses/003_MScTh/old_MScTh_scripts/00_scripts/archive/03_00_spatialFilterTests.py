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

startTime = datetime(2006,7,11,12)
endTime = datetime(2006,7,11,13)
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
cmapM = 'YlOrRd' # colormap for Model output (jet, terrain, inferno, YlOrRd)
axis = 'equal' # set 'equal' if keep aspect ratio, else 'auto'
# COLORBAR Models
autoTicks = 1 # 1 if colorbar should be set automatically
Mmask = 1 # Mask Model values lower than MThrMinRel of maximum value?
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



an2 = analysis.analysis(inpPath, fieldNames)
an2.subSpaceIndsIN = subSpaceIndsIN
an2.ag_commnds = ag_commnds
an2.i_info = i_info
an2.i_resolutions = i_resolutions
# RUN ANALYSIS
an2.run()


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
		
		# FILTER
		from scipy.ndimage import gaussian_filter
		sigma = 5
		for fldName in ['nHPBL', 'cHSURF']:
			var = an.vars[fldName]
			for res in an.resolutions:
				for mode in ['U', 'F']:
					vals = var['modelRes'][res].ncos[mode].curFld.vals
					vals = gaussian_filter(vals, sigma=sigma)
					var['modelRes'][res].ncos[mode].curFld.vals = vals
		
		HPBL = an.vars['nHPBL']
		HSURF = an.vars['cHSURF']
		
		# SEPARATE FIELDS
		hpbl = HPBL['modelRes'][res].ncos[mode].curFld
		hsurf = HSURF['modelRes'][res].ncos[mode].curFld
		
		hpbl0 = an2.vars['nHPBL']['modelRes'][res].ncos[mode].curFld
		hsurf0 = an2.vars['cHSURF']['modelRes'][res].ncos[mode].curFld
		
		# Add HSURF to HPBL
		hpbl.add(hsurf)
		hpbl0.add(hsurf)
		an._setValueLimits()
		an2._setValueLimits()
		
		#ncs.plotVar2D(an.vars['nHPBL'])
		#ncs.addContour(an.vars['cHSURF'], col='k', alpha=1)
		plt.close()
		
		######## TEST 3D
		from mpl_toolkits.mplot3d import Axes3D
		from matplotlib import cm
		from matplotlib.ticker import LinearLocator, FormatStrFormatter
		
		fig = plt.figure(figsize=plt.figaspect(0.5))

		
		# CREATE MESHGRID
		hpbl.dims['rlat'].mg, hpbl.dims['rlon'].mg = np.meshgrid(hpbl.dims['rlat'].vals,
														hpbl.dims['rlon'].vals)
		hsurf.dims['rlat'].mg, hsurf.dims['rlon'].mg = np.meshgrid(hsurf.dims['rlat'].vals,
														hsurf.dims['rlon'].vals)
		hpbl0.dims['rlat'].mg, hpbl0.dims['rlon'].mg = np.meshgrid(hpbl0.dims['rlat'].vals,
														hpbl0.dims['rlon'].vals)
		hsurf0.dims['rlat'].mg, hsurf0.dims['rlon'].mg = np.meshgrid(hsurf0.dims['rlat'].vals,
														hsurf0.dims['rlon'].vals)

		
		# Plot the surface.
		ax = fig.add_subplot(1, 2, 1, projection='3d')
		ax = fig.gca(projection='3d')
		var = hsurf
		surf = ax.plot_surface(var.dims['rlon'].mg, var.dims['rlat'].mg,
							   np.transpose(var.vals.squeeze()), cmap=cm.coolwarm,
							   linewidth=0, antialiased=True, alpha=1)
		var = hpbl				   
		surf = ax.plot_wireframe(var.dims['rlon'].mg, var.dims['rlat'].mg,
							   np.transpose(var.vals.squeeze()), color='k',
							   linewidth=1, alpha=0.3)
		ax.set_zlim(0, 5000)
							   
							   
					
		ax = fig.add_subplot(1, 2, 2, projection='3d')
		var = hpbl
		surf = ax.plot_wireframe(var.dims['rlon'].mg, var.dims['rlat'].mg,
							   np.transpose(var.vals.squeeze()), color='k',
							   linewidth=1, alpha=1)					   
		var = hpbl0
		surf = ax.plot_surface(var.dims['rlon'].mg, var.dims['rlat'].mg,
							   np.transpose(var.vals.squeeze()), cmap=cm.coolwarm,
							   linewidth=0, antialiased=True, alpha=0.3)
		ax.set_zlim(0, 5000)
		#import copy as copy
		#sfccols = copy.deepcopy(np.transpose(var.vals.squeeze()))
		#sfccols = np.abs(sfccols - np.transpose(hpbl.vals.squeeze()))
		#import matplotlib.cm as cm
		#norm = matplotlib.colors.Normalize(vmin=np.min(sfccols), vmax=np.max(sfccols))
		#sm = plt.cm.ScalarMappable(cmap=cm.bwr, norm=norm)
		#sfccols = sm.to_rgba(sfccols, alpha=0.4)
		##sfccols = cm.hot(np.abs(sfccols)/100000, alpha=0.5)
		#print(sfccols)
		##quit()
		#surf = ax.plot_surface(var.dims['rlon'].mg, var.dims['rlat'].mg,
		#					   np.transpose(var.vals.squeeze()), cmap=cm.coolwarm,
		#					   linewidth=0, antialiased=True, facecolors=sfccols)
		
			
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

		  


