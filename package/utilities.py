#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description:    Useful stuff
author:         Christoph Heim
date created:   27.06.2019
date changed:   21.07.2022
usage:          import in other scripts
"""
###############################################################################
import time, glob, os, subprocess, pickle, sys, copy
import numpy as np
import xarray as xr
#import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from datetime import time as dttime
from datetime import datetime
from contextlib import contextmanager
from pathlib import Path
from cdo import Cdo
from dateutil.relativedelta import relativedelta
from package.nl_models import nlm
###############################################################################


###############################################################################
## TIMER CLASS
###############################################################################
class Timer:
    
    TOTAL_CPU_TIME  = 'tot_cpu'
    REAL_TIME       = 'total'
    
    def __init__(self, mode='minutes', parallel=False):
        self.mode = mode
        ## TODO: this is not implemented
        ## idea is to count parallel counted timers as parallel time
        self.parallel = parallel

        self.timings = {self.TOTAL_CPU_TIME:0.}
        self.flags = {self.TOTAL_CPU_TIME:None}

        # start real total computation time timer.
        self.start(self.REAL_TIME)


    def start(self, timer_key):
        """
        Start timer with key timer_key.
        Also start TOTAL_CPU_TIME timer if not already running.
        """
        # start TOTAL_CPU_TIME timer
        if self.flags[self.TOTAL_CPU_TIME] is None:
            self.flags [self.TOTAL_CPU_TIME] = time.time()
        # start timer_key timer
        if timer_key not in self.timings.keys():
            self.timings[timer_key] = 0.
        else:
            if self.flags[timer_key] is not None:
                print('Caution: Timer', timer_key, 'already running')
        self.flags[timer_key] = time.time()

    def stop(self, timer_key):
        """
        Stop timer with key timer_key.
        Also stop TOTAL_CPU_TIME timer if timer_key is the only running task
        """
        if (timer_key not in self.flags.keys()
            or self.flags[timer_key] is None):
            raise ValueError('No time measurement in progress for timer ' +
                            str(timer_key) + '.')

        self.timings[timer_key] += time.time() - self.flags[timer_key]
        self.flags[timer_key] = None

        # Check if any other timer is running. If not, stop TOTAL_CPU_TIME timer
        other_timers_running = False
        for key,flag in self.flags.items():
            if key not in [self.TOTAL_CPU_TIME, self.REAL_TIME]:
                if flag is not None:
                    other_timers_running = True
        if not other_timers_running:
            self.timings[self.TOTAL_CPU_TIME] += (time.time() - 
                                            self.flags[self.TOTAL_CPU_TIME])
            self.flags[self.TOTAL_CPU_TIME] = None

    def merge_timings(self, Timer):
        """
        Merge timings from parallel execution Timer instances into this timer.
        """
        for timer_key in Timer.timings.keys():
            if ( (timer_key in self.timings.keys()) and 
                 (timer_key != self.REAL_TIME) ):
                self.timings[timer_key] += Timer.timings[timer_key]
            else:
                self.timings[timer_key] = Timer.timings[timer_key]

    def print_report(self, short=False):

        timer_key = self.REAL_TIME
        self.timings[timer_key] += time.time() - self.flags[timer_key]
        self.flags[timer_key] = None

        n_decimal_perc = 0
        n_decimal_sec = 1
        n_decimal_min = 2
        cpu_time = max(0.00001,self.timings[self.TOTAL_CPU_TIME])
        real_time = max(0.00001,self.timings[self.REAL_TIME])


        if not short:
            if self.mode == 'minutes':
                print('##########################################################')
                print('Took ' + str(np.round(real_time/60,n_decimal_min))
                      + ' min.')
                print('Detailed process times (cpu time, not real time):')
                for key,value in self.timings.items():
                    if key != self.REAL_TIME:
                        print(key + '\t' + 
                            str(np.round(100*value/cpu_time,n_decimal_perc)) +
                        '\t%\t' + str(np.round(value/60,n_decimal_min)) + ' \tmin')
            elif self.mode == 'seconds':
                print('##########################################################')
                print('Took ' + str(np.round(real_time,n_decimal_sec)) + ' sec.')
                print('Detailed process times (cpu time, not real time):')
                for key,value in self.timings.items():
                    if key != self.REAL_TIME:
                        print('{:15s}'.format(key) + '\t' + 
                            str(np.round(100*value/cpu_time,n_decimal_perc)) +
                        '\t%\t' + str(np.round(value,n_decimal_sec)) + ' \tsec')
            else:
                raise ValueError()
        else:
            print('##########################################################')
            print('Took ' + str(np.round(real_time/60,n_decimal_min))
                  + ' min.')







###############################################################################
## CDO COMMANDS
###############################################################################
def cdo_mergetime(inp_folder, out_folder, var_name):
    """
    Merge all nc files with name $var_name_*.nc in $inp_folder
    and copy result to $out_folder.
    Used for dyamond copies on mistral.
    """
    #inp_files = glob.glob(os.path.join(inp_folder,var_name+'_*'))
    #inp_files.sort()
    #out_file = os.path.join(out_folder,var_name+'.nc')
    #cdo.mergetime(input=inp_files, output=out_file, options='-O')
    inp_files = os.path.join(inp_folder,var_name+'_*')
    out_file = os.path.join(out_folder,var_name+'.nc')
    print(inp_files)
    print(out_file)
    subprocess.call(['cdo', '-O', 'mergetime', inp_files, out_file])







###############################################################################
## FIELD COMPUTATIONS
###############################################################################
## TODO: this is deprecated since now, the Time_Processing class does a better
# job.
#def calc_mean_diurnal_cycle(field_hourly, aggreg_type='MEAN'):
#    """
#    Calculates the mean diurnal cycle for the input field.
#    Removes dimension 'time' and introduces new dimension
#    'diurnal' ranging from 0 to 23.
#    ---------------------------------------------------------------------------
#    INPUT:
#    field_hourly:   xarray DataArray - Input field with hourly timesteps and
#                    dimension 'time'.
#    aggreg_type:    str - How to aggregate the days for one hour.
#    ---------------------------------------------------------------------------
#    OUTPUT:
#    xarray DataArray - Output field with dimension 'time' removed and dimension
#                       'diurnal' created. 
#    ---------------------------------------------------------------------------
#    COMMENTS:
#    """
#    hr_fields = []
#    for hour in range(0,24):
#        this_hr_field = field_hourly.sel(time=dttime(hour))
#        this_hr_field = this_hr_field.assign_coords(diurnal=hour)
#        hr_fields.append(this_hr_field)
#    field_diurn = xr.concat(hr_fields, dim='diurnal')
#
#
#    if aggreg_type == 'MEAN':
#        field_diurn = field_diurn.mean(dim='time')
#    else:
#        raise NotImplementedError()
#
#    return(field_diurn)


