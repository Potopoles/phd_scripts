#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     
dependencies    
author			Christoph Heim
date created    14.01.2021
date changed    22.01.2021
usage           args:
                1st:    number of parallel tasks
                2nd:    var_name
                3nd:    i_recompute (1: yes, 0: no)
                4th:    pane_label 
                5th:    domain
                6th:    model_keys
"""
###############################################################################
import os, glob, collections
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime, timedelta
from pandas.plotting import register_matplotlib_converters
from sklearn.linear_model import LinearRegression
import nl_10 as nl
from package.nl_mem_src import mem_src
from package.nl_variables import nlv
from package.var_pp import var_mapping, compute_variable
from package.utilities import (Timer, pickle_load, pickle_save,
                                select_common_timesteps)
from package.plot_functions import PlotOrganizer, draw_map
from package.functions import (load_member_var, save_member_data_to_pickle,
                               load_member_data_from_pickle,
                               time_periods_to_dates)
from package.mp import TimeStepMP, IterMP
from package.member import Member
from package.comparison import Comparison
from package.var_pp import subsel_alt
###############################################################################

def plot_line(ax, var_name, member, mem_dict, linestyle, color):
    plot_var = member[var_name].var
    plot_var = plot_var.resample({'time':'1D'}).mean()
    plot_var -= plot_var.mean()
    plot_var /= plot_var.std()
    handle, = ax.plot(plot_var.time.values,
                     plot_var.values,
                     label=mem_dict['label'],
                     linewidth=nl.nlp['mod_linewidth'],
                     color=color, linestyle=linestyle)
    return(handle)

def draw_plot(members):
    register_matplotlib_converters()

    # lists of all used resolutions in each model
    # used to select marker types
    res_lists = {}
    for mem_key,member in members.items():
        if mem_key == 'OBS': continue
        mem_dict = member[nl.main_var_name].mem_dict
        if mem_dict['mod'] not in res_lists:
            res_lists[mem_dict['mod']] = [mem_dict['res']]
        else:
            res_lists[mem_dict['mod']].append(mem_dict['res'])
    for mem_key,res_list in res_lists.items():
        res_list.sort()

    name_dict = {'':'olr_bias'}
    name_dict['dom'] = nl.cfg['domain']['code']
    name_dict['var'] = nl.main_var_name
    PO = PlotOrganizer(i_save_fig=nl.i_save_fig,
                      path=os.path.join(nl.plot_base_dir,
                                        nl.cfg['domain']['code']),
                      name_dict=name_dict, nlp=nl.nlp, geo_plot=False)
    fig,axes = PO.initialize_plot(nrows=nl.nlp['nrows'],
                                  ncols=nl.nlp['ncols'],
                                  figsize=nl.nlp['figsize'])
    ax = axes[0, 0]

    for mem_key,member in members.items():
        mem_dict = member[nl.main_var_name].mem_dict

        #format member
        if mem_key == nl.obs_key:
            linestyle = '-'
            color = 'black'
        else:
            res = mem_dict['res']
            linestyle = nl.nlp['linestyles'][res_lists[mem_dict['mod']].index(res)]
            # either take predefined color or take it from nlp
            if 'color' in mem_dict:
                color = mem_dict['color']
            else:
                color = nl.nlp['colors'][nl.nlp['mod_col_inds'].index(mem_dict['mod'])]

        #print(member[nl.main_var_name].var.time.values.shape)
        #print(member[nl.main_var_name].var.alt.values.shape)
        #print(member[nl.main_var_name].var.values.shape)
        #member[nl.main_var_name].var.T.plot.contourf()
        #handle, = ax.contourf(member[nl.main_var_name].var.time.values,
        #                 member[nl.main_var_name].var.alt.values,
        #                 member[nl.main_var_name].var.values.T)
                         #label=mem_dict['label'],
                         #linewidth=nl.nlp['mod_linewidth'],
                         #color=color, linestyle=linestyle)
        ## LWUTOA
        handle = plot_line(ax, 'LWUTOA', member,
                        mem_dict, '-', 'black')

        ## QV
        handle = plot_line(ax, nl.main_var_name, member,
                        mem_dict, '-', 'red')

        ## INVHGT
        handle = plot_line(ax, 'INVHGT', member,
                        mem_dict, '-', 'green')

        ## ALBEDO
        handle = plot_line(ax, 'ALBEDO', member,
                        mem_dict, '-', 'orange')


        PO.handles.append(handle)

    ## manually setting of ticks
    #ax.set_ylim(ylim)
    ## for > 0 fields, set xmin to 0
    #if nl.xlims is None:
    #    if nl.min_zero:
    #        ax.set_xlim(xmin=0.)
    #else:
    #    ax.set_xlim(nl.xlims)

    PO.set_axes_labels(ax, 'COORD_DATETIME', nl.main_var_name)
    ax.grid()
    # draw horizontal line at y = 0 if it is part of the y domain
    if ax.get_ylim()[0] < 0 and ax.get_ylim()[1] > 0:
        ax.axhline(color='grey')
    ax.legend(handles=PO.handles)
    fig.subplots_adjust(**nl.nlp['arg_subplots_adjust'])

    ##PO.add_panel_labels(order='cols')
    ## manually add the desired panel label
    #pan_lab_x = ax.get_xlim()[0] - (
    #                ax.get_xlim()[1] - ax.get_xlim()[0]) * \
    #                nl.nlp['panel_label_x_left_shift'] 
    #pan_lab_y = ax.get_ylim()[0] + (
    #                ax.get_ylim()[1] - ax.get_ylim()[0]) * \
    #                nl.nlp['panel_label_y_pos'] 
    #ax.text(pan_lab_x, pan_lab_y,
    #        nl.panel_label, fontsize=30, weight='bold')

    PO.finalize_plot()

def compute_regression(members):
    predictors = ['TQV']
    predictors = ['TQV', 'TQI']
    predictors = ['TQV', 'TQI', 'ALBEDO']
    npred = len(predictors)

    y_mean = np.zeros(len(members))
    X_mean = np.zeros((len(members),npred))

    colors = []
    sizes = []
    mi = 0
    for mem_key,member in members.items():
        #mem_dict = member[nl.main_var_name].mem_dict
        print(mem_key)

        # set response variable
        y_mean[mi] = member['LWUTOA'].var.values.mean()

        # set predictor variables
        for vi,var_name in enumerate(predictors):
            vals = member[var_name].var.values
            X_mean[mi,vi] = vals.mean()

        # get model color
        mod_key = member['LWUTOA'].mem_dict['mod']
        if mem_key not in ['ERA5_31', 'OBS']:
            color = nl.nlp['colors'][nl.nlp['mod_col_inds'].index(mod_key)]
            size  = 50
        elif mem_key == 'ERA5_31':
            color = 'brown'
            size  = 200
        elif mem_key == 'OBS':
            color = 'black'
            size  = 200
        colors.append(color)
        sizes.append(size)

        mi += 1

    print('###########################################')

    #print(X_mean)
    #print(y_mean)
    #quit()

    # predictors alone
    for vi,var_name in enumerate(predictors):
        reg = LinearRegression().fit(np.expand_dims(X_mean[:,vi],axis=1),y_mean)
        r2 = reg.score(np.expand_dims(X_mean[:,vi],axis=1),y_mean)
        print('R2 {}: {}'.format(var_name, r2))


    # all predictors together
    reg = LinearRegression().fit(X_mean,y_mean)
    r2 = reg.score(X_mean,y_mean)
    print('R2 {}: {}'.format('global', r2))
    print('coefficients: {}'.format(reg.coef_))


    name_dict = {'':'olr_bias'}
    PO = PlotOrganizer(i_save_fig=nl.i_save_fig,
                      path=os.path.join(nl.plot_base_dir),
                      name_dict=name_dict, nlp=nl.nlp, geo_plot=False)
    fig,axes = PO.initialize_plot(nrows=nl.nlp['nrows'],
                                  ncols=nl.nlp['ncols'],
                                  figsize=nl.nlp['figsize'])
    ## model
    ################################
    ax = axes[0,0]
    ax.grid()
    ax.scatter(reg.predict(X_mean), y_mean, color=colors,
                s=sizes)
    ax.set_xlabel('predicted {}'.format(nlv['LWUTOA']['label']))
    ax.set_ylabel('{} [{}]'.format(nlv['LWUTOA']['label'],
                                       nlv['LWUTOA']['units']))
    ## predictor 0
    ################################
    i = 0
    ax = axes[1,0]
    ax.grid()
    ax.scatter(X_mean[:,i], y_mean, color=colors, s=sizes)
    ax.set_xlabel('{} [{}]'.format(nlv[predictors[i]]['label'],
                                nlv[predictors[i]]['units']))
    ax.set_ylabel('{} [{}]'.format(nlv['LWUTOA']['label'],
                                       nlv['LWUTOA']['units']))
    ax.text(nl.nlp['textx'], nl.nlp['texty'],
            '{:3.1f} Wm-2 per kgm-2'.format(reg.coef_[i]),
        ha='center', va='center', transform=ax.transAxes)
    ## predictor 1
    ################################
    i = 1
    ax = axes[0,1]
    ax.grid()
    ax.scatter(X_mean[:,i], y_mean, color=colors, s=sizes)
    ax.set_xlim(0,0.002)
    ax.set_xlabel('{} [{}]'.format(nlv[predictors[i]]['label'],
                                nlv[predictors[i]]['units']))
    ax.set_ylabel('{} [{}]'.format(nlv['LWUTOA']['label'],
                                       nlv['LWUTOA']['units']))
    ax.text(nl.nlp['textx'], nl.nlp['texty'],
            '{:3.1f} Wm-2 per gm-2'.format(reg.coef_[i]/1000),
        ha='center', va='center', transform=ax.transAxes)

    ## predictor 2
    ################################
    i = 2
    ax = axes[1,1]
    ax.grid()
    ax.scatter(X_mean[:,i], y_mean, color=colors, s=sizes)
    ax.set_xlabel('{} [{}]'.format(nlv[predictors[i]]['label'],
                                nlv[predictors[i]]['units']))
    ax.set_ylabel('{} [{}]'.format(nlv['LWUTOA']['label'],
                                       nlv['LWUTOA']['units']))
    ax.text(nl.nlp['textx'], nl.nlp['texty'],
            '{:3.1f} Wm-2 per %'.format(reg.coef_[i]/100),
        ha='center', va='center', transform=ax.transAxes)

    fig.subplots_adjust(**nl.nlp['arg_subplots_adjust'])
    PO.finalize_plot()
    #plt.show()
    #quit()


def compute_vars(date, members):
    print(date)
    ######## LOAD MEMBERS
    ##########################################################################
    for mem_key,mem_dict in nl.sim_src_dict.items():
        for var_name in nl.var_names:
            if mem_key == 'OBS':
                mem_dict = nl.mem_src['obs'][nl.var_obs_mapping[var_name]]
            var = load_member_var(var_name, date, date, mem_dict,
                                nl.var_src_dict,
                                nl.var_src_dict[var_name]['load'],
                                domain=nl.cfg['domain'], i_debug=nl.i_debug)
            if var is not None:

                # aggregate
                var = var.mean(dim=['lon','lat','time'])
                var = var.expand_dims({'time':[date]})

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
        #print(members['COSMO_12']['LWUTOA'].var.mean().values)
        #print(members['OBS']['LWUTOA'].var.mean().values)
        #quit()
        timer.stop('compute')
        # save precomputed data
        Path(nl.pickle_dir).mkdir(exist_ok=True, parents=True)
        for mem_key,member in members.items():
            print(mem_key)
            print(member['LWUTOA'].var.mean().values)
            save_member_data_to_pickle(nl.pickle_dir, member,
                            nl.cfg['domain'], nl.var_names,
                            nl.time_periods)

    # ... or be reloaded from precomputed pickle files.
    else:
        # load precomputed data
        members = {}
        iter_mem_keys = list(nl.sim_src_dict.keys())
        #if nl.i_use_obs: iter_mem_keys.append('OBS')
        for mem_key in iter_mem_keys:
            if mem_key == 'OBS':
                members[mem_key] = {}
                for var_name in nl.var_names:
                    mem_dict = nl.mem_src['obs'][nl.var_obs_mapping[var_name]]
                    obs = load_member_data_from_pickle(nl.pickle_dir,
                                    mem_dict, nl.cfg['domain'], var_name,
                                    nl.time_periods, nl.i_skip_missing)
                    #print(obs[var_name].var.mean().values)
                    members[mem_key][var_name] = obs[var_name]
            else:
                mem_dict = nl.sim_src_dict[mem_key] 
                members[mem_key] = load_member_data_from_pickle(nl.pickle_dir,
                                mem_dict, nl.cfg['domain'], nl.var_names,
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
    # PART OF ANALYSIS FOR ENTIRE TIME SERIES
    timer.start('all')
    if nl.i_aggreg_days:
        for mem_key,member in members.items():
            for var_name in member.keys():
                member[nl.main_var_name].var = member[var_name].var.mean(dim='time')
    timer.stop('all')

    ###########################################################################
    # PLOTTING
    if nl.i_plot:
        timer.start('plot')
        draw_plot(members)
        timer.stop('plot')

    ###########################################################################
    # REGRESSION
    if nl.i_regression:
        timer.start('regression')
        compute_regression(members)
        timer.stop('regression')

    timer.print_report()
