#################################
# Calculate domain Average Precipitation
# author: Christoph Heim
# date: 21 10 2017
#################################
import os
os.chdir('00_scripts/')

i_resolutions = 2 # 1 = 4.4, 2 = 4.4 + 2.2, 3 = ...
i_plot = 1 # 0 = no plot, 1 = show plot, 2 = save plot
i_info = 2 # output some information [from 0 (off) to 5 (all you can read)]
import matplotlib
if i_plot == 2:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt


import ncClasses.analysis as analysis
from ncClasses.subdomains import setSSI
from datetime import datetime
from functions import *
####################### NAMELIST INPUTS FILES #######################
# directory of input model folders
inpPath = '../02_fields/diurnal'
fieldNames = ['cHSURF']
i_subdomain = 1
#####################################################################		
ssI = setSSI(i_subdomain, {'4.4':{},'2.2':{},'1.1':{}})
# DOMAIN 4 Greater Northern Italy Plains (use subDomDiur)
#lon0 = [45]
#lon1 = [118]
#lat0 = [12]
#lat1 = [62]
#plotName = 'locations_domain4_Greater_Northern_Italy_Plains.png'
## DOMAIN 3 Northern Italy Plains (use subDomDiur) 
#lon0 = [48]
#lon1 = [100]
#lat0 = [25]
#lat1 = [56]
#plotName = 'locations_domain3_Northern_Italy_Plains.png'
###################### NAMELIST DIMENSIONS #######################
# SUBSPACE
subSpaceIndsIN = {}

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
plotOutDir = '../00_plots/04_coldPools'
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

an.subSpaceInds = subSpaceIndsIN
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
    mainVar = an.vars[an.varNames[0]]
    someField = next(iter(mainVar.ncos.values())).field
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

        
        for varName in an.varNames:
            ncs.plotVar(an.vars[varName])
            
        #for rowInd,res in enumerate(an.resolutions):
        #    y1 = dimy.vals[lats[0]]
        #    y2 = dimy.vals[lats[1]]
        #    x1 = dimx.vals[lons[0]]
        #    x2 = dimx.vals[lons[1]]
        #    #ax.plot([x1, x1], [y1, y2], '-k')
        #    #ax.plot([x2, x2], [y1, y2], '-k')
        #    ax.plot([x1, x2], [y1, y1], '-k')
        #    #ax.plot([x1, x2], [y2, y2], '-k')
        #    #txt = str(lon)
        #    txt = ''
        #    ax.text(x1, y1, txt, size=txtSize)
        
        #####################################################################
        counts = range(0,len(lon0))
        
        txtSize = 10
        for count in counts:
            lons44 = [lon0[count], lon1[count]]
            lats44 = [lat0[count], lat1[count]]
            for rowInd,res in enumerate(an.resolutions):
                if res == '4.4':
                    lons = lons44
                    lats = lats44 
                elif res == '2.2':
                    lons = [lon*2 for lon in lons44]
                    lats = [lat*2 for lat in lats44]
                elif res == '1.1':
                    lons = [lon*4 for lon in lons44]
                    lats = [lat*4 for lat in lats44]
                
                for colInd,mode in enumerate(['', 'f']):
                    #mode = 'U'
                    if ncs.orientation == 'VER':
                        ax = ncs.axes[rowInd,colInd]
                    elif ncs.orientation == 'HOR':
                        ax = ncs.axes[colInd,rowInd]
                    
                    var = an.vars['cHSURF']
                    nco  = var.ncos[str(res)+mode]
                    fld = nco.field
                    dims = fld.noneSingletonDims			
                    dimx, dimy, fld = ncs._prepareDimAndFields(dims, fld)
                    
                    y1 = dimy.vals[lats[0]]
                    y2 = dimy.vals[lats[1]]
                    x1 = dimx.vals[lons[0]]
                    x2 = dimx.vals[lons[1]]
                    ax.plot([x1, x1], [y1, y2], '-k')
                    ax.plot([x2, x2], [y1, y2], '-k')
                    ax.plot([x1, x2], [y1, y1], '-k')
                    ax.plot([x1, x2], [y2, y2], '-k')
                    #txt = str(lon)
                    txt = ''
                    ax.text(x1, y1, txt, size=txtSize)
           
        ####################################################################
            
            
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

          


