import ncClasses.dimension as dimension
import ncClasses.field as fld
import numpy as np
import matplotlib.pyplot as plt

class ncObject:
    from netCDF4 import Dataset
    missing_value = np.nan

    def __init__(self, inpFilePath, dx, fieldName):
        self.inpFilePath = inpFilePath
        # HORIZONTAL GRID SPACING
        self.dx = dx
        self.fieldName = fieldName
        #print(self.inpFilePath)
        self.ncFile = self.Dataset(self.inpFilePath,'r')
        self.dims = self._loadDims()
        
        self.subSpaceInds = None
        
        # FIELD THAT CONTAINS THE VALUES
        self.field = fld.field(fieldName, self.ncFile, self.dims)

        
    def cutDimsToSubSpace(self):
        """selects only a dimension subspace of parent nc file"""
        """and applies this to dimensions. subSpaceInds must be set before."""
        """If used, this functions must be used before field is loaded"""
        if self.subSpaceInds is None:
            raise AttributeError('SubSpaceInds is not set!')
        for key,inds in self.subSpaceInds.items():
            if key in self.dims.keys():
                self.dims[key].cutToSubspace(inds)
            
    def extractSubspace(self, subSpaceInds):
        """extracts a dimension subspace of currently loaded field"""
        """This function is supposed to be used when the field is loaded
            already"""
        #self.subSpaceInds = subSpaceInds # DO NOT UPDATE SUBSPACEINDS TODO
        #self.ncd.cutDimsToSubsp(subSpaceInds)
        for key,inds in subSpaceInds.items():
            if key in self.dims.keys():
                self.dims[key].cutToSubspace(inds)
        self.field.extractSubspace(subSpaceInds)
        
    def prepareAggregate(self, ag_commnds):
        """Tell the field how it should aggregate when it is
            loaded. This commmand has to be run before loadField()!"""
        self.ag_commnds = {}
        for key,agc in ag_commnds.items():
            if key in self.field.dims:
                self.ag_commnds[key] = agc
        
    def aggregate(self, ag_commnds):
        """Only run after field is already loaded. Aggregate according to ag_commnds"""
        aggreg = []
        for key in self.field.dimKeys:
            if key in ag_commnds:
                aggreg.append(ag_commnds[key])
            else:
                aggreg.append(None)
        #self.ag_commnds = ag_commnds # DO NOT UPDATE AGG COMMANDS TODO
        self.field.vals = self.field._aggregate_vals(self.field.dimKeys,
                                                    aggreg, self.field.vals)
        self.field._aggregate_dims(self.field.dimKeys, aggreg)
        
                
    def loadValuesOfField(self):
        """Loads the values of the selected field and performs
            aggregation at the same time to save memory"""
        #if hasattr(self, 'ag_commnds') is False:
        #    self.ag_commnds = {}
        self.field.loadValues(self.ncFile, self.ag_commnds)
        
        
    def loadAsDiurnal(self, agg_operation):
        self.field.loadAsDiurnal(agg_operation)
        self.dims['diurnal'] = self.dims['time']
        del self.dims['time']
        
          

    # TODO is this function even used? maybe topocut? But why Dataset('w')???
    # If the file exists it should be 'a', I guess.
    def saveToExistingNC(self, outFilePath):
        """Saves copy of itself into an existing NC file and thus overwrites existing file!""" 
        from netCDF4 import Dataset
        rootgrp = Dataset(outFilePath, 'w', format='NETCDF4')

        for key,dim in self.dims.items():
            dim.saveToNC(rootgrp)
        self.field.saveToNC(rootgrp)
        rootgrp.close()

    def saveToNewNC(self, outFilePath):
        """Saves copy of itself into a new NC file.""" 
        from netCDF4 import Dataset
        rootgrp = Dataset(outFilePath, 'w', format='NETCDF4')

        for key,dim in self.dims.items():
            dim.saveToNC(rootgrp)
        self.field.saveToNC(rootgrp)
        rootgrp.close()

    def appendTimeToExistingNC(self, outFilePath):
        """Saves copy of itself into a new NC file.""" 
        from netCDF4 import Dataset
        rootgrp = Dataset(outFilePath, 'w', format='NETCDF4')

        for key,dim in self.dims.items():
            dim.saveToNC(rootgrp)
        self.field.saveToNC(rootgrp)
        rootgrp.close()


    def _loadDims(self):
        dims = {}
        for key,value in self.ncFile.dimensions.items():
            # CASE SPECIFIC STUFF: MAKE SURE VARIABLE 'HSURF' DOES NOT GET TIME DIMENSION!
            if self.fieldName == 'HSURF' and key == 'time':
                pass
            else:
                dim = dimension.dimension(self.ncFile, key, self.dx)
            # MORE CASE SPECIFIC STUFF: NAME STAGGERED DIMENSION EQUAL TO UNSTAGGERED (TODO)
            if key == 'srlon':
                key = 'rlon'
            elif key == 'srlat':
                key = 'rlat'
            # ADD DIMENSION TO LIST IF IT EXISTS (SEE EXCEPTION ABOVE)
            try:
                dims[key] = dim 
            except:
                pass
        self.ndims = len(dims)
        return(dims)
        
        
    def _copy(self):
        from copy import deepcopy
        copied = ncObject(self.inpFilePath, self.dx, self.fieldName)
        copied.ncFile = self.Dataset(self.inpFilePath,'r')
        for key,dim in self.dims.items():
            copied.dims[key] = dim._copy()
        
        copied.subSpaceInds = deepcopy(self.subSpaceInds)
        
        copied.field = self.field._copy(copied.dims)

        return(copied)



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
