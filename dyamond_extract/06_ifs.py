#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description:    Extract lat-lon box of data from model IFS.
author:         Christoph Heim
date created:   05.07.2019
date changed:   05.09.2019
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


def sellatlon_IFS(inp_file, out_file, dt, box, options, var_dict,
                  var_name, res):
    
    TM = Timer()
    file_code = '{}km_{}_{:%Y%m%d%H%M}'.format(res, var_name, dt)
    
    if os.path.exists(out_file) and not options['recompute']:
        TM.start('cdo')
        print('\t\t'+file_code+' already computed')
        TM.stop('cdo')
    else:
        print('\t\t'+file_code)

        split = os.path.split(out_file)
        tmp_file = os.path.join(split[0],'tmp_'+split[1])

        # cdo
        TM.start('cdo')
        if not os.path.exists(tmp_file): 
            cdo.select('name='+var_dict['file'],
                        input=(inp_file),
                        options='--eccodes',
                        output=tmp_file)

        if var_dict['dim'] == '3D':
            input = ('-sellevel,'+str(box['vert0'])+'/'+
                           str(box['vert1'])+
                           ' -setgridtype,regular'+
                           ' '+tmp_file)
        else:
            input = (' -setgridtype,regular'+
                     ' '+tmp_file               )

        ofile = cdo.sellonlatbox(
                    box['lon'].start, box['lon'].stop,
                    box['lat'].start, box['lat'].stop,
                    input=input,
                    output=out_file, options='-f nc')

        # delete tmp_file
        if options['rm_tmp_files']:
            os.remove(tmp_file)

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
    #box.update({'vert0':105,'vert1':137}) #top at 3km
    box.update({'vert0':94,'vert1':137}) #top at 6km
    box['lon'] = slice(box['lon'].start - padding, box['lon'].stop + padding)
    box['lat'] = slice(box['lat'].start - padding, box['lat'].stop + padding)

    # name of model 
    model_name = 'IFS'

    # variables to extract
    var_names = ['QV', 'QC', 'T', 'W',
                 'U10M', 'V10M', 'T2M', 'LWUTOA', 'SWDSFC',
                 'SLHFLX', 'SSHFLX', 'TQC', 'PPCONV', 'PPGRID']
    #var_names = ['SSHFLX', 'TQC', 'PPCONV', 'PPGRID']
    
    # model resolutions [km] of simulations
    ress = [9,4]
    ress = [9]
    
    # date range
    first_date = datetime(2016,8,11)
    last_date = datetime(2016,9,9)

    # options for computation
    options = {}
    options['recompute']        = 0
    options['rm_tmp_files']     = 1
    options['rm_tmp_folder']    = 0
    ###########################################################################


    # IFS SPECIFIC SETTINGS
    ###########################################################################
    var_dict = {
        'QV'    :{'file':'q',       'dim':'3D',
                  'group':'mars_out_ml_moist',}, 
        'QC'    :{'file':'clwc',    'dim':'3D',
                  'group':'mars_out_ml_moist',}, 
        'T'     :{'file':'t',       'dim':'3D',
                  'group':'gg_mars_out_ml_upper_sh',}, 
        'W'     :{'file':'param120.128.192','dim':'3D',
                  'group':'gg_mars_out_ml_upper_sh',}, 

        'U10M'  :{'file':'10u',     'dim':'2D',
                  'group':'mars_out',}, 
        'V10M'  :{'file':'10v',     'dim':'2D',
                  'group':'mars_out',}, 
        'T2M'   :{'file':'2t',      'dim':'2D',
                  'group':'mars_out',}, 
        'LWUTOA':{'file':'ttr',     'dim':'2D',
                  'group':'mars_out',}, 
        'SWDSFC':{'file':'ssrd',    'dim':'2D',
                  'group':'mars_out',}, 
        'SLHFLX':{'file':'slhf',    'dim':'2D',
                  'group':'mars_out',}, 
        'SSHFLX':{'file':'sshf',    'dim':'2D',
                  'group':'mars_out',}, 
        'TQC'   :{'file':'tclw',    'dim':'2D',
                  'group':'mars_out',}, 
        'PPCONV':{'file':'crr',     'dim':'2D',
                  'group':'mars_out',}, 
        'PPGRID':{'file':'lsrr',    'dim':'2D',
                  'group':'mars_out',}, 
    }

    base_time = datetime(2016,8,1)

    os.environ['GRIB_DEFINITION_PATH'] = ('/work/ka1081/programs/'+
                                    'eccodes-2.9.0/share/eccodes/definitions')
    ###########################################################################

    ## PREPARING STEPS
    TM = Timer()
    TM.start('real')
    cdo = Cdo()

    if len(sys.argv) > 1:
        n_tasks = int(sys.argv[1])
    else:
        n_tasks = 1
    print('Using ' + str(n_tasks) + ' taks.')

    ## EXTRACT VARIABLES FROM SIMULATIONS
    for var_name in var_names:
        print('############## var ' + var_name + ' ##################')
        for res in ress:
            print('############## res ' + str(res) + ' ##################')

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
            inp_files_glob = glob.glob(os.path.join(inp_dir,
                                var_dict[var_name]['group']+'.*'))
            
            inp_files_glob = [f for f in inp_files_glob if not '.tar.gz' in f]
            times = [base_time + timedelta(hours=int(
                        f.split('.')[1])) 
                        for f in inp_files_glob]
            use_times = [dt for dt in times if dt >= first_date and
                                           dt < last_date+timedelta(days=1)]
            use_files = [inp_files_glob[i] 
                        for i in range(len(inp_files_glob)) if 
                         times[i] in use_times]

            # prepare arguments for function
            args = []
            for i in range(len(use_times)):
                inp_file = use_files[i]
                out_file = os.path.join(out_tmp_dir,
                            var_name+'_{:%Y%m%d%H%M}'.format(use_times[i])+'.nc')
                args.append( (inp_file, out_file, use_times[i], box,
                              options, var_dict[var_name], var_name, res) )

            # run function serial or parallel
            if n_tasks > 1:
                with Pool(processes=n_tasks) as pool:
                    results = pool.starmap(sellatlon_IFS, args)
            else:
                results = []
                for arg in args:
                    results.append(sellatlon_IFS(*arg))

            # collect timings from subtasks
            for task_TM in results:
                TM.merge_timings(task_TM)

            # merge all time step files to one
            TM.start('merge')
            cdo_mergetime(out_tmp_dir, out_dir, var_name)
            TM.stop('merge')

    TM.print_report()
