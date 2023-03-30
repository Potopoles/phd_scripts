#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description:    Extract lat-lon box of data from model GEOS.
author:         Christoph Heim
date created:   09.07.2019
date changed:   06.09.2019
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

def sellatlon_GEOS(inp_file, out_file, dt, box, options, var_name, var_dict,
                   res):
    
    TM = Timer()
    file_code = '{}km_{}_{:%Y%m%d%H%M}'.format(res, var_name, dt)
    
    if os.path.exists(out_file) and not options['recompute']:
        TM.start('cdo')
        print('\t\t'+file_code+' already computed')
        TM.stop('cdo')
    else:
        print('\t\t'+file_code)

        # cdo
        TM.start('cdo')
        ofile = cdo.sellonlatbox(
                    box['lon'].start, box['lon'].stop,
                    box['lat'].start, box['lat'].stop,
                    input=(' -sellevidx,'+str(box['vert0'])+'/'+
                           str(box['vert1'])+
                           ' -selname,'+var_dict[var_name]['key']+
                           ' '+inp_file),
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
    #box.update({'vert0':1,'vert1':13}) # top 3km
    box.update({'vert0':1,'vert1':18}) # top 6km
    box['lon'] = slice(box['lon'].start - padding, box['lon'].stop + padding)
    box['lat'] = slice(box['lat'].start - padding, box['lat'].stop + padding)

    # name of model 
    model_name = 'GEOS'

    # variables to extract
    var_names = ['QV', 'QC', 'T', 'H', 'W',
                 'U10M', 'V10M', 'T2M', 'LWUTOA', 'SWDSFC',
                 'SLHFLX', 'SSHFLX', 'TQC', 'PPCONV', 'PPGRID', 'PPANVI']
    var_names = ['TQC', 'PPCONV', 'PPGRID', 'PPANVI']
    
    # model resolutions [km] of simulations
    ress = [3]
    
    # date range
    first_date = datetime(2016,8,11)
    last_date = datetime(2016,9,1)

    # options for computation
    options = {}
    options['recompute']        = 0
    options['rm_tmp_folder']    = 0
    ###########################################################################


    # GEOS SPECIFIC SETTINGS
    ###########################################################################
    var_dict = {
        'QV'    :{'file':'geosgcm_prog','key':'QV'}, 
        'QC'    :{'file':'geosgcm_prog','key':'QL'}, 
        'T'     :{'file':'geosgcm_prog','key':'T'}, 
        'H'     :{'file':'geosgcm_prog','key':'H'}, 
        'W'     :{'file':'geosgcm_prog','key':'W'}, 

        'U10M'  :{'file':'geosgcm_surf','key':'U10M'}, 
        'V10M'  :{'file':'geosgcm_surf','key':'V10M'}, 
        'T2M'   :{'file':'geosgcm_surf','key':'T2M'}, 
        'LWUTOA':{'file':'geosgcm_surf','key':'OLR'}, 
        'SWDSFC':{'file':'geosgcm_surf','key':'SWGDWN'}, 
        'SLHFLX':{'file':'geosgcm_surf','key':'LHFX'}, 
        'SSHFLX':{'file':'geosgcm_surf','key':'SHFX'}, 
        'TQC'   :{'file':'geosgcm_conv','key':'CWP'}, 
        'PPCONV':{'file':'geosgcm_surf','key':'CNPRCP'}, 
        'PPGRID':{'file':'geosgcm_surf','key':'LSPRCP'}, 
        'PPANVI':{'file':'geosgcm_surf','key':'ANPRCP'}, 
    }
    inc_min = {'geosgcm_prog':360, 'geosgcm_conv':15, 'geosgcm_surf':180}
    offset_min = {'geosgcm_prog':0, 'geosgcm_conv':0, 'geosgcm_surf':90}
    run_specif_name = '-MOM_NoDeepCu'
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

        dt_range = np.arange(first_date + timedelta(minutes=offset_min[
                            var_dict[var_name]['file']]),
                            last_date + timedelta(days=1),
                            timedelta(minutes=inc_min[
                            var_dict[var_name]['file']])).tolist()

        for res in ress:
            print('############## res ' + str(res) + ' ##################')

            sim_name = model_name + '-' + str(res) + 'km'+run_specif_name
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
            args = []
            for dt in dt_range:
                # execption, file that does not exist anymore
                if dt not in [datetime(2016,9,1,22,30),
                      datetime(2016,9,1,21,15),datetime(2016,9,1,21,30),
                      datetime(2016,9,1,21,45),datetime(2016,9,1,22,00),
                      datetime(2016,9,1,22,15),datetime(2016,9,1,22,30),
                      datetime(2016,9,1,22,45),datetime(2016,9,1,23,00),
                      datetime(2016,9,1,23,15),datetime(2016,9,1,23,30),
                      datetime(2016,9,1,23,45)]:
                    print(os.path.join(
                                        inp_dir,var_dict[var_name]['file'],
                                        '*{:%Y%m%d_%H%M}z.nc4'.format(dt)))
                    inp_file = glob.glob(os.path.join(
                                        inp_dir,var_dict[var_name]['file'],
                                        '*{:%Y%m%d_%H%M}z.nc4'.format(dt)))[0]
                    out_file = os.path.join(out_tmp_dir,
                                var_name+'_{:%Y%m%d%H%M}'.format(dt)+'.nc')
                    args.append( (inp_file, out_file, dt, box, options, var_name,
                                  var_dict, res) )

            # run function serial or parallel
            if n_tasks > 1:
                with Pool(processes=n_tasks) as pool:
                    results = pool.starmap(sellatlon_GEOS, args)
            else:
                results = []
                for arg in args:
                    results.append(sellatlon_GEOS(*arg))

            # collect timings from subtasks
            for task_TM in results:
                TM.merge_timings(task_TM)

            # merge all time step files to one
            TM.start('merge')
            cdo_mergetime(out_tmp_dir, out_dir, var_name)
            TM.stop('merge')

    TM.print_report()
