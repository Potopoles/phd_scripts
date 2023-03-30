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
ress = ['4.4']
modes = ['', 'f']
#modes = ['f']
i_subdomain = 0

ssI, domainName = setSSI(i_subdomain, {'4.4':{}, '2.2':{}, '1.1':{}}) 

dt0 = datetime(2006,7,11,0)
#dt0 = datetime(2006,7,13,12)
#dt1 = datetime(2006,7,20,1)
#dt0 = datetime(2006,7,20,0)
dt1 = datetime(2006,7,20,1)
#dt1 = datetime(2006,7,13,13)
dts = np.arange(dt0,dt1,timedelta(hours=1))
inpPath = '../01_rawData/topocut/'


try:
    njobs = int(sys.argv[1])
    print('number of jobs is ' + str(njobs))
except:
    print('Number of Jobs not given. Assume 1')
    njobs = 1






def calc_horflux(ncFileName):
    print(ncFileName)

    for res in ress:
        for mode in modes:
            #print('\t'+res+mode)
            srcNCPath = inpPath + res + mode + '/' + ncFileName

            ################################## AQVT
            l_already_done = False
            try:
                field = ncField.ncField('AQVT_HADV', srcNCPath, ssI)
                l_already_done = True
            except:
                pass

            if not l_already_done:
                QV_ADVncf = ncField.ncField('AQVT_ADV', srcNCPath, ssI[res])
                QV_ADVncf.loadValues()
                qv_adv = QV_ADVncf.vals
                QV_ZADVncf = ncField.ncField('AQVT_ZADV', srcNCPath, ssI[res])
                QV_ZADVncf.loadValues()
                qv_zadv = QV_ZADVncf.vals

                qv_hadv = qv_adv - qv_zadv

                QV_HADVncf = QV_ADVncf.copy() 
                QV_HADVncf.fieldName = 'AQVT_HADV'
                QV_HADVncf.vals = qv_hadv
                QV_HADVncf.addVarToExistingNC(srcNCPath)


            ################################### ATT
            #l_already_done = False
            #try:
            #    field = ncField.ncField('ATT_HADV', srcNCPath, ssI)
            #    l_already_done = True
            #except:
            #    pass

            #if not l_already_done:

            #    T_ADVncf = ncField.ncField('ATT_ADV', srcNCPath, ssI[res])
            #    T_ADVncf.loadValues()
            #    t_adv = T_ADVncf.vals
            #    T_ZADVncf = ncField.ncField('ATT_ZADV', srcNCPath, ssI[res])
            #    T_ZADVncf.loadValues()
            #    t_zadv = T_ZADVncf.vals

            #    t_hadv = t_adv - t_zadv

            #    T_HADVncf = T_ADVncf.copy() 
            #    T_HADVncf.fieldName = 'ATT_HADV'
            #    T_HADVncf.vals = t_hadv
            #    T_HADVncf.addVarToExistingNC(srcNCPath)


if njobs > 1:
    pool = mp.Pool(processes=njobs)
    input = [ ( 'lffd{0:%Y%m%d%H}z.nc'.format(dts[c].astype(datetime)), \
              ) for c in range(0,len(dts))]
    result = pool.starmap(calc_horflux, input)

else:
    for i in range(0,len(dts)):
        ncFileName = 'lffd{0:%Y%m%d%H}z.nc'.format(dts[i].astype(datetime))
        #ncFileName = 'lffd2006071512z.nc'
        calc_horflux(ncFileName)


