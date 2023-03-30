import ncClasses.analysis as analysis
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import copy as copy

class ncPlot2D():
	
	def __init__(self, an):
	

	def draw(self, i_plot):
	
		#np.seterr(all='ignore')

		Mmax = max(self.an.max['U'], self.an.max['F'])
		Mmin = min(self.an.min['U'], self.an.min['F'])
		Dmax = self.an.max['D']
		Dmin = self.an.min['D']
		DmaxA = max(abs(Dmax), abs(Dmin))
		
		if self.Mauto: # AUTOMATIC COLORBARS
			MThrMin = self.MThrMinRel*Mmax
			#DThrMin = 0.2*DmaxA # NOT LARGER THAN 0.5*DMaxA!
			
			#tTicks = np.linspace(0,4000,10, endpoint=True)
			
			if self.Mmask:
				self.Mticks = np.linspace(start=MThrMin, stop=Mmax, num=6, endpoint=True)
			else:
				self.Mticks = np.linspace(start=Mmin, stop=Mmax, num=6, endpoint=True)
			self.Dticks = np.linspace(start=-DmaxA, stop=DmaxA, num=7, endpoint=True)
			#Dticks = np.array([-DmaxA,-2*DThrMin,-DThrMin,0,DThrMin,2*DThrMin,DmaxA])
			self.DThrMin = np.abs(self.Dticks[int(0.5*(len(self.Dticks)-1)-1)])
		else: #DEFAULT COLORBARS
			self.DThrMin = 0 # TODO -> Should refer to absolute value
			
		
		for rowInd in range(0,self.nRes):
			#print(rowInd)
			res = self.an.resolutions[rowInd]
			
			# UNFILTERED PLOT
			ax = self.axes[rowInd, 0]
			ax.axis(self.axis)
			fld = self.an.modelRes[res].ncos['U'].curFld
			dims = fld.getNoneSingletonDims()			
			dimx, dimy, fld = self._prepareDimAndFields(dims, fld)
			ax = self._adjustDateAxes(ax, dimx, dimy)
			# topo
			if self.useTopo:
				self._plotTopo(ax, self.an.modelRes[res].topo['U'].curFld)					
			# plot
			CF = ax.contourf(dimx.vals, dimy.vals, fld.vals.squeeze(), self.Mticks,
							cmap=self.cmapM)
			if self.plotContour:
				ax.contour(dimx.vals, dimy.vals, fld.vals.squeeze(), self.Mticks,
							linewidths=0.5, colors='k')
						
			if rowInd == 0:
				ax.set_title(res + ' unfiltered')
			else:
				ax.set_title(res)
			xUnits, yUnits = self._getAxisUnits(dimx, dimy)
			ax.set_ylabel(dimy.label + ' ' + yUnits)
			if rowInd == self.nRes-1:
				ax.set_xlabel(dimx.label + ' ' + xUnits)
				
				
				
			# FILTERED PLOT
			ax = self.axes[rowInd, 1]
			ax.axis(self.axis)
			fld = self.an.modelRes[res].ncos['F'].curFld
			dims = fld.getNoneSingletonDims()
			dimx, dimy, fld = self._prepareDimAndFields(dims, fld)
			ax = self._adjustDateAxes(ax, dimx, dimy)
			# topo
			if self.useTopo:
				self._plotTopo(ax, self.an.modelRes[res].topo['F'].curFld)
			# plot
			CF = ax.contourf(dimx.vals, dimy.vals, fld.vals.squeeze(), self.Mticks,
								cmap=self.cmapM)
			if self.plotContour:
				ax.contour(dimx.vals, dimy.vals, fld.vals.squeeze(), self.Mticks,
							linewidths=0.5, colors='k')
						
			if rowInd == 0:
				ax.set_title(res + ' filtered')
			else:
				ax.set_title(res)
			xUnits, yUnits = self._getAxisUnits(dimx, dimy)
			if rowInd == self.nRes-1:
				ax.set_xlabel(dimx.label + ' ' + xUnits)
			
			cPosBot = 0.1
			cHeight = 0.03
			# MODEL COLORBAR
			cax = self.fig.add_axes([0.1, cPosBot, 0.55, cHeight])
			MCB = plt.colorbar(mappable=CF, ticks=self.Mticks, cax=cax,
						orientation='horizontal')
			
			
			
			# DIFFERENCE PLOT
			if self.i_diffPlot:
				ax = self.axes[rowInd, 2]
				ax.axis(self.axis)
				fld = self.an.modelRes[res].ncos['D'].curFld
				dims = fld.getNoneSingletonDims()
				dimx, dimy, fld = self._prepareDimAndFields(dims, fld)
				ax = self._adjustDateAxes(ax, dimx, dimy)
				# topo
				if self.useTopo:
					self._plotTopo(ax, self.an.modelRes[res].topo['F'].curFld)				
				# plot
				filterFld = copy.deepcopy(fld.vals.squeeze())
				if self.Dmask:
					filterFld[np.abs(filterFld) < DThrMin] = None
				CFd = ax.contourf(dimx.vals, dimy.vals, filterFld, self.Dticks,
										cmap=self.cmapD)
				if self.plotContour:
					ax.contour(dimx.vals, dimy.vals, fld.vals.squeeze(),
								np.array([-DThrMin,DThrMin]), linewidths=0.5, colors='k')
							
				if rowInd == 0:
					ax.set_title(res + ' difference')
				else:
					ax.set_title(res)
				xUnits, yUnits = self._getAxisUnits(dimx, dimy)
				if rowInd == self.nRes-1:
					ax.set_xlabel(dimx.label + ' ' + xUnits)
			
				# DIFFERENCE COLORBAR
				cax = self.fig.add_axes([0.7, cPosBot, 0.25, cHeight])
				DCB = plt.colorbar(mappable=CFd, ticks=self.Dticks, cax=cax,
							orientation='horizontal')
			

		# ADJUST SUBPLOT POSITIONS
		self.fig.subplots_adjust(wspace=0.2, hspace=0.3,
				left=0.1, right=0.95, bottom=0.2, top=0.95)
				
		return(self.fig, self.axes)
		

		

			
			

			

	def _prepareDimAndFields(self, dims, fld):
		# ORDER DIMS ACCORDING TO ordering list.
		ordering = ['time', 'rlon', 'rlat', 'altitude']
		dimsOrdered = [None, None, None, None]
		for dim in dims:
			dimsOrdered[ordering.index(dim.key)] = dim	
		dims = [dim for dim in dimsOrdered if dim is not None]
		# SET cotourf X AND Y DIMENSIONS
		dimx = dims[0]
		dimy = dims[1]
		if self.contourTranspose:
			dimx = dims[1]
			dimy = dims[0]
		# TRANSPOSE fld SUCH THAT IT FITS TO DIMENSIONS
		dimOrder = [dimy.key, dimx.key] # Like contourf needs them
		fld.transposeToOrder(dimOrder)
		return(dimx, dimy, fld)
		
	def _adjustDateAxes(self, ax, dimx, dimy):
		# ADJUST DATE AXES
		axisDateFmt = mdates.DateFormatter('%d')
		if dimx.valType == 'DATE':
			ax.xaxis.set_major_formatter(axisDateFmt)
		if dimy.valType == 'DATE':
			ax.yaxis.set_major_formatter(axisDateFmt)
		return(ax)
		
	def _getAxisUnits(self, dimx, dimy):
		if dimy.units != '':
			yUnits = '[' + dimy.units + ']'
		else:
			yUnits = ''
		if dimx.units != '':
			xUnits = '[' + dimx.units + ']'
		else:
			xUnits = ''
		return(xUnits, yUnits)
		
	def _plotTopo(self, ax, tfld):
		if self.useTopo:
			tTicks = np.array([-100,0,100,200,500,1000,1500,2000,2500,3000,3500,4000])
			tdims = tfld.getNoneSingletonDims()
			if len(tdims) == 2: # 2D TOPO
				tdimx, tdimy, tfld = self._prepareDimAndFields(tdims, tfld)
				ax.contourf(tdimx.vals, tdimy.vals, tfld.vals.squeeze(), tTicks,
					cmap='binary')
			elif len(tdims) == 1: # 1D TOPO (FROM e.g. lon cross-section)
				tfld.vals[tfld.vals < 0] = 0 # for plotting: make ground always zero.
				ax.fill_between(tdims[0].vals, 0, tfld.vals.squeeze(), color='k')
				