#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description:    Postprocess model output for usage in analyses. 
author:         Christoph Heim
date created:   24.09.2019
date changed:   04.09.2020
usage:          args:
                1st: number of parallel tasks
"""
###############################################################################
import os, sys, glob, subprocess
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from package.utilities import Timer
from package.domains import *
from package.MP import TimeStepMP
import nl_pp03 as nl
from package.pp_functions import (ncrcat_date_together, run_sellonlat,
                                  delete_15min_time_steps, run_merge_day,
                                  ARPEGE_fix_timeaxis)
from package.nc_compression import (find_minmax_val, compress_date_lossy,
                                    compress_date_conserving)
###############################################################################





    

if __name__ == '__main__':
    ###########################################################################
    ## PREPARING STEPS
    date_range = np.arange(nl.first_date, nl.last_date+timedelta(days=1),
                           timedelta(days=1)).tolist()
    tsmp = TimeStepMP(date_range, njobs=nl.njobs, run_async=True)
    skey = nl.skey
    mkey = skey.split('_')[0]

    timer = Timer()

    ###########################################################################
    ## COMPUTATIONS
    for var_name in nl.var_names:

        inp_native_dir = os.path.join(nl.scra_base_dir, skey,
                                  nl.inp_domain['code'], 'native', var_name)
        inp_daily_dir = os.path.join(nl.scra_base_dir, skey,
                                 nl.inp_domain['code'], 'daily', var_name)
        out_daily_dir = os.path.join(nl.scra_base_dir, skey,
                                 nl.out_domain['code'], 'daily', var_name)

        Path(inp_daily_dir).mkdir(parents=True, exist_ok=True)
        Path(out_daily_dir).mkdir(parents=True, exist_ok=True)

        # skip variables for which this skey has no data
        if len(os.listdir(inp_native_dir)) == 0:
            continue
        else:
            print('\t {}'.format(var_name))

        #######################################################################
        ## ARPEGE FIX TIME AXIS
        if nl.cfg['ARPEGE_fix_timeaxis']:
            timer.start('ARP_fx_ta')
            print('\t \t#### ARPEGE fix time axis')
            fargs = {'inp_native_dir':inp_native_dir, 
                     'var_name':var_name}
            tsmp.run(ARPEGE_fix_timeaxis, fargs=fargs, step_args=None)
            timer.stop('ARP_fx_ta')

        #######################################################################
        ## MERGETIME TO DAILY FILES
        if nl.cfg['merge']:
            timer.start('merge')
            print('\t \t#### merge time')
            fargs = {'inp_native_dir':inp_native_dir, 
                     'out_daily_dir':inp_daily_dir,
                     'var_name':var_name}
                     #'skey':skey}
            tsmp.run(run_merge_day, fargs=fargs, step_args=None)
            timer.stop('merge')

        ############# "ORDER" TIME STEPS
        #######################################################################
        ## make sure date is represented by correct time steps
        ## (taking into account convention that time stemp is at end
        ## of time period considered)
        #if nl.cfg['orderts']:
        #    timer.start('orderts')
        #    for i,date in enumerate(date_range):
        #        #if i < len(date_range) - 1:
        #        ncrcat_date_together(inp_daily_dir, date, var_name)
        #    ## if desired delete last day (assuming that it only contained
        #    ## 00:00 which is now part of second last date)
        #    #if options['i_delete_last_day']:
        #    #    os.remove(os.path.join(out_daily_dir, 
        #    #        '{}_{:%Y%m%d}.nc'.format(var_name, date_range[-1])))
        #    #    date_range = date_range[:-1]
        #    timer.stop('orderts')

        ############ DELETE 15/45 MIN TIME STEPS
        ######################################################################
        if nl.cfg['del15']:
            timer.start('del15')
            print('\t \t#### del 15/45 min files')
            fargs = {'directory':inp_daily_dir, 
                     'var_name':var_name}
            tsmp.run(delete_15min_time_steps, fargs=fargs, step_args=None)
            timer.stop('del15')

        ############ SEL LONLAT BOX
        ######################################################################
        if nl.cfg['selbox']:
            timer.start('selbox')
            print('\t \t#### lonlatbox')
            fargs = {'inp_daily_dir':inp_daily_dir,
                     'out_daily_dir':out_daily_dir,
                     'var_name':var_name,
                     'out_domain':nl.out_domain}
            tsmp.run(run_sellonlat, fargs=fargs, step_args=None)
            timer.stop('selbox')

        ############ COMPRESS DATA
        ######################################################################
        compr_tasks = {'compr_inp_daily':inp_daily_dir,
                       'compr_out_daily':out_daily_dir}
        for task_key,task_dir in compr_tasks.items():
            # LOSSY COMPRESSION
            if nl.cfg[task_key] == 2:
                print('\t\t#### Apply LOSSY compression to {}.'.format(task_key))
                print('\t\t find min&max')
                timer.start('minmax') 
                # find max and min value for all dates
                fargs = {'directory':task_dir, 
                         'model_name':mkey,
                         'var_name':var_name}
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
                print('\t\t compress')
                timer.start('compress') 
                fargs = {'directory':task_dir, 
                         'model_name':mkey,
                         'var_name':var_name,
                         'max_val':max_val,
                         'min_val':min_val}
                tsmp.run(compress_date_lossy, fargs=fargs, step_args=None)
                timer.stop('compress') 
            # CONSERVING COMPRESSION
            elif nl.cfg[task_key] == 1:
                print('\t\t#### Apply CONSERVING compression to {}.'.format(task_key))
                fargs = {'directory':task_dir, 
                         'var_name':var_name}
                tsmp.run(compress_date_conserving, fargs=fargs, step_args=None)

    timer.print_report()
