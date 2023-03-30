#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Correlate OSW/OLR fluxes with various variables
                Does computation on remapped fields since for domain average
                values this does not matter and is much faster.
dependencies    depends on:
                    - 004_01 for remapped fields
author			Christoph Heim
date created    25.11.2019
date changed    11.03.2021
usage           args:
                1st:    number of parallel tasks
                2nd:    i_save_fig (0: show, 1: png, 2: pdf, 3: jpg)
"""
###############################################################################
import os, glob, collections
import numpy as np
import xarray as xr
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.colors as mcolors
from pathlib import Path
from datetime import datetime, timedelta
from scipy.stats import linregress, skew
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import nl_03 as nl
from package.nl_variables import nlv,dimx,dimy,dimz,dimt
from package.utilities import (Timer, dt64_to_dt, subsel_domain,
                                select_common_timesteps)
from package.plot_functions import (PlotOrganizer, draw_map)
from package.mp import TimeStepMP
from package.member import Member
from package.functions import (load_member_var, save_member_data_to_pickle,
                               load_member_data_from_pickle,
                               time_periods_to_dates)
from package.var_pp import var_mapping, compute_variable, DERIVE, DIRECT
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

    # lists of all used resolutions in each model
    # used to select marker types
    res_lists = {}
    del_mems = []
    for mem_key,member in members.items():
        if mem_key == 'OBS': continue
        try:
            mem_dict = member[nl.var_names[0]].mem_dict
        except KeyError:
            del_mems.append(mem_key)
            continue
        if mem_dict['mod'] not in res_lists:
            res_lists[mem_dict['mod']] = [mem_dict['res']]
        else:
            res_lists[mem_dict['mod']].append(mem_dict['res'])
    for mem_key,res_list in res_lists.items():
        res_list.sort()

    for mem_key in del_mems:
        del members[mem_key]

    name_dict = {'':'corr'}
    name_dict['dom'] = nl.cfg['domain']['code']
    name_dict['sim'] = nl.sim_group
    name_dict['agg'] = nl.i_aggreg
    name_dict[nl.var_names[0]] = nl.var_names[1]

    PO = PlotOrganizer(i_save_fig=nl.i_save_fig,
                      path=os.path.join(nl.plot_base_dir,
                                        nl.cfg['domain']['code']),
                      name_dict=name_dict, nlp=nl.nlp, geo_plot=False)
    fig,axes = PO.initialize_plot(nrows=nl.nlp['nrows'],
                                  ncols=nl.nlp['ncols'],
                                  figsize=nl.nlp['figsize'])
    #print(PO.path)
    #quit()

    ax = axes[0, 0]

    all_xmean = []
    all_ymean = []
    corr_mean = []
    xmax = -9999.; xmin = 9999.
    ymax = -9999.; ymin = 9999.
    #for skey,mem in members.items():
    for mem_key in nl.nlp['plot_order']:
        print(mem_key)
        if mem_key not in members.keys():
            continue
        member = members[mem_key]
        # configure plot objects
        if mem_key == 'OBS': 
            color = nl.nlp['OBS_color']
            fill_style = color
            marker=nl.nlp['markers_aggreg'][nl.i_aggreg][1]
            # add opacity
            alpha = 1.0
            color = mcolors.to_rgb(color) + (alpha,)
        elif mem_key == 'ERA5_31': 
            color = nl.nlp['OBS_color']
            fill_style = color
            marker=nl.nlp['markers_aggreg'][nl.i_aggreg][0]
            # add opacity
            alpha = 1.0
            color = mcolors.to_rgb(color) + (alpha,)
        else:
            mod_key = nl.sim_src_dict[mem_key]['mod']
            res = nl.sim_src_dict[mem_key]['res']
            if mem_key in nl.nlp['plt_mem_cfg']:
                color = nl.nlp['plt_mem_cfg'][mem_key]['col']
            else:
                if nl.nlp['unique_colors']:
                    ## Make all of them grey
                    #if mem_key in ['NICAM_3.5', 'UM_5', 'COSMO_2.2', 'SAM_4',
                    #               'IFS_4', 'FV3_3.25', 'ICON_2.5',
                    #               'ARPEGE-NH_2.5', 'GEOS_3']:
                    #    color = 'grey'
                    #else:
                    mem_ind = list(members.keys()).index(mem_key)/(len(members.keys())-1)
                    #mem_ind = (list(members.keys()).index(mem_key)-9)/(
                    #            (len(members.keys())-1)-9)
                    color = matplotlib.cm.get_cmap('Spectral')(mem_ind)
                else:
                    color = nl.nlp['colors'][nl.nlp['mod_col_inds'].index(mod_key)]
            # for model members with shallow convection scheme, take specific marker
            if ( (mem_key in nl.convpar_dict) and 
                    (nl.convpar_dict[mem_key] > 0) ):
                fill_style = 'none'
                #fill_style = color
            else:
                fill_style = color
            marker_int = 0
            if mem_key in nl.marker_dict:
                marker_int = nl.marker_dict[mem_key]
            marker=nl.nlp['markers_aggreg'][nl.i_aggreg][marker_int]
            # add opacity
            if (res <= 5) and (res >= 2):
                alpha = 1.0
            else:
                alpha = nl.nlp['alpha_secondary_models']
            color = mcolors.to_rgb(color) + (alpha,)

        ## GET DISAGGREGATED VARIABLE VALUES
        xvals = members[mem_key][nl.var_names[0]].var

        try:
            xvals = members[mem_key][nl.var_names[0]].var
            yvals = members[mem_key][nl.var_names[1]].var
        except KeyError:
            if nl.i_use_obs and (len(members['OBS']) == 0):
                print('nl.i_use_obs=1 but no OBS available')
            else:
                print('Problem with member or fields')
            quit()

        # filter out time steps with missing values for both variables
        xvals, yvals = select_common_timesteps(xvals, yvals)
        ## remove initialization period if full aggregation
        #if nl.i_aggreg == 'all':
        #    xvals = xvals.sel(time=slice(
        #            '{:%Y-%m-%d}'.format(nl.init_period_until+timedelta(days=1)),
        #            '{:%Y-%m-%d}'.format(dt64_to_dt(xvals.time.values[-1]))))
        #    yvals = yvals.sel(time=slice(
        #            '{:%Y-%m-%d}'.format(nl.init_period_until+timedelta(days=1)),
        #            '{:%Y-%m-%d}'.format(dt64_to_dt(yvals.time.values[-1]))))

        ## COMPUTE PERCENTILES AND AGGREGATE TIME
        if nl.i_aggreg == 'all':
            xmean = xvals.mean()
            ymean = yvals.mean()
            xperc = np.percentile(xvals, nl.perc)
            yperc = np.percentile(yvals, nl.perc)
        elif nl.i_aggreg == 'yearly':
            xmean = xvals.resample({'time':'1Y'}).mean()
            ymean = yvals.resample({'time':'1Y'}).mean()
        elif nl.i_aggreg == 'monthly':
            xmean = xvals.resample({'time':'1MS'}).mean()
            ymean = yvals.resample({'time':'1MS'}).mean()
        elif nl.i_aggreg == 'none':
            xmean = xvals
            ymean = yvals
        else: raise NotImplementedError()

        # compute and print correlation if possible
        corr_vals = np.corrcoef(xvals.values[~np.isnan(xvals.values)],
                           yvals.values[~np.isnan(yvals.values)])[0,1]
        # compute and print correlation if possible
        corr_mean = np.corrcoef(xmean.values[~np.isnan(xmean.values)],
                           ymean.values[~np.isnan(ymean.values)])[0,1]

        # print disaggregated corr. coef
        try:
            len(xvals.values)
            print('{} cor disagg.: {}'.format(mem_key, corr_vals))
        except TypeError:
            print('no corr for size 1 obj.')
        # print aggregated corr. coef
        try:
            len(xmean.values)
            print('{} cor agg.: {}'.format(mem_key, corr_mean))
        except TypeError:
            print('no corr for size 1 obj.')

        ## collect statistic of normal models to get an aggregated view later
        #if mem_key != 'OBS':
        #    corr_mean.append(corr)
        #    all_xmean.append(xmean)
        #    all_ymean.append(ymean)

        # set up member label
        if mem_key == 'OBS':
            label = '{}'.format('OBS')
        else:
            label = '{}'.format(
                nl.sim_src_dict[mem_key]['label'])

        ## add scatterplot of this member
        if nl.i_aggreg == 'none':
            ## find out which values are initial period.
            #is_init_period = [dt64_to_dt(dt) <= nl.init_period_until for \
            #                dt in members[mem_key][nl.var_names[0]].var.time.values]
            #n_init_period = np.sum(is_init_period)
            #print(np.sum(is_init_period))
            #handle = ax.scatter(xmean[:n_init_period], ymean[:n_init_period],
            #        label=label,
            #        s=nl.nlp['marker_size_aggreg'][nl.i_aggreg]*4,
            #        linewidths=nl.nlp['marker_linewidths_aggreg'][nl.i_aggreg],
            #        marker='*', alpha=alpha,
            #        color=color, facecolor=fill_style)
            #handle = ax.scatter(xmean[n_init_period:], ymean[n_init_period:],
            #        label=label,
            #        s=nl.nlp['marker_size_aggreg'][nl.i_aggreg],
            #        linewidths=nl.nlp['marker_linewidths_aggreg'][nl.i_aggreg],
            #        marker=marker, alpha=alpha,
            #        color=color, facecolor=fill_style)
            handle = ax.scatter(xmean[:], ymean[:],
                    label=label,
                    s=nl.nlp['marker_size_aggreg'][nl.i_aggreg],
                    linewidths=nl.nlp['marker_linewidths_aggreg'][nl.i_aggreg],
                    marker=marker, alpha=alpha,
                    color=color, facecolor=fill_style)
        else:
            handle = ax.scatter(xmean, ymean, label=label,
                    s=nl.nlp['marker_size_aggreg'][nl.i_aggreg],
                    linewidths=nl.nlp['marker_linewidths_aggreg'][nl.i_aggreg],
                    marker=marker, alpha=alpha,
                    color=color, facecolor=fill_style)
        PO.handles.append(handle)

        # gather max and min
        xmax = max(xmax, np.nanmax(xmean))
        xmin = min(xmin, np.nanmin(xmean))
        ymax = max(ymax, np.nanmax(ymean))
        ymin = min(ymin, np.nanmin(ymean))

        # draw percentile lines
        if nl.i_aggreg in ['all']:
            if nl.i_aggreg in ['all']:
                line = mlines.Line2D([xperc[0], xperc[1]], [ymean, ymean],
                                    color=color,
                                    linewidth=nl.nlp['percentile_linewidth'])
                ax.add_line(line)
                line = mlines.Line2D([xmean, xmean], [yperc[0], yperc[1]],
                                    color=color, alpha=alpha,
                                    linewidth=nl.nlp['percentile_linewidth'])
                ax.add_line(line)
                xmax = max(xmax, xperc[1])
                xmin = min(xmin, xperc[0])
                ymax = max(ymax, yperc[1])
                ymin = min(ymin, yperc[0])

        # draw regression line
        elif nl.i_aggreg in ['none', 'monthly', 'yearly']:
            if nl.i_aggreg in ['none']:
                # make regression line and plot if sloe significantly != zero
                slope,intercept,r_val,p_val,std_err = linregress(xvals.squeeze(),
                                                                 yvals.squeeze())
            elif nl.i_aggreg in ['monthly', 'yearly']:
                slope,intercept,r_val,p_val,std_err = linregress(xmean, ymean)
            if p_val < 0.05:
                ax.plot(xvals, slope*xvals + intercept, color=color,
                        linewidth=nl.nlp['regression_linewidth'])

        # app value labels
        if nl.i_aggreg in ['yearly']:
            years = [dt64_to_dt(ts).year for ts in xmean.time]
            for i,year in enumerate(years):
                if xmean[i] >= 0.5 * (xmax + xmin):
                    offset_x = -30
                else:
                    offset_x =  10
                if ymean[i] >= 0.5 * (ymax + ymin):
                    offset_y = -17
                else:
                    offset_y =  10
                ax.annotate(year, (xmean[i],ymean[i]),
                            textcoords="offset points",
                            xytext=(offset_x,offset_y),
                            fontsize=10)

    # if specific axis limit is specified:
    if nl.i_aggreg == 'all':
        if nl.var_names[0] in nl.nlp['axis_max_agg_all']:
            xmax = nl.nlp['axis_max_agg_all'][nl.var_names[0]]
        if nl.var_names[1] in nl.nlp['axis_max_agg_all']:
            ymax = nl.nlp['axis_max_agg_all'][nl.var_names[1]]

    PO.set_axes_labels(ax, nl.var_names[0], nl.var_names[1])
    ax.set_axisbelow(True)
    ax.grid(linewidth=0.3)
    fig.subplots_adjust(**nl.nlp['arg_subplots_adjust'])

    plt.locator_params(axis='x', nbins=5)

    # set axis limits
    ax.set_xlim((xmin, xmax))
    ax.set_ylim((ymin, ymax))

    vars_key = str([nl.var_names[0], nl.var_names[1]])

    # set title (if not hidden in nlp)
    if ( (vars_key not in nl.nlp['title_hidden']) and
         (nl.i_aggreg not in nl.nlp['title_hidden']) ):
        if nl.i_aggreg == 'none':
            ax.set_title('daily means')
        elif nl.i_aggreg == 'all':
            ax.set_title('35-day mean')
        else:
            raise NotImplementedError()

    # set legend (if not hidden in nlp)
    # draw legend only if it is not set to be hidden for the given
    # variable combination
    if ( (vars_key not in nl.nlp['legend_hidden']) and
         (nl.i_aggreg not in nl.nlp['legend_hidden']) ):
        ax.legend(handles=PO.handles, bbox_to_anchor=(1.01,1.18),
                    fontsize=nl.nlp['legend_fontsize'],
                    markerscale=nl.nlp['legend_markerscale'])

    
    #PO.add_panel_labels(order='cols')
    # manually add the desired panel label
    pan_lab_x = ax.get_xlim()[0] - (
                    ax.get_xlim()[1] - ax.get_xlim()[0]) * \
                    nl.nlp['panel_label_x_left_shift'] 
    pan_lab_y = ax.get_ylim()[0] + (
                    ax.get_ylim()[1] - ax.get_ylim()[0]) * \
                    nl.nlp['panel_label_y_pos'] 
    ax.text(pan_lab_x, pan_lab_y,
            nl.panel_label, fontsize=nl.nlp['panel_label_size'],
            weight='bold')

    PO.finalize_plot()



def compute_vars(date, members):

    ######## LOAD OBSERVATIONS
    ##########################################################################
    if nl.i_use_obs:
        for var_name in nl.var_names:
            obs_key = nl.var_obs_mapping[var_name]
            obs_dict = nl.obs_src_dict[obs_key]
            print(var_name)

            var = load_member_var(var_name, date, date, obs_dict,
                                nl.var_src_dict,
                                nl.var_src_dict[var_name]['load'],
                                domain=nl.cfg['domain'], i_debug=nl.i_debug)

            if nl.cfg['domain'] is not None:
                var = subsel_domain(var, nl.cfg['domain'])

            if var is not None:
                var = var.mean(dim=['lon', 'lat', 'time'])

                member = Member(var, obs_dict, comparison=None)
                if 'OBS' not in members.keys():
                    members['OBS'] = {}
                try:
                    members['OBS'][var_name] = member
                except TypeError:
                    pass
            else:
                members['OBS'] = None


    ######## LOAD MODELS
    ##########################################################################
    for mem_key,mem_dict in nl.sim_src_dict.items():
        for var_name in nl.var_names:

            if nl.var_src_dict[var_name]['load'] in [DIRECT, DERIVE]:
                var = load_member_var(var_name, date, date, mem_dict,
                                    nl.var_src_dict,
                                    nl.var_src_dict[var_name]['load'],
                                    domain=nl.cfg['domain'], i_debug=nl.i_debug)

                if var is not None:
                    # subdomain
                    if nl.cfg['domain'] is not None:
                        var = subsel_domain(var, nl.cfg['domain'])

                    # remove alt dimension
                    if 'alt' in var.dims:
                        var = var.mean(dim='alt')

                    if 'rel_alt' in var.dims:
                        var = var.sel(rel_alt=slice(0.1,0.9))
                        var = var.mean(dim='rel_alt')

                    #print('{}_{}'.format(var_name, var.shape))
                    #print(var.lon)

                    # mean
                    if 'lat' in var.dims:
                        var = var.mean(dim=['lat'])
                    if 'lon' in var.dims:
                        var = var.mean(dim=['lon'])
                    var = var.mean(dim=['time'])
                    var = var.expand_dims({'time':[date]})
                    ## skewness
                    #skew_val = skew(var.values, axis=None,
                    #                nan_policy='omit')
                    #var = var.mean(dim=['lon', 'lat', 'time'])
                    #var.values = skew_val
                    ## standard deviation
                    #var = var.std(dim=['lon', 'lat', 'time'])
                    ## maximum
                    #var = var.max(dim=['lon', 'lat', 'time'])
                    #print('{}    {}'.format(tmp.values, var.values))
                    #print(var.values)

            elif nl.var_src_dict[var_name]['load'] in ['bin']:
                pickle_dir = os.path.join(nl.var_src_dict[var_name]['src'])
                var = load_member_data_from_pickle(pickle_dir,
                                mem_dict, nl.cfg['domain'], [var_name],
                                nl.time_periods, nl.i_skip_missing)
                if var_name in var:
                    var = var[var_name].var
                    var = var.sel(time=slice('{:%Y-%m-%d 03:00:00}'.format(date),
                                            '{:%Y-%m-%d 00:00:00}'.format(date+timedelta(days=1))))
                else: var = None


            if var is not None:
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
        timer.stop('compute')
        # save precomputed data
        Path(nl.pickle_dir).mkdir(exist_ok=True, parents=True)
        for mem_key,member in members.items():
            save_member_data_to_pickle(nl.pickle_dir, member,
                            nl.cfg['domain'], nl.var_names,
                            nl.time_periods)

    # ... or be reloaded from precomputed pickle files.
    else:
        # load precomputed data
        members = {}
        iter_mem_keys = list(nl.sim_src_dict.keys())
        if nl.i_use_obs: iter_mem_keys.append('OBS')
        for mem_key in iter_mem_keys:
            print(mem_key)
            if mem_key == 'OBS':
                all_mem_vars = {}
                for i in range(2):
                    mem_dict = nl.obs_src_dict[nl.var_obs_mapping[nl.var_names[i]]]
                    mem_var = load_member_data_from_pickle(nl.pickle_dir,
                                    mem_dict, nl.cfg['domain'], nl.var_names[i],
                                    nl.time_periods, nl.i_skip_missing)
                    all_mem_vars.update(mem_var)
                members[mem_key] = all_mem_vars
            else:
                mem_dict = nl.sim_src_dict[mem_key] 
                members[mem_key] = load_member_data_from_pickle(nl.pickle_dir,
                                mem_dict, nl.cfg['domain'], nl.var_names,
                                nl.time_periods, nl.i_skip_missing)
                if len(members[mem_key]) == 1:
                    del members[mem_key]
            

    ###########################################################################
    # PLOTTING
    if nl.i_plot:
        timer.start('plot')
        draw_plot(members)
        timer.stop('plot')

    timer.print_report()
