from netCDF4 import Dataset
import numpy as np

day0 = 11
day1 = 19 
ress = [4.4, 2.2, 1.1]
ress = [4.4]
modes = ['', 'f']
i_save = 0
outPath = '00_plots/08_cloud_cluster/'
nbins = 50
i_subdomain = 1
from ncClasses.subdomains import setSSI
ssI, domainName = setSSI(i_subdomain, {'4.4':{}, '2.2':{}, '1.1':{}}) 

import matplotlib
if i_save:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

days = np.repeat(np.arange(day0,day1+1),24)
hours = np.tile(np.arange(0,24),day1-day0+1)

allSizes = []
outRess = []
outModes = []
labels = []

for res in ress:
    xmin = ssI[str(res)]['rlon'][0]
    xmax = ssI[str(res)]['rlon'][-1]
    ymin = ssI[str(res)]['rlat'][0]
    ymax = ssI[str(res)]['rlat'][-1]
    for mode in modes:
        print(str(res)+mode)
        inpPath = '01_rawData/cloud_cluster/'+str(res)+mode
        sizes = []
        for i in range(0,len(days)):
            file = 'lffd200607'+str(days[i]).zfill(2) + str(hours[i]).zfill(2) + 'z.nc'
            fullPath = inpPath + '/' + file
            nc = Dataset(fullPath, 'r')

            factor = np.power(res,2)

            xc = nc['XCENTER'][:]
            yc = nc['YCENTER'][:]
            mask = np.argwhere((
                (xc >= xmin) & (xc <= xmax) & (
                yc >= ymin) & (yc <= ymax)).squeeze()).squeeze()

            inp = nc['SC'][:].squeeze()
            if inp.ndim > 0:
                size = inp[mask]*factor
            else:
                size = np.asarray([])
            #size = factor*nc['SC'][:].squeeze()
            size = [size] if size.ndim == 0 else size
            sizes.extend(size)
        sizes = np.asarray(sizes)
        print('n clouds: ' + str(sizes.shape[0]))
        allSizes.append(sizes)
        outRess.append(str(res))
        outModes.append(mode)
        labels.append(str(res)+mode)

bins = np.logspace(0,5,num=nbins)
binsCentred = bins[0:(len(bins)-1)] + np.diff(bins)/2

# CREATE HISTOGRAMS
nclouds = []
freqs = []
for sizes in allSizes:
    hist = np.histogram(sizes, bins=bins)
    ncloud = hist[0]
    freq = ncloud/len(sizes)
    nclouds.append(ncloud)
    freqs.append(freq)


### Relative cloud size frequency distribution
fig = plt.figure(figsize=(6,7))
handles = []
for i in range(0,len(freqs)):
    if outModes[i] == 'f':
        lstyle = '--'
    else:
        lstyle = '-'
    line, = plt.loglog(binsCentred, freqs[i], lstyle) 
    handles.append(line)
plt.legend(handles, labels)
plt.xlabel('cloud size [$km^2$]')
plt.ylabel('relative frequency')
plt.xlim((2E0,1E5))
plt.ylim((5E-6,2E-1))
plt.title('Relative Cloud Size Frequency Distribution')
plt.grid()
if i_save:
    outName = 'cloud_size_relFreq_dist.png'
    plt.savefig(outPath + outName)
else:
    plt.show()
plt.close(fig)

### Absolute cloud number distribution
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(11,7))
handles = []
for i in range(0,len(ress)):
    # ABSOLUTE VALUES
    ax = axes[0,i]
    nClRaw = nclouds[i*2]
    nClSmo = nclouds[i*2+1]
    lineRaw, = ax.loglog(binsCentred, nClRaw, '-') 
    lineSmoothed, = ax.loglog(binsCentred, nClSmo, '--') 
    ax.legend([lineRaw, lineSmoothed], ['raw      ('+str(np.sum(nclouds[i*2]))+')',
                                        'smoothed ('+str(np.sum(nclouds[i*2+1]))+')'])

    # MASKING OF VALUES WITH SMALL AMOUNT OF CLOUDS
    minNClouds = 50
    mask = np.full(len(nClRaw),1)
    mask[nClRaw < minNClouds] = 0
    mask[nClSmo < minNClouds] = 0

    ax.set_xlabel('cloud size [$km^2$]')
    ax.set_ylabel('number of clouds')
    ax.set_xlim((1E0,1E5))
    ax.set_ylim((1E0,1E5))
    ax.grid()
    ax.set_title(str(ress[i]))

    # RELATIVE DIFFERENCE 
    ax = axes[1,i]
    raw = nclouds[i*2].astype(np.float)
    sm = nclouds[i*2+1].astype(np.float)
    raw[raw == 0] = np.nan
    sm[sm == 0] = np.nan
    ratio = (raw - sm)/sm
    ratio[mask == 0] = np.nan
    line, = ax.semilogx(binsCentred, ratio, '-', color='darkgreen') 
    ax.axhline(y=0, color='k', lineWidth=0.5)
    ax.set_xlabel('cloud size [$km^2$]')
    ax.set_ylabel('(raw-smoothed)/smoothed')
    ax.set_ylim((-1,1))
    ax.set_xlim((1E0,1E5))
    ax.grid()
    ax.set_title(str(ress[i]))
    sumRaw = np.sum(nclouds[i*2])
    sumSmoothed = np.sum(nclouds[i*2+1])
    sumRatio = sumRaw/sumSmoothed
    ax.text(2E0, 0.8, 'raw/smoothed: '+str(np.round(sumRatio,2)))
plt.suptitle('Absolute Cloud Size Distribution and Relative Difference')
plt.subplots_adjust(left=0.07, right=0.95, top=0.92, bottom=0.08, wspace=0.27, hspace=0.33)
if i_save:
    outName = 'cloud_size_absFreq_dist_and_diff.png'
    plt.savefig(outPath + outName)
else:
    plt.show()
plt.close(fig)
