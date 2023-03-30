#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Interpolate model data onto locations of dardar tracks. 
author			Christoph Heim
date created    28.04.2020
date changed    11.05.2021
usage           args:
"""
###############################################################################
import copy, os, glob, time, warnings
import numpy as np
import xarray as xr
from pathlib import Path
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import nl_12 as nl
from package.nl_models import nlm
from package.nl_variables import nlv,dimx,dimy,dimz,dimt
from package.var_pp import compute_variable, var_mapping
from package.utilities import Timer, subsel_domain
from package.utilities import Time_Processing as TP
from package.plot_functions import PlotOrganizer
from package.mp import TimeStepMP
from package.functions import load_member_var
from package.member import Member
from package.nc_compression import (compress_date_conserving, find_minmax_val,
                                    compress_date_lossy)
from package.functions import (load_member_var, save_member_data_to_pickle,
                               load_member_data_from_pickle,
                               time_periods_to_dates)
from package.model_pp import MODEL_PP, MODEL_PP_DONE
from package.var_pp import DERIVE, DIRECT
from package.var_pp import subsel_alt
###############################################################################


def draw_plot(members):

    name_dict = {'':'prof'}
    name_dict[''] = nl.plot_domain['key']
    name_dict[nl.sim_group] = nl.var_name
    PO = PlotOrganizer(i_save_fig=nl.args.i_save_fig,
                      path=os.path.join(nl.plot_base_dir,
                                        nl.plot_domain['key']),
                      name_dict=name_dict, nlp=nl.nlp, geo_plot=False)
    fig,axes = PO.initialize_plot(nrows=nl.nlp['nrows'],
                                  ncols=nl.nlp['ncols'],
                                  figsize=nl.nlp['figsize'])
    ax = axes[0, 0]

    for mem_key,member in members.items():
        print(mem_key)
        mem_var = member[nl.var_name]
        # take mem_dict from namelist and not from saved pickle object
        mem_dict = nl.sim_src_dict[mem_key]

        #format member
        if mem_key == nl.obs_key:
            linestyle = '-'
            color = 'black'
            linewidth = nl.nlp['obs_linewidth']
        else:
            if mem_key in nl.nlp['specific_mem_linestyles']:
                linestyle = nl.nlp['specific_mem_linestyles'][mem_key]
            else:
                linestyle = '-'
            # either take predefined color or take it from nlp
            #if 'color' in mem_dict:
            #    color = mem_dict['color']
            if nl.nlp['unique_colors']:
                mem_ind = (list(members.keys()).index(mem_key)-0)/(
                            (len(members.keys())-2)-0)
                #color = matplotlib.cm.get_cmap('Spectral')(mem_ind)
                color = matplotlib.cm.get_cmap('viridis')(mem_ind)
            else:
                if mem_key in nl.nlp['specific_mem_colors']:
                    color = nl.nlp['specific_mem_colors'][mem_key]
                else:
                    color = nl.nlp['colors'][nl.nlp['mod_col_inds'].index(mem_dict['mod'])]
            linewidth = nl.nlp['mod_linewidth']

        vdim = 'alt'
        vdim_key = 'COORD_ALT'
        # select lowest Xkm (add some padding to make sure
        # lines do not end within plotting axes limits
        mem_var.var = subsel_alt(mem_var.var, mem_dict['mod'],
                            slice(nl.alt_limits.start,
                                  nl.alt_limits.stop*1.2))
        ylim = (nl.alt_limits.start, nl.alt_limits.stop)


        handle, = ax.plot(mem_var.var.values, mem_var.var[vdim],
                         label=mem_dict['label'],
                         linewidth=linewidth,
                         color=color, linestyle=linestyle)
        PO.handles.append(handle)

    # manually setting of ticks
    if nl.xticks is not None:
        ax.set_xticks(nl.xticks)

    ax.set_ylim(ylim)
    # for > 0 fields, set xmin to 0
    if nl.xlims is None:
        if nl.min_zero:
            ax.set_xlim(xmin=0.)
    else:
        ax.set_xlim(nl.xlims)

    PO.set_axes_labels(ax, nl.var_name, vdim_key)
    ax.grid()
    # draw vertical line at x = 0 if it is part of the x domain
    if ax.get_xlim()[0] < 0 and ax.get_xlim()[1] > 0:
        ax.axvline(color='grey')
    if nl.i_draw_legend:
        ax.legend(handles=PO.handles)
    fig.subplots_adjust(**nl.nlp['arg_subplots_adjust'])

    #PO.add_panel_labels(order='cols')
    # manually add the desired panel label
    pan_lab_x = ax.get_xlim()[0] - (
                    ax.get_xlim()[1] - ax.get_xlim()[0]) * \
                    nl.nlp['panel_label_x_left_shift'] 
    pan_lab_y = ax.get_ylim()[0] + (
                    ax.get_ylim()[1] - ax.get_ylim()[0]) * \
                    nl.nlp['panel_label_y_pos'] 
    ax.text(pan_lab_x, pan_lab_y,
            nl.panel_label, fontsize=nl.nlp['panel_label_size'], weight='bold')

    PO.finalize_plot()



def compute_field(date, members):
    if nl.i_debug >= 1:
        print('{:%Y%m%d}'.format(date))
    out_files = []
    tmp_out_files = []

    domain = nl.plot_domain
    mem_key = nl.args.mem_key
    mem_dict = nl.sim_src_dict[mem_key]
    sim_key = mem_dict['sim']

    ######## LOAD MODEL AND DARDAR DATA
    ##########################################################################
    # dardar data
    var_dar = load_member_var(nl.dar_var_name, date, date, nl.dardar_dict,
                        {nl.dar_var_name:{
                            'load':DIRECT,
                            'src_path':nl.inp_base_dir,
                            'dom_key':nl.ANA_NATIVE_domain['key']}}, 
                        DIRECT, i_debug=nl.i_debug, supress_model_pp=False)
    lon_dar = load_member_var('lon', date, date, nl.dardar_dict,
                        {'lon':{
                            'load':DIRECT,
                            'src_path':nl.inp_base_dir,
                            'dom_key':nl.ANA_NATIVE_domain['key']}}, 
                        DIRECT, i_debug=nl.i_debug, supress_model_pp=True)
    lat_dar = load_member_var('lat', date, date, nl.dardar_dict,
                        {'lat':{
                            'load':DIRECT,
                            'src_path':nl.inp_base_dir,
                            'dom_key':nl.ANA_NATIVE_domain['key']}}, 
                        DIRECT, i_debug=nl.i_debug, supress_model_pp=True)

    ### manually select domain for dardar (but only if data is available)
    if lat_dar is not None:
        use_mask = np.repeat(True, len(lat_dar))

        use_mask[lon_dar < nl.plot_domain['lon'].start] = False
        use_mask[lon_dar > nl.plot_domain['lon'].stop] = False
        use_mask[lat_dar < nl.plot_domain['lat'].start] = False
        use_mask[lat_dar > nl.plot_domain['lat'].stop] = False

        # if no points in domain set date to None
        if np.sum(use_mask) == 0:
            var_mod = None
            var_dar = None
        # else select measurements within domain
        else:
            use_mask = xr.Dataset(
                    data_vars = dict(
                        mask=(['time'], use_mask),
                    ),
                    coords = dict(
                        time = (['time'], var_dar.time),
                    )
                ).mask
            #print(lon_dar.shape)
            #print(lat_dar.shape)
            #print(var_dar.shape)
            lon_dar = lon_dar.where(use_mask, drop=True)
            lat_dar = lat_dar.where(use_mask, drop=True)
            var_dar = var_dar.where(use_mask, drop=True)
            #print(lon_dar.shape)
            #print(lat_dar.shape)
            #print(var_dar.shape)
            #quit()

            ## sort after time since some of them are not sorted (why???)
            lat_dar = lat_dar.sortby(var_dar.time)
            lon_dar = lon_dar.sortby(var_dar.time)
            var_dar = var_dar.sortby(var_dar.time)


    # load model data for this an last day for best possible time interpolation
    var_mod_this_day = load_member_var(nl.mod_var_name, date, date, mem_dict,
                        nl.var_src_dict, nl.var_src_dict[nl.mod_var_name]['load'],
                        i_debug=nl.i_debug, supress_model_pp=False,
                        domain=nl.plot_domain)
    var_mod_last_day = load_member_var(nl.mod_var_name, date-timedelta(days=1), 
                        date-timedelta(days=1), mem_dict,
                        nl.var_src_dict, nl.var_src_dict[nl.mod_var_name]['load'],
                        i_debug=nl.i_debug, supress_model_pp=False,
                        domain=nl.plot_domain)

    # concatenate them
    if (var_mod_last_day is not None) and (var_mod_this_day is not None):
        var_mod = xr.concat([var_mod_last_day, var_mod_this_day], dim='time')
    else:
        # only do analysis if both days are available
        var_mod = None
        var_dar = None
    #elif (var_mod_last_day is not None):
    #    var_mod = var_mod_last_day
    #elif (var_mod_this_day is not None):
    #    var_mod = var_mod_this_day


    if (var_mod is not None) and (var_dar is not None):

        # not necessary for sel
        #var_dar['time'] = var_dar.time.dt.round('3H')

        var_mod = var_mod.sel(lat=lat_dar, lon=lon_dar, time=var_dar.time, 
                                method='nearest')
        #var_mod = var_mod.interp(lat=lat_dar, lon=lon_dar, time=var_dar.time)

        #fig,axes = plt.subplots(1,2, figsize=(10,5))
        #axes[0].pcolormesh(var_mod.lat, var_mod.alt, var_mod.T)
        #axes[0].set_ylim((0,4000))
        #axes[1].pcolormesh(lat_dar, var_dar.alt, var_dar.T)
        #axes[1].set_ylim((0,4000))
        #plt.show()
        #plt.plot(var_mod.mean(dim='time'), var_mod.alt)
        #plt.plot(var_dar.mean(dim='time'), var_dar.alt)
        #plt.ylim((0,4000))
        #plt.show()
        #quit()


        ## determine cloud top
        if nl.var_name == 'LCLDTOP':
            var_alt_flip = var_dar.sel(alt=slice(None, None, -1))
            cloud_top_ind = np.argmax(copy.deepcopy(var_alt_flip.values), axis=1)
            cloud_top = np.take(copy.deepcopy(var_alt_flip.alt.values), cloud_top_ind)
            cloud_top[cloud_top_ind == 0] = np.nan
            ##cloud_top += 30 #TODO
            var_dar = var_dar.mean(dim='alt')
            var_dar.values = cloud_top


            var_alt_flip = var_mod.sel(alt=slice(None, None, -1))
            cloud_top_ind = np.argmax(copy.deepcopy(var_alt_flip.values), axis=1)
            cloud_top = np.take(copy.deepcopy(var_alt_flip.alt.values), cloud_top_ind)
            cloud_top[cloud_top_ind == 0] = np.nan
            ##cloud_top += 30 #TODO
            var_mod = var_mod.mean(dim='alt')
            var_mod.values = cloud_top

            #print(var_mod)

            #plt.plot(lat_dar, var_dar)
            #plt.plot(lat_dar, var_mod)
            #plt.show()
            #quit()


        elif nl.var_name == 'CLDMASK':
            var_mod = var_mod.max(dim='alt')
            var_dar = var_dar.max(dim='alt')

        elif nl.var_name == 'INVHGT':
            ##plt.pcolormesh(lat_dar, var_dar.alt, var_dar.differentiate(coord='alt').T)
            ##plt.colorbar()
            #max_inv_ind = np.argmax(copy.deepcopy(var_dar.differentiate(coord='alt').values), axis=1)
            #invhgt = np.take(copy.deepcopy(var_dar.alt.values), max_inv_ind)
            #var_dar = var_dar.mean(dim='alt')
            #var_dar.values = invhgt
            ##plt.plot(lat_dar, var_dar)
            ##plt.show()
            ##quit()

            # TODO tmp:
            var_alt_flip = var_dar.sel(alt=slice(None, None, -1))
            cloud_top_ind = np.argmax(copy.deepcopy(var_alt_flip.values), axis=1)
            cloud_top = np.take(copy.deepcopy(var_alt_flip.alt.values), cloud_top_ind)
            cloud_top[cloud_top_ind == 0] = np.nan
            ##cloud_top += 30 #TODO
            var_dar = var_dar.mean(dim='alt')
            var_dar.values = cloud_top



        mem_mod = Member(var_mod, mem_dict, comparison=None)
        mem_dar = Member(var_dar, nl.dardar_dict, comparison=None)
        if mem_key not in members.keys():
            members[mem_key] = {}
        if members[mem_key] is not None:
            members[mem_key][nl.var_name] = mem_mod
        mem_key = 'DARDAR_CLOUD'
        if mem_key not in members.keys():
            members[mem_key] = {}
        if members[mem_key] is not None:
            members[mem_key][nl.var_name] = mem_dar
    else:
        members[mem_key] = None
        members['DARDAR_CLOUD'] = None
            
    return(members)




def run_computation(ts):
    """
    Organize variable computation for a given date (ts).
    ts has to be called ts because run_for_date is called from TimeStepMP.
    """
    timer = Timer(mode='seconds')
    
    # compute field
    timer.start('var')
    members = {}
    members = compute_field(ts, members)
    timer.stop('var')

    output = {'timer':timer, 'members':members}
    return(output)
    

if __name__ == '__main__':

    ###########################################################################
    # PREPARATION STEPS
    timer = Timer(mode='seconds')
    Path(nl.ana_base_dir).mkdir(parents=True, exist_ok=True)
    dates = time_periods_to_dates(nl.time_periods)

    ###########################################################################
    # PART OF ANALYSIS SPECIFIC FOR EACH DAY

    ###########################################################################
    # COMPUTE FIELD
    if nl.args.i_recompute:
        print('COMPUTE')
        timer.start('compute')
        mem_dict = nl.sim_src_dict[nl.args.mem_key]

        tsmp = TimeStepMP(dates, njobs=nl.args.n_par, run_async=True)
        fargs = {}
        tsmp.run(run_computation, fargs=fargs, step_args=None)

        # merge timings from each run with main timer
        for output in tsmp.output:
            timer.merge_timings(output['timer'])
        tsmp.concat_timesteps()
        members = tsmp.concat_output['members']
        #print(members)
        #quit()

        for mem_key,member in members.items():
            #print(mem_key)
            var = copy.deepcopy(member[nl.var_name].var)

            ### RESAMPLE MONTHLY
            if nl.time_mode in [nl.ANNUAL_CYCLE, nl.MONTHLY_SERIES]:
                var = TP.process(var, { TP.ACTION:TP.RESAMPLE, 
                                        TP.FREQUENCY:'M', 
                                        TP.OPERATOR:TP.MEAN  })

            ### COMPUTE ANNUAL CYCLE
            if nl.time_mode == nl.ANNUAL_CYCLE:
                # split up member var into multiple vars containing the
                # specific statistical measures
                members[mem_key][nl.var_name].var = {}
                for time_mode in [TP.MEAN, TP.MIN, TP.P25, TP.P75, TP.MAX]:
                    members[mem_key][nl.var_name].var[time_mode] = \
                                 TP.process(copy.deepcopy(var), 
                                          { TP.ACTION:TP.GROUPBY, 
                                            TP.FREQUENCY:'M',
                                            TP.OPERATOR:time_mode })

                # split up member var into multiple vars containing the
                # individual years
                yearly_var = TP.process(copy.deepcopy(var), 
                                      { TP.ACTION:TP.GROUPBY, 
                                        TP.FREQUENCY:'Y',
                                        TP.OPERATOR:None })
                for year,var in yearly_var.items():
                    # convert datetime to month 
                    months = var['time.month']
                    var = var.rename(time='month')
                    var['month'].values = months
                    ### make sure month 1 is there..
                    ##if 1 not in months:
                    ##    month_1 = xr.DataArray(np.nan, [('month', [1])])
                    ##    var = xr.concat([month_1, var], dim='month')
                    members[mem_key][nl.var_name].var[year] = var

        #for mem_key,member in members.items():
        #    print(mem_key)
        #    print(member[nl.var_name].var)

        print('DONE. computed variable {}.'.format(nl.var_name))
        print('for member: {}'.format(nl.args.mem_key))
        timer.stop('compute')

        #######################################################################
        # SAVE DATA
        Path(nl.pickle_dir).mkdir(exist_ok=True, parents=True)
        for mem_key,member in members.items():
            save_member_data_to_pickle(nl.pickle_dir, member,
                            nl.plot_domain, nl.var_name,
                            nl.time_periods,
                            append=nl.time_mode)

    # ... or be reloaded from precomputed pickle files.
    else:
        raise NotImplementedError('Plot this stuff with 09_profiles')
        #######################################################################
        # LOAD DATA
        members = {}
        for mem_key in [nl.args.mem_key, 'DARDAR_CLOUD']:
            mem_dict = nl.sim_src_dict[mem_key] 
            members[mem_key] = load_member_data_from_pickle(nl.pickle_dir,
                            mem_dict, nl.plot_domain, nl.var_name,
                            nl.time_periods, nl.i_skip_missing)

    # If no member available abort
    any_data = False
    for mem_key,member in members.items():
        if len(member) > 0:
            any_data = True
    if not any_data:
        raise ValueError('No member contains data. '+
                        'Maybe recompute? Wrong dates?')

    ###########################################################################
    # PLOTTING
    if nl.i_plot:


        timer.start('plot')
        draw_plot(members)
        timer.stop('plot')


    timer.print_report()
