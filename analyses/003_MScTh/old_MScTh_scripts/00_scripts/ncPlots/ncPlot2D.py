import ncClasses.analysis as analysis
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import copy as copy

from functions import round_sig

class ncPlot2D():
    
    def __init__(self, nco):
        self.nco = nco
        nco.field.prepareForPlotting()

        self.mult = 1.5
        
        heightStretch = 6*self.mult
        widthStretch = 6.36*self.mult
        self.fig, self.ax = plt.subplots(figsize=(widthStretch,heightStretch))


    def plotNCO(self, nco):

        self.Mmax = nco.field.max
        self.Mmin = nco.field.min
        MmaxA = max(abs(self.Mmax), abs(self.Mmin))

        # COLORBAR TICKS
        if self.autoTicks: # automatic
            MThrMin = self.MThrMinRel*self.Mmax
            if self.Mmask:
                self.Mticks = np.linspace(start=MThrMin, stop=self.Mmax, num=8, endpoint=True)
            else:
                divergingMaps = ['bwr', 'seismic']
                if self.cmapM in divergingMaps:
                    self.Mticks = np.linspace(start=-self.MmaxA, stop=self.MmaxA, num=10, endpoint=True)
                else:
                    self.Mticks = np.linspace(start=self.Mmin, stop=self.Mmax, num=12, endpoint=True)
                
        ax = self.ax
        ax.axis(self.axis) # aspect ratio

        # GET VALUES AND DIMENSIONS				
        fld = nco.field
        dims = fld.noneSingletonDims			
        dimx, dimy, fld = self._prepareDimAndFields(dims, fld)


        ax = self._adjustDateAxes(ax, dimx, dimy)				
        cmap = self.cmapM
        ticks = self.Mticks

        if self.plotContour in [0, 2]:
            CF = ax.contourf(dimx.vals, dimy.vals,
                                    fld.vals.squeeze(), ticks,
                                    cmap=cmap)

        # SET DIURNAL AXIS TICKS 
        if dimx.agg_mode == 'DIURNAL': 
            ax.set_xticks([0,6,12,18,24])
            #ax.grid(color='grey', linestyle='-', linewidth=0.2, axis='x')
            ax.grid(color='grey', linestyle='-', linewidth=0.2)
        if dimy.agg_mode == 'DIURNAL': 
            ax.set_yticks([0,6,12,18,24])

        # CONTOUR
        if self.plotContour in [1, 2]:
            ax.contour(dimx.vals, dimy.vals, fld.vals.squeeze(), self.Mticks,
                        linewidths=0.5, colors='k')
        
        # SUBPLOT TITLE
        #ax.set_title(nco.fieldName)
        
        # AXES UNITS AND LABELS
        xUnits, yUnits = self._getAxisUnits(dimx, dimy)
        ax.set_ylabel(dimy.label + ' ' + yUnits,fontsize=18*self.mult)
        ax.set_xlabel(dimx.label + ' ' + xUnits,fontsize=18*self.mult)
        #ax.xaxis.get_major_ticks().label.set_fontsize(10*self.mult)
        plt.tick_params(axis='both', which='major', labelsize=11*self.mult)
               
        # MODEL COLORBAR
        cPosBot = 0.12
        xPosLeft = 0.1
        width = 0.55
        cHeight = 0.03

        #CB = self.fig.colorbar(CF, ticks=self.Mticks)
        #fldUnits = self._getUnits(fld)
        #CB.set_label(fld.label + ' ' + fldUnits)

        return(self.fig, self.ax)


    def plotTopo(self, nco):
        tfld = nco.field
        self._plotTopo(self.ax, tfld)
        


    def _prepareDimAndFields(self, dims, fld):
        # ORDER DIMS ACCORDING TO ordering list.
        ordering = ['time', 'diurnal', 'rlon', 'rlat', 'altitude']
        dimsOrdered = [None, None, None, None, None]
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
            yUnits = r'$[' + dimy.units + r']$'
        else:
            yUnits = ''
        if dimx.units != '':
            xUnits = r'$[' + dimx.units + r']$'
        else:
            xUnits = ''
        return(xUnits, yUnits)
        
    def _plotTopo(self, ax, tfld):
        tTicks = np.array([-100,0,100,200,500,1000,1500,2000,2500,3000,3500,4000])
        tdims = tfld.noneSingletonDims
        if len(tdims) == 2: # 2D TOPO
            tdimx, tdimy, tfld = self._prepareDimAndFields(tdims, tfld)
            ax.contourf(tdimx.vals, tdimy.vals, tfld.vals.squeeze(), tTicks,
                cmap='binary', alpha=0.7)
        elif len(tdims) == 1: # 1D TOPO (FROM e.g. lon cross-section)
            tfld.vals[tfld.vals < 0] = 0 # for plotting: make ground always zero.
            ax.fill_between(tdims[0].vals, 0, tfld.vals.squeeze(), color='k')
            
        ax.axis(self.axis) # aspect ratio
            
            
    def addContour(self, var, col, alpha, lineWidth):

        Mmax = max(var.max['U'], var.max['F'])
        Mmin = min(var.min['U'], var.min['F'])
        if self.i_diffPlot:
            Dmax = var.max['D']
            Dmin = var.min['D']
            DmaxA = max(abs(Dmax), abs(Dmin))
        
        # COLORBAR TICKS
        if self.autoTicks: # automatic
            MThrMin = self.MThrMinRel*Mmax
            
            if self.Mmask:
                self.Mticks = np.linspace(start=MThrMin, stop=Mmax, num=6, endpoint=True)
            else:
                self.Mticks = np.linspace(start=Mmin, stop=Mmax, num=6, endpoint=True)
            
            if self.i_diffPlot:
                self.Dticks = np.linspace(start=-DmaxA, stop=DmaxA, num=5, endpoint=True)
        else: # manual
            if self.i_diffPlot:
                self.Dticks = np.linspace(start=-DmaxA, stop=DmaxA, num=5, endpoint=True)
        
        # MAIN LOOP
        for colInd,mode in enumerate(self.modes):
            for rowInd,res in enumerate(self.ress):
                #print(rowInd)
                if self.orientation == 'VER':
                    ax = self.axes[rowInd,colInd]
                elif self.orientation == 'HOR':
                    ax = self.axes[colInd,rowInd]
                
                ax.axis(self.axis) # aspect ratio

                # GET VALUES AND DIMENSIONS				
                fld = var.modelRes[res].ncos[mode].field
                dims = fld.getNoneSingletonDims()			
                dimx, dimy, fld = self._prepareDimAndFields(dims, fld)
                
                ax = self._adjustDateAxes(ax, dimx, dimy)				

                # CONTOUR
                C = ax.contour(dimx.vals, dimy.vals, fld.vals.squeeze(), self.Mticks,
                            linewidths=lineWidth, colors=col, alpha=alpha)
                ax.clabel(C, inline=1, fontsize=10)                

                if colInd == 0 and rowInd == 0:
                    Cout = C
                    
        return(Cout)
            

    def _getUnits(self, fld):
        if fld.units != '':
            units = '[' + fld.units + ']'
        else:
            units = ''
        return(units)