def subsel_domain(ds, domain, const_file=None, mod_key=None):
    """
    Subselect latitude longitude domain.
    Input:
      ds        - an xarray Dataset/DataArray object
      domain    - a dict object describing the domain with a
                    lat and a lon slice (for a rectangular domain)
                    or single values (for a point)
    Output:
      DATE - a python datetime object
    """
    # single grid point
    if (not isinstance(domain['lon'], slice) and 
        not isinstance(domain['lat'], slice)):
        # select nearest grid point
        ds = ds.sel(lat=domain['lat'], lon=domain['lon'], method='nearest')
    # 2D domain
    else:
        if 'lon' in ds.dims:
            ds = ds.sel(lon=domain['lon'])
        if 'lat' in ds.dims:
            # revert latitude axis? (the case in IFS raw data)
            try:
                if ds.lat[-1] < ds.lat[0]:
                    lat_slice = slice(domain['lat'].stop, domain['lat'].start)
                else: lat_slice = domain['lat']
            except IndexError:
                lat_slice = domain['lat']
            ds = ds.sel(lat=lat_slice)

    # mask area specified in domain dict ['mask']
    if ('mask' in domain) and (const_file is not None):
        if mod_key is None:
            raise ValueError('Need mod_key for subsel_domain.')
        mask = xr.open_dataset(const_file)[nlm[mod_key]['vkeys'][
                                        domain['mask']['field']]]
        if mod_key in ['COSMO','INT2LM']:
            if 'rlon' in mask.dims:
                if 'lon' in mask.coords:
                    mask = mask.drop(['lon', 'lat'])
                mask = mask.rename({'rlon':'lon', 'rlat':'lat'})
        elif mod_key == 'ERA5':
            mask = mask.rename({'longitude':'lon', 'latitude':'lat'})
            # flip latitude orientation
            if mask.lat[-1] < mask.lat[0]:
                mask = mask.reindex(lat=list(reversed(mask.lat)))
        mask = subsel_domain(mask, domain, 
                            const_file=None, mod_key=None)
        if domain['mask']['transform'] is not None:
            if domain['mask']['transform'] == '1-x':
                mask = 1 - mask
            else:
                raise NotImplementedError()
        mask = mask.where(mask >= domain['mask']['thresh'], 0)
        #if domain['mask']['transform'] == 'mirror':
        #    mask = 1 - mask
        # add time dimension of variable to the mask for comparison
        #if 'time' in ds.dims:
        if 'time' in mask.dims:
            mask = mask.isel(time=0)
        mask = mask.expand_dims({'time':ds.time}, axis=0)
        mask = mask.assign_coords({'time':ds.time.values})
        #mask['time'] = ds.time
        #print(ds.shape)
        #print(mask.shape)
        #print(ds.time)
        #print(mask.time)
        #print(ds.lon)
        #print(mask.lon)
        #quit()
        ## this is necessary because for COSMO_3.3/MPI-ESM1-2-HR, 
        ## lon and or lat are not aligned... don't know why.
        mask = mask.assign_coords({'lon':ds.lon.values})
        mask = mask.assign_coords({'lat':ds.lat.values})
        #mask = mask.interp({'lon':ds.lon})
        ds = ds.where(mask == 0, np.nan)
        #plt.contourf(ds.lon, ds.lat, ds.squeeze())
        #ds.squeeze().plot.contourf()
        #plt.show()
        #quit()

    # mask area outside polygone
    if 'polygone' in domain:
        print(ds)
        quit()
    return(ds)



