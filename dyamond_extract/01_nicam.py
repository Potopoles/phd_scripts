#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description:    Extract lat-lon box of data from model NICAM.
author:         Christoph Heim
date created:   27.06.2019
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

def sellatlon_NICAM(inp_file, out_file, dt, box, options, var_dict,
                    var_name, res):
    
    TM = Timer()

    file_code = '{}km_{}_{:%Y%m%d}'.format(res, var_name, dt)
    
    if os.path.exists(out_file) and not options['recompute']:
        TM.start('cdo')
        print('\t\t'+file_code+' already computed')
        TM.stop('cdo')
    else:
        # cdo
        TM.start('cdo')
        print('\t\t'+file_code)

        if var_dict['dim'] == '3D':
            input = ('-sellevidx,'+str(box['vert0'])+'/'+
                               str(box['vert1'])+' '+inp_file)
        elif var_dict['dim'] == '2D':
            input=inp_file

        ofile = cdo.sellonlatbox(
                    box['lon'].start,box['lon'].stop,
                    box['lat'].start,box['lat'].stop,
                    input=input,
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

    # lat lon vert box to subselect
    box = domain
    #box.update({'vert0':1,'vert1':18}) # 3km
    box.update({'vert0':1,'vert1':26}) # 6km
    box['lon'] = slice(box['lon'].start - padding, box['lon'].stop + padding)
    box['lat'] = slice(box['lat'].start - padding, box['lat'].stop + padding)

    # name of model 
    model_name = 'NICAM'

    # variables to extract
    var_names = ['QV', 'QC', 'T', 'W',
                 'U10M', 'V10M', 'T2M', 'LWUTOA', 'SWDSFC',
                 'SLHFLX', 'SSHFLX', 'TQC', 'PP']
    var_names = ['PP']
    
    # model resolutions [km] of simulations
    ress = [7, 3.5]
    #ress = [7]
    #ress = [3.5]
    
    # date range
    first_date = datetime(2016,8,11)
    last_date = datetime(2016,9,9)

    # options for computation
    options = {}
    options['recompute']        = 0
    options['rm_tmp_folder']    = 0
    ###########################################################################


    # NICAM SPECIFIC SETTINGS
    ###########################################################################
    var_dict = {
        'QV'    :{'file':'ms_qv',       'dim':'3D',  }, 
        'QC'    :{'file':'ms_qc',       'dim':'3D',  }, 
        'T'     :{'file':'ms_tem',      'dim':'3D',  }, 
        'W'     :{'file':'ms_w',        'dim':'3D',  }, 

        'U10M'  :{'file':'ss_u10m',     'dim':'2D',  }, 
        'V10M'  :{'file':'ss_v10m',     'dim':'2D',  }, 
        'T2M'   :{'file':'ss_t2m',      'dim':'2D',  }, 
        'LWUTOA':{'file':'sa_lwu_toa',  'dim':'2D',  }, 
        'SWDSFC':{'file':'ss_swd_sfc',  'dim':'2D',  }, 
        'SLHFLX':{'file':'ss_lh_sfc',   'dim':'2D',  }, 
        'SSHFLX':{'file':'ss_sh_sfc',   'dim':'2D',  }, 
        'TQC'   :{'file':'sa_cldw',     'dim':'2D',  }, 
        'PP'    :{'file':'sa_tppn',     'dim':'2D',  }, 
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
        print('############## var ' + var_name + ' ##################')
        for res in ress:
            print('############## res ' + str(res) + ' ##################')
            
            # data input directory
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
                inp_files_glob = glob.glob(os.path.join(inp_dir,
                                            '{:%Y%m%d}*.000000'.format(dt)))
                inp_file = os.path.join(inp_files_glob[0],
                                    var_dict[var_name]['file'] + '.nc')

                out_file = os.path.join(out_tmp_dir,
                            var_name+'_{:%Y%m%d}'.format(dt)+'.nc')
                args.append( (inp_file, out_file, dt, box, options,
                              var_dict[var_name], var_name, res) )

    # run function serial or parallel
    if n_tasks > 1:
        with Pool(processes=n_tasks) as pool:
            results = pool.starmap(sellatlon_NICAM, args)
    else:
        results = []
        for arg in args:
            results.append(sellatlon_NICAM(*arg))

    # collect timings from subtasks
    for task_TM in results:
        TM.merge_timings(task_TM)

    # merge all time step files to one
    TM.start('merge')
    for var_name in var_names:
        for res in ress:
            out_dir, out_tmp_dir = paste_dir_names(out_base_dir,
                                                   model_name, res, domain)
            cdo_mergetime(out_tmp_dir, out_dir, var_name)
    TM.stop('merge')

    TM.print_report()
