#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     
dependencies    
author			Christoph Heim
date created    04.12.2019
date changed    15.03.2021
usage           args:
                1st:    number of parallel tasks
                2nd:    var_name
                3nd:    i_recompute (1: yes, 0: no)
                4th:    pane_label 
                5th:    domain
                6th:    draw legend
"""
###############################################################################
import os, glob, collections
import numpy as np
import xarray as xr
import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime, timedelta
import nl_02 as nl
from package.nl_variables import nlv
from package.var_pp import var_mapping, compute_variable
from package.utilities import Timer, pickle_load, pickle_save
from package.plot_functions import PlotOrganizer, draw_map
from package.functions import (load_member_var, save_member_data_to_pickle,
                               load_member_data_from_pickle,
                               time_periods_to_dates)
from package.mp import TimeStepMP, IterMP
from package.member import Member
from package.comparison import Comparison
from package.var_pp import subsel_alt
###############################################################################

def draw_plot(members):

    # lists of all used resolutions in each model
    # used to select marker types
    res_lists = {}
    for mem_key,member in members.items():
        print(mem_key)
        if mem_key == 'OBS': continue
        mem_dict = member[nl.var_name].mem_dict
        if mem_dict['mod'] not in res_lists:
            res_lists[mem_dict['mod']] = [mem_dict['res']]
        else:
            res_lists[mem_dict['mod']].append(mem_dict['res'])
    for mem_key,res_list in res_lists.items():
        res_list.sort()

    name_dict = {'':'prof'}
    name_dict['dom'] = nl.cfg['domain']['code']
    name_dict[nl.sim_group] = nl.var_name
    PO = PlotOrganizer(i_save_fig=nl.i_save_fig,
                      path=os.path.join(nl.plot_base_dir,
                                        nl.cfg['domain']['code']),
                      name_dict=name_dict, nlp=nl.nlp, geo_plot=False)
    fig,axes = PO.initialize_plot(nrows=nl.nlp['nrows'],
                                  ncols=nl.nlp['ncols'],
                                  figsize=nl.nlp['figsize'])
    ax = axes[0, 0]

    for mem_key,member in members.items():
        mem_var = member[nl.var_name]
        # take mem_dict from namelist and not from saved pickle object
        mem_dict = nl.sim_src_dict[mem_key]

        ## quick fix for transformation of KEW --> abs(W)
        #if nl.var_name in ['KEW', 'KEWNORMI']:
        #    mem.var.values = np.sqrt(mem.var.values)

        #format member
        if mem_key == nl.obs_key:
        #if mem_key == 'OBS':
            linestyle = '-'
            color = 'black'
            linewidth = nl.nlp['obs_linewidth']
        else:
            res = mem_dict['res']
            if mem_key in nl.nlp['specific_mem_linestyles']:
                linestyle = nl.nlp['specific_mem_linestyles'][mem_key]
            else:
                linestyle = nl.nlp['linestyles'][
                        res_lists[mem_dict['mod']].index(res)]
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

        if 'alt' in mem_var.var.dims:
            vdim = 'alt'
            vdim_key = 'COORD_ALT'
            # select lowest Xkm (add some padding to make sure
            # lines do not end within plotting axes limits
            mem_var.var = subsel_alt(mem_var.var, mem_dict['mod'],
                                slice(nl.alt_limits.start,
                                      nl.alt_limits.stop*1.2))
            ylim = (nl.alt_limits.start, nl.alt_limits.stop)
        elif 'rel_alt' in mem_var.var.dims:
            vdim = 'rel_alt'
            vdim_key = 'COORD_RELALT'
            ylim = (nl.rel_alt_limits.start, nl.rel_alt_limits.stop)
        else:
            raise ValueError()


        if nl.plot_semilogx:
            handle, = ax.semilogx(mem_var.var.values, mem.var[vdim],
                             label=mem_dict['label'],
                             linewidth=linewidth,
                             color=color, linestyle=linestyle)
        else:
            handle, = ax.plot(mem_var.var.values, mem_var.var[vdim],
                             label=mem_dict['label'],
                             linewidth=linewidth,
                             color=color, linestyle=linestyle)
        PO.handles.append(handle)

    #if nl.i_plot_obs:
    #    mem = members['sounding']
    #    handle, = ax.plot(mem[nl.var_name].var.values,
    #                        mem[nl.var_name].var[vdim],
    #                        label=mem[nl.var_name].label,
    #                        linewidth=nl.nlp['obs_linewidth'], color='k')
    #    PO.handles.append(handle)

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
    ax.grid(linewidth=0.5)
    # draw vertical line at x = 0 if it is part of the x domain
    if ax.get_xlim()[0] < 0 and ax.get_xlim()[1] > 0:
        ax.axvline(color='grey')
    if nl.i_draw_legend:
        ax.legend(handles=PO.handles)
    fig.subplots_adjust(**nl.nlp['arg_subplots_adjust'])

    #PO.add_panel_labels(order='cols')
    # manually add the desired panel label
    if nl.plot_semilogx:
        pan_lab_x = ax.get_xlim()[0] * 0.22
    else:
        pan_lab_x = ax.get_xlim()[0] - (
                        ax.get_xlim()[1] - ax.get_xlim()[0]) * \
                        nl.nlp['panel_label_x_left_shift'] 
    pan_lab_y = ax.get_ylim()[0] + (
                    ax.get_ylim()[1] - ax.get_ylim()[0]) * \
                    nl.nlp['panel_label_y_pos'] 
    ax.text(pan_lab_x, pan_lab_y,
            nl.panel_label, fontsize=nl.nlp['panel_label_size'], weight='bold')

    PO.finalize_plot()


def compute_vars(date, members):
    ######## LOAD OBSERVATIONS
    ##########################################################################
    if nl.i_use_obs:
        obs_key = nl.var_obs_mapping[nl.var_name]
        obs_dict = nl.obs_src_dict[obs_key]
        # load observation variable
        var = load_member_var(nl.var_name, date, date, obs_dict,
                            nl.var_src_dict,
                            nl.var_src_dict[nl.var_name]['load'],
                            domain=nl.cfg['domain'], i_debug=nl.i_debug)
        if var is not None:
            var = var.mean(dim=['lon', 'lat', 'time'])

            member = Member(var, obs_dict, comparison=None)
            if 'OBS' not in members.keys():
                members['OBS'] = {}
            try:
                members['OBS'][nl.var_name] = member
            except TypeError:
                pass
        else:
            members['OBS'] = None

    ######## LOAD MODELS
    ##########################################################################
    for mem_key,mem_dict in nl.sim_src_dict.items():
        # load simulation variable
        var = load_member_var(nl.var_name, date, date, mem_dict,
                            nl.var_src_dict,
                            nl.var_src_dict[nl.var_name]['load'],
                            domain=nl.cfg['domain'], i_debug=nl.i_debug)

        if var is not None:
            if nl.mode in ['MEAN', 'SQRTMEAN']:
                # compute target variables and do stuff
                if 'lon' in var.dims:
                    var = var.mean(dim=['lon'])
                if 'lat' in var.dims:
                    var = var.mean(dim=['lat'])
                if 'time' in var.dims:
                    var = var.mean(dim=['time'])
                    var = var.expand_dims({'time':[date]})
            elif nl.mode == 'STD':
                pass
                #var = var.std(dim=['lon', 'lat'])
            else: raise NotImplementedError()

            # create member instance
            member = Member(var, mem_dict, comparison=None)
            if mem_key not in members.keys():
                members[mem_key] = {}
            if members[mem_key] is not None:
                members[mem_key][nl.var_name] = member
        else:
            members[mem_key] = None

    return(members)



def run_for_date(ts):
    """
    Organize full analysis for a given date (ts).
    ts has to be called ts because run_for_date is called from TimeStepMP.
    """
    timer = Timer(mode='seconds')
    members = {}
    
    # compute profiles
    members = compute_vars(ts, members)

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
    # should files be computed...
    if nl.i_recompute:
        tsmp = TimeStepMP(dates, njobs=nl.njobs, run_async=False)
        fargs = {}
        timer.start('compute')
        tsmp.run(run_for_date, fargs=fargs, step_args=None)
        tsmp.concat_timesteps()
        members = tsmp.concat_output['members']
        ###########################################################################
        # PART OF ANALYSIS FOR ENTIRE TIME SERIES
        timer.start('all')
        if nl.i_aggreg_days:
            for mem_key,member in members.items():
                for var_name in member.keys():
                    if nl.mode == 'MEAN':
                        member[var_name].var = member[var_name].var.mean(dim='time')
                    elif nl.mode == 'SQRTMEAN':
                        member[var_name].var = np.sqrt(
                                        member[var_name].var.mean(dim='time'))
                    #elif nl.mode == 'STD':
                    #    print(member[var_name].var.shape)
                    #    member[var_name].var = member[var_name].var.std(
                    #                            dim=['lon', 'lat', 'time'])
                    #    print(member[var_name].var.shape)
                    #    quit()
        else:
            raise NotImplementedError()
        timer.stop('all')
        timer.stop('compute')
        # save precomputed data
        Path(nl.pickle_dir).mkdir(exist_ok=True, parents=True)
        for mem_key,member in members.items():
            save_member_data_to_pickle(nl.pickle_dir, member,
                            nl.cfg['domain'], nl.var_name,
                            nl.time_periods)

    # ... or be reloaded from precomputed pickle files.
    else:
        # load precomputed data
        members = {}
        iter_mem_keys = list(nl.sim_src_dict.keys())
        if nl.i_use_obs: iter_mem_keys.append('OBS')
        for mem_key in iter_mem_keys:
            if mem_key == 'OBS':
                mem_dict = nl.obs_src_dict[nl.var_obs_mapping[nl.var_name]]
            else:
                mem_dict = nl.sim_src_dict[mem_key] 
            members[mem_key] = load_member_data_from_pickle(nl.pickle_dir,
                            mem_dict, nl.cfg['domain'], nl.var_name,
                            nl.time_periods, nl.i_skip_missing)

    # If no member available abort
    any_data = False
    for mem_key,member in members.items():
        if len(member) > 0:
            any_data = True
    if not any_data:
        raise ValueError('No member contains data. '+
                        'Maybe recompute? Wrong dates?')


    ############################################################################
    ## PART OF ANALYSIS FOR ENTIRE TIME SERIES
    #timer.start('all')
    #if nl.i_aggreg_days:
    #    for mem_key,member in members.items():
    #        for var_name in member.keys():
    #            print(var_name)
    #            quit()
    #            member[var_name].var = member[var_name].var.mean(dim='time')
    #else:
    #    raise NotImplementedError()

    ## prepare sounding data
    #if nl.i_plot_obs:
    #    sounding = preproc_sounding(nl.var_name, n_lowest=27)
    #    sounding = sounding.sel(time=slice(nl.first_date, 
    #                                    nl.last_date+timedelta(days=1)))
    #    if nl.i_aggreg_days:
    #        timer.start('agg')
    #        sounding = sounding.mean(dim='time')
    #        timer.stop('agg')
    #    else:
    #        raise NotImplementedError()
    #    sounding = Member(sounding, {'label':'OBS (St. Helena)'}, variable=None)
    #    # add sounding to members
    #    members['sounding'] = {nl.var_name:sounding}
    #    #print(members['sounding']['T'].field.values)
    #timer.stop('all')

    ###########################################################################
    # PLOTTING
    if nl.i_plot:
        timer.start('plot')
        draw_plot(members)
        timer.stop('plot')

    timer.print_report()
