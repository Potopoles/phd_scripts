import ncClasses.analysis as analysis
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import copy as copy

class ncSubplots():
    
    def __init__(self, an, nDPlot, i_diffPlot, orientation):
        #super().__init__(an)
        self.an = an
        self.an.prepareForPlotting()
        #self.ress = list(an.vars[an.fieldNames[0]]['modelRes'].keys())
        self.ress = an.resolutions
        self.nRes = len(self.ress)
        self.nRes = len(self.ress)
        self.i_diffPlot = i_diffPlot
        self.orientation = orientation 

        self.colrs = [(1,0.5,0), (0,0.5,1), (1,0.8,0)]
       
        if orientation == 'HOR': 
            if i_diffPlot:
                self.ncols = 3
                self.nrows = 1
            else:
                self.ncols = 2
                self.nrows = 1
        elif orientation == 'VER':            
            if i_diffPlot:
                self.ncols = 1
                self.nrows = 3
            else:
                self.ncols = 1
                self.nrows = 2
                            
        # (4,4) or (6,4) so far
        stretchCol = 4
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
    
        
    def plotVar(self, var):
        Mmax = var.max
        Mmin = var.min
        MmaxA = max(abs(var.max), abs(var.min))
        
        xAxisDateFmt = mdates.DateFormatter('%d.%m')
        

        ######################## MAIN LOOP ######################
        for rowInd,mode in enumerate(var.modes):
            if self.orientation == 'VER':
                ax = self.axes[rowInd,0]
            elif self.orientation == 'HOR':
                ax = self.axes[0,rowInd]
            
            for rI,res in enumerate(self.ress):
                # GET VALUES AND DIMENSIONS				
                fld = var.ncos[str(res+mode)].field
                dim = fld.noneSingletonDims[0]
                if dim.valType == 'DATE':
                    ax.xaxis.set_major_formatter(xAxisDateFmt)			
                elif dim.valType == 'DIURNAL':
                    ax.set_xticks([0,6,12,18,24])
            
                ax.plot(dim.vals, fld.vals.squeeze(), color=self.colrs[rI])
                
            ax.grid(color='grey', Linestyle='--')
            ax.set_title(var.modeNames[rowInd])
            ax.set_ylim(Mmin, Mmax)
            ax.set_xlim(np.min(dim.vals), np.max(dim.vals))
            ax.legend(self.ress)

            yUnits = self._getUnits(fld)
            xUnits = self._getUnits(dim)
            ax.set_ylabel(fld.label + ' ' + yUnits)
            
            # X-AXIS LABEL
            if self.orientation == 'VER':
                if rowInd == len(self.modes)-1:
                    ax.set_xlabel(dim.label + ' ' + xUnits)
            elif self.orientation == 'HOR':
                    ax.set_xlabel(dim.label + ' ' + xUnits)
        ######################################################    

        ######### DIFF PLOT
        if self.i_diffPlot:
            if self.orientation == 'VER':
                ax = self.axes[2,0]
            elif self.orientation == 'HOR':
                ax = self.axes[0,2]

            for rI,res in enumerate(self.ress):
                # GET VALUES AND DIMENSIONS				
                rawfld = var.ncos[str(res)].field
                smfld = var.ncos[str(res)+'f'].field
                diff = rawfld.vals - smfld.vals
                dim = rawfld.noneSingletonDims[0]

                if dim.valType == 'DATE':
                    ax.xaxis.set_major_formatter(xAxisDateFmt)			
                elif dim.valType == 'DIURNAL':
                    ax.set_xticks([0,6,12,18,24])
                    ax.set_xlim((0,24))
            
                ax.plot(dim.vals, diff.squeeze(), color=self.colrs[rI])

            ax.axhline(y=0, color=(0.5,0.5,0.5), linestyle='-', linewidth=1)
            ax.grid(color='grey', Linestyle='--')
            ax.legend(self.ress)
            # X-AXIS LABEL
            if self.orientation == 'VER':
                if rowInd == len(self.modes)-1:
                    ax.set_xlabel(dim.label + ' ' + xUnits)
            elif self.orientation == 'HOR':
                    ax.set_xlabel(dim.label + ' ' + xUnits)
            ax.set_ylabel('raw - smoothed')
            ax.set_title('raw - smoothed')
        ######### END DIFF PLOT 

        if self.orientation == 'VER':    
            self.fig.subplots_adjust(hspace=0.3,
                    left=0.23, right=0.95, bottom=0.1, top=0.90)
        elif self.orientation == 'HOR':    
            self.fig.subplots_adjust(wspace=0.4,
                    left=0.10, right=0.95, bottom=0.15, top=0.85)


    def _getUnits(self, fld):
        if fld.units != '':
            units = '[' + fld.units + ']'
        else:
            units = ''
        return(units)
