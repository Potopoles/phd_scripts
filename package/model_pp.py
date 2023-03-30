#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Preprocess model data while loading. Do model specific
                stuff.
author			Christoph Heim
date created    09.07.2019
date changed    28.04.2022
usage           no args
"""
###############################################################################
import os, copy, warnings, random
import numpy as np
import xarray as xr
from scipy.interpolate import interp1d
from datetime import datetime, timedelta
from numba import jit, njit
from package.nl_models import nlm, models_cmip6
from package.nl_variables import (nlv, add_var_attributes,
                                  dimx,dimy,dimz,dimt)
from package.utilities import (dt64_to_dt, subsel_domain, 
                                select_common_timesteps, Timer)
from base.nl_global import inp_glob_base_dir, model_specifics_path
from package.constants import CON_G, CON_RD
###############################################################################

MODEL_PP        = 'model_pp'
MODEL_PP_DONE   = 'done'

inp_base_dir = inp_glob_base_dir

debug_level_2 = 2
debug_level_4 = 4


def preproc_model(ds, mkey, var_name, date,
                  data_inp_dir,
                  #domain,
                  dims, dep_vars={}, targ_vert_coord='alt'):
    """
    Organize preprocessing of models.
    """
    # for all models rename variables to convention of this package
    # (if not yet done)
    #print(nlm[mkey]['vkeys'])
    if nlm[mkey]['vkeys'][var_name] in ds:
        ds = ds.rename({nlm[mkey]['vkeys'][var_name]:var_name})

    if mkey in ['COSMO','COSMO_ML','INT2LM']:
    #if mkey in ['COSMO','INT2LM']:
        ds = pp_COSMO(ds, var_name, dims, mkey, targ_vert_coord, dep_vars)
    elif mkey == 'NICAM':
        ds = pp_NICAM(ds, var_name, dims)
    elif mkey == 'SAM':
        ds = pp_SAM(ds, var_name, date, data_inp_dir, dims)
    elif mkey == 'ICON':
        ds = pp_ICON(ds, var_name, mkey, date, data_inp_dir, dims)
    elif mkey == 'UM':
        ds = pp_UM(ds, var_name, dims)
    elif mkey == 'MPAS':
        ds = pp_MPAS(ds, var_name, date, data_inp_dir, dims)
    elif mkey == 'IFS':
        ds = pp_IFS(ds, var_name, date, data_inp_dir, dims, dep_vars)
    elif mkey == 'GEOS':
        ds = pp_GEOS(ds, var_name, mkey, data_inp_dir, dims, dep_vars)
    elif mkey == 'ARPEGE-NH':
        ds = pp_ARPEGE(ds, var_name, mkey, date, data_inp_dir, dims, dep_vars)
    elif mkey == 'FV3':
        ds = pp_FV3(ds, var_name, mkey, date, data_inp_dir, dims, dep_vars)
    elif mkey == 'ERA5':
        ds = pp_ERA5(ds, var_name, date, data_inp_dir, dims, targ_vert_coord, dep_vars)
    elif mkey == 'DARDAR_CLOUD':
        ds = pp_DARDAR_CLOUD(ds)
    elif mkey == 'CM_SAF_MSG_AQUA_TERRA':
        pass
    elif mkey == 'CERES_EBAF':
        pass
    elif mkey == 'CM_SAF_HTOVS':
        pass
    elif mkey == 'GPM_IMERG':
        ds = pp_GPM_IMERG(ds)
    elif mkey == 'CMORPH':
        ds = pp_CMORPH(ds)
    elif (mkey in models_cmip6) or (mkey in 'MPI-ESM1-2-HR_delta'):
        ds = pp_models_cmip6(ds, var_name, mkey, dims, 
            targ_vert_coord, dep_vars)
    else:
        print(mkey)
        print('model pp not implemented.')
        quit()

    # remove some attributes for easier readable debugging output 
    remove_attrs = ['CDI', 'history', 'Conventions',
                    'NCO', 'CDO', 'institution']
    for attr_key in remove_attrs:
        if attr_key in ds.attrs:
            del ds.attrs[attr_key]
    # set "model_pp done" flag 
    ds.attrs[MODEL_PP] = MODEL_PP_DONE
    return(ds)



def pp_COSMO(ds, var_name, dims, mkey, targ_vert_coord, dep_vars=None):
    """
    Preprocess COSMO model.
    """

    ##  TODO temporary!
    if 'x' in ds.dims:
        ds = ds.rename({'x':'rlon'})
    if 'y' in ds.dims:
        ds = ds.rename({'y':'rlat'})

    # depending on sellonlatbox box, rlon or rlat might not exist.
    # (strange cdo behavior that I could not find a way around).
    #print('slatu' in ds.keys())
    #print(ds.slonu.shape)
    if dimx in dims:
        ## quick fix for staggered grid
        # ds comes with ... 
        if 'slonu' in ds.keys():
            if 'srlon' not in ds.keys():
                ds['srlon'] = ds['slonu'].values[0,:]
                #else:
                #    ds['rlon'] = ds['lon'].values[:]
            ds = ds.drop(['slonu', 'slatu'])
            ds = ds.rename({'srlon':'lon'})
        else:
            if 'slonv' in ds.keys():
                ds = ds.rename({'slonv':'lon'})
            # ds comes with 1d rlon/rlat and 2d lon/lat(rlon/rlat)
            if 'rlon' not in ds.keys():
                if len(ds['lon'].shape) == 2:
                    ds['rlon'] = ds['lon'].values[0,:]
                else:
                    ds['rlon'] = ds['lon'].values[:]
            if 'lon' in ds.keys():
                ds = ds.drop(['lon'])
            ds = ds.rename({'rlon':'lon'})
            #print(ds)
            #quit()

    if dimy in dims:
        if 'slatv' in ds.keys():
            #if 'srlat' not in ds.keys():
            #    ds['srlat'] = ds['slatv'].values[0,:]
            #    #else:
            #    #    ds['rlon'] = ds['lon'].values[:]
            ds = ds.drop(['slatv'])
            ds = ds.rename({'srlat':'lat'})
        else:
            if 'slatu' in ds.keys():
                ds = ds.rename({'slatu':'lat'})
            if 'rlat' not in ds.keys():
                if len(ds['lat'].shape) == 2:
                    ds['rlat'] = ds['lat'].values[:,0]
                else:
                    ds['rlat'] = ds['lat'].values[:]
            if 'lat' in ds.keys():
                ds = ds.drop(['lat'])
            ds = ds.rename({'rlat':'lat'})

    if dimz in dims:
        if targ_vert_coord == 'alt':
            if 'altitude' in ds.dims:
                ds = ds.rename({'altitude':'alt'})

                ### set values below surface to nan
                # preprocess HSURF
                dep_vars['HSURF'] = dep_vars['HSURF'].isel(time=0)
                dep_vars['HSURF'] = dep_vars['HSURF'].rename({'rlat':'lat', 'rlon':'lon'})
                # set values to nan
                #print(ds[var_name].shape)
                ds[var_name] = ds[var_name].where(ds.alt > dep_vars['HSURF'], np.nan)
                #print(ds[var_name].shape)
                #quit()

            elif 'level' in ds.dims:
                half_level_alt = dep_vars['VCOORD']
                level_alt = dep_vars['VCOORD'][:-1]
                level_alt.data = half_level_alt.data[:-1] + np.diff(half_level_alt)/2
                ds = ds.assign_coords({'level':level_alt.values})
                ds = ds.rename({'level':'alt'})

                # convert INT2LM pressure deviations from reference pressure to full pressure
                if (var_name == 'P') and (mkey == 'INT2LM'):
                    pref,pref_sfc = getpref(dep_vars['VCOORD'].vcflat,
                                            dep_vars['HSURF'], level_alt)
                    ds[var_name] += pref

                # sort according to altitude
                ds = ds.sortby('alt', ascending=True)

        elif targ_vert_coord == 'plev':
            if var_name != 'P':
                if 'altitude' in ds.dims:
                    targ_plevs = [
                        7000,10000,15000,20000,30000,40000,45000,50000,55000,
                        60000,65000,70000,75000,77500,80000,82500,85000,87500,90000,
                        92500,95000,97500,99000,100000,101000,
                    ]
                    var = interp_alt_to_plev(
                        var_name, 
                        ds[var_name], 
                        dep_vars['P'], 
                        targ_plevs,
                        vdim_name='altitude'
                    )
                    ds[var_name] = var
                    del ds['altitude']
                    #ds = ds.assign_coords(plev=targ_plevs)

                    ### mask values below surfacse
                    #print(dep_vars['PS'])
                    #ds[var_name] = ds[var_name].where(ds.plev <= dep_vars['PS'], np.nan)
                    #quit()
                else:
                    raise NotImplementedError()


    # preprocessing of specific variables
    if var_name == 'PP':
        # convert total accum. precip to mm/h
        ds.PP.values = ds.PP.values / np.mean(
                    (np.diff(ds.time.values)/1E9).astype(float)/3600)

    if var_name in ['LWUTOA', 'CLWUTOA']:
        ds[var_name].values *= -1

    ## Change time of PGW runs back to present.
    #if dt64_to_dt(ds.time.mean()).year >= 2006+88:
    #    ds['time'] -= np.timedelta64(int(365.25*88),'D')
    return(ds)



def pp_ERA5(ds, var_name, date, data_inp_dir, dims, targ_vert_coord, dep_vars={}):
    """
    Preprocess ERA5 reanalysis.
    """
    if targ_vert_coord != 'alt':
        raise NotImplementedError()

    if 'longitude' in ds: ds = ds.rename({'longitude':'lon'})
    if 'latitude' in ds: ds = ds.rename({'latitude':'lat'})

    # flip latitude orientation
    if ds.lat[-1] < ds.lat[0]:
        ds = ds.reindex(lat=list(reversed(ds.lat)))

    if dimz in dims:
        # skip preprocessing for altitude field because it should
        # become the vertical coordinate later and assumed to be
        # in original format (not preprocessed).
        if var_name == 'ALT':
            # convert from geopotential to altitude
            ds['ALT'] /= CON_G
            ds['ALT'] = add_var_attributes(ds['ALT'], 'ALT')
            return(ds)

        ## vertical interpolation from plev to alt
        # make sure dependency ALT is here
        if 'ALT' not in dep_vars: raise ValueError('should get dependency ALT')
        # load target altitude (user defined)
        targ_alt = np.sort(np.loadtxt(os.path.join(model_specifics_path,
                    'ERA5_plev_mean_alt_2017_dom_SA.dat')))
                    #'ERA5_plev_mean_alt_08.2016_dom_SEA_Sc.dat')))
        #targ_alt = np.sort(np.loadtxt(os.path.join(model_specifics_path,
        #            'ERA5_mlev_mean_alt_08.2016_dom_SEA_Sc.dat')))
        # make sure ALT and preproc var have same time steps
        dep_vars['ALT'], ds = select_common_timesteps(dep_vars['ALT'], ds)


        ## interpolate plev to alt
        ######################################################################
        # sort to have levels increasing in altitude direction
        # which is required for interpolation
        ds = ds.sortby('level', ascending=False)
        dep_vars['ALT'] = dep_vars['ALT'].sortby('level', ascending=False)

        ###### NEW WAY 
        #var = xr.apply_ufunc(
        #    interp_plev_to_alt_new,
        #    targ_alt,
        #    dep_vars['ALT'],
        #    ds[var_name],
        #    input_core_dims=[["level"], ["level"], ["level"]],  # list with one entry per arg
        #    output_core_dims=[["alt"]],  # returned data has one dimension
        #    exclude_dims=set(("level",)),  # dimensions allowed to change size. Must be a set!
        #    vectorize=True,  # loop over non-core dims
        #)
        ##var = var.rename({'level':'alt'})
        #var = var.assign_coords({'alt':targ_alt}).transpose('time','alt','lat','lon')
        #print(var)
        ##quit()

        ###### OLD WAY 
        var = interp_plev_to_alt_OLD(var_name, ds[var_name], dep_vars['ALT'], targ_alt,
                                vdim_name='level')
        ds[var_name] = var

        # convert pressure velocity [Pa s-1] to geometric velocity [m s-1]
        if var_name == 'W':
            if 'P' not in dep_vars: raise ValueError('should get dependency P')
            #print(ds[var_name].mean(dim=['time','lon','lat']))
            ds[var_name] /= dep_vars['P'].differentiate(coord='alt')
            #ds[var_name].to_netcdf('test.nc')
            #quit()
            #print(ds[var_name].mean(dim=['time','lon','lat']))

        ### set values below surface to nan
        # preprocess HSURF field
        dep_vars['HSURF'] = dep_vars['HSURF'].rename(
            {'longitude':'lon','latitude':'lat'}).isel(time=0) / CON_G
        dep_vars['HSURF'] = dep_vars['HSURF'].reindex(
            lat=list(reversed(dep_vars['HSURF'].lat)))
        # set values to nan
        ds[var_name] = ds[var_name].where(ds[var_name].alt > dep_vars['HSURF'], np.nan)

    #if var_name == 'CLDF':
    #    ds[var_name].to_netcdf('test.nc')
    #    quit()

    if var_name in ['SWDTOA',
                    'SWNDTOA', 'SWNDSFC', 'CSWNDSFC',
                    'LWUTOA', 'LWNDSFC', 'CLWNDSFC']:
        # convert hourly accumulated flux to flux per time
        ds[var_name] /= 3600.
        
    if var_name in ['LWUTOA']:
        ds[var_name] *= -1.


    return(ds)


#def pp_ERA5(ds, var_name, date, data_inp_dir, dims, dep_vars={}):
#    """
#    Preprocess ERA5 reanalysis.
#    """
#    if 'longitude' in ds: ds = ds.rename({'longitude':'lon'})
#    if 'latitude' in ds: ds = ds.rename({'latitude':'lat'})
#
#    if dimz in dims:
#        # skip preprocessing for altitude field because it should
#        # become the vertical coordinate later and assumed to be
#        # in original format (not preprocessed).
#        if var_name == 'ALT':
#            # convert from geopotential to altitude
#            #ds['ALT'] /= CON_G
#            ds['ALT'] = add_var_attributes(ds['ALT'], 'ALT')
#            return(ds)
#
#        ## vertical interpolation from plev to alt
#        # make sure dependency ALT is here
#        if 'ALT' not in dep_vars: raise ValueError('should get dependency ALT')
#        # load target altitude (user defined)
#        #targ_alt = np.sort(np.loadtxt(os.path.join(model_specifics_path,
#        #            'ERA5_plev_mean_geopot_08.2016_dom_SEA_Sc.dat'))) / CON_G
#        targ_alt = np.sort(np.loadtxt(os.path.join(model_specifics_path,
#                    'ERA5_mlev_mean_alt_08.2016_dom_SEA_Sc.dat')))
#        # make sure ALT and preproc var have same time steps
#        dep_vars['ALT'], ds = select_common_timesteps(dep_vars['ALT'], ds)
#
#        # interpolate 
#        # sort to have levels increasing in altitude direction
#        # which is required for interpolation
#        ds = ds.sortby('level', ascending=False)
#        dep_vars['ALT'] = dep_vars['ALT'].sortby('level', ascending=False)
#        var = interp_plev_to_alt(ds[var_name], dep_vars['ALT'], targ_alt,
#                                vdim_name='level')
#        ds[var_name] = var
#
#        # convert pressure velocity [Pa s-1] to geometric velocity [m s-1]
#        if var_name == 'W':
#            if 'P' not in dep_vars: raise ValueError('should get dependency P')
#            #print(ds[var_name].mean(dim=['time','lon','lat']))
#            ds[var_name] /= dep_vars['P'].differentiate(coord='alt')
#            #print(ds[var_name].mean(dim=['time','lon','lat']))
#
#    if var_name in ['SWDTOA', 'SWNDTOA', 'LWUTOA']:#, 'SLHFLX', 'SSHFLX']:
#        # convert hourly accumulated flux to flux per time
#        ds[var_name] /= 3600.
#
#    return(ds)


