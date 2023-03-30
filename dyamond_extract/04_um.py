#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description:    Extract lat-lon box of data from model UM.
author:         Christoph Heim
date created:   05.07.2019
date changed:   04.09.2019
usage:          arguments:
                1st:    n jobs for multiprocessing pool
python:         3.5.2
"""
###############################################################################
import os, glob, subprocess, sys, time, shutil
import numpy as np
from datetime import datetime, timedelta
from multiprocessing import Pool
from pathlib import Path
from cdo import Cdo
from package.utilities import Timer, cdo_mergetime
from namelist import domain, padding
from functions import paste_dir_names
###############################################################################

def sellatlon_UM(inp_file, out_file, dt, box, options, var_name, res):
    
    TM = Timer()
    file_code = '{}km_{}_{:%Y%m%d}'.format(res, var_name, dt)
    
    if os.path.exists(out_file) and not options['recompute']:
        TM.start('cdo')
        print('\t\t'+file_code+' already computed')
        TM.stop('cdo')
    else:
        TM.start('cdo')
        print('\t\t'+file_code)

        ofile = cdo.sellonlatbox(
                    box['lon'].start, box['lon'].stop,
                    box['lat'].start, box['lat'].stop,
                    input=('-sellevidx,'+str(box['vert0'])+'/'+
                           str(box['vert1'])+' '+inp_file),
                    output=out_file)
        TM.stop('cdo')

    return(TM)


if __name__ == '__main__':

    # GENERAL SETTINGS
    ###########################################################################
    # input and output directories
    raw_data_dir = os.path.join('/work','ka1081','DYAMOND')
    out_base_dir = os.path.join('/work','ka1081','2019_06_Hackathon_Mainz',
                                'christoph_heim','newdata')

    # box to subselect
    box = domain
    #box.update({'vert0':1,'vert1':21}) #3km top
    box.update({'vert0':1,'vert1':30}) #6km top
    box['lon'] = slice(box['lon'].start - padding, box['lon'].stop + padding)
    box['lat'] = slice(box['lat'].start - padding, box['lat'].stop + padding)

    # name of model 
    model_name = 'UM'

    # variables to extract
    var_names = ['QV', 'QC', 'T', 'W',
                 'U10M', 'V10M', 'T2M', 'LWUTOA', 'SWDSFC',
                 'SLHFLX', 'SSHFLX', 'TQC', 'PP']
    
    # model resolutions [km] of simulations
    ress = [5]
    
    # date range
    first_date = datetime(2016,8,11)
    last_date = datetime(2016,9,8)

    # options for computation
    options = {}
    options['recompute']        = 0
    options['rm_tmp_folder']    = 0
    ###########################################################################


    # UM SPECIFIC SETTINGS
    ###########################################################################
    var_dict = {
        'QV'    :{'file':'hus',}, 
        'QC'    :{'file':'clw',}, 
        'T'     :{'file':'ta',}, 
        'W'     :{'file':'wa',}, 

        'U10M'  :{'file':'uas',}, 
        'V10M'  :{'file':'vas',}, 
        'T2M'   :{'file':'tas',}, 
        'LWUTOA':{'file':'rlut',}, 
        'SWDSFC':{'file':'rsds',}, 
        'SLHFLX':{'file':'hfls',}, 
        'SSHFLX':{'file':'hfss',}, 
        'TQC'   :{'file':'clwvi',}, 
        'PP'    :{'file':'pr',}, 
    }
    ###########################################################################

    ## PREPARING STEPS
    TM = Timer()

    dt_range = np.arange(first_date, last_date + timedelta(days=1),
                        timedelta(days=1)).tolist()

    cdo = Cdo()

    if len(sys.argv) > 1:
        n_tasks = int(sys.argv[1])
    else:
        n_tasks = 1
    print('Using ' + str(n_tasks) + ' taks.')

    ## EXTRACT VARIABLES FROM SIMULATIONS
    # args used as input to parallel executed function
    args = []
    for var_name in var_names:
        #var_name = 'T'
        print('############## var ' + var_name + ' ##################')
        for res in ress:
            print('############## res ' + str(res) + ' ##################')
            #res = 4

            sim_name = model_name + '-' + str(res) + 'km'
            inp_dir	= os.path.join(raw_data_dir, sim_name)

            # out_dir = directory for final model output (after mergetime)
            # out_tmp_dir = directory for output of files in time merge
            # level of raw model output
            out_dir, out_tmp_dir = paste_dir_names(out_base_dir,
                                                   model_name, res, domain)
            Path(out_dir).mkdir(parents=True, exist_ok=True)
            # remove temporary fils if desired
            if options['rm_tmp_folder'] and os.path.exists(out_tmp_dir):
                shutil.rmtree(out_tmp_dir)
            Path(out_tmp_dir).mkdir(parents=True, exist_ok=True)

            # find times and files that should be extracted
            # and prepare arguments for function
            for dt in dt_range:
                print(dt)
                inp_file = glob.glob(os.path.join(inp_dir,
                                            var_dict[var_name]['file'],
                                            '*{:%Y%m%d}*.nc'.format(dt)))[0]
                out_file = os.path.join(out_tmp_dir,
                            var_name+'_{:%Y%m%d}'.format(dt)+'.nc')
                args.append( (inp_file, out_file, dt, box, options,
                              var_name, res) )

    # run function serial or parallel
    if n_tasks > 1:
        with Pool(processes=n_tasks) as pool:
            results = pool.starmap(sellatlon_UM, args)
    else:
        results = []
        for arg in args:
            results.append(sellatlon_UM(*arg))

    # collect timings from subtasks
    for task_TM in results:
        TM.merge_timings(task_TM)

    # merge all time step files to one
    TM.start('merge')
    for res in ress:
        for var_name in var_names:
            out_dir, out_tmp_dir = paste_dir_names(out_base_dir,
                                                   model_name, res, domain)
            cdo_mergetime(out_tmp_dir, out_dir, var_name)
    TM.stop('merge')

    TM.print_report()
