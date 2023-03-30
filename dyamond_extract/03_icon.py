#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description:    Extract lat-lon box of data from model ICON.
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
from package.utilities import Timer, write_grid_file, cdo_mergetime
from namelist import domain, padding
from functions import paste_dir_names
###############################################################################


def comp_weights_file(target_grid, weights_file, inp_file, grid_def_file,
                      res, box, options):
    """
    """
    #if (not os.path.exists(target_grid)) or (options['recompute']):
    #    write_grid_file(box, target_grid, res)

    print('Compute weights file')
    ofile = cdo.gennn(target_grid, input=(' -setgrid,'+grid_def_file+
                           ' '+inp_file), output=weights_file,
                      options='-P 1')



def sellatlon_ICON(inp_file, out_file, grid_def_file, weights_file,
                   target_grid, dt, box, options, var_dict, var_name,
                   res):
    """
    """
    
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

        if var_dict['dim'] == '3d':
            ofile = cdo.remap(target_grid, weights_file,
                        input=(
                               ' -sellevidx,'+
                               str(box['vert0'])+'/'+str(box['vert1'])+
                               ' -setgrid,'+grid_def_file+
                               ' '+inp_file),
                        output=out_file, options='-f nc')
        elif var_dict['dim'] == '2d':
            ofile = cdo.remap(target_grid, weights_file,
                        input=(
                               ' -setgrid,'+grid_def_file+
                               ' -selname,'+var_dict['key']+
                               ' '+inp_file),
                        output=out_file, options='-f nc')

        TM.stop('cdo')

    return(TM)


if __name__ == '__main__':

    # GENERAL SETTINGS
    ###########################################################################
    # input and output directories
    raw_data_dir = os.path.join('/work','ka1081','DYAMOND')
    out_base_dir = os.path.join('/work','ka1081','2019_06_Hackathon_Mainz',
                                'christoph_heim','newdata')

    # vert box to subselect
    box = domain
    #box.update({'vert0':73-14,'vert1':91-14}) #3km top
    box.update({'vert0':64-14,'vert1':91-14}) #6km top
    box['lon'] = slice(box['lon'].start - padding, box['lon'].stop + padding)
    box['lat'] = slice(box['lat'].start - padding, box['lat'].stop + padding)

    # name of model 
    model_name = 'ICON'

    # variables to extract
    var_names = ['QV', 'QC', 'T', 'W',
                 'U10M', 'V10M', 'T2M', 'LWUTOA', 'SWNSFC', 'SWDIFFUSFC',
                 'SLHFLX', 'SSHFLX', 'TQC', 'PP']
    #var_names = ['LWUTOA']
    
    # model resolutions [km] of simulations
    #ress = [10,5,2.5]
    ress = [2.5]
    #ress = [10]
    
    # date range
    first_date = datetime(2016,8,11)
    last_date = datetime(2016,9,9)

    # options for computation
    options = {}
    options['recompute']        = 0
    options['rm_tmp_folder']    = 0
    ###########################################################################


    # ICON SPECIFIC SETTINGS
    ###########################################################################
    grid_def_base_dir = os.path.join('/work','bk1040','experiments', 'input')

    var_dict = {
    'QV'        :{'file':'qv',          'dim':'3d',  }, 
    'QC'        :{'file':'tot_qc_dia',  'dim':'3d',  }, 
    'T'         :{'file':'t',           'dim':'3d',  }, 
    'W'         :{'file':'w',           'dim':'3d',  }, 

    'U10M'      :{'file':'atm3_2d_ml',      'dim':'2d',   'key':'U_10M'}, 
    'V10M'      :{'file':'atm3_2d_ml',      'dim':'2d',   'key':'V_10M'}, 
    'T2M'       :{'file':'atm3_2d_ml',      'dim':'2d',   'key':'T_2M'}, 
    'LWUTOA'    :{'file':'atm_2d_avg_ml',   'dim':'2d',   'key':'ATHB_T'}, 
    'SWNSFC'    :{'file':'atm_2d_avg_ml',   'dim':'2d',   'key':'ASOB_S'}, 
    'SWDIFFUSFC':{'file':'atm_2d_avg_ml',   'dim':'2d',   'key':'ASWDIFU_S'}, 
    'SLHFLX'    :{'file':'atm2_2d_ml',      'dim':'2d',   'key':'LHFL_S'}, 
    'SSHFLX'    :{'file':'atm2_2d_ml',      'dim':'2d',   'key':'SHFL_S'}, 
    'TQC'       :{'file':'atm1_2d_ml',      'dim':'2d',   'key':'TQC_DIA'}, 
    'PP'        :{'file':'atm2_2d_ml',      'dim':'2d',   'key':'TOT_PREC'}, 
    }
    grid_dict = {
        10:  {'grid_def_file':os.path.join(grid_def_base_dir,
                             '10km/icon_grid_0025_R02B08_G.nc'),
            }, 
        5:  {'grid_def_file':os.path.join(grid_def_base_dir,
                             '5km_2/icon_grid_0015_R02B09_G.nc'),
            }, 
        2.5:{'grid_def_file':os.path.join(grid_def_base_dir,
                             '2.5km/icon_grid_0017_R02B10_G.nc'),
            }, 
    }

    os.environ['GRIB_DEFINITION_PATH'] = ('/mnt/lustre01/sw/rhel6-x64/eccodes'+
                                          '/definitions')
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
    for res in ress:
        print('############## res ' + str(res) + ' ##################')
        for var_name in var_names:
            print('\t############## var ' + var_name + ' ##################')

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
            # icon grid definition file
            grid_def_file = grid_dict[res]['grid_def_file']
            # weights file to compute once for a grid
            weights_file = os.path.join(out_tmp_dir,
                                'weights_{}km_dom_{}'.format(res,
                                domain['code']))
            # target grid on which to interpolate the model output
            target_grid = os.path.join('grids','latlon_{}km_dom_{}'.format(
                                        res, domain['code']))
            write_grid_file(box, target_grid, res)

            # find times and files that should be extracted
            # and prepare arguments for function
            for dt in dt_range:
                inp_files_glob = glob.glob(os.path.join(inp_dir,
                                            '*_{}_*{:%Y%m%d}*'.format(
                                            var_dict[var_name]['file'], dt)))
                inp_file = os.path.join(inp_files_glob[0])

                out_file = os.path.join(out_tmp_dir,
                            var_name+'_{:%Y%m%d}'.format(dt)+'.nc')
                args.append( (inp_file, out_file, grid_def_file,
                              weights_file, target_grid,
                              dt, box, options, var_dict[var_name],
                              var_name, res) )

            TM.start('grid')
            if ((not os.path.exists(weights_file)) or 
                (not os.path.exists(target_grid))):
                comp_weights_file(target_grid, weights_file,
                                  inp_file, grid_def_file,
                                  res, box, options)
            TM.stop('grid')

    # run function serial or parallel
    if n_tasks > 1:
        with Pool(processes=n_tasks) as pool:
            results = pool.starmap(sellatlon_ICON, args)
    else:
        results = []
        for arg in args:
            results.append(sellatlon_ICON(*arg))

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
