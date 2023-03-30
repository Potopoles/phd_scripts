#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
description	    Collection of useful functions for data handling and
                processing
author			Christoph Heim
date created    20.04.2019
date changed    29.07.2022
usage			no args
"""
##############################################################################
import os, copy
import numpy as np
import xarray as xr
from datetime import timedelta
from difflib import SequenceMatcher
from pathlib import Path
from scipy.interpolate import interp1d
from package.nl_variables import nlv, get_plt_fact
from package.utilities import pickle_save, pickle_load, subsel_domain
from package.model_pp import preproc_model, MODEL_PP, MODEL_PP_DONE
from package.var_pp import (VAR_PP, VAR_PP_DONE, DERIVE, DIRECT,
                            var_mapping, mean_var_mapping, compute_variable)
from package.nl_variables import nlv,dimz
from package.nl_models import nlm
from package.member import Member
from package.time_processing import Time_Processing as TP

import matplotlib.pyplot as plt

##############################################################################

MEM_OPER_SEP = '|'

# set debug level of load_member_var function
debug_level_0 = 1
debug_level_1 = 2
debug_level_2 = 3

  

##############################################################################
## MISCELLANEOUS FUNCTIONS
##############################################################################
def loc_to_var_name(loc_var_name):
    if '@' in loc_var_name:
        var_name = loc_var_name.split('@')[0]
    else:
        var_name = loc_var_name
    return(var_name)



##############################################################################
## IO FUNCTIONS
##############################################################################

def load_member_var(var_name, freq, 
                    first_date, last_date,
                    mem_dict, 
                    var_src_dict, 
                    mean_var_src_dict, 
                    derive_or_direct,
                    #src_domain_key,
                    i_debug=0, supress_model_pp=False,
                    domain=None, dask_chunks=None,
                    mean_dates_code=None,
                    targ_vert_coord='alt'):
    sim_key = mem_dict['sim']
    # set run modus. leads to small differences in execution.
    load_single_day = False
    if mean_dates_code is None:
        load_single_day = True
    #if first_date == last_date:
    #    load_single_day = True
    if i_debug >= debug_level_2:
        if load_single_day:
                print(('### function load_member_var: {:%Y%m%d} {:%Y%m%d} '+
                        '{} {} var {}').format(
                first_date, last_date, sim_key, derive_or_direct, var_name))
        else:
                print(('### function load_member_var MEAN: {} '+
                        '{} {} var {}').format(
                mean_dates_code, sim_key, derive_or_direct, var_name))

    if derive_or_direct == DERIVE:
        # load raw variables from which this one is derived
        raw_var_names = var_mapping[mem_dict['mod']][var_name]
        if load_single_day:
            if var_name in mean_var_mapping[mem_dict['mod']]:
                mean_raw_var_names = mean_var_mapping[mem_dict['mod']][var_name]
            else:
                mean_raw_var_names = []
        #print(raw_var_names)
        #print(mean_raw_var_names)
        #quit()

        if i_debug >= debug_level_2:
            print('from raw_vars {}'.format(raw_var_names))
            if load_single_day:
                print('from mean_raw_vars {}'.format(mean_raw_var_names))

        ### load raw variables
        ################################################################
        raw_vars = {}
        for raw_var_name in raw_var_names:
            # if the raw_var_name equals the var_name, then
            # the variable should be loaded directly and not derived
            # else we would get an infinit recursion loop.
            if raw_var_name == var_name:
                derive_or_direct = DIRECT
            # else take value according to var_src_dict
            else:
                derive_or_direct = var_src_dict[raw_var_name]['load']
            if i_debug >= debug_level_2:
                print('var_name {} and raw_var_name {} --> {} {}'.format(
                        var_name, raw_var_name, derive_or_direct,
                        raw_var_name))
            raw_var = load_member_var(raw_var_name, freq,
                                    first_date, last_date,
                                    mem_dict,
                                    var_src_dict, 
                                    mean_var_src_dict, 
                                    derive_or_direct,
                                    i_debug=i_debug,
                                    supress_model_pp=supress_model_pp,
                                    domain=domain,
                                    mean_dates_code=mean_dates_code,
                                    targ_vert_coord=targ_vert_coord)
            if raw_var is None:
                if i_debug >= debug_level_2:
                    print('return None')
                return(None)
            raw_vars[raw_var_name] = raw_var


        ### load mean raw variables
        ################################################################
        mean_raw_vars = {}
        if load_single_day:
            for mean_raw_var_name in mean_raw_var_names:
                #print(var_name)
                #print(mean_raw_var_name)

                ## mean variables can only be loaded directly
                #derive_or_direct = DIRECT
                #if i_debug >= debug_level_2:
                #    print('direct load of mean_raw_var_name {}'.format(
                #            var_name, mean_raw_var_name, derive_or_direct,
                #            mean_raw_var_name))

                derive_or_direct = mean_var_src_dict[mean_raw_var_name]['load']

                if i_debug >= debug_level_2:
                    print('var_name {} and mean_raw_var_name {} --> {} mean {}'.format(
                            var_name, mean_raw_var_name, derive_or_direct,
                            mean_raw_var_name))

                # mean variable date range code
                mean_dates_code = create_dates_code(mem_dict['dates'])

                mean_raw_var = load_member_var(mean_raw_var_name, freq,
                                        first_date, last_date,
                                        mem_dict,
                                        mean_var_src_dict, 
                                        mean_var_src_dict, 
                                        derive_or_direct,
                                        i_debug=i_debug,
                                        supress_model_pp=supress_model_pp,
                                        domain=domain,
                                        mean_dates_code=mean_dates_code,
                                        targ_vert_coord=targ_vert_coord)
                if mean_raw_var is None:
                    raise ValueError(
                        'mean_raw_var {} : {} not found!'.format(
                        mean_raw_var_name, mean_dates_code)
                    )
                    #if i_debug >= debug_level_2:
                    #    print('return None')
                mean_raw_vars[mean_raw_var_name] = mean_raw_var

        ### compute variable
        ################################################################
        # if variable should get derived from raw_vars but itself is
        # already contained in raw_vars, make sure that its not
        # computed a second time (this would cause errors).
        run_var_computation = True
        if var_name in raw_vars:
            if ( (VAR_PP in raw_vars[var_name].attrs) and
                 (raw_vars[var_name].attrs[VAR_PP] == VAR_PP_DONE) ):
                run_var_computation = False 
        if run_var_computation:
            ##TODO
            #print(raw_vars)
            var = compute_variable(
                var_name, mem_dict['mod'], 
                raw_vars, mean_raw_vars, domain
            )
            if i_debug >= debug_level_2:
                print('Computed var {} from raw_vars {}.'.format(
                            var_name, raw_var_names))
        else:
            if i_debug >= debug_level_2:
                print('Selected var {} from raw_vars {}.'.format(
                            var_name, raw_var_names))
            var = raw_vars[var_name]

    elif derive_or_direct == DIRECT:
        #### load this variable
        # if dom_key is not set specifically, take the default one for this member
        dom_key = var_src_dict[var_name]['dom_key']
        if var_src_dict[var_name]['dom_key'] is None:
            dom_key = mem_dict['dom_key']

        if load_single_day:
            inp_dir = os.path.join(var_src_dict[var_name]['src_path'],
                                   sim_key, mem_dict['case'],
                                   dom_key, freq, var_name)
            inp_file = os.path.join(inp_dir,
                        '{}_{:%Y%m%d}.nc'.format(var_name, first_date))
        else:
            inp_dir = os.path.join(var_src_dict[var_name]['src_path'],
                                   sim_key, mem_dict['case'],
                                   dom_key, 
                                   'tmean', var_name)
            inp_file = os.path.join(inp_dir,
                        '{}_{}.nc'.format(var_name, mean_dates_code))
            #print(inp_file)
            #quit()
        # load data if file exists
        if i_debug >= debug_level_2:
            print(inp_file)
        if not os.path.exists(inp_file):
            if i_debug >= debug_level_0:
                if load_single_day:
                    print('{}: No file for var {} and dates {:%Y%m%d} and {:%Y%m%d}'.format(
                                sim_key, var_name, first_date, last_date))
                else:
                    print('{}: No mean file for var {} and {}'.format(
                                sim_key, var_name, mean_dates_code))
            if i_debug >= debug_level_1:
                print(inp_file)
                #quit()
            if i_debug >= debug_level_2:
                print('return None')
            return(None)
        else:
            with xr.open_dataset(inp_file, lock=False, chunks=dask_chunks) as ds:
                # preprocess model output if not yet done.
                # testing is done with MODEL_PP flag in attributes
                # first in full data set and else in the separate
                # data fields (usually its only one, namely the
                # var_name data_var. But the loop is here to make
                # sure it does not crash if a dimension is stored
                # as data_var.
                run_model_pp = True
                # if function input argument supresses model_pp
                if supress_model_pp:
                    run_model_pp = False
                # if model_pp already done (still relevant?)                
                if ( (MODEL_PP in ds.attrs) and
                     (ds.attrs[MODEL_PP] == MODEL_PP_DONE) ):
                    run_model_pp = False
                for data_var in list(ds.data_vars.keys()):
                    if ( (MODEL_PP in ds[data_var].attrs) and
                         (ds[data_var].attrs[MODEL_PP] == MODEL_PP_DONE) ):
                        run_model_pp = False
                if run_model_pp:
                    if i_debug >= debug_level_2:
                        print('Run model preprocessing for {}'.format(var_name))
                    if not load_single_day:
                        raise NotImplementedError('Model pp should not be necessary'+
                                'for multi-day data loading and is not implemented.')

                # Some models have some variables that depend on other variables
                # for model preprocessing. (e.g. models that have pressure levels
                # require altitude of pressure levels to convert pressure levels
                # to altitude levels during model_pp).
                if run_model_pp:
                    dep_vars = {}
                    dep_var_names = []
                    #### default dependency vars
                    inp_vert_coord = nlm[mem_dict['mod']]['vert_coord']

                    ## to convert pressure to altitude and vice versa

                    if ((dimz in nlv[var_name]['dims']) and 
                        (inp_vert_coord in ['plev','hybsigp']) and 
                        (targ_vert_coord == 'alt')
                    ):
                        if var_name != 'ALT':
                            dep_var_names.append('ALT')
                        ## some CMIP6 models have hybrid sigma pressure vertical coordinate for CLDF
                        dep_var_names.append('PS')
                    elif (inp_vert_coord == 'alt') and (targ_vert_coord == 'plev'):
                        if var_name != 'P':
                            dep_var_names.append('P')

                    ## to mask 3D grid points below surface
                    if (dimz in nlv[var_name]['dims']) and (targ_vert_coord == 'alt'):
                        dep_var_names.append('HSURF')
                    elif (dimz in nlv[var_name]['dims']) and (targ_vert_coord == 'plev'):
                        dep_var_names.append('PS')
                        
                    #### extra dependency vars
                    if (('dep' in nlm[mem_dict['mod']]) and 
                        (var_name in nlm[mem_dict['mod']]['dep'])):
                        dep_var_names.extend(nlm[mem_dict['mod']]['dep'][var_name])

                    #### summary of dependencies to load
                    if i_debug >= debug_level_2:
                        print('Dependencies: {}'.format(dep_var_names))

                    #### load all dependencies
                    for dep_var_name in dep_var_names:
                        if i_debug >= debug_level_2:
                            print(('var_name {} has dependency on {}'+
                                   ' --> load dependency').format(
                                    var_name, dep_var_name))
                        #print(dep_var_name)
                        # dependency is a constant variable
                        if dep_var_name in ['HSURF', 'VCOORD']:
                            dim_key = None
                            if 'lon' in ds.dims:
                                dim_key = 'lon'
                            elif 'rlon' in ds.dims:
                                dim_key = 'rlon'
                            elif 'longitude' in ds.dims:
                                dim_key = 'longitude'
                            else:
                                ## TODO: COSMO suddenly is missing rlon in some files (WSOIL)
                                if 'lat' in ds.dims:
                                    dim_key = 'lat'
                                elif 'rlat' in ds.dims:
                                    dim_key = 'rlat'
                                elif 'latitude' in ds.dims:
                                    dim_key = 'latitude'
                                else:
                                    raise NotImplementedError()
                            #print(ds)
                            #print(dim_key)
                            #print(ds[dim_key])
                            #print(np.median(np.diff(ds[dim_key])))
                            #quit()
                            const_file = os.path.join(var_src_dict[var_name]['src_path'],
                                                   sim_key, mem_dict['case'],
                                                   dom_key,
                                                   'const_{:4.3f}.nc'.format(
                                                    np.median(np.diff(ds[dim_key]))))

                            dep_var_key = nlm[mem_dict['mod']]['vkeys'][dep_var_name]
                            dep_vars[dep_var_name] = xr.open_dataset(
                                    const_file)[dep_var_key]
                        # dependency is a normal variable
                        else:
                            #print(dep_var_name)
                            #print(supress_model_pp)
                            #quit()
                            dep_vars[dep_var_name] = load_member_var(dep_var_name, freq,
                                                    first_date, last_date,
                                                    mem_dict, 
                                                    var_src_dict,
                                                    mean_var_src_dict,
                                                    var_src_dict[dep_var_name]['load'],
                                                    #derive_or_direct,
                                                    #src_domain_key,
                                                    i_debug=i_debug, 
                                                    supress_model_pp=supress_model_pp,
                                                    # do not cut out subdomain for dep_vars
                                                    # because it is used in model preprocessing
                                                    domain=None,
                                                    targ_vert_coord=targ_vert_coord)


                    #### PREPROCESS MODEL SPECIFIC STUFF
                    ds = preproc_model(ds=ds, mkey=mem_dict['mod'],
                                       var_name=var_name,
                                       date=first_date,
                                       data_inp_dir=inp_dir,
                                       dims=nlv[var_name]['dims'],
                                       dep_vars=dep_vars,
                                       targ_vert_coord=targ_vert_coord)

                else: # if not run_model_pp
                    if i_debug >= debug_level_2:
                        print('supress model_pp.')

                # if variable is loaded from ana_base_dir, it may already
                # be derived/computed and contain the actual var_name as key.
                # and it may thus not be contained within nlm
                # If multiday is loaded, remove "_tmean" from var_name
                if load_single_day:
                    file_var_name = var_name
                else:
                    file_var_name = var_name.split('_')[0]
                try:
                    vkey = nlm[mem_dict['mod']]['vkeys'][file_var_name]
                    var = ds[vkey]
                except KeyError:
                    var = ds[file_var_name]
                # make sure var inherits model_pp flag from ds
                if MODEL_PP in ds.attrs:
                    var.attrs[MODEL_PP] = ds.attrs[MODEL_PP]

                # cut out domain of interest
                if 'lon' in var.dims:
                    dim_key = 'lon'
                # for loading of dependencies where model_pp is supressed
                elif 'longitude' in var.dims:
                    dim_key = 'longitude'
                else:
                    raise NotImplementedError()
                const_file = os.path.join(var_src_dict[var_name]['src_path'],
                                       sim_key, mem_dict['case'],
                                       dom_key, 
                                       'const_{:4.3f}.nc'.format(
                                        np.median(np.diff(var[dim_key]))))

                #print(const_file)
                #print(np.sum(np.isnan(var)))
                if domain is not None: var = subsel_domain(var, domain,
                                                const_file=const_file, 
                                                mod_key=mem_dict['mod'])
                #print(np.sum(np.isnan(var)))
                #quit()

    if i_debug >= debug_level_2:
        print('return {}'.format(var_name))
        #print(var.shape)
        #quit()
    #if not load_single_day:
    #    var.to_netcdf('test.nc')
    #    quit()
    return(var)




def time_periods_to_dates(time_periods):
    """
    Based on the time_periods list containing all time_periods,
    each represented
    as a dict like e.g.:
    time_periods = [
        {
            'first_date':    datetime(2016,8,6),
            'last_date':     datetime(2016,9,9),
        },
    ]
    create datetime representation of all dates
    """
    dates = []
    for tp in time_periods:
        dates.extend(np.arange(tp['first_date'].date(),
                          tp['last_date'].date()+timedelta(days=1),
                          timedelta(days=1)).tolist())
    return(dates)


def create_dates_code(dates):
    if len(dates) > 1:
        #print(type(dates[-1]))
        ndays_gap = (dates[-1] - dates[0]).days + 1 - len(dates)
        code = '{:%Y%m%d}-{:%Y%m%d}-gap{}'.format(dates[0], dates[-1], ndays_gap)
        #code = '{:%Y%m%d}-{:%Y%m%d}'.format(dates[0], dates[-1], ndays_gap)
    else:
        code = '{:%Y%m%d}'.format(dates[0])
    return(code)

#def create_time_periods_code(time_periods):
#    """
#    From time_periods list containing all time_periods, each represented
#    as a dict like e.g.:
#    time_periods = [
#        {
#            'first_date':    datetime(2016,8,6),
#            'last_date':     datetime(2016,9,9),
#        },
#    ]
#    this function will create a short string representation (code)
#    of the time periods to use in names of pickle files.
#    """
#    year0 = 9999
#    year1 = 0
#    month0 = 9999
#    month1 = 0
#    day0 = 9999
#    day1 = 0
#    for time_period in time_periods:
#        if time_period['first_date'].year < year0:
#            year0 = time_period['first_date'].year
#        if time_period['last_date'].year > year1:
#            year1 = time_period['last_date'].year
#        if time_period['first_date'].month < month0:
#            month0 = time_period['first_date'].month
#        if time_period['last_date'].month > month1:
#            month1 = time_period['last_date'].month
#        if time_period['first_date'].day < day0:
#            day0 = time_period['first_date'].day
#        if time_period['last_date'].day > day1:
#            day1 = time_period['last_date'].day
#        
#    time_periods_code = 'Y{}-{}m{}-{}d{}-{}'.format(year0,year1,month0,
#                                                    month1,day0,day1)
#    return(time_periods_code)


