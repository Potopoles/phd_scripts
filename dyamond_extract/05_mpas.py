#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description:    Extract lat-lon box of data from model MPAS.
author:         Christoph Heim
date created:   05.07.2019
date changed:   05.09.2019
usage:          arguments:
                1st:    n jobs for multiprocessing pool
                MPAS_3.75 : 3D var: 2 jobs (sometimes 3 possible)
                MPAS_7.50 : 3D var: 5 jobs
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


def fix_time_MPAS(out_file, dt, var_dict, var_name):
    
    if os.path.exists(out_file):
        file_code = '{}km_{}_{:%Y%m%d%H%M}'.format(res, var_name, dt)
        print('\t\t'+file_code)

        domain_str = "{},{},{},{}".format(
                        box['lon'].start, box['lon'].stop,
                        box['lat'].start, box['lat'].stop)
        levels_str = "{}/{}".format(
                        box['vert0'], box['vert1'])

        tmp_file = os.path.join(os.path.split(out_file)[0],
                                'temp_'+file_code+'.nc')
        subprocess.call(['mv', out_file, tmp_file])

        if var_dict['type'] == 'history':
            time_fmt = '{:%Y-%m-%d,%H:%M:%S,3hour}'
        elif var_dict['type'] == 'diag':
            time_fmt = '{:%Y-%m-%d,%H:%M:%S,15min}'
        cdo.setreftime('2016-08-01,00:00:00,minutes',
                        input=(' -settaxis,'+time_fmt.format(dt)+
                               ' '+ tmp_file),
                        output=out_file)

        if var_dict['type'] == 'history':
            vdim = var_dict['vdim']
        elif var_dict['type'] == 'diag':
            vdim = 'nodim'
        subprocess.call(['ncpdq', '-O',
                         '--rdr=time,{},lat,lon'.format(vdim),
                         out_file, out_file])

        os.remove(tmp_file)




