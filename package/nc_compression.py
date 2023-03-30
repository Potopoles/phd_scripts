#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description:    Functions to compress nc files using nczip (IAC, by Urs Beyerle)
author:         Christoph Heim
date created:   29.02.2020
date changed:   16.09.2021 
usage:          import from another python script 

Python wrapper functions for the IAC internal tool nczip ( which is based
on NCO ncpdq ) to compress nc files. One can do conserving compression
(lossy=False) or lossy compression (lossy=True).

The scripts are based on the assumption that the files to compress
contain for one atmospheric field the output of one day. The idea behind this
is: a) to allow for easy parallelization by running the compression
(and later the analysis) of several days in 12 parallel tasks on daint,
and b) to have files of reasonable size (not too small and not too big),
irrespective of whether its a 2D or a 3D file.

It should however be easy to change the scripts for different file
structures.

Conserving compression:
- Saves roughly 50% of disk space for an average COSMO model output
  but can save less or much more, depending on the variable considered
  and the size of the file. Optimal are variables with most values != 0 only
  at a few locations (e.g. precipitation) and large files. Like this, one
  can save up to 90% of disk space by compression.

Lossy compression:
- Converts data type of variable to short (16 bit, ~ 64'000 possible values)
  and represents a loss in data quality. For analysis, this is probably
  never an issue.
- Saves 50% of disk space in comparison to float data type output (COSMO).
- Cannot simply be applied to multi-file data set because conversion is based
  on maximum/minimum values of file. If the max-min values change strongly
  between different files, the compressed output time series will contain
  jumps (was clearly visible in my case for cloud water (check e.g. TQC).
- To prevent this problem, this file contains a function find_minmax_val 
  which can be used to determine global max/min value of all files to
  compress. It can then be given as input to the lossy compression function 
  compress_date_lossy.
- Given this problem, lossy compression is relatively cumbersome..
  .. in addition there seems to be a memory leak somewhere and the scripts
  run out of memory very quickly...
"""
###############################################################################
import os, glob, subprocess, sys, time, shutil, psutil
import xarray as xr
import numpy as np
from netCDF4 import Dataset
from package.utilities import Timer
from package.nl_models import nlm
###############################################################################


debug_level_1 = 2
debug_level_2 = 3
debug_level_3 = 4
debug_level_4 = 5

def compress_file(file, lossy=False, verbous=False):
    # compress file either in a conserving way
    # or in a lossy way
    if verbous:
        vflag = '-v -s'
    else:
        vflag = '-q'
    if lossy:
        subprocess.call(['package/my_nczip', vflag, '-p', file],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT)
    else:
        subprocess.call(['package/my_nczip', vflag, '-1', file],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT)



def compress_date_conserving(ts, directory, var_name, i_debug):
    timer = Timer()
    timer.start('compr')
    file = os.path.join(directory,
                            '{}_{:%Y%m%d}.nc'.format(var_name, ts))
    if os.path.exists(file):
        # compress file
        compress_file(file, lossy=False, verbous=False)
    else:
        print('conserv. compression: file {} does not exist.'.format(file))
    timer.stop('compr')
    output = {'timer':timer}
    return(output)



def find_minmax_val(ts, directory, model_name, var_name, i_debug, var_key=None):
    """
    If one wants to apply lossy (-p) compression with nczip (ncpdq)
    for multiple 
    """
    timer = Timer()
    timer.start('maxmin')
    if i_debug >= debug_level_1: print(ts)
    if var_key is None:
        var_key = nlm[model_name]['vkeys'][var_name]
    file = os.path.join(directory,
                            '{}_{:%Y%m%d}.nc'.format(var_name, ts))
    if os.path.exists(file):
        # store max and min value to obtain global max/min values
        # for suitable compression of single files
        with xr.open_dataset(file) as ds:
            # loop over time to compute max stepwise to save memory
            max_val = -999999999
            min_val =  999999999
            for tind in range(len(ds[var_key].time)):
                if i_debug >= debug_level_4: print(tind)
                max_val = max(max_val, np.nanmax(ds[var_key].isel(time=tind).values))
                min_val = min(min_val, np.nanmin(ds[var_key].isel(time=tind).values))
        if i_debug >= debug_level_2:
            print('memory {} GB available.'.format(
                    psutil.virtual_memory().available/1E9))

        ## stretch max/min slightly to prevent errors due to
        ## numerical precision
        if max_val >= 0: max_val *= 1.001
        else: max_val *= 0.999
        if min_val >= 0: min_val *= 0.999
        else: min_val *= 1.001

        output = {'max_val':max_val, 'min_val':min_val,
                  'timer':timer}
    else:
        output = {'max_val':np.nan, 'min_val':np.nan, 'timer':timer}
    timer.stop('maxmin')
    return(output)



def compress_date_lossy(ts, directory, model_name, var_name,
                        max_val, min_val, i_debug, var_key=None):
    timer = Timer()
    timer.start('compr')
    if var_key is None:
        var_key = nlm[model_name]['vkeys'][var_name]
    file = os.path.join(directory,
                            '{}_{:%Y%m%d}.nc'.format(var_name, ts))
    if i_debug >= debug_level_1: print(ts)
    if i_debug >= debug_level_2:
        print('memory {} GB available.'.format(
                psutil.virtual_memory().available/1E9))

    if os.path.exists(file):
        if i_debug >= debug_level_3: print('start replace values')
        # replace lower-left values with max/min of entire time series
        # this is to make sure that compression is done with same time
        # range for all dates (very important for e.g. TQC!)
        ds = Dataset(file, 'a')
        shape = ds[var_key][:].shape
        if len(shape) == 3:
            old_00 = ds.variables[var_key][0,0,0]
            old_01 = ds.variables[var_key][0,0,1]
            ds.variables[var_key][0,0,0] = max_val
            ds.variables[var_key][0,0,1] = min_val
        elif len(shape) == 4:
            old_00 = ds.variables[var_key][0,0,0,0]
            old_01 = ds.variables[var_key][0,0,0,1]
            ds.variables[var_key][0,0,0,0] = max_val
            ds.variables[var_key][0,0,0,1] = min_val
        else:
            raise NotImplementedError()
        ds.close()

        if i_debug >= debug_level_3: print('compress file')
        # compress file
        compress_file(file, lossy=True)

        if i_debug >= debug_level_3: print('replace back')
        # replace max min value with original value
        ds = Dataset(file, 'a')
        if len(shape) == 3:
            ds.variables[var_key][0,0,0] = old_00
            ds.variables[var_key][0,0,1] = old_01
        elif len(shape) == 4:
            ds.variables[var_key][0,0,0,0] = old_00
            ds.variables[var_key][0,0,0,1] = old_01
        else:
            raise NotImplementedError()
        ds.close()
        if i_debug >= debug_level_3: print('done')
    else:
        print('lossy. compression: file {} does not exist.'.format(file))

    timer.stop('compr')
    output = {'timer':timer}
    return(output)



if __name__ == '__main__':
    var_name = 'U10M' 
    date = datetime(2016,8,1)
    lossy = False
    if not lossy:
        compress_date_conserving(date, directory, var_name)
