import os
from netCDF4 import Dataset
from ncClasses.subdomains import setSSI
from datetime import datetime, timedelta
import numpy as np
from functions import loadObj
os.chdir('00_scripts/')


ress = ['4.4', '2.2', '1.1']
#ress = ['4.4', '2.2']
#ress = ['4.4']
modes = ['f', '']
modeNames = ['SM', 'RAW', '(RAW-SM)/SM']
i_save = 1
i_plotVar = 'CB'
#i_plotVar = 'CT'
i_plotVar = 'TH'
plotOutDir = '../00_plots/08_cloud_cluster'
domainName = 'Alpine_Region'
domainName = 'Northern_Italy'


# delta = 100
deltaBelow = 100
bins = np.arange(-50,6051,deltaBelow)
bins2 = np.arange(7500,10501,1000)
bins_borders = np.concatenate((bins,bins2))
bins = np.arange(0,6001,deltaBelow)
bins2 = np.arange(7000,10001,1000)
bins_centred = np.concatenate((bins,bins2))



## delta = 200
#deltaBelow = 200
#bins = np.arange(-100,6101,deltaBelow)
#bins2 = np.arange(7500,10501,1000)
#bins_borders = np.concatenate((bins,bins2))
#bins = np.arange(0,6001,deltaBelow)
#bins2 = np.arange(7000,10001,1000)
#bins_centred = np.concatenate((bins,bins2))


# delta = 300
deltaBelow = 300
bins = np.arange(-150,6151,deltaBelow)
bins2 = np.arange(7500,10501,1000)
bins_borders = np.concatenate((bins,bins2))
bins = np.arange(0,6001,deltaBelow)
bins2 = np.arange(7000,10001,1000)
bins_centred = np.concatenate((bins,bins2))


## delta = 400
#deltaBelow = 400
#bins = np.arange(-200,6201,deltaBelow)
#bins2 = np.arange(7500,10501,1000)
#bins_borders = np.concatenate((bins,bins2))
#bins = np.arange(0,6001,deltaBelow)
#bins2 = np.arange(7000,10001,1000)
#bins_centred = np.concatenate((bins,bins2))


## delta = 500
#deltaBelow = 500
#bins = np.arange(-250,6251,deltaBelow)
#bins2 = np.arange(7500,10501,1000)
#bins_borders = np.concatenate((bins,bins2))
#bins = np.arange(0,6001,deltaBelow)
#bins2 = np.arange(7000,10001,1000)
#bins_centred = np.concatenate((bins,bins2))


# delta = 1000
deltaBelow = 1000
bins_borders = np.arange(-500,10501,1000)
bins_centred = np.arange(0,10001,1000) 

print(bins_borders)
print(bins_centred)

folder = '../08_lwp_and_clustering'
name = 'cloud_vertical_'+domainName
out = loadObj(folder,name)



vars = ['CT','CB', 'TH']
for res in ress:
    for mode in modes:
        for var in vars:
            vals = out[res+mode][var]['vals']
            vals = vals[vals != -999] 
            hist_vals = np.histogram(vals, bins_borders)[0] 

            # ADJUST FOR DIFFERENT RESOLUTION
            hist_vals[bins_centred > 6000] = hist_vals[bins_centred > 6000]/ \
                                            (1000/deltaBelow)

            #### add lower values to 6000 for transition from high resolution to low
            #val6000 = hist_vals[bins_centred == 6000]
            #val7000 = hist_vals[bins_centred == 7000]
            #logmean = (val7000 - val6000)/(np.log(val7000) - np.log(val6000))
            #print(val6000 - logmean)
            #print(logmean - val7000)
            #ratio = logmean/val6000
            #print(logmean/val6000)

            #moveFreq = hist_vals[bins_centred == 6000]*ratio
            #print(moveFreq)

            #hist_vals[bins_centred == 6000] = hist_vals[bins_centred == 6000] - moveFreq
            #hist_vals[bins_centred == 7000] = hist_vals[bins_centred == 7000] + moveFreq
            #hist_vals[bins_centred == 6000] = hist_vals[bins_centred == 6000] - moveFreq

            #hist_vals[bins_centred == 6000] = hist_vals[bins_centred == 6000] + \
            #        np.sum(hist_vals[(bins_centred >= 5700) & (bins_centred < 6000)])

            out[res+mode][var]['pdf'] = hist_vals

# DIFFERENCE
minNumb = 30
for res in ress:
    out[res+'d'] = {}
    for var in vars:
        out[res+'d'][var] = {}
        raw = out[res+''][var]['pdf']
        smo = out[res+'f'][var]['pdf']
        # create mask
        mask = np.full(len(raw),1)
        mask[smo < minNumb] = 0
        mask[raw < minNumb] = 0
        # calc relative frequency 
        raw = raw/np.sum(raw)
        smo = smo/np.sum(smo)

        out[res+'f'][var]['pdf'] = smo
        out[res+''][var]['pdf'] = raw
        # create difference
        out[res+'d'][var]['pdf'] = []
        out[res+'d'][var]['pdf'] = (raw - smo)/smo
        #out[res+'d'][var]['pdf'].append(out[res+''][var]['pdf'])
        out[res+'d'][var]['pdf'][mask == 0] = np.nan
        #if var == 'TH':
        #    print(out[res+'d'][var]['pdf'][0])
modes.append('d')

import matplotlib
if i_save > 0:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

colrs = [(0,0,0), (0,0,1), (1,0,0)]
labelsize = 12
titlesize = 14

var = i_plotVar
handles = []
labels = []
fig,axes = plt.subplots(1,3, figsize=(12,4))
for rI,res in enumerate(ress):
    for mI,mode in enumerate(modes):
        ax = axes[mI]
        pdf = out[res+mode][var]['pdf']
        #alts = out[res+mode][var]['pdf'][1][0:-1]+500
        if mode in ['', 'f']:
            line, = ax.semilogy(bins_centred,pdf,color=colrs[rI])
            ax.set_ylim((1E-4,1E0))
            if mode == '':
                handles.append(line)
                labels.append(res)
        elif mode == 'd':
            ax.plot(bins_centred,pdf,color=colrs[rI])
            if var == 'CB':
                ax.set_ylim((-1,3))
            else:
                ax.set_ylim((-1,1))
            ax.axhline(y=0,color='k',lineWidth=1)
        ax.set_xlim((0,10000))
        ax.set_title(modeNames[mI],fontsize=titlesize)
        ax.grid()
        if mode == 'f':
            ax.set_ylabel('Frequency',fontsize=labelsize)
        if var == 'CB':
            ax.set_xlabel('Cloud Base [$m$]',fontsize=labelsize)
        elif var == 'CT':
            ax.set_xlabel('Cloud Top [$m$]',fontsize=labelsize)
        elif var == 'TH':
            ax.set_xlabel('Cloud Depth [$m$]',fontsize=labelsize)
axes[0].legend(handles,labels)
#plt.suptitle(var)
fig.subplots_adjust(wspace=0.23,left=0.07, right=0.95, bottom=0.15, top=0.85)
if i_save == 1:
    plotName = 'cloud_vertical_'+var+'_'+domainName+'.png'
    plt.savefig(plotOutDir+'/'+plotName)
    plt.close('all')
if i_save == 2:
    plotName = 'cloud_vertical_'+var+'_'+domainName+'.pdf'
    plt.savefig(plotOutDir+'/'+plotName, format='pdf')
    plt.close('all')
else:
    plt.show()
#print(sums)
