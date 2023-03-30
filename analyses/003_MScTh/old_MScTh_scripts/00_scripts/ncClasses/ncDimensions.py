import numpy as np
import ncClasses.dimension as dimension

class ncDimensions:
    #def __init__(self, ncFile):
    #    self.keys = [] # contains the key of all dimensions
    #    self.dims = {} # contains all dimensions
    #    self.ncFile = ncFile        
    #    self._loadDims(ncFile, self.keys, self.dims)
    #    
    #    self.ndim = len(self.dims)
        
        
            

    #def cutDimsToSubsp(self, subSpaceInds):
    #    """Cuts each dimension to fit in subspace"""
    #    for key,inds in subSpaceInds.items():
    #        if key in self.dims.keys():
    #            self.dims[key].cutToSubspace(inds)
            
        
    #def _loadDims(self, ncFile, keys, dims):
    #    """Load list of dimension"""
    #    for key,value in ncFile.dimensions.items():
    #        keys.append(key)
    #        dims[key] = dimension.dimension(ncFile, key)

            
    def _copy(self):
        from copy import deepcopy
        copied = ncDimensions(self.ncFile)
        for key,dim in self.dims.items():
            copied.dims[key] = dim._copy()
        
        return(copied)

    #def saveToNC(self, outFile):
    #    for key,dim in self.dims.items():
    #        print(key)
    #        print(dim.key)
    #        print()
    #        dim.saveToNC(outFile)
