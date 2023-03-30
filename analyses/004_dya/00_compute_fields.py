#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Compute derived fields and store in nl.ana_base_dir to use in
                different scripts.
author			Christoph Heim
date created    18.02.2020
date changed    21.01.2021
usage           args:
                1st:    number of parallel tasks
"""
###############################################################################
import os, glob, time, warnings
import numpy as np
import xarray as xr
from pathlib import Path
from datetime import datetime, timedelta
import nl_00 as nl
from package.nl_models import nlm
from package.nl_variables import nlv,dimx,dimy,dimz,dimt
from package.var_pp import compute_variable, var_mapping
from package.utilities import (Timer, remap_member_for_date,
                            write_grid_des_file, subsel_domain)
from package.mp import TimeStepMP
from package.functions import load_member_var
from package.nc_compression import (compress_date_conserving, find_minmax_val,
                                    compress_date_lossy)
from package.model_pp import MODEL_PP, MODEL_PP_DONE
from package.var_pp import DERIVE, DIRECT
###############################################################################

def compute_field(date, members):
    if nl.i_debug >= 1:
        print('{:%Y%m%d}'.format(date))
    out_files = []
    tmp_out_files = []

    # if remapped do not use domain
    if nl.var_cfg[nl.var_name]['remap']: domain = None
    else: domain = nl.domain

    ######## LOAD OBSERVATIONS
    ##########################################################################
    if nl.i_use_obs and nl.var_cfg[nl.var_name]['obs'] is not False:
        obs_key = nl.var_cfg[nl.var_name]['obs']

        var = load_member_var(nl.var_name, date, date,
                            nl.obs_src_dict[obs_key], nl.var_src_dict,
                            nl.var_src_dict[nl.var_name]['load'],
                            i_debug=nl.i_debug,
                            domain=domain)
        #var = subsel_domain(var, domain)

        if var is not None:
            # save main variable
            if nl.var_cfg[nl.var_name]['remap']:
                out_base_dir = os.path.join(nl.ana_base_dir,
                                        'remapped_{:g}'.format(nl.remap_dx))
            else:
                out_base_dir = os.path.join(nl.ana_base_dir, 'native_grid')
            out_path = os.path.join(out_base_dir, obs_key,
                                    nl.obs_src_dict[obs_key]['case'], 'daily',
                                    nl.var_name)
            Path(out_path).mkdir(parents=True, exist_ok=True)
            out_file = os.path.join(out_path,
                            '{}_{:%Y%m%d}.nc'.format(nl.var_name, date))
            tmp_out_file = os.path.join(out_path,
                            '{}_{:%Y%m%d}.nc.tmp'.format(nl.var_name, date))
            # save file to tmp file (necessary because input and output
            # file could be idential if variable is computed directly
            # and not derived).
            #if os.path.exists(out_file):
            #    os.remove(out_file)
            #quit()
            var.to_netcdf(tmp_out_file)
            out_files.append(out_file)
            tmp_out_files.append(tmp_out_file)


    ######## LOAD MODELS
    ##########################################################################
    for mem_key,mem_dict in nl.sim_src_dict.items():
        modres_key =  '{}_{:g}'.format(mem_dict['mod'], mem_dict['res'])
        #pp_var_dependency = 'H'
        var = load_member_var(nl.var_name, date, date, mem_dict,
                            nl.var_src_dict,
                            nl.var_src_dict[nl.var_name]['load'],
                            i_debug=nl.i_debug,
                            domain=domain)
        #if domain is not None: var = subsel_domain(var, domain)

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
                # supress warning
                #with warnings.catch_warnings():
                #    warnings.simplefilter("ignore", category=RuntimeWarning)
                var = var.mean(dim='time')

            # save main variable
            if nl.var_cfg[nl.var_name]['remap']:
                out_base_dir = os.path.join(nl.ana_base_dir,
                                    'remapped_{:g}'.format(nl.remap_dx))
            else:
                out_base_dir = os.path.join(nl.ana_base_dir, 'native_grid')
            out_path = os.path.join(out_base_dir, modres_key,
                                    mem_dict['case'], 'daily', nl.var_name)
            Path(out_path).mkdir(parents=True, exist_ok=True)
            out_file = os.path.join(out_path,
                            '{}_{:%Y%m%d}.nc'.format(nl.var_name, date))
            tmp_out_file = os.path.join(out_path,
                            '{}_{:%Y%m%d}.nc.tmp'.format(nl.var_name, date))

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



def run_remapping_for_date(ts):
    """
    Organize remapping for a given date (ts).
    ts has to be called ts because run_for_date is called from TimeStepMP.
    """
    timer = Timer(mode='seconds')
    timer.start('remap')

    ## REMAP OBSERVATIONS
    if (nl.var_cfg[nl.var_name]['obs'] is not False) and nl.i_use_obs:
        obs_key = nl.var_cfg[nl.var_name]['obs']
        remap_member_for_date(ts, obs_key, nl.obs_src_dict[obs_key],
                              nl.var_name,
                              nl.inp_base_dir,
                              nl.ana_base_dir,
                              grid_des_file, nl.remap_dx)


    # REMAP MODELS
    for mem_key,mem_dict in nl.sim_src_dict.items():
        modres_key =  '{}_{:g}'.format(mem_dict['mod'],
                                       mem_dict['res'])
        if nl.var_src_dict[nl.var_name]['load'] == DERIVE:
            raw_var_names = var_mapping[mem_dict['mod']][nl.var_name]
        elif nl.var_src_dict[nl.var_name]['load'] == DIRECT:
            raw_var_names = [nl.var_name]
        for raw_var_name in raw_var_names:
            #inp_base_dir = nl.var_src[raw_var_name]['src']
            remap_member_for_date(ts, modres_key, mem_dict,
                                  raw_var_name,
                                  nl.inp_base_dir,
                                  #os.path.join(nl.ana_base_dir,'native_grid'),
                                  nl.ana_base_dir,
                                  grid_des_file, nl.remap_dx)
    timer.stop('remap')
    output = {'timer':timer}
    return(output)


def run_computation(ts):
    """
    Organize variable computation for a given date (ts).
    ts has to be called ts because run_for_date is called from TimeStepMP.
    """
    timer = Timer(mode='seconds')
    
    # compute field
    timer.start('var')
    #print('RUN {:%Y%m%d}'.format(ts))
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
    grid_des_file   = os.path.join(nl.ana_base_dir, 
                                'grid_{}km'.format(nl.remap_dx))
    try:
        os.remove(grid_des_file)
    except FileNotFoundError: pass
    write_grid_des_file(nl.domain, grid_des_file, nl.remap_dx,
                    padding=nl.remap_padding)

    ###########################################################################
    # PART OF ANALYSIS SPECIFIC FOR EACH DAY
    
    # REMAPPING
    if nl.i_remap and nl.var_cfg[nl.var_name]['remap']:
        print('REMAP')
        timer.start('remap')
        # remap one day earlier to use the preceeding day
        # in computation of fields (e.g. for diff)
        dates = np.arange(nl.first_date-timedelta(days=1),
                          nl.last_date+timedelta(days=1),
                          timedelta(days=1)).tolist()
        tsmp = TimeStepMP(dates, njobs=nl.njobs, run_async=True)
        fargs = {}
        tsmp.run(run_remapping_for_date, fargs=fargs, step_args=None)
        timer.stop('remap')

    # COMPUTE FIELD
    if nl.i_compute:
        print('COMPUTE')
        timer.start('compute')

        dates = np.arange(nl.first_date, nl.last_date+timedelta(days=1),
                          timedelta(days=1)).tolist()
        tsmp = TimeStepMP(dates, njobs=nl.njobs, run_async=True)
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
            time_series = time_series.mean(dim='time')
            # make sure that model_pp flag is set
            time_series.attrs[MODEL_PP] = MODEL_PP_DONE
            # save time series under 'case'/tmean/'var_name'
            if nl.var_cfg[nl.var_name]['remap']:
                out_base_dir = os.path.join(nl.ana_base_dir,
                                    'remapped_{:g}'.format(nl.remap_dx))
            else:
                out_base_dir = os.path.join(nl.ana_base_dir, 'native_grid')
            # TODO: only runs for 1 member at a time, correct?
            mem_dict = nl.sim_src_dict[list(nl.sim_src_dict.keys())[0]]
            modres_key =  '{}_{:g}'.format(mem_dict['mod'], mem_dict['res'])
            out_path = os.path.join(out_base_dir, modres_key,
                                    mem_dict['case'], 'tmean',
                                    '{}_tmean'.format(nl.var_name))
            Path(out_path).mkdir(parents=True, exist_ok=True)
            out_file = os.path.join(out_path,
                            '{}_tmean_{:%Y%m%d}_{:%Y%m%d}.nc'.format(
                            nl.var_name, nl.first_date, nl.last_date))
            time_series.to_netcdf(out_file)
            # delete temporary files in daily dir
            for i in range(len(tsmp.output)):
                if len(tsmp.output[i]['tmp_out_file']) > 0:
                    os.remove(tsmp.output[i]['tmp_out_file'][0])
            #try:
            #    var.to_netcdf(tmp_out_file)
            ## in UM_5 var PP we get duplicate _Fill_Values.
            #except ValueError:
            #    del var.encoding['_FillValue']
            #    var.to_netcdf(tmp_out_file)
            timer.stop('timeaverage')
        else: raise ValueError()

        print('DONE. computed variable {}.'.format(nl.var_name))
        print('for members: {}'.format(list(nl.sim_src_dict.keys())))
        timer.stop('compute')

    # COMPRESSION
    if nl.i_compress:
        timer.start('compress')
        dates = np.arange(nl.first_date, nl.last_date+timedelta(days=1),
                          timedelta(days=1)).tolist()
        tsmp = TimeStepMP(dates, njobs=nl.njobs, run_async=True)

        if nl.var_cfg[nl.var_name]['remap']:
            out_base_dir = os.path.join(nl.ana_base_dir,
                                'remapped_{:g}'.format(nl.remap_dx))
        else:
            out_base_dir = os.path.join(nl.ana_base_dir, 'native_grid')

        for mem_key,mem_dict in nl.sim_src_dict.items():
            sim_case_var_path = os.path.join(out_base_dir,
                                mem_key, nl.sim_src_dict[mem_key]['case'],
                                'daily', nl.var_name)
            # LOSSY COMPRESSION
            if nl.i_compress == 2:
                if nl.i_debug >= 1:
                    print('Apply LOSSY compression to {}.'.format(mem_key))
                if nl.i_debug >= 2:
                    print('\t\t find min&max')
                # find max and min value for all dates
                fargs = {'directory':sim_case_var_path, 
                         'model_name':mem_dict['mod'],
                         'var_name':nl.var_name,
                         'i_debug':nl.i_debug,
                         'var_key':nl.var_name}
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
                         'var_name':nl.var_name,
                         'max_val':max_val,
                         'min_val':min_val,
                         'i_debug':nl.i_debug,
                         'var_key':nl.var_name}
                tsmp.run(compress_date_lossy, fargs=fargs, step_args=None)
            # CONSERVING COMPRESSION
            elif nl.i_compress == 1:
                if nl.i_debug >= 1:
                    print('Apply CONSERVING compression to {}.'.format(mem_key))
                fargs = {'directory':sim_case_var_path, 
                         'var_name':nl.var_name,
                         'i_debug':nl.i_debug}
                tsmp.run(compress_date_conserving, fargs=fargs, step_args=None)
        timer.stop('compress')
    timer.print_report()
