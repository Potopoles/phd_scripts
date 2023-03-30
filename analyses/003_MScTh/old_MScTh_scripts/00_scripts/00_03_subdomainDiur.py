#################################
# Calculate domain Average Precipitation
# author: Christoph Heim
# date: 21 10 2017
#################################
import os
os.chdir('00_scripts/')

i_resolutions = 3 # 1 = 4.4, 2 = 4.4 + 2.2, 3 = ...
i_info = 0 # output some information [from 0 (off) to 5 (all you can read)]

import ncClasses.analysis as analysis
from datetime import datetime
from functions import *
####################### NAMELIST INPUTS FILES #######################
# directory of input model folders
inpPath = '../02_fields/diurnal'
outPath = '../02_fields/subDomDiur'

others = ['cHSURF', 'nTOT_PREC', 'nHPBL']
hydrometeors = ['zQC', 'zQI', 'zQV', 'zQR', 'zQS', 'zQG']
TTendencies = ['zATT_MIC', 'zATT_RAD', 'zATT_ADV', 'zATT_ZADV', 'zATT_TURB', 'zATT_TOT']
QVTendencies = ['zAQVT_MIC', 'zAQVT_ADV', 'zAQVT_ZADV', 'zAQVT_TURB', 'zAQVT_TOT']
dynamics = ['zW', 'zU', 'zV', 'zT', 'zP']

fieldNames = QVTendencies
fieldNames = ['nATHB_T']
#####################################################################		

####################### NAMELIST DIMENSIONS #######################
subDomain = 1 # 0: full domain, 1: alpine region, 2: zoom in
# SUBSPACE
subSpaceInds = {}
if subDomain == 1: # alpine region
    subSpaceInds['rlon'] = [50,237]
    subSpaceInds['rlat'] = [41,155]
elif subDomain == 2: # zoom in subdomain
    subSpaceInds['rlon'] = [70,100]
    subSpaceInds['rlat'] = [70,100]

if i_resolutions == 1:
    ress = ['4.4']
elif i_resolutions == 2:
    ress = ['4.4', '2.2']
elif i_resolutions == 3:
    ress = ['4.4', '2.2', '1.1']
elif i_resolutions == 4:
    ress = ['2.2']
elif i_resolutions == 5:
    ress = ['1.1']
modes = ['', 'f']
    
for fieldName in fieldNames:
    print(fieldName)
    fieldList = [fieldName]

    print('ANALYSIS')
    an = analysis.analysis(inpPath, fieldList)

    an.subSpaceInds = subSpaceInds
    an.ag_commnds = {}
    an.i_info = i_info
    an.i_resolutions = i_resolutions

    # RUN ANALYSIS
    an.run()

    print('SAVING')
    for res in ress:
        for mode in modes:
            print('\t'+str(res)+mode)
            nco = an.vars[fieldName].ncos[res+mode]
            outFilePath = outPath + '/' + res+mode + '/' + fieldName + '.nc'
            nco.saveToNC(outFilePath)
