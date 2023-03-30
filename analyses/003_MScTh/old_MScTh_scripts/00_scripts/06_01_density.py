import os
os.chdir('00_scripts/')

import ncClasses.ncObject as ncObject
import numpy as np
import ncClasses.analysis as analysis

inpPath = '../02_fields/topocut'
outPath = '../02_fields/topocut'

hydrometeors = ['zQC', 'zQI', 'zQV', 'zQR', 'zQS', 'zQG']
TTendencies = ['zATT_MIC', 'zATT_RAD', 'zATT_ADV', 'zATT_ZADV', 'zATT_TURB', 'zATT_TOT']
QVTendencies = ['zAQVT_MIC', 'zAQVT_ADV', 'zAQVT_ZADV', 'zAQVT_TURB', 'zAQVT_TOT']
dynamics = ['zW', 'zU', 'zV', 'zT', 'zP']
QVTendencies = ['zAQVT_TURB', 'zAQVT_TOT']

fieldNames = hydrometeors + ['zT', 'zP']
#fieldNames = ['zQV', 'zQC', 'zQR', 'zT', 'zP']

i_resolution = 5 
modes = ['', 'f']
modes = ['f']
i_copy = 0
i_info = 2
####################################################################k		
if i_resolution == 1:
    ress = ['4.4']
elif i_resolution == 2:
    ress = ['4.4', '2.2']
elif i_resolution == 3:
    ress = ['4.4','2.2','1.1']
elif i_resolution == 4:
    ress = ['2.2']
elif i_resolution == 5:
    ress = ['1.1']

subSpaceIndsIN = {}
ag_commnds = {}
altInds = list(range(0,65)) 
altInds = [62,63,64] 

from netCDF4 import Dataset
from shutil import copyfile
if i_copy:
    print('COPY')
    for res in ress:
        if i_info >= 1:
            print(res)
        for mode in modes:
            print(mode)
            inpFilePath = inpPath + '/' + res+mode + '/zT.nc'
            outFilePath = outPath + '/' + res+mode + '/zRHO.nc'
            copyfile(inpFilePath, outFilePath)
            ncFile = Dataset(outFilePath,'a')
            ncFile.renameVariable('T','RHO')
            ncFile['RHO'].units = 'kg/m^3'
            ncFile.close()
            


print('################### ITERATE THROUGH VERTICAL LEVELS ###################')
for altInd in altInds:
    print(altInd)

    subSpaceIndsIN['altitude'] = [altInd]
    an = analysis.analysis(inpPath, fieldNames)
    an.subSpaceIndsIN = subSpaceIndsIN
    an.ag_commnds = ag_commnds
    an.i_info = i_info
    an.i_resolutions = i_resolution
    an.run()

    # SUM UP HYDROMETEORS
    an.vars['hydrotot'] = an.vars['zQC'].addVar(an.vars['zQR'], label='sum hydrometeors')
    del an.vars['zQC']
    del an.vars['zQR']
    an.vars['hydrotot'] = an.vars['hydrotot'].addVar(an.vars['zQI'], label='sum hydrometeors')
    del an.vars['zQI']
    an.vars['hydrotot'] = an.vars['hydrotot'].addVar(an.vars['zQS'], label='sum hydrometeors')
    del an.vars['zQS']
    an.vars['hydrotot'] = an.vars['hydrotot'].addVar(an.vars['zQG'], label='sum hydrometeors')
    del an.vars['zQG']

    # CALCULATE FACTOR
    an.vars['zQV'].multConst(0.6078)
    an.vars['zQV'].addConst(1)
    an.vars['factor'] = an.vars['zQV'].subtractVar(an.vars['hydrotot'], label='factor')

    # CALCULATE DENSITY TEMPERATURE
    an.vars['TD'] = an.vars['zT'].multiplyVar(an.vars['factor'], label='density temperature')

    # CALCULATE DENSITY
    Rd = 287.1
    an.vars['TD'].multConst(Rd)
    an.vars['zRHO'] = an.vars['zP'].divideVar(an.vars['TD'], label='density')
    


    ## SAVE
    #[ncos,varName] = an.getNCOsOfVar(fieldName='zRHO')
    #print(ncos)
    #for nco in ncos:
    #    path = outPath + '/' + nco.name + '/result.nc'
    #    print(path)
    #    nco.saveToNC(path)


    print('SAVE')
    for res in ress:
        for mode in modes:
            filePath = outPath + '/' + res+mode + '/zRHO.nc'
            if mode == '':
                modestr = 'U'
            elif mode == 'f':
                modestr = 'F'
            fld = an.vars['zRHO'].modelRes[res].ncos[modestr].curFld
            #print('field shape')
            #print(fld.vals.shape)
            #print(fld.dimKeys)

            # OPEN COPIED NC FILE
            ncFile = Dataset(filePath,'a')

            #s0 = slice(indices[0].start,indices[0].stop)
            #s1 = slice(indices[1].start,indices[1].stop)
            #s2 = slice(indices[2].start,indices[2].stop)
            #s3 = slice(indices[3].start,indices[3].stop)
                
            #ncFile['RHO'][s0,s1,s2,s3] = selfSlice
            ncFile['RHO'][:,altInd,:,:] = fld.vals

            ncFile.close()
