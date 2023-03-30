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
hrs = range(0,24)
#hrs = range(19,20)
altInds = [10,20,30,40,50,60,61,62,63,64]
altInds = [63]
vars = ['zW', 'CW', 'PR', 'zQC', 'zQI', 'zQR', 'zQG', 'zQS']
vars = ['zW']

for var in vars:
    print('\n\n##################### '+var+' #######################')

    if var == 'CW': # Cloud water (QC and QI)
        fieldNames.append('zQC')
        fieldNames.append('zQI')
    elif var == 'PR': # Precipitating water (QR and QG and QS)
        fieldNames.append('zQR')
        fieldNames.append('zQG')
        fieldNames.append('zQS')
    else:
        fieldNames.append(var)

    for altInd in altInds:
        #altInd = 62
        print('\t alt'+str(altInd))

        if altInd > 60:
            altitude = 6000 + (altInd-60)*1000
        else:
            altitude = altInd*100

        for hour in hrs:
            #hour = 12
            print('\t\t hr'+str(hour))


            ####################### NAMELIST DIMENSIONS #######################
            subDomain = 1 # 0: full domain, 1: alpine region, 2: zoom in
            # SUBSPACE
            subSpaceIndsIN = {}
            if subDomain == 1: # alpine region
                subSpaceIndsIN['rlon'] = [50,237]
                subSpaceIndsIN['rlat'] = [41,155]
            elif subDomain == 2: # zoom in subdomain
                subSpaceIndsIN['rlon'] = (70,100)
                subSpaceIndsIN['rlat'] = (70,100)
            elif subDomain == 3: # zoom in subdomain
                subSpaceIndsIN['rlon'] = (50,130)
                subSpaceIndsIN['rlat'] = (41,105)
            subSpaceIndsIN['altitude'] = [altInd]
            subSpaceIndsIN['diurnal'] = [hour]
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
            plotOutDir = '../00_plots/05_hCS_tA_diurnalEvol/'+var
            import os
            if not os.path.exists(plotOutDir):
                os.makedirs(plotOutDir)
            plotName = var+'_hCS_tA_diurnalEvol'+'_alt_'+str(altitude)+'_hr_'+str(hour)+'.png'
            ##### 1D PLOT #########

            ##### 2D Contour ######
            contourTranspose = 0 # Reverse contour dimensions?
            plotContour = 0 # Besides the filled contour, also plot the contour?
            cmapM = 'jet' # colormap for Model output (jet, terrain, inferno, YlOrRd)
            axis = 'equal' # set 'equal' if keep aspect ratio, else 'auto'
            # COLORBAR Models
            autoTicks = 1 # 1 if colorbar should be set automatically
            Mmask = 1 # Mask Model values lower than MThrMinRel of maximum value?
            MThrMinRel = 0.15 # Relative amount of max value to mask (see Mmask)
            Mticks = [0.0001,0.0002,0.0003,0.0004,0.0005]
            #if var == 'zW': 
            #    autoTicks = 1
            #    Mticks = list(np.arange(1,17,2))
            #elif var == 'CW':
            #    autoTicks = 1
            #    Mticks = list(np.arange(0.3,2.1,0.3))
            #elif var == 'PR':
            #    autoTicks = 1
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


            # SUM UP CLOUD WATER SPECIES
            if var == 'CW':
                an.vars['sum'] = an.vars['zQC'].addVar(an.vars['zQI'], label='total cloud water')
            if var == 'PR':
                an.vars['sum'] = an.vars['zQR'].addVar(an.vars['zQG'], label='total precipitating water')
                an.vars['sum'] = an.vars['sum'].addVar(an.vars['zQS'], label='total precipitating water')

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
                    
                    if var == 'CW' or var == 'PR':
                        fig, axes, MCB = ncs.plotVar(an.vars['sum'])
                    else:
                        fig, axes, MCB = ncs.plotVar(an.vars[var])
                    
                    #if var == 'CW' or var == 'PR':
                    #    title = an.vars['sum'].label+' hCS tA alt: '+\
                    #                str(altitude)+' hr: '+str(hour)
                    #else:
                    #    title = an.vars[fieldNames[1]].label+' hCS tA alt: '\
                    #                +str(altitude)+' hr: '+str(hour)
                    #ncs.fig.suptitle(title, fontsize=14)

                    MCB.set_label('Vertical Velocity [$ms^{-1}$]',fontsize=13)

                else:
                    raise ValueError('ERROR: CANNOT MAKE ' + str(nDPlot) + 'D-PLOT WITH ' +
                    str(someField.nNoneSingleton) + ' NON-SINGLETON DIMS!')

                
                if i_plot == 1:
                    plt.show()
                elif i_plot == 2:
                    plotPath = plotOutDir + '/' + plotName
                    plt.savefig(plotPath, format='png', bbox_inches='tight')
                    plt.close('all')

                      

