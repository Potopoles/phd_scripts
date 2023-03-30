#!/usr/bin/python
# -*- coding: utf-8 -*-
#title			:calc_WVP.py
#description	:Calculate the water vapor path between two heights
#                and store.
#author			:Christoph Heim
#date			:20190426
#version		:1.00
#usage			:python calc_WVP.py
#notes			:
#python_version	:3.7.7
#==============================================================================
import matplotlib.pyplot as plt
import collections, time, copy
from datetime import datetime
import numpy as np
import namelist as NL
from package.variable import Variable
from package.nl_variables import nlv as VNL
from package.MP import TimeStepMP
from package.field_io import FieldLoader
from package.functions import get_dt_range


def calc_wvp(ts, task_no, member_dict, var_dicts, wvp_dict, height_lims):

    
    loaders = {}
    for var_name,dict in var_dicts.items():
        loader = FieldLoader(var_name, member_dict,
                    var_dicts[var_name], chunks=NL.chunks)
        loader.load_timesteps(ts)
        loaders[var_name] = loader
    
    # water vapor mass
    wvm = loaders['RHO'].field*loaders['QV'].field

    # subselect vertical segment
    wvm = wvm.sel(altitude=slice(height_lims[0],height_lims[1]))

    # integrate vertically (and set nan to zero because integrate
    # does not know nan-treatment)
    wvm = wvm.where(~np.isnan(wvm),0)
    wvp = wvm.integrate(dim='altitude')

    # create FieldLoader instance for WVP
    height_lim_str = str(height_lims[0])+'_and_'+str(height_lims[1])+'_m'
    new_attr = {
        'standard_name':'water_wapor_path',
        'long_name':'water_vapor_path_between_'+height_lim_str,
        'units':'kg m-2',
        'grid_mapping':loaders['QV'].field.attrs['grid_mapping'],
    }
    wvp_loader = loaders['QV'].clone_to_new_field(
                            wvp_dict['sh_name'], wvp, new_attr, wvp_dict)
    if wvp_loader.is_cloned:
        wvp_loader.save_field_to_nc(skip_existing=False)

    return(wvp_loader)





def calc_lwp(ts, task_no, member_dict, var_dicts, lwp_dict, height_lims):

    
    loaders = {}
    for var_name,dict in var_dicts.items():
        loader = FieldLoader(var_name, member_dict,
                    var_dicts[var_name], chunks=NL.chunks)
        loader.load_timesteps(ts)
        loaders[var_name] = loader
    
    # cloud water mass
    lwm = loaders['RHO'].field*(loaders['QC'].field + loaders['QR'].field)

    # subselect vertical segment
    lwm = lwm.sel(altitude=slice(height_lims[0],height_lims[1]))

    # integrate vertically (and set nan to zero because integrate
    # does not know nan-treatment)
    lwm = lwm.where(~np.isnan(lwm),0)
    lwp = lwm.integrate(dim='altitude')

    # create FieldLoader instance for WVP
    height_lim_str = str(height_lims[0])+'_and_'+str(height_lims[1])+'_m'
    new_attr = {
        'standard_name':'liquid_water_path',
        'long_name':'liquid_water_path_between_'+height_lim_str,
        'units':'kg m-2',
        'grid_mapping':loaders['QC'].field.attrs['grid_mapping'],
    }
    lwp_loader = loaders['QC'].clone_to_new_field(
                            lwp_dict['sh_name'], lwp, new_attr, lwp_dict)
    if lwp_loader.is_cloned:
        lwp_loader.save_field_to_nc(skip_existing=False)

    return(lwp_loader)





if __name__ == '__main__':
    t00 = time.time()

    calc_var = (NL.calc_var + '_' + str(int(NL.height_lims[0]/1000)) + 
                    '_' + str(int(NL.height_lims[1]/1000)))
    print('Calculate ' + calc_var)

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
        if NL.calc_var == 'WVP':
            fargs = {
                'member_dict':member_dict,
                'var_dicts':{'QV':VNL['QV'],
                             'RHO':VNL['RHO']},
                'wvp_dict':VNL[calc_var],
                'height_lims':NL.height_lims,
                }
            run_func = calc_wvp
        elif NL.calc_var == 'LWP':
            fargs = {
                'member_dict':member_dict,
                'var_dicts':{'QR':VNL['QR'],
                             'QC':VNL['QC'],
                             'RHO':VNL['RHO']},
                'lwp_dict':VNL[calc_var],
                'height_lims':NL.height_lims,
                }
            run_func = calc_lwp

        step_args = []
        for i,dt in enumerate(dt_range[member_dict['dt']]):
            step_args.append({'task_no':i})
            
        TSMP = TimeStepMP(dt_range[member_dict['dt']])
        TSMP.run(func=run_func, fargs=fargs, step_args=step_args)

        t1 = time.time()
        print(t1 - t0)

    t1 = time.time()
    print(t1 - t00)