def pp_DARDAR_CLOUD(ds):
    """
    Preprocess DARDAR cloud obs.
    """
    # flip vertical coordinate to have increasing alt with index
    ds = ds.sel(alt=slice(None, None, -1))
    return(ds)


def pp_GPM_IMERG(ds):
    """
    Preprocess GPM IMERG precipitation obs.
    """
    ds = ds.transpose('time','bnds','lat','lon')
    if len(ds.time) == 1:
        # convert mm/day to mm/h
        ds.PP.values /= 24
    else:
        raise ValueError()
    return(ds)

def pp_CMORPH(ds):
    """
    Preprocess CMORPH precipitation obs.
    """
    if len(ds.time) == 1:
        # convert mm/day to mm/h
        ds.PP.values /= 24
    else:
        raise ValueError()
    return(ds)


def pp_models_cmip6(ds, var_name, mkey, dims, targ_vert_coord, dep_vars={}):
    """
    Preprocess CMIP6 models.
    """
    if mkey in ['CAMS-CSM1-0', 'E3SM-1-1','GFDL-CM4','CESM2','CMCC-CM2-SR5',
                  'GFDL-ESM4','CMCC-ESM2','NorESM2-LM','NorESM2-MM',
                  'TaiESM1','FGOALS-f3-L','CanESM5','FGOALS-g3',
                  'GISS-E2-1-G','HadGEM3-GC31-LL','HadGEM3-GC31-MM',
                  'INM-CM4-8','CESM2-WACCM','INM-CM5-0','UKESM1-0-LL']:

        with warnings.catch_warnings():
            ## ignore calendar conversion warning
            warnings.simplefilter("ignore")

            # convert from non-leap calendar to normal calendar
            ds['time'] = ds.indexes['time'].to_datetimeindex()


    if dimz in dims:
        # skip preprocessing for altitude field because it should
        # become the vertical coordinate later and assumed to be
        # in original format (not preprocessed).
        if var_name in ['ALT', 'ALT_Amon']:
            #if ds['ALT'].max() > 60000:
            #    raise NotImplementedError()
            ## convert from geopotential to altitude
            #ds['ALT'] /= CON_G
            ds['ALT'] = add_var_attributes(ds['ALT'], 'ALT')
            return(ds)


        #### GENERIC STEPS
        ######################################################################
        if mkey in ['ACCESS-CM2','ACCESS-ESM1-5','HadGEM3-GC31-LL','UKESM1-0-LL']:
            skip_step = True
            if 'HSURF' in dep_vars:
                dep_var_name_surf = 'HSURF'
                skip_step = False
            elif 'PS' in dep_vars:
                dep_var_name_surf = 'PS'
                skip_step = False

            if not skip_step:
                i_interp_lon = 0
                if len(ds.lon) != len(dep_vars[dep_var_name_surf].lon):
                    i_interp_lon = 1
                else:
                    if np.any(ds.lon.values - dep_vars[dep_var_name_surf].lon.values != 0):
                        i_interp_lon = 1
                if i_interp_lon:
                    ds = ds.interp(lon=dep_vars[dep_var_name_surf].lon.values, 
                                                kwargs={'fill_value':'extrapolate'})
                i_interp_lat = 0
                if len(ds.lat) != len(dep_vars[dep_var_name_surf].lat):
                    i_interp_lat = 1
                else:
                    if np.any(ds.lat.values - dep_vars[dep_var_name_surf].lat.values != 0):
                        i_interp_lat = 1
                if i_interp_lat:
                    ds = ds.interp(lat=dep_vars[dep_var_name_surf].lat.values, 
                                                kwargs={'fill_value':'extrapolate'})

        # for FGOALS-g3 HSURF has lat_2 instead of lat
        if 'HSURF' in dep_vars:
            try:
                dep_vars['HSURF'] = dep_vars['HSURF'].rename({'lat_2':'lat'})
            except ValueError:
                pass

            # for CMCC-CM2, HSURF is NaN over oceans.
            dep_vars['HSURF'] = dep_vars['HSURF'].where(~np.isnan(dep_vars['HSURF']), 0)


        ## for exception of IPSL-CM6A-LR
        if mkey == 'IPSL-CM6A-LR':
            raise NotImplementedError()
            ds = ds.rename({'klevp1':'lev'})
            ds[var_name] = ds[var_name].rename({'presnivs':'lev'})
            #ds = ds.rename({'presnivs':'lev'})



        ## VERTICAL INTERPOLATION MLEV TO PLEV
        ######################################################################
        var = ds[var_name]

        #print(ds.dims)
        #print(mkey)

        # load target altitude (user defined)
        targ_alt = np.sort(np.loadtxt(os.path.join(model_specifics_path,
                    #'MPI-ESM1-2-HR_plev_mean_alt_historical_1985_2015_Amon.dat')))
                    'MPI-ESM1-2-HR_plev_mean_alt_historical_1985_2015_Emon.dat')))
                    #'alts_COSMO.txt')))
        #targ_alt = np.sort(np.loadtxt(os.path.join(model_specifics_path,
        #            'ERA5_mlev_mean_alt_08.2016_dom_SEA_Sc.dat')))

        i_interp_plev_to_alt = 0
        if 'lev' in ds.dims:

            # find name of vertical coordinate coefficients
            if mkey in ['CAMS-CSM1-0', 'CMCC-CM2-SR5', 'CMCC-ESM2', 'CESM2', 'CESM2-WACCM',
                'E3SM-1-1','FGOALS-f3-L','GISS-E2-1-G','MIROC6','MIROC-ES2L','MRI-ESM2-0',
                'NorESM2-LM','NorESM2-MM','TaiESM1',
            ]:
                a_coef = 'a'
                b_coef = 'b'
                lev_type = 'hybsigp'
            elif mkey in ['CanESM5',
                'CNRM-CM6-1', 'CNRM-CM6-1-HR', 'CNRM-ESM2-1','GFDL-CM4','GFDL-ESM4',
                'IPSL-CM6A-LR','MPI-ESM1-2-HR','MPI-ESM1-2-LR', 
            ]:
                a_coef = 'ap'
                b_coef = 'b'
                lev_type = 'hybsigp'
            elif mkey in ['ACCESS-CM2', 'ACCESS-ESM1-5','HadGEM3-GC31-LL','UKESM1-0-LL']:
                a_coef = 'lev'
                b_coef = 'b'
                lev_type = 'height'
            elif mkey in ['FGOALS-g3',
            ]:
                p_lev = (ds.ptop + ds.lev*(ds.ps - ds.ptop)).transpose(
                                            'time', 'lev', 'lat', 'lon')
                lev_type = 'sigp'
            else:
                print('################### {}'.format(mkey))
                print(ds)
                raise NotImplementedError()

            if lev_type == 'hybsigp':
                #print(ds[a_coef])
                #print(ds[b_coef])
                #print(ds.ps)
                #quit()
                if 'ps' not in ds:
                    ps = dep_vars['PS']
                else:
                    ps = ds.ps 
                p_lev = (ds[a_coef] + ds[b_coef] * ps).transpose(
                                            'time', 'lev', 'lat', 'lon')
            if lev_type in ['hybsigp', 'sigp']:

                p_lev_mean = p_lev.mean(dim=['time','lon','lat'])

                #plev_targ = dep_vars['ALT'].plev
                #plev_targ = plev_targ.rename({'plev':'lev'})

                targ_plevs = [
                        100000.,  97500., 95000., 92500.,  90000.,
                        85000.,  80000., 75000., 70000.,
                        65000., 60000.,  55000., 50000.,  
                        45000., 40000.,  35000., 30000.,  
                        25000.,  20000.,  15000., 10000.,
                        9000.,8000.,7000.,6000.,5000.,4000.,3000.,2000.,
                        1000.,    500.,    100.]
                plev_targ = xr.DataArray(
                    data=targ_plevs,
                    dims=["lev"],
                    coords=dict(
                        lev=(["lev"], targ_plevs),
                    )
                )

                #print(plev_targ)
                #quit()
                p_targ = plev_targ.expand_dims(
                                dim={'lon':ds.lon,
                                     'lat':ds.lat,
                                     'time':ds.time}).transpose(
                                            'time', 'lev', 'lat', 'lon')

                # ensure the levels are ascending
                p_targ = p_targ.sortby('lev', ascending=True)
                if p_lev_mean.values[-1] < p_lev_mean.values[0]:
                    p_lev = p_lev.sortby('lev', ascending=True)
                    var = var.sortby('lev', ascending=True)

                #print(var.shape)
                #print(p_lev.shape)
                #print(p_lev.isel(lat=100,lon=100,time=0))
                #print(p_targ.shape)
                #quit()

                var_plev = interp_logp_4d(var, p_lev, p_targ,
                                    lon_key='lon', lat_key='lat', time_key='time',
                                    extrapolate='constant')
                var_plev = var_plev.rename({'lev':'plev'})
                var_plev = var_plev.assign_coords({'plev':plev_targ.sortby(
                                                'lev', ascending=True).values})
                #print(var_plev)
                #var_plev.to_netcdf('test.nc')
                #quit()
                # sort back to ascending in pressure
                var = var_plev.sortby('plev', ascending=False)

                i_interp_plev_to_alt = 1

            elif lev_type == 'height':
                alt_lev = (ds[a_coef] + ds[b_coef] * dep_vars['HSURF']).expand_dims(
                                dim={'time':var.time}).transpose(
                                            'time', 'lev', 'lat', 'lon')

                alt_targ = xr.DataArray(
                    data=targ_alt,
                    dims=["lev"],
                    coords=dict(
                        lev=(["lev"], targ_alt),
                    )
                ).expand_dims(
                        dim={'lon':ds.lon,
                             'lat':ds.lat,
                             'time':ds.time}).transpose(
                                    'time', 'lev', 'lat', 'lon')

                #print(var.dims)
                #print(alt_lev.dims)
                #print(alt_targ.dims)
                #quit()

                var_alt = interp_logp_4d(var, alt_lev, alt_targ,
                                    lon_key='lon', lat_key='lat', time_key='time',
                                    extrapolate='constant',
                                    no_logp=True)
                var_alt = var_alt.rename({'lev':'alt'})
                var = var_alt.assign_coords({'alt':targ_alt})
                #print(var)
                ##var.to_netcdf('test.nc')
                #quit()
            
            else:
                raise NotImplementedError()


        #### VERTICAL INTERPOLATION TO ALTITUDE LEVELS
        ######################################################################
        if targ_vert_coord == 'alt':
            ## vertical interpolation from plev to alt
            # make sure dependency ALT is here
            if ('ALT' not in dep_vars) and ('ALT_Amon' not in dep_vars): 
                raise ValueError('should get dependency ALT')

            # make sure ALT and preproc var have same time steps
            dep_vars['ALT'], ds = select_common_timesteps(dep_vars['ALT'], ds)
            if (len(ds.time) == 0) | (len(dep_vars['ALT'].time) == 0):
                raise ValueError('Time dimensions do not agree with dep vars!!')



            if 'plev' in ds.dims:
                var = ds[var_name]
                i_interp_plev_to_alt = 1
            #else:
            #    var = ds[var_name]


            if i_interp_plev_to_alt:

                ## very ugly fix for very ugly problem of missing values in E3SM-1-1
                if mkey in ['E3SM-1-1']:
                    dep_vars['ALT'] = dep_vars['ALT'].where(dep_vars['ALT'] < 60000, np.nan)

                ## if var and alt are not given on same vertical grid
                ## interp lower res to higher res
                if len(var.plev) > len(dep_vars['ALT'].plev):
                    dep_vars['ALT'] = dep_vars['ALT'].interp(plev=var.plev.values, 
                                                kwargs={'fill_value':'extrapolate'})
                elif len(var.plev) < len(dep_vars['ALT'].plev):
                    var = var.interp(plev=dep_vars['ALT'].plev.values, 
                                                kwargs={'fill_value':'extrapolate'})


                ## interp if var and alt are not given on same horizontal grid
                ## but only for some known exceptions to avoid things getting out of hand..
                if mkey in ['ACCESS-CM2','ACCESS-ESM1-5','HadGEM3-GC31-LL','UKESM1-0-LL']:
                    i_interp_lon = 0
                    if len(var.lon) != len(dep_vars['ALT'].lon):
                        i_interp_lon = 1
                    else:
                        if np.any(var.lon.values - dep_vars['ALT'].lon.values != 0):
                            i_interp_lon = 1
                    if i_interp_lon:
                        dep_vars['ALT'] = dep_vars['ALT'].interp(lon=var.lon.values, 
                                                    kwargs={'fill_value':'extrapolate'})
                        #var = var.interp(lon=dep_vars['ALT'].lon.values, 
                        #                            kwargs={'fill_value':'extrapolate'})

                    i_interp_lat = 0
                    if len(var.lat) != len(dep_vars['ALT'].lat):
                        i_interp_lat = 1
                    else:
                        if np.any(var.lat.values - dep_vars['ALT'].lat.values != 0):
                            i_interp_lat = 1
                    if i_interp_lat:
                        dep_vars['ALT'] = dep_vars['ALT'].interp(lat=var.lat.values, 
                                                    kwargs={'fill_value':'extrapolate'})
                        #var = var.interp(lat=dep_vars['ALT'].lat.values, 
                        #                            kwargs={'fill_value':'extrapolate'})

                #print(mkey)
                #print(var.lat)
                #print(dep_vars['ALT'].lat)
                #print(var.lat.values - dep_vars['ALT'].lat.values)
                var = interp_plev_to_alt_OLD(var_name, var, dep_vars['ALT'], targ_alt,
                                        vdim_name='plev')
                #print(var)
                #var.to_netcdf('test.nc')
                #quit()

            #if var_name == 'T':
            #    var.to_netcdf('test.nc')
            #    quit()

        #### VARIABLE SPECIFCI COMPUTATIONS
        ######################################################################
        # cloud fraction should go from 0-1
        if var_name in ['CLDF']:
            var /= 100 

        # RH should go from 0-1
        if var_name in ['RH']:
            var /= 100 

        # convert pressure velocity [Pa s-1] to geometric velocity [m s-1]
        if var_name == 'W':
            if 'P' not in dep_vars: raise ValueError('should get dependency P')
            #print(var.mean(dim=['time','lon','lat']))
            dPdz = dep_vars['P'].differentiate(coord='alt')
            if np.any(dPdz == 0):
                raise ValueError('Zero vertical P-gradient encountered!')
            #dPdz.to_netcdf('test.nc')
            #dep_vars['P'].to_netcdf('test.nc')
            #quit()
            var /= dep_vars['P'].differentiate(coord='alt')
            #var.to_netcdf('test.nc')
            #quit()
            #print(var.mean(dim=['time','lon','lat']))


        #print(var)
        #print(mkey)

        #### MASK BELOW SURFACE
        ######################################################################
        if targ_vert_coord == 'alt':
            try:
                var = var.where(var.alt >= dep_vars['HSURF'], np.nan)
            except ValueError:
                #print('Warning: Coords of 3D field and HSURF differ. model_pp {}.'.format(mkey))
                #dep_vars['HSURF'] = dep_vars['HSURF'].assign_coords({'lon':var.lon.values})
                dep_vars['HSURF'] = dep_vars['HSURF'].assign_coords({'lat':var.lat.values})

                var = var.where(var.alt >= dep_vars['HSURF'], np.nan)

        elif targ_vert_coord == 'plev':
            var = var.where(var.plev <= dep_vars['PS'], np.nan)

        #if var_name == 'CLDF':
        #    var.to_netcdf('test.nc')
        #    quit()

        ds[var_name] = var

    return(ds)


