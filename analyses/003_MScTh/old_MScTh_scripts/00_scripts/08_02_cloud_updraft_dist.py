from netCDF4 import Dataset
import numpy as np

day0 = 11
day1 = 19
ress = [4.4, 2.2, 1.1]
#ress = [4.4, 2.2]
modes = ['', 'f']
i_save = 1
outPath = '00_plots/08_cloud_cluster/'
nbins = 50

import matplotlib
if i_save:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

days = np.repeat(np.arange(day0,day1+1),24)
hours = np.tile(np.arange(0,24),day1-day0+1)

allWms = []
outRess = []
outModes = []
labels = []

for res in ress:
    for mode in modes:
        print(str(res)+mode)
        inpPath = '01_rawData/cloud_cluster/'+str(res)+mode
        wms = []
        for i in range(0,len(days)):
            file = 'lffd200607'+str(days[i]).zfill(2) + str(hours[i]).zfill(2) + 'z.nc'
            fullPath = inpPath + '/' + file
            nc = Dataset(fullPath, 'r')
            wm = nc['WM'][:].squeeze()
            wm = [wm] if wm.ndim == 0 else wm
            wms.extend(wm)
        wms = np.asarray(wms)
        print('n clouds: ' + str(wms.shape[0]))
        allWms.append(wms)
        outRess.append(str(res))
        outModes.append(mode)
        labels.append(str(res)+mode)

bins = np.linspace(0,10,num=nbins)
binsCentred = bins[0:(len(bins)-1)] + np.diff(bins)/2
# CREATE HISTOGRAMS
freqs = []
nclouds = []
for wms in allWms:
    ncloud = np.histogram(wms, bins=bins)
    nclouds.append(ncloud[0])
    freq = ncloud[0]/len(wms)
    freqs.append(freq)


#### PLOT ALL RESS TOGETHER
#fig = plt.figure(figsize=(6,7))
#handles = []
#for i in range(0,len(freqs)):
#    if outModes[i] == 'f':
#        lstyle = '--'
#    else:
#        lstyle = '-'
#    line, = plt.semilogy(binsCentred, freqs[i], lstyle) 
#    handles.append(line)
#plt.legend(handles, labels)
#plt.xlabel('mean updraft [m/s]')
#plt.ylabel('relative frequency')
#plt.xlim((0,10))
#plt.ylim((1E-6,1E0))
#plt.title('Cloud Updraft Distribution')
#plt.grid()
#if i_save:
#    outName = 'cloud_updraft_dist.png'
#    plt.savefig(outPath + outName)
#else:
#    plt.show()
#plt.close(fig)



### PLOT RES SEPARATELY AND DIFFERENCE BETWEEN MODES
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(11,7))
for i in range(0,len(ress)):
    # ABSOLUTE VALUES
    ax = axes[0,i]
    lineRaw, = ax.semilogy(binsCentred, freqs[i*2], '-') 
    lineSmoothed, = ax.semilogy(binsCentred, freqs[i*2+1], '--') 
    ax.legend([lineRaw, lineSmoothed], ['raw','smoothed'])
    ax.set_xlabel('mean updraft [m/s]')
    ax.set_ylabel('relative frequency')
    ax.set_xlim((0,10))
    #ax.set_ylim((1E0,1E5))
    ax.grid()
    ax.set_title(str(ress[i]))
    
    # MASKING OF VALUES WITH SMALL NUMBER OF SAMPLES 
    minSamples = 100
    nRaw = nclouds[i*2]
    nSmooth = nclouds[i*2+1]
    mask = np.full(len(nRaw),1)
    mask[nRaw < minSamples] = 0
    mask[nSmooth < minSamples] = 0

    # DIFFERENCE 
    ax = axes[1,i]
    raw = freqs[i*2]
    sm = freqs[i*2+1]
    raw[raw == 0] = np.nan
    sm[sm == 0] = np.nan
    ratio = (raw - sm)/sm
    ratio[mask == 0] = np.nan
    line, = ax.plot(binsCentred, ratio, '-', color='darkgreen') 
    ax.axhline(y=0, color='k', lineWidth=0.5)
    ax.set_xlabel('mean updraft [m/s]')
    ax.set_ylabel('(raw-smoothed)/smoothed')
    ax.set_ylim((-1,1))
    ax.set_xlim((0,10))
    ax.grid()
    ax.set_title(str(ress[i]))
plt.suptitle('Cloud Updraft Distribution and Relative Difference')
plt.subplots_adjust(left=0.07, right=0.95, top=0.92, bottom=0.08, wspace=0.27, hspace=0.33)
if i_save:
    outName = 'cloud_updraft_dist_and_diff.png'
    plt.savefig(outPath + outName)
else:
    plt.show()
plt.close(fig)
