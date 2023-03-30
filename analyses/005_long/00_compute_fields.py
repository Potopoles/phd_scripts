#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Compute derived fields and store in nl.ana_base_dir to use in
                different scripts.
author			Christoph Heim
date created    18.02.2020
date changed    22.04.2022
usage           args:
                1st:    number of parallel tasks
"""
###############################################################################
import os, glob, time, warnings
import numpy as np
import xarray as xr
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
#from dateutil.relativedelta import relativedelta
import nl_00 as nl
from package.nl_models import nlm
from package.nl_variables import nlv,dimx,dimy,dimz,dimt
from package.var_pp import compute_variable, var_mapping
from package.utilities import Timer, subsel_domain, dt64_to_dt
from package.mp import TimeStepMP
from package.time_processing import Time_Processing as TP
from package.functions import (
    load_member_var, 
    create_dates_code, 
    time_periods_to_dates
)
from package.nc_compression import (compress_date_conserving, find_minmax_val,
                                    compress_date_lossy)
from package.model_pp import MODEL_PP, MODEL_PP_DONE
from package.var_pp import DERIVE, DIRECT
###############################################################################

def compute_field(date, members):
    out_files = []
    tmp_out_files = []

    domain = nl.domain
    var_name = nl.args.var_name
    mem_key = nl.args.mem_key
    mem_dict = nl.mem_src[nl.args.mem_key]
    sim_key = mem_dict['sim']

    ######## LOAD MODELS
    ##########################################################################
    # skip any date != first date of the month for
    # members with frequency monthly.
    if (mem_dict['freq'] == 'monthly') and (date.day != 1):
        var = None
    else:
        var = load_member_var(var_name, mem_dict['freq'],
                            date, date, mem_dict,
                            nl.var_src_dict,
                            nl.mean_var_src_dict,
                            nl.var_src_dict[var_name]['load'],
                            #nl.src_domain_key,
                            i_debug=nl.i_debug,
                            domain=domain)

    if var is not None:
        if nl.i_debug >= 3:
            print(var.mean())
            #var = var.mean(dim=['alt','time'])
            #print('DONE')
            #import matplotlib.pyplot as plt
            #var.contourf()
            #plt.show()
            #quit()

        # if we want to compute the time average, do averaging
        # already here to save (lots of!) time later
        # because time averaging is done after reloading daily_tmp files
        if nl.time_mode == 'tmean':
            var = TP.run_aggregation_step(var, 
                      { TP.ACTION:TP.RESAMPLE, 
                        TP.FREQUENCY:'D', 
                        TP.OPERATOR:TP.MEAN  })

        # save main variable
        out_base_dir = os.path.join(nl.ana_base_dir, 'native_grid')
        out_path = os.path.join(out_base_dir, sim_key, mem_dict['case'], 
                                nl.domain['key'], mem_dict['freq'], var_name)
        Path(out_path).mkdir(parents=True, exist_ok=True)
        out_file = os.path.join(out_path,
                        '{}_{:%Y%m%d}.nc'.format(var_name, date))
        tmp_out_file = os.path.join(out_path,
                        '{}_{:%Y%m%d}.nc.tmp'.format(var_name, date))

        # link const.nc file to analysis subdirectory
        ana_const_dir = os.path.join(out_base_dir, sim_key, mem_dict['case'], 
                                        nl.domain['key'])
        inp_const_files = glob.glob(os.path.join(nl.inp_base_dir, sim_key, 
                                        mem_dict['case'], 
                                        mem_dict['dom_key'], 'const*.nc'))
        for inp_const_file in inp_const_files:
            try:
                os.symlink(inp_const_file, 
                    os.path.join(ana_const_dir, Path(inp_const_file).name))
            except FileExistsError:
                pass

        # save file to tmp file (necessary because input and output
        # file could be idential if variable is computed directly
        # and not derived).
        #if os.path.exists(out_file):
        #    os.remove(out_file)
        try:
            var.to_netcdf(tmp_out_file)
        # in UM_5 var PP we get duplicate _Fill_Values.
        except ValueError:
            del var.encoding['_FillValue']
            var.to_netcdf(tmp_out_file)
        out_files.append(out_file)
        tmp_out_files.append(tmp_out_file)
            
    return(out_files, tmp_out_files)




def run_computation(ts):
    """
    Organize variable computation for a given date (ts).
    ts has to be called ts because run_for_date is called from TimeStepMP.
    """
    timer = Timer(mode='seconds')
    if nl.i_debug >= 2:
        print('{} {:%Y%m%d}'.format(nl.args.var_name, ts))
    
    # compute field
    timer.start('var')
    members = {}
    out_file, tmp_out_file = compute_field(ts, members)
    timer.stop('var')

    output = {'timer':timer, 'out_file':out_file,
              'tmp_out_file':tmp_out_file}
    return(output)
    

if __name__ == '__main__':

    ###########################################################################
    # PREPARATION STEPS
    timer = Timer(mode='seconds')
    Path(nl.ana_base_dir).mkdir(parents=True, exist_ok=True)
    mem_key = nl.args.mem_key
    mem_dict = nl.mem_src[nl.args.mem_key]
    dates = time_periods_to_dates(nl.time_periods)
    if mem_dict['freq'] == 'daily':
        pass
    elif mem_dict['freq'] == 'monthly':
        dates = [dt for dt in dates if dt.day == 1 ]
    else:
        raise NotImplementedError()
    tsmp = TimeStepMP(dates, njobs=nl.args.n_par, run_async=True)

    ###########################################################################
    # PART OF ANALYSIS SPECIFIC FOR EACH DAY

    # COMPUTE FIELD
    if nl.i_compute:
        print('COMPUTE')
        timer.start('compute')

        fargs = {}
        tsmp.run(run_computation, fargs=fargs, step_args=None)


        # if we want to compute daily files for this variable
        if nl.time_mode == 'daily':
            # replace original files with tmp files
            # (thus rename tmp files to orig file name)
            # has to be done outside of parallel region
            for i in range(len(tsmp.output)):
                tmp_out_files = tsmp.output[i]['tmp_out_file']
                out_files = tsmp.output[i]['out_file']
                for j in range(len(tmp_out_files)):
                    os.rename(tmp_out_files[j], out_files[j])
        # if we want to compute time mean files for this variable
        elif nl.time_mode == 'tmean':
            timer.start('timeaverage')
            print('COMPUTE TIME AVERAGE')
            daily_vars = []
            for i in range(len(tsmp.output)):
                if len(tsmp.output[i]['tmp_out_file']) > 0:
                    ds = xr.open_dataset(tsmp.output[i]['tmp_out_file'][0])
                    daily_vars.append(ds)
                else:
                    print('Day file missing for time average')
            # concatenate all days to one time series
            time_series = xr.concat(daily_vars, dim='time')
            # compute time mean values
            time_series = time_series.mean(dim='time').expand_dims(
                {'time':[time_series.time.values[0]]}, axis=0)
            # make sure that model_pp flag is set
            time_series.attrs[MODEL_PP] = MODEL_PP_DONE
            out_base_dir = os.path.join(nl.ana_base_dir, 'native_grid')
            out_dir = os.path.join(out_base_dir, mem_dict['sim'],
                                    mem_dict['case'], nl.domain['key'], 
                                    'tmean', nl.args.var_name)
            mean_dates_code = create_dates_code(dates)
            Path(out_dir).mkdir(parents=True, exist_ok=True)
            out_file = os.path.join(out_dir,
                            '{}_{}.nc'.format(nl.args.var_name, mean_dates_code))
            time_series.to_netcdf(out_file)
            # delete temporary files in daily dir
            for i in range(len(tsmp.output)):
                if len(tsmp.output[i]['tmp_out_file']) > 0:
                    os.remove(tsmp.output[i]['tmp_out_file'][0])
            timer.stop('timeaverage')
        else: raise ValueError()

        print('DONE. computed variable {}.'.format(nl.args.var_name))
        print('for member: {}'.format(nl.args.mem_key))
        timer.stop('compute')

    if nl.time_mode == 'daily':
        # COMPRESSION
        if nl.i_compress:
            timer.start('compress')

            out_base_dir = os.path.join(nl.ana_base_dir, 'native_grid')

            sim_case_var_path = os.path.join(out_base_dir,
                                mem_dict['sim'],
                                mem_dict['case'],
                                nl.domain['key'],
                                'daily', nl.args.var_name)
            # LOSSY COMPRESSION
            if nl.i_compress == 2:
                if nl.i_debug >= 1:
                    print('Apply LOSSY compression to {}.'.format(mem_key))
                if nl.i_debug >= 2:
                    print('\t\t find min&max')
                # find max and min value for all dates
                fargs = {'directory':sim_case_var_path, 
                         'model_name':mem_dict['mod'],
                         'var_name':nl.args.var_name,
                         'i_debug':nl.i_debug,
                         'var_key':nl.args.var_name}
                tsmp.run(find_minmax_val, fargs=fargs, step_args=None)
                max_val = np.zeros(len(dates))
                min_val = np.zeros(len(dates))
                for i,output in enumerate(tsmp.output):
                    max_val[i] = output['max_val']
                    min_val[i] = output['min_val']
                # ignore nan warnings due tot all-nan grid points
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore', category=RuntimeWarning)
                    max_val = np.nanmax(max_val)
                    min_val = np.nanmin(min_val)
                if nl.i_debug >= 2:
                    print('\t\t\tmax {}'.format(max_val))
                    print('\t\t\tmin {}'.format(min_val))

                # compress
                if nl.i_debug >= 2:
                    print('\t\t compress')
                fargs = {'directory':sim_case_var_path, 
                         'model_name':mem_dict['mod'],
                         'var_name':nl.args.var_name,
                         'max_val':max_val,
                         'min_val':min_val,
                         'i_debug':nl.i_debug,
                         'var_key':nl.args.var_name}
                tsmp.run(compress_date_lossy, fargs=fargs, step_args=None)
            # CONSERVING COMPRESSION
            elif nl.i_compress == 1:
                if nl.i_debug >= 1:
                    print('Apply CONSERVING compression to {}.'.format(mem_key))
                fargs = {'directory':sim_case_var_path, 
                         'var_name':nl.args.var_name,
                         'i_debug':nl.i_debug}
                tsmp.run(compress_date_conserving, fargs=fargs, step_args=None)
            timer.stop('compress')
    timer.print_report()