def select_common_timesteps(array1, array2):
    """
    Select from both arrays only the time step they have in common.
    Input:
      array1,array2 - to xr data arrays containing time
    Output:
      array1,array2 reduced to common time steps.
    """
    if ('time' in array1.dims) and ('time' in array2.dims):
        sel_time = []
        for ts in array1.time.values:
            if ts in array2.time:
                sel_time.append(ts)
        array2 = array2.sel(time=sel_time)
        sel_time = []
        for ts in array2.time.values:
            if ts in array1.time:
                sel_time.append(ts)
        array1 = array1.sel(time=sel_time)
    return((array1, array2))





###############################################################################
## REMAPPING FUNCTIONS
###############################################################################
def write_grid_des_file(domain, file, dx_km, padding=0):
    """
    Writes a file with a grid description that can be used for cdo remap
    """
    rE = 6371
    dx_deg = dx_km / rE / np.pi * 180
    lat0 = domain['lat'].start - padding
    lat1 = domain['lat'].stop + padding
    lon0 = domain['lon'].start - padding
    lon1 = domain['lon'].stop + padding
    xsize = (lon1 - lon0)/dx_deg
    ysize = (lat1 - lat0)/dx_deg
    with open(file, 'w') as f:
        f.write('gridtype    =   lonlat\n')
        f.write('xsize       =   '+str(int(np.ceil(xsize)))+'\n')
        f.write('ysize       =   '+str(int(np.ceil(ysize)))+'\n')
        f.write('xname       =   lon'+'\n')
        f.write('xlongname   =   "longitude"'+'\n')
        f.write('xunits      =   "degrees_east"'+'\n')
        f.write('yname       =   lat'+'\n')
        f.write('ylongname   =   "latitude"'+'\n')
        f.write('yunits      =   "degrees_north"'+'\n')
        f.write('xfirst      =   '+str(lon0)+'\n')
        f.write('xinc        =   '+str(np.round(dx_deg,3))+'\n')
        f.write('yfirst      =   '+str(lat0)+'\n')
        f.write('yinc        =   '+str(np.round(dx_deg,3))+'\n')


def cdo_remap(grid_des_file, inp_file, out_file, method='bil'):
    """
    Run cdo remap command.
    """
    cdo = Cdo()
    #print('remap {}'.format(inp_file))
    if method == 'bil':
        cdo.remapbil(grid_des_file, input=inp_file, output=out_file)
    elif method == 'con':
        cdo.remapcon(grid_des_file, input=inp_file, output=out_file)


