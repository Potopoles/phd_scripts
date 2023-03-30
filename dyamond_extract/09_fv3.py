#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description:    Extract lat-lon box of data from model FV3.
author:         Christoph Heim
date created:   20.07.2019
date changed:   09.07.2019
usage:          arguments:
                1st:    n jobs for multiprocessing pool
                FV3_3.25 : 3D var: 5 jobs
"""
###############################################################################
import os, glob, subprocess, sys, time, shutil
import numpy as np
from datetime import datetime, timedelta
from multiprocessing import Pool
from pathlib import Path
from cdo import Cdo
from package.utilities import Timer, write_grid_file, cdo_mergetime
from namelist import domain, padding
from functions import paste_dir_names
###############################################################################


def sellatlon_FV3(inp_file, out_file, dt, box, options, var_dict,
                  target_grid, var_name, res):
    
    TM = Timer()
    file_code = '{}km_{}_{:%Y%m%d%H%M}'.format(res, var_name, dt)

    if os.path.exists(out_file) and not options['recompute']:
        TM.start('run')
        print('\t\t'+file_code+' already computed')
        TM.stop('run')
    else:
        TM.start('run')
        print('\t\t'+file_code)

        domain_str = "{},{},{},{}".format(
                        box['lon'].start, box['lon'].stop,
                        box['lat'].start, box['lat'].stop)

        if 'levtype' in var_dict:
            levels_str = "{}/{}".format(
                            box[var_dict['levtype']]['vert0'],
                            box[var_dict['levtype']]['vert1'])
            
        else:
            levels_str = "1/1"

        if i_bash_output:
            subprocess.call(['./run_FV3.sh', domain_str, levels_str,
                             str(res), os.path.split(out_file)[0],
                             os.path.split(out_file)[1][:-3],
                             inp_file, target_grid,
                            ], )
        else:
            subprocess.call(['./run_FV3.sh', domain_str, levels_str,
                             str(res), os.path.split(out_file)[0],
                             os.path.split(out_file)[1][:-3],
                             inp_file, target_grid,
                            ], stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
        TM.stop('run')

    TM.print_report(short=True)
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
    ## 3km top
    #box.update({'plev' :{'vert0':23,'vert1':31},
    #            'mfull':{'vert0':55,'vert1':79},
    #            'mhalf':{'vert0':55,'vert1':80},},)
    ## 6km top
    box.update({'plev' :{'vert0':18,'vert1':31},
                'mfull':{'vert0':42,'vert1':79},
                'mhalf':{'vert0':42,'vert1':80},},)
    box['lon'] = slice(box['lon'].start - padding, box['lon'].stop + padding)
    box['lat'] = slice(box['lat'].start - padding, box['lat'].stop + padding)

    # name of model 
    model_name = 'FV3'

    # variables to extract
    var_names = ['H', 'T', 'QV', 'QC', 'W',
                 'U10M', 'V10M', 'T2M', 'LWUTOA', 'SWDSFC',
                 'TQC', 'PP']

    #var_names = ['H', 'T', 'QC', 'QV', 'W']
    #var_names = ['QC', 'QV', 'W']
    #var_names = ['U10M', 'V10M', 'T2M', 'LWUTOA', 'SWDSFC',
    #             'TQC']
    ress = [3.25]

    i_bash_output = 1
    
    # date range
    first_date = datetime(2016,8,11) # must be 1,11,21,31
    last_date = datetime(2016,9,9)

    # options for computation
    options = {}
    options['recompute']        = 0
    options['rm_tmp_files']     = 1
    options['rm_tmp_folder']    = 0
    ###########################################################################


    # FV3 SPECIFIC SETTINGS
    ###########################################################################
    var_dict = {
        'H'     :{'file':'h_plev_3hr',  'levtype':'plev'}, 
        'T'     :{'file':'temp_3hr',    'levtype':'mfull'}, 
        'QV'    :{'file':'q_plev_3hr',  'levtype':'plev'}, 
        'QC'    :{'file':'ql_plev_3hr', 'levtype':'plev'}, 
        'W'     :{'file':'w_3hr',       'levtype':'mfull'}, 

        'U10M'  :{'file':'u10m_15min',}, 
        'V10M'  :{'file':'v10m_15min',}, 
        'T2M'   :{'file':'t2m_15min',}, 
        'LWUTOA':{'file':'flut_15min',}, 
        'SWDSFC':{'file':'fsds_15min',}, 
        'SLHFLX':{'file':'lhflx_15min',}, 
        'SSHFLX':{'file':'shflx_15min',}, 
        'TQC'   :{'file':'intql_15min',}, 
        'PP'    :{'file':'pr_15min',}, 
    }
    grid_dict = { 3.25:{'grid_def_file':'gridspec.nc',},}
    ###########################################################################

    ## PREPARING STEPS
    TM = Timer()
    cdo = Cdo()

    if len(sys.argv) > 1:
        n_tasks = int(sys.argv[1])
    else:
        n_tasks = 1
    print('Using ' + str(n_tasks) + ' taks.')

    dt_range = np.arange(first_date, last_date + timedelta(days=1),
                    timedelta(days=10)).tolist()

    ## EXTRACT VARIABLES FROM SIMULATIONS
    # args used as input to parallel executed function
    args = []
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

            # prepare grid interpolation
            # fv3 grid definition file
            grid_def_file = os.path.join(out_tmp_dir, '..',
                                grid_dict[res]['grid_def_file'])
            # target grid on which to interpolate the model output
            target_grid = os.path.join('grids','latlon_{}km_dom_{}'.format(
                                        res, domain['code']))
            write_grid_file(box, target_grid, res)

            # find times and files that should be extracted
            # and prepare arguments for function
            for dt in dt_range:
                inp_file_patt = os.path.join(
                                inp_dir, '{:%Y%m%d%H}'.format(dt),
                                '{}.tile?.nc'.format(
                                var_dict[var_name]['file']))
                out_file = os.path.join(out_tmp_dir,
                            var_name+'_{:%Y%m%d%H%M}'.format(dt)+'.nc')
                args.append( (inp_file_patt, out_file, dt, box,
                              options, var_dict[var_name],
                              target_grid, var_name, res) )

    # run function serial or parallel
    if n_tasks > 1:
        with Pool(processes=n_tasks) as pool:
            results = pool.starmap(sellatlon_FV3, args)
    else:
        results = []
        for arg in args:
            results.append(sellatlon_FV3(*arg))

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
