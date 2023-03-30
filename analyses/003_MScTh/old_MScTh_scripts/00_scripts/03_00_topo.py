#################################
# Calculate domain Average Precipitation
# author: Christoph Heim
# date: 21 10 2017
#################################
import os
os.chdir('00_scripts/')

i_resolutions = 3 # 1 = 4.4, 2 = 4.4 + 2.2, 3 = ...
i_plot = 2 # 0 = no plot, 1 = show plot, 2 = save plot
i_info = 1 # output some information [from 0 (off) to 5 (all you can read)]
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
#inpPath = '../02_fields/topocut'
inpPath = '../02_fields/diurnal'
#fieldNames = ['zQC', 'nHPBL', 'cHSURF']
fieldNames = ['cHSURF','nTOT_PREC']
#####################################################################		

####################### NAMELIST DIMENSIONS #######################
i_subDomain = 0 # 0: full domain, 1: alpine region
ssI, domainName = setSSI(i_subDomain, {'4.4':{}, '2.2':{}, '1.1':{}}) 
ssI_AR, domainName = setSSI(1, {'4.4':{}, '2.2':{}, '1.1':{}}) 
#####################################################################

####################### NAMELIST AGGREGATE #######################
# Options: MEAN, SUM, DIURNAL
ag_commnds = {}
#ag_commnds['rlat'] = 'MEAN'
#ag_commnds['rlon'] = 'MEAN'
ag_commnds['time'] = 'MEAN'
#ag_commnds['altitude'] = 'MEAN'
#####################################################################

####################### NAMELIST PLOT #######################
nDPlot = 2 # How many dimensions should plot have (1 or 2)
plotOutDir = '../00_plots'
plotName = 'domain.png'
plotName = 'domain_Northern_Italy.png'
plotName = 'domain_AR_and_NI.png'
##### 1D PLOT #########

##### 2D Contour ######
contourTranspose = 0 # Reverse contour dimensions?
plotContour = 0 # Besides the filled contour, also plot the contour?
#cmapM = 'terrain' # colormap for Model output (jet, terrain, inferno, YlOrRd)
cmapM = 'Greys_r' # colormap for Model output (jet, terrain, inferno, YlOrRd)
axis = 'equal' # set 'equal' if keep aspect ratio, else 'auto'
# COLORBAR Models
autoTicks = 1 # 1 if colorbar should be set automatically
Mmask = 0 # Mask Model values lower than MThrMinRel of maximum value?
MThrMinRel = 0.15 # Relative amount of max value to mask (see Mmask)
Mticks = [0.0001,0.0002,0.0003,0.0004,0.0005]
Mticks = list(np.arange(0.0002,0.0022,0.0002))
#####################################################################


an = analysis.analysis(inpPath, fieldNames)

an.subSpaceInds = ssI
an.ag_commnds = ag_commnds
an.i_info = i_info
an.i_resolutions = i_resolutions



# RUN ANALYSIS
an.run()

# if import topocut
#rad_1_1 = an.vars[fieldNames[1]].ncos['1.1r'].field.vals.squeeze().filled(fill_value=np.nan)
# if import diurnal
rad_1_1 = an.vars[fieldNames[1]].ncos['1.1r'].field.vals[3,:,:].squeeze().filled(fill_value=np.nan)
rad_1_1[:,:ssI_AR['1.1']['rlon'][0]] = np.nan
rad_1_1[ssI_AR['1.1']['rlat'][-1]:,:] = np.nan
# fix some area with missing values for cosmetical reasons
rad_1_1[490:510,650:670] = 1


width = 2
max_sum = (width*2+1)**2
mask = rad_1_1.copy()
for j in range(0,rad_1_1.shape[0]):
    for i in range(0,rad_1_1.shape[1]):
        #i = 1
        #j = 3
        yrange = np.minimum(np.maximum(
                    np.arange((j - width), (j + width + 1)).astype(np.int),0),
                        rad_1_1.shape[0]-1)
        xrange = np.minimum(np.maximum(
                    np.arange((i - width), (i + width + 1)).astype(np.int),0),
                        rad_1_1.shape[1]-1)
        if np.sum(np.isnan(rad_1_1[yrange,xrange])) == 0:
            mask[j,i] = np.nan
rad_1_1_line = rad_1_1.copy()
rad_1_1_line[np.isnan(mask)] = np.nan
rad_1_1_line[~np.isnan(rad_1_1_line)] = 1
rad_1_1_line[10,10] = 0



import matplotlib
if i_plot == 2:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt


