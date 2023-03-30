#!/usr/bin/python
# -*- coding: utf-8 -*-
#title			:calc_RHO.py
#description	:Calculate the air density and store.
#author			:Christoph Heim
#date			:20190423
#version		:1.00
#usage			:python calc_RHO.py
#notes			:
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


def calc_rho(ts, task_no, member_dict, var_dicts, rho_dict):
    
    loaders = {}
    for var_name,dict in var_dicts.items():
        loader = FieldLoader(var_name, member_dict,
                    var_dicts[var_name], 
                    NL.chunks)
        loader.load_timesteps(ts)
        loaders[var_name] = loader
    
    hydrotot = copy.deepcopy(loaders['QC'].field)
    for var_name in ['QR', 'QI', 'QS', 'QG']:
        hydrotot = hydrotot + loaders[var_name].field

    tempFactor = loaders['QV'].field*0.622 + 1 - hydrotot 
    Tdens = loaders['T'].field*tempFactor 
    Rd = 287.1
    rho = loaders['P'].field/(Tdens*Rd)

    new_attr = {
        'standard_name':'air_density',
        'long_name':'air_density',
        'units':'kg m-3',
        'grid_mapping':loaders['QV'].field.attrs['grid_mapping'],
    }
    rho_loader = loaders['QC'].clone_to_new_field(
                                'RHO', rho, new_attr, rho_dict)

    if rho_loader.is_cloned:
        rho_loader.save_field_to_nc(skip_existing=False)

    #rho_loader.subselect(alt=slice(100, 100))
    #rho_loader.field = rho_loader.field.mean(dim=['altitude'])
    #print(rho_loader.field)
    #print(rho_loader.field.shape)
    #quit()

    return(rho_loader)



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
                         'QC':VNL['QC'],
                         'QR':VNL['QR'],
                         'QI':VNL['QI'],
                         'QS':VNL['QS'],
                         'QG':VNL['QG'],
                         'T':VNL['T'],
                         'P':VNL['P']},
            'rho_dict':VNL['RHO'],
            }

        step_args = []
        for i,dt in enumerate(dt_range[member_dict['dt']]):
            step_args.append({'task_no':i})
            
        TSMP = TimeStepMP(dt_range[member_dict['dt']])
        TSMP.run(func=calc_rho, fargs=fargs, step_args=step_args)

        t1 = time.time()
        print(t1 - t0)

    t1 = time.time()
    print(t1 - t00)



