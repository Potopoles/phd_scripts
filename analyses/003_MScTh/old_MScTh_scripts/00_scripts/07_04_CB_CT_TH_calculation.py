import os
from netCDF4 import Dataset
from ncClasses.subdomains import setSSI
from datetime import datetime, timedelta
import numpy as np
from functions import saveObj
os.chdir('00_scripts/')


ress = ['4.4', '2.2', '1.1']
#ress = ['4.4', '2.2']
#ress = ['4.4']
modes = ['f', '']
modeNames = ['smoothed', 'raw', '(raw-smo)/smo']
i_subdomain = 2
ssI, domainName = setSSI(i_subdomain, {'4.4':{}, '2.2':{}, '1.1':{}}) 

dt0 = datetime(2006,7,11,0)
#dt0 = datetime(2006,7,12,0)
dt1 = datetime(2006,7,20,1)
#dt1 = datetime(2006,7,12,1)
dts = np.arange(dt0,dt1,timedelta(hours=1))
inpPath = '../01_rawData/cloud_cluster/'

vars = ['CT','CB']
out = {}
for res in ress:
    xmin = ssI[res]['rlon'][0]
    xmax = ssI[res]['rlon'][-1]
    ymin = ssI[res]['rlat'][0]
    ymax = ssI[res]['rlat'][-1]
    for mode in modes:
        print('###### '+res+mode+' ######')
        out[res+mode] = {}

        for var in vars:
            out[res+mode][var] = {}
            out[res+mode][var]['vals'] = [] 

        for tCount in range(0,len(dts)):
            ncFileName = 'lffd{0:%Y%m%d%H}z.nc'.format(dts[tCount].astype(datetime))
            if tCount % 24 ==  0:
                print('\t\t'+ncFileName)

            srcNCPath = inpPath + res + mode + '/' + ncFileName
            nc = Dataset(srcNCPath, 'r')
            
            xc = nc['XCENTER'][:]
            yc = nc['YCENTER'][:]
            mask = np.argwhere((
                (xc >= xmin) & (xc < xmax) & (
                yc >= ymin) & (yc < ymax)).squeeze()).squeeze()

            for var in vars:
                inp = nc[var][:].squeeze()
                if inp.ndim > 0 and mask.ndim > 0:
                    vals = inp[mask]
                    out[res+mode][var]['vals'].extend(vals.data)

for res in ress:
    for mode in modes:
        for var in vars:
            out[res+mode][var]['vals'] = np.asarray(out[res+mode][var]['vals'])
        out[res+mode]['TH'] = {}
        out[res+mode]['TH']['vals'] = out[res+mode]['CT']['vals'] - out[res+mode]['CB']['vals']

folder = '../08_lwp_and_clustering'
name = 'cloud_vertical_'+domainName
saveObj(out, folder, name)

