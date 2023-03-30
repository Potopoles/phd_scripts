import os, sys
import ncClasses.ncField as ncField
from ncClasses.subdomains import setSSI
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
import multiprocessing as mp
os.chdir('00_newScripts/')


ress = ['4.4', '2.2', '1.1']
#ress = ['2.2', '1.1']
#ress = ['4.4']
modes = ['', 'f']
#modes = ['']
i_subdomain = 0
var = 'FQV'
#var = 'FQVx'
var = 'FQVy'

ssI, domainName = setSSI(i_subdomain, {'4.4':{}, '2.2':{}, '1.1':{}}) 

#dt0 = datetime(2006,7,20,0)
dt0 = datetime(2006,7,11,0)
dt1 = datetime(2006,7,20,1)
dts = np.arange(dt0,dt1,timedelta(hours=1))
inpPath = '../01_rawData/topocut/'

if len(sys.argv) > 1:
    njobs = int(sys.argv[1])
    print('number of jobs is ' + str(njobs))
else:
    print('Number of Jobs not given. Assume 1')
    njobs = 1


def calc_fqv(ncFileName):
    print(ncFileName)
    for res in ress:
        for mode in modes:
            print('\t'+res+mode)
            srcNCPath = inpPath + res + mode + '/' + ncFileName

            l_already_done = False
            try:
                fqvfield = ncField.ncField(var, srcNCPath, ssI)
                l_already_done = True
            except:
                pass

            if not l_already_done:
                ncf = ncField.ncField('QV', srcNCPath, ssI)
                ncf.loadValues()
                qv = ncf.vals
                FQVncf = ncf.copy() 
                FQVncf.fieldName = var

                ncf = ncField.ncField('RHO', srcNCPath, ssI)
                ncf.loadValues()
                rho = ncf.vals
                
                if (var == 'FQV') or (var == 'FQVx'):
                    ncf = ncField.ncField('U', srcNCPath, ssI)
                    ncf.loadValues()
                    u = ncf.vals

                if (var == 'FQV') or (var == 'FQVy'):
                    ncf = ncField.ncField('V', srcNCPath, ssI)
                    ncf.loadValues()
                    v = ncf.vals

                if (var == 'FQV'):
                    uv = np.sqrt(np.power(u,2) + np.power(v,2))
                    fqv = rho*uv*qv
                elif (var == 'FQVx'):
                    fqv = rho*u*qv
                elif (var == 'FQVy'):
                    fqv = rho*v*qv

                FQVncf.vals = fqv
                FQVncf.addVarToExistingNC(srcNCPath)



if njobs > 1:
    pool = mp.Pool(processes=njobs)
    input = [ ( 'lffd{0:%Y%m%d%H}z.nc'.format(dts[c].astype(datetime)), \
              ) for c in range(0,len(dts))]
    result = pool.starmap(calc_fqv, input)

else:
    for i in range(0,len(dts)):
        ncFileName = 'lffd{0:%Y%m%d%H}z.nc'.format(dts[i].astype(datetime))
        calc_fqv(ncFileName)

