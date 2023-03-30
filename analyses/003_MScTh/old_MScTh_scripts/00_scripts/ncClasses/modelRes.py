import ncClasses.ncObject as ncObject
import ncClasses.ncDimensions as ncDimensions
import ncClasses.field as fld
import numpy as np
from timeit import default_timer as timer



class modelRes:
    from netCDF4 import Dataset
        
    mdNms = ['U', 'F', 'D']

    #def __init__(self, inpFolder, inpFileName, resolution, i_info):
    #    
    #    self.inpFolder = inpFolder
    #    self.resolution = resolution
    #    self.inpFileName = inpFileName
    #    self.i_info = i_info
    #    
    #    
    #    self.ncos = dict(U=None,F=None,D=None)
    #    
    #    # LOAD UNFILTERED MODEL
    #    modelName = self.resolution
    #    inpFilePath = self.inpFolder + '/' + modelName + '/' + inpFileName
    #    name = self.resolution + ''
    #    if self.i_info >= 4:
    #            print('\t\t\t'+inpFilePath)
    #    self.ncos['U'] = ncObject.ncObject(inpFilePath, name, self.resolution)

    #    # LOAD UNFILTERED PLACEHOLDER FOR DIFFERENCE MODEL (later subtract filtered)
    #    name = self.resolution + 'd'
    #    self.ncos['D'] = ncObject.ncObject(inpFilePath, name, self.resolution)
    #    
    #    # LOAD FILTERED MODEL
    #    modelName = self.resolution + 'f'
    #    inpFilePath = self.inpFolder + '/' + modelName + '/' + inpFileName
    #    name = self.resolution + 'f'
    #    self.ncos['F'] = ncObject.ncObject(inpFilePath, name, self.resolution)

                
        
    #def selSubspace(self):
    #    """For each ncObject tell it to select the subspace"""
    #    for key,nco in self.ncos.items():
    #            nco.selSubspace(self.subSpaceInds)

    #def selField(self, name):
    #    """For each ncObject tell it to select the field 'name'
    #            However does not yet load the values of the fields
    #            Only prepares dimensions"""
    #    self.ncos['U'].selField(name)
    #    self.ncos['F'].selField(name)
    #    self.ncos['D'].selField(name)
            
    #def prepareAggregate(self, ag_commnds):
    #    """Tells each ncObject to aggregate"""
    #    self.ncos['U'].prepareAggregate(ag_commnds)
    #    self.ncos['F'].prepareAggregate(ag_commnds)
    #    self.ncos['D'].prepareAggregate(ag_commnds)

                    
    #def loadFields(self):
    #    """For each ncObject tell it to load the values of the selected
    #    field. Also, calculates the field values of the ncObject
    #    'Difference'"""

    #    self.ncos['U'].loadField()
    #    self.ncos['F'].loadField()
    #    self.ncos['D'].loadField()
    #    self.ncos['D'].curFld.subtract(self.ncos['F'].curFld)
            
                    
                    
    #def cutOutTopo(self, topo):
    #    print('U')
    #    self.ncos['U'].cutOutTopo(topo['U'])
    #    print('F')
    #    self.ncos['F'].cutOutTopo(topo['F'])
            
    def _copy(self):
        from copy import deepcopy
        copied = modelRes(self.inpFolder, self.inpFileName, self.resolution, self.i_info)
        
        copied.ncos['U'] = self.ncos['U']._copy()
        copied.ncos['F'] = self.ncos['F']._copy()
        copied.ncos['D'] = self.ncos['D']._copy()
        return(copied)

            
