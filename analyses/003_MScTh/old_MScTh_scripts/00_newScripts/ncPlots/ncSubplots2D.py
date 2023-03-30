import ncClasses.analysis as analysis
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import copy as copy

from functions import round_sig

class ncSubplots():
    
    def __init__(self, an, nDPlot, i_diffPlot, orientation):
        self.an = an
        self.an.prepareForPlotting()
        self.ress = an.resolutions
        self.nRes = len(self.ress)
        self.nRes = len(self.ress)
        self.i_diffPlot = i_diffPlot
        self.orientation = orientation
       
        if orientation == 'HOR': 
            if i_diffPlot:
                self.ncols = self.nRes
                self.nrows = 3
            else:
                self.ncols = self.nRes
                self.nrows = 2
        elif orientation == 'VER':            
            if i_diffPlot:
                self.ncols = 3
                self.nrows = self.nRes
            else:
                self.ncols = 2
                self.nrows = self.nRes
                                        
        # (4,4) or (6,4) so far
        if self.orientation == 'VER':
            stretchCol = 4
            stretchRow = 4
        elif self.orientation == 'HOR':
            stretchCol = 5
            stretchRow = 4

        self.fig, self.axes = plt.subplots(ncols=self.ncols,
                                        nrows=self.nrows,
                                        figsize=(self.ncols*stretchCol,self.nrows*stretchRow))
                                        
        
        # MAKE SURE THAT self.axes IS 2D ARRAY
        self.axes = np.asarray(self.axes)
        if len(self.axes.shape) == 1:
            if self.ncols == 1:
                self.axes = np.expand_dims(self.axes,1)
            elif self.nrows == 1:
                self.axes = np.expand_dims(self.axes,0)
            
        # CONTAINS THE ACTUAL PLOTTED INSTANCES (LIKE filled contour)
        self.plts = np.zeros(self.axes.shape).tolist()
    
    def plotTopo(self, topo):
        for colInd,mode in enumerate(topo.modes):
            for rowInd,res in enumerate(self.ress):
                if self.orientation == 'VER':
                    ax = self.axes[rowInd,colInd]
                elif self.orientation == 'HOR':
                    ax = self.axes[colInd,rowInd]
                tfld = topo.ncos[str(res+mode)].field
                self._plotTopo(ax, tfld)
                

    def plotVar(self, var):
        Mmax = var.max
        Mmin = var.min
        MmaxA = max(abs(var.max), abs(var.min))

        divergingMaps = ['bwr', 'seismic']
           
        MThrMin = self.MThrMinRel*MmaxA

        # MAIN LOOP
        for colInd,mode in enumerate(var.modes):
            for rowInd,res in enumerate(self.ress):
                if self.orientation == 'VER':
                    ax = self.axes[rowInd,colInd]
                elif self.orientation == 'HOR':
                    ax = self.axes[colInd,rowInd]
                
                ax.axis(self.axis) # aspect ratio

                # GET VALUES AND DIMENSIONS				
                fld = var.ncos[str(res+mode)].field
                dims = fld.noneSingletonDims			
                dimx, dimy, fld = self._prepareDimAndFields(dims, fld)

                #ax = self._adjustDateAxes(ax, dimx, dimy)				

                # COLORMAP and TICKS
                cmap = self.cmapM
                ticks = self.Mticks
                    
                # FILLED CONTOUR
                if dimx.key == 'rlon' and dimy.key == 'rlat':
                    i_plotType = 1
                else:
                    i_plotType = 0

                # MASK MOUNTAIN

                # CREATE LEVELS
                fld.vals = np.ma.masked_where(np.isnan(fld.vals), fld.vals) 
                from matplotlib.ticker import MaxNLocator
                if self.cmapM in divergingMaps:
                    levels = MaxNLocator(nbins=15).tick_values(-MmaxA, MmaxA)
                    if self.Mmask:
                        fld.vals = np.ma.masked_where(abs(fld.vals) <= MThrMin, fld.vals) 
                else:
                    if self.autoTicks:
                        if MThrMin < Mmax:
                            levels = MaxNLocator(nbins=15).tick_values(MThrMin, Mmax)
                        elif MThrMin > Mmax:
                            levels = MaxNLocator(nbins=15).tick_values(MThrMin, Mmax)
                        if self.Mmask:
                            fld.vals = np.ma.masked_where(fld.vals <= MThrMin, fld.vals) 
                    else:
                        levels = self.Mticks
                        if self.Mmask:
                            fld.vals = np.ma.masked_where(fld.vals <= levels[0], fld.vals) 
                        

                cmap = plt.get_cmap(cmap)

                # FILLED CONTOUR WITH INTERPOLATION
                if i_plotType == 0:
                    CF = ax.contourf(dimx.vals, dimy.vals,
                                            fld.vals.squeeze(), levels=levels,
                                            cmap=cmap)

                # COLORMESH SHOWING PIXELS. NO INTERPOLATION
                elif i_plotType == 1:
                    [gridx, gridy] = np.meshgrid(dimx.vals, dimy.vals)
                    from matplotlib.colors import BoundaryNorm
                    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
                    CF = ax.pcolormesh(gridx, gridy, fld.vals.squeeze(), cmap=cmap, norm=norm)
                    
                if self.orientation == 'VER':
                    self.plts[rowInd][colInd] = CF
                elif self.orientation == 'HOR':
                    self.plts[colInd][rowInd] = CF

                # SET DIURNAL AXIS TICKS 
                if dimx.agg_mode == 'DIURNAL': 
                    ax.set_xticks([0,6,12,18,24])
                    ax.grid(color='grey', linestyle='-', linewidth=0.2)
                if dimy.agg_mode == 'DIURNAL': 
                    ax.set_yticks([0,6,12,18,24])

                # SUBPLOT TITLE
                ax.set_title(res + ' ' + var.modeNames[colInd])
                
                # AXES UNITS AND LABELS
                xUnits, yUnits = self._getAxisUnits(dimx, dimy)
                ax.set_ylabel(dimy.label + ' ' + yUnits)
                if self.orientation == 'VER':
                    if colInd == self.nRes-1:
                        ax.set_xlabel(dimx.label + ' ' + xUnits)
                elif self.orientation == 'HOR':
                    if colInd == self.nrows-1:
                        ax.set_xlabel(dimx.label + ' ' + xUnits)

        ######### DIFF PLOT
        if self.i_diffPlot:
            for rI,res in enumerate(self.ress):
                if self.orientation == 'VER':
                    ax = self.axes[rI,2]
                elif self.orientation == 'HOR':
                    ax = self.axes[2,rI]
                # GET VALUES AND DIMENSIONS				
                rawfld = var.ncos[str(res)].field
                smfld = var.ncos[str(res)+'f'].field
                diff = rawfld.vals - smfld.vals
                dims = rawfld.noneSingletonDims			
                dimx, dimy, fld = self._prepareDimAndFields(dims, rawfld)

                # COLORMAP and TICKS
                cmap = self.cmapM
                ticks = self.Mticks
                    
                # FILLED CONTOUR
                # CREATE LEVELS
                dmin = np.nanmin(diff)
                dmax = np.nanmax(diff)
                dabsmax = np.max((np.abs(dmin), np.abs(dmax)))
                levels = MaxNLocator(nbins=15).tick_values(-dabsmax, dabsmax)
                #if self.Mmask:
                #    fld.vals = np.ma.masked_where(abs(fld.vals) <= MThrMin, fld.vals) 
                cmap = plt.get_cmap('seismic')

                # FILLED CONTOUR WITH INTERPOLATION
                if i_plotType == 0:
                    DCF = ax.contourf(dimx.vals, dimy.vals,
                                            diff.squeeze(), levels=levels,
                                            cmap=cmap)

                # COLORMESH SHOWING PIXELS. NO INTERPOLATION
                elif i_plotType == 1:
                    [gridx, gridy] = np.meshgrid(dimx.vals, dimy.vals)
                    from matplotlib.colors import BoundaryNorm
                    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
                    DCF = ax.pcolormesh(gridx, gridy, diff.squeeze(),
                                    cmap=cmap, norm=norm)
                    
                if self.orientation == 'VER':
                    self.plts[rowInd][2] = CF
                elif self.orientation == 'HOR':
                    self.plts[2][rowInd] = CF

                # SET DIURNAL AXIS TICKS 
                if dimx.agg_mode == 'DIURNAL': 
                    ax.set_xticks([0,6,12,18,24])
                    ax.grid(color='grey', linestyle='-', linewidth=0.2)
                if dimy.agg_mode == 'DIURNAL': 
                    ax.set_yticks([0,6,12,18,24])
                
                # SUBPLOT TITLE
                ax.set_title('raw - smoothed')
                
                # AXES UNITS AND LABELS
                xUnits, yUnits = self._getAxisUnits(dimx, dimy)
                ax.set_ylabel(dimy.label + ' ' + yUnits)
                if self.orientation == 'VER':
                    if colInd == self.nRes-1:
                        ax.set_xlabel(dimx.label + ' ' + xUnits)
                elif self.orientation == 'HOR':
                    if colInd == self.nrows-1:
                        ax.set_xlabel(dimx.label + ' ' + xUnits)
        ######### END DIFF PLOT 
                    
        # MODEL COLORBAR
        if self.orientation == 'VER':
            cPosBot = 0.12
            xPosLeft = 0.1
            if self.i_diffPlot:
                width = 0.55
            else:
                width = 0.85
        elif self.orientation == 'HOR':
            cPosBot = 0.07
            xPosLeft = 0.1
            if self.nRes < 2:
                xPosLeft = 0.1
                width = 0.8
            else:
                if self.i_diffPlot:
                    xPosLeft = 0.1
                    width = 0.5
                else:
                    xPosLeft = 0.25
                    width = 0.5

        cHeight = 0.03

        cax = self.fig.add_axes([xPosLeft, cPosBot, width, cHeight])
        MCB = plt.colorbar(mappable=CF, cax=cax,
                    orientation='horizontal')
        fldUnits = self._getUnits(fld)
        MCB.set_label(fld.label + ' ' + fldUnits)
                    
        # DIFFERENCE COLORBAR
        if self.i_diffPlot:
            cax = self.fig.add_axes([0.7, cPosBot, 0.25, cHeight])
            DCB = plt.colorbar(mappable=DCF, cax=cax,
                        orientation='horizontal')
            fldUnits = self._getUnits(fld)
            DCB.set_label(fld.label + ' ' + fldUnits)
                            

        # ADJUST SUBPLOT POSITIONS
        if self.orientation == 'VER':
            if self.nRes < 2:
                self.fig.subplots_adjust(wspace=0.3, hspace=0.3,
                        left=0.1, right=0.95, bottom=0.3, top=0.85)
            else:
                self.fig.subplots_adjust(wspace=0.3, hspace=0.3,
                        left=0.1, right=0.95, bottom=0.22, top=0.91)
        elif self.orientation == 'HOR':
            if self.nRes < 2:
                self.fig.subplots_adjust(wspace=0.3, hspace=0.4,
                        left=0.2, right=0.85, bottom=0.25, top=0.90)
            else:
                self.fig.subplots_adjust(wspace=0.22, hspace=0.3,
                        left=0.07, right=0.96, bottom=0.18, top=0.90)
                    
        return(self.fig, self.axes)
        


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
            yUnits = '[' + dimy.units + ']'
        else:
            yUnits = ''
        if dimx.units != '':
            xUnits = '[' + dimx.units + ']'
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
                self.Mticks = np.linspace(start=MThrMin, stop=Mmax, num=4, endpoint=True)
            else:
                self.Mticks = np.linspace(start=Mmin, stop=Mmax, num=4, endpoint=True)
            
            if self.i_diffPlot:
                self.Dticks = np.linspace(start=-DmaxA, stop=DmaxA, num=3, endpoint=True)
        else: # manual
            if self.i_diffPlot:
                self.Dticks = np.linspace(start=-DmaxA, stop=DmaxA, num=3, endpoint=True)
        
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
                fld = var.modelRes[res].ncos[mode].curFld
                dims = fld.noneSingletonDims			
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
