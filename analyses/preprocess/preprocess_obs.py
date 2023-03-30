#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     
author			Christoph Heim
date created    10.02.2020 
date changed    04.07.2022
usage           no args:
"""
###############################################################################
import os, glob, collections, subprocess
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import nl_preprocess_obs as nl
from base.nl_domains import dom_meteosat_disk, point_st_helena
from package.utilities import Timer, dt64_to_dt, write_grid_des_file, cdo_remap
from package.functions import time_periods_to_dates
from package.var_pp import compute_variable
from package.obs_pp import (pp_DARDAR_CLOUD,
                            pp_CORREFL_tiff_to_nc,
                            pp_preproc_radio_sounding,
                            pp_CMORPH)
from package.mp import TimeStepMP
###############################################################################


def _run_remap_CM_SAF_MSG_AQUA_TERRA(ts, inp_base_dir, out_base_dir):
    date = ts
    inp_file = os.path.join(inp_base_dir, '{}_{:%Y%m%d}.nc'.format(
                            nl.args.var_name, date))
    if os.path.exists(inp_file):
        out_file = os.path.join(out_base_dir, '{}_{:%Y%m%d}.nc'.format(
                            nl.args.var_name, date))
        tmp_out_file = os.path.join(out_base_dir, '{}_{:%Y%m%d}.nc.tmp'.format(
                            nl.args.var_name, date))
        cdo_remap(grid_des_file, inp_file, tmp_out_file, method='bil')
        # time stamps are bad in CM SAF monthly data
        command = "cdo -settaxis,{:%Y-%m}-16,00:00:00,1day {} {}".format(date, tmp_out_file, out_file)
        ## alternative for CM SAF daily data
        #command = "mv {} {}".format(tmp_out_file, out_file)
        subprocess.run(command, shell=True)

    else:
        print('file {} does not exist.'.format(inp_file))

if __name__ == '__main__':
    timer = Timer(mode='seconds')

    ### TODO: not all scripts use dates, some just process all the data
    dates = time_periods_to_dates(nl.time_periods)
    tsmp = TimeStepMP(dates, njobs=nl.args.n_par, run_async=True)

    ###########################################################################
    # REMAP CM SAF MSG AQUA TERRA DATA from sinusoidal projection to lon lat
    if nl.args.var_name in ['LWUTOA', 'SWUTOA', 'SWDTOA']:
        grid_des_file = os.path.join(nl.use_obs[nl.args.var_name]['obs_dir'],
                                    'grid_des.txt')
        write_grid_des_file(dom_meteosat_disk, grid_des_file, 45, padding=0)

        # expects daily files named with in format VARNAME_YYYYMMDD.nc
        inp_base_dir = os.path.join(nl.use_obs[nl.args.var_name]['raw_dir'])
        out_base_dir = os.path.join(nl.use_obs[nl.args.var_name]['obs_dir'],
                            #'MSG', dom_meteosat_disk['key'], 'daily',
                            'MSG', dom_meteosat_disk['key'], 'monthly',
                            nl.args.var_name)
        Path(out_base_dir).mkdir(parents=True, exist_ok=True)
        fargs = {'out_base_dir':out_base_dir,
                 'inp_base_dir':inp_base_dir}
        tsmp.run(_run_remap_CM_SAF_MSG_AQUA_TERRA, fargs=fargs, step_args=None)


    ###########################################################################
    # PROCESS DARDAR DATA
    if nl.args.var_name in ['CLDMASK', 'T']:

        fargs = {'raw_dir':nl.use_obs[nl.args.var_name]['raw_dir'],
                 'domain':nl.domain,
                 'out_base_dir':nl.use_obs[nl.args.var_name]['obs_dir'],
                 'var_name':nl.args.var_name}
        tsmp.run(pp_DARDAR_CLOUD, fargs=fargs, step_args=None)
        

    ###########################################################################
    # PREPROCESS CORREFL FROM VIIRS ON SUOMI NPP
    if nl.args.var_name == 'CORREFL':
        case = 'SA'
        
        tiff_dir = os.path.join(nl.obs_base_dir, nl.use_obs[nl.var_name]['obs'],
                                'raw_data', case)
        nc_dir = os.path.join(nl.obs_base_dir, nl.use_obs[nl.var_name]['obs'],
                                case, 'daily', nl.var_name)
        Path(nc_dir).mkdir(parents=True, exist_ok=True)
        pp_CORREFL_tiff_to_nc(tiff_dir, nc_dir, i_aggregate_rgb=1)
        

    ###########################################################################
    # PREPROCESS PP FROM CMORPH
    if nl.args.var_name == 'PP':
        raw_dir = os.path.join(nl.use_obs[nl.args.var_name]['raw_dir'])
        out_dir = os.path.join(nl.use_obs[nl.args.var_name]['obs_dir'])
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        fargs = {'raw_dir':raw_dir,
                 'out_dir':out_dir,
                }
        tsmp.run(pp_CMORPH, fargs=fargs, step_args=None)

    #elif nl.args.var_name in ['RH','T']:
    #    timer.start('all')
    #    case = 'ST_HELENA'
    #    time_str = '20140801_20140910'

    #    raw_inp_file = os.path.join(nl.inp_base_dir, nl.use_obs[nl.var_name]['obs'],
    #                                'raw_data', case, nl.var_name,
    #                                'radio_sthel_{}.txt'.format(time_str))
    #    sounding = pp_preproc_radio_sounding(raw_inp_file, nl.var_name, n_lowest=27)
    #    #sounding = sounding.expand_dims(lon=[point_st_helena['lon']],
    #    #                                lat=[point_st_helena['lat']])
    #    #sounding = sounding.to_dataset(name='T')
    #    nc_dir = os.path.join(nl.inp_base_dir, nl.use_obs[nl.var_name]['obs'],
    #                          case ,'daily', nl.var_name)
    #    Path(nc_dir).mkdir(parents=True, exist_ok=True)
    #    for dt64 in sounding.time.values:
    #        dt = dt64_to_dt(dt64)
    #        this_day = sounding.sel(time=dt)
    #        this_day = this_day.expand_dims(time=[dt])
    #        out_file = os.path.join(nc_dir, 'T_{:%Y%m%d}.nc'.format(dt))
    #        this_day.to_netcdf(out_file, 'w')

    #    timer.stop('all')


    timer.print_report()






    #obs_file = os.path.join(nl.obs_base_dir, 'aqua', 'test.hdf')
    #import Nio
    #obs_hdf = Nio.open_file(obs_file)
    #lat = obs_hdf.variables['Latitude']
    #lon = obs_hdf.variables['Longitude']
    #time = obs_hdf.variables['Scan_Start_Time']
    #TQC = obs_hdf.variables['Cloud_Water_Path']
    #print(lat)
    #print(lon)
    #print(time)
    #lat = lat[:]
    #lon = lon[:]
    #lon = lon[:]
    
