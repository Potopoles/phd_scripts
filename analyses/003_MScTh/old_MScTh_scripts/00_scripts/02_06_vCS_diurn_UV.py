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
inpPath = '../02_fields/subDomDiur'
#####################################################################		
diurnalInds = range(0,24)
#diurnalInds = [19]

lons = [10, 40, 70, 100, 130, 160, None, None, None, None, None, None, None, None, None]
#lons = [130]
lats = [None, None, None, None, None, None, 10, 25, 40, 55, 62, 70, 77, 85, 100]
#lats = [None]

counts = range(0,len(lons))
#counts = [8]

for count in counts:
    lon = lons[count]
    lat = lats[count]
    print(str(lon)+' '+str(lat))
    
    if lon == None:
        varNames = ['zU', 'zW']
    elif lat == None:
        varNames = ['zV', 'zW']
    fieldNames = varNames + ['cHSURF']
    ####################### NAMELIST DIMENSIONS #######################
    subDomain = 0 # 0: full domain, 1: alpine region, 2: zoom in
    # SUBSPACE
    subSpaceInds = {}
    if lat != None:
        subSpaceInds['rlat'] = [lat]
    elif lon != None:
        subSpaceInds['rlon'] = [lon]
    
    #subSpaceInds['time'] = [datetime(2006,7,12,0), datetime(2006,7,13,0)]
    subSpaceInds['altitude'] = list(range(0,65))

    for diurnalInd in diurnalInds:
        #print(diurnalInd)
        subSpaceInds['diurnal'] = [diurnalInd] 
        #####################################################################

        ####################### NAMELIST AGGREGATE #######################
        # Options: MEAN, SUM, DIURNAL
        ag_commnds = {}
        if lat != None:
            ag_commnds['rlat'] = 'MEAN'
        elif lon != None:
            ag_commnds['rlon'] = 'MEAN'
        ag_commnds['diurnal'] = 'MEAN'
        #ag_commnds['altitude'] = 'MEAN'
        #####################################################################

        ####################### NAMELIST PLOT #######################
        nDPlot = 2 # How many dimensions should plot have (1 or 2)
        i_diffPlot = 0 # Draw plot showing difference filtered - unfiltered # TODO
        #plotOutDir = '../00_plots/02_vCS/'+varNames[0]+'_hrs_'+str(subSpaceInds['diurnal'])
        plotOutDir = '../00_plots/02_vCS/'+varNames[0]
        import os
        if not os.path.exists(plotOutDir):
            os.makedirs(plotOutDir)
        if lat == None:
            plotName = (varNames[0]+'_vCS_diurn_lon_'+str(lon)+'_hrs_'+
                        str(subSpaceInds['diurnal'][0])+'.png')
        elif lon == None:
            plotName = (varNames[0]+'_vCS_diurn_lat_'+str(lat)+'_hrs_'+
                        str(subSpaceInds['diurnal'][0])+'.png')

        ##### 2D Contour ######
        contourTranspose = 0 # Reverse contour dimensions?
        plotContour = 0 # Besides the filled contour, also plot the contour?
        # COLORMAPS diverging: seismic
        cmapM = 'seismic' # colormap for Model output (jet, terrain, inferno, YlOrRd)
        axis = 'auto' # set 'equal' if keep aspect ratio, else 'auto'
        # COLORBAR Models
        autoTicks = 1 # 1 if colorbar should be set automatically
        Mmask = 1 # Mask Model values lower than MThrMinRel of maximum value?
        MThrMinRel = 0.15 # Relative amount of max value to mask (see Mmask)
        Mticks = list(np.arange(0.0001,0.00035,0.00005))
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

            if 'cHSURF' in an.fieldNames:
                ncs.plotTopo(an.vars['cHSURF'])
                
            ncs.plotVar(an.vars[varNames[0]])

            if len(varNames) > 1:
                ncs.autoTicks = 0 # 1 if colorbar should be set automatically
                #Mmask = 1 # Mask Model values lower than MThrMinRel of maximum value?
                ncs.Mticks = [-0.5,0.5] 
                ncs.addContour(an.vars[varNames[1]], 'orange', 1, 1)
            
        else:
            raise ValueError('ERROR: CANNOT MAKE ' + str(nDPlot) + 'D-PLOT WITH ' +
            str(someField.nNoneSingleton) + ' NON-SINGLETON DIMS!')

        ## PBL Height
        #for colInd,mode in enumerate(ncs.modes):
        #    for rowInd,res in enumerate(ncs.ress):
        #        #print(rowInd)
        #        ax = ncs.axes[rowInd,colInd]

        #        # GET VALUES AND DIMENSIONS				
        #        fld = an.vars['nHPBL']['modelRes'][res].ncos[mode].curFld
        #        dim = fld.getNoneSingletonDims()[0]	

        #        topo = an.vars['cHSURF']['modelRes'][res].ncos[mode].curFld
        #        
        #        fld.vals = fld.vals + topo.vals
        #        ax.plot(dim.vals, fld.vals.squeeze(), color='darkgreen')
        #        ax.axhline(y=np.mean(fld.vals), linestyle='--', linewidth=1, color = 'darkgreen')
        #        ax.axhline(y=np.mean(topo.vals), linestyle='--', linewidth=1, color = 'black')
            
        if lat == None:
            title = varNames[0]+' vCS diurn hrs: '+str(subSpaceInds['diurnal'][0])+' lon: ' + str(lon)
        elif lon == None:
            title = varNames[0]+' vCS diurn hrs: '+str(subSpaceInds['diurnal'][0])+' lat: ' + str(lat)
        #print(title)
        ncs.fig.suptitle(title, fontsize=14)
                


        if i_plot == 1:
            plt.show()
        elif i_plot == 2:
            plotPath = plotOutDir + '/' + plotName
            plt.savefig(plotPath, format='png', bbox_inches='tight')

                  