def sellatlon_MPAS(inp_file, out_file, dt, box, options, var_dict,
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
        levels_str = "{}/{}".format(
                        box['vert0'], box['vert1'])
        if var_dict['type'] == 'history':
            time_fmt = '{:%Y-%m-%d,%H:%M:%S,3hour}'.format(dt)
        elif var_dict['type'] == 'diag':
            time_fmt = '{:%Y-%m-%d,%H:%M:%S,15min}'.format(dt)
        if var_dict['type'] == 'history':
            vdim = var_dict['vdim']
        elif var_dict['type'] == 'diag':
            vdim = 'nodim'

        if i_bash_output:
            subprocess.call(['./run_MPAS.sh', domain_str, levels_str,
                             str(res), os.path.split(out_file)[0],
                             os.path.split(out_file)[1][:-3],
                             var_dict['file'], inp_file, target_grid,
                             time_fmt, vdim])
        else:
            subprocess.call(['./run_MPAS.sh', domain_str, levels_str,
                             str(res), os.path.split(out_file)[0],
                             os.path.split(out_file)[1][:-3],
                             var_dict['file'], inp_file, target_grid,
                             time_fmt, vdim
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
    #box.update({'vert0':1,'vert1':22}) #3km top
    box.update({'vert0':1,'vert1':31}) #6km top
    box['lon'] = slice(box['lon'].start - padding, box['lon'].stop + padding)
    box['lat'] = slice(box['lat'].start - padding, box['lat'].stop + padding)

    # name of model 
    model_name = 'MPAS'

    # variables to extract
    var_namess = {
        '3D':['T', 'QV', 'QC', 'W'],
        '3D':['QV', 'QC'],
        #'2D':['LWUTOA', 'T2M', 'U10M', 'V10M', 'SWDSFC',
        #      'TQC', 'PPCONV', 'PPGRID'],
        '2D':['U10M', 'V10M', 'SWDSFC',
              'TQC', 'PPCONV', 'PPGRID'],
    }

    run_var_type = '3D'
    #run_var_type = '2D'

    var_names = var_namess[run_var_type]

    #ress = [7.5, 3.75]
    ress = [3.75]
    #ress = [7.5]

    i_bash_output = 1
    
    # date range
    first_date = datetime(2016,8,11)
    last_date = datetime(2016,9,9)

    # position 1 mistpp1

    # position 2 mistpp2

    ## position 3 mistpp3

    ## position 4 mistpp4

    # position 5 mistpp5 3D
    first_date = datetime(2016,8,11)
    last_date = datetime(2016,9,9)


    # options for computation
    options = {}
    options['recompute']        = 0
    options['rm_tmp_files']     = 1
    options['rm_tmp_folder']    = 0
    ###########################################################################


    # MPAS SPECIFIC SETTINGS
    ###########################################################################
    grid_def_base_dir = os.path.join('/work','ka1081',
                            '2019_06_Hackathon_Mainz', 'falko')

    var_dict = {
        'QV'    :{'file':'qv',          'type':'history','vdim':'nVertLevels'}, 
        'QC'    :{'file':'qc',          'type':'history','vdim':'nVertLevels'}, 
        'T'     :{'file':'temperature', 'type':'history','vdim':'nVertLevels'}, 
        'W'     :{'file':'w',           'type':'history','vdim':'nVertLevelsP1'}, 

        'U10M'  :{'file':'u10',         'type':'diag'}, 
        'V10M'  :{'file':'v10',         'type':'diag'}, 
        'T2M'   :{'file':'t2m',         'type':'diag'}, 
        'LWUTOA':{'file':'olrtoa',      'type':'diag'}, 
        'SWDSFC':{'file':'acswdnb',     'type':'diag'}, 
        # missing in model output
        #'SLHFLX':{'file':'',     'type':'diag'}, 
        #'SSHFLX':{'file':'',     'type':'diag'}, 
        'TQC'   :{'file':'vert_int_qc', 'type':'diag'}, 
        'PPCONV':{'file':'rainc',       'type':'diag'}, 
        'PPGRID':{'file':'rainnc',      'type':'diag'}, 
    }
    grid_dict = {
        3.75:{'grid_def_file':os.path.join(grid_def_base_dir,
                             'MPAS_3.75km_grid.nc'),
            }, 
        7.5: {'grid_def_file':os.path.join(grid_def_base_dir,
                             'MPAS_7.5km_grid.nc'),
            }, 
    }
    inc_min = {'history':180, 'diag':15}
    ###########################################################################

    ## PREPARING STEPS
    TM = Timer()
    cdo = Cdo()

    if len(sys.argv) > 1:
        n_tasks = int(sys.argv[1])
    else:
        n_tasks = 1
    print('Using ' + str(n_tasks) + ' taks.')

    ## EXTRACT VARIABLES FROM SIMULATIONS
    for var_name in var_names:
        print('############## var ' + var_name + ' ##################')

        dt_range = np.arange(first_date, last_date + timedelta(days=1),
                        timedelta(minutes=inc_min[
                        var_dict[var_name]['type']])).tolist()

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
            # mpas grid definition file
            grid_def_file = grid_dict[res]['grid_def_file']
            # target grid on which to interpolate the model output
            target_grid = os.path.join('grids','latlon_{}km_dom_{}'.format(
                                        res, domain['code']))
            write_grid_file(box, target_grid, res)

            # find times and files that should be extracted
            # and prepare arguments for function
            args = []
            for dt in dt_range:
                # missing time step:
                if dt != datetime(2016,9,5,0,0,0):
                    inp_file = glob.glob(os.path.join(
                                    inp_dir,var_dict[var_name]['type']+
                                    '.{:%Y-%m-%d_%H.%M.%S}.nc'.format(dt)))[0]
                    out_file = os.path.join(out_tmp_dir,
                                var_name+'_{:%Y%m%d%H%M}'.format(dt)+'.nc')
                    args.append( (inp_file, out_file, dt, box, options,
                                  var_dict[var_name],
                                  target_grid, var_name, res) )

                #fix_time_MPAS(out_file, dt, var_dict[var_name], var_name)

            # run function serial or parallel
            if n_tasks > 1:
                with Pool(processes=n_tasks) as pool:
                    results = pool.starmap(sellatlon_MPAS, args)
            else:
                results = []
                for arg in args:
                    results.append(sellatlon_MPAS(*arg))
            
            # collect timings from subtasks
            for task_TM in results:
                TM.merge_timings(task_TM)

            # merge all time step files to one
            TM.start('merge')
            cdo_mergetime(out_tmp_dir, out_dir, var_name)
            TM.stop('merge')

    TM.print_report()
