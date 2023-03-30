#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Create spatial mean time line plots.
author			Christoph Heim
date created    21.11.2020
date changed    03.03.2020
usage           args:
                1st:    number of parallel tasks
                2nd:    i_save_fig (0: show, 1: png, 2: pdf, 3: jpg)
"""
###############################################################################
import os, glob, collections, copy
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
from datetime import datetime, timedelta
from scipy.stats import linregress, skew
import nl_09 as nl
from package.nl_variables import nlv
from package.var_pp import var_mapping, compute_variable
from package.utilities import Timer, dt64_to_dt
from package.plot_functions import PlotOrganizer, draw_map
from package.functions import load_member_var, time_periods_to_dates
from package.mp import TimeStepMP, IterMP
from package.member import Member
from package.comparison import Comparison
###############################################################################


def draw_plot(ts, members):
    timer = Timer(mode='seconds')
    timer.start('plot')
    
    name_dict = {}
    name_dict['timeline']   = nl.domain['code']
    name_dict[nl.i_aggreg]        = nl.var_name
    out_path = nl.plot_base_dir

    #comparison = Comparison(nl.var_name, members)   
    #comparison.calc_statistics()

    PO = PlotOrganizer(i_save_fig=nl.i_save_fig, path=out_path,
                      name_dict=name_dict, nlp=nl.nlp, geo_plot=False)
    fig,axes = PO.initialize_plot(nrows=nl.nlp['nrows'],
                                  ncols=nl.nlp['ncols'],
                                  figsize=nl.nlp['figsize'])
    ax = axes[0,0]

    for mem_key,member in members.items():
        print(mem_key)
        if nl.var_name not in member:
            continue
        #print(member[nl.var_name].mem_dict)
        #quit()

        if mem_key == nl.obs_key: 
            color = nl.nlp['OBS_color']
        elif mem_key == 'ERA5_31': 
            color = nl.nlp['OBS_color']
        else:
            mod_key = nl.sim_src_dict[mem_key]['mod']
            color = nl.nlp['colors'][nl.nlp['mod_col_inds'].index(mod_key)]

        handle, = ax.plot(member[nl.var_name].var.time,
                        member[nl.var_name].var.values, marker='o',
                        label=member[nl.var_name].mem_dict['label'],
                        color=color)
        PO.handles.append(handle)

        locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
        formatter = mdates.ConciseDateFormatter(locator)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)

        if nl.i_plot_trend_line:
            nts = len(member[nl.var_name].var.values)
            slope,intercept,r_val,p_val,std_err = linregress(
                                np.arange(nts),
                                member[nl.var_name].var.values)
            trend_line = intercept + np.arange(nts) * slope 
            ax.plot(member[nl.var_name].var.time, trend_line,
                    color=handle.get_color(), linestyle='--')

    #if nl.i_compute_corr:
    #    corr_vals = np.corrcoef(xvals.values[~np.isnan(xvals.values)],
    #                       yvals.values[~np.isnan(yvals.values)])[0,1]


    #ax.legend(handles=PO.handles)

    PO.add_panel_labels(order='cols',
                    start_ind=nl.nlp['panel_labels_start_ind'])
    fig.subplots_adjust(**nl.nlp['subplts'])

    PO.set_axes_labels(ax, 'COORD_DATETIME', nl.var_name)

    PO.finalize_plot()

    timer.stop('plot')
    output = {'timer':timer}
    return(output)



def compute_field(date, members):

    ######## LOAD MEMBERS
    ##########################################################################
    for mem_key,mem_dict in nl.sim_src_dict.items():
        var = load_member_var(nl.var_name, date, date, mem_dict,
                            nl.var_src_dict,
                            nl.var_src_dict[nl.var_name]['load'],
                            domain=nl.domain, i_debug=nl.i_debug)

        if var is not None:
            if nl.i_aggreg is not 'none':
                var = var.mean(dim='time')
                var = var.expand_dims({'time':[date]})
            var = var.mean(dim=['lon', 'lat'])

            # create member instance
            member = Member(var, mem_dict,
                              #{'label':sdict['label'],'res':sdict['res']},
                              comparison=None)
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
    # compute field
    timer.start('var')
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
    timer.start('comp')
    for mem_key,member in members.items():
        if nl.i_aggreg == 'all':
            member[nl.var_name].var = \
                            member[nl.var_name].var.mean(dim='time')
        elif nl.i_aggreg == 'yearly':
            member[nl.var_name].var = member[nl.var_name].var.resample(
                                        {'time':'1Y'}).mean(dim='time')
        elif nl.i_aggreg == 'monthly':
            member[nl.var_name].var = member[nl.var_name].var.resample(
                                        {'time':'1MS'}).mean(dim='time')
        elif nl.i_aggreg == 'daily':
            pass
        elif nl.i_aggreg == 'none':
            pass
        else: raise NotImplementedError()
    timer.stop('comp')

    ###########################################################################
    # PLOTTING
    # quit now if not plotting required
    if not nl.i_plot:
        timer.print_report()
        quit()
    timer.start('plot')
    draw_plot(ts=None, members=members)
    timer.stop('plot')

    timer.print_report()
