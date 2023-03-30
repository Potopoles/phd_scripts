import os
os.chdir('00_scripts/')

import ncClasses.ncObject as ncObject
import numpy as np

inpPath = '../02_fields/result'
outPath = '../02_fields/topocut'

hydrometeors = ['zQC', 'zQI', 'zQV', 'zQR', 'zQS', 'zQG']
TTendencies = ['zATT_MIC', 'zATT_RAD', 'zATT_ADV', 'zATT_ZADV', 'zATT_TURB', 'zATT_TOT']
QVTendencies = ['zAQVT_MIC', 'zAQVT_ADV', 'zAQVT_ZADV', 'zAQVT_TURB', 'zAQVT_TOT']
dynamics = ['zW', 'zU', 'zV', 'zT', 'zP']
QVTendencies = ['zAQVT_TURB', 'zAQVT_TOT']

fieldNames = ['nU_10M', 'nV_10M']

i_resolution = 3 
modes = ['', 'f']
#modes = ['']
i_copy = 1
#####################################################################		
if i_resolution == 1:
    ress = ['4.4']
elif i_resolution == 2:
    ress = ['4.4', '2.2']
elif i_resolution == 3:
    ress = ['4.4','2.2','1.1']

subSpaceIndsIN = {}
from shutil import copyfile

for fieldName in fieldNames:
    print(fieldName) 
    inpFileName = fieldName + '.nc'

    for res in ress:
        for mode in modes:
            print(str(res) + mode)

            varName = fieldName[1:]

            inpFilePath = inpPath + '/' + res+mode + '/' + fieldName + '.nc'
            inpTopoFilePath = inpPath + '/' + res+mode + '/' + 'cHSURF' + '.nc' 
            outFilePath = outPath + '/' + res+mode + '/' + fieldName + '.nc'

            if i_copy:
                print('\tCOPY')
                copyfile(inpFilePath, outFilePath)

            print('\tPROCESS')
            nco = ncObject.ncObject(outFilePath, fieldName, res)        
            topo = ncObject.ncObject(inpTopoFilePath, 'cHSURF', res)        
            nco.selField(varName)
            topo.selField('HSURF')
            nco.cutOutTopo(topo)
