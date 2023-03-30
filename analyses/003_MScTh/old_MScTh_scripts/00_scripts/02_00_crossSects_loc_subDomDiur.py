#################################
# Calculate domain Average Precipitation
# author: Christoph Heim
# date: 21 10 2017
#################################
import os
os.chdir('00_scripts/')

i_resolutions = 3 # 1 = 4.4, 2 = 4.4 + 2.2, 3 = ...
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
inpPath = '../02_fields/subDomDiur'
fieldNames = ['cHSURF']
#####################################################################		

####################### NAMELIST DIMENSIONS #######################
# SUBSPACE
subSpaceInds = {}
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
plotOutDir = '../00_plots/02_vCS'
plotName = 'locations_subDomDiur.png'
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

an.subSpaceInds = subSpaceInds
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
    someField = mainVar.modelRes['4.4'].ncos['U'].curFld
    if i_info >= 1:
        print('NONSINGLETONS: ' + str(someField.nNoneSingleton))
    
    if nDPlot == 2 and someField.nNoneSingleton == 2:
        import ncPlots.ncSubplots2D as ncSubplots
        ncs = ncSubplots.ncSubplots(an, nDPlot, i_diffPlot, 'HOR')

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
            ncs.plotVar(an.vars[fldName])
            
        
        #####################################################################
        lons = [10, 40, 70, 100, 130, 160, None, None, None, None, None, None, None, None, None]
        lats = [None, None, None, None, None, None, 10, 25, 40, 55, 62, 70, 77, 85, 100]
        #lons = [None]
        #lats = [60]
        counts = range(0,len(lons))
        #counts = [1,2,3,7,8,9]
        
        txtSize = 10
        for count in counts:
            print(count)
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
                    if ncs.orientation == 'VER':
                        ax = ncs.axes[rowInd,colInd]
                    elif ncs.orientation == 'HOR':
                        ax = ncs.axes[colInd,rowInd]
                    
                    var = an.vars['cHSURF']
                    nco  = var.modelRes[res].ncos[mode]
                    fld = nco.curFld
                    dims = fld.noneSingletonDims			
                    dimx, dimy, fld = ncs._prepareDimAndFields(dims, fld)
                    
                    if lat == None:
                        y1 = dimy.valsUncut[0]
                        y2 = dimy.valsUncut[-1]
                        x = dimx.valsUncut[lon]
                        ax.plot([x, x], [y1, y2], '-k')
                        txt = str(lon)
                        ax.text(x, y1, txt, size=txtSize)
                    elif lon == None:
                        y = dimy.valsUncut[lat]
                        x1 = dimx.valsUncut[0]
                        x2 = dimx.valsUncut[-1]
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

          


