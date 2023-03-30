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
ress = ['4.4']
modes = ['', 'f']
modes = ['f']
i_subdomain = 1
ssI, domainName = setSSI(i_subdomain, {'4.4':{}, '2.2':{}, '1.1':{}}) 
altInds = list(range(45,61))
altInds = list(range(0,26))
#altInds = list(range(0,41))
#altInds = list(range(45,61))
ssI['4.4']['altitude'] = altInds 
ssI['2.2']['altitude'] = altInds 
ssI['1.1']['altitude'] = altInds 

# Altitude arrays
altI = np.asarray(altInds)
alts = np.asarray(altInds)
alts[altI <= 60] = altI[altI <= 60]*100
alts[altI > 60] = (altI[altI > 60] - 60)*1000 + 6000
dz = np.diff(alts)
#altsu = unstaggerZ_1D(alts)

nameString = 'alts_'+str(alts[0])+'_'+str(alts[-1])+'_'+domainName
folder = '../06_bulk' +'/' + nameString
if not os.path.exists(folder):
    os.mkdir(folder)

inpPath = '../01_rawData/topocut/'
inpPathNoTopocut = '../01_rawData/'

days = list(range(11,20))
hours = list(range(0,24))

vars = ['AQVT_ADV', 'AQVT_ZADV', 'AQVT_HADV'] 

var = 'AQVT_ZADV'
#var = 'AQVT_TOT'
res = '4.4'
mode = 'f'
dx = float(res)*1000
A = np.power(dx,2)
diurnal = np.full(24,np.nan)
#diurnalSlab = np.full(24,np.nan)

for hr in hours:
    print(hr)
    #hr = 12 
    dts = list()
    for day in days:
        dts.append(datetime(2006,7,day,hr))

    MFsum = 0
    #MFsumSlab = 0
    for dt in dts:
        #print(dt)
        ncFileName = 'lffd{0:%Y%m%d%H}z.nc'.format(dt)
        srcNCPath = inpPath + res + mode + '/' + ncFileName

        # LOAD RHO
        RHOncf = ncField.ncField('RHO', srcNCPath, ssI[res])
        RHOncf.loadValues()
        rho = RHOncf.vals

        #srcNCPath = inpPathNoTopocut + res + mode + '/' + ncFileName
        NCF = ncField.ncField(var, srcNCPath, ssI[res])
        NCF.loadValues()
        vals = NCF.vals

        MF = np.nansum(vals*rho*100*A)
        #MF = np.nanmean(vals)
        MFsum = MFsum + MF
        #print(MF)

        ## slabs
        #ncf = ncField.ncField('W', srcNCPath, ssI[res])
        #ncf.loadValues()
        #W = ncf.vals

        #ncf = ncField.ncField('QV', srcNCPath, ssI[res])
        #ncf.loadValues()
        #QV = ncf.vals

        #slab2 = np.nansum(W[0,-1,:,:]*QV[0,-1,:,:]*rho[0,-1,:,:]*A)
        #slab1 = np.nansum(W[0,0,:,:]*QV[0,0,:,:]*rho[0,0,:,:]*A)
        #diff = slab1 - slab2
        #MFsumSlab = MFsumSlab + diff
        ##quit()

    MFmean = MFsum/len(dts)
    #MFmeanSlab = MFsumSlab/len(dts)
    diurnal[hr] = MFmean
    #diurnalSlab[hr] = MFmeanSlab
#diurnal = diurnal/1E9*3600
diurnal = diurnal
print(diurnal)
plt.plot(hours,diurnal)
#plt.plot(hours,diurnalSlab)
plt.grid()
plt.show()

quit()

print('#########################')
print(nameString)
print('#########################')
for res in ress:
    dx = float(res)*1000
    A = np.power(dx,2)
    for mode in modes:
        print('###### '+res+mode+' ######')

        # MODEL SPECIFIC OUTPUT
        out = {}
        for var in vars:
            out[var] = np.full(len(dts), np.nan)
        out['time'] = dts
        out['alts'] = alts
        #out['altsu'] = altsu
        out['domainName'] = domainName

        for tCount in range(0,len(dts)):
            ncFileName = 'lffd{0:%Y%m%d%H}z.nc'.format(dts[tCount].astype(datetime))
            if tCount % 24 == 0:
                print('\t\t'+ncFileName)
            #print('\t\t'+ncFileName)

            srcNCPath = inpPath + res + mode + '/' + ncFileName

            RHOncf = ncField.ncField('RHO', srcNCPath, ssI[res])
            RHOncf.loadValues()
            rho = RHOncf.vals

            nt,nzs,ny,nx = rho.shape

            ## TOTAL MASS
            #Mtot = 0
            #for i in range(0,nx):
            #    for j in range(0,ny):
            #        #Mtot = Mtot + np.nansum(rhou[0,:,j,i]*dz*A)
            #        Mtot = Mtot + np.nansum(rho[0,:,j,i]*dz*A)
            #out['Mtot'][tCount] = Mtot

            # CALCULATE TENDENCIES
            for var in vars:
                NCF = ncField.ncField(var, srcNCPath, ssI[res])
                NCF.loadValues()
                vals = NCF.vals
                print(vals.shape)
                out[var][tCount] = np.nansum(vals*rho*100*A)

        if i_variables == 'QV': 
            name = 'AQVT_'+res+mode
        elif i_variables == 'T':
            name = 'ATT_'+res+mode
        print(folder)
        print(name)
        saveObj(out,folder,name)  

#quit()
#lines = []
#for i in range(0,len(vars)):
#    line, = plt.plot(dts, out[vars[i]], label=vars[i])
#    lines.append(line)
#plt.legend(lines)
#plt.show()
