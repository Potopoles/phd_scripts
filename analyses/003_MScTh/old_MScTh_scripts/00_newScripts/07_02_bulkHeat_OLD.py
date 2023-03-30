import os
import ncClasses.ncField as ncField
from ncClasses.subdomains import setSSI
from datetime import datetime, timedelta
import numpy as np
os.chdir('00_newScripts/')

from functions import saveObj 

## THIS SCRIPT ONLY WORKS UP TO A HIGHT OF 6000 m !!!!!

def calcVolAvTend(val, rho, Mtot, nx, ny, A):
    VAL = 0
    for i in range(0,nx):
        for j in range(0,ny):
            VAL = VAL + np.nansum(valu[0,:,j,i]*rhou[0,:,j,i]*dz*A)
    VAL = VAL/Mtot*3600
    return(VAL)

ress = ['4.4', '2.2', '1.1']
ress = ['4.4']
modes = ['', 'f']
#modes = ['f']
i_subdomain = 1
i_variables = 'QV' # 'QV' or 'T'
ssI, domainName = setSSI(i_subdomain, {'4.4':{}, '2.2':{}, '1.1':{}}) 
altInds = list(range(50,61))
#altInds = list(range(25,63))
ssI['4.4']['altitude'] = altInds 
ssI['2.2']['altitude'] = altInds 
ssI['1.1']['altitude'] = altInds 

# Altitude arrays
altI = np.asarray(altInds)
alts = np.asarray(altInds)
alts[altI <= 60] = altI[altI <= 60]*100
alts[altI > 60] = (altI[altI > 60] - 60)*1000 + 6000

nameString = 'alts_'+str(alts[0])+'_'+str(alts[-1])+'_'+domainName
folder = '../06_bulk_noStag' +'/' + nameString
if not os.path.exists(folder):
    os.mkdir(folder)

dt0 = datetime(2006,7,11,0)
dt1 = datetime(2006,7,20,1)
dts = np.arange(dt0,dt1,timedelta(hours=1))
inpPath = '../01_rawData/topocut/'

if i_variables == 'QV': 
    vars = ['AQVT_TOT', 'AQVT_ADV', 'AQVT_HADV', 'AQVT_ZADV', 'AQVT_TURB', 'AQVT_MIC'] 
elif i_variables == 'T':
    vars = ['ATT_TOT', 'ATT_ADV', 'ATT_HADV', 'ATT_ZADV', 'ATT_RAD', 'ATT_TURB', 'ATT_MIC'] 

print('#########################')
print(nameString)
print(i_variables)
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
        out['Mtot'] = np.full(len(dts), np.nan)
        out['time'] = dts
        out['alts'] = alts
        out['domainName'] = domainName

        for tCount in range(0,len(dts)):
            ncFileName = 'lffd{0:%Y%m%d%H}z.nc'.format(dts[tCount].astype(datetime))
            if tCount % 24 == 0:
                print('\t\t'+ncFileName)

            srcNCPath = inpPath + res + mode + '/' + ncFileName

            RHOncf = ncField.ncField('RHO', srcNCPath, ssI[res])
            RHOncf.loadValues()
            rho = RHOncf.vals
            rhou = unstaggerZ_4D(rho)

            nt,nzs,ny,nx = rho.shape

            # TOTAL MASS
            Mtot = 0
            for i in range(0,nx):
                for j in range(0,ny):
                    Mtot = Mtot + np.nansum(rhou[0,:,j,i]*dz*A)
            out['Mtot'][tCount] = Mtot

            # CALCULATE TENDENCIES
            for var in vars:
                if var == 'AQVT_HADV':
                    NCFZ = ncField.ncField('AQVT_ZADV', srcNCPath, ssI[res])
                    NCFT = ncField.ncField('AQVT_ADV', srcNCPath, ssI[res])
                    NCFZ.loadValues()
                    NCFT.loadValues()
                    valsZ = unstaggerZ_4D(NCFZ.vals)
                    valsT = unstaggerZ_4D(NCFT.vals)
                    vals = valsT - valsZ
                elif var == 'ATT_HADV':
                    NCFZ = ncField.ncField('ATT_ZADV', srcNCPath, ssI[res])
                    NCFT = ncField.ncField('ATT_ADV', srcNCPath, ssI[res])
                    NCFZ.loadValues()
                    NCFT.loadValues()
                    valsZ = unstaggerZ_4D(NCFZ.vals)
                    valsT = unstaggerZ_4D(NCFT.vals)
                    vals = valsT - valsZ
                else:
                    NCF = ncField.ncField(var, srcNCPath, ssI[res])
                    NCF.loadValues()
                    vals = unstaggerZ_4D(NCF.vals)
                out[var][tCount] = calcVolAvTend(vals, rhou, Mtot, nx, ny, A)

        
        if i_variables == 'QV': 
            name = 'AQVT_'+res+mode
        elif i_variables == 'T':
            name = 'ATT_'+res+mode
        saveObj(out,folder,name)  

#quit()
#lines = []
#for i in range(0,len(vars)):
#    line, = plt.plot(dts, out[vars[i]], label=vars[i])
#    lines.append(line)
#plt.legend(lines)
#plt.show()
