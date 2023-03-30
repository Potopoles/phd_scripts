#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Plot evolution of domain average daily mean values.
                Does computation on remapped fields since for domain average
                values this does not matter and is much faster.
dependencies    depends on:
author			Christoph Heim
date created    17.01.2020
date changed    17.01.2020
usage           args:
                1st:    number of parallel tasks
"""
###############################################################################
import os, glob, collections
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pathlib import Path
import nl_05 as nl
from package.nl_models import nlm, nld
from package.nl_variables import nlv,dimx,dimy,dimz,dimt
from package.model_pp import preproc_model, subsel_domain
from package.var_pp import compute_variable, var_mapping
from package.utilities import Timer, write_grid_file, cdo_remap
from package.plot_functions import PlotOrganizer, draw_map
from package.MP import TimeStepMP
from package.member import Member
from package.variable import Variable
###############################################################################


#from scipy.stats import skew
#def skewness_2d(array, axis=None):
#    """
#    Compute skewness of 2D slices. Input array must be 3D.
#    """
#    # select unused dimension
#    dim_inds = np.arange(array.ndim)
#    unused_dim = [i for i in dim_inds if i not in axis]
#    if len(unused_dim) > 1:
#        raise ValueError('input array can be no more than 3D.')
#    else:
#        unused_dim = unused_dim[0]
#    skewness = np.zeros(array.shape[unused_dim])
#    # iterate over unused dimension
#    for i in range(array.shape[unused_dim]):
#        arr_slice = np.take(array, indices=i, axis=unused_dim)
#        flat = arr_slice[~np.isnan(arr_slice)].flatten()
#        skewness[i] = skew(flat)
#    return(skewness)


def draw_plot(members):

    # dict with all resolutions for each model
    # used to select marker types
    mdicts = {}
    for skey,sdict in nl.cfg['use_sims'].items():
        if sdict['mkey'] not in mdicts:
            mdicts[sdict['mkey']] = [sdict['res']]
        else:
            mdicts[sdict['mkey']].append(sdict['res'])
    for mkey,mdict in mdicts.items():
        mdict.sort()

    name_dict = {'daily_variab':nl.cfg['plot_var_name']}
    name_dict[nl.var_names[0]] = nl.var_names[1]

    PO = PlotOrganizer(i_save_fig=nl.i_save_fig,
                      path=os.path.join(nl.plot_base_dir),
                      name_dict=name_dict, nlp=nl.nlp, geo_plot=False)
    fig,axes = PO.initialize_plot(nrows=nl.cfg['nrows'],
                                  ncols=nl.cfg['ncols'],
                                  figsize=nl.cfg['figsize'])

    ax = axes[0, 0]

    all_x = []
    all_y = []
    for skey,mem in members.items():
        if skey == 'SEVIRI_CERES': 
            continue
        print(skey)
        mkey = nl.cfg['use_sims'][skey]['mkey']
        res = nl.cfg['use_sims'][skey]['res']
        xvals = members[skey][nl.var_names[0]].field.values
        yvals = members[skey][nl.var_names[1]].field.values
        try:
            all_x.extend(xvals)
            all_y.extend(yvals)
        except TypeError:
            xvals = np.expand_dims(xvals, axis=0)
            yvals = np.expand_dims(yvals, axis=0)
            all_x.extend(xvals)
            all_y.extend(yvals)
        #quit()
        corr = np.corrcoef(xvals, yvals)[0,1]
        print('{} cor: {}'.format(skey, corr))

        label = '{}'.format(members[skey][nl.var_names[0]].mem_dict['label'])
        if not nl.i_aggreg_days:
            label = '{} c{:3.2f}'.format(label, corr)
        handle = ax.scatter(xvals, yvals, label=label,
                            marker=nl.nlp['markers'][mdicts[mkey].index(res)],
                            color=nl.nlp['colors'][list(mdicts.keys()).index(mkey)])
        PO.handles.append(handle)

    corr = np.corrcoef(all_x, all_y)[0,1]
    print('all cor: {}'.format(corr))

    if nl.i_plot_obs and (len(
        [el for el in nl.var_names if el in nl.use_obs.keys()]) > 0):
        xlim = ax.get_xlim()
        ax.set_xlim(xlim)
        # observations
        yvals = members['SEVIRI_CERES'][nl.var_names[1]].field.values
        try: len(yvals)
        except TypeError: yvals = np.expand_dims(yvals, axis=0)
        handle = ax.scatter(np.full(len(yvals), xlim[0]),
                            yvals, label='OBS', color='k',
                            marker=nl.nlp['markers'][0])
        PO.handles.append(handle)

    xlabel = '{} [{}]'.format(nlv[nl.var_names[0]]['lo_name'],
                              nlv[nl.var_names[0]]['unit'])
    ylabel = '{} [{}]'.format(nlv[nl.var_names[1]]['lo_name'],
                              nlv[nl.var_names[1]]['unit'])
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid()

    ax.legend(handles=PO.handles)

    fig.subplots_adjust(**nl.cfg['subplts'])
    #PO.add_panel_labels(order='cols')
    PO.finalize_plot()



