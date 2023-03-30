# Calculate domain Average Precipitation
# author: Christoph Heim
# date: 21 10 2017
#################################
import os
os.chdir('00_scripts/')

i_resolutions = 1 # 1 = 4.4, 2 = 4.4 + 2.2, 3 = ...
i_plot = 0 # 0 = no plot, 1 = show plot, 2 = save plot
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
inpPath = '../02_fields/result'
fieldNames = ['cHSURF', 'nTOT_PREC', 'nV_10M']
fieldNames = ['cHSURF', 'nTOT_PREC', 'nU_10M']
#####################################################################		
hrs = range(0,24)
startDateTime = datetime(2006,7,11,0)
nts = 217
#nts = 24
import datetime
dtlist = [startDateTime + datetime.timedelta(hours=x) for x in range(0,nts)]
#hrs = range(12,13)
vars = ['nU_10M']
vars = ['nV_10M']

for var in vars:
    print('\n\n##################### '+var+' #######################')

    fieldNames.append(var)

    for dt in dtlist:
        #hour = 12
        print('\t\t   datetime: '+str(dt))


        ####################### NAMELIST DIMENSIONS #######################
        subDomain = 2 # 0: full domain, 1: alpine region, 2: zoom in
        # SUBSPACE
        subSpaceIndsIN = {}
        if subDomain == 1: # alpine region
            subSpaceIndsIN['rlon'] = (50,237)
            subSpaceIndsIN['rlat'] = (41,155)
        elif subDomain == 2: # italy region
            subSpaceIndsIN['rlon'] = (80,180)
            subSpaceIndsIN['rlat'] = (50,120)
        #subSpaceIndsIN['altitude'] = (altInd, altInd+1)
        startTime = dt
        endTime = dt + datetime.timedelta(hours=1)
        subSpaceIndsIN['time'] = (startTime,endTime)
        #####################################################################

        ####################### NAMELIST AGGREGATE #######################
        # Options: MEAN, SUM, DIURNAL
        ag_commnds = {}
        #ag_commnds['rlat'] = 'MEAN'
        #ag_commnds['rlon'] = 'MEAN'
        #####################################################################

        ####################### NAMELIST PLOT #######################
        nDPlot = 2 # How many dimensions should plot have (1 or 2)
        i_diffPlot = 0 # Draw plot showing difference filtered - unfiltered # TODO
        plotOutDir = '../00_plots/04_coldPools/convPrec'+var
        import os
        if not os.path.exists(plotOutDir):
            os.makedirs(plotOutDir)
        #hrStr = '{num:02d}'.format(num=hour)
        dtStr = format(dt,'%d_%H') 
        plotName = var+'_timeSeries'+'_dt_'+dtStr+'.png'
        ##### 1D PLOT #########

        ##### 2D Contour ######
        contourTranspose = 0 # Reverse contour dimensions?
        plotContour = 0 # Besides the filled contour, also plot the contour?
        cmapM = 'seismic' # colormap for Model output (jet, terrain, inferno, YlOrRd)
        axis = 'equal' # set 'equal' if keep aspect ratio, else 'auto'
        # COLORBAR Models
        autoTicks = 0 # 1 if colorbar should be set automatically
        Mmask = 0 # Mask Model values lower than MThrMinRel of maximum value?
        MThrMinRel = 0.15 # Relative amount of max value to mask (see Mmask)
        Mticks = [-16,-14,-12,-10,-8,-6,-4,-2,2,4,6,8,10,12,14,16]
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
    
        # CALCULATE CONVERGENCE
        an.vars['conv'] = an.vars['nU_10M']._copy()
        an.fieldNames.append('conv')
        modes = ['U', 'F']
        ress = an.resolutions
        for res in ress:
            #print(res)
            for mode in modes:
                #print(mode)
                CONV = an.vars['conv'].modelRes[res].ncos[mode].curFld
                CONV.name = 'conv'
                conv = CONV.vals
                u = an.vars['nU_10M'].modelRes[res].ncos[mode].curFld.vals
                v = an.vars['nV_10M'].modelRes[res].ncos[mode].curFld.vals
                conv[:] = np.nan
                (nt,nlat,nlon) = conv.shape
                dx = float(res)*1000
                for y in range(1,nlat-1):
                    for x in range(1,nlon-1):
                        conv[0,y,x] = (u[0,y,x-1] - u[0,y,x+1])/(2*dx) + (v[0,y-1,x] - v[0,y+1,x])/(2*dx)
                an.vars['conv'].modelRes[res].ncos[mode].curFld.vals = conv 
                #print('max ' + str(np.nanmax(conv)))
                #print('min ' + str(np.nanmin(conv)))


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
                import ncPlots.ncSubplots2D_05_02 as ncSubplots
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
                
                ncs.plotVar(an.vars[var])

                # CONVERGENCE
                ncs.autoTicks = 0 # 1 if colorbar should be set automatically
                ncs.Mticks = [-0.0008, 0.0008]
                ncs.Mticks = [0.003]
                ncs.addContour(an.vars['conv'], col='orange', lineWidth=1.5, alpha=1)

                # PRECIPITATION
                ncs.autoTicks = 0 # 1 if colorbar should be set automatically
                ncs.Mticks = [5]
                ncs.addContour(an.vars['nTOT_PREC'], col='green', lineWidth=1.5, alpha=1)
                

                title = an.vars[fieldNames[1]].label+' hCS tA dt: '+str(dt)
                ncs.fig.suptitle(title, fontsize=14)

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

                  

        if 'conv' in an.fieldNames: an.fieldNames.remove('conv')
