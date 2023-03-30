import os
import ncClasses.ncField as ncField
from ncClasses.subdomains import setSSI
from datetime import datetime, timedelta
import numpy as np
os.chdir('00_newScripts/')

from functions import saveObj 


ress = ['4.4', '2.2', '1.1']
ress = ['4.4']
#modes = ['', 'f']
modes = ['f']
i_subdomain = 9
ssI, domainName = setSSI(i_subdomain, {'4.4':{}, '2.2':{}, '1.1':{}}) 
z0 = 20 
zs0 = z0-1
z1 = 55
zs1 = z1+1
altInds = list(range(zs0,zs1+1))
kk = np.asarray(list(range(1,len(altInds)-1)))
ssI['4.4']['altitude'] = altInds 
ssI['2.2']['altitude'] = altInds 
ssI['1.1']['altitude'] = altInds 

# Altitude arrays
altI = np.asarray(altInds)
alts = np.asarray(altInds)
alts[altI <= 60] = altI[altI <= 60]*100
alts[altI > 60] = (altI[altI > 60] - 60)*1000 + 6000
#altsu = np.nan

#dt0 = datetime(2006,7,12,0)
#dt1 = datetime(2006,7,12,1)
#dts = np.arange(dt0,dt1,timedelta(hours=1))
inpPath = '../01_rawData/topocut/'
res = '4.4'
mode = ''
srcNCPath = inpPath + res + mode + '/' + 'lffd2006071508z.nc'

RHOncf = ncField.ncField('RHO', srcNCPath, ssI[res])
RHOncf.loadValues()
rho = RHOncf.vals.squeeze()
Wncf = ncField.ncField('W', srcNCPath, ssI[res])
Wncf.loadValues()
w = Wncf.vals.squeeze()
QVncf = ncField.ncField('QV', srcNCPath, ssI[res])
QVncf.loadValues()
qv = QVncf.vals.squeeze()
AQVT_ZADVncf = ncField.ncField('AQVT_ZADV', srcNCPath, ssI[res])
AQVT_ZADVncf.loadValues()
aqvtz = AQVT_ZADVncf.vals.squeeze()

dA = np.power(4400,2)
dz = 100
dV = dz*dA

## LHS
qdwdz = np.full(len(qv),np.nan)
qdwdz[kk] = qv[kk]*(w[kk+1]-w[kk-1])/200
print(qdwdz[kk])
print(aqvtz[kk])
sumboth = aqvtz + qdwdz
#sumboth = aqvtz 
print(sumboth[kk])
volInt = np.sum(sumboth[kk]*dz*dA)

## RHS
wqv = w*qv
print(wqv[kk])
surfInt = dA*(wqv[kk[-1]] - wqv[kk[0]])


print(volInt)
print(surfInt)
print(volInt/surfInt)

quit()


aqvt = aqvt_zadv*rho*100*A
aqvt = aqvt.squeeze()
print(aqvt)
print(np.sum(aqvt))


quit()

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
        out['altsu'] = altsu
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
