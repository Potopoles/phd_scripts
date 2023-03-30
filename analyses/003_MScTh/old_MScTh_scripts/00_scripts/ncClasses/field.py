import numpy as np
import ncClasses.dimension as dim
import sys
import resource as resource
import copy

class field:

    missing_value = -9999
    #missing_values = [-9999, '---'
    #missing_value = np.inf

    def __init__(self, name, ncFile, dims):
        self.name = name
        self.ncFile = ncFile
        self.meta = ncFile[name]
        # THE DIMENSIONS AS GIVEN IN THE NC FILE
        self.fileDimKeys = list(self.meta.dimensions)
        # THE DIMENSIONS AS SHOULD BE USED ACCORDING TO ncObject
        self.dimKeys = [] 
        for dK in self.fileDimKeys:
            if (dK == 'srlon') and ('rlon' in list(dims.keys())):
                self.dimKeys.append('rlon')
            elif (dK == 'srlat') and ('rlat' in list(dims.keys())):
                self.dimKeys.append('rlat')
            elif (dK == 'x_1') and ('x_1' in list(dims.keys())):
                self.dimKeys.append('x_1')
            elif (dK == 'y_1') and ('y_1' in list(dims.keys())):
                self.dimKeys.append('y_1')
            elif dK in list(dims.keys()):
                self.dimKeys.append(dK)

        # TAKE FROM ncObject dims ONLY THOSE THAT ARE WITHIN self.dimKeys
        self.dims = {}
        for key,dim in dims.items():
            #print(key)
            if key in self.dimKeys:
                self.dims[key] = dim


        # GET UNITS AND NAME (label) FROM FILE
        try:
            self.units = ncFile[self.name].units
        except:
            self.units = 'NA'
        self.label = ncFile[self.name].name

        # PREPARE FIELDS values, max AND min
        self.vals = None
        self.max = None
        self.min = None
        
        # Number of dimensions that are not singleton
        self.nNoneSingleton = None


    def setDims(self, dims):
        for i in range(0,len(self.dimKeys)):
            # CURRENTLY NOT TAKING INTO ACCOUNT STAGGERING (TODO?)
            if self.dimKeys[i] == 'srlon':
                self.dimKeys[i] = 'rlon'
            if self.dimKeys[i] == 'srlat':
                self.dimKeys[i] = 'rlat'
            #print(self.dimKeys[i])
            self.dims[self.dimKeys[i]] = dims[self.dimKeys[i]]
        #self.dims = dict((k, dims[k]) for k in self.dimKeys)
        


    ######################## ARITHMETICS
    def add(self, addFld):
        """Add values of addFld"""
        if self.vals.shape == addFld.vals.shape:			
            self.vals = self.vals + addFld.vals
            self._calcMaxMin()
        elif np.sum(np.asarray(self.vals.shape)) == np.sum(np.asarray(addFld.vals.shape)):
            print('WARNING: different ordering')
        else:
            print('ERROR: at field.add --> fields do not have same shape')
    def subtract(self, subFld):
        """Subtracts values of subFld"""
        if self.vals.shape == subFld.vals.shape:			
            self.vals = self.vals - subFld.vals
            self._calcMaxMin()
        elif np.sum(np.asarray(self.vals.shape)) == np.sum(np.asarray(addFld.vals.shape)):
            print('WARNING: different ordering')
        else:
            print('ERROR: at field.add --> fields do not have same shape')
    def multiply(self, addFld):
        """Multiplies itself with values of addFld"""
        if self.vals.shape == addFld.vals.shape:			
            self.vals = self.vals * addFld.vals
            self._calcMaxMin()
        elif np.sum(np.asarray(self.vals.shape)) == np.sum(np.asarray(addFld.vals.shape)):
            print('WARNING: different ordering')
        else:
            print('ERROR: at field.add --> fields do not have same shape')
    def divide(self, addFld):
        """Divides itself by values of addFld"""
        if self.vals.shape == addFld.vals.shape:			
            self.vals = self.vals / addFld.vals
            self._calcMaxMin()
        elif np.sum(np.asarray(self.vals.shape)) == np.sum(np.asarray(addFld.vals.shape)):
            print('WARNING: different ordering')
        else:
            print('ERROR: at field.add --> fields do not have same shape')
    ####################################

    #def getNoneSingletonDims(self):
    #    nsd = []
    #    for key,dim in self.dims.items():
    #        if dim.size > 1:
    #            nsd.append(dim)
    #    return(nsd)

    def _updatenNoneSingleton(self):
        """Checks how many dimensions are non singleton"""
        self.nNoneSingleton = 0
        self.noneSingletonDims = []
        for key,dim in self.dims.items():
            if dim.size > 1:
                self.nNoneSingleton += 1
                self.noneSingletonDims.append(dim)
        
    def transposeToOrder(self, dimOrder):
        """Transposes field values such that the first n dimensions
            are those given by dim Order"""
        dimInds = np.arange(0,len(self.dimKeys))
        oldOrder = []
        for dO in dimOrder:
            oldOrder.append(self._getDimInd(dO))
        otherDims = list(set(dimInds) - set(oldOrder))
        oldOrder.extend(otherDims)
        self.vals = np.transpose(self.vals, oldOrder) # transpose values
        self.dimKeys = np.take(self.dimKeys,oldOrder).tolist() # transpose dimKeys
        
    def loadValues(self, ncFile, ag_commands):
        """Loads the vals np array with field values for dimension selection
            given by self.dims. This means that THIS function actually
            does the subspace cutting and aggregation of the field!"""

        # FIND VALUE INDICES FOR ALL DIMS
        indices = [] # INDICES HOW TO USE THE LOADED ARRAY
        indicesFile = [] # INDICES HOW TO LOAD FROM FILE
        aggreg = []
        for key in self.fileDimKeys:
            if key == 'srlon':
                key = 'rlon'
            #elif key == 'x_1':
            #    key = 'rlon'
            elif key == 'srlat':
                key = 'rlat'
            #elif key == 'y_1':
            #    key = 'rlat'
            if key in self.dimKeys: # IF THE DIMENSION FROM NCFILE SHOULD ALSO BE USED.
                indices.append(self.dims[key].inds)
                indicesFile.append(self.dims[key].inds)
                if key in ag_commands:
                    aggreg.append(ag_commands[key])
                else:
                    aggreg.append(None)				
            else: # IF DUMMY DIMENSION (LIKE FOR INSTANCE time in HSURF)
                indicesFile.append(0)


        # LOAD AND AGGREGATE VALUE ARRAY
        vals = ncFile[self.name][indicesFile]
        vals[vals == self.missing_value] = np.nan # replace missing values
        self.vals = self._aggregate_vals(self.dimKeys, aggreg, vals)

        # AGGREGATE DIMENSIONS
        self._aggregate_dims(self.dimKeys, aggreg)
        
        # CALCULATE MAXIMUM AND MINIMUM VALUES IN VALUE ARRAY
        self._calcMaxMin()

        
    def extractSubspace(self, subSpaceInds):
        """Extract certain subspace of the current values"""
        for key,inds in subSpaceInds.items():
            dimInd = self._getDimInd(key)
            self.vals = np.take(self.vals, inds, axis=dimInd)
        self._updatenNoneSingleton()
        self._calcMaxMin()


    def saveToNC(self, outFile):
        # TODO: Specifically for Radar files
        self.dimKeys = ['rlon' if dk == 'x_1' else dk for dk in self.dimKeys]
        self.dimKeys = ['rlat' if dk == 'y_1' else dk for dk in self.dimKeys]
        
        vals = outFile.createVariable(self.name, 'f4', (self.dimKeys),
                                        fill_value=self.missing_value)
        vals[:] = self.vals
        vals.setncattr('units', self.units)
        vals.setncattr('name', self.label)
        

    def _getDimInd(self, key):
        """For a given dimension key this function returns the index in the field."""
        """Returns None if dimension is not contained"""
        return(self.dimKeys.index(key))
        
                
    def _calcMaxMin(self):
        """Sets maximum and minimum value in Field. Has to updated after
           every change of vals"""
        self.max = np.nanmax(self.vals)
        self.min = np.nanmin(self.vals)
        
    def _copy(self, ncd):
        from copy import deepcopy
        copied = field(self.name, self.ncFile, self.dims)
        
        # SET FIELD VALUES, MAX, MIN
        copied.vals = deepcopy(self.vals)
        copied.max = deepcopy(self.max)
        copied.min = deepcopy(self.min)
        copied.nNoneSingleton = deepcopy(self.nNoneSingleton)
        #copied.setDims(ncd)
        copied._updatenNoneSingleton() 
        #copied.label = deepcopy(self.label)
        #copied.units = deepcopy(self.units) 
        return(copied)

    def prepareForPlotting(self):
        hydrometeors = ['QC','QI','QV','QR','QG','QS','CW','PW']
        TTendencies = ['ATT_MIC', 'ATT_RAD', 'ATT_ADV', 'ATT_ZADV', 'ATT_TURB', 'ATT_TOT', 'ATT_HADV']
        QVTendencies = ['AQVT_MIC', 'AQVT_ADV', 'AQVT_ZADV', 'AQVT_TURB', 'AQVT_TOT', 'AQVT_HADV']


        # ADJUST UNITS
        if self.name in hydrometeors:
            self.vals = self.vals*1000
            self.units = 'g/kg'
        if self.name in TTendencies:
            self.vals = self.vals*3600
            self.units = 'K/hr'
        if self.name in QVTendencies:
            self.vals = self.vals*3600*1000
            self.units = 'g/(kg*hr)'
            self.label = self.name[4:]
        if self.name == 'TOT_PREC':
            self.units = 'mm'
        
        self._calcMaxMin()
        

        # IF DIURNAL CYCLE --> EXPAND VALUES AND DIM AT THE END FOR NICR PLOT
        if 'diurnal' in self.dimKeys:
            ind = self._getDimInd('diurnal')
            diDim = self.dims['diurnal']
            if diDim.vals is not None:
                if len(diDim.vals) == 24:
                    diDim.vals = np.append(diDim.vals, 24)
                    diDim.size = diDim.size + 1
                    diDim.inds = range(0,25) 
            
                    slice0 = np.take(self.vals,indices=0, axis=ind)
                    slice0 = np.expand_dims(slice0,ind)
                    self.vals = np.append(self.vals, slice0, axis=ind)



    #### AGGREGATION FUNCTIONS
    def _aggregate_vals(self, dimKeys, aggreg, vals):
        for i,agg in enumerate(aggreg):
            if self.dims[dimKeys[i]].size > 1:
                if agg == 'MEAN':
                    vals = np.nanmean(vals,i,keepdims=1)
                elif agg == 'SUM':
                    # this version replaces all-nan vectors with 0
                    #vals = np.nansum(vals,i,keepdims=1)
                    # this version replaces all-nan vectors with nan
                    vals = np.nanmean(vals,i,keepdims=1)*vals.shape[i]
                #vals[np.isnan(vals)] = 0
        return(vals)
        
    def _aggregate_dims(self, dimKeys, aggreg):
        for i,agg in enumerate(aggreg):
            if agg == 'MEAN':
                self.dims[dimKeys[i]].updateToAggregate('MEAN')
            elif agg == 'SUM':
                self.dims[dimKeys[i]].updateToAggregate('SUM')
        self._updatenNoneSingleton()
        





    def loadAsDiurnal(self, agg_operation):
        import copy as copy

        # FIND INDICES FOR NONE TIME DIMENSIONS
        extractInds = []
        shapeDiurnal = []
        for i,key in enumerate(self.dimKeys):
            if key != 'time':
                extractInds.append(self.dims[key].inds)
                shapeDiurnal.append(self.dims[key].size)
            else:
                extractInds.append(None)
                timeDimInd = i
                shapeDiurnal.append(24)


        # CREATE DIURNAL FIELD 
        diurnal = np.full(shapeDiurnal, np.nan)

        insertInds = copy.deepcopy(extractInds)
        # LOOP THROUGH HOURS
        for hr in range(0,24):
            insertInds[timeDimInd] = [hr]
            hrInds = []
            for ind,dt in enumerate(self.dims['time'].vals):
                if dt.hour == hr and dt.day not in [10,20]: # ATTENTION LIKE THIS ONLY VALID FOR MASTERTHESIS CASE (TODO)
                    hrInds.append(ind) 

            # DALY AVERAGE (AVERAGE OVER ALL DAYS FOR CURRENT HOUR)
            extractInds[timeDimInd] = hrInds
            vals = self.ncFile[self.name][extractInds]
            vals[vals == self.missing_value] = np.nan # replace missing values
            vals[vals.mask] = np.nan # replace masked values with missing values
            if agg_operation == 'MEAN':
                vals = np.mean(vals, axis=timeDimInd, keepdims=1)
            elif agg_operation == 'SUM':
                vals = np.sum(vals, axis=timeDimInd, keepdims=1)

            # INSERT DAILY AVERAGE HOUR VALUE INTO DIURNAL ARRAY
            insertSlice = []
            for i in range(0,len(insertInds)):
                if len(insertInds[i]) == 1:
                    sliceI0 = insertInds[i][0]
                    sliceI1 = insertInds[i][0]+1
                else:
                    sliceI0 = insertInds[i][0]
                    sliceI1 = insertInds[i][-1]+1
                #sl = slice(insertInds[i].start,insertInds[i].stop)
                sl = slice(sliceI0,sliceI1)
                insertSlice.append(sl)
            diurnal[insertSlice] = vals

        self.vals = diurnal

        self.dims['diurnal'] = self.dims['time']
        self.dims.pop('time')
        self.dims['diurnal'].updateToAggregate('DIURNAL')
        self.dimKeys = ['diurnal' if dk == 'time' else dk for dk in self.dimKeys]

