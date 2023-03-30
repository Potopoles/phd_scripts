#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Compute scaling
author			Christoph Heim
date created    31.05.2022
date changed    31.05.2022
usage           args:
"""
###############################################################################
import os, argparse
import numpy as np
import xarray as xr
import pandas as pd
from types import SimpleNamespace
from pathlib import Path
from scipy.stats import linregress
from an_super import Analysis
from package.utilities import Timer, area_weighted_mean_lat_lon
from package.time_processing import Time_Processing as TP
from package.nl_variables import nlv, get_plt_fact, get_plt_units
from package.plot_functions import PlotOrganizer
from package.functions import import_namelist
from package.mp import TimeStepMP
from package.member import Member
###############################################################################

class Analysis_18(Analysis):

    def __init__(self, nl):
        super(Analysis_18, self).__init__(nl)
        self.nl = nl
        self.ana_number = 18


    def draw_axis(self, PO, members, ax):
        print(members)
        rel_agg_var_name = TP.get_agg_var_name(self.nl.rel_var_name, self.nl.agg_level)
        diff_agg_var_name = TP.get_agg_var_name(self.nl.diff_var_name, self.nl.agg_level)
        print('dprec {:4.2f}%, dT {:4.1f}, dprec/dT {:4.2f}%'.format(
            members[self.nl.rel_mem_key].vars[rel_agg_var_name].values*100,
            members[self.nl.diff_mem_key].vars[diff_agg_var_name].values,
            members[self.nl.rel_mem_key].vars[rel_agg_var_name].values*100 / 
            members[self.nl.diff_mem_key].vars[diff_agg_var_name].values))
        quit()



    def compute_var(self, var):
        # average horizontally
        var = area_weighted_mean_lat_lon(var)
        #var = var.mean(dim=['lon', 'lat'])

        # resample to daily mean values if required.
        if self.nl.agg_level not in [TP.HOURLY_SERIES, TP.DIURNAL_CYCLE]:
            var = TP.run_aggregation_step(var, 
                      { TP.ACTION:TP.RESAMPLE, 
                        TP.FREQUENCY:'D', 
                        TP.OPERATOR:TP.MEAN  })
        return(var)



    def prepare_namelist(self):

        self.prepare_namelist_DEFAULT()       

        ## ATTENTION: has to be run after prepare_namelist_DEFAULT!
        for var_name in self.nl.var_names:
            self.nl.var_dom_map[var_name] = self.nl.overwrite_var_dom_map[var_name]


    

if __name__ == '__main__':

    # READ INPUT ARGUMENTS
    ###########################################################################
    parser = argparse.ArgumentParser(description = 'Compute mean value and scale.')
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
    import nl_18 as nl_ana_raw
    from nl_plot_18 import nlp
    ana = Analysis_18(nl=SimpleNamespace())
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
        ana.save_data(ana.indiv_targ_members)
        
    # ... or be reloaded from precomputed pickle files.
    else:
        # LOAD PRECOMPUTED DATA FROM PICKLE
        ######################################################################
        ana.indiv_targ_members = ana.load_data()

    # PLOTTING
    ##########################################################################
    if ana.nl.i_plot:
        timer.start('prepare')
        targ_members = ana.prepare_for_plotting(ana.indiv_targ_members)
        timer.stop('prepare')

        ## SET UP PLOT IO PATH
        ######################################################################
        timer.start('plot')

        name_dict = {}
        name_dict['crf']   = ana.nl.agg_level 
        name_dict[ana.nl.main_domain['key']] = ''
        if ana.nl.plot_append != '':
            name_dict[ana.nl.plot_append] = ''

        ## INITIALIZE PLOT
        ######################################################################
        PO = PlotOrganizer(i_save_fig=ana.nl.i_save_fig,
                            path=ana.nl.plot_base_dir,
                            name_dict=name_dict, nlp=ana.nl.nlp,
                            geo_plot=ana.nl.nlp['geo_plot'])
        fig,axes = PO.initialize_plot(nrows=ana.nl.nrows, ncols=ana.nl.ncols,
                                      figsize=ana.nl.figsize,
                                      args_subplots_adjust=ana.nl.arg_subplots_adjust)

        ### DRAW AXES
        ######################################################################
        ax_ind = 0
        ax = PO.get_axis(ax_ind, order='cols')
        ana.draw_axis(PO, targ_members, ax)

        ### FINAL FORMATTING
        ######################################################################
        PO.remove_axis_labels()
        #PO.add_panel_labels(order='cols',
        #                start_ind=ana.nl.nlp['panel_labels_start_ind'],
        #                shift_right=ana.nl.nlp['panel_labels_shift_right'],
        #                shift_up=ana.nl.nlp['panel_labels_shift_up'],
        #                fontsize=ana.nl.nlp['panel_labels_fontsize'])
        fig.subplots_adjust(**ana.nl.arg_subplots_adjust)
        PO.finalize_plot()
        timer.stop('plot')

    timer.print_report()