def save_member_to_pickle(base_dir, member, 
                        #time_periods,
                        #dates,
                        append=None):
    mem_dict = member.mem_dict
    #time_periods_code = create_time_periods_code(time_periods)
    #dates_code = create_dates_code(dates)
    pickle_dir = os.path.join(base_dir, mem_dict['sim'],
                              mem_dict['case'])
    #pickle_file = '{}'.format(time_periods_code)
    #pickle_file = '{}'.format(dates_code)
    pickle_file = '{}'.format(member.dates_code)
    if append != '':
        pickle_file += '_{}'.format(append)
    pickle_file += '_member'
    save_member = copy.copy(member)
    # reset vars as they are not stored in the member pickle file
    save_member.vars = {}
    pickle_save(save_member, pickle_dir, pickle_file)


def save_member_var_to_netcdf(base_dir, member, domain, var_name,
                                #time_periods, 
                                #dates, 
                                append=None,
                                netcdf=True):
    # skip var if this member does not contain in.
    if var_name not in member.vars:
        return()
    if member.vars[var_name] is None:
        return()
    var = member.vars[var_name]
    mem_dict = member.mem_dict
    file_dir = os.path.join(base_dir, mem_dict['sim'],
                              mem_dict['case'],
                              domain['key'])
    file_name = '{}_var_{}'.format(member.dates_code, var_name)
    if append != '':
        file_name += '_{}'.format(append)
    Path(file_dir).mkdir(exist_ok=True, parents=True)
    if netcdf:
        file_name += '.nc'
        var.to_netcdf(os.path.join(file_dir, file_name))
    else:
        pickle_save(var, file_dir, file_name)


