import os
import ncClasses.ncField as ncField
from ncClasses.subdomains import setSSI
import matplotlib.pyplot as plt
import numpy as np
os.chdir('00_newScripts/')


i_resolutions = 3 
i_subdomain = 0

ssI, domainName = setSSI(i_subdomain, {}) 

inpPath = '../01_rawData/topocut/'
#inpPath = '../01_rawData/'
res = '4.4'
mode = ''
ncFileName = 'lffd2006071515z.nc'
#ncFileName = 'constantParams.nc'

#inpPath = '../02_fields/topocut/'
#res = '4.4'
#mode = ''
#ncFileName = 'zQV.nc'


srcNCPath = inpPath + res + mode + '/' + ncFileName
print(srcNCPath)
qc = ncField.ncField('QC', srcNCPath, ssI)
#qc.saveToNewNC('../uTest.nc')
qc.addVarToExistingNC('../uTest.nc')
#plt.contourf(qc.vals[0,10,:,:].squeeze())
#plt.colorbar()
#plt.show()
