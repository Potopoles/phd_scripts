import numpy as np
import ncClasses.ncObject as ncObject

class LoadField:

    def __init__(self, inpPath, res, mode, subSpaceInds):
        self.inpPath = inpPath
        self.res = res
        self.mode = mode
        self.subSpaceInds = subSpaceInds
 
    def loadField(self, fileName, varName):
        inpFilePath = self.inpPath + '/' + self.res+self.mode + '/' + fileName 
        VAR = ncObject.ncObject(inpFilePath, varName, self.res)
        VAR.selField(varName)
        VAR.selSubspace(self.subSpaceInds)
        VAR.loadField()
        var = VAR.curFld.vals
        return(VAR, var)





def vertProf(var, rho):
    densityWeight = 1

    if densityWeight:
        M_prof = np.nansum(rho*1E6, axis=(2,3))
        # MAKE SURE LEVELS WITH ONLY NAN ARE NOT 0 BUT NAN!
        M_prof[np.abs(M_prof) < 1E-20] = np.nan
        #print(M_prof)
        var_prof = np.nansum(rho*var*1E6, axis=(2,3))
        # MAKE SURE LEVELS WITH ONLY NAN ARE NOT 0 BUT NAN!
        var_prof[np.abs(var_prof) < 1E-20] = np.nan
        #print(var_prof)

        # DIVIDE BY TOTAL MASS OF LAYER
        var_prof = var_prof/M_prof
        #print(var_prof)
    else:
        var_prof = np.nanmean(var, axis=(2,3))
    return(var_prof)