def load_member_from_pickle(base_dir, mem_dict,
                            #time_periods, 
                            dates, 
                            skip_missing, append=None):
    #time_periods_code = create_time_periods_code(time_periods)
    dates_code = create_dates_code(dates)
    pickle_dir = os.path.join(base_dir, mem_dict['sim'], 
                            mem_dict['case'])
    #pickle_file = '{}'.format(time_periods_code)
    pickle_file = '{}'.format(dates_code)
    if append is not None:
        pickle_file += '_{}'.format(append)
    pickle_file += '_member'
    member = pickle_load(pickle_dir, pickle_file)
    if member is not None:
        # replace mem_dict of loaded member with the one
        # given as input argument
        member.mem_dict = mem_dict
        return(member)
    else:
        print('No pickle file {}/{} for member {}'.format(
                    pickle_dir, pickle_file, mem_dict['sim']))
        if skip_missing:
            return(None)


def load_member_var_from_netcdf(base_dir, mem_dict, domain, var_name,
                               #time_periods, 
                               #dates, 
                               dates_code,
                               skip_missing, append=None,
                               netcdf=True):
    #time_periods_code = create_time_periods_code(time_periods)
    #dates_code = create_dates_code(dates)
    file_dir = os.path.join(base_dir, mem_dict['sim'], 
                            mem_dict['case'], domain['key'])
    #file_name = '{}_var_{}'.format(time_periods_code, var_name)
    file_name = '{}_var_{}'.format(dates_code, var_name)
    #print(file_name)
    if append != '':
        file_name += '_{}'.format(append)
    if netcdf:
        file_name += '.nc'
        file_path = os.path.join(file_dir, file_name)
        if os.path.exists(file_path):
            var = xr.open_dataset(file_path)
            return(var)
        else:
            print('No variable file {} for {}'.format(
                        file_path, mem_dict['sim']))
            if skip_missing:
                return(None)
    else:
        file_path = os.path.join(file_dir, '{}.pkl'.format(file_name))
        if os.path.exists(file_path):
            var = pickle_load(file_dir, file_name)
            return(var)
        else:
            print('No variable file {} for {}'.format(
                        file_path, mem_dict['sim']))
            if skip_missing:
                return(None)


