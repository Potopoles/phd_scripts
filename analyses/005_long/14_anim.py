#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Create fancy animation.
author			Christoph Heim
date created    29.07.2021
date changed    29.04.2022
usage           args: print help for args or check namelist
"""
###############################################################################
import os, glob, collections, copy
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime, timedelta
import nl_14 as nl
from package.nl_variables import nlv
from nl_var_src import ANA_NATIVE
from package.var_pp import var_mapping, compute_variable
from package.utilities import Timer, dt64_to_dt, subsel_domain
from package.time_processing import Time_Processing as TP
from package.plot_functions import PlotOrganizer, draw_map, draw_domain
from package.functions import time_periods_to_dates, load_member_var
from package.mp import TimeStepMP, IterMP
from package.member import Member
###############################################################################

def plot_var(ax, var_name, member):
    if nl.plot_type == 'contourf':
        mappable = member.vars[var_name].squeeze().\
                plot.contourf(ax=ax,
                cmap=nl.nlp['cmaps'][var_name],
                vmin=nl.var_cfgs[var_name]['min_max'][0],
                vmax=nl.var_cfgs[var_name]['min_max'][1],
                add_colorbar=False, add_labels=False,
                rasterized=True, linewidth=0, edgecolor='face',
                levels=100, antialiased=True)
    elif nl.plot_type == 'pcolormesh':
        mappable = member.vars[var_name].squeeze().\
                plot.pcolormesh(ax=ax,
                cmap=nl.nlp['cmaps'][var_name],
                vmin=nl.var_cfgs[var_name]['min_max'][0],
                vmax=nl.var_cfgs[var_name]['min_max'][1],
                add_colorbar=False, add_labels=False,
                rasterized=True, linewidth=0, edgecolor='face')

def draw_axis(ax, nl, member, mem_key, timer):
    draw_map(ax, nl.plot_domain, nl.nlp,
             add_xlabel=True, add_ylabel=True,
             dticks=nl.plot_domain['dticks'])

    mem_dict = copy.copy(member.mem_dict)
    timer.start('plot.const')

    dummy_var = member.vars[list(member.vars.keys())[0]]
    const = xr.open_dataset(
                os.path.join(nl.inp_base_dir, mem_dict['sim'], 
                            mem_dict['case'], mem_dict['dom_key'],
                           'const_{:4.3f}.nc'.format(
                            np.median(np.diff(dummy_var['lon'])))))
    const = const.drop(['lon', 'lat'])
    const = const.rename({'rlon':'lon', 'rlat':'lat'})
    #const = const.drop('rotated_pole')
    #const = const.mean(dim='time')
    const = subsel_domain(const, nl.plot_domain)
    const_fr_land = const.FR_LAND.load()
    const_for_e = const.FOR_E.load()
    const_for_d = const.FOR_D.load()
    const_alb_dif = const.ALB_DIF.load()
    const.close()
    const_fr_land = const_fr_land.mean(dim='time')
    const_for_e = const_for_e.mean(dim='time')
    const_for_d = const_for_d.mean(dim='time')
    const_alb_dif = const_alb_dif.mean(dim='time')
    timer.stop('plot.const')

    ## land mask
    grass_mask = const_fr_land.copy()
    grass_mask *= (1 - const_for_e.copy())
    grass_mask *= (1 - const_for_d.copy())
    #grass_mask.values[grass_mask.values > 0] = 1
    #grass_mask.values[grass_mask.values == 0] = np.nan
    grass_greenness = grass_mask * (1 - const_alb_dif.copy())
    #grass_greenness = grass_mask

    ## forest mask
    forest_mask = const_for_e + const_for_d
    #forest_mask.values[forest_mask.values > 0] = 1
    #forest_mask.values[forest_mask.values == 0] = np.nan
    forest_greenness = forest_mask * (1 - const_alb_dif)
    #forest_greenness = forest_mask

    timer.start('plot.wsoil')
    # if WSOIL is given, scale land albedos with soil moisture
    if 'WSOIL' in member.vars: 
        var_name = 'WSOIL'
        wsoil = member.vars[var_name]
        # this is necessary due to some weird reasons.....
        wsoil = wsoil.interp({'lon':forest_mask.lon})
        wsoil_grass = copy.copy(wsoil.sel(soil1 = nl.soil_levels_grass))
        wsoil_forest = copy.copy(wsoil.sel(soil1 = nl.soil_levels_forest))
        wsoil_grass = wsoil_grass.sum(dim='soil1')
        wsoil_forest = wsoil_forest.sum(dim='soil1')
        max_val = 0
        for lev in nl.soil_levels_grass:
            max_val += nl.saturation[lev]
        sat_soil_grass = wsoil_grass / max_val
        max_val = 0
        for lev in nl.soil_levels_forest:
            max_val += nl.saturation[lev]
        sat_soil_forest = wsoil_forest / max_val

        max_growth = 1.0
        plant_growth_grass = grass_mask * sat_soil_grass / nl.land_plant_max_growth_sat_soil
        plant_growth_grass.values[plant_growth_grass.values > max_growth] = max_growth
        plant_growth_forest = forest_mask * sat_soil_forest / nl.forest_plant_max_growth_sat_soil
        plant_growth_forest.values[plant_growth_forest.values > max_growth] = max_growth

        grass_greenness = grass_greenness * plant_growth_grass
        forest_greenness = forest_greenness * plant_growth_forest

        forest_greenness.values[
                    (forest_mask.values > 0.3) &
                    (forest_greenness.values < nl.min_forest_greenness)] = \
                                nl.min_forest_greenness

    land_greenness = grass_greenness + forest_greenness
    timer.stop('plot.wsoil')

    ##### DRAW PANELS
    #########################################################################
    timer.start('plot.draw')
    if nl.plot_type == 'contourf':
        land_greenness.squeeze().\
                plot.contourf(ax=ax,
                cmap=nl.nlp['cmaps']['land'],
                vmin=0.0, vmax=0.9,
                add_colorbar=False, add_labels=False,
                levels=10, antialiased=True)
    if nl.plot_type == 'pcolormesh':
        land_greenness.squeeze().\
                plot.pcolormesh(ax=ax,
                cmap=nl.nlp['cmaps']['land'],
                vmin=0.0, vmax=0.9,
                add_colorbar=False, add_labels=False)

    ## ocean mask
    ocean_mask = 1 - const.FR_LAND
    if nl.plot_type == 'contourf':
        ocean_mask.squeeze().\
                plot.contourf(ax=ax,
                cmap=nl.nlp['cmaps']['ocean'],
                add_colorbar=False, add_labels=False,
                levels=10, antialiased=True)
    if nl.plot_type == 'pcolormesh':
        ocean_mask.squeeze().\
                plot.pcolormesh(ax=ax,
                cmap=nl.nlp['cmaps']['ocean'],
                add_colorbar=False, add_labels=False)

    if nl.i_plot_vars:
        ## draw plot
        var_name = 'TQV'
        if var_name in member.vars:
            # only plot TQV over ocean
            ocean_mask = ocean_mask.isel(time=0)
            #print(ocean_mask)
            #print(member.vars[var_name])
            #quit()
            ocean_mask['lon'] = member.vars[var_name].lon
            ocean_mask['lat'] = member.vars[var_name].lat
            member.vars[var_name] = member.vars[var_name].where(ocean_mask, np.nan)
            plot_var(ax, var_name, member)

        # draw plot
        var_name = 'TQC'
        if var_name in member.vars:
            plot_var(ax, var_name, member)

        var_name = 'TQI'
        if var_name in member.vars:
            plot_var(ax, var_name, member)

        # draw plot
        var_name = 'PP'
        if var_name in member.vars:
            plot_var(ax, var_name, member)

        # draw plot
        var_name = 'QV2M'
        if var_name in member.vars:
            plot_var(ax, var_name, member)

    ## plot domain boundaries
    handles = []
    for dom_entry in nl.add_domain_boundaries:
        line = draw_domain(ax, dom_entry['dom'], nl.nlp, 
                        color=dom_entry['color'], 
                        linestyle=dom_entry['linestyle'],
                        linewidth=nl.nlp['lw'], zorder=1) 
        if 'hide_legend' in dom_entry['dom']:
            if not dom_entry['dom']['hide_legend']:
                handles.append(line)
        else:
            handles.append(line)
    if len(handles) > 0:
        ax.legend(handles=handles, loc='lower left')


    timer.stop('plot.draw')



def draw_plot(ts, members):
    timer = Timer(mode='seconds', parallel=True)

    # retrieve member keys
    mem_keys = list(members.keys())
    mem_label = ''
    for mem_key in mem_keys:
        mem_label += mem_key + '_'
    mem_label = mem_label[:-1]

    ## SET UP PLOT IO PATHS
    #########################################################################
    name_dict = {}

    # create directory to store all snapshots within
    sub_folder = '{}_{}{}'.format(nl.plot_domain['key'], 
                                   mem_label, nl.anim_name)
    out_path = os.path.join(nl.plot_base_dir, sub_folder)
    Path(out_path).mkdir(parents=True, exist_ok=True)
    name_dict['dt']='{:%Y%m%d_%H%M}'.format(ts)

    ## SETUP PLOT ORGANIZER 
    PO = PlotOrganizer(i_save_fig=nl.args.i_save_fig, path=out_path,
                      name_dict=name_dict, nlp=nl.nlp, geo_plot=True)
    fig,axes = PO.initialize_plot(
        nrows=nl.nrows,
        ncols=nl.ncols,
        figsize=nl.figsize,
        args_subplots_adjust=nl.subplts,
    )


    ### DRAW SPATIAL PLOTS
    col_ind = 0
    row_ind = 0
    #print('######## draw spatial plots ########')
    for mem_key,member in members.items():
        #print('{} {} {}'.format(mem_key, row_ind, col_ind))
        ax = axes[row_ind, col_ind]
        # show hidden axis again
        ax.set_visible(True)

        draw_axis(ax, nl, member, mem_key, timer)

        col_ind += 1
        if col_ind == PO.ncols:
            col_ind = 0
            row_ind += 1

    ### DRAW COLORBAR
    #if ('hide_colorbar' in nl.cfg) and nl.cfg['hide_colorbar']:
    #    pass
    #else:
    #    cax = fig.add_axes([0.15, 0.11, 0.70, 0.03])
    #    ticks = np.linspace(comparison.stats['min'],
    #                        comparison.stats['max'], 5)
    #    colorbar = plt.colorbar(mappable=comparison.mappable, cax=cax, 
    #                            orientation='horizontal',
    #                            ticks=ticks)
    #    unit = nlv[nl.main_var_name]['units']
    #    unit = '' if unit == '' else '[{}]'.format(unit)
    #    cax.set_xlabel('{} {}'.format(nlv[nl.main_var_name]['label'], unit))

    ##  FORMAT AXES
    if nl.i_remove_axes:
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.xaxis.set_ticklabels([])
        ax.yaxis.set_ticklabels([])
        ax.xaxis.set_ticks([])
        ax.yaxis.set_ticks([])

    plt.suptitle('{:%d.%m.%Y %H:00}'.format(ts), 
                x=nl.nlp['time_label_xpos'],
                horizontalalignment='right',
                color=nl.nlp['time_label_color'],
                zorder=2)

    if nl.nlp['i_draw_panel_labels']:
        PO.add_panel_labels(order='cols',
                        start_ind=nl.nlp['panel_labels_start_ind'])

    timer.start('plot.fin')
    PO.finalize_plot()
    timer.stop('plot.fin')

    output = {'timer':timer}
    return(output)



def compute_field(ts):
    members = {}
    ######## LOAD MODELS
    ##########################################################################
    for mem_key,mem_dict in nl.mem_src_dict.items():
        # create member instance
        members[mem_key] = Member(mem_dict, val_type='abs')
        # set time key
        members[mem_key].time_key = 'time'
        for var_name in nl.var_names:
            # load variable
            var = load_member_var(var_name, mem_dict['freq'],
                                ts, ts, mem_dict,
                                nl.var_src_dict,
                                nl.mean_var_src_dict,
                                nl.var_src_dict[var_name]['load'],
                                domain=nl.plot_domain, i_debug=nl.i_debug,
                                dask_chunks=nl.dask_chunks)
            if var is not None:
                members[mem_key].add_var(var_name, var)
            else:
                members[mem_key].add_var(var_name, None)
    output = {'members':members}
    return(output)


def run_for_date(ts, n_par_per_day=1):
    """
    Organize full analysis for a given date (ts).
    ts has to be called ts because run_for_date is called from TimeStepMP.
    """
    timer = Timer(mode='seconds', parallel=False)
    if nl.i_debug >= 2:
        print('{:%Y%m%d}'.format(ts))

    # compute field
    timer.start('load')
    dates = np.arange(ts-timedelta(days=1),
                      ts+timedelta(days=2),
                      timedelta(days=1)).tolist()
    tsmp = TimeStepMP(dates, njobs=min(nl.args.n_par,3), run_async=True)
    fargs = {}
    tsmp.run(compute_field, fargs=fargs, step_args=None)
    tsmp.concat_timesteps()
    members = tsmp.concat_output['members']
    #print(members[nl.mem_key]['TQC'].var.time)
    mem_keys = list(members.keys())
    timer.stop('load')

    timer.start('plot')
    time_steps = np.arange(ts, ts+timedelta(days=1), nl.time_delta).tolist()
    #print(time_steps)
    step_args = []
    for ts in time_steps:
        #print(ts)
        ts_members = {}
        for mem_key in mem_keys:
            if mem_key not in ts_members:
                ts_members[mem_key] = Member(copy.copy(members[mem_key].mem_dict),
                                            val_type='abs')
            for var_name in nl.var_names:

                if np.datetime64(ts) in members[mem_key].vars[var_name].time.values:
                    ts_var = members[mem_key].vars[var_name].sel(time=ts)
                    ts_members[mem_key].vars[var_name] = ts_var
                    continue
                """
                if current ts not in field check for earlier and/or later
                time step until time window max_delta_search timedelta is reached.
                if value before and after are found: interpolate bebetween earlier and next.
                if only one is found: take that value. 
                if neither is found: skip this timestep.
                """
                found_last_ts = False
                backward_delta = timedelta(minutes=0)
                while not found_last_ts:
                    # check if time step exists
                    if (np.datetime64(ts+backward_delta) in 
                        members[mem_key].vars[var_name].time.values):
                        last_ts_var = members[mem_key].vars[var_name].sel(time=ts+backward_delta)
                        found_last_ts = True
                    else:
                        backward_delta -= nl.time_delta 
                    if backward_delta < -nl.max_delta_search:
                        #print('FAILED backward for var {} ts {:%Y%m%d %H%M} and member {}'.format(
                        #        var_name, ts, mem_key))
                        break

                # if current ts not in field check for next time step
                # until max_delta_search timedelta is reached.
                # if that is the case, skip this timestep
                found_next_ts = False
                forward_delta = timedelta(minutes=0)
                while not found_next_ts:
                    # check if time step exists
                    if (np.datetime64(ts+forward_delta) in 
                        members[mem_key].vars[var_name].time.values):
                        next_ts_var = members[mem_key].vars[var_name].sel(time=ts+forward_delta)
                        found_next_ts = True
                    else:
                        forward_delta += nl.time_delta 
                    if forward_delta > nl.max_delta_search:
                        #print('FAILED forward for var {} ts {:%Y%m%d %H%M} and member {}'.format(
                        #        var_name, ts, mem_key))
                        break

                # only last ts is available
                if (found_last_ts and not found_next_ts):
                    print('{} {:%Y%m%d-%H:%M} found last ts only'.format(var_name, ts))
                    ts_members[mem_key].vars[var_name] = last_ts_var
                # only next ts is available
                elif (not found_last_ts and found_next_ts):
                    print('{} {:%Y%m%d-%H:%M} found next ts only'.format(var_name, ts))
                    ts_members[mem_key].vars[var_name] = next_ts_var
                # last and next ts are available
                elif (found_last_ts and found_next_ts):
                    #print('{:%Y%m%d-%H:%M} found both next and last ts'.format(ts))
                    forward_hrs = forward_delta.days*24 + forward_delta.seconds/3600
                    backward_hrs = abs(backward_delta.days*24 + backward_delta.seconds/3600)
                    forward_weight = 1 - forward_hrs / (backward_hrs + forward_hrs)
                    backward_weight = 1 - backward_hrs / (backward_hrs + forward_hrs)
                    ts_members[mem_key].vars[var_name] = (backward_weight * last_ts_var + 
                                                          forward_weight * next_ts_var)
                # neither last nor next ts are available
                elif (not found_last_ts and not found_next_ts):
                    print('{} {:%Y%m%d-%H:%M} found no ts!!'.format(var_name, ts))
                    ts_members[mem_key][var_name] = None
                # case should not exist
                else: raise ValueError()


        #draw_plot(ts, ts_members)
        step_args.append({
            'ts':       ts,
            'members':  ts_members,
        })

    imp = IterMP(njobs=n_par_per_day, run_async=True)
    imp.run(draw_plot, fargs={}, step_args=step_args)
    timer.stop('plot')
    # merge timings from each run with main timer
    for output in imp.output:
        timer.merge_timings(output['timer'])
    output = {'timer':timer}
    return(output)
    

if __name__ == '__main__':

    ###########################################################################
    # PREPARATION STEPS
    timer = Timer(mode='seconds')
    Path(nl.ana_base_dir).mkdir(parents=True, exist_ok=True)
    dates = time_periods_to_dates(nl.time_periods)


    ###########################################################################
    # PART OF ANALYSIS SPECIFIC FOR EACH DAY
    n_par_per_day = min(nl.args.n_par, int(timedelta(days=1) / nl.time_delta))
    n_days_par = max(1, int(nl.args.n_par / n_par_per_day))
    # TODO would need to make subprocess class non-daemonic for have nested subprocesses
    n_days_par = 1
    print('n_par_per_day: {}, n_days_par: {}'.format(n_par_per_day, n_days_par))
    tsmp = TimeStepMP(dates, njobs=n_days_par, run_async=True)
    fargs = {'n_par_per_day':n_par_per_day}
    tsmp.run(run_for_date, fargs=fargs, step_args=None)
    # merge timings from each run with main timer
    for output in tsmp.output:
        timer.merge_timings(output['timer'])
    #tsmp.concat_timesteps()
    #members = tsmp.concat_output['members']

    timer.print_report()