###############################################################################
###############################################################################
###############################################################################


@njit()
def interp_vprof_with_time(orig_array, src_vcoord_array,
                targ_vcoord, interp_array,
                ntime, nlat, nlon, sfc_extrap='const'):
    """
    Helper function for vertical interpolation using Numba.
    Speedup of ~100 time compared to pure python code!
    """
    for time_ind in range(ntime):
        #print(time_ind)
        for lat_ind in range(nlat):
            #lat_ind = 72
            for lon_ind in range(nlon):
                #lon_ind = 136

                orig_vcol = orig_array[time_ind, :, lat_ind, lon_ind]
                src_vcoord_vcol = src_vcoord_array[time_ind, :, lat_ind, lon_ind]
                interp_vcol = np.interp(targ_vcoord, src_vcoord_vcol, orig_vcol)

                ##print(src_vcoord_vcol)
                ##print(targ_vcoord)
                ##print(orig_vcol)
                ##print(interp_vcol)
                if np.all(np.isnan(src_vcoord_vcol)):
                    continue

                # constant extrapolation is the default
                if sfc_extrap == 'const':
                    pass
                elif sfc_extrap == 'nan':
                    ## this masks extrapolation values:
                    ## if not used, constant extrapolation is done by np.interp
                    interp_vcol[targ_vcoord < np.min(src_vcoord_vcol)] = np.nan
                elif sfc_extrap == 'linear':
                    min_src_vc_ind = np.argmin(src_vcoord_vcol)
                    if min_src_vc_ind == len(src_vcoord_vcol) - 1: 
                        raise ValueError()
                    slope = (
                        (orig_vcol[min_src_vc_ind+1] - orig_vcol[min_src_vc_ind]) / 
                        (src_vcoord_vcol[min_src_vc_ind+1] - src_vcoord_vcol[min_src_vc_ind])
                    )
                    x0 = src_vcoord_vcol[min_src_vc_ind]
                    y0 = orig_vcol[min_src_vc_ind]
                    #print(min_src_vc_ind)
                    #print(interp_vcol[targ_vcoord < np.min(src_vcoord_vcol)])
                    #print(slope)
                    #print(x0)
                    #print(y0)
                    #print(y0 - slope * (x0 - targ_vcoord[targ_vcoord < np.min(src_vcoord_vcol)]))
                    interp_vcol[targ_vcoord < np.min(src_vcoord_vcol)] = (
                        y0 - slope * 
                        (x0 - targ_vcoord[targ_vcoord < np.min(src_vcoord_vcol)]) 
                    )
                else:
                    raise ValueError()

                #print(interp_vcol)
                #quit()
                interp_array[time_ind, :, lat_ind, lon_ind] = interp_vcol
    return(interp_array)