def import_namelist(targ_nl, src_nl):
    # dynamically copy attributes from analysis namelist 
    exceptions = ['__name__', '__doc__', '__package__', '__loader__',
                '__spec__', '__file__', '__cached__', '__builtins__',
                'datetime', 'timedelta', 'np', 'TP', 'copy', 'os']
    for attr_key,attr in src_nl.__dict__.items():
        #if attr_key not in locals():
        if ( (attr_key not in targ_nl.__dict__.keys()) &
             (attr_key not in exceptions) ):
            setattr(targ_nl, attr_key, getattr(src_nl, attr_key))


##############################################################################
## MEMBER FUNCTIONS
##############################################################################


def calc_global_min_max(members, sym_zero=False):
    """
    Calculate min and max values of all members.
    ARGS:
        sym_zero:   log -   should value range min/max be centred around
                            zero?
    COMMENTS:
    """
    min_max = {}
    if len(members) == 0:
        raise ValueError('No member contained 3492013')
    for var_name in list(members[list(members.keys())[0]].vars.keys()):
        glob_min = np.Inf
        glob_max = -np.Inf
        for mem_key,member in members.items():
            #print(mem_key)
            if member.vars[var_name] is not None:
                mem_min = member.vars[var_name].min().values
                if mem_min < glob_min:
                    glob_min = mem_min
                mem_max = member.vars[var_name].max().values
                if mem_max > glob_max:
                    glob_max = mem_max
        # centre values around 0
        if sym_zero:
            glob_max = np.max([np.abs(glob_min), np.abs(glob_max)]) 
            glob_min = - glob_max
        min_max = [glob_min, glob_max]

        # set values in members
        for mem_key,member in members.items():
            member.plot_min_max[var_name] = min_max



