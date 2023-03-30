#################################
# Calculate domain Average Precipitation
# author: Christoph Heim
# date: 21 10 2017
#################################
import os
os.chdir('00_scripts/')

import matplotlib.pyplot as plt


import ncClasses.ncObject as ncObject
from datetime import datetime
from functions import *
import os, sys
####################### NAMELIST INPUTS FILES #######################
# directory of input model folders
inpPath = '../02_fields/topocut'
outPath = '../02_fields/diurnal'

others = ['nTOT_PREC', 'nHPBL']
hydrometeors = ['zQC', 'zQI', 'zQV', 'zQR', 'zQS', 'zQG']
TTendencies = ['zATT_MIC', 'zATT_RAD', 'zATT_ADV', 'zATT_ZADV', 'zATT_TURB', 'zATT_TOT', 'zATT_HADV']
QVTendencies = ['zAQVT_MIC', 'zAQVT_ADV', 'zAQVT_ZADV', 'zAQVT_TURB', 'zAQVT_TOT','zAQVT_HADV']
LWP = ['zALL', 'zHYD', 'zIWP', 'zLWP', 'zWVP']
clouds = ['zCB', 'zCT', 'zMF', 'zWM']
dynamics = ['zW', 'zU', 'zV', 'zT', 'zP']

#fieldNames = ['nALHFL_S', 'nASHFL_S']
#fieldNames = ['nALHFL_S']
#fieldNames = ['zAQVT_TURB']
#fieldNames = TTendencies
#fieldNames = QVTendencies
#fieldNames = ['zCW', 'zPW']
#fieldNames = ['zWV_mass']
#fieldNames = ['nCAPE_ML', 'nCIN_ML']
#fieldNames = ['nTOT_PREC']
#fieldNames = ['zQC']

if len(sys.argv) > 1:
    fieldNames = [sys.argv[1]]
    print('fieldName is ' + str(fieldNames))
else:
    print('No fieldName argument given')
    print('exit')
    quit()


i_resolution = 3
#####################################################################		
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
modes = ['', 'f']
#modes = ['r']


for fieldName in fieldNames:
    print(fieldName)
    for res in ress:
        for mode in modes:
            print(str(res) + mode)

            varName = fieldName[1:]

            inpFilePath = inpPath + '/' + res+mode + '/' + fieldName + '.nc'
            outFilePath = outPath + '/' + res+mode + '/' + fieldName + '.nc'

            nco = ncObject.ncObject(inpFilePath, res, fieldName[1:])        
            #quit()
            #nco.selField(varName)
            if fieldName in 'nTOT_PREC':
                nco.loadAsDiurnal('SUM')
            else:
                nco.loadAsDiurnal('MEAN')
            # SAVE FILE
            if os.path.exists(outFilePath):
                os.remove(outFilePath)
            nco.saveToNewNC(outFilePath)

