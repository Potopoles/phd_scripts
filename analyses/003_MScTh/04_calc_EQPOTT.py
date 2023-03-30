#!/usr/bin/python
# -*- coding: utf-8 -*-
#title			:calc_EQPOTT.py
#description	:Calculate the equivalent potential temperature and store.
#author			:Christoph Heim
#date			:20190510
#version		:1.00
#usage			:python calc_EQPOTT.py
#notes			:calculated according to Stull 1988, p546 (see wikipedia)
#python_version	:3.7.7
#==============================================================================
import collections, time, copy
from datetime import datetime
import namelist as NL
from package.Variable import Variable
from package.variable_namelist import VNL
from package.MP import TimeStepMP
from package.FieldLoader import FieldLoader
from package.functions import get_dt_range


def calc_eqpott(ts, task_no, member_dict, var_dicts, eqpott_dict):
    
    loaders = {}
    for var_name,dict in var_dicts.items():
        loader = FieldLoader(var_name, member_dict,
                    var_dicts[var_name], 
                    NL.chunks)
        loader.load_timesteps(ts)
        loaders[var_name] = loader

    # latent heat of evaporation
    L_v = 2400000 # J/kg at 25°C
    # specific heat at constant pressure
    cpd = 1004 # J/(kg K)
    # reference pressure
    p0 = 1E5 # Pa
    # Rd/cpd
    kd = 0.2854

    # equivalent temperature
    eqt = loaders['T'].field + L_v/cpd * loaders['QV'].field 
    # equivalent potential temperature
    eqpott = eqt * (p0/loaders['P'].field)**kd

    new_attr = {
        'standard_name':'equivalent_potential_temperature',
        'long_name':'equivalent_potential_temperature',
        'units':'K',
        'grid_mapping':loaders['QV'].field.attrs['grid_mapping'],
    }
    eqpott_loader = loaders['QV'].clone_to_new_field(
                                'EQPOTT', eqpott, new_attr, eqpott_dict)

    if eqpott_loader.is_cloned:
        eqpott_loader.save_field_to_nc(skip_existing=False)

    return(eqpott_loader)



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
                         'T':VNL['T'],
                         'P':VNL['P']},
            'eqpott_dict':VNL['EQPOTT'],
            }

        step_args = []
        for i,dt in enumerate(dt_range[member_dict['dt']]):
            step_args.append({'task_no':i})
            
        TSMP = TimeStepMP(dt_range[member_dict['dt']])
        TSMP.run(func=calc_eqpott, fargs=fargs, step_args=step_args)

        t1 = time.time()
        print(t1 - t0)

    t1 = time.time()
    print(t1 - t00)