def get_comb_mem_key(comb_instr):
    if 'mem_key' in comb_instr:
        return(comb_instr['mem_key'])
    elif 'mem_keys' in comb_instr:
        comb_mem_key = '{}{}{}'.format(MEM_OPER_SEP,comb_instr['mem_oper'],MEM_OPER_SEP)
        for i,sub_mem_cfg in enumerate(comb_instr['mem_keys']):
            if 'mem_keys' in sub_mem_cfg:
                sub_mem_date_key = get_comb_mem_key(sub_mem_cfg)
            else:
                #dates_code = create_dates_code(sub_mem_cfg['dates'])
                dates_code = create_dates_code(time_periods_to_dates(sub_mem_cfg['time_periods']))
                sub_mem_date_key = '{}#time#{}'.format(sub_mem_cfg['mem_key'], dates_code)
            comb_mem_key += sub_mem_date_key
            if i < len(comb_instr['mem_keys'])-1:
                comb_mem_key += '#+++#'
            else:
                comb_mem_key += '{}end{}{}'.format(MEM_OPER_SEP,comb_instr['mem_oper'],MEM_OPER_SEP)
        return(comb_mem_key)
    else:
        raise ValueError()


def interp_same_grid_horizontal(inp_vars):
    for dim_key in ['lon','lat']:
        # check if members contain dim
        has_dim = []
        for inp_var in inp_vars:
            if dim_key in inp_var.dims:
                has_dim.append(True)
            else:
                has_dim.append(False)
        # raise value if dimension is not consistently represented 
        # (or not represented) in all members
        if not len(set(has_dim)) <= 1:
            raise ValueError('Combine_members: Not all members have dim {}'.format(
                             dim_key))
        # skip if members do not have this dimension
        if not all(has_dim):
            continue

        # compute member dlat/dlon and check if all members have same dimension
        all_equal_grid = True
        mem_dlatlon = []
        ref_mem_ind = 0
        for mem_ind in range(len(inp_vars)):
            mem_dlatlon.append(np.median(
                 np.diff(inp_vars[mem_ind][dim_key])))

            # check for different coordinate length
            if ( len(inp_vars[mem_ind][dim_key]) != 
                 len(inp_vars[ref_mem_ind][dim_key]) ):
                all_equal_grid = False
            else:
                # check for different values in coordinate
                if np.sum(np.abs(inp_vars[mem_ind][dim_key].values - 
                                 inp_vars[ref_mem_ind][dim_key].values)) != 0.:
                    all_equal_grid = False

        if all_equal_grid:
            continue

        ## take finest
        remap_target_mem_ind = np.argmin(mem_dlatlon)
        ### take coarsest
        #remap_target_mem_ind = np.argmax(mem_dlatlon)

        ### interpolate all members to the coordinate of the target one 
        for mem_ind in range(len(inp_vars)):
            if mem_ind != remap_target_mem_ind:
                #print('remap {} from member {} to member {}'.format(dim_key, mem_ind, remap_target_mem_ind))
                # this is done with simple bilinear interpolation
                # TODO: implement conserving interpolation
                inp_vars[mem_ind] = inp_vars[mem_ind].interp(
                    {dim_key:inp_vars[remap_target_mem_ind][dim_key]},
                    ## fill missing values at the boundaries that may become NaN due to interpolation
                    kwargs={'fill_value':'extrapolate'})




