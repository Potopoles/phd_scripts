#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Plot cross-sections of certain quantities
dependencies    depends on:
author			Christoph Heim
date created    29.01.2021
date changed    13.04.2021
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
import nl_04 as nl
from package.nl_variables import nlv,dimx,dimy,dimz,dimt
from package.utilities import (Timer, dt64_to_dt, subsel_domain,
                                select_common_timesteps)
from package.plot_functions import (PlotOrganizer, draw_map)
from package.mp import TimeStepMP
from package.member import Member
from package.functions import (load_member_var, save_member_data_to_pickle,
                               load_member_data_from_pickle,
                               time_periods_to_dates)
from package.var_pp import var_mapping, compute_variable
from package.comparison import Comparison
###############################################################################

def draw_plot(domains, dates):
    #print(dates)
    #quit()
    for date in dates:
        print(date)
        for mem_ind,mem_key in enumerate(nl.mem_subsel):
            for time_ind,hour in enumerate(nl.plot_hours):
                name_dict = {'':'cs'}
                name_dict['mem'] = mem_key.replace('.','')
                name_dict['date'] = '{:%Y%m%d}_{}'.format(date, time_ind)
                PO = PlotOrganizer(i_save_fig=nl.i_save_fig,
                                  path=os.path.join(nl.plot_base_dir),
                                  name_dict=name_dict, nlp=nl.nlp, geo_plot=False)
                fig,axes = PO.initialize_plot(nrows=nl.nlp['nrows'],
                                              ncols=nl.nlp['ncols'],
                                              figsize=nl.nlp['figsize'])


                #PO.handles = []
                #mem_ind = 0
                for col_ind,domain in enumerate(nl.domains):
                    member = domains[domain['code']][mem_key]
                    ax = axes[0, col_ind]

                    #comparison = Comparison(nl.var_names_3d_fc[0], members)   
                    #comparison.calc_statistics(centred0=True)
                    #factor = 1
                    #vmin = comparison.stats['min']*factor
                    #vmax = comparison.stats['max']*factor
                    #print(member)
                    #quit()

                    ## clear axis if no member available
                    #if len(members)-1 < mem_ind:
                    #    axes[row_ind,col_ind].remove()
                    #    continue

                    ## get member
                    #mem_key = list(members.keys())[mem_ind]
                    #print(mem_key)

                    ### vertical velocity
                    var_name = nl.var_names_3d_fc[0]
                    mem_dict = member[var_name].mem_dict
                    try:
                        plot_var = member[var_name].var.loc[
                                    {'time':'{:%Y-%m-%d}'.format(date)}]
                    except KeyError:
                        continue
                    try:
                        plot_var = plot_var.isel(time=time_ind)
                    except IndexError:
                        continue
                    plot_var *= 100
                    plot_var = plot_var.where(plot_var >= np.min(nl.nlp['cfw_levels']),
                                                    0.99*np.min(nl.nlp['cfw_levels']))
                    plot_var = plot_var.where(plot_var <= np.max(nl.nlp['cfw_levels']),
                                                    0.99*np.max(nl.nlp['cfw_levels']))
                    CFW = ax.contourf(plot_var.lon.values,
                                plot_var.alt.values,
                                plot_var.values,
                                cmap=nl.nlp['cfw_cmap'],
                                levels=nl.nlp['cfw_levels'])
                                #vmin=vmin, vmax=vmax)

                    ### cloud field contour
                    var_name = nl.var_names_3d_lc[0]
                    plot_var = member[var_name].var.loc[{'time':'{:%Y-%m-%d}'.format(date)}]
                    try:
                        plot_var = plot_var.isel(time=time_ind)
                    except IndexError:
                        continue
                    plot_var *= 1000
                    plot_var = plot_var.where(plot_var <= np.max(nl.nlp['cfqc_levels']),
                                                    0.99*np.max(nl.nlp['cfqc_levels']))
                    CFQC = ax.contourf( plot_var.lon.values,
                                plot_var.alt.values,
                                plot_var.values, cmap=nl.nlp['cfqc_cmap'],
                                levels=nl.nlp['cfqc_levels'])
                                #norm=mcolors.LogNorm())

                    ### specific height lines
                    for vi,var_name in enumerate(nl.var_names_2d):
                        print(var_name)
                        plot_var = member[var_name].var.loc[{'time':'{:%Y-%m-%d}'.format(date)}]
                        try:
                            plot_var = plot_var.isel(time=time_ind)
                        except IndexError:
                            continue
                        if var_name == 'LCL' and mem_key == 'FV3_3.25':
                            print('skip LCL for FV3 cause technical issue.')
                            continue
                        handle, = ax.plot(plot_var.lon.values,
                                         plot_var.values,
                                         label='test',
                                         linewidth=nl.nlp['linewidths'][vi],
                                         color=nl.nlp['colors'][vi],
                                         linestyle=nl.nlp['linestyles'][vi])
                        PO.handles.append(handle)

                    ax.set_ylim(nl.alt_lims)
                    ax.set_xlim((domain['lon'].start,
                                domain['lon'].stop))
                    ax.set_xlabel('longitude')

                    if col_ind == 0:
                        ax.set_title('CS2', x=0.10)
                        ax.set_ylabel(r'height [$m$]')
                        # manually add the desired panel label
                        pan_lab_x = ax.get_xlim()[0] - (
                                        ax.get_xlim()[1] - ax.get_xlim()[0]) * \
                                        nl.nlp['panel_label_x_left_shift'] 
                        pan_lab_y = ax.get_ylim()[0] + (
                                        ax.get_ylim()[1] - ax.get_ylim()[0]) * \
                                        nl.nlp['panel_label_y_pos'] 
                        ax.text(pan_lab_x, pan_lab_y,
                                nl.nlp['panel_labels'][mem_ind],
                                fontsize=nl.nlp['panel_label_size'], weight='bold')
                    elif col_ind == 1:
                        ax.set_title('CS1', x=0.9)
                        ax.get_yaxis().set_visible(False)
                    #ax.legend(handles=PO.handles)
                    ## manually setting of ticks
                    #ax.set_ylim(nl.nlp['ylim'][nl.main_var_name][vol_key])

                    #mem_ind += 1
                    #col_ind += 1
                    #if col_ind == nl.nlp['ncols']:
                    #    col_ind = 0
                    #    row_ind += 1

                if mem_key == nl.nlp['cfw_colorbar']:
                    mappable = CFW
                    levels = nl.nlp['cfw_levels']
                    ticks = nl.nlp['cfw_cb_ticks']
                    var_name = nl.var_names_3d_fc[0]
                    unit = '$cm$ $s^{-1}$'
                    plot_colorbar = True
                elif mem_key == nl.nlp['cfqc_colorbar']:
                    mappable = CFQC
                    levels = nl.nlp['cfqc_levels']
                    ticks = nl.nlp['cfqc_cb_ticks']
                    var_name = nl.var_names_3d_lc[0]
                    unit = '$g$ $kg^{-1}$'
                    plot_colorbar = True
                else:
                    plot_colorbar = False
                if plot_colorbar:
                    cax = fig.add_axes(nl.nlp['colorbar_pos'])
                    #ticks = np.linspace(levels[0], levels[-1], np.ceil(len(levels)/2))
                    cbar = plt.colorbar(mappable=mappable, cax=cax, 
                                            orientation='horizontal',
                                            ticks=ticks)
                    cbar.ax.set_xticklabels(ticks)
                    unit = '' if unit == '' else '[{}]'.format(unit)
                    cax.set_xlabel('{} {}'.format(nlv[var_name]['label'], unit))


                fig.subplots_adjust(**nl.nlp['arg_subplots_adjust'])
                #fig.suptitle('{:%Y%m%d} {}'.format(date, hour))
                fig.suptitle('{}'.format(nl.sim_src_dict[mem_key]['label']),
                            x=0.55)


                #PO.add_panel_labels(order='cols')

                PO.finalize_plot()

            #quit()



