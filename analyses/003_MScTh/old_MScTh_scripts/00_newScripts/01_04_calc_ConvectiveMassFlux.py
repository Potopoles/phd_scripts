import os
import ncClasses.ncField as ncField
from ncClasses.subdomains import setSSI
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
from functions import saveObj, loadObj
os.chdir('00_newScripts/')


ress = ['4.4', '2.2', '1.1']
#ress = ['4.4']
modes = ['', 'f']
i_subdomain = 2
alt_inds = range(0,65)
velocity_threshold = 0.5
velocity_threshold = 1

ssI, domainName = setSSI(i_subdomain, {'4.4':{}, '2.2':{}, '1.1':{}}) 


dt0 = datetime(2006,7,11,0)
#dt0 = datetime(2006,7,12,12)
dt1 = datetime(2006,7,20,1)
#dt1 = datetime(2006,7,14,2)
dts = np.arange(dt0,dt1,timedelta(hours=1))
inpPath = '../01_rawData/topocut/'

# PREPARE OUTPUT
out = {}
out['times'] = []
for res in ress:
    for mode in modes:
        out[res+mode] = np.zeros((len(alt_inds),len(dts)))


for i in range(0,len(dts)):
    ncFileName = 'lffd{0:%Y%m%d%H}z.nc'.format(dts[i].astype(datetime))
    print(ncFileName)

    out['times'].append(dts[i].astype(datetime))

    for aI,alt_ind in enumerate(alt_inds):
        for res in ress:
            for mode in modes:
                #print('\t'+res+mode)
                srcNCPath = inpPath + res + mode + '/' + ncFileName

                res_ssI = {}
                res_ssI['altitude'] = [alt_ind]
                for key in ['rlon','rlat']:
                    res_ssI[key] = ssI[res][key]
                

                NCF = ncField.ncField('QC', srcNCPath, res_ssI)
                NCF.loadValues()
                qc = NCF.vals

                NCF = ncField.ncField('QI', srcNCPath, res_ssI)
                NCF.loadValues()
                qi = NCF.vals

                NCF = ncField.ncField('W', srcNCPath, res_ssI)
                NCF.loadValues()
                w = NCF.vals

                NCF = ncField.ncField('RHO', srcNCPath, res_ssI)
                NCF.loadValues()
                rho = NCF.vals


                nlat = qc.shape[2]
                nlon = qc.shape[3]

                mask = ((qc > 1E-6) | (qi > 1E-10)) & (w > velocity_threshold)
                cmflx = w[mask]*rho[mask]
                cmflx_mean = np.sum(cmflx)/(nlat*nlon)


                out[res+mode][aI,i] = cmflx_mean

folder = '../06_bulk'
name = 'convective_mass_flux_'+domainName
saveObj(out,folder,name)  

                
