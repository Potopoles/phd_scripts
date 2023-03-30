from datetime import datetime, timedelta
import numpy as np
import os
os.chdir('00_newScripts/')

from functions import loadObj 

ress = ['4.4', '2.2', '1.1']
#ress = ['4.4', '2.2']
#ress = ['4.4']
modes = ['f', '', 'd']
#i_variables = 'QV' # 'QV' or 'T'
#i_variables = 'T' # 'QV' or 'T'
i_plot = 1
i_diurnal = 1
i_variabless = ['QV', 'T']
i_variabless = ['T']

path = 'alts_2500_6000_Alpine_Region'
#path = 'alts_0_2500_Alpine_Region'
#path = 'alts_0_2500_South_Western_Alps'
#path = 'alts_0_4000_Alpine_Region'
#path = 'alts_800_2200_Alpine_Region'
#path = 'alts_1800_1800_Alpine_Region'
folder = '../06_bulk/' + path
plotOutDir = '../00_plots/06_bulk/'+path
if not os.path.exists(plotOutDir):
    os.mkdir(plotOutDir)
modeNames = ['smoothed', 'raw', 'raw - smoothed']

import matplotlib
if i_plot == 2:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

for i_variables in i_variabless:
    print('######## '+i_variables+' ########')
    if i_variables == 'QV': 
        vars = ['AQVT_TOT', 'AQVT_ADV', 'AQVT_HADV', 'AQVT_ZADV', 'AQVT_TURB', 'AQVT_MIC'] 
        #vars = ['AQVT_ZADV', 'AQVT_ADV', 'AQVT_HADV'] 
        #vars = ['AQVT_TURB']
        #unit = '[g/(kg*h)]'
        #unit = '[1E9*kg/h]'
        unit = '[1/s]'
    elif i_variables == 'T':
        vars = ['ATT_TOT', 'ATT_ADV', 'ATT_HADV', 'ATT_ZADV', 'ATT_RAD', 'ATT_TURB', 'ATT_MIC'] 
        unit = '[K/h]'

    for var in vars:
        #var = vars[varI]
        print(var)
        plotName = var + '.png'

        # PREAPRE DATA FOR PLOTTING
        out = {}
        if i_diurnal:
            out['hrs'] = np.arange(0,25)
        max = -np.Inf
        min = np.Inf
        for res in ress:
            for mode in modes[0:2]:
                if i_variables == 'T':
                    name = 'ATT_'+res+mode
                elif i_variables == 'QV':
                    name = 'AQVT_'+res+mode
                obj = loadObj(folder,name)  

                dates = obj['time'].astype(datetime)
                if not i_diurnal:
                    out['hrs'] = dates

                # MEAN DIURNAL
                #vals = obj[var]/1E9*3600
                vals = obj[var]
                if i_diurnal:
                    hrs = np.arange(0,24)
                    hrVals = np.full(len(hrs), np.nan)
                    for hr in hrs:
                        inds = [i for i in range(0,len(dates)) if dates[i].hour == hr]
                        hrVals[hr] = np.mean(vals[inds])
                    hrVals = np.append(hrVals, hrVals[0])
                    out[res+mode] = hrVals
                else:
                    out[res+mode] = vals

                # calc max min
                vals = out[res+mode]
                max = np.max(vals) if np.max(vals) > max else max
                min = np.min(vals) if np.min(vals) < min else min
            
            # CALCUALTE DIFFERENCE
            out[res+'d'] = out[res+''] - out[res+'f']
            maxd = np.max(out[res+'d'])
            mind = np.min(out[res+'d'])
            max = np.max(out[res+'d']) if np.max(out[res+'d']) > max else max
            min = np.min(out[res+'d']) if np.min(out[res+'d']) < min else min


            #print(out)
            #quit()


        # PLOT
        fig,axes = plt.subplots(1,3, figsize=(12,5))
        for axI,mode in enumerate(modes):
            ax = axes[axI]
            lines = []
            for resI,res in enumerate(ress):
                line, = ax.plot(out['hrs'], out[res+mode])
                lines.append(line)

            ax.legend(lines, labels=ress)
            ax.axhline(y=0, color='k', lineWidth=1)
            if i_diurnal:
                ax.set_xticks([0,6,12,18,24])
                ax.set_xlim((0,24))
            ax.set_ylabel(unit)
            if mode != 'd':
                ax.set_ylim((min,max))
            else:
                centre = (max + min)*0.5
                centred = (maxd + mind)*0.5
                d = centred - centre
                ax.set_ylim((min+d, max+d))
            #ax.set_ylim((min,max))
            ax.grid()
            ax.set_title(modeNames[axI])


        fig.suptitle(var + ' ' + path)
        fig.subplots_adjust(wspace=0.4,
                left=0.10, right=0.95, bottom=0.15, top=0.85)

        if i_plot == 1:
            plt.show()
            plt.close(fig)
        elif i_plot == 2:
            plotPath = plotOutDir + '/' + plotName
            plt.savefig(plotPath, format='png', bbox_inches='tight')
            plt.close(fig)

            
