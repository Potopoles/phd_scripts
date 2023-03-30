#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    Test nc files for time step with missing values
author			Christoph Heim
date created    01.03.2020
date changed    20.03.2020
usage			no args
"""
###############################################################################
import os, glob, sys
import xarray as xr
import numpy as np
from package.nl_models import nlm
from package.utilities import dt64_to_dt
###############################################################################
sim_base_dir = os.path.join('/scratch/snx3000/heimc/data/simulations/')


var_names = ['U', 'V', 'W', 'T', 'H', 'P', 'QV', 'QC', 
             'U10M', 'V10M', 'T2M', 'PS', 'MSLP', 
             'LWUTOA', 'SWNDTOA', 'SWDTOA', 'SWUTOA',
             'SST', 'SLHFLX', 'SSHFLX',
             'CLCT', 'CLCT', 
             'TQC', 'TQI', 'TQV',
             'PP', 'PPCONV', 'PPGRID']

var_names = ['CLCT', 'CLCT', 
             'TQC', 'TQI', 'TQV',
             'PP', 'PPCONV', 'PPGRID']


tag = 'DYAMOND_2'
time_type = 'native'

mkey = sys.argv[2]
res = float(sys.argv[3])
skey = '{}_{:g}'.format(mkey, res)

print('RUNNING FOR {}'.format(skey))

for var_name in var_names:
    print('################# {} ##############'.format(var_name))

    sim_dir = os.path.join(sim_base_dir, skey, tag, time_type, var_name)
    if os.path.exists(sim_dir):
        files = os.listdir(sim_dir)
        last_nnan = 0
        #last_file_size = np.nan
        for file in files:
            print(file)
            file_path = os.path.join(sim_dir, file)

            # check for number of nans in file
            with xr.open_dataset(file_path) as ds:
                var = ds[nlm[mkey]['vkeys'][var_name]]
                times = ds.time
                for t in times:
                    #print(dt64_to_dt(t.values))
                    time_slice = var.sel(time=t).values
                    nnan = np.sum(np.isnan(time_slice))
                    ngp = 1
                    for dim in np.shape(var.values): ngp *= dim
                    mean_val = np.nanmean(time_slice)
                    #print('{:%Y%m%d%H%M}\t{}{:3.1f} % nan \t mean: {:6.2f}'.format(
                    #            dt64_to_dt(t.values), tab, nnan/ngp*100, mean_val))
                    if last_nnan != nnan:
                        error_string = \
                        '{:%Y%m%d%H%M}\t\t\t{:3.1f} % nan \t mean: {:8.4f}'.format(
                                dt64_to_dt(t.values), nnan/ngp*100, mean_val)
                        print(error_string)
                    last_nnan = nnan


    else:
        print('Skip {}. Does not exit.'.format(var_name))
