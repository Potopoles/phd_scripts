from netCDF4 import Dataset
import numpy as np

day0 = 11
#day0 = 12
day1 = 19 
#day1 = 12 
ress = [4.4, 2.2, 1.1]
#ress = [4.4, 2.2]
#ress = [4.4]

modes = ['', 'f']
i_plot = 3
plotOutDir = '00_plots/08_cloud_cluster'
plotName = 'cloud_size_absFreq_dist_and_diff_NEW'
nbins = 40
minNClouds = 30
i_subdomain = 1
from ncClasses.subdomains import setSSI
ssI, domainName = setSSI(i_subdomain, {'4.4':{}, '2.2':{}, '1.1':{}}) 

colrs = [(0,0,0), (0,0,1), (1,0,0)]
labelsize = 13
titlesize = 16

import matplotlib
if i_plot > 1:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

days = np.repeat(np.arange(day0,day1+1),24)
hours = np.tile(np.arange(0,24),day1-day0+1)


allSizes = {}
outRess = []
outModes = []
labels = []

########################################################################
# 
########################################################################
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
        #allSizes.append(sizes)
        allSizes[str(res)+mode] = sizes
        outRess.append(str(res))
        outModes.append(mode)
        labels.append(str(res)+mode)


########################################################################
# GENERATE BINS
########################################################################
# old way (same bins for every resolution)
#bins = np.logspace(0,5,num=nbins)
#binsCentred = bins[0:(len(bins)-1)] + np.diff(bins)/2

# new way (specific bins for every resolution)
bins_res = {}
bins_centred_res = {}
for res in ress:
    bins = np.logspace(0,5,num=nbins)
    thresh_ind = np.argwhere(np.diff(bins) >= float(res)**2)[0][0]
    thresh_val = bins[thresh_ind]
    linear_spacing = []
    i = 1
    while float(res)**2*i <= thresh_val:
        linear_spacing.append(float(res)**2*i - float(res)**2/2)
        i += 1
    bins = bins[thresh_ind:]
    both = []; both.extend(linear_spacing); both.extend(bins)
    bins_centred = both[0:(len(both)-1)] + np.diff(both)/2
    bins_res[str(res)] = both
    bins_centred_res[str(res)] = bins_centred

#print(bins_res)
#print()
#print(bins_centred_res)
#quit()

########################################################################
# CALCULATE HISTOGRAMS
########################################################################
nclouds = {}
for res in ress:
    for mode in modes:
        hist = np.histogram(allSizes[str(res)+mode], bins=bins_res[str(res)])
        ncloud = hist[0]

        ncloud = ncloud.astype(np.float)
        ncloud[ncloud < 0.9] = np.nan

        nclouds[str(res)+mode] = ncloud

########################################################################
#  CREATE PLOTS
########################################################################
### Absolute cloud number distribution
colrs = [(0,0,0), (0,0,1), (1,0,0)]
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(11,4))
handles = []
modeStrings = ['SM', 'RAW', '(RAW - SM)/SM']


for rI,res in enumerate(ress):

    # ABSOLUTE VALUES
    nClRaw = nclouds[str(res)+'']
    nClSmo = nclouds[str(res)+'f']
    line, = axes[0].loglog(bins_centred_res[str(res)], nClSmo, '-', color=colrs[rI]) 
    axes[1].loglog(bins_centred_res[str(res)], nClRaw, '-', color=colrs[rI]) 
    handles.append(line)

    if rI == len(ress)-1:
        axes[0].legend(handles, ress)


    # MASKING OF VALUES WITH SMALL AMOUNT OF CLOUDS
    mask = np.full(len(nClRaw),1)
    mask[nClRaw < minNClouds] = 0
    mask[nClSmo < minNClouds] = 0


    # RELATIVE DIFFERENCE 
    ax = axes[2]
    raw = nClRaw.astype(np.float)
    sm = nClSmo.astype(np.float)
    raw[raw == 0] = np.nan
    sm[sm == 0] = np.nan
    ratio = (raw - sm)/sm
    ratio[mask == 0] = np.nan
    line, = ax.semilogx(bins_centred_res[str(res)], ratio, '-', color=colrs[rI]) 
    sumRaw = np.nansum(raw)
    sumSmoothed = np.nansum(sm)
    sumRatio = sumRaw/sumSmoothed
    #ax.text(2E0, 0.8, 'raw/smoothed: '+str(np.round(sumRatio,2)))

    # LABELS
    ax = axes[1]
    x = 1.5
    yTop = 3E1
    ry = 0.42
    size = 13
    if i == 0:
        ax.text(x, yTop, 'RAW/SM:', size=size,
                bbox=dict(boxstyle='square',ec=(1,1,1,0.5),fc=(1,1,1,0.5)))
    ax.text(x, yTop*(ry**(rI+1)), '{:3.2f}'.format(sumRatio,2), size=size, color=colrs[rI],
            bbox=dict(boxstyle='square',ec=(1,1,1,0.5),fc=(1,1,1,0.5)))


for j in range(0,3):
    ax = axes[j]
    ax.set_xlabel('Cloud Size [$km^2$]',fontsize=labelsize)
    if j == 0:
        ax.set_ylabel('Number of Clouds',fontsize=labelsize)
    elif j == 2:
        ax.set_ylabel('Relative Difference',fontsize=labelsize)
    ax.set_xlim((1E0,1E5))
    if j < 2:
        ax.set_ylim((1E0,1E6))
    elif j == 2:
        ax.set_ylim((-0.6,0.6))
        #ax.set_ylim((-1,1))
        ax.axhline(y=0, color='k', lineWidth=0.5)
    ax.set_title(modeStrings[j],fontsize=titlesize)
    ax.grid()



#plt.suptitle('Absolute Cloud Size Distribution and Relative Difference')
#plt.subplots_adjust(left=0.07, right=0.95, top=0.92, bottom=0.08, wspace=0.27, hspace=0.33)
fig.subplots_adjust(wspace=0.30,left=0.07, right=0.95, bottom=0.15, top=0.85)

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

		  