if i_plot > 0:
    if i_info >= 3:
        print('plotting')
    mainVar = an.vars[an.varNames[0]]
    nco = mainVar.ncos['1.1']
    someField = next(iter(mainVar.ncos.values())).field
    if i_info >= 1:
        print('NONSINGLETONS: ' + str(someField.nNoneSingleton))
    
    if nDPlot == 2 and someField.nNoneSingleton == 2:
        import ncPlots.ncPlot2D as ncPlot
        ncp = ncPlot.ncPlot2D(nco)

        ncp.contourTranspose = contourTranspose
        ncp.plotContour = plotContour
        ncp.cmapM = cmapM
        ncp.axis = axis
        ncp.autoTicks = autoTicks
        ncp.Mmask = Mmask
        ncp.MThrMinRel = MThrMinRel
        ncp.Mticks = Mticks
   
        fig, ax = ncp.plotNCO(nco)

        text_size = 25
        df = 50
        col2 = 'red'
        col3 = 'red'

        col_D = 'white'
        col_D = 'orange'
        
        # ALPINE REGION
        x0 = 50; x1 = 237
        y0 = 41; y1 = 155
        #ax.plot([220, 1042.8], [180.4, 180.4], '-k')
        #ax.plot([220, 1042.8], [682, 682], '-k')
        #ax.plot([220, 220], [180.4, 682], '-k')
        #ax.plot([1042.8, 1042.8], [180.4, 682], '-k')
        ax.plot([x0*4.4, x1*4.4], [y0*4.4, y0*4.4], '-w', linewidth=2)
        ax.plot([x0*4.4, x1*4.4], [y1*4.4, y1*4.4], '-w', linewidth=2)
        ax.plot([x0*4.4, x0*4.4], [y0*4.4, y1*4.4], '-w', linewidth=2)
        ax.plot([x1*4.4, x1*4.4], [y0*4.4, y1*4.4], '-w', linewidth=2)
        ax.text(x1*4.4-df, y0*4.4+df/3, 'A', fontsize=text_size, color='w')

        # First part: DOMAIN D
        x0 = 50; x1 = 164
        y0 = 71; y1 = 155
        ax.text(665, y1*4.4-df, 'D', fontsize=text_size, color=col_D)
        shift = 3
        ax.plot([x0*4.4+shift, x0*4.4+shift], [y0*4.4, (y1-1)*4.4], '-', linewidth=1.5, color=col_D)
        ax.plot([(x0+1)*4.4, x1*4.4], [y1*4.4-shift, y1*4.4-shift], '-', linewidth=1.5, color=col_D)

        # NORTHERN ITALY
        x0 = 95; x1 = 160
        y0 = 60; y1 = 100
        #ax.plot([418, 704], [264, 264], '--k')
        #ax.plot([418, 704], [440, 440], '--k')
        #ax.plot([418, 418], [264, 440], '--k')
        #ax.plot([704, 704], [264, 440], '--k')
        ax.plot([x0*4.4, x1*4.4], [y0*4.4, y0*4.4], '--', lineWidth=2.5, color=col2)
        ax.plot([x0*4.4, x1*4.4], [y1*4.4, y1*4.4], '--', lineWidth=2.5, color=col2)
        ax.plot([x0*4.4, x0*4.4], [y0*4.4, y1*4.4], '--', lineWidth=2.5, color=col2)
        ax.plot([x1*4.4, x1*4.4], [y0*4.4, y1*4.4], '--', lineWidth=2.5, color=col2)
        ax.text(x1*4.4-df, y1*4.4-df, 'B', fontsize=text_size, color=col2)

        # CROSSSECT
        #x0 = 107; x1 = 130
        #y0 = 50; y1 = 135
        x0 = 110; x1 = 135
        y0 = 52; y1 = 135
        ax.plot([x0*4.4, x1*4.4], [y0*4.4, y0*4.4], '-', lineWidth=2, color=col3)
        ax.plot([x0*4.4, x1*4.4], [y1*4.4, y1*4.4], '-', lineWidth=2, color=col3)
        ax.plot([x0*4.4, x0*4.4], [y0*4.4, y1*4.4], '-', lineWidth=2, color=col3)
        ax.plot([x1*4.4, x1*4.4], [y0*4.4, y1*4.4], '-', lineWidth=2, color=col3)
        ax.text(x1*4.4-df, y1*4.4-df, 'C', fontsize=text_size, color=col3)
            
        #title = 'topography' 
        #ncp.fig.suptitle(title, fontsize=14)

        dimx = an.vars['cHSURF'].ncos['1.1'].field.dims['rlon']
        dimy = an.vars['cHSURF'].ncos['1.1'].field.dims['rlat']
        [gridx, gridy] = np.meshgrid(dimx.vals, dimy.vals)
        from matplotlib.colors import BoundaryNorm

        #rad_1_1_line = rad_1_1_line[0,:,:]

        #print(np.nanmean(rad_1_1_line))
        #quit()
        if col_D == 'orange':
            CF = ax.pcolormesh(gridx, gridy, rad_1_1_line, cmap='Wistia')
        elif col_D == 'white':
            CF = ax.pcolormesh(gridx, gridy, rad_1_1_line, cmap='Greys_r')
        else:
            raise ValueError()
        #CF = ax.pcolormesh(gridx, gridy, rad_1_1_line, cmap='Greys')
        res = 1.1
        nth_ind = 10
        x0_inds = np.arange(0,900,nth_ind)
        for i in range(0,len(x0_inds)):
            x0_km = x0_inds[i]*res
            if np.sum(~np.isnan(rad_1_1[:,x0_inds[i]])) > 0:
                non_nan_yinds = np.argwhere(~np.isnan(rad_1_1[:,x0_inds[i]]))
                y0_km = non_nan_yinds[0]*res
                y1_km = non_nan_yinds[-1]*res
                ax.plot([x0_km,x0_km], [y0_km, y1_km],
                        '-w', color=col_D, linewidth=0.3)
        y0_inds = np.arange(0,900,nth_ind)
        for j in range(0,len(y0_inds)):
            y0_km = y0_inds[j]*res
            if np.sum(~np.isnan(rad_1_1[y0_inds[j],:])) > 0:
                non_nan_xinds = np.argwhere(~np.isnan(rad_1_1[y0_inds[j],:]))
                x0_km = non_nan_xinds[0]*res
                x1_km = non_nan_xinds[-1]*res
                ax.plot([x0_km,x1_km], [y0_km, y0_km],
                        '-', color=col_D, linewidth=0.3)


    else:
        raise ValueError('ERROR: CANNOT MAKE ' + str(nDPlot) + 'D-PLOT WITH ' +
        str(someField.nNoneSingleton) + ' NON-SINGLETON DIMS!')

    
    if i_plot == 1:
        plt.show()
    elif i_plot == 2:
        plotPath = plotOutDir + '/' + plotName
        plt.savefig(plotPath, format='png', bbox_inches='tight')

          


