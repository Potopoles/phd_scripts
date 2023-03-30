import os
import ncClasses.ncField as ncField
from ncClasses.subdomains import setSSI
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
os.chdir('00_newScripts/')


i_resolutions = 1 
ress = ['4.4', '2.2', '1.1']
modes = ['', 'f']
i_subdomain = 0

ssI, domainName = setSSI(i_subdomain, {}) 

dt0 = datetime(2006,7,20,0)
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

            QVncf = ncField.ncField('QV', srcNCPath, ssI)
            QVncf.loadValues()
            Pncf = ncField.ncField('P', srcNCPath, ssI)
            Pncf.loadValues()
            Tncf = ncField.ncField('T', srcNCPath, ssI)
            Tncf.loadValues()

            RHncf = QVncf.copy() 
            RHncf.fieldName = 'RH'

            qv = QVncf.vals
            p = Pncf.vals
            T = Tncf.vals
            TC = T - 273.15

            eps = 0.622
            e = p*qv/(eps+qv) # vapor pressure
            es = 611*np.exp(17.27*TC/(273.3+TC)) # saturation vapor pressure
            RH = e/es*100

            RHncf.vals = RH
            RHncf.addVarToExistingNC(srcNCPath)
