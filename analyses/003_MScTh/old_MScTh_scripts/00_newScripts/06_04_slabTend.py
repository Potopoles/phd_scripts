import os
import ncClasses.ncField as ncField
from ncClasses.subdomains import setSSI
from datetime import datetime, timedelta
import numpy as np
os.chdir('00_newScripts/')

from functions import saveObj 


ress = ['4.4', '2.2', '1.1']
ress = ['4.4']
modes = ['', 'f']
modes = ['f']
i_subdomain = 1
i_variables = 'QV' # 'QV' or 'T'
ssI, domainName = setSSI(i_subdomain, {'4.4':{}, '2.2':{}, '1.1':{}}) 
altInds = list(range(25,26))
#altInds = list(range(60,61))
#altInds = list(range(30,31))
#altInds = list(range(45,46))
altInds = list(range(40,41))
ssI['4.4']['altitude'] = altInds 
ssI['2.2']['altitude'] = altInds 
ssI['1.1']['altitude'] = altInds 

# Altitude arrays
altI = np.asarray(altInds)
alts = np.asarray(altInds)
alts[altI <= 60] = altI[altI <= 60]*100
alts[altI > 60] = (altI[altI > 60] - 60)*1000 + 6000
#altsu = np.nan

nameString = 'alt_'+str(alts[0])+'_'+domainName
folder = '../06_bulk/horSlab' +'/' + nameString
if not os.path.exists(folder):
    os.mkdir(folder)

dt0 = datetime(2006,7,11,0)
#dt0 = datetime(2006,7,12,0)
dt1 = datetime(2006,7,20,0)
#dt1 = datetime(2006,7,11,1)
dts = np.arange(dt0,dt1,timedelta(hours=1))
inpPath = '../01_rawData/topocut/'


print('#########################')
print(nameString)
print(i_variables)
print('#########################')
for res in ress:
    dx = float(res)*1000
    for mode in modes:
        print('###### '+res+mode+' ######')

        # MODEL SPECIFIC OUTPUT
        out = {}
        out['Fqv'] = np.full(len(dts), np.nan)
        out['time'] = dts
        out['alts'] = alts
        #out['altsu'] = altsu
        out['domainName'] = domainName

        for tCount in range(0,len(dts)):
            ncFileName = 'lffd{0:%Y%m%d%H}z.nc'.format(dts[tCount].astype(datetime))
            if tCount % 24 == 0:
                print('\t\t'+ncFileName)

            srcNCPath = inpPath + res + mode + '/' + ncFileName

            RHOncf = ncField.ncField('RHO', srcNCPath, ssI[res])
            RHOncf.loadValues()
            rho = RHOncf.vals
            Wncf = ncField.ncField('W', srcNCPath, ssI[res])
            Wncf.loadValues()
            w = Wncf.vals
            QVncf = ncField.ncField('QV', srcNCPath, ssI[res])
            QVncf.loadValues()
            qv = QVncf.vals

            nt,nz,ny,nx = rho.shape
            A = np.power(dx,2)
            
            Fqv = A*w*qv*rho
            sumFqv = np.nansum(Fqv)
            #print(sumFqv/1000)

            out['Fqv'][tCount] = sumFqv

        
        name = 'Fqv_'+res+mode
        saveObj(out,folder,name)  

#lines = []
#line, = plt.plot(dts, out[vars[i]], label=vars[i])
#lines.append(line)
#plt.legend(lines)
#plt.show()
