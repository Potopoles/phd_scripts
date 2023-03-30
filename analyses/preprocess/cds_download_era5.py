#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Download ERA5 data from cds store and format for analysis
author			Christoph Heim
date created    01.12.2020
date changed    01.09.2021
args:
parser.add_argument('-p', '--time_period', type=str)
parser.add_argument('-v', '--variables', type=str)
parser.add_argument('-d', '--domain', type=str)
"""
###############################################################################
import os, cdsapi, argparse, subprocess, warnings
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from base.nl_global import inp_glob_base_dir
from package.nl_models import nlm
from package.utilities import Timer
from base.nl_domains import *
from package.mp import TimeStepMP
from package.nc_compression import (compress_date_conserving, find_minmax_val,
                                    compress_date_lossy)
###############################################################################


def process_after_download(date, tmp_files, out_file):
    for tmp_file in tmp_files:
        # make time a record dimension
        command_list = ["ncks", "-O", "--mk_rec_dmn", "time"]
        command_list.append(tmp_file)
        command_list.append(tmp_file)
        subprocess.call(command_list)

        # uncompress (because of different scale factors and offsets)
        command_list = ["ncpdq", "-U", "-O"]
        command_list.append(tmp_file)
        command_list.append(tmp_file)
        subprocess.call(command_list)

    # concatenate file such that the date contains values
    # from 00:15 until 00:00 next day (timestamp is valid backwards)
    command_list = ["ncrcat", "-O", "-d",
                   r'"time,{:%Y-%m-%d %H:%M:%S},{:%Y-%m-%d}"'.format(
                   date+timedelta(minutes=15), date+timedelta(days=1))]
    command_list.append(tmp_files[0][:-1]+'*')
    command_list.append(out_file)
    command_str = ""
    for cmd in command_list:
        command_str += cmd
        command_str += " "
    subprocess.call(command_str, shell=True)
    for tmp_file in tmp_files:
        os.remove(tmp_file)


def cds_request_mlev_for_date(date, var_name_era5, out_file, domain):
    raise NotImplementedError()
    param_numbers = {
        #'z':'129', #this would be geopotential of model levels. does not work.
        'z':'129.128', #geopotential of surface
        'sp':'134', 
        't':'130',
        'u':'131',
        'v':'132',
        'w':'135',
        'q':'133',
        'clwc':'246',
    }
    param = param_numbers[var_name_era5]
    # for HSURF and PS take levtype 'sfc' instead of 'ml'
    levtype = 'ml'
    if param in ['129.128','134']:
        levtype = 'sfc'
    levelist=''.join([str(el)+'/' for el in np.arange(80,138)])[:-1]

    c = cdsapi.Client()
    c.retrieve('reanalysis-era5-complete', {
        #'class':'ea',
        'date':'{}/to/{}'.format(date.date(), (date+timedelta(days=1)).date()),
        'time':'00/to/23/by/3',
        'levelist':levelist,
        'levtype':levtype,
        'param':param,
        'stream':'oper',
        'type':'an',
        'area':'{}/{}/{}/{}'.format(
                int(domain['lat'].stop),
                int(domain['lon'].start),
                int(domain['lat'].start),
                int(domain['lon'].stop)),
        'grid':'0.5/0.5', # native would be 0.28125
        'format':'netcdf'
    }, out_file+'.tmp')

    process_after_download(date, out_file)

def cds_request_plev_for_date(date, var_name_era5, out_file, domain):
    c = cdsapi.Client()

    # download this and next date first time step
    dates = [date.date(), (date+timedelta(days=1)).date()]
    times = [['03:00','06:00','09:00','12:00','15:00','18:00','21:00'],
             ['00:00']]
    tmp_files = ['{}.tmp{}'.format(out_file, 0),
                 '{}.tmp{}'.format(out_file, 1)]
    for daydate,daytimes,tmp_file in zip(dates,times,tmp_files): 
        c.retrieve('reanalysis-era5-pressure-levels', {
            'product_type':'reanalysis',
            'variable':var_name_era5,
            'pressure_level':['1000', '975', '950', '925',
                               '900', '875', '850', '825',
                               '800', '775', '750',
                               '700', '650', 
                               '600', '550', 
                               '500', '450', 
                               '400', '350',
                               '300', '250', '225',
                               '200', '175', '150', '125',
                               '100',  '70',  '50'],
            'year':str(daydate.year),
            'month':str(daydate.month),
            'day':str(daydate.day),
            'area':[str(domain['lat'].stop),
                    str(domain['lon'].start),
                    str(domain['lat'].start),
                    str(domain['lon'].stop)],
            'time':daytimes,
            'format':'netcdf'
        }, tmp_file)

    process_after_download(date, tmp_files, out_file)



def cds_request_single_lev_for_date(date, var_name_era5, out_file, domain):
    c = cdsapi.Client()
    # download this and next date first time step
    dates = [date.date(), (date+timedelta(days=1)).date()]
    times = [[        '01:00','02:00','03:00','04:00','05:00',
              '06:00','07:00','08:00','09:00','10:00','11:00',
              '12:00','13:00','14:00','15:00','16:00','17:00',
              '18:00','19:00','20:00','21:00','22:00','23:00'],
             ['00:00']]
    tmp_files = ['{}.tmp{}'.format(out_file, 0),
                 '{}.tmp{}'.format(out_file, 1)]
    for daydate,daytimes,tmp_file in zip(dates,times,tmp_files): 
        c.retrieve('reanalysis-era5-single-levels', {
            'product_type':'reanalysis',
            'variable':var_name_era5,
            'year':str(daydate.year),
            'month':str(daydate.month),
            'day':str(daydate.day),
            'area':[str(domain['lat'].stop),
                    str(domain['lon'].start),
                    str(domain['lat'].start),
                    str(domain['lon'].stop)],
            'time':daytimes,
            'format':'netcdf'
        }, tmp_file)

    process_after_download(date, tmp_files, out_file)


var_f_map = {
    ## for download on model level
    ## takes ages because data comes from tape.
    ## unless you need very high vertical resolution, use
    ## data from plev as given below.
    #'T':cds_request_mlev_for_date,
    #'U':cds_request_mlev_for_date,
    #'V':cds_request_mlev_for_date,
    #'W':cds_request_mlev_for_date,
    #'QV':cds_request_mlev_for_date,
    #'QC':cds_request_mlev_for_date,

    'ALT':cds_request_plev_for_date,
    'T':cds_request_plev_for_date,
    'U':cds_request_plev_for_date,
    'V':cds_request_plev_for_date,
    'W':cds_request_plev_for_date,
    'QV':cds_request_plev_for_date,
    'QC':cds_request_plev_for_date,
    'QI':cds_request_plev_for_date,
    'QR':cds_request_plev_for_date,
    'QS':cds_request_plev_for_date,
    'CLDF':cds_request_plev_for_date,


    'PP':cds_request_single_lev_for_date,
    'U10M':cds_request_single_lev_for_date,
    'V10M':cds_request_single_lev_for_date,
    'T2M':cds_request_single_lev_for_date,
    'TD2M':cds_request_single_lev_for_date,
    'CLCM':cds_request_single_lev_for_date,
    'CLCL':cds_request_single_lev_for_date,
    'CLCH':cds_request_single_lev_for_date,
    'CLCT':cds_request_single_lev_for_date,
    'SWDTOA':cds_request_single_lev_for_date,
    'SWNDTOA':cds_request_single_lev_for_date,
    'CSWNDTOA':cds_request_single_lev_for_date,
    'LWUTOA':cds_request_single_lev_for_date,
    'SWNDSFC':cds_request_single_lev_for_date,
    'CSWNDSFC':cds_request_single_lev_for_date,
    'LWNDSFC':cds_request_single_lev_for_date,
    'SLHFLX':cds_request_single_lev_for_date,
    'SSHFLX':cds_request_single_lev_for_date,
    'TQC':cds_request_single_lev_for_date,
    'TQI':cds_request_single_lev_for_date,
    'TQV':cds_request_single_lev_for_date,
    'PS':cds_request_single_lev_for_date,
    'PMSL':cds_request_single_lev_for_date,
    'SST':cds_request_single_lev_for_date,
    'TSURF':cds_request_single_lev_for_date,

    'HSURF':cds_request_single_lev_for_date,
    'FRLAND':cds_request_single_lev_for_date,

}

if __name__ == '__main__':

    case_key = 'plev'
    #case_key = 'mlev'

    # compression
    n_par_compress = 12
    i_debug = 2
    
    parser = argparse.ArgumentParser(description = 
                    'Retrieve ERA5 data on pressure levels')
    parser.add_argument('-p', '--time_period', type=str, 
                            default='20060801,20101231')
    parser.add_argument('-v', '--variables', type=str, 
            default='ALT,T,U,V,W,QV,QC,QI,PS,SLHFLX,SSHFLX,TQV,TQI,TQC,U10M,V10M,PP,SWDTOA,SWNDTOA,LWUTOA,SST,T2M,TD2M')
    parser.add_argument('-d', '--domain', type=str, 
                            default='dom_ERA5')
    parser.add_argument('-o', '--out_base_dir', type=str, 
                            default=None)
    parser.add_argument('-l', '--i_download', type=int, 
                            default=1)
    parser.add_argument('-c', '--i_compress_lossy', type=int, 
                            default=0)
    args = parser.parse_args()

    timer = Timer(mode='seconds')

    # compute date range based on user input
    first_date = datetime.strptime(
                    args.time_period.split(',')[0], '%Y%m%d')
    last_date = datetime.strptime(
                    args.time_period.split(',')[1], '%Y%m%d')
    dates = np.arange(first_date.date(),
                          last_date.date()+timedelta(days=1),
                          timedelta(days=1)).tolist()

    # get variable names from user input
    var_names = args.variables.split(',')

    # get domain based on user input
    if args.domain == 'dom_ERA5':
        domain = dom_ERA5
    elif args.domain == 'dom_SEA_Sc':
        domain = dom_SEA_Sc
    elif args.domain == 'dom_ERA5_COSMO_nesting':
        domain = dom_ERA5_COSMO_nesting
    elif args.domain == 'dom_ERA5_gulf':
        domain = dom_ERA5_gulf
    # domain must have 0.5° increment (see grid in mlev function)
    else:
        raise NotImplementedError

    timer.start('download')
    for date in dates:
        for var_name in var_names:
            print('{}: {}'.format(date, var_name))
            # if no default output directory is given, choose
            # the location assumed by my scripts..
            if args.out_base_dir is None:
                out_dir = os.path.join(inp_glob_base_dir, 'ERA5_31',
                                case_key, domain['key'], 'daily', var_name)
            else:
                out_dir = os.path.join(args.out_base_dir, var_name)

            Path(out_dir).mkdir(parents=True, exist_ok=True)
            out_path = os.path.join(out_dir, 
                            '{}_{:%Y%m%d}.nc'.format(var_name, date))

            # get var_name for ERA5 data set
            var_name_era5 = nlm['ERA5_download']['vkeys'][var_name]

            if args.i_download:
                # run donwload
                var_f_map[var_name](date, var_name_era5, out_path, domain)

                # conserving compression (do always, does not harm) 
                print('conserving compression')
                compress_date_conserving(date, out_dir, var_name, i_debug)
    timer.stop('download')

    # LOSSY COMPRESSION (only for entire time series)
    if args.i_compress_lossy:
        timer.start('lossy_comp')
        print('LOSSY COMPRESSION')
        tsmp = TimeStepMP(dates, njobs=n_par_compress, run_async=True)
        for var_name in var_names:
            if args.out_base_dir is None:
                out_dir = os.path.join(inp_glob_base_dir, 'ERA5_31',
                                case_key, domain['key'], 'daily', var_name)
            else:
                out_dir = os.path.join(args.out_base_dir, var_name)

            # LOSSY COMPRESSION
            # find max and min value for all dates
            fargs = {'directory':out_dir, 
                     'model_name':'ERA5',
                     'var_name':var_name,
                     'i_debug':i_debug}
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

            print('\t\t\tmax {}'.format(max_val))
            print('\t\t\tmin {}'.format(min_val))

            fargs = {'directory':out_dir, 
                     'model_name':'ERA5',
                     'var_name':var_name,
                     'max_val':max_val,
                     'min_val':min_val,
                     'i_debug':i_debug}
            tsmp.run(compress_date_lossy, fargs=fargs, step_args=None)
        timer.stop('lossy_comp')
        print('LOSSY COMPRESSION DONE')
    timer.print_report()
