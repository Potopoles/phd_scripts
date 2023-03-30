################################
# Calculate domain Average Precipitation
# author: Christoph Heim
# date: 21 10 2017
#################################
import os
os.chdir('00_scripts/')

i_resolutions = 3 # 1 = 4.4, 2 = 4.4 + 2.2, 3 = ...
i_plot = 3 # 0 = no plot, 1 = show plot, 2 = save plot
i_info = 1 # output some information [from 0 (off) to 5 (all you can read)]
import matplotlib
if i_plot == 2:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt


import ncClasses.analysis as analysis
from ncClasses.ncObject import ncObject
from datetime import datetime
from functions import *
from ncClasses.subdomains import setSSI
from netCDF4 import Dataset
####################### NAMELIST INPUTS FILES #######################
inpPath = '../02_fields/diurnal'
#inpPath = '../02_fields/topocut'

fieldNames = ['nTOT_PREC', 'cHSURF']
modes = ['', 'f', 'r']
model_modes = ['', 'f']
#ress = [4.4]

i_subDomain = 1 # 0: full domain, 1: alpine region
ssI, domainName = setSSI(i_subDomain, {'4.4':{}, '2.2':{}, '1.1':{}}) 
startTime = datetime(2006,7,11,00)
endTime = datetime(2006,7,19,23)
ssI['time'] = [startTime,endTime] # border values (one value if only one time step desired)
#ssI['diurnal'] = [20,21,22,23,0,1,2,3,4,5,6,7] # list values
#ssI['diurnal'] = [8,9,10,11,12,13,14,15,16,17,18,19] # list values
#####################################################################		

####################### NAMELIST AGGREGATE #######################
# Options: MEAN, SUM 
ag_commnds = {}
#ag_commnds['diurnal'] = 'SUM'

#ag_commnds['rlat'] = 'MEAN'
#ag_commnds['rlon'] = 'MEAN'
#ag_commnds['x_1'] = 'MEAN'
#ag_commnds['y_1'] = 'MEAN'
#####################################################################

####################### NAMELIST PLOT #######################
nDPlot = 1 # How many dimensions should plot have (1 or 2)
i_diffPlot = 0 # Draw plot showing difference filtered - unfiltered # TODO
plotOutDir = '../00_plots'

# 2D PLOT
#plotName = '10_evaluation/2D'
#plotName = '10_evaluation/2D_night'
#plotName = '10_evaluation/2D_day'
# 1D PLOT
plotName = '10_evaluation/1D'

##### 2D Contour ######
contourTranspose = 0 # Reverse contour dimensions?
plotContour = 0 # Besides the filled contour, also plot the contour?
cmapM = 'jet' # colormap for Model output (jet, terrain, inferno, YlOrRd)
axis = 'equal' # set 'equal' if keep aspect ratio, else 'auto'
# COLORBAR Models
autoTicks = 0 # 1 if colorbar should be set automatically
Mmask = 1 # Mask Model values lower than MThrMinRel of maximum value?
MThrMinRel = 0.03 # Relative amount of max value to mask (see Mmask)
Mticks = list(np.arange(10,320,20))
# COLORBAR Models
cmapD = 'bwr' # colormap for Difference output (bwr)
#####################################################################


an = analysis.analysis(inpPath, fieldNames)

#an.subSpaceInds = subSpaceInds
an.ag_commnds = ag_commnds
an.subSpaceInds = ssI
an.i_info = i_info
an.i_resolutions = i_resolutions

# RUN ANALYSIS
if nDPlot == 2:
    ag_commnds['diurnal'] = 'SUM'
    an.ag_commnds = ag_commnds
    an.run()

    radar_masks = {}
    for res in an.resolutions:
        radar_masks[res] = np.isnan(an.vars[fieldNames[0]].ncos[res+'r'].field.vals)


    for res in an.resolutions:
        for mode in an.modes:
            vals = an.vars[fieldNames[0]].ncos[res+mode].field.vals
            #print(res+mode)
            #print(np.nanmean(vals))
            if mode in model_modes:
                vals[radar_masks[res]] = np.nan
                #pass
            #print(np.sum(np.isnan(vals)))
            #print(np.nanmean(vals))

elif nDPlot == 1:
    an.run()

    radar_masks = {}
    for res in an.resolutions:
        radar_masks[res] = np.isnan(an.vars[fieldNames[0]].ncos[res+'r'].field.vals)

    values_masked = {}

    for res in an.resolutions:
        for mode in an.modes:
            vals = an.vars[fieldNames[0]].ncos[res+mode].field.vals
            #print(res+mode)
            #print(np.nanmean(vals))
            if mode in model_modes:
                vals[radar_masks[res]] = np.nan
                #pass
            #print(np.sum(np.isnan(vals)))
            #print(np.nanmean(vals))

            vals = np.nanmean(vals, axis=1)
            vals = np.nanmean(vals, axis=1)
            values_masked[res+mode] = vals


    ag_commnds = {}
    ag_commnds['rlat'] = 'MEAN'
    ag_commnds['rlon'] = 'MEAN'
    ag_commnds['x_1'] = 'MEAN'
    ag_commnds['y_1'] = 'MEAN'
    an.ag_commnds = ag_commnds

    an.run()

    for res in an.resolutions:
        for mode in an.modes:
            vals = an.vars[fieldNames[0]].ncos[res+mode].field.vals
            vals[:,0,0] =  values_masked[res+mode]


#plt.contourf(radar_masks['4.4'].squeeze())
#plt.contourf(an.vars[fieldNames[0]].ncos['4.4f'].field.vals.squeeze())
#plt.show()
#quit()

