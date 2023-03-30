from datetime import datetime, timedelta
import numpy as np
import os
os.chdir('00_newScripts/')

from functions import loadObj 


## VERY FAST! CAN BE DONE ALL TOGETHER WITHIN DEBUG 30 MIN WITH 12 CPUS

ress = ['4.4', '2.2', '1.1']
#ress = ['4.4', '2.2']
#ress = ['2.2']
#ress = ['4.4']
#ress = ['1.1']
modes = ['f', '', 'd']

i_plot = 3
i_var_plot_mode = 2
i_print_values = 0

subdomain = 'Alpine_Region'
subdomain = 'Northern_Italy'

if subdomain == 'Alpine_Region':
    alts = 'alts_0_2500'
    #alts = 'alts_2000_4000'
    #alts = 'alts_0_10000'
    #alts = 'alts_2500_10000'
elif subdomain == 'Northern_Italy':
    alts = 'alts_0_2000'
    #alts = 'alts_2000_4000'
    #alts = 'alts_0_10000'
    #alts = 'alts_2000_10000'

path = alts + '_' + subdomain

fact = 1

varGroup = 'AQVT'
plotName = 'AQVT_' +subdomain + '_' + alts +'_' + str(i_var_plot_mode)
if i_var_plot_mode == 0:
    vars =      ['AQVT_TOT', 'AQVT_ADV', 'AQVT_TURB', 'AQVT_MIC']
    varLabels = ['TOT'     , 'ADV'     , 'TURB'     , 'MIC'     ]
    ltypes = ['-', '-', ':', '-.']
    lwidths = [1.8,0.8,1,1]
elif i_var_plot_mode == 1:
    vars =      ['AQVT_TOT', 'AQVT_ADV', 'AQVT_ZADV', 'AQVT_MIC', 'AQVT_HADV']
    varLabels = ['TOT'     , 'ADV'     , 'ZADV'     , 'MIC'     , 'HADV']
    ltypes = ['-', '-', ':', '-.', '--']
    lwidths = [1.8,0.8,1,1,2]
elif i_var_plot_mode == 2:
    vars =      ['AQVT_TOT', 'AQVT_ADV', 'AQVT_ZADV', 'AQVT_HADV']
    varLabels = ['TOT'     , 'ADV'     , 'ZADV'     , 'HADV']
    ltypes = ['-', '-', ':', '-.']
    lwidths = [1.8,0.8,1,1]
    fact = fact*2
unit = r'$[mm$ $h^{-1}]$'
ylabel = 'Net Moistening '+unit


###########################################
if subdomain == 'Alpine_Region':
    fact = fact*0.5
#    # ALPINE REGION
#    minm = -1.0
#    maxm = 1.0
#    mind = -0.5
#    maxd = 0.5
###########################################
if subdomain == 'Northern_Italy':
    fact = fact*1
#    # NORTHERN ITALY PLAINS
#    minm = -0.5
#    maxm = 0.5
#    mind = -0.25
#    maxd = 0.25
###########################################

minm = -1.0*fact
maxm =  1.0*fact
mind = -0.5*fact
maxd =  0.5*fact

if i_plot == 3:
    if (subdomain == 'Alpine_Region') and (alts == 'alts_0_2500'):
        minm = -0.75
        maxm =  0.5
        mind = -0.2
        maxd =  0.2
    if (subdomain == 'Northern_Italy') and (alts == 'alts_0_2000'):
        minm = -0.75
        maxm =  0.5
        mind = -0.2
        maxd =  0.2


    

folder = '../06_bulk/' + path
#plotOutDir = '../00_plots/06_bulk/'+path
plotOutDir = '../00_plots/06_bulk/'
if not os.path.exists(plotOutDir):
    os.mkdir(plotOutDir)
modeNames = ['SM', 'RAW', 'RAW - SM']

colrs = [(0,0,0), (0,0,1), (1,0,0)]
labelsize = 16
titlesize = 18
ticklabelsize = 12
legend_fontsize = 12

import matplotlib
if i_plot > 1:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

