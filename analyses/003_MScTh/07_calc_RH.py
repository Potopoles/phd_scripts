#!/usr/bin/python
# -*- coding: utf-8 -*-
#title			:calc_RH.py
#description	:Calculate the relative humidity and store.
#author			:Christoph Heim
#created		:20190513
#modified		:20190513
#usage			:python calc_RH.py $n_jobs
#notes			:
#python_version	:3.7.1
#==============================================================================
import collections, time, copy
from datetime import datetime
import numpy as np
import namelist as NL
from package.Variable import Variable
from package.variable_namelist import VNL
from package.MP import TimeStepMP
from package.FieldLoader import FieldLoader
from package.functions import get_dt_range


def calc_rh(ts, task_no, member_dict, var_dicts, rh_dict):
    
    loaders = {}
    for var_name,dict in var_dicts.items():
        loader = FieldLoader(var_name, member_dict,
                    var_dicts[var_name], 
                    NL.chunks)
        loader.load_timesteps(ts)
        loaders[var_name] = loader

    # from master thesis
    #eps = 0.622
    #loaders['T'].field = loaders['T'].field - 273.15
    ## vapor pressure
    #e = ( loaders['P'].field * loaders['QV'].field /
    #      ( eps + loaders['QV'].field ))
    ## saturation vapor pressure
    #es = 611 * np.exp(17.27 * loaders['T'].field /
    #                    (273.3 + loaders['T'].field))
    #rh = e / es * 100

    #https://earthscience.stackexchange.com/questions/2360/
    #how-do-i-convert-specific-humidity-to-relative-humidity
    rh = ( 0.263 * loaders['P'].field * loaders['QV'].field *
            np.exp( 17.67 * (loaders['T'].field - 273.16) /
                    ( loaders['T'].field - 29.65 ) )**(-1) )

    new_attr = {
        'standard_name':'relative_humidity',
        'long_name':'relative_humidity',
        'units':'%',
        'grid_mapping':loaders['QV'].field.attrs['grid_mapping'],
    }
    rh_loader = loaders['QV'].clone_to_new_field(
                                'RH', rh, new_attr, rh_dict)

    if rh_loader.is_cloned:
        rh_loader.save_field_to_nc(skip_existing=False)

    return(rh_loader)



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
        fargs = {
            'member_dict':member_dict,
            'var_dicts':{'QV':VNL['QV'],
                         'P':VNL['P'],
                         'T':VNL['T']},
            'rh_dict':VNL['RH'],
            }

        step_args = []
        for i,dt in enumerate(dt_range[member_dict['dt']]):
            step_args.append({'task_no':i})
            
        TSMP = TimeStepMP(dt_range[member_dict['dt']])
        TSMP.run(func=calc_rh, fargs=fargs, step_args=step_args)

        t1 = time.time()
        print(t1 - t0)

    t1 = time.time()
    print(t1 - t00)



