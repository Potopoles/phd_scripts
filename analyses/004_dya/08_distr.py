#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Create distributions (e.g. frequency distr.) of variables.
author			Christoph Heim
date created    02.10.2020
date changed    02.10.2020
usage           args:
                1st:    number of parallel tasks
                2nd:    i_save_fig (0: show, 1: png, 2: pdf, 3: jpg)
"""
###############################################################################
import os, glob, collections
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from pathlib import Path
from datetime import datetime, timedelta
from scipy import stats
import nl_08 as nl
from package.nl_variables import nlv
from package.var_pp import var_mapping, compute_variable
from package.utilities import Timer 
from package.plot_functions import PlotOrganizer, draw_map
from package.functions import load_member_var
from package.mp import TimeStepMP, IterMP
from package.member import Member
from package.comparison import Comparison
###############################################################################

def draw_plot(ts, members):
    timer = Timer(mode='seconds')
    timer.start('plot')
    
    name_dict = {'spatial':nl.run_mode,
                 'var':nl.var_name}
    # if snapshot plot, create directory to store all snapshots within
    if nl.cfg['snapshots']['on']:
        sub_folder = 'spatial_{}_var_{}'.format(nl.run_mode, nl.var_name)
        out_path = os.path.join(nl.plot_base_dir, sub_folder)
        Path(out_path).mkdir(parents=True, exist_ok=True)
        name_dict['dt']='{:%Y%m%d_%H%M}'.format(ts)
    else:
        out_path = nl.plot_base_dir

    comparison = Comparison(nl.var_name, members)   
    comparison.calc_statistics()
    # set min and max values
    if nl.cfg['min_max'][0] is None:
        pass
    elif nl.cfg['min_max'][0] == 'obs':
        comparison.stats['min'] = \
                    members['CM_SAF'][nl.var_name].var.values.min() 
    else:
        comparison.stats['min'] = nl.cfg['min_max'][0]
    if nl.cfg['min_max'][1] is None:
        pass
    elif nl.cfg['min_max'][1] == 'obs':
        comparison.stats['max'] = \
                    members['CM_SAF'][nl.var_name].var.values.max() 
    else:
        comparison.stats['max'] = nl.cfg['min_max'][1]


    # sort after resolution
    if nl.nlp['plot_order'] == 'resolution':
        mem_keys = list(members.keys())
        include_obs = True if (nl.i_use_obs and nl.cfg['obs']
                                    is not False) else False
        if include_obs: mem_keys.remove(nl.cfg['obs'])
        mem_res = [members[mem_key][nl.var_name].mem_dict['res'] \
                                                for mem_key in mem_keys]
        sort_inds = np.argsort(mem_res)[::-1]
        sort_mem_keys = np.asarray(mem_keys)[sort_inds]
        ordered = collections.OrderedDict()
        for mem_key in sort_mem_keys:
            ordered[mem_key] = members[mem_key]
        if include_obs: ordered[nl.cfg['obs']] = members[nl.cfg['obs']]
        members = ordered

    PO = PlotOrganizer(i_save_fig=nl.i_save_fig, path=out_path,
                      name_dict=name_dict, nlp=nl.nlp, geo_plot=True)
    fig,axes = PO.initialize_plot(nrows=nl.nlp['nrows'],
                                  ncols=nl.nlp['ncols'],
                                  figsize=nl.nlp['figsize'])

    if ('add_bias_labels' in nl.nlp.keys()) and nl.nlp['add_bias_labels']:
        obs_mean = members[nl.cfg['obs']][
                        nl.var_name].var.mean(dim=['lon','lat'])

    col_ind = 0
    row_ind = 0
    for mem_key,member in members.items():
        if nl.nlp['plot_order'] == 'position':
            if mem_key != nl.cfg['obs']:
                col_ind = nl.cfg['use_sims'][mem_key]['plot_pos'][0]
                row_ind = nl.cfg['use_sims'][mem_key]['plot_pos'][1]
            else:
                row_ind = nl.nlp['nrows'] - 1
                col_ind = nl.nlp['ncols'] - 1

        ax = axes[row_ind, col_ind]

        ## test frequency of inversion
        #print(skey)
        #print((1- sim.var.mean().values)*100)
        #print()

        draw_map(ax, nl.cfg['domain'], nl.nlp,
                 add_xlabel=True, add_ylabel=True,
                 dticks=nl.cfg['domain']['dticks'])
        member[nl.var_name].plot_lat_lon(ax, nlp=nl.nlp)

        if ('add_bias_labels' in nl.nlp.keys()) and nl.nlp['add_bias_labels']:
            if mem_key != nl.cfg['obs']:
                mem_diff = (member[nl.var_name].var.mean(
                                dim=['lon','lat']) - obs_mean).values
                # strangely, NICAM returns a list..
                try:
                    mem_diff = mem_diff[0]
                except IndexError: pass
                #if isinstance(mem_diff, list):
                #    mem_diff = mem_diff[0]
                label = '{:5.1f}'.format(mem_diff)
                label += ' Wm$^{-2}$'
                pan_lab_x = ax.get_xlim()[0] + (
                                ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.01
                pan_lab_y = ax.get_ylim()[0] + (
                                ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.03
                ax.text(pan_lab_x, pan_lab_y, label,
                        fontdict={'fontsize':12, 'color':'black'})

        if col_ind > 0:
           ax.set_yticklabels([]) 
           ax.set_ylabel('')
        if row_ind < PO.nrows-1:
           ax.set_xticklabels([]) 
           ax.set_xlabel('')


        if nl.nlp['plot_order'] == 'resolution':
            col_ind += 1
            if col_ind == PO.ncols:
                col_ind = 0
                row_ind += 1
    # end loop

    ## colorbar
    if ('hide_colorbar' in nl.cfg) and nl.cfg['hide_colorbar']:
        pass
    else:
        cax = fig.add_axes([0.15, 0.10, 0.70, 0.03])
        ticks = np.linspace(comparison.stats['min'],
                            comparison.stats['max'], 5)
        colorbar = plt.colorbar(mappable=comparison.mappable, cax=cax, 
                                orientation='horizontal',
                                ticks=ticks)
        unit = nlv[nl.var_name]['unit']
        unit = '' if unit == '' else '[{}]'.format(unit)
        cax.set_xlabel('{} {}'.format(nlv[nl.var_name]['label'], unit))

    #cax.set_xticklabels(ticks)
    if nl.cfg['snapshots']['on']:
        plt.suptitle('{:%d.%m.%Y %H:%M}'.format(ts))
        #max_bright = 1.0
        #min_bright = 0.5
        #hour = ts.hour + ts.minute/60
        #bright = min_bright + (max_bright - min_bright) * (
        #            1/2 + np.sin((hour-6)/24*2*np.pi)/2 )
        #bg_color = (bright,bright,bright)
        #plt.rcParams['savefig.facecolor'] = bg_color 

    PO.add_panel_labels(order='cols',
                    start_ind=nl.nlp['panel_labels_start_ind'])
    fig.subplots_adjust(**nl.cfg['subplts'])
    PO.finalize_plot()

    timer.stop('plot')
    output = {'timer':timer}
    return(output)



def compute_field(date, members):

    ######## LOAD OBSERVATIONS
    ##########################################################################
    #if nl.i_use_obs:
    #    obs_key = nl.cfg['obs']
    #    obs_dict = nl.obs_src_dict[obs_key]
    #    var = load_member_var(nl.var_name, date, date, obs_dict,
    #                        nl.var_src_dict,
    #                        nl.var_src_dict[nl.var_name]['load'],
    #                        domain=domain, i_debug=nl.i_debug)
    #    if var is not None:
    #        member = Member(var, obs_dict,
    #                        #{'label':'OBS ({})'.format(
    #                        #nl.use_obs[obs_key]['label'])},
    #                        comparison=None)

    #        if obs_key not in members.keys():
    #            members[obs_key] = {}
    #        members[obs_key][nl.var_name] = member
    #    else:
    #        members[obs_key] = None

    ######## LOAD MODELS
    ##########################################################################
    for mem_key,mem_dict in nl.use_sims.items():
        var = load_member_var(nl.var_name, date, date, mem_dict,
                            nl.var_src_dict,
                            nl.var_src_dict[nl.var_name]['load'],
                            domain=nl.domain, i_debug=nl.i_debug)

        if var is not None:
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
    timer.start('comp')
    for mem_key,member in members.items():
        print(mem_key)
        values = member[nl.var_name].var.values.flatten()
        values = values[~np.isnan(values)]
        #var.values[var.values == 0] = np.nan
        bins = np.arange(0,3000,200)
        #density = stats.gaussian_kde(values)
        #n, x, _ = plt.hist(values, bins=bins, histtype=u'step', density=True)
        #plt.plot(x, density(x))
        plt.hist(values, bins=bins, histtype=u'step', density=True,
                            label=mem_key)
    raw_handles, labels = plt.gca().get_legend_handles_labels()
    handles = [Line2D([],[], c=h.get_edgecolor()) for h in raw_handles]
    #plt.yscale('log', nonposy='clip')
    plt.legend(handles=handles, labels=labels)
    plt.show()
    quit()
        #member[nl.var_name].var = 
    timer.stop('comp')

    ###########################################################################
    # PLOTTING
    # quit now if not plotting required
    if not nl.i_plot:
        timer.start('plot')
        draw_plot(ts=None, members=members)
        timer.stop('plot')

    timer.print_report()
