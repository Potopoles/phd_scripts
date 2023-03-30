#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Preprocess observation data sets while loading. Do stuff
                specific to each data set and the analysis.
author			Christoph Heim
date created    13.02.2020
date changed    05.05.2022
usage           no args
"""
###############################################################################
import os, re, glob, copy, subprocess
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime, timedelta
from scipy.interpolate import interp1d
from package.utilities import cdo_remap
#import Nio
#import rasterio as rio
###############################################################################


def pp_DARDAR_CLOUD(ts, raw_dir, domain, out_base_dir, var_name):
    print(ts)
    date = ts

    # range of vertical indices to select in DARDAR data set
    vert_inds = (318,-18) # 0-6.0km
    vert_inds = (343,-18) # 0-4.5km
    vert_inds = (368,-18) # 0-3.0km

    ### set up variable template
    #glon = np.arange(domain['lon'].start, domain['lon'].stop + res_hori, res_hori)
    #glat = np.arange(domain['lat'].start, domain['lat'].stop + res_hori, res_hori)
    #time = pd.date_range("2007-01-01 03:00", periods=8, freq="3h")
    #reference_time = pd.Timestamp("2007-01-01")

    #nentries = xr.Dataset(
    #        data_vars = dict(
    #            nentries=(['lat', 'lon'], 
    #            np.zeros((len(glat),len(glon))))
    #        ),
    #        coords = dict(
    #            lat = (['lat'], glat),
    #            lon = (['lon'], glon),
    #        )
    #        #)
    #    )

    entry_counter = 0

    raw_date_dir = os.path.join(raw_dir, '{:%Y_%m_%d}'.format(date))
    date_files = glob.glob(os.path.join(raw_date_dir, '*.hdf'))

    for file_path in date_files:

        try:
            hdf = Nio.open_file(file_path)
        except Nio.NIOError:
            print('Could not load file {}'.format(file_path))
            continue
        #print(hdf.variables.keys())
        if var_name == 'CLDMASK':
            var = hdf.variables[
                        'DARMASK_Simplified_Categorization'][:,vert_inds[0]:vert_inds[1]]
            var = var.filled(0)
        elif var_name == 'T':
            var = hdf.variables[
                        'temperature'][:,vert_inds[0]:vert_inds[1]]
        else:
            raise NotImplementedError()
        lon = np.round(hdf.variables['longitude'][:], 4)
        lat = np.round(hdf.variables['latitude'][:], 4)
        alt = np.round(hdf.variables['height'][vert_inds[0]:vert_inds[1]],0)
        time = hdf.variables['time'][:]

        ### subselect inside domain
        use_mask = np.repeat(True, len(lon))

        use_mask[lon < domain['lon'].start] = False
        use_mask[lon > domain['lon'].stop] = False
        use_mask[lat < domain['lat'].start] = False
        use_mask[lat > domain['lat'].stop] = False

        time = time[use_mask]
        lon = lon[use_mask]
        lat = lat[use_mask]
        var = var[use_mask,:]

        if np.sum(use_mask) > 0:

            # convert second timestamp to datetime
            time = pd.to_datetime(
                    [date+timedelta(milliseconds=int(1000*sec)) for sec in time])
            loc = np.arange(len(time)) + entry_counter

            if var_name == 'CLDMASK':
                ### adjust categories
                #val_cloud = 3
                #val_no_cloud = 0
                #val_unknown = 1
                #val_rain = 2
                #cloudrainmask = var.copy()
                #cloudrainmask[cloudrainmask == -9] = val_no_cloud # ground
                #cloudrainmask[cloudrainmask == -1] = val_unknown # don't know
                #cloudrainmask[cloudrainmask ==  1] = val_no_cloud # ice
                #cloudrainmask[cloudrainmask ==  2] = val_no_cloud # ice & supercooled
                #cloudrainmask[cloudrainmask ==  3] = val_cloud # liquid warm
                #cloudrainmask[cloudrainmask ==  4] = val_no_cloud # supercooled
                #cloudrainmask[cloudrainmask ==  5] = val_rain # rain
                #cloudrainmask[cloudrainmask ==  6] = val_no_cloud # aerosol
                #cloudrainmask[cloudrainmask ==  7] = val_unknown # maybe insects
                #cloudrainmask[cloudrainmask ==  8] = val_unknown # stratospheric feature

                #### simplified categories
                ## rain
                #rainmask = var.copy()
                #rainmask[rainmask != 5] = 0
                #rainmask[rainmask == 5] = 1

                # liquid cloud
                cloudmask = var.copy()
                cloudmask[cloudmask != 3] = 0
                cloudmask[cloudmask == 3] = 1

                ## for now add rainmask to cloudmask
                #cloudmask[rainmask == 1] = 1

                out_var = cloudmask

            ds = xr.Dataset(
                    data_vars = { 
                        var_name:(['time', 'alt'], out_var),
                        'lat':(['time'], lat),
                        'lon':(['time'], lon),
                    },
                    coords = dict(
                        time = (['time'], time),
                        alt = (['alt'], alt),
                    )
                )

            if entry_counter == 0:
                full_ds = copy.deepcopy(ds)
            else:
                full_ds = xr.concat([full_ds, ds], dim='time')
                #print(full_ds)

            # increase entry counter
            entry_counter += len(time)


            #### determine cloud top
            #cloud_top_ind = np.argmax(cloudmask, axis=1)
            #cloud_top = np.take(alt, cloud_top_ind)
            #cloud_top += 30
            #cloud_top[cloud_top_ind == 0] = np.nan
            #### determine cloud base
            #cloud_base_ind = np.argmax(np.flip(cloudmask, axis=1), axis=1)
            #cloud_base = np.take(np.flip(alt), cloud_base_ind)
            #cloud_base -= 30
            #cloud_base[cloud_base_ind == 0] = np.nan
            ## for now, remove cloud base for rainy clouds
            #has_rain = np.any(rainmask, axis=1)
            #cloud_base[has_rain] = np.nan

            ###plot_ax = loc
            ###plot_ax = lon
            #plot_ax = lat
            ##plot_ax = time
            #plt.pcolormesh(plot_ax, alt, cloudmask.T)
            #plt.plot(plot_ax, cloud_top)
            ###plt.plot(plot_ax, cloud_base)
            #plt.colorbar()
            #plt.show()
            #quit()

            #print(np.unique(np.diff(lon)))
            #print(np.unique(np.diff(lat)))
            #quit()

            #from scipy.interpolate import griddata
            #GLON, GLAT = np.meshgrid(glon, glat)
            ##int = griddata((lon,lat), cloud_top, (GLON,GLAT), method='linear')  
            #int = griddata((lon,lat), np.ones(len(lon)),
            #                (GLON,GLAT), method='linear') 
            #int[np.isnan(int)] = 0
            #
            #data = xr.Dataset(
            #        data_vars = dict(
            #            nentries=(['lat', 'lon'], int)
            #        ),
            #        coords = dict(
            #            lat = (['lat'], glat),
            #            lon = (['lon'], glon),
            #        )
            #        #)
            #    )


    out_path = os.path.join(out_base_dir, 'DARDAR_CLOUD', domain['key'],
                            'daily', var_name)
    Path(out_path).mkdir(exist_ok=True, parents=True)
    out_file = os.path.join(out_path,
                            '{}_{:%Y%m%d}.nc'.format(var_name, date))
    
    #plt.plot(full_ds.CLDMASK.mean(dim='time'), full_ds.alt)
    #plt.show()
    #quit()

    try:
        full_ds.to_netcdf(out_file, unlimited_dims=['time'])#,
                        #encoding={
                        #    'time':{
                        #        'units':'milliseconds since 2006-08-01',
                        #        #'units':'seconds since 2007-01-01',
                        #        'dtype':'int32'
                        #    },
                        #})
    except UnboundLocalError:
        pass


    #full_ds = full_ds.mean(dim='loc')
    #plt.plot(full_ds.CLDMASK, full_ds.alt)
    #plt.show()
    #quit()
    #nentries.to_netcdf('data_test.nc')


def pp_CORREFL_tiff_to_nc(tiff_dir, nc_dir, i_aggregate_rgb=0):
    dates = [datetime.strptime(file[9:19], '%Y-%m-%d') \
                for file in os.listdir(tiff_dir)]
    dates.sort()

    for dtI,dt in enumerate(dates):
        print(dt)
        nc_dt = dt + timedelta(hours=12)
        img_name = 'snapshot-{:%Y-%m-%d}T00_00_00Z.tiff'.format(dt)

        sat_tiff =  rio.open(os.path.join(tiff_dir,img_name))
        nx = sat_tiff.meta['width']
        ny = sat_tiff.meta['height']
        dx = sat_tiff.res[0]
        dy = sat_tiff.res[1]
        lons = np.arange(sat_tiff.bounds.left,
                         sat_tiff.bounds.right - dx/2, dx)
        lats = np.arange(sat_tiff.bounds.bottom,
                         sat_tiff.bounds.top - dy/2, dy)
        data = sat_tiff.read()

        ## THIS IS NOT NECESSARY FOR VIIRS BECAUSE IT DOES NOT HAVE
        ## GAPS. MODIS DOES.
        ## set entries with sum(rgb) == 0 to np.nan
        ## this gives an approximate satellite coverage mask
        ## approx. because there might be some few areas with natural 0 rgb.
        #data = data.astype(np.float)
        #data = np.flip(data, axis=1)
        #mask = np.sum(data, axis=0) == 0
        #for r in range(3):
        #    data[r,:,:][mask] = np.nan
        #data = np.expand_dims(data, axis=0)

        data = data.astype(np.float)
        data = np.flip(data, axis=1)
        ## convert RGB 8 bit to 0-1.
        for r in range(3):
            data[r,:,:] /= 255
        data = np.expand_dims(data, axis=0)

        if i_aggregate_rgb:
            data = data.mean(1)
            data = xr.DataArray(data, coords={'time':[nc_dt], 
                                'lat':lats,'lon':lons},
                                dims=['time', 'lat','lon'],
                                name='CORREFL')
            # coarse grain array to 2km x 2km
            data = data.coarsen(lon=2, lat=2).mean()
            data = data.rename('CORREFL')
        else:
            data = xr.DataArray(data, coords={'time':[nc_dt], 
                                'rgb':['r','g','b'],'lat':lats,'lon':lons},
                                dims=['time', 'rgb','lat','lon'],
                                name='CORREFL')

        out_file = os.path.join(nc_dir, 'CORREFL_{:%Y%m%d}.nc'.format(dt))
        data.to_netcdf(out_file, 'w')



def pp_preprocess_radio_sounding_day(dt, hght, pres, temp, dpd, wdir, wind):
    # finalize day array
    for numb in [-9999, -8888]:
        hght[hght == numb] = np.nan
        temp[temp == numb] = np.nan
        dpd[dpd == numb] = np.nan
        wdir[wdir == numb] = np.nan
        wind[wind == numb] = np.nan

    #inds_temp = np.argwhere(~np.isnan(temp) & ~np.isnan(dpd))
    #print(inds_temp)
    # convert variables
    # temperature to temperature
    temp = temp/10 + 273.15
    # dew point depression to qv
    dpd = dpd/10 + 273.15
    # wind speed
    wind = wind/10
    # store in dict
    this_day = {
        'date'  :dt,
        'pres'  :pres,
        'hght'  :hght,
        'temp'  :temp,
        'dpd'   :dpd,
        'wdir'  :wdir,
        'wind'  :wind,
    }      
    return(this_day)

#def pp_radio_sounding_compute_user_vars(this_day):
#    if var_name == 'RH':
#        print('RH')
#    return(this_day)

def pp_preproc_radio_sounding(raw_inp_file, var_name, n_lowest):
    """
    """
    lon=-5.6672,
    lat=-15.9419,
    line_inds = {
        'pres':slice(9,15), # pressure
        'hght':slice(16,21), # height
        'temp':slice(22,27), # air temperature
        #'relh':slice(28,33), # not in data set (use dpd).
        'dpd':slice(34,39), # dew point depression
        'wdir':slice(40,45), # wind direction
        'wind':slice(46,51), # wind speed
    }

    # READ DATA FROM FILE
    with open(raw_inp_file, 'r') as f:
        raw_in = f.readlines()
    day_data = []
    c = 0
    for line in raw_in:
        split = re.split(r'\s+', line)
        # new day
        if split[0][0] == '#':
            try:
                day_data.append(pp_preprocess_radio_sounding_day(dt, hght, pres,
                            temp, dpd, wdir, wind))
            # on first day none exists
            except UnboundLocalError:
                pass
            dt = datetime(int(split[1]), int(split[2]), int(split[3]), int(split[4]))
            nlev    = int(split[6])
            pres    = np.zeros(nlev)
            hght    = np.zeros(nlev)
            temp    = np.zeros(nlev)
            dpd     = np.zeros(nlev)
            wdir    = np.zeros(nlev)
            wind    = np.zeros(nlev)
            i = 0
        # next level of same day
        else:
            pres[i] = float(line[line_inds['pres']])
            hght[i] = float(line[line_inds['hght']])
            temp[i] = float(line[line_inds['temp']])
            dpd[i]  = float(line[line_inds['dpd']])
            wdir[i] = float(line[line_inds['wdir']])
            wind[i] = float(line[line_inds['wind']])
            i += 1
    day_data.append(pp_preprocess_radio_sounding_day(dt, hght, pres, temp, dpd,
                                                    wdir, wind))
    #for dd in day_data:
    #    print(dd['date'])
    #print(len(day_data))
    #quit()

    # INTERPOLATE DATA ONTO CONSTANT Z GRID
    type_vnames = {'TEMP':['pres', 'temp', 'dpd'], 'WIND':['pres', 'wdir', 'wind']}
    type_vars = {}
    for type,vnames in type_vnames.items():
        type_vars[type] = {} 
        for vname in vnames:
            type_vars[type][vname] = np.zeros((n_lowest,len(day_data)))
    type_hgts = {'TEMP':np.zeros((n_lowest,len(day_data))),
                 'WIND':np.zeros((n_lowest,len(day_data)))}
    dates = []
    for dI in range(len(day_data)):
        #print(dI)
        dayd = day_data[dI]
        dates.append(dayd['date'])
        # get match between p and h on significant levels
        inds = np.argwhere(~np.isnan(dayd['hght']))
        p_ref = dayd['pres'][inds].squeeze()
        h_ref = dayd['hght'][inds].squeeze()
        # get values on all levels (also non-significant)
        type_inds = {}
        type_inds['TEMP'] = np.argwhere(~np.isnan(dayd['temp']) & ~np.isnan(dayd['dpd']))
        type_inds['WIND'] = np.argwhere(~np.isnan(dayd['wdir']) & ~np.isnan(dayd['wind']))
        for type in ['TEMP', 'WIND']:
            inds = type_inds[type]
            p = dayd['pres'][inds].squeeze()
            # logarithmically interpolate (and extrapolate) height 
            # for all levels based on significant levels
            interp = interp1d(np.log10(p_ref), np.log10(h_ref), fill_value='extrapolate')
            h = 10**interp(np.log10(p))
            # return n_lowest levels
            type_hgts[type][:,dI] = h[:n_lowest]
            for vkey in type_vars[type]:
                var = dayd[vkey][inds].squeeze()
                type_vars[type][vkey][:,dI] = var[:n_lowest]


    # compute specific var_names (user input) variables.
    if var_name == 'T':
        type = 'TEMP'
        var = type_vars[type]['temp']
    pvar = type_vars[type]['pres']

    # APPROXIMATION: average height for all days over time to get one
    # vertical grid for all days
    h_mean = np.mean(type_hgts[type], axis=1)

    var = np.expand_dims(np.expand_dims(var.T, 2),3)
    pvar = np.expand_dims(np.expand_dims(pvar.T, 2),3)
    var_xr = xr.DataArray(var, coords=[dates, h_mean,
                                np.asarray(lat), np.asarray(lon)],
                        dims=['time', 'alt', 'lat', 'lon'], name=var_name)
    p_xr = xr.DataArray(pvar, coords=[dates, h_mean,
                                np.asarray(lat), np.asarray(lon)],
                        dims=['time', 'alt', 'lat', 'lon'], name=var_name)
    sounding = xr.Dataset({var_name:var_xr, 'P':p_xr})

    #test = sounding.isel(time=0)
    #import matplotlib.pyplot as plt
    #plt.plot(test[var_name], test.alt)
    #plt.show()
    #quit()
    #quit()
    return(sounding)


def pp_CMORPH(ts, raw_dir, out_dir):
    print(ts)
    print(raw_dir)
    print(out_dir)
    inp_file = os.path.join(raw_dir, 
        '{:%Y}'.format(ts), 
        '{:%m}'.format(ts), 
        'CMORPH_V1.0_ADJ_0.25deg-DLY_00Z_{:%Y%m%d}.nc'.format(ts)
    )
    out_file = os.path.join(out_dir, 'PP_{:%Y%m%d}.nc'.format(ts))
    bash_command = 'cdo sellonlatbox,{},{},{},{} {} {}'.format(
        -56,29,-39,26, inp_file, out_file)
    process = subprocess.Popen(bash_command.split(),
                                stdout=subprocess.PIPE)
    output, error = process.communicate()
