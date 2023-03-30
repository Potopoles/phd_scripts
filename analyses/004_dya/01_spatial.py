#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Create spatial plots of various horizontal 2d fields.
                If observations are available, show them along the models
                e.g. validate radiative flux with satellite obs.
author			Christoph Heim
date created    18.11.2019
date changed    30.03.2021
usage           args:
                1st:    number of parallel tasks
                2nd:    i_save_fig (0: show, 1: png, 2: pdf, 3: jpg)
"""
###############################################################################
import os, glob, collections, copy
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime, timedelta
import nl_01 as nl
from package.nl_variables import nlv
from package.var_pp import var_mapping, compute_variable
from package.utilities import Timer, dt64_to_dt, subsel_domain
from package.plot_functions import PlotOrganizer, draw_map
from package.functions import load_member_var, time_periods_to_dates
from package.mp import TimeStepMP, IterMP
from package.member import Member
from package.comparison import Comparison
###############################################################################

def draw_axis(ax, nl, member, mem_key, obs_mean=None):
    draw_map(ax, nl.cfg['domain'], nl.nlp,
             add_xlabel=True, add_ylabel=True,
             dticks=nl.cfg['domain']['dticks'])

    #print(mem_key)
    #print(member[nl.var_name].var.mean(dim=['lon','lat']))
    #print(member[nl.var_name].var.max(dim=['lon','lat']))
    #print(member[nl.var_name].var.min(dim=['lon','lat']))
    #quit()

    if ( ('add_bias_labels' in nl.nlp.keys()) and 
         nl.nlp['add_bias_labels'] and
         nl.i_use_obs ):
        if mem_key != nl.cfg['obs']:
            #print(obs_mean)

            if nl.cfg['domain'] is not None:
                memb_var = subsel_domain(member[nl.var_name].var,
                                        nl.cfg['domain'])
            mem_diff = copy.deepcopy((memb_var.mean(dim=['lon','lat']) - obs_mean).values)
            # strangely, NICAM returns a list..
            try:
                mem_diff = mem_diff[0]
            except IndexError: pass
            #if isinstance(mem_diff, list):
            #    mem_diff = mem_diff[0]
            label = '{:6.2f} '.format(mem_diff)
            unit = nlv[nl.var_name]['units']
            label += unit
            #label += ' Wm$^{-2}$'
            #print(label)
            pan_lab_x = ax.get_xlim()[0] + (
                            ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.01
            pan_lab_y = ax.get_ylim()[0] + (
                            ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.03
            ax.text(pan_lab_x, pan_lab_y, label,
                    fontdict={'fontsize':nl.nlp['bias_labels_fontsize'], 'color':'black'})

    # compute bias 
    if nl.i_plot_bias:
        obs = members[nl.cfg['obs']][nl.var_name].var
        memb = member[nl.var_name].var
        #memb = memb.interp(lon=obs.lon, lat=obs.lat)
        obs = obs.interp(lon=memb.lon, lat=memb.lat)
        memb.values -= obs.values
        nl.nlp['cmap'] = nl.nlp['cmaps']['blue_red'] 

    member[nl.var_name].plot_lat_lon(ax, nlp=nl.nlp)


def draw_plot(ts, members):
    timer = Timer(mode='seconds')
    timer.start('plot')
    
    name_dict = {}
    name_dict['spatial']          = nl.cfg['domain']['code']
    if nl.i_plot_bias:
        name_dict[nl.run_mode]        = 'bias_{}'.format(nl.var_name)
    else:
        name_dict[nl.run_mode]        = nl.var_name
    # if snapshot plot, create directory to store all snapshots within
    if nl.cfg['snapshots']['on']:
        sub_folder = 'spatial_{}_var_{}'.format(nl.run_mode, nl.var_name)
        out_path = os.path.join(nl.plot_base_dir, sub_folder)
        Path(out_path).mkdir(parents=True, exist_ok=True)
        name_dict['dt']='{:%Y%m%d_%H%M}'.format(ts)
    else:
        out_path = nl.plot_base_dir

    # for members with multiple time steps split up into different members
    ts_members = {}
    if nl.i_aggreg not in ('all', 'none'):
        #if nl.nlp['plot_order'] == 'time':
        for mem_key,member in members.items():
            for i,ts64 in enumerate(member[nl.var_name].var.time):
                ts = dt64_to_dt(ts64)
                ts_mem_dict = copy.copy(member[nl.var_name].mem_dict)
                if nl.i_aggreg == 'monthly':
                    ts_mem_key = '{}_{:%m}'.format(mem_key, ts)
                    ts_mem_dict['label'] = ts.month
                elif nl.i_aggreg == 'yearly':
                    ts_mem_key = '{}_{:%Y}'.format(mem_key, ts)
                    ts_mem_dict['label'] = '{} {}'.format(ts_mem_dict['label'],
                                                        ts.year)
                elif nl.i_aggreg == 'none':
                    ts_mem_key = '{}_{:%Y%m%d%H%M}'.format(mem_key, ts)
                    ts_mem_dict['label'] = '{:%Y%m%d%H%M}'.format(ts)
                else: raise NotImplementedError()
                ts_member = Member(member[nl.var_name].var.isel(time=i),
                                    ts_mem_dict)
                ts_members[ts_mem_key] = {}
                ts_members[ts_mem_key][nl.var_name] = ts_member
        members = ts_members
        #else:
        #    for mem_key,member in members.items():
        #        if (len(member[nl.var_name].var.time) > 1):             
        #            raise ValueError('Member {} contains multiple '.format(mem_key)+
        #                             'even though plot_order!="time"')

    comparison = Comparison(nl.var_name, members)   
    comparison.calc_statistics()

    if nl.i_plot_bias:
        nl.cfg['min_max'] = nl.cfg['min_max_bias']

    # set min and max values
    if nl.cfg['min_max'][0] is None:
        pass
    elif nl.cfg['min_max'][0] == 'obs':
        comparison.stats['min'] = \
                    members[nl.cfg['obs']][nl.var_name].var.values.min() 
    else:
        comparison.stats['min'] = nl.cfg['min_max'][0]
    if nl.cfg['min_max'][1] is None:
        pass
    elif nl.cfg['min_max'][1] == 'obs':
        comparison.stats['max'] = \
                    members[nl.cfg['obs']][nl.var_name].var.values.max() 
    else:
        comparison.stats['max'] = nl.cfg['min_max'][1]

    if nl.nlp['plot_order'] != 'position':
        mem_keys = list(members.keys())
        include_obs = True if (nl.i_use_obs and nl.cfg['obs']
                                    is not False) else False
        contains_ERA5 = False
        if ( ('ERA5_31' in mem_keys) and ('ERA5_31' != nl.cfg['obs']) and
             nl.ERA5_as_obs ):
            contains_ERA5 = True
            mem_keys.remove('ERA5_31')
        if include_obs: mem_keys.remove(nl.cfg['obs'])
        # sort after resolution
        if nl.nlp['plot_order'] == 'resolution':
            mem_res = [members[mem_key][nl.var_name].mem_dict['res'] \
                                                    for mem_key in mem_keys]
            sort_inds = np.argsort(mem_res)[::-1]
            sort_mem_keys = np.asarray(mem_keys)[sort_inds]

            ordered = collections.OrderedDict()
            for mem_key in sort_mem_keys:
                ordered[mem_key] = members[mem_key]
            if contains_ERA5:
                ordered['ERA5_31'] = members['ERA5_31']
            if include_obs: 
                ordered[nl.cfg['obs']] = members[nl.cfg['obs']]
            members = ordered

    PO = PlotOrganizer(i_save_fig=nl.i_save_fig, path=out_path,
                      name_dict=name_dict, nlp=nl.nlp, geo_plot=True)
    print(nl.nlp['figsize'])
    fig,axes = PO.initialize_plot(nrows=nl.nlp['nrows'],
                                  ncols=nl.nlp['ncols'],
                                  figsize=nl.nlp['figsize'])

    # hide all axes to later only show those with a member
    for axs in axes:
        for ax in axs:
            ax.set_visible(False)

    if ( ('add_bias_labels' in nl.nlp.keys()) and 
         nl.nlp['add_bias_labels'] and
         nl.i_use_obs ):
        if nl.cfg['domain'] is not None:
            obs_var = subsel_domain(
                        members[nl.cfg['obs']][nl.var_name].var,
                        nl.cfg['domain'])
            obs_mean = obs_var.mean(dim=['lon','lat'])
    else:
        obs_mean = None

    col_ind = 0
    row_ind = 0
    print('######## draw spatial plots ########')
    for mem_key,member in members.items():
        print('{} {} {}'.format(mem_key, row_ind, col_ind))
        if nl.nlp['plot_order'] == 'position':
            if mem_key != nl.cfg['obs']:
                col_ind = nl.cfg['use_sims'][mem_key]['plot_pos'][1]
                row_ind = nl.cfg['use_sims'][mem_key]['plot_pos'][0]
            else:
                row_ind = nl.nlp['nrows'] - 1
                col_ind = nl.nlp['ncols'] - 1

        ax = axes[row_ind, col_ind]
        # show hidden axis again
        ax.set_visible(True)

        ## test frequency of inversion
        #print(skey)
        #print((1- member.var.mean().values)*100)
        #print()

        draw_axis(ax, nl, member, mem_key, obs_mean)

        if col_ind > 0:
           ax.set_yticklabels([]) 
           ax.set_ylabel('')
        if row_ind < PO.nrows-1:
           ax.set_xticklabels([]) 
           ax.set_xlabel('')

        if nl.nlp['plot_order'] != 'position':
            col_ind += 1
            if col_ind == PO.ncols:
                col_ind = 0
                row_ind += 1
    # end loop

    ## colorbar
    if ('hide_colorbar' in nl.cfg) and nl.cfg['hide_colorbar']:
        pass
    else:
        cax = fig.add_axes([0.15, 0.12, 0.70, 0.03])
        ticks = np.linspace(comparison.stats['min'],
                            comparison.stats['max'], 5)
        colorbar = plt.colorbar(mappable=comparison.mappable, cax=cax, 
                                orientation='horizontal',
                                ticks=ticks)
        unit = nlv[nl.var_name]['units']
        unit = '' if unit == '' else '[{}]'.format(unit)
        cax.set_xlabel('{} {}'.format(nlv[nl.var_name]['label'], unit))

    #cax.set_xticklabels(ticks)
    if nl.cfg['snapshots']['on'] and nl.nlp['snapshots_plot_time']:
        plt.suptitle('{:%d.%m.%Y %H:%M}'.format(ts), fontsize=10)

        #max_bright = 1.0
        #min_bright = 0.5
        #hour = ts.hour + ts.minute/60
        #bright = min_bright + (max_bright - min_bright) * (
        #            1/2 + np.sin((hour-6)/24*2*np.pi)/2 )
        #bg_color = (bright,bright,bright)
        #plt.rcParams['savefig.facecolor'] = bg_color 

    if nl.nlp['i_draw_panel_labels']:
        PO.add_panel_labels(order='cols',
                        start_ind=nl.nlp['panel_labels_start_ind'],
                        shift_right=nl.nlp['panel_labels_shift_right'], 
                        shift_up=0.12, fontsize=11)
    fig.subplots_adjust(**nl.cfg['subplts'])
    PO.finalize_plot()

    timer.stop('plot')
    output = {'timer':timer}
    return(output)



def compute_field(date, members):
    ## in case of remapping don't select domain because it will have a gap
    #if 'remapped' in os.path.split(nl.var_src_dict[nl.var_name]['src'])[1]:
    #    domain = None
    #else: domain = nl.cfg['domain']
    domain = nl.cfg['domain']
    load_domain = copy.deepcopy(domain)
    load_domain['lon'] = slice(domain['lon'].start-0.5,
                               domain['lon'].stop+0.5)
    load_domain['lat'] = slice(domain['lat'].start-0.5,
                               domain['lat'].stop+0.5)

    ######## LOAD OBSERVATIONS
    ##########################################################################
    if nl.i_use_obs and nl.cfg['obs'] is not False:
        obs_key = nl.cfg['obs']
        obs_dict = nl.obs_src_dict[obs_key]
        var = load_member_var(nl.var_name, date, date, obs_dict,
                            nl.var_src_dict,
                            nl.var_src_dict[nl.var_name]['load'],
                            domain=load_domain, i_debug=nl.i_debug)
                            #domain=nl.cfg['domain'], i_debug=nl.i_debug)
                            #domain=None, i_debug=nl.i_debug)
        if var is not None:
            member = Member(var, obs_dict,
                            #{'label':'OBS ({})'.format(
                            #nl.use_obs[obs_key]['label'])},
                            comparison=None)

            if obs_key not in members.keys():
                members[obs_key] = {}
            members[obs_key][nl.var_name] = member
        else:
            members[obs_key] = None

    ######## LOAD MODELS
    ##########################################################################
    for mem_key,mem_dict in nl.cfg['use_sims'].items():
        var = load_member_var(nl.var_name, date, date, mem_dict,
                            nl.var_src_dict,
                            nl.var_src_dict[nl.var_name]['load'],
                            domain=load_domain, i_debug=nl.i_debug)
                            #domain=nl.cfg['domain'], i_debug=nl.i_debug)
                            #domain=None, i_debug=nl.i_debug)
        if var is not None:
            # if not snapshots desired, aggregate here
            if not nl.cfg['snapshots']['on']:
                var = var.mean(dim='time')
                var = var.expand_dims({'time':[date]})
                #var = var.median(dim='time')
            #var = var.sel(rel_alt=slice(0,1))
            #var = var.mean(dim='rel_alt')

            # coarse-grain the dataset
            if nl.i_coarse_grain > 0:
                print('COARSE GRAIN')
                window = int(nl.i_coarse_grain/mem_dict['res'])
                var = var.coarsen({'lon':window, 'lat':window},
                                   boundary='trim').mean()
                var = var.rename(nl.var_name)

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
    # if not snapshots compute mean based on chosen aggregation intervals
    if not nl.cfg['snapshots']['on']:
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
    # plot either snapshots or time mean plot
    if nl.cfg['snapshots']['on']:
        # without first step because it is 00:00 which is absent in files
        # (initializaiton of models)
        first_date = nl.time_periods[0]['first_date']
        last_date = nl.time_periods[0]['last_date']
        dates = np.arange(first_date, last_date+timedelta(days=1),
                          nl.cfg['snapshots']['freq']).tolist()[1:]
        #dates = dates[0:3]
        #dates = [dates[23]]
        #dates = [dates[0]]
        #print(dates)

        step_args = []
        for ts in dates:
            #print('####{}'.format(ts))
            step_members = {}
            found_all_members = True
            for mem_key,member in members.items():
                #print(mem_key)
                # if current ts not in field check for earlier time step
                # until nl.cfg['snapshots']['max_back'] timedelta is reached.
                # if that is the case, skip this timestep
                found_ts = False
                backward_delta = timedelta(minutes=0)
                while not found_ts:
                    try:
                        #print(ts-backward_delta)
                        ts_field = members[mem_key][nl.var_name].var.sel(
                                                    time=ts-backward_delta)
                        found_ts = True
                    except KeyError:
                        backward_delta += nl.cfg['snapshots']['freq'] 
                    if backward_delta > nl.cfg['snapshots']['max_back']:
                        print('FAILED for ts {:%Y%m%d_%H%M} and member {}'.format(
                                ts, mem_key))
                        break

                if found_ts:
                    #print('\t found ts')
                    if mem_key not in step_members:
                        step_members[mem_key] = {}
                    step_members[mem_key][nl.var_name] = Member(ts_field,
                                members[mem_key][nl.var_name].mem_dict)
                else:
                    found_all_members = False
                    break
                    
            if found_all_members:
                step_args.append({'ts':ts, 'members':step_members})

        imp = IterMP(njobs=nl.njobs, run_async=False)
        imp.run(draw_plot, fargs={}, step_args=step_args)
        # merge timings from each run with main timer
        for output in imp.output:
            timer.merge_timings(output['timer'])
    else:
        timer.start('plot')
        draw_plot(ts=None, members=members)
        timer.stop('plot')

    timer.print_report()
