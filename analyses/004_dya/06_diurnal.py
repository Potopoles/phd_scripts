#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Compute and plot diurnal cycle.
author			Christoph Heim
date created    17.08.2020
date changed    18.08.2020
usage           args:
                1st:    number of parallel tasks
                2nd:    i_save_fig (0: show, 1: png, 2: pdf, 3: jpg)
"""
###############################################################################
import os, glob, collections
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime, timedelta
import nl_06 as nl
from package.nl_variables import nlv
from package.var_pp import var_mapping, compute_variable
from package.utilities import Timer, calc_mean_diurnal_cycle 
from package.plot_functions import PlotOrganizer, draw_map
from package.functions import load_member_var_for_date
from package.mp import TimeStepMP, IterMP
from package.member import Member
from package.comparison import Comparison
###############################################################################

def draw_plot(ts, members):

    timer = Timer(mode='seconds')
    timer.start('plot')
    
    name_dict = {'spatial':nl.run_mode,
                 'var':nl.cfg['var_name']}
    out_path = nl.plot_base_dir

    comparison = Comparison(nl.cfg['var_name'], members)   
    comparison.calc_statistics()

    PO = PlotOrganizer(i_save_fig=nl.i_save_fig, path=out_path,
                      name_dict=name_dict, nlp=nl.nlp, geo_plot=False)

    fig,axes = PO.initialize_plot(nrows=nl.nlp['nrows'],
                                  ncols=nl.nlp['ncols'],
                                  figsize=nl.nlp['figsize'])
    col_ind = 0
    row_ind = 0
    for skey,sim in members.items():
        mem = sim[nl.cfg['var_name']]
        ax = axes[row_ind, col_ind]

        handle, = ax.plot(mem.var, label=nl.cfg['use_sims'][skey]['label'])
        PO.handles.append(handle)
        #plt.show()
        #quit()

        #ax.set_yticklabels([]) 
        #ax.set_ylabel('')
        #ax.set_xticklabels([]) 
        #ax.set_xlabel('')

    # end loop

    ax.legend(handles=PO.handles)

    PO.set_axes_labels(ax, 'DIURN', nl.cfg['var_name'])
    ax.set_xlim((0,24))
    PO.add_panel_labels(order='cols')
    fig.subplots_adjust(**nl.nlp['arg_subplots_adjust'])
    PO.finalize_plot()

    timer.stop('plot')
    output = {'timer':timer}
    return(output)



def compute_field(date, members):
    var_name = nl.cfg['var_name']
    # in case of remapping don't select domain because it will have a gap
    if 'remapped' in os.path.split(nl.var_src[var_name]['src'])[1]:
        domain = None
    else: domain = nl.cfg['domain']

    ######## LOAD MODELS
    ##########################################################################
    for skey,sdict in nl.cfg['use_sims'].items():
        var = load_member_var_for_date(var_name, date, skey, sdict,
                            nl.var_src, nl.var_src[var_name]['load'],
                            domain=domain, i_debug=nl.i_debug)

        if var is not None:
            var = var.mean(dim=['lon','lat'])
            # create member instance
            member = Member(var,
                              {'label':sdict['label'],'res':sdict['res']},
                              comparison=None)
            if skey not in members.keys():
                members[skey] = {}
            if members[skey] is not None:
                members[skey][var_name] = member
        else:
            members[skey] = None
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
    # if not snapshots compute mean
    timer.start('comp')
    for memkey,mem in members.items():
        mem[nl.cfg['var_name']].var = calc_mean_diurnal_cycle(
                            mem[nl.cfg['var_name']].var, aggreg_type='MEAN')
        #plt.plot(mem[nl.cfg['var_name']].var.time,
        #         mem[nl.cfg['var_name']].var)
    #plt.show()
    #quit()
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