def interp_same_grid_vertical(inp_vars):
    dim_key = 'alt'
    # check if members contain dim
    has_dim = []
    for mem_ind in range(len(inp_vars)):
        if dim_key in inp_vars[mem_ind].dims:
            has_dim.append(True)
        else:
            has_dim.append(False)
    # raise value error if dimension is not consistently represented 
    # (or not represented) in all members
    #print(has_dim)
    #quit()
    #if not len(set(has_dim)) <= 1:
    #    raise ValueError('Combine_members: Not all members have dim {}'.format(
    #                     dim_key))
    # skip if members do not have this dimension
    if not all(has_dim):
        return()

    # compute member dlat/dlon and check if all members have same dimension
    all_equal_grid = True
    ref_mem_ind = 0
    for mem_ind in range(len(inp_vars)):

        # check for different coordinate length
        if ( len(inp_vars[mem_ind][dim_key]) != 
             len(inp_vars[ref_mem_ind][dim_key]) ):
            all_equal_grid = False
        else:
            #print(inp_vars[mem_ind][dim_key])
            #print(inp_vars[ref_mem_ind][dim_key])
            #quit()
            #print(np.abs(inp_vars[mem_key][dim_key].values - 
            #                 inp_vars[ref_mem_key][dim_key].values))
            #print(np.sum(np.abs(inp_vars[mem_key][dim_key].values - 
            #                 inp_vars[ref_mem_key][dim_key].values)))

            # check for different values in coordinate
            if np.sum(np.abs(inp_vars[mem_ind][dim_key].values - 
                             inp_vars[ref_mem_ind][dim_key].values)) != 0.:
                all_equal_grid = False

    if all_equal_grid:
        return()
    #else:
    #    raise NotImplementedError()

    # get common vertical grid
    # (take levels from all members and combine to finer common grid)
    alts = []
    for mem_ind in range(len(inp_vars)):
        alts.extend(inp_vars[mem_ind][dim_key].values)
    alts = np.unique(np.asarray(alts))
    alts.sort()

    #alts = [1000, 2000]
    #print(alts)

    ### interpolate all members to the coordinate of the target one 
    for mem_ind in range(len(inp_vars)):
        print('remap {} for member {}'.format(dim_key, mem_ind))

        #print(inp_vars[mem_ind])
        #inp_vars[mem_ind] = inp_vars[mem_ind].isel(alt=slice(1,len(inp_vars[mem_ind].alt)))

        #print(inp_vars[mem_ind].shape)
        #print(inp_vars[mem_ind].alt.values)
        #inp_vars[mem_ind] = inp_vars[mem_ind].isel(lat=slice(0,20))
        #print(inp_vars[mem_ind].isel(lat=slice(878,882)).values)
        #inp_vars[mem_ind] = inp_vars[mem_ind].where(np.isnan(inp_vars[mem_ind]), 1000)
        # this is done with cubic interpolation
        #print(inp_vars[mem_ind].alt)
        #print(np.isnan(inp_vars[mem_ind]).sum(dim='alt'))
        #inp_vars[mem_ind] = inp_vars[mem_ind].interp(
        #                        {dim_key:alts}, method='quadratic')#,
        #                        #kwargs=dict(fill_value='extrapolate'))

        inp_dims = inp_vars[mem_ind].dims
        #plt.contourf(inp_vars[mem_ind])
        #plt.show()
        inp_vars[mem_ind] = xr.apply_ufunc(
            interp_alt_to_alt,
            alts,
            inp_vars[mem_ind].alt,
            inp_vars[mem_ind],
            input_core_dims=[["alt"], ["alt"], ["alt"]],  # list with one entry per arg
            output_core_dims=[["alt"]],  # returned data has one dimension
            exclude_dims=set(("alt",)),  # dimensions allowed to change size. Must be a set!
            vectorize=True,  # loop over non-core dims
        ).transpose(*inp_dims).assign_coords({inp_dims[0]:alts})
        #print(inp_vars[mem_ind].alt)
        #quit()
        #print(np.sum(np.isnan(inp_vars[mem_ind])))
        #print(inp_vars[mem_ind])
        #plt.contourf(inp_vars[mem_ind])
        #plt.show()
        #inp_vars[mem_ind].to_netcdf('test.nc')

                ### take altitude grid from member with
                ### more levels and make sure that
                ### upper-most and lower-most levels
                ### are not beyond any of the input grids.
                #nlev_0 = len(member_0_var.alt.values)
                #nlev_1 = len(member_1_var.alt.values)
                #if nlev_0 >= nlev_1:
                #    targ_alt = member_0_var.alt.values
                #else:
                #    targ_alt = member_1_var.alt.values
                ## make sure lowest value is not below lowest value of
                ## any of the two members
                #for i in range(len(targ_alt)):
                #    if targ_alt[i] < np.min(member_0_var.alt):
                #        targ_alt[i] = np.min(member_0_var.alt)
                #    if targ_alt[i] < np.min(member_1_var.alt):
                #        targ_alt[i] = np.min(member_1_var.alt)
                #targ_alt = np.unique(targ_alt)
                ## make sure highest value is not above highest value of
                ## any of the two members
                #for i in range(len(targ_alt)-1,-1,-1):
                #    if targ_alt[i] > np.max(member_0_var.alt):
                #        targ_alt[i] = np.max(member_0_var.alt)
                #    if targ_alt[i] > np.max(member_1_var.alt):
                #        targ_alt[i] = np.max(member_1_var.alt)
                #targ_alt = np.unique(targ_alt)
                ## interpolate both members onto target grid
                #member_0_var = member_0_var.interp({dim_key:targ_alt})
                #member_1_var = member_1_var.interp({dim_key:targ_alt})


