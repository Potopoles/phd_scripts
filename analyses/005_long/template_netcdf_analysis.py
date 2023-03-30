#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    Simple template script to read in some 2D netCDF data, perform
                an average and plot the result as a .jpg figure.
author			Christoph Heim
date created    20.05.2022
"""
###############################################################################
# system stuff for e.g. I/O
import os
# numpy for matrices
import numpy as np
# xarray for netcdf data
import xarray as xr
# pandas for smart data analysis
import pandas as pd
# plotting
import matplotlib.pyplot as plt
# for geographic plots
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
# handling of dates and time
from datetime import datetime, timedelta
# additional stuff for I/O
from pathlib import Path
##############################################################################

#### Namelist (all the user specified settings at the start of the code
####           separated from the rest of the code)
##############################################################################
# base directory where your analysis data is stored
data_base_dir = '/net/o3/hymet_nobackup/heimc/data/input/sample_data_fengge'

# path to the data of the model data you want to analyse 
# relative to the data base directy (example)
model_data = 'lm_f'

# first and last time step to analyse and frequency of time steps in between
ts_first = datetime(2015,8,1,0,0)
ts_last = datetime(2015,8,1,3,0)
ts_freq = '1H'

# netCDF variable name of variable to plot
plot_var_key = 'QV_2M'


# plot directory where you want to save your finished plots
plot_dir = '/net/o3/hymet_nobackup/heimc/plots/sample_plot_fengge'

# name of the plot
plot_name = 'test.jpg'



#### Load data and do computations
##############################################################################

# merge data_base_dir with model_key to one path pointing to the model data
model_data_dir = os.path.join(data_base_dir, model_data)

# for each file that should be opened, create an absolute path pointing
# to the file
tss = pd.date_range(ts_first, ts_last, freq=ts_freq)

# create file paths
file_paths = []
for ts in tss:
    file_paths.append(
        os.path.join(model_data_dir, 'lffd{:%Y%m%d%H%M%S}.nc'.format(ts))
    )

# Open multiple data files at once and merge along time dimension.
# Optionally you can also use xr.open_dataset() to open one file
# at a time and later merge them together. The first approach
# is simpler but the second is more robust and more perhaps more
# flexible.
ds = xr.open_mfdataset(paths=file_paths, concat_dim='time')

# select variable that should be plotted
var = ds[plot_var_key]
# print some information about varaible dimensions, coordinates and metadata
print(var)

# average in time
var = var.mean(dim='time')



#### Plot result
##############################################################################

# create figure object
fig = plt.figure(figsize=(5,3))

# add panel (axis) with geographic projection PlateCarree
ax = plt.axes(projection=ccrs.PlateCarree())

# add coastlines
ax.coastlines()

## format axes
ax.set_xticks(np.arange(40,66,5))
ax.set_yticks(np.arange(15,36,5))
lon_formatter = LongitudeFormatter(degree_symbol='°',
                                    dateline_direction_label=True)
ax.xaxis.set_major_formatter(lon_formatter)
lat_formatter = LatitudeFormatter(degree_symbol='°')
ax.yaxis.set_major_formatter(lat_formatter)


# plot variable as a contour plot
xr.plot.contourf(
    var,
    ax=ax,
    cmap='plasma_r',
)

# adjust axis labels
ax.set_xlabel('longitude')
ax.set_ylabel('latitude')

# set panel title
ax.set_title(plot_var_key)

# try to make margins look better automatically
# they can also be set manually
fig.tight_layout()


#### Show plot or save figure as jpg
##############################################################################
#plt.show()

# make sure the plot directory exists, else create it
Path(plot_dir).mkdir(parents=True, exist_ok=True)

# plot output path
plot_path = os.path.join(plot_dir, plot_name)

plt.savefig(plot_path)
