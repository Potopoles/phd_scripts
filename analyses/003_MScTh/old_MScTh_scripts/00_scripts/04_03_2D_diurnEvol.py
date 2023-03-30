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
inpPath = '../02_fields/diurnal'
fieldNames = ['cHSURF']
#####################################################################		
hrs = list(range(8,24))
hrs.extend(list(range(0,8)))
nts = 24
vars = ['zWVP']
#vars = ['zWV_mass']
altInd = []

####################### NAMELIST DIMENSIONS #######################
subDomain = 1 # 0: full domain, 1: alpine region
# SUBSPACE
subSpaceInds = {}
if subDomain == 0: # (use topocut) 
    domainName = 'Whole_Domain'
if subDomain == 1: 
    domainName = 'Alpine_Region'
    subSpaceInds['rlon'] = [50,237]
    subSpaceInds['rlat'] = [41,155]
if subDomain == 2: # small Debug domain (use topocut)
    subSpaceInds['rlon'] = [60,90]
    subSpaceInds['rlat'] = [70,90]
if subDomain == 3: # Northern Italy plains (use subDomDiur)
    domainName = 'Northern_Italy_Plains'
    subSpaceInds['rlon'] = [48,100]
    subSpaceInds['rlat'] = [25,56]
if subDomain == 4: # Greater Northern Italy plains (use subDomDiur)
    domainName = 'Greater_Northern_Italy_Plains'
    subSpaceInds['rlon'] = [45,118]
    subSpaceInds['rlat'] = [12,62]

subSpaceInds['altitude'] = list(range(30,62))

####################### NAMELIST AGGREGATE #######################
# Options: MEAN, SUM, DIURNAL
ag_commnds = {}
#ag_commnds['rlat'] = 'MEAN'
#ag_commnds['rlon'] = 'MEAN'
ag_commnds['altitude'] = 'SUM'
#####################################################################

for var in vars:
    print('\n\n##################### '+var+' #######################')

    fieldNames.append(var)
    #fieldNames.append('nTOT_PREC')

    for i in range(0,len(hrs)):
        hr = hrs[i]
        print('\t\t   hr: '+str(hr))

        subSpaceInds['diurnal'] = [hr]

        ####################### NAMELIST PLOT #######################
        nDPlot = 2 # How many dimensions should plot have (1 or 2)
        i_diffPlot = 0 # Draw plot showing difference filtered - unfiltered # TODO
        if len(altInd) > 0:
            plotOutDir = '../00_plots/04_coldPools/diurn_'+var+'_alt_'+str(altitude)
        else:
            plotOutDir = '../00_plots/04_coldPools/diurn_'+var
        import os
        if not os.path.exists(plotOutDir):
            os.makedirs(plotOutDir)
        #hrStr = '{num:02d}'.format(num=hour)
        if len(altInd) > 0:
            plotName = str(i)+'_'+var+'_diurnEvol'+'_alt_'+str(altitude)+'_dt_'+str(hr)+'.png'
        else:
            plotName = str(i)+'_'+var+'_diurnEvol'+'_hr_'+str(hr)+'.png'
        ##### 1D PLOT #########

        ##### 2D Contour ######
        contourTranspose = 0 # Reverse contour dimensions?
        plotContour = 0 # Besides the filled contour, also plot the contour?
        cmapM = 'jet' # colormap for Model output (jet, terrain, inferno, YlOrRd)
        axis = 'equal' # set 'equal' if keep aspect ratio, else 'auto'
        # COLORBAR Models
        autoTicks = 0 # 1 if colorbar should be set automatically
        Mmask = 1 # Mask Model values lower than MThrMinRel of maximum value?
        MThrMinRel = 0.33 # Relative amount of max value to mask (see Mmask)
        # PRECIPITATION
        Mticks = [5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90]
        Mticks = [2,4,6,8,10,15,20,25,30,35,40,45,50,60,70,80,90]
        Mticks = np.arange(6,13.1,0.5)
        Mticks = np.arange(20,40,1)
        ## CAPE
        #Mticks = list(range(400,3600,200))
        ## CIN
        #Mticks = list(range(0,900,50))
        #if var == 'zAQVT_ADV' or var == 'zAQVT_ZADV':
        #    Mticks = list(range(-19,20,2))
        #elif var == 'zAQVT_TOT':
        #    Mticks = list(range(-15,16,2))
        #elif var == 'zRH':
        #    Mticks = list(range(0,120,5))
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

        #for res in an.resolutions:
        #    for mode in an.modes:
        #        nco = an.vars['zWV_mass'].ncos[res+mode]
        #        nco.field.vals = nco.field.vals*100

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
            
                if 'cHSURF' in an.varNames:
                    ncs.plotTopo(an.vars['cHSURF'])
                
                if i_diffPlot:
                    fig, axes, MCB, DCB = ncs.plotVar(an.vars[var])
                else:
                    fig, axes, MCB = ncs.plotVar(an.vars[var])

                #ncs.Mticks = [5]
                #ncs.addContour(an.vars['nTOT_PREC'], col='green', lineWidth=1.5, alpha=1)
                
                #title = an.vars[fieldNames[1]].label+' hCS diurnal hr: '+str(hr)
                #ncs.fig.suptitle(title, fontsize=14)

                MCB.set_label('Water Vapor Path $[kg$ $m^{-2}]$',fontsize=13) 

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
                plt.close('all')

                  