def interp_plev_to_alt_OLD(var_name, var_on_plev, alt_of_plev, targ_alt,
                        vdim_name='level'):
    """
    interpolate from pressure levvels to constant altitude levels.
    Currently only does linear interpolation and for extrapolation
    assumes constant values (extrapolated value = nearby value)
    Also assumes that alt_of_plev is sorted in the same direction
    as targ_alt.
    """

    # determine how surface extrapolation should be handled based 
    # on variable to interpoalte
    #print(var_name)
    if var_name in ['P', 'W', 'QC', 'QI', 'QV', 'T', 'U', 'V', 'CLDF', 'RH']:
        sfc_extrap = 'linear'
    elif var_name in []:
        sfc_extrap = 'const'
    else:
        raise ValueError("Don't know how to extrapolate variable {} at the surface.".format(var_name))

    # make sure variables have same order of dimensions
    if ( (list(var_on_plev.dims) != ['time', vdim_name, 'lat', 'lon']) or
         (list(alt_of_plev.dims) != ['time', vdim_name, 'lat', 'lon']) ):
        print(vdim_name)
        print(var_on_plev.dims)
        print(alt_of_plev.dims)
        raise ValueError('Variables not to have same order of dimensions')

    # make sure dimensions are identical
    for dim_key in ['time', 'lat', 'lon']:
        #print(dim_key)
        if len(var_on_plev[dim_key]) != len(alt_of_plev[dim_key]):
            raise ValueError(
                'Vars have different number of elements for {}.'.format(dim_key))
        if np.any(np.abs(var_on_plev[dim_key].values.astype(float) - 
                         alt_of_plev[dim_key].values.astype(float)) > 0):
            raise ValueError(
                'Vars have different elements for {}.'.format(dim_key))

    # create array for interpolated var values
    var_on_alt = xr.full_like(var_on_plev.isel({vdim_name:1}, drop=True),
                    np.nan).expand_dims(alt=targ_alt, axis=1)
    var_on_alt_array = np.full_like(var_on_alt.values, np.nan)
    # interpolate from plev to alt (var_on_plev -> var_on_alt)
    var_on_alt.values = interp_vprof_with_time(
                    var_on_plev.values,
                    alt_of_plev.values,
                    targ_alt,
                    var_on_alt_array,
                    len(var_on_plev.time.values),
                    len(var_on_plev.lat.values),
                    len(var_on_plev.lon.values),
                    sfc_extrap)
    var_on_alt.alt.attrs['units'] = 'm'
    var_on_alt.alt.attrs['long_name'] = 'altitude'
    return(var_on_alt)


def interp_plev_to_alt_new(x_out, x_in, data_in):
    print(x_out)
    print(x_in)
    print(data_in)
    quit()
    # TODO: ACCESS models have nan for data within orography --> whole
    #       column becomes nan over orography.
    # TODO: implement adjustment to orography.
    #out = np.interp(x_out, x_in, data_in)
    #print(out)
    ##return(out)
    #quit()
    #f = interp1d(x_in, data_in, kind='linear', 
    #            fill_value=np.nan, bounds_error=False)
    #f = interp1d(x_in, data_in, kind='linear', 
    #            fill_value='extrapolate', bounds_error=False)
    x_in2 = x_in.copy()
    #if np.sum(np.isnan(data_in)) > 0:
    #    print(~np.isnan(data_in))
    #    quit()
    #    #x_in2 = x_in.copy()
    #    #x_in[np.isnan(x_in)] = 0
    #    #x_in = np.where(~np.isnan(x_in), x_in, 0)
    #    x_in2[0] = 1
    #    x_in2[1] = 2
    #    x_in2[2] = 3
    #    x_in2[3] = 4
    #    #print(x_in2)
    #    #quit()
    #print(x_in2)
    #print(x_out)
    data_in2 = data_in.copy()
    data_in2[np.isnan(data_in2)] = 0
    #print(data_in)
    f = interp1d(x_in2, data_in2, kind='cubic', 
                fill_value='extrapolate', bounds_error=False)
    out = f(x_out)
    #print(out)
    #if np.sum(np.isnan(data_in)) > 0:
    #    quit()
    #print(out)
    #quit()
    return(out)


def interp_alt_to_plev(var_name, var_on_alt, p_of_alt, targ_plev,
                        vdim_name='alt'):
    """
    """
    ## flip to decreasing altitude which is required for correct execution
    var_on_alt = var_on_alt.reindex({vdim_name:list(reversed(var_on_alt[vdim_name]))})
    p_of_alt = p_of_alt.reindex({vdim_name:list(reversed(p_of_alt[vdim_name]))})

    # make sure variables have same order of dimensions
    if ( (list(var_on_alt.dims) != ['time', vdim_name, 'lat', 'lon']) or
         (list(p_of_alt.dims) != ['time', vdim_name, 'lat', 'lon']) ):
        print(vdim_name)
        print(var_on_alt.dims)
        print(p_of_alt.dims)
        raise ValueError('Variables not to have same order of dimensions')


    # make sure dimensions are identical
    for dim_key in ['time', 'lat', 'lon']:
        #print(dim_key)
        if len(var_on_alt[dim_key]) != len(p_of_alt[dim_key]):
            raise ValueError(
                'Vars have different number of elements for {}.'.format(dim_key))
        if np.any(np.abs(var_on_alt[dim_key].values.astype(float) - 
                         p_of_alt[dim_key].values.astype(float)) > 0):
            raise ValueError(
                'Vars have different elements for {}.'.format(dim_key))

    var_on_plev = xr.full_like(var_on_alt.isel({vdim_name:1}, drop=True),
                    np.nan).expand_dims(plev=targ_plev, axis=1)
    var_on_plev_array = np.full_like(var_on_plev.values, np.nan)
    # interpolate from plev to alt (var_on_plev -> var_on_alt)
    var_on_plev.values = interp_vprof_with_time(
                    var_on_alt.values,
                    p_of_alt.values,
                    np.asarray(targ_plev),
                    var_on_plev_array,
                    len(var_on_alt.time.values),
                    len(var_on_alt.lat.values),
                    len(var_on_alt.lon.values),
                    'const')
    var_on_plev.plev.attrs['units'] = 'Pa'
    var_on_plev.plev.attrs['long_name'] = 'pressure'
    #var_on_plev = var_on_plev.assign_coords({'plev':targ_plev})

    #print(var_on_plev)
    #var_on_plev.to_netcdf('test.nc')
    #quit()
    return(var_on_plev)


