#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Download IGRA radio sounding data for specific geographic
                regions
author			Christoph Heim
date created    05.11.2021
date changed    05.11.2021
"""
###############################################################################
import os, argparse#, subprocess, warnings
import numpy as np
import pandas as pd
from importlib import import_module
from datetime import datetime, timedelta
#from pathlib import Path
#from base.nl_global import inp_glob_base_dir
#from package.nl_models import nlm
from package.utilities import Timer
#from base.nl_domains import *
#from package.mp import TimeStepMP
#from package.nc_compression import (compress_date_conserving, find_minmax_val,
#                                    compress_date_lossy)
###############################################################################

igra_stat_path = os.path.join('igra2', 'igra2-station-list.txt')

if __name__ == '__main__':

    i_debug = 2
    
    parser = argparse.ArgumentParser(description = 
                    'Retrieve radio sounding data')
    parser.add_argument('-p', '--time_period', type=str, 
                            default='20150701,20150810')
    #parser.add_argument('-v', '--variables', type=str, 
    #        default='ALT,T,U,V,W,QV,QC,PS,SLHFLX,SSHFLX,TQV,TQI,TQC,U10M,V10M,PP,SWDTOA,SWNDTOA,LWUTOA,SST')
    parser.add_argument('-d', '--domain', type=str, 
                            default='dom_SA_3km_large3')
    parser.add_argument('-o', '--out_base_dir', type=str, 
                            default=None)
    args = parser.parse_args()

    timer = Timer(mode='seconds')

    # compute date range based on user input
    first_date = datetime.strptime(
                    args.time_period.split(',')[0], '%Y%m%d')
    last_date = datetime.strptime(
                    args.time_period.split(',')[1], '%Y%m%d')
    #dates = np.arange(first_date.date(),
    #                      last_date.date()+timedelta(days=1),
    #                      timedelta(days=1)).tolist()

    # get domain based on user input
    nl_domains = import_module('base.nl_domains')
    domain = getattr(nl_domains, args.domain)

    stat = pd.read_csv(igra_stat_path, sep=";")
    space_selection = (
        (stat.LATITUDE >= domain['lat'].start) &
        (stat.LATITUDE <= domain['lat'].stop) &
        (stat.LONGITUDE >= domain['lon'].start) &
        (stat.LONGITUDE <= domain['lon'].stop)
    )
    print(np.sum(space_selection))
    time_selection = (
        (stat.FSTYEAR <= last_date.year) &
        (stat.LSTYEAR >= first_date.year)
    )
    print(np.sum(time_selection))
    full_selection = space_selection & time_selection
    print(np.sum(full_selection))
    stat = stat[full_selection]
    print(stat)
    quit()

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
