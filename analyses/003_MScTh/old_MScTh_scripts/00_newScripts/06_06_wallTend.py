import os
import copy
import ncClasses.ncField as ncField
from ncClasses.subdomains import setSSI
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
os.chdir('00_newScripts/')

from functions import saveObj 

i_save = 0

ress = ['4.4', '2.2', '1.1']
#ress = ['2.2', '1.1']
#ress = ['1.1']
#ress = ['4.4']
modes = ['', 'f']
#modes = ['f']
i_subdomain = 1
i_variables = 'Fqv'
ssI, domainName = setSSI(i_subdomain, {'4.4':{}, '2.2':{}, '1.1':{}}) 
#altInds = list(range(25,61))
#altInds = list(range(0,26))
#altInds = list(range(45,61))
#altInds = list(range(50,52))
#altInds = list(range(0,11))
altInds = list(range(0,21))
ssI['4.4']['altitude'] = altInds 
ssI['2.2']['altitude'] = altInds 
ssI['1.1']['altitude'] = altInds 
#ssIRaw = copy.deepcopy(ssI)

i_walls = ['left', 'right', 'top', 'bottom']
i_walls = ['bottom']
i_walls = ['top']


ssIRaw = ssI
for i_wall in i_walls:
    print('########################## ' + i_wall + ' ###########################')
    #i_wall = 'left'
    ssI = copy.deepcopy(ssIRaw)

    if i_wall == 'left':
        for res in ress:
            ssI[res]['rlon'] = [ssIRaw[res]['rlon'][0]]
            ssI[res]['srlon'] = [ssIRaw[res]['srlon'][0]]
        normVec = 1
    elif i_wall == 'right':
        for res in ress:
            ssI[res]['rlon'] = [ssIRaw[res]['rlon'][-1]]
            ssI[res]['srlon'] = [ssIRaw[res]['srlon'][-1]]
        normVec = -1
    elif i_wall == 'bottom':
        for res in ress:
            ssI[res]['rlat'] = [ssIRaw[res]['rlat'][0]]
            #print(ssI[res]['rlat'])
            #quit()
            ssI[res]['srlat'] = [ssIRaw[res]['srlat'][0]]
        normVec = 1
    elif i_wall == 'top':
        for res in ress:
            ssI[res]['rlat'] = [ssIRaw[res]['rlat'][-1]]
            #print(ssI[res]['rlat'])
            #quit()
            ssI[res]['srlat'] = [ssIRaw[res]['srlat'][-1]]
        normVec = -1

    print(i_wall)
    print(ssI[res]['rlat'])
    #quit()

    # Altitude arrays
    altI = np.asarray(altInds)
    alts = np.asarray(altInds)
    alts[altI <= 60] = altI[altI <= 60]*100
    alts[altI > 60] = (altI[altI > 60] - 60)*1000 + 6000
    dz = np.diff(alts)
    #altsu = unstaggerZ_1D(alts)

    nameString = 'alts_'+str(alts[0])+'_'+str(alts[-1])+'_'+domainName
    folder = '../06_bulk/vertSlab' +'/' + nameString
    if not os.path.exists(folder):
        os.mkdir(folder)

    dt0 = datetime(2006,7,11,0)
    #dt0 = datetime(2006,7,12,0)
    dt1 = datetime(2006,7,20,0)
    #dt1 = datetime(2006,7,13,0)
    dts = np.arange(dt0,dt1,timedelta(hours=1))
    inpPath = '../01_rawData/topocut/'


    #print('#########################')
    #print(i_variables)
    #print('#########################')
    for res in ress:
        dx = float(res)*1000
        for mode in modes:
            print('###### '+res+mode+' ######')

            # MODEL SPECIFIC OUTPUT
            out = {}
            out['Fqv'] = np.full(len(dts), np.nan)
            out['Mtot'] = np.full(len(dts), np.nan)
            out['time'] = dts
            out['alts'] = alts
            out['ssI'] = ssIRaw[res]

            nlon = len(ssIRaw[res]['rlon'])
            nlat = len(ssIRaw[res]['rlat'])
            Area = nlon * nlat * float(res)**2
            print('Area is: ' + str(round(Area,0)) + ' km**2')
            out['Area'] = Area
            #quit()
            #quit()
            #out['altsu'] = altsu
            out['domainName'] = domainName

            for tCount in range(0,len(dts)):
                ncFileName = 'lffd{0:%Y%m%d%H}z.nc'.format(dts[tCount].astype(datetime))
                if tCount % 24 == 0:
                    print('\t\t'+ncFileName)

                srcNCPath = inpPath + res + mode + '/' + ncFileName

                #print(srcNCPath)
                #quit()

                #print(res)
                #HSURF = ncField.ncField('HSURF', '../01_rawData/HSURF/'+res+'.nc', ssI[res])
                #HSURF.loadValues()
                #plt.contourf(HSURF.vals.squeeze())
                #plt.show()
                #quit()

                RHOncf = ncField.ncField('RHO', srcNCPath, ssI[res])
                RHOncf.loadValues()
                rho = RHOncf.vals
                #rhou = unstaggerZ_4D(rho)
                if i_wall in ['left', 'right']:
                    VELncf = ncField.ncField('U', srcNCPath, ssI[res])
                elif i_wall in ['bottom', 'top']:
                    VELncf = ncField.ncField('V', srcNCPath, ssI[res])
                VELncf.loadValues()
                vel = VELncf.vals
                #velu = unstaggerZ_4D(vel)
                QVncf = ncField.ncField('QV', srcNCPath, ssI[res])
                QVncf.loadValues()
                qv = QVncf.vals
                #qvu = unstaggerZ_4D(qv)

                #nt,nzs,ny,nx = rho.shape

                vel = vel*normVec

                Fqv = dx*100*vel*qv*rho
                sumFqv = np.nansum(Fqv)
                #print(sumFqv)
                out['Fqv'][tCount] = sumFqv

            
            name = 'Fqv_'+i_wall+'_'+res+mode
            print(name)
            print(folder)
            if i_save:
                saveObj(out,folder,name)  

