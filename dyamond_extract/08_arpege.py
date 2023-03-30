#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description:    Extract lat-lon box of data from model ARPEGE-NH.
author:         Christoph Heim
date created:   09.07.2019
date changed:   10.09.2019
usage:          arguments:
                1st:    n jobs for multiprocessing pool
python:         3.5.2
"""
###############################################################################
import os, glob, subprocess, sys, time, shutil, copy
import numpy as np
from datetime import datetime, timedelta
from multiprocessing import Pool
from pathlib import Path
from cdo import Cdo
from package.utilities import Timer, cdo_mergetime, write_grid_file, cd
from namelist import domain, padding
from functions import paste_dir_names
###############################################################################

def check_missing(inp_list, box, var_dict, var_name, file_code):
    """
    Checks for var given by var_dict whether inp_list contains all the
    necessary gribsplit levels (files)
    """
    missing = False
    missing_levels = []
    if var_dict['vdim'] == '3D':
        levels = ['l{}00'.format(lev) for lev in range(box['vert0'],
                                                    box['vert1']+1)]
        for lev in levels:
            lev_in_files = False
            for file in inp_list:
                if lev in file:
                    lev_in_files = True

            if not lev_in_files:
                missing = True
                missing_levels.append(lev)
        #if missing:
        #    #print('missing levels:', missing_levels, 'for', var_name, 'in',
        #    print('missing levels for', var_name, 'in',file_code) 

    else:
        if len(inp_list) == 0:
            missing = True
            #print('missing one-layer file', 'for', var_name, 'in',
            #      file_code)
    return(missing)
    


def filter_levels(inp_list, box, var_dict):
    """
    Remove files from inp_list that are not within vertical levels
    return copy of inp_list
    """
    file_list = copy.copy(inp_list) 
    if var_dict['vdim'] == '3D':
        # Remove unnecessary levels
        levels = ['l{}00'.format(lev) for lev in range(box['vert0'],
                                                    box['vert1']+1)]
        remove = []
        for file in file_list:
            match = False
            for lev in levels:
                if lev in file:
                    match = True
            if not match:
                remove.append(file)
        for file in remove:
            file_list.remove(file)   
    return(file_list)


def get_splf(split_files, var_dict):
    """
    Get glob search pattern for grib var split file.    
    """
    split_file_descr = '{}.{}*{}.gp'
    splf = split_file_descr.format(split_files, var_dict['grb_srf'],
                               var_dict['file'])
    return(splf)


def comp_weights_file(target_grid, weights_file, inp_file, grid_def_file,
                      res, box, options):
    """
    """
    print('Compute weights file')
    #ofile = cdo.gennn(target_grid,
    #                  input=(' -setgrid,mpas:'+grid_def_file+
    #                       ' '+inp_file),
    #                  output=weights_file)

    frmt_string = ("-sellonlatbox,{},{},{},{} -setgrid,{}"+
                   " -setgridtype,regular {}")
    input = frmt_string.format(
                            box['lon'].start,box['lon'].stop,
                            box['lat'].start,box['lat'].stop,     
                            grid_def_file,
                            inp_file)
    ofile = cdo.gennn(target_grid,
                      input=input, output=weights_file)


def sellatlon_ARPEGE(inp_file, out_file, dt, box, options, var_name, var_dicts,
                     res, weights_file, target_grid):

    TM = Timer()
    file_code = '{}km_{}_{:%Y%m%d%H%M}'.format(res, var_name, dt)
    broken_grib_file = 'broken_grib_files_arpege'
    
    # read file containing list of broken grib files
    broken = []
    with open(broken_grib_file, 'r') as f:
        for line in f:
            broken.append(line[:-1])

    if file_code in broken:
        print('skip', file_code, 'due to bad grib file.')
    elif os.path.exists(out_file) and not options['recompute']:
        pass
        #print('\t\t'+file_code+' already computed')
    else:
        print(file_code)
        TM.start('prep') 
        split = os.path.split(out_file)
        tmp_dir = os.path.join(split[0],'dirtmp_{:%Y%m%d%H%M}'.format(dt))
        Path(tmp_dir).mkdir(parents=True, exist_ok=True)
        split_files = os.path.join(tmp_dir,'split')

        # run gribsplit if not already done
        #print(get_splf(split_files, var_dicts[var_name]))
        search = glob.glob(get_splf(split_files, var_dicts[var_name]))
        missing = check_missing(search, box, var_dicts[var_name], var_name,
                                file_code)

        if missing and var_name == main_var:
            print('run gribsplit')
            # Split original grib files
            command = './gribsplit'
            gribsplit_file = os.path.join(tmp_dir,'gribsplit')
            if os.path.exists(gribsplit_file):
                os.remove(gribsplit_file)
            subprocess.call(['cp', 'gribsplit', tmp_dir])
            # change context to local directory because gribsplit
            # produces _tmpfile in directory where it is called.
            # Changing directory allows to run in parallel by preventing
            # _tmpfiles from being overwritten by parallel processes.
            with cd(tmp_dir):
                subprocess.call([command, inp_file,
                                os.path.split(split_files)[1]],
                                stdout=subprocess.DEVNULL)

            # remove all split variables that are irrelevant
            keep_files = []
            for key,var_dict in var_dicts.items():
                search = glob.glob(get_splf(split_files, var_dict))
                search = filter_levels(search, box, var_dicts[var_name])
                keep_files.extend(search)

            ## For the moment do not remove files from other variables
            ## since they may be used later..
            #search = glob.glob('{}/*.gp'.format(tmp_dir))
            #for file in search:
            #    if file not in keep_files:
            #        os.remove(file)
            search = glob.glob('{}/*.spectral'.format(tmp_dir))
            for file in search:
                os.remove(file)

        # Check if valid files remain
        tmp_files = glob.glob(get_splf(split_files, var_dicts[var_name]))
        # if not, this means that the grib file is broken
        if len(tmp_files) == 0:
            # write this to the broken grib files list
            with open(broken_grib_file, 'a') as f:
                f.write(file_code+'\n')
            print('No valid files for ' + file_code)
            return(TM)
        TM.stop('prep') 

        # if grid does not exist compute it
        TM.start('grid') 
        if not os.path.exists(weights_file):
            comp_weights_file(target_grid, weights_file,
                              tmp_files[0], grid_def_file,
                              res, box, options)
        TM.stop('grid') 

        # cdo
        TM.start('cdo')
        merge_files = []
        for tmp_file in tmp_files:
            input = ("-sellonlatbox,{},{},{},{} -setgrid,{}"+
                     " -setgridtype,regular {}").format(
                        box['lon'].start, box['lon'].stop,
                        box['lat'].start, box['lat'].stop,     
                        grid_def_file,
                        tmp_file)
            #input = ("-remap,{},{} -setgrid,{}"+
            #         " -setgridtype,regular {}").format(
            #            target_grid, weights_file,
            #            grid_def_file, tmp_file)
            if var_dicts[var_name]['vdim'] == '3D':
                out_file_use = tmp_file + '.nc'
                merge_files.append(out_file_use)
            else:
                out_file_use = out_file

            if options['rm_tmp_files'] and os.path.exists(out_file_use):
                os.remove(out_file_use)
            if not os.path.exists(out_file_use):
                ofile = cdo.remap(target_grid, weights_file,
                                input=input, output=out_file_use,
                                options='-f nc4')
            #ofile = cdo.sellonlatbox(
            #            box['lon'].start, box['lon'].stop,
            #            box['lat'].start, box['lat'].stop,     
            #            input=input, output=out_file_use, options='-f nc4')

        # merge vertical levels
        if var_dicts[var_name]['vdim'] == '3D':
            merge_files.sort()
            cdo.merge(input=merge_files, output=out_file)
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
    #box.update({'vert0':54,'vert1':75}) # 3km top
    box.update({'vert0':45,'vert1':75}) # 6km top
    box['lon'] = slice(box['lon'].start - padding, box['lon'].stop + padding)
    box['lat'] = slice(box['lat'].start - padding, box['lat'].stop + padding)

    # name of model 
    model_name = 'ARPEGE-NH'

    # variables to extract
    var_namess = {
        #'3D':['T', 'QV', 'QC', 'W', 'H'],
        '3D':['QV', 'QC', 'W', 'H'],
        #'2D':['LWUTOA', 'T2M', 'U10M', 'V10M', 'SWDSFC',
        #      'SLHFLX', 'SSHFLX', 'TQC', 'PP'],
        '2D':['SSHFLX', 'TQC', 'PP'],
    }
    # first variable that is read from grib file
    main_vars =  {'3D':'T','2D':'LWUTOA'}

    run_var_type = '3D'
    #run_var_type = '2D'
    
    var_names = var_namess[run_var_type]
    main_var  = main_vars[run_var_type]

    # model resolutions [km] of simulations
    ress = [2.5]

    # 2D: done
    first_date = datetime(2016,8,11)
    last_date = datetime(2016,9,9)
    ## 3D: done
    #first_date = datetime(2016,8,11)
    #last_date = datetime(2016,9,12)


    ## 2D: laptop postition 3 mistpp4 
    #first_date = datetime(2016,8,13)
    #last_date = datetime(2016,8,25)

    ## 3D: laptopt postition 4 mistpp5 
    #first_date = datetime(2016,8,26)
    #last_date = datetime(2016,9,9)

    # options for computation
    options = {}
    options['recompute']        = 0
    options['rm_tmp_files']     = 1 # necessary
    options['rm_tmp_folder']    = 0
    ###########################################################################


    # ARPEGE SPECIFIC SETTINGS
    ###########################################################################
    var_dict = {
        'QV'    :{'file':'0.1.0',       'grb_srf':'t119',   'vdim':'3D',}, 
        'QC'    :{'file':'0.1.83',      'grb_srf':'t119',   'vdim':'3D',}, 
        'T'     :{'file':'0.0.0',       'grb_srf':'t119',   'vdim':'3D',}, 
        'W'     :{'file':'0.2.9',       'grb_srf':'t119',   'vdim':'3D',}, 
        'H'     :{'file':'0.3.4' ,      'grb_srf':'t119',   'vdim':'3D',}, 

        'LWUTOA':{'file':'0.5.5',       'grb_srf':'t8',     'vdim':'2D',}, 
        'U10M'  :{'file':'0.2.2',       'grb_srf':'t103',   'vdim':'2D',}, 
        'V10M'  :{'file':'0.2.3',       'grb_srf':'t103',   'vdim':'2D',}, 
        'T2M'   :{'file':'0.0.0',       'grb_srf':'t103',   'vdim':'2D',}, 
        'SWDSFC':{'file':'0.4.7',       'grb_srf':'t1',     'vdim':'2D',}, 
        'SLHFLX':{'file':'0.0.10',      'grb_srf':'t1',     'vdim':'2D',}, 
        'SSHFLX':{'file':'0.0.11',      'grb_srf':'t1',     'vdim':'2D',}, 
        'TQC'   :{'file':'192.128.78',  'grb_srf':'t1',     'vdim':'2D',}, 
        'PP'    :{'file':'0.1.8',       'grb_srf':'t1',     'vdim':'2D',}, 
    }
    inc_min = {'3D':180, '2D':15}
    remap_res = 2.5
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
                            var_dict[var_name]['vdim']])).tolist()

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
            # ARPGEGE grid definition file
            grid_def_file = 'griddes.arpege1'
            # weights file to compute once for a grid
            weights_file = os.path.join(out_tmp_dir,
                                'weights_{}km_dom_{}'.format(remap_res,
                                domain['code']))
            # target grid on which to interpolate the model output
            target_grid = os.path.join('grids','latlon_{}km_dom_{}'.format(
                                        remap_res, domain['code']))
            write_grid_file(box, target_grid, remap_res)

            # find times and files that should be extracted
            # and prepare arguments for function
            # (treat ingenious idea of using 2400 for midnight instead of 0000)
            args = []
            for ti,dt in enumerate(dt_range):
                if (dt.hour == 0) and (dt.minute == 0):
                    dt_tmp = dt - timedelta(days=1)
                    file_name = 'ARPNH{}{:%Y%m%d}2400'.format(
                                        var_dict[var_name]['vdim'], dt_tmp)
                    inp_file = glob.glob(os.path.join(inp_dir,
                                    '{:%Y%m%d}'.format(dt_tmp), file_name))[0]
                else:
                    file_name = 'ARPNH{}{:%Y%m%d%H%M}'.format(
                                        var_dict[var_name]['vdim'], dt)
                    inp_file = glob.glob(os.path.join(inp_dir,
                                        '{:%Y%m%d}'.format(dt), file_name))[0]

                out_file = os.path.join(out_tmp_dir,
                            var_name+'_{:%Y%m%d%H%M}'.format(dt)+'.nc')

                args.append( (inp_file, out_file, dt, box, options, var_name,
                              var_dict, res, weights_file, target_grid) )

                # compute weights file if necessary
                if ti == 0:
                    if not os.path.exists(weights_file):
                        sellatlon_ARPEGE(inp_file, out_file, dt, box, options,
                                       var_name, var_dict, res, weights_file,
                                       target_grid)

            # run function serial or parallel
            if n_tasks > 1:
                with Pool(processes=n_tasks) as pool:
                    results = pool.starmap(sellatlon_ARPEGE, args)
            else:
                results = []
                for arg in args:
                    results.append(sellatlon_ARPEGE(*arg))

            # collect timings from subtasks
            for task_TM in results:
                TM.merge_timings(task_TM)

            # merge all time step files to one
            TM.start('merge')
            cdo_mergetime(out_tmp_dir, out_dir, var_name)
            TM.stop('merge')

    TM.print_report()
