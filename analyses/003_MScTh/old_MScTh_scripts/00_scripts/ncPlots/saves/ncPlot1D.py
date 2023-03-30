import ncClasses.analysis as analysis
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

class ncPlot1D():
	
	def __init__(self, an):
		#super().__init__(an)
		self.an = an
		self.nRes = len(an.modelRes)
		
		self.colrs = [(1,0.5,0), (0,0.5,1), (1,0.8,0)]
		
	def prepare(self):
		if self.i_diffPlot:
			self.nCols = 2
		else:
			self.nCols = 1

		self.fig, self.axes = plt.subplots(ncols=self.nCols,
										nrows=3, figsize=(12,8))


	def draw(self, i_plot):
		
		Mmax = max(self.an.max['U'], self.an.max['F'])
		Mmin = min(self.an.min['U'], self.an.min['F'])
		Dmax = self.an.max['D']
		Dmin = self.an.min['D']
		
		xAxisDateFmt = mdates.DateFormatter('%d.%m')
		
		for rowInd in range(0,self.nRes):
			res = self.an.resolutions[rowInd]
			
			# MODEL PLOT
			ax = self.axes[rowInd, 0]
			fld = self.an.modelRes[res].ncos['U'].curFld
			dim = fld.getNoneSingletonDims()[0]
			
			if dim.valType == 'DATE':
				ax.xaxis.set_major_formatter(xAxisDateFmt)
			
			ax.plot(dim.vals, fld.vals.squeeze(), color=self.colrs[0])
			fld = self.an.modelRes[res].ncos['F'].curFld
			dim = fld.getNoneSingletonDims()[0]
			ax.plot(dim.vals, fld.vals.squeeze(), color=self.colrs[1])
			ax.grid()
			if rowInd == 0:
				ax.set_title('Models ' + res)
			else:
				ax.set_title(res)
			ax.set_ylim(Mmin, Mmax)
			ax.set_xlim(np.min(dim.vals), np.max(dim.vals))
			ax.legend(['unfiltered', 'filtered'])
			if fld.units != '':
				yUnits = '[' + fld.units + ']'
			else:
				yUnits = ''
			if dim.units != '':
				xUnits = '[' + dim.units + ']'
			else:
				xUnits = ''
			ax.set_ylabel(fld.label + ' ' + yUnits)
			if rowInd == self.nRes-1:
				ax.set_xlabel(dim.label + ' ' + xUnits)
				
			# DIFFERENCE PLOT
			ax = self.axes[rowInd, 1]
			fld = self.an.modelRes[res].ncos['D'].curFld
			dim = fld.getNoneSingletonDims()[0]
			
			if dim.valType == 'DATE':
				ax.xaxis.set_major_formatter(xAxisDateFmt)
			
			ax.axhline(y=0, color=(0.5,0.5,0.5), linestyle='-', linewidth=1)
			ax.plot(dim.vals, fld.vals.squeeze(), color=self.colrs[2])
			ax.grid()
			if rowInd == 0:
				ax.set_title('Difference ' + res)
			else:
				ax.set_title(res)
			ax.set_ylim(Dmin, Dmax)
			ax.set_xlim(np.min(dim.vals), np.max(dim.vals))
			leg = ax.legend(['filtered - unfiltered'])
			# make sure legend line color is plot line color and not axhline color.
			leg.legendHandles[0].set_color(self.colrs[2])
			if rowInd == self.nRes-1:
				ax.set_xlabel(dim.label + ' ' + xUnits)
			
			
		
		plt.tight_layout()
			
		if i_plot == 1:
			plt.show()
		elif i_plot == 2:
			plt.savefig(self.plotPath, format='png')
			

			