def fix_wrong_time_steps(ds, mkey):
    """
    If some of the time steps are not unique (who knows why, it is a mess!)
    create a manually created time series under the assumption that
    the time step is constant and that first time step in series is correct.
    """
    if len(np.unique(ds.time.values)) != len(ds.time.values):
        print('{}: fix problem with time steps in preprocessing'.format(mkey))
        supposed_dt = (np.diff(ds.time.values[0:2])/1E9).astype(float)
        start_date = dt64_to_dt(ds.time.values[0])
        time_steps = np.arange(start_date, start_date +
                        (len(ds.time.values)) * 
                         timedelta(seconds=int(supposed_dt)),
                         timedelta(seconds=int(supposed_dt)))
        ds.time.values = time_steps
    return(ds)



def compute_ALT_of_plev(mem_dict, P, PHLEV, T, QV, HSURF=None, i_debug=0):
    """
    Integrate geopotential to obtain altitude.
    - Attention!!! this function currently only considers surface elevation
      if it is given as an input argument. Else it assumes HSURF=0
      and thus only works over the ocean!!!
    - Currently neglects QC!
    """
    mod_key = mem_dict['mod']
    # model levels
    if mod_key == 'ERA5':
        # for P lev is already renamed during computation of P
        T = T.rename({'level':'lev'})
        QV = QV.rename({'level':'lev'})
        lev = P.lev.values
    elif mod_key == 'IFS':
        lev = P.lev.values
    elif mod_key == 'FV3':
        # interpolate qv to same levels as T
        QV = QV.interp(plev=T.pfull)
        # replace levels by indices
        orig_lev = P.pfull.values
        P.pfull.values = np.arange(0,len(orig_lev))
        P = P.rename({'pfull':'lev'})
        lev = P.lev.values
        PHLEV.hlev.values = np.arange(0,len(orig_lev)+1)
        T = T.rename({'pfull':'lev'})
        T.lev.values = lev
        QV = QV.rename({'pfull':'lev'})
        QV.lev.values = lev
    else: raise NotImplementedError()

    ### COMPUTE ALT (at same time steps as P)
    #######################################################################
    # make sure the same time steps are selected in all data sets
    QV, T = select_common_timesteps(QV, T)
    P, T = select_common_timesteps(P, T)
    PHLEV, T = select_common_timesteps(PHLEV, T)
    QV, T = select_common_timesteps(QV, T)

    # load arrays into memory to speed up the vertical integration
    if i_debug >= debug_level_2: print('load fields')
    T.load()
    QV.load()
    PHLEV.load()
    if i_debug >= debug_level_2: print('load fields done')

    # altitude at full levels (vertical mass points)
    ALT = xr.full_like(P, fill_value=0)
    # altitude at half levels (vertical interfaces)
    ALTHLEV = xr.full_like(PHLEV, fill_value=0)
    # add surface height to obtain altitude as a result instead of height
    if HSURF is not None:
        ALTHLEV.loc[{'hlev':ALTHLEV.hlev[-1]}] = HSURF
    # integrate upward
    if i_debug >= debug_level_2: print('integrate')
    for l in np.flip(lev):
        if i_debug >= debug_level_4: print(l)
        # pressure at lower (altitudewise) half level
        pbelow = PHLEV.sel(hlev=l+1)
        # pressure at upper (altitudewise) half level
        pabove = PHLEV.sel(hlev=l)
        dlogp   = np.log(pbelow/pabove)
        dp      = pbelow - pabove
        alpha   = 1. - ( (pabove/dp) * dlogp )
        # virtual temperature at full level
        Tv_full = T.sel(lev=l) * (1. + 0.609133 * QV.sel(lev=l) )
        # compute geopotential at this full level from half level below
        ALT.loc[{'lev':l}] = (ALTHLEV.sel(hlev=l+1) + Tv_full * 
                                    CON_RD * alpha )
        # compute geopotential at next half level
        ALTHLEV.loc[{'hlev':l}] = (ALTHLEV.sel(hlev=l+1) + Tv_full * 
                                    CON_RD * dlogp)
    if i_debug >= debug_level_2: print('integrate done')

    # convert geopotential to height
    ALT /= CON_G
    ALT = add_var_attributes(ALT, 'ALT')
    ALT['time'] = P.time

    ALT['lon'] = P.lon
    ALT['lat'] = P.lat

    # replace labels with original ones
    if mod_key == 'ERA5':
        ALT = ALT.rename({'lev':'level'})
    elif mod_key == 'FV3':
        ALT.lev.values = orig_lev
        ALT = ALT.rename({'lev':'pfull'})

    return(ALT)

def compute_P_plev(mem_dict, T):
    mkey = mem_dict['mod']
    if mkey == 'ERA5':
        vert_key = 'level'
        lat_key = 'latitude'
        lon_key = 'longitude'
        fact = 100
    elif mkey == 'FV3':
        vert_key = 'pfull'
        lat_key = 'lat'
        lon_key = 'lon'
        fact = 100
    elif mkey in models_cmip6:
        vert_key = 'plev'
        lat_key = 'lat'
        lon_key = 'lon'
        fact = 1
    # take pressure from vertical coordinate and expand to 3D field
    P = T[vert_key].expand_dims(dim={
                            'time':T.time,
                            lat_key:T[lat_key],
                            lon_key:T[lon_key]})
    P['time'] = T.time
    P[lon_key] = T[lon_key]
    P[lat_key] = T[lat_key]
    P = P.copy()
    P.values *= fact
    P = add_var_attributes(P, 'P')
    P = P.transpose('time', vert_key, lat_key, lon_key)
    return(P)

def interp_PHLEV_from_P(mem_dict, PS, P):
    """
    Use PS as lowest half level for all levels above, apply 
    simple linear interpolation.... (TODO: could be improved..)
    """
    # for ERA5
    if 'level' in P.dims:
        P = P.rename({'level':'lev'})

    mkey = mem_dict['mod']
    # load variables into memory for later speedup
    P.load()
    if mkey in ['ERA5', 'IFS']:
        lev = P['lev'].values
        # extend full levels by one at the end to obtain
        # half levels
        hlev = np.append(lev, lev[-1]+1)
    elif mkey == 'FV3':
        lev = P['pfull'].values
        # simply set surface half level to some pressure value
        # as a place holder.
        # and keep other levels like full levels
        # this is all incorrect but the level names only act 
        # as names from here on.
        hlev = np.append(lev, 1000.)
        P = P.rename({'pfull':'lev'})
    else: raise NotImplementedError()

    PHLEV = PS.copy()
    PHLEV = PHLEV.sel(time=P.time)
    PHLEV = PHLEV.expand_dims(dim={'hlev':hlev}, axis=1)
    PHLEV = PHLEV.copy()
    # set surface to surface pressure
    PHLEV.loc[{'hlev':hlev[-1]}] = PS.sel(time=PHLEV.time).values
    # interpolate pressure of non-boundary levels
    PHLEV.loc[{'hlev':hlev[1:-1]}] = 0.5 * (P.sel(lev=lev[1:]).values + 
                                         P.sel(lev=lev[:-1]).values)
    ## uppermost (geometrically speaking) half level pressure is not required
    ## for integration of geopotential
    ##PHLEV.loc[{'hlev':hlev[0]}] = np.nan
    # extrapolate uupermost half level pressure
    PHLEV.loc[{'hlev':hlev[0]}] = P.sel(lev=lev[1]).values + 1.5 * (
                                        P.sel(lev=lev[1]).values - 
                                        P.sel(lev=lev[2]).values   )

    return(PHLEV)

def compute_P_hybplev(mem_dict, PS, T):
    mod_key = mem_dict['mod']

    # for ERA5
    if mod_key == 'ERA5':
        if 'level' in T.dims:
            T = T.rename({'level':'lev'})
        if 'latitude' in T.dims:
            T = T.rename({'latitude':'lat'})
            PS = PS.rename({'latitude':'lat'})
        if 'longitude' in T.dims:
            T = T.rename({'longitude':'lon'})
            PS = PS.rename({'longitude':'lon'})

    # number of full levels in the model output
    nlev = len(T.lev)

    ### COMPUTE P (at same time steps as T)
    #######################################################################
    # hybrid pressure coordinates
    # compute pressure at mid-levels based on hyam + hybm*PS
    ## orig (correct) alt inds as reference for new method
    #alt_inds = {'IFS':93, 'ARPEGE-NH':15}
    # total number of full vertical levels for whic the model was run
    # determined based on vertical grid parameters
    tot_nlev = len(np.loadtxt(os.path.join(model_specifics_path,
                    '{}_hyam.txt'.format(mod_key))))
    v_ind_start = tot_nlev - nlev
    # levels and half levels of imported data set
    lev = np.arange(tot_nlev - nlev+1, tot_nlev+1)
    #hlev = np.arange(tot_nlev - nlev+1, tot_nlev+2)
    # full level hybrid coordinate components
    hyam = xr.DataArray(np.loadtxt(os.path.join(model_specifics_path,
                    '{}_hyam.txt'.format(mod_key)))[v_ind_start:],
                    dims=('lev',), coords={'lev':lev})
    hybm = xr.DataArray(np.loadtxt(os.path.join(model_specifics_path,
                    '{}_hybm.txt'.format(mod_key)))[v_ind_start:],
                    dims=('lev',), coords={'lev':lev})
    # compute level pressure from PS and hyam, hybm
    P = PS.load()
    P = P.sel(time=T.time)
    P['time'] = T.time
    P = P.expand_dims(dim={'lev':lev}, axis=1)
    P = hyam + P*hybm
    P['lev'] = T.lev
    P = P.transpose('time', 'lev', 'lat', 'lon')
    P = add_var_attributes(P, 'P')

    ## estimation of half-level pressure
    #PHLEV = PS.copy()
    #PHLEV = PHLEV.sel(time=T.time)
    #PHLEV = PHLEV.expand_dims(dim={'hlev':hlev}, axis=1)
    ## For IFS, we have given the grid parameters for the half levels
    ## and can use them.
    #if mod_key == 'IFS':
    #    # half level hybrid coordinate components
    #    hyai = xr.DataArray(np.loadtxt(os.path.join(model_specifics_path,
    #                    '{}_hyai.txt'.format(mod_key)))[v_ind_start:],
    #                    dims=('hlev',), coords={'hlev':hlev})
    #    hybi = xr.DataArray(np.loadtxt(os.path.join(model_specifics_path,
    #                    '{}_hybi.txt'.format(mod_key)))[v_ind_start:],
    #                    dims=('hlev',), coords={'hlev':hlev})
    #    # compute level and half-level pressure from PS and hyax, hybx
    #    PHLEV = hyai + PHLEV*hybi
    #    PHLEV = PHLEV.transpose('time', 'hlev', 'lat', 'lon')

    # for ERA5
    if mod_key == ['ERA5']:
        P = P.rename({'lev':'level',
                      'lat':'latitude',
                      'lon':'longitude'})


    return(P)