def remap_member_for_date(date, mem_key, mem_dict, var_name,
                           inp_base_dir, out_base_dir,
                           grid_des_file, remap_dx):
    """
    Wrapper to construct input and output paths for remapping based on
    date, mem_key, mem_dict, var_name. Then calls cdo_remap().
    """
    inp_file = os.path.join(inp_base_dir, mem_key,
                            mem_dict['case'], 'daily', var_name,
                            '{}_{:%Y%m%d}.nc'.format(var_name, date) )
    out_path = os.path.join(out_base_dir,
                        'remapped_{:g}'.format(remap_dx), mem_key,
                        mem_dict['case'], 'daily', var_name)
    Path(out_path).mkdir(parents=True, exist_ok=True)
    out_file = os.path.join(out_path,
                    '{}_{:%Y%m%d}.nc'.format(var_name, date))
    #print(out_file)
    #quit()
    if os.path.exists(inp_file):
        cdo_remap(grid_des_file, inp_file, out_file)
    else:
        loc = 'package.utilities.remap_member_for_date()'
        print('WARNING: {} file {} not found.'.format(loc, inp_file))





###############################################################################
## IO FUNCTIONS
###############################################################################
def pickle_load(folder, name):
    file = os.path.join(folder, '{}.pkl'.format(name))
    if os.path.exists(file):
        with open(file, 'rb') as f:
            return(pickle.load(f))
    else: return(None)

def pickle_save(obj, folder, name):
    Path(folder).mkdir(parents=True, exist_ok=True)
    file = os.path.join(folder, '{}.pkl'.format(name))
    with open(file, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout



###############################################################################
## FIELD COMPUTATIONS
###############################################################################
def area_weighted_mean_lat_lon(field, dims=['lon','lat']):
    dlat_0D = np.median(np.diff(field.lat))
    dlon_0D = np.median(np.diff(field.lon))
    ## TODO: ugly solution start:
    ## ATTENTION! full_like does not work in some cases.
    ## Xarray bug.
    #dlat = xr.full_like(field, dlat_0D)
    #dlon = xr.full_like(field, dlon_0D)
    dim_keys = ["time", "alt", "rel_alt", "lat", "lon"]
    use_dims = []
    use_coords = {}
    for dim_key in dim_keys:
        if dim_key in field.dims:
            #print(dim_key)
            use_dims.append(dim_key)
            use_coords[dim_key] = field[dim_key]
    dlat = xr.DataArray(
        data=dlat_0D,
        dims=use_dims,
        coords=use_coords)
    dlon = xr.DataArray(
        data=dlon_0D,
        dims=use_dims,
        coords=use_coords)
    ## TODO: ugly solution stop:
    area = dlat * dlon * np.cos(field.lat / 180 * np.pi)
    weighted_mean = ((area * field).mean(dim=dims)/area.mean(
                                                        dim=dims))
    # this is not nice but is a fix for a wrong reformatting of the dataarray
    # after the above equation
    output = field.mean(dim=dims, keep_attrs=True)
    output.values = weighted_mean.values
    return(output)


###############################################################################
## OTHER
###############################################################################
class cd:
    def __init__(self, new_path):
        self.new_path = os.path.expanduser(new_path)

    def __enter__(self):
        self.saved_path = os.getcwd()
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)

def dt64_to_dt(date):
    """
    Converts a numpy datetime64 object to a python datetime object 
    Input:
      date - a np.datetime64 object
    Output:
      DATE - a python datetime object
    source: https://gist.github.com/blaylockbk/1677b446bc741ee2db3e943ab7e4cabd
    """
    #print(type(date))
    #print(type(np.datetime64('1970-01-01T00:00:00')))
    #quit()
    timestamp = ((date - np.datetime64('1970-01-01T00:00:00'))
                 / np.timedelta64(1, 's'))
    return datetime.utcfromtimestamp(timestamp)






if __name__ == '__main__':
    #domain = {'lon'=slice(265,281, 'lat0': -24, 'lat1': -14,
    #       'vert0':1,'vert1':22}
    file = 'test_grid'
    write_grid_file(box, file, dx_km=1)