# PLOT
fig,axes = plt.subplots(1,3, figsize=(12,4))


varLegendLines = []
for varI,var in enumerate(vars):
    print(var)

    # PREAPRE DATA FOR PLOTTING
    out = {}
    out['hrs'] = np.arange(0,25)
    max = -np.Inf
    min = np.Inf
    for res in ress:
        if i_print_values:
            print(res)
        for mode in modes[0:2]:
            name = varGroup+'_'+res+mode
            obj = loadObj(folder,name)  
            dates = obj['time'].astype(datetime)


            # MEAN DIURNAL
            vals = obj[var]#*6.8E6
            hrs = np.arange(0,24)
            hrVals = np.full(len(hrs), np.nan)
            for hr in hrs:
                inds = [i for i in range(0,len(dates)) if dates[i].hour == hr]
                hrVals[hr] = np.mean(vals[inds])

            hrVals = np.append(hrVals, hrVals[0])
            hrs = np.append(hrs, 25)
            out[res+mode] = hrVals
            out['hrs'] = hrs

        # CALCUALTE DIFFERENCE
        out[res+'d'] = out[res+''] - out[res+'f']
        if i_print_values:
            print('RAW ' + str(np.nanmean(out[res+'f'])))
            print('RAW ' + str(np.nanmean(out[res+''])))
            print('RAW ' + str(np.nanmean(out[res+'d'])))
            print()

    # PLOT
    for axI,mode in enumerate(modes):
        #print(mode)
        ax = axes[axI]
        ax.tick_params(axis='both', which='major', labelsize=ticklabelsize)
        lines = []
        for resI,res in enumerate(ress):
            if mode == 'd' and res == '4.4':
                pass
            else:
                line, = ax.plot(out['hrs'], out[res+mode], linestyle=ltypes[varI],
                                color=colrs[resI], lineWidth=lwidths[varI])
            lines.append(line)
            #if (axI == 0) and (resI == 0):
            if varI == 0:
                varLegendLines.append(line)

#quit()


for axI,mode in enumerate(modes):
    ax = axes[axI]
    if axI == 1:
        ax.legend(lines, labels=ress, fontsize=legend_fontsize)
    elif axI == 0:
        leg = ax.legend(varLegendLines, labels=varLabels, fontsize=legend_fontsize)
        for i in range(0,len(vars)):
            leg.legendHandles[i].set_color('k')
            leg.legendHandles[i].set_linestyle(ltypes[i])
            leg.legendHandles[i].set_linewidth(lwidths[i])

    ax.axhline(y=0, color='k', lineWidth=1)
    ax.set_xticks([0,6,12,18,24])
    ax.set_xlim((0,24))
   
    #from matplotlib.ticker import FormatStrFormatter
    #ax.yaxis.set_major_formatter(FormatStrFormatter('%.2E'))
    from matplotlib.ticker import ScalarFormatter
    yfmt = ScalarFormatter()
    yfmt.set_powerlimits((-3,3))
    ax.yaxis.set_major_formatter(yfmt)

    if axI == 0:
        ax.set_ylabel(ylabel,fontsize=labelsize)
    ax.set_xlabel('Hour',fontsize=labelsize)

    if axI == 2:
        ax.set_ylim((mind,maxd))
    else:
        ax.set_ylim((minm,maxm))
    ax.grid()
    ax.set_title(modeNames[axI], fontsize=titlesize)

if i_plot < 3:
    fig.suptitle(subdomain + ' ' + alts)
fig.subplots_adjust(wspace=0.23,
        left=0.07, right=0.96, bottom=0.15, top=0.85)



if i_plot == 1:
    plt.show()
    plt.close(fig)
elif i_plot == 2:
    plotPath = plotOutDir + '/' + plotName+'.png'
    plt.savefig(plotPath, format='png', bbox_inches='tight')
    plt.close(fig)
elif i_plot == 3:
    plotPath = plotOutDir + '/' + plotName+'.pdf'
    plt.savefig(plotPath, format='pdf', bbox_inches='tight')
    plt.close('all')

    
        
