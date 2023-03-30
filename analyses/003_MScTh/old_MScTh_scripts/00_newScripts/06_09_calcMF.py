import os
import ncClasses.ncField as ncField
from ncClasses.subdomains import setSSI
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
os.chdir('00_newScripts/')


ress = ['4.4', '2.2', '1.1']
#ress = ['4.4']
modes = ['', 'f']
i_subdomain = 0

ssI, domainName = setSSI(i_subdomain, {'4.4':{}, '2.2':{}, '1.1':{}}) 

dt0 = datetime(2006,7,11,0)
dt1 = datetime(2006,7,20,1)
dts = np.arange(dt0,dt1,timedelta(hours=1))
inpPath = '../01_rawData/topocut/'

for i in range(0,len(dts)):
    ncFileName = 'lffd{0:%Y%m%d%H}z.nc'.format(dts[i].astype(datetime))
    print(ncFileName)

    for res in ress:
        for mode in modes:
            #print('\t'+res+mode)
            srcNCPath = inpPath + res + mode + '/' + ncFileName

            RHOncf = ncField.ncField('RHO', srcNCPath, ssI)
            RHOncf.loadValues()
            rho = RHOncf.vals
            Uncf = ncField.ncField('U', srcNCPath, ssI)
            Uncf.loadValues()
            u = Uncf.vals
            Vncf = ncField.ncField('V', srcNCPath, ssI)
            Vncf.loadValues()
            v = Vncf.vals

            uv = np.sqrt(np.power(u,2) + np.power(v,2))
            MFL = uv*rho
            
            MFLncf = RHOncf.copy() 
            MFLncf.fieldName = 'MFL'
            MFLncf.vals = MFL
            MFLncf.addVarToExistingNC(srcNCPath)