def remap(date, grid_des_file):

    # main var models
    for skey,sdict in nl.cfg['use_sims'].items():
        for var_name in nl.var_names:
            raw_var_names = var_mapping[sdict['mkey']][var_name]
            if 'SWDTOA' in raw_var_names: raw_var_names.remove('SWDTOA')
            for raw_var_name in raw_var_names:
                if nl.i_debug:
                    print('remap {} in {}'.format(raw_var_name, skey))

                inp_file = glob.glob(os.path.join(nl.sim_base_dir, skey,
                                    sdict['sim'], 'daily', raw_var_name,
                                    '{}_{:%Y%m%d}*.nc'.format(raw_var_name, date) ))[0]
                out_path = os.path.join(nl.ana_base_dir, skey, raw_var_name)
                Path(out_path).mkdir(parents=True, exist_ok=True)
                out_file = os.path.join(out_path,
                                '{}_{:%Y%m%d}.nc'.format(raw_var_name, date))
                cdo_remap(grid_des_file, inp_file,  out_file)





def compute_vars(date, members):
    var_name = nl.cfg['var_name']

    # compute for observation
    if var_name in nl.use_obs.keys():
        # compute for observation
        inp_file = os.path.join(nl.ana_base_dir, nl.use_obs[var_name]['name'],
                                var_name,
                                '{}_{:%Y%m%d}.nc'.format(var_name, date))
        ds = xr.open_dataset(inp_file)
        var = ds[nld[nl.use_obs[var_name]['name']]['vkeys'][var_name]]
        var = var.mean(['lon', 'lat'])
        var = Member(var, {'label':'OBS (SEVIRI_CERES)'}, variable=None)
        members['SEVIRI_CERES'] = {var_name:var}

        # preload SWDTOA for later usage in some of the models
    if var_name == 'SWUTOA':
            inp_dir = os.path.join(nl.ana_base_dir, 'FV3_3.25', 'SA',
                                    'daily', 'SWDTOA')
            inp_file = os.path.join(inp_dir,
                            '{}_{:%Y%m%d}.nc'.format('SWDTOA', date))
            ds = xr.open_dataset(inp_file)
            ds = preproc_model(ds=ds, mkey='FV3',
                               var_name='SWDTOA',
                               date=date,
                               data_inp_dir=inp_dir,
                               domain=nl.cfg['domain'],
                               dims=[dimx,dimy,dimt])
            #ds = select_frequency(ds, date, nl.frequency)
            #ds = ds.resample(time='3h', label='right').mean()
            ds = ds.mean(dim='time')
            vkey = nlm['FV3']['vkeys']['SWDTOA']
            ds = ds.rename({vkey:'SWDTOA'})
            swdtoa = ds['SWDTOA']

    for skey,sdict in nl.cfg['use_sims'].items():
        mreskey =  '{}_{:g}'.format(sdict['mkey'], sdict['res'])
        if nl.i_debug:
            print(skey)

        # load raw input variables
        raw_vars = {}
        if 'SWUTOA' in nl.var_names:
            raw_vars['SWDTOA'] = swdtoa
        no_data = False
        for var_name in nl.var_names:
            raw_var_names = var_mapping[sdict['mkey']][var_name]
            if 'SWDTOA' in raw_var_names: raw_var_names.remove('SWDTOA')
            for raw_var_name in raw_var_names:
                inp_dir = os.path.join(nl.ana_base_dir, mreskey, sdict['sim'],
                                       'daily', raw_var_name)
                inp_file = os.path.join(inp_dir,
                            '{}_{:%Y%m%d}.nc'.format(raw_var_name, date))
                # load data if file exists
                if not os.path.exists(inp_file):
                    print('{}: No file for var {} and date {:%Y%m%d}'.format(
                                skey, raw_var_name, date))
                    no_data = True
                    continue
                ds = xr.open_dataset(inp_file)
                ds = preproc_model(ds=ds, mkey=sdict['mkey'],
                                   var_name=raw_var_name,
                                   date=date,
                                   data_inp_dir=inp_dir,
                                   domain=nl.cfg['domain'],
                                   dims=nlv[raw_var_name]['dims'])
                #ds = subsel_domain(ds, sdict['mkey'], nl.cfg['domain'])
                vkey = nlm[sdict['mkey']]['vkeys'][raw_var_name]
                var = ds[vkey]
                #print(ds)
                # nasty fix for icon which has running averages for radiative
                # fluxes. (why would you??)
                if (raw_var_name == 'SWNDTOA') and (sdict['mkey'] == 'ICON'):
                    var = var.sel(time=date + timedelta(hours=23, minutes=45))
                else:
                    var = var.mean(dim='time')
                raw_vars[raw_var_name] = var

        # compute target variables and do stuff
        if not no_data:
            for var_name in nl.var_names:
                var = compute_variable(var_name, sdict['mkey'], raw_vars)


                #var = var.mean(dim=['lon', 'lat', 'time'])
                if var_name == 'W':
                    var = var.sel(alt=800, method='nearest')
                    #var = var.sel(alt=3000, method='nearest')
                    #var.values[var.values < 0] = np.nan
                    #var = var.std(dim=['lon', 'lat'])
                    #var.values[var.values > 0] = np.nan
                    var.values = np.abs(var.values)
                elif var_name == 'QV':
                    # for QV select QV at 500m
                    #var = var.interp(alt=1500)
                    var = var.interp(alt=1000) - var.interp(alt=2500)

                # remove alt dimension
                if 'alt' in var.dims:
                    var = var.mean(dim='alt')

                #if var_name == 'SWUTOA':
                var = var.mean(dim=['lon', 'lat'])


                #print(var.values.shape)
                #print(skew(var.values))
                #print(skew(var.values).shape)
                #print(var.reduce(skewness_2d, dim=['lon', 'lat']))

                #var = var.reduce(skewness_2d, dim=['lon', 'lat'])

                #print(var)
                #var = var.resample(time='1D').mean()
                #var = var.resample(time='1D').std()

                #member = Member(var, {'label':slab}, variable=None)
                member = Member(var, {'label':sdict['label'],
                                      'res':sdict['res']},
                                variable=None)
                if skey not in members.keys():
                    members[skey] = {}
                members[skey][var_name] = member
        else:
            members[skey] = None
    return(members)