def interp_alt_to_alt(x_out, x_in, data_in):
    #print('############################')
    #print(x_out)
    #print(x_in)
    #print(data_in)

    if np.sum(np.isnan(data_in)) > 0:
        first_ind = np.min(np.argwhere(~np.isnan(data_in)))
        x_in_use = x_in[first_ind:]
        data_in_use = data_in[first_ind:]
        #print('test')
        #print(x_in_use)
        #print(data_in_use)
        #quit()
    else:
        x_in_use = x_in
        data_in_use = data_in

    f = interp1d(x_in_use, data_in_use, kind='quadratic', 
                fill_value=np.nan, bounds_error=False)
    out = f(x_out)
    #print(out)
    #if np.sum(np.isnan(data_in)) > 0:
    #    quit()
    return(out)




def create_combined_member(members, comb_instr):
    #print(members[0].val_type)
    #print(members[1].val_type)
    #quit()
    #print('function create_combined_member()')
    # determine combination operator
    operator_val_type_mapping = {
        'diff': 'diff',
        'bias': 'bias',
        'mean': 'inherit',
        'perc': 'inherit',
        'rel': 'rel',
        'sum': 'inherit',
    }

    if comb_instr['mem_oper'] not in operator_val_type_mapping:
        if (
            (not 'perc' in comb_instr['mem_oper']) and 
            (not 'rel' in comb_instr['mem_oper'])
        ):
            raise NotImplementedError()

    ## go one level downward if the input_member are combinations
    #for inp_mem_key in inp_mem_keys:
    #    #print(inp_mem_key)
    #    if isinstance(inp_mem_key, dict):
    #        #print('go deeper {}'.format(inp_mem_key))
    #        create_combined_member(members, inp_mem_key)
    #        #print('go shallower to {}'.format(inp_mem_key))

    ## convert the inp_mem_key dicts to strings
    #for i in range(len(inp_mem_keys)):
    #    inp_mem_keys[i] = get_comb_mem_key(inp_mem_keys[i])

    ## get combined member's mem_dict (start with the one of the first one
    comb_mem_dict = copy.deepcopy(members[0].mem_dict)

    ## set up label for combined member
    if comb_instr['mem_oper'] in ['diff', 'bias']:
        #match = SequenceMatcher(None, 
        #            members[inp_mem_keys[0]].mem_dict['label'], 
        #            members[inp_mem_keys[1]].mem_dict['label']).find_longest_match(
        #            0,  len(members[inp_mem_keys[0]].mem_dict['label']), 0, 
        #                len(members[inp_mem_keys[1]].mem_dict['label']))
        #match_str = members[inp_mem_keys[0]].mem_dict['label'][
        #            match.a: match.a + match.size]
        #comb_mem_dict['label'] = '{}: {} - {}'.format(
        #            match_str,
        #            members[inp_mem_keys[0]].mem_dict['label'].replace(
        #                                            match_str, ''),
        #            members[inp_mem_keys[1]].mem_dict['label'].replace(
        #                                            match_str, ''))
        comb_mem_dict['label'] = '{}$-${}'.format(
                    members[0].mem_dict['label'],
                    members[1].mem_dict['label'])
        #comb_mem_dict['label'] = '{}'.format(
        #            members[inp_mem_keys[0]].mem_dict['label'])
    elif comb_instr['mem_oper'] == 'mean':
        comb_mem_dict['label']= 'MEAN'
    elif comb_instr['mem_oper'][0:4] == 'perc':
        comb_mem_dict['label']= 'PERC{}'.format(comb_instr['mem_oper'][4:])
    elif comb_instr['mem_oper'][0:3] == 'rel':
        comb_mem_dict['label']= 'REL'
    elif comb_instr['mem_oper'] == 'sum':
        comb_mem_dict['label']= 'SUM'
    else:
        raise NotImplementedError()

    ## initialize combined member
    # inherit value type or set according to dict
    if comb_instr['mem_oper'] in operator_val_type_mapping:
        use_key = comb_instr['mem_oper']
    else:
        if 'perc' in comb_instr['mem_oper']:
            # percentile
            use_key = comb_instr['mem_oper'][0:4]
        if 'rel' in comb_instr['mem_oper']:
            # relative difference
            use_key = comb_instr['mem_oper'][0:3]
    if operator_val_type_mapping[use_key] == 'inherit':
        val_type = members[0].val_type
    else:
        val_type = operator_val_type_mapping[use_key]
    comb_member = Member(comb_mem_dict, val_type=val_type)

    ### combine all variables
    for var_name in list(members[0].vars.keys()):
        #print(var_name)

        ### make sure each member has variable
        all_data_available = True
        all_data_missing = True
        for mem_ind in range(len(members)):
            if members[mem_ind].vars[var_name] is None:
                all_data_available = False
            else:
                all_data_missing = False

        #print(all_data_available)
        #print(all_data_missing)

        ### skip this variable if not available for any of the members.
        if all_data_missing:
            print('Attention in function create_combined_member for {}! '.format(comb_instr) +
                  'None of the input members contain data for var_name {}!'.format(var_name))
            comb_member.add_var(var_name, None)

        ### skip this variable if not complete and difference should be taken.
        elif (not all_data_available) and (comb_instr['mem_oper'] == 'diff'):
            print('Attention in function create_combined_member for {}! '.format(comb_instr)+
                  'Not both input members of operator "diff" contain data for var_name {}!'.format(
                    var_name))
            comb_member.add_var(var_name, None)

        ### complete or incomplete (but not problematic) data
        ### --> combine this variable!
        else:
            if not all_data_available:
                print('Attention, not all data available for {} and var {}'.format(
                        comb_instr, var_name))

            ### copy data to combine it
            inp_vars = []
            #remove_keys = []
            for mem_ind in range(len(members)):
            #for mem_key in inp_mem_keys:
                # if data available only..
                if members[mem_ind].vars[var_name] is not None:
                    inp_vars.append(members[mem_ind].vars[var_name].copy())
                ## else remove member from list
                #else:
                #    remove_keys.append(mem_key)
            #for mem_key in remove_keys:
            #    inp_mem_keys.remove(mem_key)

            ### do horizontal interpolation
            interp_same_grid_horizontal(inp_vars)

            ### do vertical interpolation
            interp_same_grid_vertical(inp_vars)

            ### combine with operator
            if comb_instr['mem_oper'] in ['diff', 'bias']:
                # take difference
                if len(inp_vars) > 2:
                    raise ValueError('Cannot take difference between more than 2 members.')
                #print(inp_vars)
                comb_var = inp_vars[0].copy()
                ## do subtraction based on numpy arrays because time is allowed to differ
                ## between the members of the difference
                comb_var.values = (
                    inp_vars[0].values - 
                    inp_vars[1].values
                )
                # take attributes from first member
                for key,value in inp_vars[0].attrs.items():
                    comb_var.attrs[key] = value
                comb_member.add_var(var_name, comb_var)
            elif comb_instr['mem_oper'] == 'mean':
                # compute average value over all members
                comb_var = xr.Dataset()
                for mem_ind in range(1,len(inp_vars)):
                    comb_var[mem_ind] = inp_vars[mem_ind]
                comb_var = comb_var.to_array(dim='new').mean('new')
                ##comb_var = inp_vars[inp_mem_keys[0]]
                ##for mem_key in inp_mem_keys[1:]:
                ##    comb_var += inp_vars[mem_key]
                ##comb_var /= len(inp_mem_keys)
                comb_member.add_var(var_name, comb_var)
            elif comb_instr['mem_oper'][0:4] == 'perc':
                percentile = float(comb_instr['mem_oper'][4:])
                # compute percentile value over all members
                comb_var = xr.Dataset()
                for mem_ind in range(1,len(inp_vars)):
                    comb_var[mem_ind] = inp_vars[mem_ind]
                comb_var = comb_var.to_array(dim='new').quantile(percentile/100, dim='new')
                comb_member.add_var(var_name, comb_var)
            elif comb_instr['mem_oper'][0:3] == 'rel':
                # mask all dividend values below min val
                #min_val = (
                #    float(comb_instr['mem_oper'][3:]) / 
                #    get_plt_fact(loc_to_var_name(TP.get_var_name(var_name)))
                #)
                min_rel_val = float(comb_instr['mem_oper'][3:]) 
                min_val = min_rel_val * np.max(np.abs(inp_vars[1])).values
                comb_var = inp_vars[1].where(np.abs(inp_vars[1]) >= min_val, np.nan)
                # compute ratio between dividend and divisor
                comb_var = inp_vars[0] / comb_var - 1
                # take attributes from first member
                for key,value in inp_vars[0].attrs.items():
                    comb_var.attrs[key] = value
                comb_member.add_var(var_name, comb_var)
            elif comb_instr['mem_oper'] == 'sum':
                if len(inp_mem_keys) > 2:
                    raise NotImplementedError
                # take sum
                comb_var = (inp_vars[0] + 
                            inp_vars[1])
                # take attributes from first member
                for key,value in inp_vars[0].attrs.items():
                    comb_var.attrs[key] = value
                comb_member.add_var(var_name, comb_var)
            else:
                raise NotImplementedError()

    # get combined member's mem_key
    comb_mem_key = get_comb_mem_key(comb_instr) 


    return(comb_mem_key, comb_member)


