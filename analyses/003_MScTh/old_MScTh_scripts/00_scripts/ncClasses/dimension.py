import numpy as np
from datetime import datetime
from datetime import timedelta

class dimension:

    def __init__(self, ncFile, key, dx):
        self.ncFile = ncFile # if dim is built from multiple files only first one is saved here
        self.key = key
        self.dx = float(dx)
        # Get dimension size from nc file (thus not cut to any subspace)
        self.size = self.ncFile.dimensions[key].size
        
        # inds means indices of dimension that should be used
        self.inds = list(range(0,self.size))
        
        # values of this dimension (not cut down to subspace) and physical units and ax label
        # DIMENSION VALUES
        self.vals = None
        # UNITS
        self.units = None
        # LABEL TO USE FOR AXIS IN PLOTS
        self.label = None
        # VALUE TYPE OF DIMENSION: OPTIONS: 'DATE' or 'NUM'
        self.valType = None
        # LOAD vals, units, label, valType
        self._loadValuesFromFile()

        #self.function = None
        # HOW DIMENSION IS AGGREGATED
        self.agg_mode = None
        
        
    def cutToSubspace(self, inds):
        """inds = indice borders. Changes the inds and updates size"""
        # IF DIMENSION IS SET AND SUBSPACEABLE
        if self.vals is not None:
            # Set indices and size
            self.inds = inds
            self.size = len(self.inds)
            # Cut values of dimension to subspace
            self.vals = np.take(self.vals, self.inds, axis=0)
        else:
            raise ValueError('Dimension' + self.key + 'is not set!')
        
    def updateToAggregate(self, mode):
        """If field was aggregated this function adjusts the dimension"""
        if mode == 'MEAN':
            self.inds = list(range(0,1))
            self.size = 1
            self.vals = None
            self.agg_mode = 'MEAN'
        elif mode == 'SUM':
            self.inds = list(range(0,1))
            self.size = 1
            self.vals = None
            self.agg_mode = 'SUM'
        elif mode == 'DIURNAL': # THIS IS DONE BY NCOBJECT LOADASDIURNAL FUNCTION
            #self.inds = range(0,25)
            self.inds = list(range(0,24))
            #self.size = 25
            self.size = 24
            #self.vals = np.arange(0,25)
            self.vals = np.arange(0,24)
            #self.vals = np.append(self.vals, 0)
            self.units = ''
            self.label = 'day time'
            self.valType = 'DIURNAL'
            self.agg_mode = 'DIURNAL'
            self.key = 'diurnal'
        else:
            raise ValueError('ERROR: UNKNOWN AGGREGATE MODE')
        
    def _loadValuesFromFile(self):
        """Loads the dimension vals, units, label and valType from nc file"""
        """This function is highly adjusted to the nc files in use"""

        horizontalKeys = ['rlon', 'rlat', 'srlon', 'srlat', 'x_1', 'y_1']
        
        if self.key == 'bnds':
            pass
            
        elif self.key == 'time':
            timeSec = self.ncFile[self.key][:]
            dt0 = datetime.strptime('2006-07-11 00:00:00', '%Y-%m-%d %H:%M:%S')
            dtime = dt0 + timeSec*timedelta(seconds=1)
            self.vals = dtime
            self.label = 'Date'
            self.units = ''
            self.valType = 'DATE'
            self.agg_mode = None
            #self.function = 'time'
            
        elif self.key == 'diurnal':
            self.vals = self.ncFile[self.key][:]
            self.label = 'Hour'
            self.units = ''
            self.valType = 'DIURNAL'                
            self.agg_mode = 'DIURNAL'

        elif self.key in horizontalKeys: 
            # CURRENTLY IGNORING STAGGERING (TODO?)
            if self.key == 'srlon':
                self.key = 'rlon'
            elif self.key == 'srlat':
                self.key = 'rlat'
            elif self.key == 'srlat':
                self.key = 'rlat'
            elif self.key == 'x_1':
                self.key = 'rlon'
            elif self.key == 'y_1':
                self.key = 'rlat'


            self.vals = np.arange(0,self.size)*self.dx
            if self.key == 'rlon':
                self.label = 'longitude'
                self.label = 'x'
            elif self.key == 'rlat':
                self.label = 'latitude'
                self.label = 'y'
            self.units = 'km'
            self.valType = 'NUM'
            #self.function = 'hor'
            
        elif self.key == 'altitude':
            #self.vals = np.append(np.arange(0,6000,100), np.arange(6000,10001,1000))
            self.vals = np.append(np.arange(0,6,0.1), np.arange(6,10.1,1))
            self.label = 'Altitude'
            #self.units = 'm'
            self.units = 'km'
            self.valType = 'NUM'
            #self.function = 'vert'
        else:
            raise ValueError('UNKNOWN DIMENSION KEY! CODE NEEDS TO BE EXTENDED!')
                
        
    def extendInTime(self, timeDims):
        """Append all dimensions objects in timeDims to this one"""
        for td in timeDims:
            self.size = self.size + td.size
            self.valsUncut = np.append(self.valsUncut, td.valsUncut)
            self.vals = np.append(self.vals, td.vals)
        self.inds = range(0,self.size)
        
    def _copy(self):
        from copy import deepcopy
        copied = dimension(self.ncFile, self.key, self.dx)

        copied.vals = deepcopy(self.vals)
        copied.size = deepcopy(self.size)
        copied.inds = deepcopy(self.inds)
        
        copied.units = deepcopy(self.units)
        copied.label = deepcopy(self.label)
        copied.valType = deepcopy(self.valType)
        copied.agg_mode = deepcopy(self.agg_mode)
        
        return(copied)

    def saveToNC(self, outFile):
        #self.outFile.dimensions[self.key].size = self.size
        selfnc = outFile.createDimension(self.key, self.size) 
        if self.key == 'time':
            vals = outFile.createVariable(self.key, 'f8', (self.key))
        elif self.key == 'diurnal':
            vals = outFile.createVariable(self.key, 'i2', (self.key))
        else:
            vals = outFile.createVariable(self.key, 'f4', (self.key))

        # CONVERT DATETIME OBJECTS BACK TO SECONDS SINCE 2006-07-11
        if self.valType == 'DATE':
            dt0 = datetime.strptime('2006-07-11 00:00:00', '%Y-%m-%d %H:%M:%S')
            timeSec = np.empty([len(self.vals)])
            for i,ts in enumerate(self.vals):
               timeSec[i] = (ts - dt0).total_seconds()
            self.vals = timeSec
            
        vals[:] = self.vals
