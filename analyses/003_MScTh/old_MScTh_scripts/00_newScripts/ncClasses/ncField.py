import ncClasses.dimension as dimension
import numpy as np

class ncField:
    from netCDF4 import Dataset
    missing_value = 9.96920997e36 

    def __init__(self, fieldName, srcNCPath, ssI):
        # Name of field to look at in ncFile
        self.fieldName = fieldName
        # Path to ncFile
        self.srcNCPath = srcNCPath

        self.ncFile = self.Dataset(self.srcNCPath,'r')

        # dims: Dictionary containing dimensions
        # dfks: Keys of dimensions used by field in the right order
        self.dims, self.fdks = self._loadDimsFromNC()
        self.fdks = list(self.ncFile[self.fieldName].dimensions)
        
        # Cut dimensions to Subspace
        # Subspace indices
        self.ssI = ssI
        self.cutDimsToSubSpace()

        # Value of variable
        self.vals = None 
        # Max and Min values of variable
        self.min = None
        self.max = None

        # Information for plotting
        self.units = self.ncFile[self.fieldName].units
        # How field will be labeled to during plotting
        self.label = self.ncFile[self.fieldName].name

        # TODO NOT YET IMPLEMENTED
        # Number of dimensions that are not singleton
        self.nNoneSingleton = None

    def loadValues(self):
        selInds = []
        for key in self.fdks:
            selInds.append(self.dims[key].inds)
        self.vals = self.ncFile[self.fieldName][selInds] 
        if self.vals.count() == self.vals.shape[1]*self.vals.shape[2]*self.vals.shape[3]:
            raise ValueError('Array has Topography values not set to nan')
        #self.vals[self.vals == self.missing_value] = np.nan
        self.calcMaxMin()
         

    def calcMaxMin(self):
        """Sets maximum and minimum value in."""
        self.max = np.nanmax(self.vals)
        self.min = np.nanmin(self.vals)
        
    def _loadDimsFromNC(self):
        keysRaw = self.ncFile[self.fieldName].dimensions
        keysFinal = []
        dims = {}
        for key in keysRaw:
            # CASE SPECIFIC STUFF: MAKE SURE VARIABLE 'HSURF' DOES NOT GET TIME DIMENSION!
            if self.fieldName == 'HSURF' and key == 'time':
                pass
            else:
                #if key == 'srlon':
                #    key = 'rlon'
                #elif key == 'srlat':
                #    key = 'rlat'
                dim = dimension.dimension(self.ncFile, key)
                keysFinal.append(key)
                dims[key] = dim
        return(dims, keysFinal)
        
        
    def cutDimsToSubSpace(self):
        """
        Selects only a dimension subspace of parent nc file
        and applies this to dimensions. ssI must be set before.
        This functions must be used before vals are loaded
        """
        if self.ssI is None:
            raise AttributeError('ssI is not set!')
        for key,inds in self.ssI.items():
            if key in self.fdks:
                self.dims[key].cutToSubspace(inds)


            
    def saveToNewNC(self, outFilePath):
        """Saves itself into a NC file and thus overwrites existing files!""" 
        from netCDF4 import Dataset
        rootgrp = Dataset(outFilePath, 'w', format='NETCDF4')

        for key,dim in self.dims.items():
            dim.saveToNC(rootgrp)
        vals = rootgrp.createVariable(self.fieldName, 'f4', (self.fdks))
        vals[:] = self.vals
        vals.setncattr('units', self.units)
        vals.setncattr('name', self.label)
        rootgrp.close()
     
    def addVarToExistingNC(self, outFilePath):
        """
        Saves itself as an additional variable into an existing nc file.
        If self has dimension that does not exist in nc, adds this dim to nc.
        Tests:
            Existing dimensions have same shape?
            Field not yet contained in nc?
        """ 
        from netCDF4 import Dataset
        rootgrp = Dataset(outFilePath, 'a', format='NETCDF4')
        ncDimKeys = rootgrp.dimensions.keys()

        # Check if dimensions already in nc.
        for key in self.fdks:
            if key in ncDimKeys:
                # check if dimensions have same size
                if rootgrp.dimensions[key].size == self.dims[key].size:
                    pass # same size --> all fine!
                else:
                    print(rootgrp.dimensions[key].size)
                    print(self.dims[key].size)
                    rootgrp.close()
                    raise ValueError('Dimension '+str(key)+' size does not match between '+
                                        'ncField and nc file equivalent!')
                    
            else:
                print('ADDING DIMENSION '+str(key)+' TO '+str(outFilePath))
                self.dims[key].saveToNC(rootgrp)
                
        # Check that variable does not yet exist
        if self.fieldName in rootgrp.variables.keys():
            import warnings
            warnings.warn('Field '+self.fieldName+
                            ' already in nc file! Did nothing.')
        else:
            vals = rootgrp.createVariable(self.fieldName, 'f4', (self.fdks))
            vals[:] = self.vals
            vals.setncattr('units', self.units)
            vals.setncattr('name', self.label)
        rootgrp.close()

    def copy(self):
        from copy import deepcopy
        copied = ncField(self.fieldName, self.srcNCPath, self.ssI)
        for key,dim in self.dims.items():
            copied.dims[key] = dim.copy()
        copied.vals = self.vals
        return(copied)

    #def prepareAggregate(self, ag_commnds):
    #    """Tell the field how it should aggregate when it is
    #        loaded. This commmand has to be run before loadField()!"""
    #    self.ag_commnds = {}
    #    for key,agc in ag_commnds.items():
    #        if key in self.field.dims:
    #            self.ag_commnds[key] = agc
    #    ## DELETE ALL AGGREGATION COMMANDS FOR WHICH THE DIMENSION IS LEN = 1 OR THAT ARE
    #    ## NOT CONTAINED IN THE DIMENSION
    #    #removeKeys = []
    #    #for key,agc in ag_commnds.items():
    #    #    if key in self.field.dims:
    #    #        if self.field.dims[key].size == 1:
    #    #            removeKeys.append(key)
    #    #
    #    #for rK in removeKeys:
    #    #    del ag_commnds[rK]
    #    ##SAVE COMMANDS
    #    #self.ag_commnds = ag_commnds
        
    #def aggregate(self, ag_commnds):
    #    """Only run after field is already loaded. Aggregate according to ag_commnds"""
    #    aggreg = []
    #    for key in self.field.dimKeys:
    #        if key in ag_commnds:
    #            aggreg.append(ag_commnds[key])
    #        else:
    #            aggreg.append(None)
    #    #self.ag_commnds = ag_commnds # DO NOT UPDATE AGG COMMANDS TODO
    #    self.field.vals = self.field._aggregate_vals(self.field.dimKeys,
    #                                                aggreg, self.field.vals)
    #    self.field._aggregate_dims(self.field.dimKeys, aggreg)
        
        
    #def cutOutTopo(self, topo):
    #    
    #    self.ncFile.close()
    #    self.ncFile = self.Dataset(self.inpFilePath,'a')
    #    
    #    indices = []
    #    topoInds = []
    #    altDim = None
    #    tDim = None
    #    for i,key in enumerate(self.field.dimKeys):
    #        if key == 'time':
    #            indices.append(None)
    #            tDim = i
    #            topoInds.append(range(0,1))
    #        elif key == 'altitude':
    #            altDim = i
    #            indices.append(None)
    #        else:
    #            indices.append(self.field.dims[key].inds)
    #            topoInds.append(topo.field.dims[key].inds)
    #    
    #    
    #    if 'altitude' in self.field.dimKeys:
    #        for tInd in self.field.dims['time'].inds:
    #            for aInd in self.field.dims['altitude'].inds:
    #                if aInd <= 43: # ABOVE THERE ARE NO MOUNTAINS
    #                    height = self.field.dims['altitude'].vals[aInd]

    #                    indices[tDim] = range(tInd,tInd+1)
    #                    indices[altDim] = range(aInd,aInd+1)

    #                    selfSlice = self.ncFile[self.field.name][indices]

    #                    topoSlice = topo.ncFile[topo.field.name][topoInds]
    #                    topoSlice = np.expand_dims(topoSlice, axis=altDim)

    #                    selfSlice[topoSlice > height] = self.missing_value

    #                    s0 = slice(indices[0].start,indices[0].stop)
    #                    s1 = slice(indices[1].start,indices[1].stop)
    #                    s2 = slice(indices[2].start,indices[2].stop)
    #                    s3 = slice(indices[3].start,indices[3].stop)
    #                        
    #                    self.ncFile[self.field.name][s0,s1,s2,s3] = selfSlice

    #    self.ncFile.close()
    #    self.ncFile = self.Dataset(self.inpFilePath,'r')
        
    #def loadAsDiurnal(self, agg_operation):
    #    self.field.loadAsDiurnal(agg_operation)
    #    self.dims['diurnal'] = self.dims['time']
    #    del self.dims['time']
        
          




        
        





    #def cutOutTopo(self, topo):
    #    """From currently selected (but not loaded) field cuts out all values that are within topography.
    #       Sets these values to nan. Saves the topoCut file to output directory"""
    #    
    #    indices = []
    #    topoInds = []
    #    altDim = None
    #    tDim = None
    #    for i,key in enumerate(self.curFld.dimKeys):
    #        if key == 'time':
    #            indices.append(None)
    #            tDim = i
    #            topoInds.append(range(0,1))
    #        elif key == 'altitude':
    #            altDim = i
    #            indices.append(None)
    #        else:
    #            indices.append(self.curFld.dims[key].inds)
    #            topoInds.append(topo.curFld.dims[key].inds)
    #    
    #    
    #    for tInd in self.curFld.dims['time'].inds:
    #        for aInd in self.curFld.dims['altitude'].inds:
    #            
    #            height = self.curFld.dims['altitude'].vals[aInd]

    #            indices[tDim] = range(tInd,tInd+1)
    #            indices[altDim] = range(aInd,aInd+1)

    #            selfSlice = self.curFld.vals[indices]

    #            topoSlice = topo.curFld.vals[topoInds]
    #            topoSlice = np.expand_dims(topoSlice, axis=altDim)

    #            selfSlice[topoSlice > height] = self.missing_value

    #            s0 = slice(indices[0].start,indices[0].stop)
    #            s1 = slice(indices[1].start,indices[1].stop)
    #            s2 = slice(indices[2].start,indices[2].stop)
    #            s3 = slice(indices[3].start,indices[3].stop)
    #                
    #            self.vals[s0,s1,s2,s3] = selfSlice
