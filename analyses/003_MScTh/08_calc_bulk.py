#!/usr/bin/python
# -*- coding: utf-8 -*-
#title			:calc_bulk.py
#description	:Calculate bulk tendencies for subvolumes.
#author			:Christoph Heim
#created		:20190522
#modified		:20190522
#usage			:python calc_bulk.py $n_jobs
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


def calc_bulk(ts, task_no, member_dict, var_dicts):
    
    loaders = {}
    for var_name,dict in var_dicts.items():
        loader = FieldLoader(var_name, member_dict,
                    var_dicts[var_name], 
                    NL.chunks)
        loader.load_timesteps(ts)
        loaders[var_name] = loader

        loader.sel_subdomain(NL._08['domain'])
        loader.field = loader.field.sel(altitude=NL._08['altitudes'])

    area = loader.calc_rotated_cell_area()
    print((np.max(area)/np.min(area)-1)*100)
    quit()

    #alts = loaders['RHO'].field.coords['altitude']
    #dz = (alts + alts.diff('altitude', label='lower')/2).values.tolist()
    #dz.append(alts.values[-1])
    #dz.insert(0,0.)
    #layer_thickness = np.diff(np.asarray(dz))
    #print(layer_thickness)
    #quit()

    #mass = loaders['RHO'].field * area
    #mass = mass.sum(dim=['rlat','rlon'])
    #mass = mass.integrate(dim='altitude')
    #print(mass)

    tend = loaders['target'].field * area * loaders['RHO'].field
    tend = tend.sum(dim=['rlat','rlon'])
    tend = tend.integrate(dim='altitude')

    print(tend/area.sum(dim=['rlat','rlon'])*3600)

    raise NotImplementedError()
    new_attr = {
        'standard_name':'bulk_',
        'long_name':'bulk_tendency_of_'+var_name+'_over_'+domain,
        'units':'%',
    }
    targ_loader = loaders['QV'].clone_to_new_field(
                                'RH', targ_field, new_attr, targ_dict)

    #targ_loader.save_field_to_nc(skip_existing=False)

    #return(targ_loader)



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
            'var_dicts':{'target':VNL['AQVT_TOT'],
                         'RHO':VNL['RHO']},
            }

        step_args = []
        for i,dt in enumerate(dt_range[member_dict['dt']]):
            step_args.append({'task_no':i})
            
        TSMP = TimeStepMP(dt_range[member_dict['dt']])
        TSMP.run(func=calc_bulk, fargs=fargs, step_args=step_args)

        t1 = time.time()
        print(t1 - t0)

    t1 = time.time()
    print(t1 - t00)