#get reference pressure function (from PGW Python by Roman Brogli)
def getpref(vcflat, hsurf, height_flat):
    smoothing = (vcflat - height_flat) / vcflat
    smoothing = np.where(smoothing > 0, smoothing, 0)

    # the height at which the reference pressure needs to be computed 
    # needs to be derived form the terrain following coordinates:
    newheights = np.zeros((len(height_flat), hsurf.shape[0], hsurf.shape[1]))

    #avoid forloop
    newheights = height_flat.values[:,None,None] + hsurf.values[None,:,:] * smoothing[:,None,None]

    #New formulation as researched by Christian Steger (untested)
    # Constants
    p0sl = height_flat.p0sl # sea-level pressure [Pa]
    t0sl = height_flat.t0sl   # sea-level temperature [K]
    # Source: COSMO description Part I, page 29
    g = 9.80665     # gravitational acceleration [m s-2]
    R_d = 287.05    # gas constant for dry air [J K-1 kg-1]
    # Source: COSMO source code, data_constants.f90

    # irefatm = 2
    delta_t = height_flat.delta_t
    h_scal = height_flat.h_scal
    # Source: COSMO description Part VII, page 66
    t00 = t0sl - delta_t

    pref = p0sl * np.exp (-g / R_d * h_scal / t00 * \
               np.log((np.exp(newheights / h_scal) * t00 + delta_t) / \
                      (t00 + delta_t)) )
    pref_sfc = p0sl * np.exp (-g / R_d * h_scal / t00 * \
               np.log((np.exp(hsurf.data / h_scal) * t00 + delta_t) / \
                      (t00 + delta_t)) )

    return pref, pref_sfc









































def pp_NICAM(ds, var_name, dims):
    """
    Preprocess NICAM model.
    """
    # rename dimensions
    if 'lev' in ds.keys():
        ds = ds.rename({'lev':'alt'})

    # preprocessing of specific variables
    if var_name == 'PP':
        # convert kg/m2/s precip to mm/h
        ds = ds * 3600
    return(ds)


def pp_SAM(ds, var_name, date, data_inp_dir, dims):
    """
    Preprocess SAM model.
    """
    if (dimz in dims) and ('z' in ds):
        # rename dimensions
        ds = ds.rename({'z':'alt'})
    # preprocessing of specific variables
    if var_name == 'PP':
        # convert all time accum mm precip to mm/h
        # load last date file and then apply diff to convert
        # accumulated precip to a precip flux.
        last_date_file = os.path.join(data_inp_dir,
                    '{}_{:%Y%m%d}.nc'.format(var_name,
                                        date-timedelta(days=1)))
        last_date_ds = xr.open_dataset(last_date_file)
        last_time_step = last_date_ds.isel(time=-1)
        ds = xr.concat([last_time_step, ds], dim='time')
        ds = ds.diff(dim='time')
        time_slice = slice('{:%Y-%m-%d}'.format(date),
                           '{:%Y-%m-%d}'.format(date+timedelta(days=1)))
        ds = ds.sel(time=time_slice)
        ds = ds / np.mean(np.diff(ds.time.values)/1E9).astype(float)*3600

    elif var_name == 'P':
        # convert perturbation pressure to absolute pressure 
        #print(ds.mean(dim=['lon', 'lat', 'time']).PP.values)
        p_mean = ds.p*100.
        p_mean = p_mean.expand_dims(lat=ds['P'].lat, axis=1)
        p_mean = p_mean.expand_dims(lon=ds['P'].lon, axis=2)
        p_mean = p_mean.expand_dims(time=ds['P'].time, axis=0)
        ds['P'] = ds['P'] + p_mean
        #print(ds.mean(dim=['lon', 'lat', 'time']).PP.values)

    elif var_name in ['QV','QC']:
        # convert from g/kg to kg/kg
        ds[var_name] /= 1000.

    return(ds)


def pp_ICON(ds, var_name, mkey, date, data_inp_dir, dims):
    """
    Preprocess ICON model.
    """
    # do this not in dimz part because some 2D vars
    # have height as coordinate.
    if (dimz in dims) and ('height' in ds.coords):
        # rename dimensions
        ds = ds.rename({'height':'alt'})

        # transform altitude coordinate
        hgt_in = np.loadtxt(os.path.join(model_specifics_path, 'ICON_hgt.txt'))
        #print(hgt_in)
        #print(ds['alt'].values)
        #print(ds['alt'].values.shape)
        #print(var_name)
        if var_name in ['W']:
            ## surface not part of extracted W field.
            #hgt_in = hgt_in[:-1]
            pass
        else:
            # convert from half levels to full levels
            hgt_in = hgt_in[1:] - np.diff(hgt_in)/2
        #print(hgt_in)
        ds['alt'].values -= 1
        ds['alt'].values = hgt_in[ds['alt'].values.astype(np.int)]
        ds['alt'].attrs['units'] = 'm'
        # flip vertical coordinate to have increasing alt with index
        ds = ds.sel(alt=slice(None, None, -1))

    # preprocessing of specific variables
    if var_name == 'PP':
        # convert all time accum mm precip to mm/h
        # load last date file and then apply diff to convert
        # accumulated precip to precipitation flux.
        last_date_file = os.path.join(data_inp_dir,
                    '{}_{:%Y%m%d}.nc'.format(var_name,
                                        date-timedelta(days=1)))
        last_date_ds = xr.open_dataset(last_date_file)
        # rename var name to package naming convention
        last_date_ds = last_date_ds.rename(
                {nlm['ICON']['vkeys'][var_name]:var_name})
        last_time_step = last_date_ds.isel(time=-1)
        ds = xr.concat([last_time_step, ds], dim='time')
        ds = ds.diff(dim='time')
        time_slice = slice('{:%Y-%m-%d}'.format(date),
                           '{:%Y-%m-%d}'.format(date+timedelta(days=1)))
        ds = ds.sel(time=time_slice)
        ds = ds / np.mean(np.diff(ds.time.values)/1E9).astype(float)*3600

    if var_name in ['LWUTOA', 'SWNDTOA']:
        start_date = np.datetime64(datetime(2016,8,1))
        last_date_file = os.path.join(data_inp_dir,
                    '{}_{:%Y%m%d}.nc'.format(var_name,
                                        date-timedelta(days=1)))
        #last_date_ds = xr.open_dataset(last_date_file)
        with xr.open_dataset(last_date_file) as last_date_ds:
            # rename var name to package naming convention
            last_date_ds = last_date_ds.rename(
                    {nlm['ICON']['vkeys'][var_name]:var_name})
            last_time_step = last_date_ds.isel(time=-1)
            ds = xr.concat([last_time_step, ds], dim='time')

        ## look up vkey. if var has already been computed, then take var_name
        #vkey = nlm[mkey]['vkeys'][var_name]
        #if vkey not in ds: vkey = var_name

        # determine output step (output is every 30min)
        #cout = ((ds.time - start_date)/1E9/(3600*0.5)).astype(float)
        cout = ((ds.time - start_date)/1E9/ \
                (np.mean(np.diff(ds.time.values)/1E9))).astype(float)


        time_index = list(ds.coords.keys()).index('time')
        if time_index == 2:
            for i in range(len(cout)):
                ds[var_name].values[:,:,i] *= cout.values[i]
        else:
            raise NotImplementedError()
        ds = ds.diff(dim='time')
        # alternative way how to remove running mean.
        # A(n) = n*A_mean(n) - (n-1)*A_mean(n-1)
        time_slice = slice('{:%Y-%m-%d}'.format(date),
                           '{:%Y-%m-%d}'.format(date+timedelta(days=1)))
        ds = ds.sel(time=time_slice)
        ds = ds.transpose('time','lat','lon')

    return(ds)


def pp_UM(ds, var_name, dims):
    """
    Preprocess UM model.
    """
    if (dimz in dims) and ('model_level_number' in ds):
        # rename dimensions
        ds = ds.rename({'model_level_number':'alt'})
        # transform altitude coordinate
        hgt_in = np.loadtxt(os.path.join(model_specifics_path, 'UM_hgt.txt'))
        ds['alt'].values = hgt_in[ds['alt'].values.astype(np.int)-1]
    # rename dimensions
    try:
        ds = ds.rename({'latitude':'lat', 'longitude':'lon'})
    except ValueError:
        pass

    # preprocessing of specific variables
    if var_name == 'PP':
        # convert kg/m2/s precip to mm/h
        ds.precipitation_flux.values = ds.precipitation_flux.values * 3600

    # TODO this exception may also ocurr in other variables
    #print(var_name)
    #print(ds.time)
    #quit()
    #if var_name in ['SWUTOA']:
    #    #print(ds.time)
    #    ds.time.values += np.timedelta64(30, 'm')
    #    #print(ds.time)
    #    #quit()
    return(ds)


