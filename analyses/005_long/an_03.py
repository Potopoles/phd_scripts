#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Create scatter plot
author			Christoph Heim
date created    25.11.2019
date changed    17.11.2021
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
from package.plot_functions import PlotOrganizer
from package.functions import import_namelist
from package.mp import TimeStepMP
from package.member import Member
###############################################################################

class Analysis_03(Analysis):

    def __init__(self, nl):
        super(Analysis_03, self).__init__(nl)
        self.nl = nl
        self.ana_number = 3


    def draw_axis(self, ts, members, ax):
        self.draw_axis_DEFAULT(ax)

        ### FORMAT MEMBERS FOR PLOTTING
        ##########################################################################
        for mem_key,member in members.items():
            #print(mem_key)
            for agg_var_name,var in member.vars.items():
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
        #ax.grid(axis='y')

        ### ITERATE THROUGH MEMBERS FOR PLOTTING
        ##########################################################################
        mem_ind = 0
        line_x_val = None
        for mem_key,member in members.items():
            #print(mem_key)

            ### MEMBER SPECIFIC PROPERTIES
            ######################################################################
            ### colors for specific member groups
            color = 'k'
            markersize = self.nl.nlp['markersize'][agg_level]

            for mem_grp_key,mem_grp in self.nl.mem_groups.items():
                if member.mem_dict['label'] in mem_grp:
                    color = self.nl.nlp['mem_group_colors'][mem_grp_key]
                    break

            if member.mem_dict['label'] in self.nl.nlp['mem_colors']:
                color = self.nl.nlp['mem_colors'][member.mem_dict['label']]
                markersize = 30


            ### ITERATE THROUGH AGGREGATED VARIABLES FOR PLOTTING
            ######################################################################
            agg_var_name_1 = list(member.vars.keys())[0]
            agg_var_name_2 = list(member.vars.keys())[1]
            plot_var_1 = member.vars[agg_var_name_1].values
            plot_var_2 = member.vars[agg_var_name_2].values

            # TODO For paper figure
            plot_var_1 = (member.vars[agg_var_name_1] / member.vars[agg_var_name_2]).values

            if member.mem_dict['mod'] in self.nl.ecs: 
                plot_var_2 = self.nl.ecs[member.mem_dict['mod']]
            else:
                if member.mem_dict['label'] == self.nl.line_member:
                    line_x_val = plot_var_1.item()
                continue
            # TODO For paper figure

            # in case no data is available:
            if (plot_var_1 is None) or (plot_var_2 is None):
                continue

            #var_name_1 = TP.get_var_name(agg_var_name_1)
            #var_name_2 = TP.get_var_name(agg_var_name_2)
            #agg_level = TP.get_agg_level(agg_var_name_1)
            #agg_operator = TP.get_agg_operator(agg_var_name_1)
            ##if agg_operator not in self.nl.plot_lines[agg_level]:
            ##    continue

            #if var_name_1 in self.nl.nlp['axlims']:
            #    ax.set_xlim(self.nl.nlp['axlims'][var_name_1])
            #if var_name_2 in self.nl.nlp['axlims']:
            #    ax.set_ylim(self.nl.nlp['axlims'][var_name_2])

            #print(plot_var_2)
            #quit()


            ### DRAW PLOT
            ##################################################################

            #print(plot_var_1.values)
            #print(plot_var_2.values)
            handle = ax.scatter(plot_var_1, plot_var_2,
                            color=color,
                            s=markersize,
                            label=member.mem_dict['label'])
            if member.mem_dict['label'] not in self.nl.no_legend_mem_keys: 
                PO.handles.append(handle)

            #### PLOT SPREAD INTERVAL
            #######################################################################
            #if self.nl.agg_level in self.nl.plot_spread:
            #    lower_var_name = TP.get_agg_var_name(self.nl.var_names[0],
            #            self.nl.agg_level,
            #            agg_operator=self.nl.plot_spread[self.nl.agg_level][0])
            #    upper_var_name = TP.get_agg_var_name(self.nl.var_names[0], 
            #            self.nl.agg_level,
            #            agg_operator=self.nl.plot_spread[self.nl.agg_level][1])
            #    # if spread interval is shown for difference member, make
            #    # sure that it still covers the entire spread.
            #    if member.val_type == 'diff':
            #        upper_vals = np.maximum(member.vars[lower_var_name],
            #                                member.vars[upper_var_name])
            #        lower_vals = np.minimum(member.vars[lower_var_name],
            #                                member.vars[upper_var_name])
            #        member.vars[upper_var_name] = upper_vals
            #        member.vars[lower_var_name] = lower_vals
            #    ax.fill_between(member.vars[lower_var_name],
            #                    member.vars[lower_var_name].values,
            #                    member.vars[upper_var_name].values,
            #                    color='{}{}'.format(color, '40'), linewidth=0.5)

            mem_ind += 1


        #### DRAW REGRESSION LINE
        ###########################################################################
        for mem_group_key,mem_group in self.nl.mem_groups.items():
            if mem_group_key not in self.nl.nlp['regression_mem_groups']:
                continue
            xvals = []
            yvals = []
            for mem_key,member in members.items():
                print(member.mem_dict['label'])
                if member.mem_dict['label'] in mem_group:
                    agg_var_name_1 = list(member.vars.keys())[0]
                    agg_var_name_2 = list(member.vars.keys())[1]
                    plot_var_1 = member.vars[agg_var_name_1].values
                    plot_var_2 = member.vars[agg_var_name_2].values

                    # TODO For paper figure
                    plot_var_1 = (member.vars[agg_var_name_1] / member.vars[agg_var_name_2]).values
                    if member.mem_dict['mod'] in self.nl.ecs: 
                        plot_var_2 = self.nl.ecs[member.mem_dict['mod']]
                    else:
                        continue
                    # TODO For paper figure

                    if (plot_var_1 is not None) and (plot_var_2 is not None):
                        xvals.append(plot_var_1)
                        yvals.append(plot_var_2)
                        #print('{} {} {}'.format(agg_var_name_1, mem_key, xvar.values))
                        #print('{} {} {}'.format(agg_var_name_2, mem_key, yvar.values))
            xvals = np.asarray(xvals)
            yvals = np.asarray(yvals)
            slope,intercept,r_val,pval,std_err = linregress(xvals, yvals)
            print('{} pval {}'.format(mem_group_key, pval))
            print('{} R2 {}'.format(mem_group_key, r_val**2))
            if pval < self.nl.pval_regression:
                xmin = np.min(xvals)*1.1
                xmax = np.max(xvals)*1.1
                ymin = np.min(slope*xmin + intercept)
                ymax = np.max(slope*xmax + intercept)
                ax.plot([xmin,xmax],[ymin,ymax],
                        color=self.nl.nlp['mem_group_colors'][mem_group_key],
                        linewidth=self.nl.nlp['regr_linewidth'])


                if line_x_val is not None:
                    line_y_val = slope*line_x_val + intercept
                    print(line_x_val)
                    print(line_y_val)
                    ax.plot([np.min(xvals)*1.1,line_x_val], [line_y_val,line_y_val], color='red',
                        linestyle='--')
                    ax.plot([line_x_val,line_x_val], [np.min(yvals)*0.9,line_y_val], color='red')

                    ax.set_xlim(xmin, xmax)
                    ax.set_ylim(ymin*0.9, ymax*1.1)

                if self.nl.uncertainty_range_xvals is not None:
                    x_min = self.nl.uncertainty_range_xvals[0]
                    x_max = self.nl.uncertainty_range_xvals[1]
                    y_min = slope*x_min + intercept
                    y_max = slope*x_max + intercept
                    ax.fill_between(
                        [x_min, x_max], [y_min,y_max], 
                        facecolor='red', alpha=0.3
                    )
                    #ax.fill_between(
                    #    [xmin, x_min], [y_max,y_max], [y_min,y_min], 
                    #    facecolor='red', alpha=0.3
                    #)
                    #ax.fill_between(
                    #    [x_min, x_max], [y_max,y_max], [y_min,y_max], 
                    #    facecolor='red', alpha=0.3
                    #)
                    #ax.fill_between([0, x_min], [y_max,y_max], [y_min,y_min], color='red', alpha=0.3)
                    #ax.plot([line_x_val,line_x_val], [np.min(yvals)*0.9,line_y_val], color='red')




        #### FORMAT AXIS
        ###########################################################################
        if len(PO.handles):
            ax.legend(handles=PO.handles)
        #ax.set_title(nlv[nl.args.var_name]['label'])
        PO.set_axes_labels(ax, self.nl.var_names[0], self.nl.var_names[1])
        # add domain specification to axis labels
        #ax.set_xlabel('{}: {}'.format(
        #        self.nl.var_dom_map[self.nl.var_names[0]]['label'], 
        #        ax.get_xlabel()))
        #ax.set_ylabel('{}: {}'.format(
        #        self.nl.var_dom_map[self.nl.var_names[1]]['label'], 
        #        ax.get_ylabel()))
        ax.set_ylabel('ECS [$K$]')
        ax.set_xlabel('ATL CRF [$W$ $m^{-2}$ $K^{-1}$]')



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

        ## find all aggregation operators that should be computed
        ## this may lead to NotImplementedError in time_processing.py
        #agg_operators = []
        #agg_operators.extend(self.nl.plot_lines[self.nl.agg_level])
        #if self.nl.agg_level in self.nl.plot_spread:
        #    agg_operators.extend(self.nl.plot_spread[self.nl.agg_level])
        #self.nl.agg_operators = list(set(agg_operators))
        #
        ## aggregated var names for loading
        #self.nl.load_agg_var_names = []
        #for var_name in self.nl.var_names:
        #    for agg_operator in self.nl.agg_operators:
        #        agg_var_name = TP.get_agg_var_name(var_name, 
        #                    self.nl.agg_level, agg_operator)
        #        self.nl.load_agg_var_names.append(agg_var_name)

        
        self.prepare_namelist_DEFAULT()       

        ## ATTENTION: has to be run after prepare_namelist_DEFAULT!
        for var_name in self.nl.var_names:
            self.nl.var_dom_map[var_name] = self.nl.overwrite_var_dom_map[var_name]


    

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
    import nl_03 as nl_ana_raw
    from nl_plot_03 import nlp
    ana = Analysis_03(nl=SimpleNamespace())
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

        ## SET UP PLOT IO PATH
        ######################################################################

        name_dict = {}
        name_dict['corr']   = ana.nl.agg_level 
        name_dict[ana.nl.var_names[0]] = ana.nl.var_dom_map[
                                                ana.nl.var_names[0]]['key']
        name_dict[ana.nl.var_names[1]] = ana.nl.var_dom_map[
                                                ana.nl.var_names[1]]['key']
        if ana.nl.plot_append != '':
            name_dict[ana.nl.plot_append] = ''
        timer.stop('prepare')

        ## INITIALIZE PLOT
        ######################################################################
        timer.start('plot')
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