def compute_vars(date, members, domain):

    ######## LOAD OBSERVATIONS
    ##########################################################################
    if nl.i_use_obs:
        raise NotImplementedError()
        #for var_name in nl.var_names:
        #    obs_key = nl.var_obs_mapping[var_name]
        #    obs_dict = nl.obs_src_dict[obs_key]

        #    var = load_member_var(var_name, date, date, obs_dict,
        #                        nl.var_src_dict,
        #                        nl.var_src_dict[var_name]['load'],
        #                        domain=nl.cfg['domain'], i_debug=nl.i_debug)
        #    if nl.cfg['domain'] is not None:
        #        var = subsel_domain(var, nl.cfg['domain'])

        #    if var is not None:
        #        var = var.mean(dim=['lon', 'lat', 'time'])

        #        member = Member(var, obs_dict, comparison=None)
        #        if 'OBS' not in members.keys():
        #            members['OBS'] = {}
        #        try:
        #            members['OBS'][var_name] = member
        #        except TypeError:
        #            pass
        #    else:
        #        members['OBS'] = None


    ######## LOAD MODELS
    ##########################################################################
    for mem_key,mem_dict in nl.sim_src_dict.items():
        for var_name in nl.var_names:
            var = load_member_var(var_name, date, date, mem_dict,
                                nl.var_src_dict,
                                nl.var_src_dict[var_name]['load'],
                                domain=domain, i_debug=nl.i_debug)
            if var is not None:
                var = var.sel(lat=domain['lat'].start, method='nearest')

                # subsel altitude slice for 3d vars
                if 'z' in nlv[var_name]['dims']:
                    var = var.sel(alt=slice(0,5000))

                # create member instance
                member = Member(var, mem_dict, comparison=None)

                if mem_key not in members.keys():
                    members[mem_key] = {}
                if members[mem_key] is not None:
                    members[mem_key][var_name] = member
            else:
                members[mem_key] = None
    return(members)







def run_for_date(ts, domain):
    """
    Organize full analysis for a given date (ts).
    ts has to be called ts because run_for_date is called from TimeStepMP.
    """
    timer = Timer(mode='seconds')
    members = {}
    
    # compute variables
    timer.start('vars')
    members = compute_vars(ts, members, domain)
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
        for domain in nl.domains:
            timer.start('compute')
            fargs = {'domain':domain}
            tsmp.run(run_for_date, fargs=fargs, step_args=None)
            tsmp.concat_timesteps()
            members = tsmp.concat_output['members']
            timer.stop('compute')
            # save precomputed data
            Path(nl.pickle_dir).mkdir(exist_ok=True, parents=True)
            for mem_key,member in members.items():
                save_member_data_to_pickle(nl.pickle_dir, member,
                                domain, list(member.keys()),
                                nl.time_periods)

    # ... or be reloaded from precomputed pickle files.
    else:
        # load precomputed data
        domains = {}
        for domain in nl.domains:
            members = {}
            iter_mem_keys = list(nl.sim_src_dict.keys())
            for mem_key in iter_mem_keys:
                mem_dict = nl.sim_src_dict[mem_key] 
                members[mem_key] = load_member_data_from_pickle(nl.pickle_dir,
                                mem_dict, domain, nl.var_names,
                                nl.time_periods, nl.i_skip_missing)
            domains[domain['code']] = members


    ###########################################################################
    # PLOTTING
    if nl.i_plot:
        timer.start('plot')
        draw_plot(domains, dates)
        timer.stop('plot')

    timer.print_report()