def run_for_date(ts):
    """
    Organize full analysis for a given date (ts).
    ts has to be called ts because run_for_date is called from TimeStepMP.
    """
    timer = Timer(mode='seconds')
    members = {}
    
    if nl.i_remap:
        # remap observations
        timer.start('remap')
        if not os.path.exists(nl.grid_des_file):
            write_grid_file(nl.cfg['domain'], nl.grid_des_file, 45,
                            padding=nl.remap_padding)
        remap(ts, nl.grid_des_file)
        timer.stop('remap')
    else:
        # compute variables
        timer.start('vars')
        members = compute_vars(ts, members)
        timer.stop('vars')

    output = {'timer':timer, 'members':members}
    return(output)

if __name__ == '__main__':

    ###########################################################################
    # PREPARATION STEPS
    timer = Timer(mode='seconds')
    Path(nl.ana_base_dir).mkdir(parents=True, exist_ok=True)
    dates = np.arange(nl.first_date, nl.last_date+timedelta(days=1),
                      timedelta(days=1)).tolist()

    ###########################################################################
    # PART OF ANALYSIS SPECIFIC FOR EACH DAY
    tsmp = TimeStepMP(dates, njobs=nl.njobs, run_async=False)
    fargs = {}
    tsmp.run(run_for_date, fargs=fargs, step_args=None)
    # merge timings from each run with main timer
    for output in tsmp.output:
        timer.merge_timings(output['timer'])
    tsmp.concat_timesteps()
    members = tsmp.concat_output['members']

    ###########################################################################
    # PART OF ANALYSIS FOR ENTIRE TIME SERIES
    if nl.i_aggreg_days:
        timer.start('agg')
        for skey,mem in members.items():
            for vkey,var in mem.items():
                mem[vkey].field = mem[vkey].field.mean(dim='time')
        timer.stop('agg')

    ###########################################################################
    # PLOTTING
    if not nl.i_remap:
        timer.start('plot')
        draw_plot(members)
        timer.stop('plot')

    timer.print_report()
