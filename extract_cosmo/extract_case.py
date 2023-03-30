#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description:    Extract/Set up/Compress model output of COSMO & others TODO.
author:         Christoph Heim
date created:   24.07.2019
date changed:   18.01.2022
usage:          arguments:
                1st:    n jobs for multiprocessing pool
                2nd:    case dictionary key 
                3rd:    case dictionary simulation name
"""
###############################################################################
import os, glob, subprocess, sys, time, shutil
import numpy as np
import xarray as xr
from datetime import datetime, timedelta
from multiprocessing import Pool
from pathlib import Path
#from cdo import Cdo
from netCDF4 import Dataset
import nl_e_c as nl
from package.utilities import Timer#, cdo_mergetime
from package.nl_models import nlm
from package.mp import TimeStepMP
from package.nc_compression import (compress_date_lossy,
                                    compress_date_conserving,
                                    find_minmax_val)
from package.pp_functions import ncrcat_date_together, run_merge_day
#from Python_CDO_grid.Functions.remap_utilities_cdo import griddesc
###############################################################################


def extract_var_ncrcat(inp_file, out_file, dt, box, options, var_name, res_string,
                        weights_file_path=None):
    
    TM = Timer()
    TM.start('native')

    # skip if already exists
    if (not nl.options['i_overwrite_native']) and os.path.exists(out_file):
        print('file {} already exists.'.format(out_file))
        TM.stop('native')
        return(TM)

    file_code = '{}km_{}_{:%Y%m%d%H%M}'.format(res_string, var_name, dt)
    var_key = nlm[nl.model_name]['vkeys'][var_name]

    bash_command = 'ncrcat -O -v {} {} {}'.format(
                    var_key, inp_file, out_file)
    #print(bash_command)
    #quit()
    process = subprocess.Popen(bash_command.split(),
                                stdout=subprocess.PIPE)
    output, error = process.communicate()
    
    # coarse grain if grid file is given
    if options['i_coarse_grain']:
        if var_name in nl.coarse_grain_var_dict['on']:
            target_grid = options['coarse_grid']
            source_grid = options['fine_grid']

            # rename file to temporary file
            bash_command = 'mv {} {}.tmp'.format(out_file, out_file)
            process = subprocess.Popen(bash_command.split(),
                                        stdout=subprocess.PIPE)
            output, error = process.communicate()

            # coarse grain
            #bash_command = 'cdo remapbil,{} {}.tmp {}'.format(
            #    target_grid, out_file, out_file)
            #bash_command = 'cdo remapcon,{} -setgrid,{} {}.tmp {}'.format(
            #    target_grid, source_grid, out_file, out_file)
            bash_command = 'cdo remap,{},{} {}.tmp {}'.format(
                target_grid, weights_file_path, out_file, out_file)
            process = subprocess.Popen(bash_command.split(),
                                        stdout=subprocess.PIPE)
            output, error = process.communicate()

            # delete temporary file
            bash_command = 'rm {}.tmp'.format(out_file)
            process = subprocess.Popen(bash_command.split(),
                                        stdout=subprocess.PIPE)
        elif var_name in nl.coarse_grain_var_dict['off']:
            pass
        else:
            raise NotImplementedError('var_name {} not in coarse_grain_vars dict'.format(
                                    var_name))
    TM.stop('native')
    return(TM)





if __name__ == '__main__':

    ## PREPARING STEPS
    timer = Timer()
    #cdo = Cdo()

    print('Read user input:')
    print('Using ' + str(nl.args.n_par) + ' task(s).')
    print('Running case {}: simulation {} {} sim name {}'.format(
            nl.args.case_key, nl.model_name, nl.res, nl.out_sim_name))
    print('Variables: {}'.format(nl.var_names))
    print('#############################################')


    ## EXTRACT VARIABLES FROM SIMULATIONS
    print('#####################################################')
    print('copy variables')
    for var_name in nl.var_names:
        print('\t ############## var ' + var_name + ' ##################')
        # has to be reinitialized for each var_name because is cut at the end below
        date_range = np.arange(nl.first_date-timedelta(hours=nl.first_date.hour),
                                nl.last_date+timedelta(days=1),
                               timedelta(days=1)).tolist()
        tsmp = TimeStepMP(date_range, njobs=nl.args.n_par, run_async=True)

        dt_range = np.arange(nl.first_date, nl.last_date + timedelta(days=1,
                            minutes=nl.inc_min[nl.var_dict[var_name]['folder']]),
                            timedelta(minutes=nl.inc_min[
                            nl.var_dict[var_name]['folder']])).tolist()

        inp_dir	= os.path.join(nl.raw_data_dir, nl.inp_tag, nl.inp_sub_folder,
                               nl.var_dict[var_name]['folder'])

        # out_dir = directory for final model output (after mergetime)
        # out_native_dir = directory for output of files in time merge
        # level of raw model output
        out_dir = os.path.join(nl.out_base_dir,
                            '{}_{:g}'.format(nl.model_name, nl.res),
                            nl.out_sim_name)
        out_native_dir = os.path.join(nl.out_base_dir,
                            '{}_{:g}'.format(nl.model_name, nl.res),
                            nl.out_sim_name, 'native', var_name)
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        Path(out_native_dir).mkdir(parents=True, exist_ok=True)

        # weights file
        weights_file_path = os.path.join(out_dir, 'native', 'weights.nc')


        ####### 01.2 COARSE GRAIN PREPARATIONS
        ######################################################################
        if nl.options['i_coarse_grain'] and nl.options['i_compute_native']:
            print('#####################################################')
            #print('coarse grain')
            # Get source grid information
            #print(os.path.join(inp_dir, str(dt_range[0].year),
            #                'lffd{:%Y%m%d%H%M}*.nc'.format(dt_range[0])))
            #quit()
            inp_file_path = glob.glob(os.path.join(inp_dir, str(dt_range[0].year),
                            'lffd{:%Y%m%d%H%M}*.nc'.format(dt_range[0])))[0]
            #ds = xr.open_dataset(inp_file_path)
            #rlon_cent_in = ds["rlon"].values
            #rlat_cent_in = ds["rlat"].values
            #grid_mapping_name = ds["rotated_pole"].grid_mapping_name
            #pole_longitude = ds["rotated_pole"].grid_north_pole_longitude
            #pole_latitude = ds["rotated_pole"].grid_north_pole_latitude
            #ds.close()

            target_grid = nl.options['coarse_grid']
            source_grid = nl.options['fine_grid']
            ## TODO: this can be run to create a new source grid
            ## however, note that rlon and rlat will be called x and y!
            #griddesc(source_grid, gridtype="projection",
            #                 xsize=len(rlon_cent_in), ysize=len(rlat_cent_in),
            #                 xfirst=rlon_cent_in[0], yfirst=rlat_cent_in[0],
            #                 xinc=np.diff(rlon_cent_in).mean(),
            #                 yinc=np.diff(rlat_cent_in).mean(),
            #                 grid_mapping_name="rotated_latitude_longitude",
            #                 grid_north_pole_longitude=pole_longitude,
            #                 grid_north_pole_latitude=pole_latitude)

            ### compute weights
            if not os.path.exists(weights_file_path):
                print('compute weights coarse grain')
                var_key = nlm[nl.model_name]['vkeys'][var_name]
                bash_command = 'cdo gencon,{} -setgrid,{} -selname,{} {} {}'.format(
                    target_grid, source_grid, var_key, inp_file_path, weights_file_path)
                process = subprocess.Popen(bash_command.split(),
                                            stdout=subprocess.PIPE)
                output, error = process.communicate()

        


        ##### 03 NCRCAT VARIABLES FROM OUTPUT FILES ON NATIVE GRID
        ######################################################################
        if nl.options['i_compute_native']:
            print('compute native')
            timer.start('ncrcat')

            # find times and files that should be extracted
            # and prepare arguments for function
            args = []
            for dt in dt_range:
                #print(dt)
                #print(os.path.join(inp_dir,
                #                'lffd{:%Y%m%d%H%M}*.nc'.format(dt)))
                #quit()
                try:
                    inp_file = glob.glob(os.path.join(inp_dir, str(dt.year),
                                    'lffd{:%Y%m%d%H%M}*.nc'.format(dt)))[0]
                    out_file = os.path.join(out_native_dir,
                                var_name+'_{:%Y%m%d%H%M%S}'.format(dt)+'.nc')
                    args.append( (inp_file, out_file, dt, nl.box, nl.options,
                                  var_name, nl.res, weights_file_path) )
                # file not found
                except IndexError:
                    # if file is not part of the last date, throw warning.
                    # we do not expect those of the last date to be present,
                    # except of 00:00, since this is assumed to be the last
                    # date of the simulation.
                    if '{:%Y%m%d}'.format(dt) != '{:%Y%m%d}'.format(date_range[-1]):
                        print('\t\t WARN: no file for var '+
                              '{} and ts {:%Y%m%d-%H:%M}'.format(
                              var_name,dt))
                        print(os.path.join(inp_dir, str(dt.year),
                                        'lffd{:%Y%m%d%H%M}*.nc'.format(dt)))

            # run function serial or parallel
            if nl.args.n_par > 1:
                with Pool(processes=nl.args.n_par) as pool:
                    results = pool.starmap(extract_var_ncrcat, args)
            else:
                results = []
                for arg in args:
                    results.append(extract_var_ncrcat(*arg))
            timer.stop('ncrcat')

        inp_native_dir = out_native_dir
        out_daily_dir = os.path.join(nl.out_base_dir,
                                '{}_{:g}'.format(nl.model_name, nl.res),
                                nl.out_sim_name, 'daily', var_name)
        Path(out_daily_dir).mkdir(parents=True, exist_ok=True)

        if nl.options['i_compute_daily']:
            print('compute daily')

            ########### MERGE TIME STEP FILES TO DAILY FILES AND FIND MAX/MIN
            #####################################################################
            timer.start('merge')
            # merge time step files for each day separately
            fargs = {'inp_native_dir':inp_native_dir, 
                     'out_daily_dir':out_daily_dir,
                     'var_name':var_name,
                     'i_overwrite_daily':nl.options['i_overwrite_daily']}
            tsmp.run(run_merge_day, fargs=fargs, step_args=None)
            timer.stop('merge')

        ############ COMPRESS DATA
        ######################################################################
        compress_mode = 0
        # determine compress mode based on variable
        if var_name in nl.compress_var_dict['2']:
            compress_mode = 2
        elif var_name in nl.compress_var_dict['1']:
            compress_mode = 1
        else:
            raise NotImplementedError(
                'var_name {} not in compress_var_dict'.format(var_name))
        # force lower compress mode if set globally in namelist
        if nl.options['i_compress'] == 1:
            compress_mode = 1
        elif nl.options['i_compress'] == 0:
            compress_mode = 0

        # LOSSY COMPRESSION
        if compress_mode == 2:
            print('Apply LOSSY compression.')
            timer.start('minmax') 
            # find max and min value for all dates
            fargs = {'directory':out_daily_dir, 
                     'model_name':'{}'.format(nl.model_name),
                     'var_name':var_name,
                     'i_debug':nl.i_debug}
            tsmp.run(find_minmax_val, fargs=fargs, step_args=None)
            max_val = np.zeros(len(date_range))
            min_val = np.zeros(len(date_range))
            for i,output in enumerate(tsmp.output):
                max_val[i] = output['max_val']
                min_val[i] = output['min_val']
            max_val = np.nanmax(max_val)
            min_val = np.nanmin(min_val)
            print('\t\t\tmax {}'.format(max_val))
            print('\t\t\tmin {}'.format(min_val))
            timer.stop('minmax') 

            # compress
            timer.start('compress') 
            fargs = {'directory':out_daily_dir, 
                     'model_name':'{}'.format(nl.model_name),
                     'var_name':var_name,
                     'max_val':max_val,
                     'min_val':min_val,
                     'i_debug':nl.i_debug}
            tsmp.run(compress_date_lossy, fargs=fargs, step_args=None)
            timer.stop('compress') 

        # CONSERVING COMPRESSION
        if compress_mode == 1:
            print('Apply CONSERVING compression.')
            fargs = {'directory':out_daily_dir, 
                     'var_name':var_name,
                     'i_debug':nl.i_debug}
            tsmp.run(compress_date_conserving, fargs=fargs, step_args=None)
            for i,output in enumerate(tsmp.output):
                timer.merge_timings(output['timer'])


    timer.print_report()
    print('######################################')
    print('Sucessfully finished case {}: simulation {} {} sim name {}'.format(
            nl.args.case_key, nl.model_name, nl.res, nl.out_sim_name))
    print('######################################')