#an.vars[fieldNames[0]].ncos[res+mode].field.vals = \
#    np.nanmean(an.vars[fieldNames[0]].ncos[res+mode].field.vals, axis=1)
#an.vars[fieldNames[0]].ncos[res+mode].field.vals = \
#    np.nanmean(an.vars[fieldNames[0]].ncos[res+mode].field.vals, axis=1)
#print(an.vars[fieldNames[0]].ncos[res+mode].field.vals.shape)

if i_plot > 0:
    if i_info >= 3:
        print('plotting')
    mainVar = an.vars[an.varNames[0]]
    someField = next(iter(mainVar.ncos.values())).field
    if i_info >= 1:
        print('NONSINGLETONS: ' + str(someField.nNoneSingleton))
    
    if nDPlot == 2 and someField.nNoneSingleton == 2:
        from ncPlots.ncSubplots2D_radar import ncSubplots
        ncs = ncSubplots(an, nDPlot, i_diffPlot, 'HOR')

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
        
        #ncs.plotVar(an.vars[an.varNames[0]])
        (fig,axes,MCB) = ncs.plotVar(an.vars[an.varNames[0]])

        MCB.set_label(r'Total Accumulated Precipitation $[mm]$', fontsize=13*ncs.MAG)
            
        #title = 'Time mean rain rate' 
        #ncs.fig.suptitle(title, fontsize=14)

    elif nDPlot == 1 and someField.nNoneSingleton == 1:
        from ncPlots.ncSubplots1D import ncSubplots
        ncs = ncSubplots(an, nDPlot, i_diffPlot, 'HOR')

        for varName in an.varNames:
            if varName != 'cHSURF':
                ncs.plotVar(an.vars[varName])

        xvals = np.arange(0,25)
        for mI,mode in enumerate(model_modes):
            ax = ncs.axes[0,mI]
            vals = an.vars[fieldNames[0]].ncos['1.1r'].field.vals
            line, = ax.plot(xvals, vals.squeeze(), color='grey', label='OBS')
            if ax.get_legend() is not None:
                lines = ax.get_legend().get_lines()
                texts = ax.get_legend().get_texts()
                labels = [text.get_text() for text in texts]
                labels.append('OBS')
                lines.append(line)
                ax.legend(handles=lines, labels=labels)
            ylim = ax.get_ylim()
            ylim = (ylim[0], ylim[1]*1.05)
            ax.set_ylim(ylim)

            if mI == 0:
                ax.set_ylabel('Rain Rate $[mm$ $h^{-1}]$')
            else:
                ax.set_ylabel('')
            ax.set_xlabel('Hour')


        # PRECIP MEAN DAILY SUM
        x = 3
        yTop = 1.1
        dy = 0.18
        size = 12
        for rowInd,mode in enumerate(model_modes):

            # TODO: Turn around because sum labels are wrong else
            # Don't know why --> it's a mess!
            if mode == 'f':
                mode = ''
            elif mode == '':
                mode = 'f'


            if ncs.orientation == 'VER':
                ax = ncs.axes[rowInd,0]
            elif ncs.orientation == 'HOR':
                ax = ncs.axes[0,rowInd]
            if mode != 'D':
                ax.text(x, yTop+dy, 'Sum:', size=size,
                        bbox=dict(boxstyle='square',ec=(1,1,1,0.5),fc=(1,1,1,0.5)))
            # PLOT ADJUSTMENTS
            ax.set_xlabel('Hour',fontsize=12)
            if mode == '':
                #ax.legend_.remove()
                ax.set_ylabel('',fontsize=12)
            else:
                ax.set_ylabel(r'Rain Rate $[mm$ $h^{-1}]$',fontsize=12)
            ax.set_ylim(0,2.7)



            # MODEL RESOLUTIONS
            for rI,res in enumerate(ncs.ress):
                # GET VALUES AND DIMENSIONS				
                fld = an.vars['nTOT_PREC'].ncos[str(res+mode)].field
                if mode != 'd':
                    sum = str(round(np.sum(fld.vals),1)) + ' mm' 
                    ax.text(x, yTop-dy*rI, sum, color=ncs.colrs[rI], size=size,
                            bbox=dict(boxstyle='square',ec=(1,1,1,0.5),fc=(1,1,1,0.5)))
            # RADAR
            fld = an.vars['nTOT_PREC'].ncos[str(res)+'r'].field
            if mode != 'd':
                sum = str(round(np.sum(fld.vals),1)) + ' mm' 
                ax.text(x, yTop-dy*(rI+1), sum, color='grey', size=size,
                        bbox=dict(boxstyle='square',ec=(1,1,1,0.5),fc=(1,1,1,0.5)))


        #stretchCol = 3.8
        #stretchRow = 3.8
        #ncols = 2; nrows = 1
        #fig, axes = plt.subplots(ncols=ncols, nrows=nrows,
        #                figsize=(ncols*stretchCol,nrows*stretchRow))
        #for mI,mode in enumerate(model_modes):
        #    ax = axes[mI]
        #    for res in an.resolutions:
        #        vals = an.vars[fieldNames[0]].ncos[res+mode].field.vals
        #        ax.plot(vals.squeeze())
        #plt.show()

    else:
        raise ValueError('ERROR: CANNOT MAKE ' + str(nDPlot) + 'D-PLOT WITH ' +
        str(someField.nNoneSingleton) + ' NON-SINGLETON DIMS!')

    
    if i_plot == 1:
        plt.show()
    elif i_plot == 2:
        plotPath = plotOutDir + '/' + plotName+'.png'
        plt.savefig(plotPath, format='png', bbox_inches='tight')
        plt.close('all')
    elif i_plot == 3:
        plotPath = plotOutDir + '/' + plotName+'.pdf'
        plt.savefig(plotPath, format='pdf', bbox_inches='tight')
        plt.close('all')

          


