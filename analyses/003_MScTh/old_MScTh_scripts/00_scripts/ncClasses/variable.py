#import ncClasses.modelRes as modelRes
import numpy as np
import copy as copy
from timeit import default_timer as timer
from datetime import datetime, timedelta

# CLASS USED TO HANDLE SEVERAL ncObjects THAT DESCRIBE A SPECIFIC VARIABLE
# CAN PERFORM OPERATIONS WITH OTHER VARIABLES.
class variable:
    from netCDF4 import Dataset

    modes = ['f', ''] # '' = raw, 'f' = filtered
    modeNames = ['SM', 'RAW']

    # TODO TMP
    modes = ['f', '', 'r'] # '' = raw, 'f' = filtered
    modeNames = ['SM', 'RAW', 'OBS']

    def __init__(self, varName):
        self.varName = varName
        
        # WILL CONTAIN ALL ncObjects THAT REPRESENT THE NCFILES OF THIS variable.
        self.ncos = {}
        # MAXIMUM AND MINIMUM VALUES OF ALL ncObjects fields.
        self.max = -np.Inf 
        self.min = np.Inf 
        
        # ATTRIBUTES USED EXTERNALLY
        self.name = None
        self.label = None

    #def addNco(self, mrKey, mr):
    #    self.modelRes[mrKey] = mr
    #    self.name = mr.ncos['U'].curFld.name
    #    self.label = mr.ncos['U'].curFld.label
    #    self.nNoneSingleton = mr.ncos['U'].curFld.nNoneSingleton

    def setValueLimits(self):
        """Get min and max of all used resolutions for each mode (U,F,D)."""
        self.max = -np.Inf
        self.min = np.Inf
        for key,nco in self.ncos.items():
            nco.field._calcMaxMin()
            if nco.field.max > self.max:
                self.max = nco.field.max
            if nco.field.min < self.min:
                self.min = nco.field.min


    #### ARITHMETICS WITH 2 FIELDS
    #def addVar(self, var, label):
    #    """Clones itself and adds the field values of variable 'var'"""
    #    copied = self._copy()
    #    for res in self.resolutions:
    #        for mdNm in self.mdNms:
    #            copied.modelRes[res].ncos[mdNm].curFld.add(var.modelRes[res].ncos[mdNm].curFld)
    #            # SET LABEL TO FIELD
    #            copied.modelRes[res].ncos[mdNm].curFld.label = label
    #            # SET NAME TO NCO
    #            copied.modelRes[res].ncos[mdNm].name = self.modelRes[res].ncos[mdNm].name
    #    copied.label = label
    #    copied.setValueLimits()
    #    return(copied)
    #def subtractVar(self, var, label):
    #    """Clones itself and subtracts the field values of variable 'var'"""
    #    copied = self._copy()
    #    for res in self.resolutions:
    #        for mdNm in self.mdNms:
    #            copied.modelRes[res].ncos[mdNm].curFld.subtract(var.modelRes[res].ncos[mdNm].curFld)
    #            # SET LABEL TO FIELD
    #            copied.modelRes[res].ncos[mdNm].curFld.label = label
    #            # SET NAME TO NCO
    #            copied.modelRes[res].ncos[mdNm].name = self.modelRes[res].ncos[mdNm].name
    #    copied.label = label
    #    copied.setValueLimits()
    #    return(copied)
    #def multiplyVar(self, var, label):
    #    """Clones itself and multiplies it with the field values of variable 'var'"""
    #    copied = self._copy()
    #    for res in self.resolutions:
    #        for mdNm in self.mdNms:
    #            copied.modelRes[res].ncos[mdNm].curFld.multiply(var.modelRes[res].ncos[mdNm].curFld)
    #            # SET LABEL TO FIELD
    #            copied.modelRes[res].ncos[mdNm].curFld.label = label
    #            # SET NAME TO NCO
    #            copied.modelRes[res].ncos[mdNm].name = self.modelRes[res].ncos[mdNm].name
    #    copied.label = label
    #    copied.setValueLimits()
    #    return(copied)
    #def divideVar(self, var, label):
    #    """Clones itself and divide it by the field values of variable 'var'"""
    #    copied = self._copy()
    #    for res in self.resolutions:
    #        for mdNm in self.mdNms:
    #            copied.modelRes[res].ncos[mdNm].curFld.divide(var.modelRes[res].ncos[mdNm].curFld)
    #            # SET LABEL TO FIELD
    #            copied.modelRes[res].ncos[mdNm].curFld.label = label
    #            # SET NAME TO NCO
    #            copied.modelRes[res].ncos[mdNm].name = self.modelRes[res].ncos[mdNm].name
    #    copied.label = label
    #    copied.setValueLimits()
    #    return(copied)




    #### SIMPLE ARITHMETICS
    #def addConst(self, const):
    #    """Adds a number to the field"""
    #    for res in self.resolutions:
    #        for mdNm in self.mdNms:
    #            self.modelRes[res].ncos[mdNm].curFld.vals = self.modelRes[res].ncos[mdNm].curFld.vals + const
    #    self.setValueLimits()
    #def subConst(self, const):
    #    """Subtracts a number from the field"""
    #    for res in self.resolutions:
    #        for mdNm in self.mdNms:
    #            self.modelRes[res].ncos[mdNm].curFld.vals = self.modelRes[res].ncos[mdNm].curFld.vals - const
    #    self.setValueLimits()
    #def multConst(self, const):
    #    """Multiplies the field with a number"""
    #    for res in self.resolutions:
    #        for mdNm in self.mdNms:
    #            self.modelRes[res].ncos[mdNm].curFld.vals = self.modelRes[res].ncos[mdNm].curFld.vals * const
    #    self.setValueLimits()
        

    ### FUNCTIONS TO CHANGE CERTAIN STUFF
    #def setFieldUnits(self, newUnits):
    #    for res in self.resolutions:
    #        for mdNm in self.mdNms:
    #            self.modelRes[res].ncos[mdNm].curFld.units = newUnits
        
               
               
    def _copy(self):
        from copy import deepcopy
        copied = variable(self.varName)
        copied.modes = self.modes
        copied.modeNames = self.modeNames
        for key,nco in self.ncos.items():
            copied.ncos[key] = self.ncos[key]._copy()
        copied.setValueLimits()
        return(copied)
