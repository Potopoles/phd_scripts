import sys
import os
import ncClasses.ncField as ncField
from ncClasses.subdomains import setSSI
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
import multiprocessing as mp
os.chdir('00_newScripts/')



ress = ['4.4', '2.2', '1.1']
#ress = ['2.2', '1.1']
#ress = ['4.4', '2.2']
ress = ['1.1']
modes = ['', 'f']
modes = ['f']
i_subdomain = 0

#ssI, domainName = setSSI(i_subdomain, {}) 
ssI, domainName = setSSI(i_subdomain, {'4.4':{}, '2.2':{}, '1.1':{}}) 

dt0 = datetime(2006,7,11,0)
#dt0 = datetime(2006,7,20,0)
dt1 = datetime(2006,7,20,1)
dts = np.arange(dt0,dt1,timedelta(hours=1))
inpPath = '../01_rawData/topocut/'

try:
    njobs = int(sys.argv[1])
    print('number of jobs is ' + str(njobs))
except:
    print('Number of Jobs not given. Assume 1')
    njobs = 1




def calc_rho(ncFileName):
    print(ncFileName)
    for res in ress:
        for mode in modes:
            #print('\t'+res+mode)

            srcNCPath = inpPath + res + mode + '/' + ncFileName

            l_already_done = False
            try:
                rhofield = ncField.ncField('RHO', srcNCPath, ssI)
                l_already_done = True
            except:
                pass


            if not l_already_done:
                QCncf = ncField.ncField('QC', srcNCPath, ssI)
                QCncf.loadValues()
                qc = QCncf.vals
                QRncf = ncField.ncField('QR', srcNCPath, ssI)
                QRncf.loadValues()
                qr = QRncf.vals
                QIncf = ncField.ncField('QI', srcNCPath, ssI)
                QIncf.loadValues()
                qi = QIncf.vals
                QSncf = ncField.ncField('QS', srcNCPath, ssI)
                QSncf.loadValues()
                qs = QSncf.vals
                QGncf = ncField.ncField('QG', srcNCPath, ssI)
                QGncf.loadValues()
                qg = QGncf.vals
                
                hydrotot = qc + qr + qi + qs + qg

                QVncf = ncField.ncField('QV', srcNCPath, ssI)
                QVncf.loadValues()
                qv = QVncf.vals
                Tncf = ncField.ncField('T', srcNCPath, ssI)
                Tncf.loadValues()
                T = Tncf.vals
                Pncf = ncField.ncField('P', srcNCPath, ssI)
                Pncf.loadValues()
                P = Pncf.vals

                tempFactor = qv*0.622 + 1 - hydrotot 
                Tdens = T*tempFactor 
                Rd = 287.1
                RHO = P/(Tdens*Rd)

                
                RHOncf = QVncf.copy() 
                RHOncf.fieldName = 'RHO'
                RHOncf.vals = RHO
                RHOncf.addVarToExistingNC(srcNCPath)


if njobs > 1:
    pool = mp.Pool(processes=njobs)
    input = [ ( 'lffd{0:%Y%m%d%H}z.nc'.format(dts[c].astype(datetime)), \
              ) for c in range(0,len(dts))]
    result = pool.starmap(calc_rho, input)

else:
    for i in range(0,len(dts)):
        ncFileName = 'lffd{0:%Y%m%d%H}z.nc'.format(dts[i].astype(datetime))
        calc_rho(ncFileName)

