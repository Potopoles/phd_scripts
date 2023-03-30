#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     compute reynolds decomposed and averaged mean terms and
                turbulent flux components.
author			Christoph Heim
date created    02.09.2020
date changed    09.09.2020
usage           args:
                1st:    number of parallel tasks
                2nd:    model key
"""
###############################################################################
import os, glob, time
import numpy as np
import xarray as xr
from pathlib import Path
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import nl_07 as nl
from package.nl_models import nlm
from package.nl_variables import nlv,dimx,dimy,dimz,dimt
from package.var_pp import compute_variable, var_mapping
from package.utilities import (Timer, remap_member_for_date,
                            write_grid_des_file)
from package.mp import TimeStepMP
from package.functions import load_member_var
from package.nc_compression import (compress_date_conserving, find_minmax_val,
                                    compress_date_lossy)
###############################################################################

def create_links(ts, var_name, src_file, target_dir):
    target_file = os.path.join(target_dir,
                    '{}_{:%Y%m%d}.nc'.format(var_name, ts))
    if os.path.exists(target_file):
        os.remove(target_file)
    os.symlink(src_file, target_file)

def save_tmean_variable_as_tmean_and_daily(var_name, var,
                                    modres_key, mem_dict):
    # save time series under 'case'/tmean/'var_name'
    out_base_dir = os.path.join(nl.ana_base_dir, 'native_grid')
    out_path = os.path.join(out_base_dir, modres_key,
                            mem_dict['case'], 'tmean',
                            '{}_tmean'.format(var_name))
    Path(out_path).mkdir(parents=True, exist_ok=True)
    out_file = os.path.join(out_path,
                    '{}_tmean_{:%Y%m%d}_{:%Y%m%d}.nc'.format(
                    var_name, nl.first_date, nl.last_date))
    var.to_netcdf(out_file)

    # link mean file to daily files
    dates = np.arange(nl.first_date, nl.last_date+timedelta(days=1),
                      timedelta(days=1)).tolist()
    tsmp = TimeStepMP(dates, njobs=nl.njobs, run_async=True)
    target_dir = os.path.join(out_base_dir, modres_key,
                            mem_dict['case'], 'daily',
                            '{}'.format(var_name))
    Path(target_dir).mkdir(parents=True, exist_ok=True)
    fargs = {'var_name':var_name, 
            'src_file':out_file,
            'target_dir':target_dir}
    tsmp.run(create_links, fargs=fargs, step_args=None)


if __name__ == '__main__':

    ###########################################################################
    # PREPARATION STEPS
    timer = Timer(mode='seconds')
    Path(nl.ana_base_dir).mkdir(parents=True, exist_ok=True)

    ###########################################################################
    # COMPUTE MEAN TERM
    for mem_key,mem_dict in nl.sim_src_dict.items():
        #mem_key = nl.use_sim_key
        #mem_dict = nl.use_sims[mem_key]
        print('####### {} ########'.format(mem_key))
        mod_key = mem_dict['mod']
        modres_key =  '{}_{:g}'.format(mem_dict['mod'], mem_dict['res'])

        # load mean variables
        tmean = {}
        for var_name in ['W', 'POTT', 'U', 'V', 'INVHGT']:
            var_name_tmean = '{}_tmean'.format(var_name)
            tmean[var_name] = load_member_var(var_name_tmean, nl.first_date,
                                    nl.last_date, mem_dict,
                                    nl.var_src_dict,
                                    nl.var_src_dict[var_name_tmean]['load'],
                                    domain=nl.domain, i_debug=nl.i_debug)

        tmean['POTTVDIV'] = compute_variable('POTTVDIV', mod_key, tmean)
        tmean['POTTHDIV'] = compute_variable('POTTHDIV', mod_key, tmean)


        # ABSOLUTE HEIGHT
        var_name = 'POTTHDIVMEAN'
        tmean[var_name] = compute_variable(var_name, mod_key, tmean)
        save_tmean_variable_as_tmean_and_daily(var_name, tmean[var_name],
                                        modres_key, mem_dict)
        var_name = 'POTTVDIVMEAN'
        tmean[var_name] = compute_variable(var_name, mod_key, tmean)
        save_tmean_variable_as_tmean_and_daily(var_name, tmean[var_name],
                                        modres_key, mem_dict)
        var_name = 'POTTDIVMEAN'
        tmean[var_name]   = compute_variable(var_name, mod_key, tmean)
        save_tmean_variable_as_tmean_and_daily(var_name, tmean[var_name],
                                        modres_key, mem_dict)
        var_name = 'WMEAN'
        tmean[var_name]   = compute_variable(var_name, mod_key, tmean)
        save_tmean_variable_as_tmean_and_daily(var_name, tmean[var_name],
                                        modres_key, mem_dict)


        # RELATIVE HEIGHT
        var_name = 'POTTHDIVMEANNORMI'
        tmean[var_name] = compute_variable(var_name, mod_key, tmean)
        save_tmean_variable_as_tmean_and_daily(var_name, tmean[var_name],
                                        modres_key, mem_dict)
        var_name = 'POTTVDIVMEANNORMI'
        tmean[var_name] = compute_variable(var_name, mod_key, tmean)
        save_tmean_variable_as_tmean_and_daily(var_name, tmean[var_name],
                                        modres_key, mem_dict)
        var_name = 'POTTDIVMEANNORMI'
        tmean[var_name] = compute_variable(var_name, mod_key, tmean)
        save_tmean_variable_as_tmean_and_daily(var_name, tmean[var_name],
                                        modres_key, mem_dict)


        #tmean['DIABH'] = tmean['DIABH'].mean(dim=['lon','lat'])
        #plt.plot(tmean['DIABH'], tmean['DIABH'].alt)
        #plt.show()
        #quit()

    timer.print_report()