def pp_MPAS(ds, var_name, date, data_inp_dir, dims):
    """
    Preprocess MPAS model.
    """
    if ( (dimz in dims) and 
         ( ('nVertLevels' in ds.dims) or ('nVertLevelsP1' in ds.dims)) ):
        # rename dimensions and load height levels
        hgt_in = np.loadtxt(os.path.join(model_specifics_path, 'MPAS_hgt.txt'))
        try:
            #print('nVertLevels')
            ds = ds.rename({'nVertLevels':'alt'})
            hgt_in = hgt_in[1:] - np.diff(hgt_in)/2
        except ValueError:
            pass
        try:
            #print('nVertLevelsP1')
            ds = ds.rename({'nVertLevelsP1':'alt'})
        except ValueError:
            pass
        ds['alt'] = hgt_in[np.arange(ds.dims['alt'])]

    # preprocessing of specific variables
    if var_name in ['SWNDTOA']:
        # load last date file and then apply diff to convert
        # accumulated radiative energy to a radiative flux.
        last_date_file = os.path.join(data_inp_dir,
                    '{}_{:%Y%m%d}.nc'.format(var_name,
                                        date-timedelta(days=1)))
        last_date_ds = xr.open_dataset(last_date_file)
        # rename var name to package naming convention
        last_date_ds = last_date_ds.rename(
                {nlm['MPAS']['vkeys'][var_name]:var_name})
        last_time_step = last_date_ds.isel(time=-1)
        ds = xr.concat([last_time_step, ds], dim='time')
        ds = ds.diff(dim='time')
        time_slice = slice('{:%Y-%m-%d}'.format(date),
                           '{:%Y-%m-%d}'.format(date+timedelta(days=1)))
        ds = ds.sel(time=time_slice)
        ds = ds / np.mean(np.diff(ds.time.values)/1E9).astype(float)
    if var_name in ['PPGRID', 'PPCONV']:
        # convert all time accum mm precip to mm/h
        # load last date file and then apply diff
        last_date_file = os.path.join(data_inp_dir,
                    '{}_{:%Y%m%d}.nc'.format(var_name,
                                        date-timedelta(days=1)))
        last_date_ds = xr.open_dataset(last_date_file)
        # rename var name to package naming convention
        last_date_ds = last_date_ds.rename(
                {nlm['MPAS']['vkeys'][var_name]:var_name})
        last_time_step = last_date_ds.isel(time=-1)
        ds = xr.concat([last_time_step, ds], dim='time')
        ds = ds.diff(dim='time')
        time_slice = slice('{:%Y-%m-%d}'.format(date),
                           '{:%Y-%m-%d}'.format(date+timedelta(days=1)))
        ds = ds.sel(time=time_slice)
        ds = ds / np.mean(np.diff(ds.time.values)/1E9).astype(float) * 3600
    return(ds)


def pp_IFS(ds, var_name, date, data_inp_dir, dims, dep_vars={}):
    """
    Preprocess IFS model.
    """
    if (dimz in dims) and ('lev' in ds):

        # skip preprocessing for altitude field because it should
        # become the vertical coordinate later and assumed to be
        # in original format (not preprocessed).
        if var_name == 'ALT': return(ds)

        ## vertical interpolation from plev to alt
        # make sure dependency ALT is here
        if 'ALT' not in dep_vars: raise ValueError('should get dependency ALT')
        # load target altitude (user defined)
        targ_alt = np.sort(np.loadtxt(os.path.join(model_specifics_path,
                    'IFS_mean_alt_20160810_dom_SEA_Sc.dat')))

        # sort to have levels increasing in altitude direction
        # which is required for interpolation
        ds = ds.sortby('lev', ascending=False)
        dep_vars['ALT'] = dep_vars['ALT'].sortby('lev', ascending=False)
        # make sure ALT and preproc var have same time steps
        dep_vars['ALT'], ds = select_common_timesteps(dep_vars['ALT'], ds)
        # interpolate 
        var = interp_plev_to_alt(ds[var_name], dep_vars['ALT'], targ_alt,
                                vdim_name='lev')
        ds[var_name] = var
        #print(ds)
        #var.to_netcdf('test.nc')
        #quit()

        # delete unnecessary stuff
        for key in ['hyai', 'hybi', 'hyam', 'hybm']:
            if key in ds: del ds[key] 


    # preprocessing of specific variables
    if var_name in ['SWNDTOA', 'LWUTOA', 'SLHFLX', 'SSHFLX']:
        # load last date file and then apply diff to convert
        # accumulated radiative energy to a radiative flux.
        last_date_file = os.path.join(data_inp_dir,
                    '{}_{:%Y%m%d}.nc'.format(var_name,
                                        date-timedelta(days=1)))
        last_date_ds = xr.open_dataset(last_date_file)
        # rename var name to package naming convention
        last_date_ds = last_date_ds.rename(
                            {nlm['IFS']['vkeys'][var_name]:var_name})
        last_time_step = last_date_ds.isel(time=-1)
        ds = xr.concat([last_time_step, ds], dim='time')
        ds = ds.diff(dim='time')
        time_slice = slice('{:%Y-%m-%d}'.format(date),
                           '{:%Y-%m-%d}'.format(date+timedelta(days=1)))
        ds = ds.sel(time=time_slice)
        ds = ds / np.mean(np.diff(ds.time.values)/1E9).astype(float)
        ds = ds.transpose('time','lat','lon')

        # convert LWNDTOA to LWUTOA
        if var_name == 'LWUTOA': ds[var_name] *= -1

    if var_name in ['PPCONV', 'PPGRID']:
        # convert kg/m2/s precip to mm/h
        ds = ds * 3600
    return(ds)


def pp_GEOS(ds, var_name, mkey, data_inp_dir, dims, dep_vars={}):
    """
    Preprocess GEOS model.
    """
    if (dimz in dims) and ('lev' in ds):

        # skip preprocessing for altitude field because it should
        # become the vertical coordinate later and assumed to be
        # in original format (not preprocessed).
        if var_name == 'ALT': return(ds)

        ## vertical interpolation from plev to alt
        # make sure dependency ALT is here
        if 'ALT' not in dep_vars: raise ValueError('should get dependency ALT')
        # load target altitude (user defined)
        targ_alt = np.sort(np.loadtxt(os.path.join(model_specifics_path,
                    'GEOS_mean_alt_20160810_dom_SEA_Sc.dat')))

        # sort to have levels increasing in altitude direction
        # which is required for interpolation
        ds = ds.sortby('lev', ascending=False)
        dep_vars['ALT'] = dep_vars['ALT'].sortby('lev', ascending=False)
        # make sure ALT and preproc var have same time steps
        dep_vars['ALT'], ds = select_common_timesteps(dep_vars['ALT'], ds)
        # interpolate 
        var = interp_plev_to_alt(ds[var_name], dep_vars['ALT'], targ_alt,
                                vdim_name='lev')
        ds[var_name] = var

    ## preprocessing of specific variables
    if var_name in ['PPCONV', 'PPGRID']:
        # convert kg/m2/s precip to mm/h
        ds = ds * 3600

    return(ds)


def pp_ARPEGE(ds, var_name, mkey, date, data_inp_dir, dims, dep_vars={}):
    """
    Preprocess ARPEGE model.
    """
    # do this not in dimz part because some 2D vars
    # have height as coordinate.
    if 'height' in ds.coords:
        # rename dimensions
        ds = ds.rename({'height':'alt'})
    if (dimz in dims) and ('lev' in ds):

        # remove levels > 6.5km and < -0.5km
        ds = ds.sel(lev=slice(45,73))

        # skip preprocessing for altitude field because it should
        # become the vertical coordinate later and assumed to be
        # in original format (not preprocessed).
        if var_name == 'ALT':
            # convert from geopotential to altitude
            ds['ALT'] /= CON_G
            ds['ALT'] = add_var_attributes(ds['ALT'], 'ALT')
            return(ds)

        #if var_name in ['W']:
        #    print('rerunning model_pp for W in ARPEGE!!!')
        #    quit()
        #    W_file = os.path.join(inp_base_dir, 'ARPEGE-NH_2.5',
        #                            'SA', 'W_mean.nc')
        #    W_mean = xr.open_dataset(W_file)
        #    W_mean = W_mean.isel(lev=59)

        #    #fig,axes = plt.subplots(1,2, figsize=(10,5))
        #    #cf1 = axes[0].pcolormesh(ds['wz'].isel(lev=59, time=0).values.squeeze(),
        #    #                        vmin=-0.01, vmax=0.01)
        #    #ds['wz'].load()
        #    #print('yoo')
        #    #W_mean['wz'].load()
        #    #print('yoo')
        #    #ds['wz'] = ds['wz'] - W_mean['wz']
        #    ds['wz'].values = ds['wz'].values - W_mean['wz'].values
        #    #ds['wz'].values -= ds['wz'].values - 3. 
        #    #cf2 = axes[1].pcolormesh(ds['wz'].isel(lev=59, time=0).values.squeeze(),
        #    #                        vmin=-0.01, vmax=0.01)
        #    #fig.colorbar(cf1, ax=axes[0])
        #    #fig.colorbar(cf2, ax=axes[1])
        #    #plt.show()
        #    #quit()

        ## vertical interpolation from plev to alt
        # make sure dependency ALT is here
        if 'ALT' not in dep_vars: raise ValueError('should get dependency ALT')
        # load target altitude (user defined)
        targ_alt = np.sort(np.loadtxt(os.path.join(model_specifics_path,
                    'ARPEGE-NH_mean_geopot_20160810_dom_SEA_Sc.dat')))/CON_G 
        # sort to have levels increasing in altitude direction
        # which is required for interpolation
        ds = ds.sortby('lev', ascending=False)
        dep_vars['ALT'] = dep_vars['ALT'].sortby('lev', ascending=False)
        # make sure ALT and preproc var have same time steps
        dep_vars['ALT'], ds = select_common_timesteps(dep_vars['ALT'], ds)
        # interpolate 
        var = interp_plev_to_alt(ds[var_name], dep_vars['ALT'], targ_alt,
                                vdim_name='lev')
        ds[var_name] = var

    ### PREPROCESSING OF SPECIFIC VARIABLES
    # TODO this should be not required anymore
    #var_key = list(ds.data_vars.keys())[0]
    #print(ds[var_key].attrs['units'])
    #print(ds[var_key].attrs['units'] == 'J m**-2')
    if (var_name in ['SWNDTOA', 'LWUTOA']):
        # radiative fluxes are given accumulated on a daily basis.
        # Reset is done at 00:00. Thus 00:30 shows the accumulated
        # flux between 00:00 and 00:30. 06:00 shows the accum.
        # between 00:00 and 06:00.
        # convert to J/m^{2}/(output increment)
        ds = xr.concat([ds.isel(time=[0]), ds.diff(dim='time')],
                        dim='time')
        # convert to W/m^{2}
        ds = ds / np.mean(np.diff(ds.time.values)/1E9).astype(float)
        # adjust units in data array
        ds[var_name].attrs['units'] = 'W m^{-2}'
        #print(ds.mean(dim=['lon', 'lat']).values)
    if var_name in ['PP']:
        # convert from daily accumulated values to mm/h
        # do not load previous values because reset is done after 00:00
        # only (one should however generate the daily files differently..)
        # namely such that 00:00 is part of the last date instead of this date.
        ds = ds.isel(time=range(1,len(ds.time)))
        ds = ds.diff(dim='time')
        ds = ds / np.mean(np.diff(ds.time.values)/1E9).astype(float) * 3600

    return(ds)


