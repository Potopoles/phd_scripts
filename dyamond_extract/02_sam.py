#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description:    Extract lat-lon box of data from model SAM.
author:         Christoph Heim
date created:   20.06.2019
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

def sellatlon_SAM(inp_file, out_file, dt, box, options, var_name, res):
    
    TM = Timer()

    file_code = '{}km_{}_{:%Y%m%d%H%M}'.format(res, var_name, dt)
    
    if os.path.exists(out_file) and not options['recompute']:
        TM.start('nco')
        TM.start('cdo')
        print('\t\t'+file_code+' already computed')
        TM.stop('nco')
        TM.stop('cdo')
    else:
        print('\t\t'+file_code)

        split = os.path.split(out_file)
        nco_file = os.path.join(split[0],'nco_'+split[1])

        # nco
        if not os.path.exists(nco_file):
            TM.start('nco')
            bash_command = ('ncatted -O -a units,lon,o,c,degrees_east ' + 
                            '-a units,lat,o,c,degrees_north '+inp_file+
                            ' '+nco_file)
            process = subprocess.Popen(bash_command.split(),
                                        stdout=subprocess.PIPE)
            output, error = process.communicate()
            TM.stop('nco')
        else:
            TM.start('nco')
            TM.stop('nco')

        # cdo
        TM.start('cdo')
        if var_dict[var_name]['loc'] == 'OUT_3D':
            time_fmt = '{:%Y-%m-%d,%H:%M:%S,3hour}'
        elif var_dict[var_name]['loc'] == 'OUT_2D':
            time_fmt = '{:%Y-%m-%d,%H:%M:%S,30min}'
        ofile = cdo.sellonlatbox(
                    box['lon'].start,box['lon'].stop,
                    box['lat'].start,box['lat'].stop,
                    input=('-sellevidx,'+str(box['vert0'])+'/'+
                           str(box['vert1'])+
                           ' -setreftime,2016-08-01,00:00:00,minutes'+
                           ' -settaxis,'+time_fmt.format(dt)+
                           ' '+nco_file),
                    output=out_file)
        TM.stop('cdo')

        # delete tmp_file
        if options['rm_tmp_files']:
            os.remove(nco_file)

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
    #box.update({'vert0':1,'vert1':28}) #3km
    box.update({'vert0':1,'vert1':35}) #6km
    box['lon'] = slice(box['lon'].start - padding, box['lon'].stop + padding)
    box['lat'] = slice(box['lat'].start - padding, box['lat'].stop + padding)

    # name of model 
    model_name = 'SAM'

    # variables to extract
    var_names = ['QV', 'QC', 'T', 'W',
                 'U10M', 'V10M', 'T2M',
                 'LWUTOA', 'SWDSFC',
                 'SLHFLX', 'SSHFLX', 'TQC', 'PP']
    
    # model resolutions [km] of simulations
    ress = [4]
    
    # date range
    first_date = datetime(2016,8,11)
    last_date = datetime(2016,9,9)

    # options for computation
    options = {}
    options['recompute']        = 0
    options['rm_tmp_files']     = 1
    options['rm_tmp_folder']    = 0
    ###########################################################################


    # SAM SPECIFIC SETTINGS
    ###########################################################################
    var_dict = {
        'QV'    :{'file':'QV',
                  'loc':'OUT_3D','fntime':(-16,-6),}, 
        'QC'    :{'file':'QC',
                  'loc':'OUT_3D','fntime':(-16,-6),}, 
        'T'     :{'file':'TABS',
                  'loc':'OUT_3D','fntime':(-18,-8),}, 
        'W'     :{'file':'W',
                  'loc':'OUT_3D','fntime':(-15,-5),}, 

        'U10M'  :{'file':'U10m',
                  'loc':'OUT_2D','fntime':(-21,-11),}, 
        'V10M'  :{'file':'V10m',
                  'loc':'OUT_2D','fntime':(-21,-11),}, 
        'T2M'   :{'file':'T2mm',
                  'loc':'OUT_2D','fntime':(-21,-11),}, 
        'LWUTOA':{'file':'LWNTA',
                  'loc':'OUT_2D','fntime':(-22,-12),}, 
        'SWDSFC':{'file':'SWDSA',
                  'loc':'OUT_2D','fntime':(-22,-12),}, 
        'SLHFLX':{'file':'LHF',
                  'loc':'OUT_2D','fntime':(-20,-10),}, 
        'SSHFLX':{'file':'SHF',
                  'loc':'OUT_2D','fntime':(-20,-10),}, 
        'TQC'   :{'file':'CWP',
                  'loc':'OUT_2D','fntime':(-20,-10),}, 
        'PP'    :{'file':'Precac',
                  'loc':'OUT_2D','fntime':(-23,-13),}, 
    }


    dt = 7.5
    base_time = datetime(2016,8,1)
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
        for res in ress:
            print('############## res ' + str(res) + ' ##################')

            sim_name = model_name + '-' + str(res) + 'km'
            inp_dir	= os.path.join(raw_data_dir, sim_name,
                                   var_dict[var_name]['loc'])
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
            if var_dict[var_name]['loc'] == 'OUT_3D':
                inp_files_glob = glob.glob(os.path.join(inp_dir,
                                    '*_'+var_dict[var_name]['file']+'.nc'))
            elif var_dict[var_name]['loc'] == 'OUT_2D':
                inp_files_glob = glob.glob(os.path.join(inp_dir,
                                    '*'+var_dict[var_name]['file']+'*.nc'))

            times = [base_time + timedelta(seconds=dt*int(
                        f[var_dict[var_name]['fntime'][0]:
                          var_dict[var_name]['fntime'][1]])) 
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
                              options, var_name, res) )

            # run function serial or parallel
            if n_tasks > 1:
                with Pool(processes=n_tasks) as pool:
                    results = pool.starmap(sellatlon_SAM, args)
            else:
                results = []
                for arg in args:
                    results.append(sellatlon_SAM(*arg))

            # collect timings from subtasks
            for task_TM in results:
                TM.merge_timings(task_TM)

            TM.start('merge')
            # merge all time step files to one
            cdo_mergetime(out_tmp_dir, out_dir, var_name)
            TM.stop('merge')

    TM.print_report()
