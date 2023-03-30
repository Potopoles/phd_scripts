#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     
author			Christoph Heim
date created    02.12.2020 
date changed    12.11.2021
usage           no args:
"""
###############################################################################
import os, glob, collections, subprocess
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import nl_preprocess_mod as nl
from package.utilities import Timer, dt64_to_dt
from package.var_pp import DIRECT, DERIVE
from package.functions import load_member_var
from package.model_pp import (compute_P_hybplev, compute_P_plev,
                              compute_ALT_of_plev, interp_PHLEV_from_P)
from package.nc_compression import (compress_date_conserving, find_minmax_val,
                                    compress_date_lossy)
from package.nl_models import nlm
from package.mp import TimeStepMP
###############################################################################


def process_CERES_EBAF(ts, mem_dict, var_name):
    mod_key = mem_dict['mod']
    file_start_date = datetime(ts.year - (ts.year % 5),1,1)
    file_end_date = file_start_date + (relativedelta(years=5) - 
                                        relativedelta(days=1))

    mem_base_dir = os.path.join(nl.inp_base_dir,
                           mem_dict['sim'], mem_dict['case'],
                           mem_dict['dom_key'])

    print(var_name)
    inp_path = os.path.join(nl.inp_base_dir,
                       mem_dict['sim'], 'raw_data',
                'CERES_EBAF-TOA_Ed4.1_Subset_200003-202107.nc')
                #'CERES_EBAF-TOA_Ed4.1_Subset_200608-201912.nc')

    out_dir = os.path.join(nl.inp_base_dir,
                           mem_dict['sim'], mem_dict['case'],
                           mem_dict['dom_key'], 'monthly', var_name)
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    out_file = '{}_{:%Y%m%d}.nc'.format(var_name, ts)
    out_path = os.path.join(out_dir, out_file)
    if ts.day == 1:
        command = 'cdo selname,{} -selyear,{:%Y} -selmonth,{:%m} {} {}'.format(
                                nlm[mem_dict['mod']]['vkeys'][var_name],
                                ts, ts, inp_path, out_path)
        subprocess.run(command, shell=True)

def extract_CMIP6(ts, mem_dict, var_name):
    #print(ts)
    mod_key = mem_dict['mod']
    #file_start_date = datetime(ts.year - (ts.year % year_inc),1,1)
    #file_end_date = file_start_date + (relativedelta(years=year_inc) - 
    #                                    relativedelta(days=1))

    if 'historical' in mem_dict['case']:
        scenario = 'historical'
    elif 'ssp585' in mem_dict['case']:
        scenario = 'ssp585'
    elif 'ssp245' in mem_dict['case']:
        scenario = 'ssp245'
    else:
        raise NotImplementedError()
    #ens_mem = 'r1i1p1f1'
    ens_mem = mem_dict['case'][-8:]
    ## exceptions
    #if (var_name == 'CLDF') and (mod_key == 'EC-Eearth3'):
    #    ens_mem = 'r10i1p1f1' 

    cmip_vkey = nlm[mod_key]['vkeys'][var_name]
    ##  try all possible grid_labels
    ## (see https://github.com/WCRP-CMIP/CMIP6_CVs/blob/master/CMIP6_grid_label.json)
    possible_grid_labels = ['gn', 'gr', 'gr1','cl']
    found_files = False
    for grid_label in possible_grid_labels:
        inp_dir = os.path.join(nl.base_dir_cmip6, scenario, 
                                nl.cmip6_var_src[var_name], cmip_vkey, mod_key,
                                ens_mem, grid_label)
        #print(inp_dir)
        # list all nc files in inp_dir
        file_paths = glob.glob(os.path.join(inp_dir,'*.nc'))
        # find the appropriate file for current ts
        if len(file_paths) > 0:
            found_files = True
            break

    # find the appropriate file for current ts
    if not found_files:
        raise ValueError('No files found for this model and scenario')

    for file_path in file_paths:
        file_start_date = datetime.strptime(
            Path(file_path).name.split('.nc')[0].split(
                    '{}_'.format(grid_label))[-1].split('-')[0],'%Y%m')
        file_end_date = datetime.strptime(
            Path(file_path).name.split('.nc')[0].split(
                    '{}_'.format(grid_label))[-1].split('-')[1],'%Y%m')
        if (file_start_date <= ts) and (file_end_date >= ts):
            break

    # format file name
    inp_file = '{}_{}_{}_{}_{}_{}_{:%Y%m}-{:%Y%m}.nc'.format(
                                cmip_vkey, nl.cmip6_var_src[var_name], mod_key,
                                scenario, ens_mem, grid_label,
                                file_start_date, file_end_date)
    inp_path = os.path.join(inp_dir, inp_file)

    # fourmat out_file path
    out_dir = os.path.join(nl.inp_base_dir,
                           mem_dict['sim'], mem_dict['case'],
                           mem_dict['dom_key'], 'monthly', var_name)
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    out_file = '{}_{:%Y%m%d}.nc'.format(var_name, ts)
    out_path = os.path.join(out_dir, out_file)
    if ts.day == 1:
        #if mod_key in ['ACCESS-CM2', 'ACCESS-ESM1-5']:
        #    command = 'cdo sellonlatbox,-180,180,-90,90 -selyear,{:%Y} -selmonth,{:%m} -selname,{},b {} {}'.format(
        #                        ts, ts, cmip_vkey, inp_path, out_path)
        #else:
        #    #command = 'cdo sellonlatbox,-180,180,-90,90 -selyear,{:%Y} -selmonth,{:%m} {} {}'.format(
        #    #                    ts, ts, inp_path, out_path)
        #subprocess.run(command, shell=True)
        ## add 5 days to ensure that this month is selected for
        ## time stamps in the middle of the month
        command = "ncks -O -d time,'{:%Y-%m-%d}' {} {}".format(
                            ts+timedelta(days=5), inp_path, out_path)
        subprocess.run(command, shell=True)
        command = 'ncks -O --msa -d lon,180.,360. -d lon,0.,179.999999 {} {}'.format(out_path, out_path)
        subprocess.run(command, shell=True)
        command = "ncap2 -O -s 'where(lon >= 180) lon=lon-360' {} {}".format(out_path, out_path)
        subprocess.run(command, shell=True)
        #quit()
    #else:
    #    first_day_month = ts.replace(day = 1)
    #    inp_file = '{}_{:%Y%m%d}.nc'.format(var_name, first_day_month)
    #    inp_path = os.path.join(out_dir, inp_file)
    #    command = 'ln -s {} {}'.format(inp_path, out_path)
    #print(command)
    #quit()

        ### exceptions
        ######################################################################
        ## upper-most level in GFDL-CM4 Amon is missing values
        if (mod_key == 'GFDL-CM4') and (nl.cmip6_var_src[var_name] == nl.amon):
            command = "ncks -O -F -d plev,1,18 {} {}".format(out_path, out_path)
            subprocess.run(command, shell=True)
        ## upper-most two levels in CAMS-CSM1-0 Amon are missing values
        if (mod_key == 'CAMS-CSM1-0') and (nl.cmip6_var_src[var_name] == nl.amon):
            command = "ncks -O -F -d plev,1,17 {} {}".format(out_path, out_path)
            subprocess.run(command, shell=True)


    ### constant file
    ##########################################################################
    # if first ts get resolution that might be needed for constant file
    # comparison
    if ts == nl.first_date:
        ds = xr.open_dataset(inp_path)
        dlon = np.median(np.diff(ds.lon.values))
        dlat = np.median(np.diff(ds.lat.values))
    
    # get resolution
    if ts == nl.first_date:
        const_out_paths = []
        for const_var_name in ['sftlf', 'orog']:
            const_out_dir = os.path.join(nl.inp_base_dir,
                                   mem_dict['sim'], mem_dict['case'],
                                   mem_dict['dom_key'])
            #const_out_file_search = glob.glob(os.path.join(const_out_dir, 'const_*.nc'))
            #const_out_file_search = glob.glob(os.path.join(const_out_dir, '{}_*.nc'.format(const_var_name)))

            const_inp_dir = os.path.join(nl.base_dir_cmip6, '*', 
                                        'fx', const_var_name, mod_key,
                                        '*', grid_label)
            const_inp_file = '{}_{}_{}_{}_{}_{}.nc'.format(
                                        const_var_name, 'fx', mod_key,
                                        '*', '*', grid_label)
            const_inp_file_search = glob.glob(os.path.join(const_inp_dir, const_inp_file))
            #print(os.path.join(const_inp_dir, const_inp_file))
            #print(const_inp_file_search)
            if len(const_inp_file_search) == 0:
                raise ValueError('No const file found for this model')
                #pass
            const_inp_path = None
            # look in all scenarios and try to fined constant file and make sure
            # resolution is the same as for model output
            for path in const_inp_file_search:

                # compare resolution
                ds = xr.open_dataset(inp_path)
                const_dlon = np.median(np.diff(ds.lon.values))
                const_dlat = np.median(np.diff(ds.lat.values))
                if (const_dlat == dlat) and (const_dlon == dlon):
                    const_inp_path = path
                    print('take const from scenario: {}'.format(path))
                    break
            #quit()

            if const_inp_path is None:
                print('Const file does not exist for this model.')
                print(const_inp_file_search)
                quit()

            #if ( (len(const_out_file_search) == 0) and 
            #    (const_inp_path is not None) ):
            if const_inp_path is not None:

                #const_out_file = 'const_{:4.3f}.nc'.format(
                resolution = '{:4.3f}'.format(np.median(np.diff(
                                        xr.open_dataset(const_inp_path).lon)))
                const_out_file = '{}_{}.nc'.format(const_var_name, resolution)
                const_out_path = os.path.join(const_out_dir, const_out_file)

                #print(const_inp_path)
                #print(const_out_path)
                print('done')
                if const_var_name == 'sftlf':
                    command = 'cdo sellonlatbox,-180,180,-90,90 -divc,100 -selname,{} {} {}'.format(
                                        const_var_name, const_inp_path, const_out_path)
                elif const_var_name == 'orog':
                    command = 'cdo sellonlatbox,-180,180,-90,90 -selname,{} {} {}'.format(
                                        const_var_name, const_inp_path, const_out_path)
                else:
                    raise NotImplementedError()
                subprocess.run(command, shell=True)
                const_out_paths.append(const_out_path)
        command = 'cdo -O merge '
        for const_out_path in const_out_paths:
            command += '{} '.format(const_out_path)
        resolution = Path(const_out_paths[0]).name.split('_')[1].split('.nc')[0]
        command += os.path.join(Path(const_out_paths[0]).parent, 'const_{}.nc'.format(resolution))
        #print(command)
        #quit()
        subprocess.run(command, shell=True)


def _call_compute_P_plev(ts, mem_dict, mem_inp_dir):
    if (mem_dict['freq'] == 'monthly') and (ts.day != 1):
        return()
    date = ts
    T = load_member_var(
        'T', mem_dict['freq'], 
        date, date, mem_dict,
        nl.var_src_dict, 
        nl.mean_var_src_dict,
        DIRECT,
        i_debug=nl.i_debug, supress_model_pp=True)

    # compute P
    P = compute_P_plev(mem_dict, T)

    # store P in input directory
    var_name = 'P'
    path = os.path.join(mem_inp_dir, var_name)
    Path(path).mkdir(parents=True, exist_ok=True)
    file_name = os.path.join(path, '{}_{:%Y%m%d}.nc'.format(var_name, date))
    P.to_netcdf(file_name, unlimited_dims=['time'])


def _call_compute_P_hybplev(ts, mem_dict, mem_inp_dir):
    date = ts
    # load PS and T to compute P from hybrid p levels
    # (T is only used for information about vertical coordinate)
    PS = load_member_var('PS', date, date, mem_dict,
                nl.var_src_dict, DIRECT,
                i_debug=nl.i_debug, supress_model_pp=True)
    T = load_member_var('T', date, date, mem_dict,
                        nl.var_src_dict, DIRECT,
                        i_debug=nl.i_debug, supress_model_pp=True)

    if (PS is None) or (T is None):
        print('Skip computation of because of missing fields')
        return()

    # compute P
    P = compute_P_hybplev(mem_dict, PS, T)

    # store P in input directory
    var_name = 'P'
    path = os.path.join(mem_inp_dir, var_name)
    Path(path).mkdir(parents=True, exist_ok=True)
    file_name = os.path.join(path, '{}_{:%Y%m%d}.nc'.format(var_name, date))
    P.to_netcdf(file_name, unlimited_dims=['time'])


def _call_integrate_ALT(ts, mem_dict, mem_inp_dir):
    date = ts
    # load P, PS, QV and T to integrate geopotential
    PS = load_member_var('PS', date, date, mem_dict,
                nl.var_src_dict, DIRECT,
                i_debug=nl.i_debug, supress_model_pp=True)
    P = load_member_var('P', date, date, mem_dict,
                nl.var_src_dict, DIRECT,
                i_debug=nl.i_debug, supress_model_pp=True)
    QV = load_member_var('QV', date, date, mem_dict,
                nl.var_src_dict, DIRECT,
                i_debug=nl.i_debug, supress_model_pp=True)
    T = load_member_var('T', date, date, mem_dict,
                nl.var_src_dict, DIRECT,
                i_debug=nl.i_debug, supress_model_pp=True)
    HSURF = load_member_var('HSURF', date, date, mem_dict,
                nl.var_src_dict, DIRECT,
                i_debug=nl.i_debug, supress_model_pp=True)

    if (P is None) or (PS is None) or (QV is None) or (T is None):
        print('Skip computation of because of missing fields')
        return()

    # compute PHLEV (used for integration of geopotential)
    PHLEV = interp_PHLEV_from_P(mem_dict, PS, P)

    # integrate geopotential and compute ALT
    ALT = compute_ALT_of_plev(mem_dict, P, PHLEV, T, QV,
                            HSURF=HSURF, i_debug=nl.i_debug)

    # store ALT in input directory
    var_name = 'ALT'
    path = os.path.join(mem_inp_dir, var_name)
    Path(path).mkdir(parents=True, exist_ok=True)
    file_name = os.path.join(path, '{}_{:%Y%m%d}.nc'.format(var_name, date))
    ALT.to_netcdf(file_name, unlimited_dims=['time'])




if __name__ == '__main__':
    timer = Timer(mode='seconds')

    ### PREPARATION STEPS
    ###########################################################################
    # directory where input fields for this member are stored
    mem_dict = nl.mem_dict

    # directory where daily input variables are stored for this member
    # and case
    mem_inp_dir = os.path.join(nl.inp_base_dir,
                           mem_dict['sim'], mem_dict['case'],
                           mem_dict['dom_key'], mem_dict['freq'])

    # dates to compute
    dates = np.arange(nl.first_date, nl.last_date+timedelta(days=1),
                      timedelta(days=1)).tolist()
    # months to compute
    months = [date for date in dates if date.day == 1 ]

    mod_key = mem_dict['mod']
    tsmp = TimeStepMP(dates, njobs=nl.args.n_par, run_async=True)

    ### COMPUTE PRESSURE AND ALTITUDE FOR MODEL OUTPUT NOT GIVEN AT ALTITUDE
    ### LEVELS
    ###########################################################################
    timer.start('compute')
    if nl.i_compute:

        if nl.mem_dict['mod'] in nl.models_cmip6:
            if nl.var_name == 'P':
                fargs = {'mem_dict':mem_dict, 'mem_inp_dir':mem_inp_dir}
                tsmp.run(_call_compute_P_plev, fargs)
            else:
                fargs = {'mem_dict':mem_dict, 'var_name':nl.var_name}
                tsmp.run(extract_CMIP6, fargs)
        else:
            if 'P' == nl.var_name:
                #if mod_key in ['ERA5', 'IFS', 'ARPEGE-NH']:
                if mod_key in ['IFS', 'ARPEGE-NH']:
                    fargs = {'mem_dict':mem_dict, 'mem_inp_dir':mem_inp_dir}
                    tsmp.run(_call_compute_P_hybplev, fargs)

                #elif mod_key in ['FV3']:
                elif mod_key in ['ERA5', 'FV3']:
                    fargs = {'mem_dict':mem_dict, 'mem_inp_dir':mem_inp_dir}
                    tsmp.run(_call_compute_P_plev, fargs)

            if 'ALT' == nl.var_name:
                fargs = {'mem_dict':mem_dict, 'mem_inp_dir':mem_inp_dir}
                tsmp.run(_call_integrate_ALT, fargs)

            if (nl.mem_key == 'CERES_EBAF'):
                fargs = {'mem_dict':mem_dict, 'var_name':nl.var_name}
                tsmp.run(process_CERES_EBAF, fargs)

    timer.stop('compute')

    ### APPLY LOSSY COMPRESSION
    ###########################################################################
    timer.start('compress')
    print('compress {}'.format(nl.var_name))
    sim_case_var_path = os.path.join(mem_inp_dir, nl.var_name)
    # LOSSY COMPRESSION
    if nl.i_compress == 2:
        if nl.i_debug >= 1:
            print('Apply LOSSY compression to {}.'.format(mem_dict['sim']))
        if nl.i_debug >= 2:
            print('\t\t find min&max')
        # find max and min value for all dates
        fargs = {'directory':sim_case_var_path, 
                 'model_name':mem_dict['mod'],
                 'var_name':nl.var_name,
                 'i_debug':nl.i_debug}#,
                 #'var_key':nl.var_name}
        tsmp.run(find_minmax_val, fargs=fargs, step_args=None)
        max_val = np.zeros(len(dates))
        min_val = np.zeros(len(dates))
        for i,output in enumerate(tsmp.output):
            max_val[i] = output['max_val']
            min_val[i] = output['min_val']
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
                 'i_debug':nl.i_debug}#,
                 #'var_key':nl.var_name}
        tsmp.run(compress_date_lossy, fargs=fargs, step_args=None)
    # CONSERVING COMPRESSION
    elif nl.i_compress == 1:
        if nl.i_debug >= 1:
            print('Apply CONSERVING compression to {}.'.format(mem_dict['sim']))
        fargs = {'directory':sim_case_var_path, 
                 'var_name':nl.var_name,
                 'i_debug':nl.i_debug}
        tsmp.run(compress_date_conserving, fargs=fargs, step_args=None)
    timer.stop('compress')



        
    timer.print_report()