def pp_FV3(ds, var_name, mkey, date, data_inp_dir, dims, dep_vars={}):
    """
    Preprocess FV3 model.
    """
    plev_vars = ['ALT', 'QC', 'QV']
    pfull_vars = ['P', 'T', 'U', 'V', 'W'] 
    if dimz in dims:
    
        # skip preprocessing for altitude field because it should
        # become the vertical coordinate later and assumed to be
        # in original format (not preprocessed).
        if var_name == 'ALT': return(ds)

        # the plev variables are given on fewer levels than the pfull
        # variables and therefore are interpolated to the pfull levels
        if var_name in plev_vars:
            #print(ds[var_name])
            #plt.plot(ds[var_name].mean(dim=['lat','lon','time']), ds[var_name].plev)
            ds[var_name] = ds[var_name].interp(plev=dep_vars['ALT'].pfull)
            #print(ds[var_name])
            #plt.plot(ds[var_name].mean(dim=['lat','lon','time']), ds[var_name].pfull)
            #plt.show()
            #quit()
        elif var_name in pfull_var:
            pass
        else:
            raise NotImplementedError()

        # checking because some files contained wrong minute values
        if dt64_to_dt(ds.time.values[0]).minute != 0:
            print(dt64_to_dt(ds.time.values[0]))
            raise ValueError()
            quit()

        ## vertical interpolation from plev to alt
        # make sure dependency ALT is here
        if 'ALT' not in dep_vars: raise ValueError('should get dependency ALT')
        # load target altitude (user defined)
        #if var_name in plev_vars:
        #    targ_alt = np.sort(np.loadtxt(os.path.join(model_specifics_path,
        #                'FV3_mean_alt_plev_2016081_dom_SEA_Sc.dat'))) 
        #    pvar_name = 'pfull'
        #elif var_name in pfull_vars:
        targ_alt = np.sort(np.loadtxt(os.path.join(model_specifics_path,
                    'FV3_mean_alt_pfull_2016081_dom_SEA_Sc.dat'))) 
        pvar_name = 'pfull'
        #else:
        #    raise NotImplementedError()
        # sort to have levels increasing in altitude direction
        # which is required for interpolation
        ds = ds.sortby(pvar_name, ascending=False)
        dep_vars['ALT'] = dep_vars['ALT'].sortby(pvar_name, ascending=False)
        # make sure ALT and preproc var have same time steps
        dep_vars['ALT'], ds = select_common_timesteps(dep_vars['ALT'], ds)
        # interpolate 
        #print(ds[var_name])
        #plt.plot(ds[var_name].mean(dim=['lat','lon','time']), ds[var_name].pfull)
        #plt.show()
        var = interp_plev_to_alt(ds[var_name], dep_vars['ALT'], targ_alt,
                                vdim_name=pvar_name)
        ds[var_name] = var
        #print(ds[var_name])
        #plt.plot(ds[var_name].mean(dim=['lat','lon','time']), ds[var_name].alt)
        #plt.show()
        #quit()


    # CLCT contains this
    if 'grid_xt' in ds.dims.keys():
        ds = ds.rename({'grid_xt':'lon'})
    if 'grid_yt' in ds.dims.keys():
        ds = ds.rename({'grid_yt':'lat'})
    return(ds)





#### 4D PRESSURE INTERPOLATION FUNCTIONS FROM PGW_FOR_ERA5
##################################################################
def interp_logp_4d(var, source_P, targ_P,
                   time_key, lat_key, lon_key, extrapolate='off',
                   no_logp=False):
    """
    Interpolate 3D array in vertical (pressure) dimension using the
    logarithm of pressure.
    extrapolate:
        - off: no extrapolation
        - linear: linear extrapolation
        - constant: constant extrapolation
        - nan: set to nan
    """
    if extrapolate not in ['off', 'linear', 'constant', 'nan']:
        raise ValueError('Invalid input value for "extrapolate"')

    #print(var.shape)
    #print(source_P.shape)
    #print(targ_P.shape)

    if ( (var.shape[0] != source_P.shape[0]) or
         (var.shape[0] != targ_P.shape[0])   ):
         print(source_P.shape)
         print(targ_P.shape)
         raise ValueError('Time dimension of input files is inconsistent!')
    if ( (var.shape[2] != source_P.shape[2]) or
         (var.shape[2] != targ_P.shape[2])   ):
         print(source_P.shape)
         print(targ_P.shape)
         raise ValueError('Lat dimension of input files is inconsistent!')
    if ( (var.shape[3] != source_P.shape[3]) or
         (var.shape[3] != targ_P.shape[3])   ):
         print(source_P.shape)
         print(targ_P.shape)
         raise ValueError('Lon dimension of input files is inconsistent!')

    targ = xr.zeros_like(targ_P)
    tmp = np.zeros_like(targ.values)
    if no_logp:
        interp_1d_for_timelatlon(var.values,
                    source_P.values,
                    targ_P.values,
                    tmp,
                    len(targ_P[time_key]), len(targ_P[lat_key]),
                    len(targ_P[lon_key]),
                    extrapolate)
    else:
        interp_1d_for_timelatlon(var.values,
                    np.log(source_P).values,
                    np.log(targ_P).values,
                    tmp,
                    len(targ_P[time_key]), len(targ_P[lat_key]),
                    len(targ_P[lon_key]),
                    extrapolate)
    targ.values = tmp
    return(targ)

@njit()
def interp_1d_for_timelatlon(orig_array, src_p, targ_p, interp_array,
                        ntime, nlat, nlon, extrapolate):
    """
    Vertical interpolation helper function with numba njit for
    fast performance.
    Loop over time lat and lon dimensions and interpolate each column
    individually
    extrapolate:
        - off: no extrapolation
        - linear: linear extrapolation
        - constant: constant extrapolation
        - nan: set to nan
    """
    for time_ind in range(ntime):
        for lat_ind in range(nlat):
            for lon_ind in range(nlon):
                src_val_col = orig_array[time_ind, :, lat_ind, lon_ind]
                src_p_col = src_p[time_ind, :, lat_ind, lon_ind]
                targ_p_col = targ_p[time_ind, :, lat_ind, lon_ind]

                if src_p_col[-1] < src_p_col[0]:
                    raise ValueError('Source pressure values must be ascending!')
                if targ_p_col[-1] < targ_p_col[0]:
                    raise ValueError('Target pressure values must be ascending!')

                #print(src_val_col)
                #print(src_p_col)
                #print(targ_p_col)

                # all-nan column should be set to all nan
                if np.sum(np.isnan(src_val_col)) == len(src_val_col):
                    interp_col = np.full(len(targ_p_col), np.nan)
                else:
                    # call 1D interpolation function for current column
                    interp_col = interp_extrap_1d(src_p_col, src_val_col,
                                                targ_p_col, extrapolate)

                #print(interp_col)
                #quit()

                interp_array[time_ind, :, lat_ind, lon_ind] = interp_col


@njit()
def interp_extrap_1d(src_x, src_y, targ_x, extrapolate):
    """
    Numba helper function for interpolation of 1d vertical column.
    Does constant extrapolation which is used for the climate deltas.
    extrapolate:
        - off: no extrapolation
        - linear: linear extrapolation
        - constant: constant extrapolation
        - nan: set to nan
    """
    targ_y = np.zeros(len(targ_x))
    for ti in range(len(targ_x)):
        i1 = -1
        i2 = -1
        require_extrap = False
        for si in range(len(src_x)):
            ty = np.nan
            # extrapolate lower end
            if (si == 0) and src_x[si] > targ_x[ti]:
                if extrapolate == 'linear':
                    i1 = si
                    i2 = si + 1
                elif extrapolate == 'constant':
                    i1 = si
                    i2 = si
                require_extrap = True
                break
            # exact match
            elif src_x[si] == targ_x[ti]:
                i1 = si
                i2 = si
                break
            # upper src_x found (interpolation)
            elif src_x[si] > targ_x[ti]:
                i1 = si - 1
                i2 = si
                break
            # we are still smaller than targ_x[ti]
            else:
                pass

        # extrapolate upper end
        if i1 == -1:
            if extrapolate == 'linear':
                i1 = len(src_x) - 2
                i2 = len(src_x) - 1
            elif extrapolate == 'constant':
                i1 = len(src_x) - 1
                i2 = len(src_x) - 1
            require_extrap = True

        # raise value if extrapolation is required but not enabled.
        if require_extrap and extrapolate == 'off':
            raise ValueError('Extrapolation deactivated but data '+
                             'out of bounds.')

        # interpolate/extrapolate values
        if require_extrap and extrapolate == 'nan':
            targ_y[ti] = np.nan
        else:
            if i1 == i2:
                targ_y[ti] = src_y[i1]
            else:
                targ_y[ti] = (
                    src_y[i1] + (targ_x[ti] - src_x[i1]) *
                    (src_y[i2] - src_y[i1]) / (src_x[i2] - src_x[i1])
                )

    return(targ_y)
