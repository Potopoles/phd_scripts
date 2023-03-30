#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
"""
##############################################################################
import argparse, os
import xarray as xr
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from functions import (
    specific_to_relative_humidity,
    relative_to_specific_humidity,
    load_delta,
    load_delta_interp,
    integ_geopot,
    interp_logp_4d,
    determine_p_ref,
    )
from constants import CON_G, CON_RD
from parallel import IterMP
from settings import (
    i_debug,
    era5_file_name_base,
    var_name_map,
    TIME_ERA, LEV_ERA, HLEV_ERA, LON_ERA, LAT_ERA, SOIL_HLEV_ERA,
    TIME_GCM, PLEV_GCM,
    i_reinterp,
    p_ref_inp,
    thresh_phi_ref_max_error,
    max_n_iter,
    adj_factor,
    )

import matplotlib.pyplot as plt
##############################################################################

def aggreg_lat_lon(ds):
    #lon_ind = 0
    #lat_ind = 0
    #return(ds.isel(lon=lon_ind, lat=lat_ind))
    return(ds.mean(dim=['lon','lat']))

def pgw_for_era5(inp_era_file_path, out_era_file_path,
                delta_input_dir, era_step_dt,
                ignore_top_pressure_error,
                debug_mode=None):
    if i_debug >= 0:
        print('Start working on input file {}'.format(inp_era_file_path))

    #########################################################################
    ### PREPARATION STEPS
    #########################################################################
    # containers for variable computation
    vars_era = {}
    vars_pgw = {}
    deltas = {}

    # open data set
    era_file = xr.open_dataset(inp_era_file_path, decode_cf=False)

    ## compute pressure on ERA5 full levels and half levels
    # pressure on half levels
    pa_hl_era = (era_file.ak + 
                era_file[var_name_map['ps']] * era_file.bk).transpose(
                TIME_ERA, HLEV_ERA, LAT_ERA, LON_ERA)
    # if akm and akb coefficients (for full levels) exist, use them
    if 'akm' in era_file:
        akm = era_file.akm
        bkm = era_file.bkm
    # if akm and abk  coefficients do not exist, computed them
    # with the average of the half-level coefficients above and below
    else:
        akm = (
            0.5 * era_file.ak.diff(
            dim=HLEV_ERA, 
            label='lower').rename({HLEV_ERA:LEV_ERA}) + 
            era_file.ak.isel({HLEV_ERA:range(len(era_file.level1)-1)}).values
        )
        bkm = (
            0.5 * era_file.bk.diff(
            dim=HLEV_ERA, 
            label='lower').rename({HLEV_ERA:LEV_ERA}) + 
            era_file.bk.isel({HLEV_ERA:range(len(era_file.level1)-1)}).values
        )
    # pressure on full levels
    pa_era = (akm + era_file[var_name_map['ps']] * bkm).transpose(
                TIME_ERA, LEV_ERA, LAT_ERA, LON_ERA)

    # compute relative humidity in ERA climate state
    era_file[var_name_map['hur']] = specific_to_relative_humidity(
                        era_file[var_name_map['hus']], 
                        pa_era, era_file[var_name_map['ta']]).transpose(
                        TIME_ERA, LEV_ERA, LAT_ERA, LON_ERA)

    #########################################################################
    ### START UPDATING 3D FIELDS
    #########################################################################
    # If no re-interpolation is done, the final PGW climate state
    # variables can be computed already now, before updating the 
    # surface pressure. This means that the climate deltas or
    # interpolated on the ERA5 model levels of the ERA climate state.
    if not i_reinterp:

        ### interpolate climate deltas onto ERA5 grid
        for var_name in ['ta','hur']:#,'ua','va']:
            if i_debug >= 2:
                print('update {}'.format(var_name))

            ## interpolate climate deltas to ERA5 model levels
            ## use ERA climate state
            delta_var = load_delta_interp(delta_input_dir,
                    var_name, pa_era, era_file[TIME_ERA], era_step_dt,
                    ignore_top_pressure_error)
            deltas[var_name] = delta_var

            ## compute PGW climate state variables
            vars_pgw[var_name] = (
                    era_file[var_name_map[var_name]] + 
                    deltas[var_name]
            )

            # convert relative humidity to specific humidity
            # take PGW climate state temperature and relative humidity
            # but assume ERA climate state pressure
            if var_name == 'hur':
                vars_pgw['hus'] = relative_to_specific_humidity(
                                vars_pgw['hur'], pa_era, vars_pgw['ta'])


    #########################################################################
    ### UPDATE SURFACE PRESSURE USING ITERATIVE PROCEDURE
    #########################################################################
    p_ref_opts = load_delta(delta_input_dir, 'zg',
                        era_file[TIME_ERA], era_step_dt)[PLEV_GCM]
    #p_refs = p_ref_opts.values[p_ref_opts.values >= 90000]
    #p_refs = p_ref_opts.values[p_ref_opts.values >= 70000]
    #p_refs = p_ref_opts.values[p_ref_opts.values >= 30000]
    p_refs = p_ref_opts.values[p_ref_opts.values >= 10000]
    climate_delta_ta = aggreg_lat_lon(load_delta(delta_input_dir, 'ta',
                era_file[TIME_ERA], era_step_dt)).isel(time=0).sel(plev=p_refs).values
    climate_delta_hur = aggreg_lat_lon(load_delta(delta_input_dir, 'hur',
                era_file[TIME_ERA], era_step_dt)).isel(time=0).sel(plev=p_refs).values
    output = {
        'climate_delta_ta':climate_delta_ta,
        'climate_delta_hur':climate_delta_hur,
        'p_refs':p_refs,
        'delta_phi_ref':[],
        'delta_ps':[],
        'climate_delta_phi_ref':[],
    }
    #print(output)
    #quit()
    for p_ref in p_refs:
        print('########################################################')
        print('########################################################')
        print('########################################################')
        print(p_ref)
        print('########################################################')
        print('########################################################')
        print('########################################################')

        if i_debug >= 2:
            print('###### Start with iterative surface pressure adjustment.')
        # change in surface pressure between ERA and PGW climate states
        delta_ps = xr.zeros_like(era_file[var_name_map['ps']])
        # increment to adjust delta_ps with each iteration
        adj_ps = xr.zeros_like(era_file[var_name_map['ps']])
        # maximum error in geopotential (used in iteration)
        phi_ref_max_error = np.inf

        it = 1
        while phi_ref_max_error > thresh_phi_ref_max_error:

            # update surface pressure
            delta_ps += adj_ps
            ps_pgw = era_file[var_name_map['ps']] + delta_ps

            # recompute pressure on full and half levels
            pa_pgw = (akm + ps_pgw * bkm).transpose(
                        TIME_ERA, LEV_ERA, LAT_ERA, LON_ERA)
            pa_hl_pgw = (era_file.ak + ps_pgw * era_file.bk).transpose(
                        TIME_ERA, HLEV_ERA, LAT_ERA, LON_ERA)


            if i_reinterp:
                # interpolate ERA climate state variables as well as
                # climate deltas onto updated model levels, and
                # compute PGW climate state variables
                for var_name in ['ta', 'hur']:
                    vars_era[var_name] = interp_logp_4d(
                                    era_file[var_name_map[var_name]], 
                                    pa_era, pa_pgw, extrapolate='constant')
                    deltas[var_name] = load_delta_interp(delta_input_dir,
                                                    var_name, pa_pgw,
                                                    era_file[TIME_ERA], era_step_dt,
                                                    ignore_top_pressure_error)
                    vars_pgw[var_name] = vars_era[var_name] + deltas[var_name]

                # convert relative humidity to speicifc humidity in pgw
                vars_pgw['hus'] = relative_to_specific_humidity(
                                vars_pgw['hur'], pa_pgw, vars_pgw['ta'])


            # compute updated geopotential at reference pressure
            phi_ref_pgw = integ_geopot(pa_hl_pgw, era_file.FIS, vars_pgw['ta'], 
                                        vars_pgw['hus'], era_file[HLEV_ERA], p_ref)
            # recompute original geopotential
            phi_ref_era = integ_geopot(pa_hl_era, era_file.FIS,
                                        era_file[var_name_map['ta']], 
                                        era_file[var_name_map['hus']], 
                                        era_file[HLEV_ERA], p_ref)

            delta_phi_ref = phi_ref_pgw - phi_ref_era

            if it == 1:
                output['delta_phi_ref'].append(aggreg_lat_lon(delta_phi_ref).values)

            ## load climate delta for reference pressure level
            climate_delta_phi_ref = load_delta(delta_input_dir, 'zg',
                                era_file[TIME_ERA], era_step_dt) * CON_G
            climate_delta_phi_ref = climate_delta_phi_ref.sel({PLEV_GCM:p_ref})
            del climate_delta_phi_ref[PLEV_GCM]

            # error in future geopotential
            phi_ref_error = delta_phi_ref - climate_delta_phi_ref

            adj_ps = - adj_factor * ps_pgw / (
                    CON_RD * 
                    vars_pgw['ta'].sel({LEV_ERA:np.max(era_file[LEV_ERA])})
                ) * phi_ref_error
            if LEV_ERA in adj_ps.coords:
                del adj_ps[LEV_ERA]

            phi_ref_max_error = np.abs(phi_ref_error).max().values
            if i_debug >= 2:
                print('### iteration {:03d}, phi max error: {}'.
                                format(it, phi_ref_max_error))

            it += 1

            if it > max_n_iter:
                raise ValueError('ERROR! Pressure adjustment did not converge '+
                      'for file {}. '.format(inp_era_file_path) +
                      'Consider increasing the value for "max_n_iter" in ' +
                      'settings.py')

        output['climate_delta_phi_ref'].append(aggreg_lat_lon(climate_delta_phi_ref).values)
        output['delta_ps'].append(aggreg_lat_lon(delta_ps).values)

    return(output)




##############################################################################
if __name__ == "__main__":
    ## input arguments
    input_dir = os.path.join('/net/o3/hymet_nobackup/heimc/data/pgw/ERA/paper_plot_ERA5')
    delta_input_dirs = {
        'Amon':os.path.join('/net/o3/hymet_nobackup/heimc/data/pgw/deltas/regridded_paper_plot/Amon/MPI-ESM1-2-HR'),
        'Emon':os.path.join('/net/o3/hymet_nobackup/heimc/data/pgw/deltas/regridded_paper_plot/Emon/MPI-ESM1-2-HR'),
    }
    first_era_step = '2006080100'
    last_era_step = '2006080100'
    hour_inc_step = 3
    ignore_top_pressure_error = 0
    debug_mode = None
    ##########################################################################

    # first date and last date to datetime object
    first_era_step = datetime.strptime(first_era_step, '%Y%m%d%H')
    last_era_step = datetime.strptime(last_era_step, '%Y%m%d%H')

    # time steps to process
    era_step_dts = np.arange(first_era_step,
                        last_era_step+timedelta(hours=hour_inc_step),
                        timedelta(hours=hour_inc_step)).tolist()

    run_type_outputs = dict(Amon=None,Emon=None)
    #run_type_outputs = dict(Amon=None)

    for run_type,output in run_type_outputs.items():
        fargs = dict(
            delta_input_dir = delta_input_dirs[run_type],
            ignore_top_pressure_error = ignore_top_pressure_error,
            debug_mode = debug_mode,
        )
        step_args = []

        ##########################################################################
        # iterate over time step and prepare function arguments
        for era_step_dt in era_step_dts:
            print(era_step_dt)

            # set output and input ERA5 file
            inp_era_file_path = os.path.join(input_dir, 
                    era5_file_name_base.format(era_step_dt))
            out_era_file_path = os.path.join('/')

            step_args.append(dict(
                inp_era_file_path = inp_era_file_path,
                out_era_file_path = out_era_file_path,
                era_step_dt = era_step_dt
                )
            )

        output = pgw_for_era5(**fargs, **step_args[0])
        run_type_outputs[run_type] = output

    ## run in parallel if args.n_par > 1
    #IMP.run(run_function, fargs, step_args)

    #output = IMP.output

    fig,axes = plt.subplots(2,2, figsize=(6,6))

    axlims = {
        'ta':(1.5,5.5),
        'hur':(-10,10),
        'pa':(1000,100),
        'phi':(-10,10),
        'ps':(-1,1),
    }


    i = 0
    for run_type,output in run_type_outputs.items():
        print(output)
        quit()

        #### preparation
        error_delta_phi_ref = np.asarray(output['delta_phi_ref']) - np.asarray(output['climate_delta_phi_ref']) -3.6*9.81 # -3.6 to account for error we get at lowest level due to non-zero surface elevation in MPI-ESM1-2-HR over sea (spectral features).
        climate_delta_ps = -42
        error_delta_ps = (np.asarray(output['delta_ps']) - climate_delta_ps) / 100
        p_refs = np.asarray(output['p_refs'])/100

        #### plot temperature delta
        ax = axes[i,0]
        ax.set_title('{} climate deltas'.format(run_type))
        ax.plot(output['climate_delta_ta'], p_refs, color='orange')
        ax.set_xlabel('$\Delta$T [K]')
        ax.set_ylabel('p [hPa]')
        ax.set_xlim(axlims['ta'])
        ax.set_ylim(axlims['pa'])
        # format axis color
        ax.spines['bottom'].set_color('orange')
        ax.xaxis.label.set_color('orange')
        ax.tick_params(axis='x', colors='orange')

        #### plot relative humidity delta
        ax2 = ax.twiny()
        ax2.plot(output['climate_delta_hur'], p_refs, color='blue')
        ax2.set_xlabel('$\Delta RH$ [%]')
        ax2.set_xlim(axlims['hur'])
        # format axis color
        ax2.spines['top'].set_color('blue')
        ax2.xaxis.label.set_color('blue')
        ax2.tick_params(axis='x', colors='blue')

        #### plot geopotential delta
        ax = axes[i,1]
        ax.set_title('{} pressure adjustment'.format(run_type))
        ax.plot(error_delta_phi_ref/9.81, p_refs, color='k')
        ax.set_xlabel('error $\Delta \phi$ [m]')
        ax.set_ylabel('p [hPa]')
        ax.set_xlim(axlims['phi'])
        ax.set_ylim(axlims['pa'])

        #### plot pressure adjustment delta
        color = 'red'
        ax2 = ax.twiny()
        ax2.plot(error_delta_ps, p_refs, color=color)
        ax2.set_xlabel('error $\Delta p_{sfc}$ [hPa]')
        ax2.set_xlim(axlims['ps'])
        # format axis color
        ax2.spines['top'].set_color(color)
        ax2.xaxis.label.set_color(color)
        ax2.tick_params(axis='x', colors=color)

        i += 1

    fig.tight_layout()
    #plt.show()
    fig.savefig('/net/o3/hymet_nobackup/heimc/plots/005_long/Figure_SLP_adjustment.pdf')
    quit()



