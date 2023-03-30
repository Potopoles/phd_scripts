#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Create spatial mean altitude time cross-sects.
author			Christoph Heim
date crated     06.04.2022
date changed    06.04.2022
usage           args:
"""
###############################################################################
import os, argparse
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.dates as mdates
from types import SimpleNamespace
from an_super import Analysis
from package.nl_variables import nlv, get_plt_units, get_plt_fact
from package.utilities import Timer, area_weighted_mean_lat_lon
from package.time_processing import Time_Processing as TP
from package.plot_functions import PlotOrganizer
from package.functions import import_namelist, loc_to_var_name
from package.mp import TimeStepMP

import matplotlib.pyplot as plt
###############################################################################

class Analysis_10(Analysis):

    def __init__(self, nl):
        super(Analysis_10, self).__init__(nl)
        self.nl = nl
        self.ana_number = 10


    def draw_axis(self, PO, members, ax):
        self.draw_axis_DEFAULT(ax)

        # multi-member plotting not implemented here.
        if len(members) == 0:
            print('warning. 0 mebmers to plot!!')
            return()
        mem_key = list(members.keys())[0]
        member = members[mem_key]

        ### FORMAT MEMBERS FOR PLOTTING
        ##########################################################################
        #print(mem_key)
        agg_var_name = list(member.vars.keys())[0]
        var = member.vars[agg_var_name]
        var_name = TP.get_var_name(agg_var_name)
        agg_level = TP.get_agg_level(agg_var_name)
        agg_operator = TP.get_agg_operator(agg_var_name)
        if agg_level == TP.DIURNAL_CYCLE:
            i_plot_spread   = 1
            # append time 00:00 as time 24:00 at the end of the diurnal cycle
            # to make the plot periodic.
            hr_24 = var.sel(hour = 0).copy()
            hr_24['hour'] = 24
            member.vars[agg_var_name] = xr.concat([var, hr_24], dim='hour')

        ### FORMAT AXIS
        ##########################################################################
        time_key = self.nl.nlp['time_key'][agg_level]
        if self.nl.nlp['xlim'][agg_level] is not None:
            ax.set_xlim(self.nl.nlp['xlim'][agg_level])

        # set xaxis locator/formatter
        locator = self.nl.nlp['tick_locator'][agg_level]
        if time_key == 'time':
            ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
        else:
            ax.xaxis.set_major_locator(locator)




        ### DRAW PLOT
        ##########################################################################
        ### MEMBER SPECIFIC PROPERTIES
        ######################################################################

        agg_var_name = list(member.vars.keys())[0]
        var = member.vars[agg_var_name]
        var_name = TP.get_var_name(agg_var_name)
        #agg_level = TP.get_agg_level(agg_var_name)
        #agg_operator = TP.get_agg_operator(agg_var_name)

        plot_var = var * get_plt_fact(var_name)


        ### DRAW PLOT
        ##################################################################
        #print(plot_var)
        #quit()

        plot_var.squeeze().plot.contourf(
            time_key, 'alt',
            cmap=self.nl.nlp['cmaps']['cf']['abs'][var_name],
            levels=self.nl.nlp['levels']['cf']['abs'][var_name],
            #vmin=nl.var_cfgs[var_name]['min_max'][0],
            #vmax=nl.var_cfgs[var_name]['min_max'][1],
            add_colorbar=False, add_labels=False,
            #rasterized=True, linewidth=0, edgecolor='face',
            #levels=100, antialiased=True
        )


        ### FINAL FORMAT AXIS
        ##########################################################################

        ## plot title
        try:
            ax.set_title(self.nl.title)
        except AttributeError:
            pass

        ## axes labels
        if time_key in 'month':
            PO.set_axes_labels(ax, 'COORD_MONTH', 
                            loc_to_var_name(self.nl.var_names[0]))
        elif time_key == 'time':
            PO.set_axes_labels(ax, 'COORD_DATETIME', 
                            loc_to_var_name(self.nl.var_names[0]))
        elif time_key == 'hour':
            PO.set_axes_labels(ax, 'COORD_HOUR', 
                            loc_to_var_name(self.nl.var_names[0]))
        else:
            raise NotImplementedError()

        ## axes limits
        ax.set_ylim(self.nl.alt_lims)



    def compute_var(self, var):
        # average horizontally
        #var = var.mean(dim=['lon', 'lat'])
        var = area_weighted_mean_lat_lon(var)

        # resample to daily mean values if required.
        if self.nl.agg_level not in [TP.HOURLY_SERIES, TP.DIURNAL_CYCLE]:
            var = TP.run_aggregation_step(var, 
                      { TP.ACTION:TP.RESAMPLE, 
                        TP.FREQUENCY:'D', 
                        TP.OPERATOR:TP.MEAN  })
        return(var)


    def prepare_namelist(self):

        ## find all aggregation operators that should be computed
        ## this may lead to NotImplementedError in time_processing.py
        #agg_operators = []
        #agg_operators.extend(self.nl.plot_lines[self.nl.agg_level])
        #if self.nl.agg_level in self.nl.plot_spread:
        #    agg_operators.extend(self.nl.plot_spread[self.nl.agg_level])
        #self.nl.agg_operators = list(set(agg_operators))

        ## aggregated var names for loading
        #self.nl.load_agg_var_names = []
        #for var_name in self.nl.var_names:
        #    for agg_operator in self.nl.agg_operators:
        #        agg_var_name = TP.get_agg_var_name(var_name, 
        #                    self.nl.agg_level, agg_operator)
        #        self.nl.load_agg_var_names.append(agg_var_name)

        self.prepare_namelist_DEFAULT()       


    

if __name__ == '__main__':

    # READ INPUT ARGUMENTS
    ###########################################################################
    parser = argparse.ArgumentParser(description = 'Draw timeline plots.')
    # variable to plot
    parser.add_argument('var_names', type=str)
    # number of parallel processes
    parser.add_argument('-p', '--n_par', type=int, default=1)
    # save or not? (0: show, 1: png, 2: pdf, 3: jpg)
    parser.add_argument('-s', '--i_save_fig', type=int, default=3)
    # recompute?
    parser.add_argument('-r', '--i_recompute', type=int, default=0)
    # computation mode? (normal, load, dask)
    parser.add_argument('-c', '--computation_mode', type=str, default='load')
    args = parser.parse_args()

    # PREPARATION STEPS
    ###########################################################################
    timer = Timer(mode='seconds')
    import nl_10 as nl_ana_raw
    from nl_plot_10 import nlp
    ana = Analysis_10(nl=SimpleNamespace())
    import_namelist(ana.nl, nl_ana_raw)
    ana.nl.nlp = nlp

    # input arguments
    ana.nl.i_recompute = args.i_recompute
    ana.nl.i_save_fig = args.i_save_fig
    ana.nl.n_par = args.n_par
    ana.nl.var_names = args.var_names.split(',')
    ana.nl.computation_mode = args.computation_mode

    ana.prepare_namelist()
    if ana.nl.i_recompute: ana.nl.i_plot = 0

    # should files be computed...
    if ana.nl.i_recompute:
        # PART OF ANALYSIS SPECIFIC FOR EACH DAY
        ######################################################################
        timer.start('daily')
        tsmp = TimeStepMP(ana.iter_dates, njobs=ana.nl.n_par, run_async=True)
        fargs = {}
        tsmp.run(ana.compute_src_members_for_date, fargs=fargs, step_args=None)
        tsmp.concat_timesteps()
        src_members = tsmp.concat_output['members']
        timer.stop('daily')

        # PART OF ANALYSIS FOR ENTIRE TIME SERIES
        ######################################################################
        # compute aggregation/grouping on entire time series
        timer.start('all')
        ana.indiv_targ_members = ana.aggreg_src_members_to_indiv_targ_members(
                                        src_members)
        timer.stop('all')

        # SAVE DATA TO PICKLE
        ######################################################################
        ana.save_to_pickle(ana.indiv_targ_members)
        
    # ... or be reloaded from precomputed pickle files.
    else:
        # LOAD PRECOMPUTED DATA FROM PICKLE
        ######################################################################
        ana.indiv_targ_members = ana.load_from_pickle()

    # PLOTTING
    ##########################################################################
    if ana.nl.i_plot:
        timer.start('prepare')
        #print(ana.indiv_targ_members.keys())
        targ_members = ana.prepare_for_plotting(ana.indiv_targ_members)
        #print(targ_members.keys())
        #quit()

        timer.stop('prepare')

        ## SET UP PLOT IO PATH
        ######################################################################
        timer.start('plot')

        name_dict = {}
        name_dict['timeline']   = ana.nl.plot_domain['key']
        name_dict[ana.nl.agg_level] = ana.nl.var_names[0]
        if ana.nl.plot_append != '':
            name_dict[ana.nl.plot_append] = ''

        ## INITIALIZE PLOT
        ######################################################################
        PO = PlotOrganizer(i_save_fig=ana.nl.i_save_fig,
                            path=ana.nl.plot_base_dir,
                            name_dict=name_dict, nlp=ana.nl.nlp,
                            geo_plot=ana.nl.nlp['geo_plot'])
        fig,axes = PO.initialize_plot(nrows=ana.nl.nrows, ncols=ana.nl.ncols,
                                      figsize=ana.nl.figsize)

        ### DRAW AXES
        ######################################################################
        print(axes)
        print(targ_members)
        quit()
        ax_ind = 0
        for mem_key,member in targ_members.items():
            print(mem_key)
            print(ax_ind)
            ax = PO.get_axis(ax_ind, order='cols')
            print(ax)
            ana.draw_axis(PO, {mem_key:member}, ax)
            ax_ind += 1
        #ax_ind = 0
        #ax = PO.get_axis(ax_ind, order='cols')
        #ana.draw_axis(PO, targ_members, ax)

        #### FINAL FORMATTING
        #######################################################################
        PO.remove_axis_labels()
        ##PO.add_panel_labels(order='cols',
        ##                start_ind=ana.nl.nlp['panel_labels_start_ind'],
        ##                shift_right=ana.nl.nlp['panel_labels_shift_right'],
        ##                shift_up=ana.nl.nlp['panel_labels_shift_up'],
        ##                fontsize=ana.nl.nlp['panel_labels_fontsize'])
        #fig.subplots_adjust(**ana.nl.arg_subplots_adjust)
        PO.finalize_plot()
        timer.stop('plot')

    timer.print_report()
