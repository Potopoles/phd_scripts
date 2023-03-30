#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description:    Extract lat-lon box of data from model COSMO.
author:         Christoph Heim
date created:   24.07.2019
date changed:   09.09.2019
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

def sellatlon_COSMO(inp_file, out_file, dt, box, options, var_name, res):
    
    TM = Timer()
    file_code = '{}km_{}_{:%Y%m%d%H%M}'.format(res, var_name, dt)
    
    if os.path.exists(out_file) and not options['recompute']:
        TM.start('cdo')
        print('\t\t'+file_code+' already computed')
        TM.stop('cdo')
    else:
        TM.start('cdo')
        print('\t\t'+file_code)

        split = os.path.split(out_file)
        nco_file = os.path.join(split[0],'nco_'+split[1])
        #print(nco_file)

        ## nco
        #if not os.path.exists(nco_file):
        #    TM.start('nco')
        #    bash_command = 'ncrcat -O -v {} {} {}'.format(
        #                    var_dict[var_name]['key'], inp_file,
        #                    nco_file)
        #    process = subprocess.Popen(bash_command.split(),
        #                                stdout=subprocess.PIPE)
        #    output, error = process.communicate()
        #    TM.stop('nco')
        #else:
        #    TM.start('nco')
        #    TM.stop('nco')

        if var_dict[var_name]['dim'] == '3D':
            bash_command = 'ncrcat -O -v {} {} {}'.format(
                            var_dict[var_name]['key'], inp_file,
                            nco_file)
            process = subprocess.Popen(bash_command.split(),
                                        stdout=subprocess.PIPE)
            output, error = process.communicate()
            ofile = cdo.sellonlatbox(
                        box['lon'].start, box['lon'].stop,
                        box['lat'].start, box['lat'].stop,
                        input=(' -sellevidx,'+str(box['vert0'])+'/'+
                               str(box['vert1'])+
                               #' -selname,'+var_dict[var_name]['key'] +
                               ' '+nco_file),
                        output=out_file)

            # delete tmp file
            bash_command = 'rm {}'.format(nco_file)
            process = subprocess.Popen(bash_command.split(),
                                        stdout=subprocess.PIPE)

        elif var_dict[var_name]['dim'] == '2D':
            bash_command = 'ncrcat -O -v {} {} {}'.format(
                            var_dict[var_name]['key'], inp_file,
                            out_file)
            process = subprocess.Popen(bash_command.split(),
                                        stdout=subprocess.PIPE)
            output, error = process.communicate()
        #    ofile = cdo.sellonlatbox(
        #                box['lon'].start, box['lon'].stop,
        #                box['lat'].start, box['lat'].stop,
        #                input=(nco_file),
        #                #input=(' -selname,'+var_dict[var_name]['key'] +
        #                #       ' '+inp_file),
        #                output=out_file)
        TM.stop('cdo')

    return(TM)


if __name__ == '__main__':

    # GENERAL SETTINGS
    ###########################################################################
    # input and output directories
    raw_data_dir = os.path.join('/project','pr04','heimc','data','cosmo_out')
    out_base_dir = os.path.join('/project','pr04','heimc','data','dyamond')

    # box to subselect
    box = domain
    #box.update({'vert0':40,'vert1':60}) # 3km top
    box.update({'vert0':32,'vert1':60}) # 6km top
    box['lon'] = slice(box['lon'].start - padding, box['lon'].stop + padding)
    box['lat'] = slice(box['lat'].start - padding, box['lat'].stop + padding)

    # name of model 
    model_name = 'COSMO'

    # variables to extract
    var_names = ['QV', 'QC', 'T', 'W',
                 'U10M', 'V10M', 'T2M', 'LWUTOA', 'SWDSFC',
                 'SLHFLX', 'SSHFLX', 'TQC', 'PP']
    var_names = ['SWDSFC']
    
    # model resolutions [km] of simulations
    ress = [12, 4.4]
    ress = [12]
    
    # date range
    first_date = datetime(2016,8,1)
    last_date = datetime(2016,8,2)

    # options for computation
    options = {}
    options['recompute']        = 0
    options['rm_tmp_folder']    = 0
    ###########################################################################


    # COSMO SPECIFIC SETTINGS
    ###########################################################################
    var_dict = {
        'QV'    :{'key':'QV',       'folder':'3h_3D',       'dim':'3D'}, 
        'QC'    :{'key':'QC',       'folder':'3h_3D',       'dim':'3D'}, 
        'T'     :{'key':'T',        'folder':'3h_3D',       'dim':'3D'}, 
        'W'     :{'key':'W',        'folder':'3h_3D',       'dim':'3D'}, 

        'U10M'  :{'key':'U_10M',    'folder':'1h_2D',       'dim':'2D'}, 
        'V10M'  :{'key':'V_10M',    'folder':'1h_2D',       'dim':'2D'}, 
        'T2M'   :{'key':'T_2M',     'folder':'1h_2D',       'dim':'2D'}, 
        'LWUTOA':{'key':'ATHB_T',   'folder':'1h_rad',      'dim':'2D'}, 
        'SWDSFC':{'key':'ASWD_S',   'folder':'1h_rad',      'dim':'2D'}, 
        'SLHFLX':{'key':'ALHFL_S',  'folder':'1h_2D',       'dim':'2D'}, 
        'SSHFLX':{'key':'ASHFL_S',  'folder':'1h_2D',       'dim':'2D'}, 
        'TQC'   :{'key':'TQC',      'folder':'15min_water', 'dim':'2D'}, 
        'PP'    :{'key':'TOT_PREC', 'folder':'15min_water', 'dim':'2D'}, 
    }
    inc_min = {'3h_3D':180, '1h_2D':60, '15min_water':15}

    model_dict = {
        12: 'c',
        4.4:'f',
    }

    sim_tag = 'SA_12_4'
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

        dt_range = np.arange(first_date, last_date,
                            timedelta(minutes=inc_min[
                            var_dict[var_name]['folder']])).tolist()

        for res in ress:
            print('############## res ' + str(res) + ' ##################')
            #res = 4

            sim_name = 'lm_' + model_dict[res]
            inp_dir	= os.path.join(raw_data_dir, sim_tag, sim_name,
                                   var_dict[var_name]['folder'],
                                   str(dt_range[0].year))

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
            args = []
            for dt in dt_range:
                inp_file = glob.glob(os.path.join(inp_dir,
                                        'lffd{:%Y%m%d%H%M%S}.nc'.format(dt)))[0]
                out_file = os.path.join(out_tmp_dir,
                            var_name+'_{:%Y%m%d%H%M}'.format(dt)+'.nc')

                args.append( (inp_file, out_file, dt, box, options,
                              var_name, res) )

            # run function serial or parallel
            if n_tasks > 1:
                with Pool(processes=n_tasks) as pool:
                    results = pool.starmap(sellatlon_COSMO, args)
            else:
                results = []
                for arg in args:
                    results.append(sellatlon_COSMO(*arg))

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
