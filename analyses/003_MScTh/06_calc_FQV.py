#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Calculate vapor fluxes in any direction
author			Christoph Heim
date created    23.04.2019
date changed    29.01.2020
usage           use in another script
"""
###############################################################################
import os, collections, time, copy
import numpy as np
from datetime import datetime
from pathlib import Path
import namelist as NL
from package.nl_variables import nlv
from package.MP import TimeStepMP
from package.field_io import FieldLoader
from package.functions import get_dt_range
###############################################################################


def calc_fqvz(ts, task_no, member_dict, var_dicts):
    loaders = {}
    for var_name,dict in var_dicts.items():
        loader = FieldLoader(var_name, member_dict,
                    var_dicts[var_name], 
                    NL.chunks)
        loader.load_timesteps(ts, dict['nc_prefix'], dict['nc_key'])
        loaders[var_name] = loader

    new_var_key = 'FQVZ'
    fqv = ( loaders['W'].field     *
             loaders['RHO'].field   *
             loaders['QV'].field    )
    new_attr = {
        'standard_name':'vertical_qv_flux',
        'long_name':'resolved_vertical_water_vapor_flux',
        'units':'kg m-2 s-1',
        'grid_mapping':loaders['QV'].field.attrs['grid_mapping'],
    }
    output_path = os.path.join(loaders['QV'].member_dict['inp_path'], 'calc', new_var_key,
                  'lffd{0:%Y%m%d%H}z.nc'.format(ts))

    for key,value in new_attr.items():
        fqv.attrs[key] = value
    fqv = fqv.rename(new_var_key)

    if os.path.exists(output_path):
        os.remove(output_path)
    fqv.to_netcdf(output_path, encoding={new_var_key:{'_FillValue':np.nan}})
    
    #fqvz = ( loaders['W'].field     *
    #         loaders['RHO'].field   *
    #         loaders['QV'].field    )

    #fqvz_loader = loaders['QV'].clone_to_new_field(
    #                            'FQVZ', fqvz, new_attr, fqvz_dict)

    #if fqvz_loader.is_cloned:
    #    fqvz_loader.save_field_to_nc(skip_existing=False)


    #return(fqvz_loader)


def calc_fqvx(ts, task_no, member_dict, var_dicts):
    loaders = {}
    for var_name,dict in var_dicts.items():
        loader = FieldLoader(var_name, member_dict,
                    var_dicts[var_name], 
                    NL.chunks)
        loader.load_timesteps(ts, dict['nc_prefix'], dict['nc_key'])
        loaders[var_name] = loader

    new_var_key = 'FQVX'
    fqv_vals = ( loaders['U'].field.values     *
                 loaders['RHO'].field.values   *
                 loaders['QV'].field.values    )
    fqv = loaders['QV'].field.copy()
    fqv.values = fqv_vals


    new_attr = {
        'standard_name':'zonal_qv_flux',
        'long_name':'resolved_zonal_water_vapor_flux',
        'units':'kg m-2 s-1',
        'grid_mapping':loaders['QV'].field.attrs['grid_mapping'],
    }
    out_dir = os.path.join(loaders['QV'].member_dict['inp_path'], 'calc', new_var_key)
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    output_path = os.path.join(out_dir, 'lffd{0:%Y%m%d%H}z.nc'.format(ts))

    for key,value in new_attr.items():
        fqv.attrs[key] = value
    fqv = fqv.rename(new_var_key)

    if os.path.exists(output_path):
        os.remove(output_path)
    fqv.to_netcdf(output_path, encoding={new_var_key:{'_FillValue':np.nan}})



def calc_fqvy(ts, task_no, member_dict, var_dicts):
    loaders = {}
    for var_name,dict in var_dicts.items():
        loader = FieldLoader(var_name, member_dict,
                    var_dicts[var_name], 
                    NL.chunks)
        loader.load_timesteps(ts, dict['nc_prefix'], dict['nc_key'])
        loaders[var_name] = loader

    new_var_key = 'FQVY'
    fqv_vals = ( loaders['V'].field.values     *
                 loaders['RHO'].field.values   *
                 loaders['QV'].field.values    )
    fqv = loaders['QV'].field.copy()
    fqv.values = fqv_vals
    new_attr = {
        'standard_name':'meridional_qv_flux',
        'long_name':'resolved_meridional_water_vapor_flux',
        'units':'kg m-2 s-1',
        'grid_mapping':loaders['QV'].field.attrs['grid_mapping'],
    }
    out_dir = os.path.join(loaders['QV'].member_dict['inp_path'], 'calc', new_var_key)
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    output_path = os.path.join(out_dir, 'lffd{0:%Y%m%d%H}z.nc'.format(ts))

    for key,value in new_attr.items():
        fqv.attrs[key] = value
    fqv = fqv.rename(new_var_key)

    if os.path.exists(output_path):
        os.remove(output_path)
    fqv.to_netcdf(output_path, encoding={new_var_key:{'_FillValue':np.nan}})







if __name__ == '__main__':

    t00 = time.time()

    ### PREPARATIONS 
    # date ranges
    dt_range = get_dt_range(NL.first_date, NL.last_date)

    # select members
    member_dicts = {}
    for member_key,member_dict in NL.member_dicts.items():
        if member_key in NL.use_members:
            member_dicts[member_key] = member_dict

    # RUN CALCULATIONS
    members = {}
    for member_key,member_dict in member_dicts.items():
        t0 = time.time()
        print(member_key)
        qv_dict = nlv['QV']
        qv_dict.update({'nc_prefix':'zlev','nc_key':'QV'})
        u_dict = nlv['U']
        u_dict.update({'nc_prefix':'zlev','nc_key':'U'})
        v_dict = nlv['V']
        v_dict.update({'nc_prefix':'zlev','nc_key':'V'})
        w_dict = nlv['W']
        w_dict.update({'nc_prefix':'zlev','nc_key':'W'})
        rho_dict = nlv['RHO']
        rho_dict.update({'nc_prefix':'calc','nc_key':'RHO'})
        if NL._06['direction'] == 'z':
            fargs = {
                'member_dict':member_dict,
                'var_dicts':{'QV':qv_dict,
                             'W':w_dict,
                             'RHO':rho_dict},
                }
        elif NL._06['direction'] == 'x':
            fargs = {
                'member_dict':member_dict,
                'var_dicts':{'QV':nlv['QV'],
                             'U':nlv['U'],
                             'RHO':nlv['RHO']},
                }
        elif NL._06['direction'] == 'y':
            fargs = {
                'member_dict':member_dict,
                'var_dicts':{'QV':nlv['QV'],
                             'V':nlv['V'],
                             'RHO':nlv['RHO']},
                }

        step_args = []
        for i,dt in enumerate(dt_range[member_dict['dt']]):
            step_args.append({'task_no':i})
            
        TSMP = TimeStepMP(dt_range[member_dict['dt']])
        if NL._06['direction'] == 'z':
            TSMP.run(func=calc_fqvz, fargs=fargs, step_args=step_args)
        elif NL._06['direction'] == 'x':
            TSMP.run(func=calc_fqvx, fargs=fargs, step_args=step_args)
        elif NL._06['direction'] == 'y':
            TSMP.run(func=calc_fqvy, fargs=fargs, step_args=step_args)

        t1 = time.time()
        print(t1 - t0)

    t1 = time.time()
    print(t1 - t00)



