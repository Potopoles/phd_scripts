import os
import ncClasses.ncField as ncField
from ncClasses.subdomains import setSSI
from datetime import datetime, timedelta
import numpy as np
os.chdir('00_newScripts/')
import matplotlib.pyplot as plt

#from functions import unstaggerZ_1D, unstaggerZ_4D, saveObj 
from functions import saveObj 

ress = ['4.4', '2.2', '1.1']
#ress = ['4.4']
modes = ['', 'f']
#modes = ['f']
i_subdomain = 1
ssI, domainName = setSSI(i_subdomain, {'4.4':{}, '2.2':{}, '1.1':{}}) 
altInds = list(range(62,65))
#altInds = list(range(10,20))
dz = 1000
#dz = 100

dt0 = datetime(2006,7,11,0)
#dt0 = datetime(2006,7,12,0)
dt1 = datetime(2006,7,20,0)
#dt1 = datetime(2006,7,12,0)

hydrometeors = ['zQC', 'zQI', 'zQV', 'zQR', 'zQS', 'zQG']
TTendencies=['zATT_MIC','zATT_RAD','zATT_ADV','zATT_ZADV','zATT_TURB','zATT_TOT','zATT_HADV']
QVTendencies=['zAQVT_MIC','zAQVT_ADV','zAQVT_ZADV','zAQVT_TURB','zAQVT_TOT','zAQVT_HADV']
dynamics = ['zW', 'zU', 'zV', 'zT', 'zP', 'zRH']

fieldNames = ['zW']
fieldNames = TTendencies
#fieldNames = hydrometeors
#fieldNames = ['zATT_MIC']
fieldNames = ['zQI']
fieldNames = ['zW', 'zQC']
fieldNames =['zQV', 'zQS', 'zQG']

ssI['4.4']['altitude'] = altInds 
ssI['2.2']['altitude'] = altInds 
ssI['1.1']['altitude'] = altInds 

# Altitude arrays
altI = np.asarray(altInds)
alts = np.asarray(altInds)
alts[altI <= 60] = altI[altI <= 60]*100
alts[altI > 60] = (altI[altI > 60] - 60)*1000 + 6000
print(alts)

nameString = 'alts_'+str(alts[0])+'_'+str(alts[-1])+'_'+domainName
folder = '../06_bulk' +'/' + nameString
if not os.path.exists(folder):
    os.mkdir(folder)

dts = np.arange(dt0,dt1,timedelta(hours=1))
inpPath = '../01_rawData/topocut/'


print(nameString)
for fieldName in fieldNames:
    print('#########################')
    print(fieldName)
    print('#########################')
    out = {}
    out['time'] = dts
    out['alts'] = alts
    out['domainName'] = domainName

    for res in ress:
        dx = float(res)*1000
        A = np.power(dx,2)

        for mode in modes:
            print('###### '+res+mode+' ######')

            out[res+mode] = np.full(len(out['time']), np.nan)

            for tCount in range(0,len(dts)):
                ncFileName = 'lffd{0:%Y%m%d%H}z.nc'.format(dts[tCount].astype(datetime))
                if tCount % 24 == 0:
                    print('\t\t'+ncFileName)
                #print('\t\t'+ncFileName)

                srcNCPath = inpPath + res + mode + '/' + ncFileName

                RHOncf = ncField.ncField('RHO', srcNCPath, ssI[res])
                RHOncf.loadValues()
                rho = RHOncf.vals

                # CALCULATE VOL AV DENSITY WEIGHT
                Mtot = np.nansum(rho*dz*A)
                NCF = ncField.ncField(fieldName[1:], srcNCPath, ssI[res])
                NCF.loadValues()
                vals = NCF.vals
                out[res+mode][tCount] = np.nansum(vals*rho*dz*A)/Mtot
                out['units'] = NCF.units


    name = fieldName
    saveObj(out,folder,name)  

