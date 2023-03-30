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
i_diffPlot = 0
import matplotlib
if i_plot == 2:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt


import ncClasses.analysis as analysis
from datetime import datetime
from functions import *
from ncClasses.subdomains import setSSI
####################### NAMELIST INPUTS FILES #######################
# directory of input model folders
inpPath = '../02_fields/diurnal'
others = ['cHSURF', 'nTOT_PREC']
hydrometeors = ['zQC', 'zQI', 'zQV', 'zQR', 'zQS', 'zQG']
TTendencies=['zATT_MIC','zATT_RAD','zATT_ADV','zATT_ZADV','zATT_TURB','zATT_TOT','zATT_HADV']
QVTendencies=['zAQVT_MIC','zAQVT_ADV','zAQVT_ZADV','zAQVT_TURB','zAQVT_TOT','zAQVT_HADV']
#dynamics = ['zW', 'zU', 'zV', 'zT', 'zP', 'zRH']
dynamics = ['zW', 'zU', 'zV', 'zT', 'zRH']

group = 'AQVT'
group = 'ATT'
#group = 'AQVT1'
group = 'ATT1'

xlims = {}
if group == 'AQVT':
    fieldNames = QVTendencies
    xlims[''] = (-0.6,0.6)
    xlims['f'] = (-0.6,0.6)
    xlims['d'] = (-0.15,0.15)
elif group == 'AQVT1':
    fieldNames = ['zAQVT_MIC','zAQVT_ADV','zAQVT_TURB','zAQVT_TOT']
    xlims[''] = (-0.6,0.6)
    xlims['f'] = (-0.6,0.6)
    xlims['d'] = (-0.11,0.11)
elif group == 'ATT':
    fieldNames = TTendencies
    xlims[''] = (-1.6,1.6)
    xlims['f'] = (-1.6,1.6)
    xlims['d'] = (-0.35,0.35)
elif group == 'ATT1':
    fieldNames = ['zATT_MIC','zATT_RAD','zATT_ADV','zATT_TURB','zATT_TOT']
    xlims[''] = (-1.2,1.5)
    xlims['f'] = (-1.2,1.5)
    xlims['d'] = (-0.2,0.2)

diurnals = list(range(6,24))
diurnals.extend(list(range(0,6)))



####################### NAMELIST DIMENSIONS #######################
i_subDomain = 1 # 0: full domain, 1: alpine region
ssI, domainName = setSSI(i_subDomain, {'4.4':{}, '2.2':{}, '1.1':{}}) 
startHght = 2 
endHght = 64 
altInds = list(range(startHght,endHght+1))
for i in range(0,len(diurnals)):
    print(diurnals[i])
    ssI['altitude'] = altInds 
    ssI['diurnal'] = [diurnals[i]]
    #####################################################################

    ####################### NAMELIST AGGREGATE #######################
    # Options: MEAN, SUM, DIURNAL
    ag_commnds = {}
    ag_commnds['rlat'] = 'MEAN'
    ag_commnds['rlon'] = 'MEAN'
    ag_commnds['diurnal'] = 'MEAN'
    #ag_commnds['altitude'] = 'MEAN'
    #####################################################################

    ####################### NAMELIST PLOT #######################
    nDPlot = 1 # How many dimensions should plot have (1 or 2)
    plotOutDir = '../00_plots/01_domAv_Fields/domain_'+str(domainName)+'/diurnal/'+group
    import os
    if not os.path.exists(plotOutDir):
        os.makedirs(plotOutDir)
    plotName = 'dA_'+group+'_dom_'+str(domainName)+'_'+str(i)+'_hr_'+str(diurnals[i])+'.png'
    #print(plotName)
    ##### 1D PLOT #########

    ##### 2D Contour ######
    contourTranspose = 0 # Reverse contour dimensions?
    plotContour = 0 # Besides the filled contour, also plot the contour?
    axis = 'auto' # set 'equal' if keep aspect ratio, else 'auto'
    # COLORBAR Models
    cmapM = 'seismic'
    Mmask = 0
    autoTicks = 0
    absMax = 0.4
    step = 0.02
    Mticks = list(np.arange(-absMax,absMax+0.001,step))
    MThrMinRel = 0.15 # Relative amount of max value to mask (see Mmask)
    # COLORBAR Models
    cmapD = 'bwr' # colormap for Difference output (bwr)
    #####################################################################


    an = analysis.analysis(inpPath, fieldNames)

    an.subSpaceInds = ssI
    an.ag_commnds = ag_commnds
    an.i_info = i_info
    an.i_resolutions = i_resolutions

    # RUN ANALYSIS
    an.run()


    import matplotlib
    if i_plot == 2:
        matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    an.prepareForPlotting()

    fig,axes = plt.subplots(3,3,figsize=(12,12))
    for rI,res in enumerate(an.resolutions):
        for mI,mode in enumerate(['f','','d']):
            ax = axes[rI,mI] 
            lines = []
            for var in fieldNames:
                alts = an.vars[var].ncos[res+''].dims['altitude'].vals
                if mode == 'd':
                    raw = an.vars[var].ncos[res+''].field.vals
                    sm = an.vars[var].ncos[res+'f'].field.vals
                    vals = raw - sm
                else:
                    vals = an.vars[var].ncos[res+mode].field.vals

                line, = ax.plot(vals.squeeze(),alts)
                lines.append(line)
            ax.axvline(x=0)
            ax.grid()
            ax.set_xlim(xlims[mode])
            ax.set_ylim((0,10000))
            if rI == 0 and mI == 0:
                ax.legend(lines, labels=fieldNames)

    title = 'dA ' + group + ' hr ' + str(diurnals[i])
    fig.suptitle(title, fontsize=14)
    plt.tight_layout()

        
    if i_plot == 1:
        plt.show()
    elif i_plot == 2:
        plotPath = plotOutDir + '/' + plotName
        plt.savefig(plotPath, format='png', bbox_inches='tight')



