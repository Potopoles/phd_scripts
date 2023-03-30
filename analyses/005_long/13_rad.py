#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Compute radiative balance.
author			Christoph Heim
date created    02.07.2021
date changed    02.07.2021
usage           args:
"""
###############################################################################
import copy#, os, glob, collections
import numpy as np
#import xarray as xr
import matplotlib.pyplot as plt
from pathlib import Path
#from datetime import datetime, timedelta
import nl_13 as nl
from package.nl_variables import nlv
#from package.constants import CON_RAD_EARTH
#from nl_var_src import ANA_NATIVE
#from package.var_pp import var_mapping, compute_variable
from package.utilities import Timer#, dt64_to_dt, subsel_domain
from package.utilities import Time_Processing as TP
from package.plot_functions import PlotOrganizer
from package.functions import (load_member_var, save_member_data_to_pickle,
                               load_member_data_from_pickle,
                               time_periods_to_dates)
from package.mp import TimeStepMP
from package.member import Member
#from package.comparison import Comparison
###############################################################################


def draw_plot(ts, members):

    def plot_var(ax, x, var_name, members, sign=1, hatch='',
                add_xlabel=True):
        legend = {'colors':[], 'labels':[]}
        if add_xlabel:
            xticks_pos.append(x + dx_mem * (len(members)/2.-0.5))
            xticks_lab.append(nlv[var_name]['label'])
        for mem_key,member in members.items():
            print(mem_key)
            print(member[var_name].var.values)

            if hatch == '':
                color = nl.nlp['colors'][
                        nl.nlp['mem_col_inds'].index(mem_key)]
            else:
                color = 'none'


            ax.bar(x, sign * member[var_name].var,
                   width=dx_mem,
                   facecolor=color,
                   edgecolor='k',
                   hatch=hatch)
            legend['colors'].append(color)
            legend['labels'].append(member[var_name].mem_dict['label'])

            x += dx_mem

        x += dx_var
        legend['handles'] = [plt.Rectangle((0,0),1,1, color=legend['colors'][i]) \
                        for i in range(len(legend['colors']))]
        return(x, legend)

    timer = Timer(mode='seconds')
    timer.start('plot')

    # retrieve member keys
    mem_keys = list(members.keys())

    ## SET UP PLOT IO PATHS
    #########################################################################
    name_dict = {}
    name_dict['rad']          = nl.plot_domain['key']
    name_dict[nl.plot_mode]   = ''

    PO = PlotOrganizer(i_save_fig=nl.args.i_save_fig, path=nl.plot_base_dir,
                      name_dict=name_dict, nlp=nl.nlp, geo_plot=False)
    fig,axes = PO.initialize_plot(nrows=nl.nlp['nrows'],
                                  ncols=nl.nlp['ncols'],
                                  figsize=nl.nlp['figsize'])

    ## COMPUTE ABSOLUTE AND RELATIVE DIFFERENCE
    #########################################################################
    rel_diff_members = {}
    abs_diff_members = {}
    for mem_key,mem_dict in members.items():
        rel_diff_members[mem_key] = {}
        abs_diff_members[mem_key] = {}
        for var_name in nl.var_names:
            rel_diff_members[mem_key][var_name] = copy.deepcopy(
                                    members[mem_key][var_name])
            abs_diff_members[mem_key][var_name] = copy.deepcopy(
                                    members[mem_key][var_name])
            rel_diff_members[mem_key][var_name].var = (
                            (rel_diff_members[mem_key][var_name].var /
                            members[nl.ref_mem_key][var_name].var) - 1) * 100
            abs_diff_members[mem_key][var_name].var = (
                            abs_diff_members[mem_key][var_name].var -
                            members[nl.ref_mem_key][var_name].var)
         

    ## DRAW PLOT
    #########################################################################
    ax = axes[0,0]
    # namelist
    dx_margin = 5
    dx_mem = 5
    dx_var = 2
    xlims = (0,100)
    ylims = (-400,400)
    xticks_lab = []
    xticks_pos = []

    if nl.plot_mode == 'abs_val':
        plot_members = members
    elif nl.plot_mode == 'abs_diff':
        plot_members = abs_diff_members
    elif nl.plot_mode == 'rel_diff':
        plot_members = rel_diff_members

    # first computations
    n_mems = len(nl.mem_src_dict)

    #ax.set_xlim(xlims)
    #ax.set_ylim(ylims)


    x = dx_margin

    ## SHORTWAVE DOWNWARD
    sign = 1
    var_name = 'SWDTOA'
    if var_name in nl.var_names:
        x, legend = plot_var(ax, x, var_name, plot_members, sign=sign)

    ## SHORTWAVE UPWARD
    sign = -1
    var_name = 'SWUTOA'
    if var_name in nl.var_names:
        xbefore = x
        x, legend = plot_var(ax, x, var_name, plot_members, sign=sign)
        x = xbefore
    var_name = 'CSWUTOA'
    if var_name in nl.var_names:
        x, dummy = plot_var(ax, x, var_name, plot_members, hatch='///',
                    add_xlabel=False, sign=sign)

    ## SHORTWAVE NET DOWNWARD
    sign = 1
    var_name = 'SWNDTOA'
    if var_name in nl.var_names:
        xbefore = x
        x, legend = plot_var(ax, x, var_name, plot_members, sign=sign)
        x = xbefore
    var_name = 'CSWNDTOA'
    if var_name in nl.var_names:
        x, dummy = plot_var(ax, x, var_name, plot_members, hatch='///',
                    add_xlabel=False, sign=sign)

    ## LONGWAVE UPWARD
    sign = -1
    var_name = 'LWUTOA'
    if var_name in nl.var_names:
        xbefore = x
        x, legend = plot_var(ax, x, var_name, plot_members, sign=sign)
        x = xbefore
    var_name = 'CLWUTOA'
    if var_name in nl.var_names:
        x, dummy = plot_var(ax, x, var_name, plot_members, hatch='///',
                    add_xlabel=False, sign=sign)

    ## TOTAL NET DOWNWARD
    sign = 1
    var_name = 'RADNDTOA'
    if var_name in nl.var_names:
        xbefore = x
        x, legend = plot_var(ax, x, var_name, plot_members, sign=sign)
        x = xbefore
    var_name = 'CRADNDTOA'
    if var_name in nl.var_names:
        x, dummy = plot_var(ax, x, var_name, plot_members, hatch='///',
                    add_xlabel=False, sign=sign)

    #quit()
    #dxax_var = (xlims[1] - xlims[0])/len(nl.var_names)
    #dxax_mem = dxax_var/n_mems

    ## SWNDTOA
    #print(dxax_var + dxax_mem * mem_ind)



    ### FINALIZE PLOT
    ax.legend(legend['handles'], legend['labels'])
    ax.set_xticks(xticks_pos)
    ax.set_xticklabels(xticks_lab)
    if nl.plot_mode == 'abs_val':
        ax.set_ylabel('\u2193 flux [$W$ $m^{-2}$]')
    elif nl.plot_mode == 'abs_diff':
        ax.set_ylabel('\u2193 flux difference (PGW - CTRL) [$W$ $m^{-2}$]')
    else: raise NotImplementedError()

    if nl.nlp['i_draw_panel_labels']:
        PO.add_panel_labels(order='cols',
                        start_ind=nl.nlp['panel_labels_start_ind'])
    fig.subplots_adjust(**nl.nlp['arg_subplots_adjust'])

    PO.finalize_plot()

    timer.stop('plot')
    output = {'timer':timer}
    return(output)



def compute_field(date, members):

    ######## LOAD MODELS
    ##########################################################################
    for mem_key,mem_dict in nl.mem_src_dict.items():
        for var_name in nl.var_names:
            # load variable
            var = load_member_var(var_name, date, date, mem_dict,
                                nl.var_src_dict,
                                nl.var_src_dict[var_name]['load'],
                                domain=nl.plot_domain, i_debug=nl.i_debug)
            if var is not None:
                # average horizontally
                var = var.mean(dim=['lon', 'lat'])

                # resample to daily mean values.
                var = TP.process(var, { TP.ACTION:TP.RESAMPLE, 
                                        TP.FREQUENCY:'D', 
                                        TP.OPERATOR:TP.MEAN  })

                # create member instance
                member = Member(var, mem_dict, comparison=None)
                if mem_key not in members.keys():
                    members[mem_key] = {}
                if members[mem_key] is not None:
                    members[mem_key][var_name] = member
            else:
                members[mem_key] = None
    return(members)


def run_for_date(ts):
    """
    Organize full analysis for a given date (ts).
    ts has to be called ts because run_for_date is called from TimeStepMP.
    """
    timer = Timer(mode='seconds')
    if nl.i_debug >= 2:
        print('{:%Y%m%d}'.format(ts))

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
    # should files be computed...
    if nl.args.i_recompute:
        tsmp = TimeStepMP(dates, njobs=nl.args.n_par, run_async=False)
        fargs = {}
        tsmp.run(run_for_date, fargs=fargs, step_args=None)
        # merge timings from each run with main timer
        for output in tsmp.output:
            timer.merge_timings(output['timer'])
        tsmp.concat_timesteps()
        members = tsmp.concat_output['members']


        #######################################################################
        # PART OF ANALYSIS FOR ENTIRE TIME SERIES

        # compute aggregation/grouping on entire time series
        timer.start('comp')
        for mem_key,member in members.items():
            for var_name in nl.var_names:
                var = member[var_name].var

                ### RESAMPLE FULL TIME SERIES
                members[mem_key][var_name].var = \
                            TP.process(var, { TP.ACTION:TP.RESAMPLE, 
                                        TP.FREQUENCY:None, 
                                        TP.OPERATOR:TP.MEAN  })
        timer.stop('comp')

        # save precomputed data
        Path(nl.pickle_dir).mkdir(exist_ok=True, parents=True)
        for mem_key,member in members.items():
            #for var_name in nl.var_names:
            save_member_data_to_pickle(nl.pickle_dir, member,
                            nl.plot_domain, nl.var_names,
                            nl.time_periods)

        
    # ... or be reloaded from precomputed pickle files.
    else:
        # load precomputed data
        members = {}
        iter_mem_keys = list(nl.mem_src_dict.keys())
        for mem_key in iter_mem_keys:
            mem_dict = nl.mem_src_dict[mem_key] 
            members[mem_key] = load_member_data_from_pickle(nl.pickle_dir,
                            mem_dict, nl.plot_domain, nl.var_names,
                            nl.time_periods, nl.i_skip_missing)

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
