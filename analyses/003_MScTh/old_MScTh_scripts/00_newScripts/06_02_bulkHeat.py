import os, sys
import ncClasses.ncField as ncField
from ncClasses.subdomains import setSSI
from datetime import datetime, timedelta
import numpy as np
os.chdir('00_newScripts/')
import matplotlib.pyplot as plt
import multiprocessing as mp

#from functions import unstaggerZ_1D, unstaggerZ_4D, saveObj 
from functions import saveObj 

ress = ['4.4', '2.2', '1.1']
#ress = ['4.4']
modes = ['', 'f']
#modes = ['']
i_subdomain = 2
i_variables = 'QV' # 'QV' or 'T'
#i_variables = 'T' # 'QV' or 'T'
ssI, domainName = setSSI(i_subdomain, {'4.4':{}, '2.2':{}, '1.1':{}}) 

altInds = list(range(0,21))
#altInds = list(range(0,26))



#altInds = list(range(0,65))
#altInds = list(range(20,65))
#altInds = list(range(25,65))
#altInds = list(range(20,41))

dt0 = datetime(2006,7,11,0)
#dt0 = datetime(2006,7,12,0)
dt1 = datetime(2006,7,20,0)
#dt1 = datetime(2006,7,13,0)


print(altInds)
ssI['4.4']['altitude'] = altInds 
ssI['2.2']['altitude'] = altInds 
ssI['1.1']['altitude'] = altInds 

# Altitude arrays
altI = np.asarray(altInds)
alts = np.asarray(altInds)
alts[altI <= 60] = altI[altI <= 60]*100
alts[altI > 60] = (altI[altI > 60] - 60)*1000 + 6000
#dz = np.diff(alts)
dz = []
for i in range(0,len(alts)):
    im1 = max(i-1,0)
    ip1 = min(i+1,len(alts)-1)
    dz.append( (alts[ip1] - alts[i])/2 + (alts[i] - alts[im1])/2 )
dz = np.asarray(dz)
    
#altsu = unstaggerZ_1D(alts)

nameString = 'alts_'+str(alts[0])+'_'+str(alts[-1])+'_'+domainName
folder = '../06_bulk' +'/' + nameString
if not os.path.exists(folder):
    os.mkdir(folder)

dts = np.arange(dt0,dt1,timedelta(hours=1))
inpPath = '../01_rawData/topocut/'

try:
    njobs = int(sys.argv[1])
    print('number of jobs is ' + str(njobs))
except:
    print('Number of Jobs not given. Assume 1')
    njobs = 1



if i_variables == 'QV': 
    vars = ['AQVT_TOT', 'AQVT_ADV', 'AQVT_HADV', 'AQVT_ZADV', 'AQVT_TURB', 'AQVT_MIC'] 
    #vars = ['AQVT_TOT', 'AQVT_ADV', 'AQVT_TURB', 'AQVT_MIC'] 
    #vars = ['AQVT_ADV', 'AQVT_HADV', 'AQVT_ZADV', 'AQVT_TOT']
    #vars = ['AQVT_TURB']
elif i_variables == 'T':
    vars = ['ATT_TOT', 'ATT_ADV', 'ATT_HADV', 'ATT_ZADV', 'ATT_RAD', 'ATT_TURB', 'ATT_MIC'] 


def calc_bulk(tCount, VOL, Atot):
    ncFileName = 'lffd{0:%Y%m%d%H}z.nc'.format(dts[tCount].astype(datetime))
    if tCount % 24 == 0:
        print('\t\t'+ncFileName)
    #print('\t\t'+ncFileName)

    srcNCPath = inpPath + res + mode + '/' + ncFileName

    RHOncf = ncField.ncField('RHO', srcNCPath, ssI[res])
    RHOncf.loadValues()
    rho = RHOncf.vals

    result = {}

    # CALCULATE TENDENCIES
    #Mtot = np.nansum(rho*100*A)
    MASS = rho * VOL
    for var in vars:
        NCF = ncField.ncField(var, srcNCPath, ssI[res])
        NCF.loadValues()
        vals = NCF.vals
        if i_variables == 'QV':
            # unit is domain average mm/h precipitation
            result[var] = np.sum(MASS*vals*3600)/Atot
            #print(out[var][tCount])
        else:
            raise NotImplementedError()
        #out[var][tCount] = np.nansum(vals*rho*100*A)/Mtot

    return(result)


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
        out['domainName'] = domainName
        out['Mtot'] = np.full(len(dts), np.nan)
        out['time'] = dts
        out['alts'] = alts
        out['dz'] = dz
        # CALCULATE CELL VOLUME
        VOL = np.zeros(( 1, len(dz), len(ssI[res]['rlat']), len(ssI[res]['rlon']) ))
        Atot = len(ssI[res]['rlat'])*len(ssI[res]['rlon'])*A
        for k in range(0,len(dz)):
            VOL[0,k,:,:] = A * dz[k]
        out['VOL_k'] = A * dz


        if njobs == 1:
            for tCount in range(0,len(dts)):
                result = calc_bulk(tCount, VOL, Atot)
                for var in vars:
                    out[var][tCount] = result[var]
        else:
            pool = mp.Pool(processes=njobs)
            input = [ ( tCount, VOL, Atot ) for tCount in range(0,len(dts))]
            pool_out = pool.starmap(calc_bulk, input)
            pool.close()
            pool.join()

            for tCount in range(0,len(dts)):
                for var in vars:
                    out[var][tCount] = pool_out[tCount][var]



        if i_variables == 'QV': 
            name = 'AQVT_'+res+mode
        elif i_variables == 'T':
            name = 'ATT_'+res+mode
        print(folder)
        print(name)
        saveObj(out,folder,name)  

