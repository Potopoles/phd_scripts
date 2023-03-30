#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Create spatial mean time line plots.
author			Christoph Heim
date created    21.11.2020
date changed    05.04.2022
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
from package.utilities import Timer, area_weighted_mean_lat_lon
from package.nl_variables import nlv, get_plt_fact, get_plt_units
from package.time_processing import Time_Processing as TP
from package.plot_functions import PlotOrganizer
from package.functions import import_namelist, loc_to_var_name, MEM_OPER_SEP
from package.mp import TimeStepMP
###############################################################################

class Analysis_09(Analysis):

    def __init__(self, nl):
        super(Analysis_09, self).__init__(nl)
        self.nl = nl
        self.ana_number = 9


    def draw_axis(self, PO, members, ax):
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
        time_key = self.nl.nlp['time_key'][agg_level]
        if self.nl.nlp['xlim'][agg_level] is not None:
            ax.set_xlim(self.nl.nlp['xlim'][agg_level])

        # set xaxis locator/formatter
        locator = self.nl.nlp['tick_locator'][agg_level]
        if time_key == 'time':
            ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
        else:
            ax.xaxis.set_major_locator(locator)


        ### ITERATE THROUGH MEMBERS FOR PLOTTING
        ##########################################################################
        mem_ind = 0
        for mem_key,member in members.items():
            #del member.mem_dict['dates']
            #print(member.mem_dict)
            print(mem_key)
            #quit()
            # skip this member if it is part of a spread interval
            if 'spread' in member.mem_dict:
                continue
            raw_mem_key = mem_key.split('#time#')[0]

            ### MEMBER SPECIFIC PROPERTIES
            ######################################################################
            ### color
            if self.nl.ref_key is not None and self.nl.ref_key in mem_key: 
                color = self.nl.nlp['ref_color']
                zorder = 3
            elif self.nl.ref2_key is not None and self.nl.ref2_key in mem_key: 
                color = self.nl.nlp['ref2_color']
                zorder = 2
            else:
                if raw_mem_key in self.nl.nlp['mem_colors']: 
                    color = self.nl.nlp['mem_colors'][raw_mem_key]
                elif member.mem_dict['label'] in self.nl.nlp['mem_colors']: 
                    color = self.nl.nlp['mem_colors'][member.mem_dict['label']]
                else:
                    color = '#BBBBBB'
                zorder = 1

            ### linestyle
            if self.nl.ref_key is not None and self.nl.ref_key in mem_key: 
                linestyle = self.nl.nlp['ref_linestyle']
            elif self.nl.ref2_key is not None and self.nl.ref2_key in mem_key: 
                linestyle = self.nl.nlp['ref2_linestyle']
            elif raw_mem_key in self.nl.nlp['mem_linestyles']: 
                linestyle = self.nl.nlp['mem_linestyles'][raw_mem_key]
            elif member.mem_dict['label'] in self.nl.nlp['mem_linestyles']: 
                linestyle = self.nl.nlp['mem_linestyles'][member.mem_dict['label']]
            else:
                linestyle = '-'

            if 'zorder' in member.mem_dict:
                zorder = member.mem_dict['zorder']

            #print(mem_key)
            #print(member.mem_dict['label'])
            #print(linestyle)

            ### ITERATE THROUGH AGGREGATED VARIABLES FOR PLOTTING
            ######################################################################
            for agg_var_name,var in member.vars.items():
                var_name = TP.get_var_name(agg_var_name)
                agg_level = TP.get_agg_level(agg_var_name)
                agg_operator = TP.get_agg_operator(agg_var_name)
                if agg_operator not in self.nl.plot_lines[agg_level]:
                    continue

                plot_var = var*get_plt_fact(var_name)
                if self.nl.i_subtract_mean:
                    plot_var_mean = plot_var.mean().values
                    print(plot_var_mean)
                    plot_var -= plot_var_mean
                    print()

                if var_name in self.nl.nlp['ylims'][member.val_type]:
                    ax.set_ylim(self.nl.nlp['ylims'][member.val_type][var_name])


                ### DRAW PLOT
                ##################################################################

                ## this is for vertical profiles: TODO
                #if 'alt' in mem_var[TP.MEAN].dims:
                #    raise NotImplementedError()
                #else:

                if agg_operator in self.nl.nlp['linewidths'][agg_level]:
                    linewidth = self.nl.nlp['linewidths'][agg_level][agg_operator]
                    markersize = self.nl.nlp['markersize'][agg_level][agg_operator]
                else:
                    linewidth = 0.5
                    markersize = 0

                handle, = ax.plot(var[time_key], 
                                plot_var.values,
                                marker='o', color=color,
                                linewidth=linewidth,
                                linestyle=linestyle,
                                markersize=markersize,
                                label=member.mem_dict['label'],
                                zorder=zorder)
                if agg_operator == TP.MEAN:
                    PO.handles.append(handle)

            ### PLOT SPREAD INTERVAL
            ######################################################################
            if (
                (self.nl.agg_level in self.nl.plot_spread) and 
                (raw_mem_key not in self.nl.nlp['hide_spread_mem_key'])
            ):
                lower_var_name = TP.get_agg_var_name(self.nl.var_names[0],
                        self.nl.agg_level,
                        agg_operator=self.nl.plot_spread[self.nl.agg_level][0])
                upper_var_name = TP.get_agg_var_name(self.nl.var_names[0], 
                        self.nl.agg_level,
                        agg_operator=self.nl.plot_spread[self.nl.agg_level][1])

                upper_vals = member.vars[upper_var_name]
                lower_vals = member.vars[lower_var_name]

                upper_vals *= get_plt_fact(var_name)
                lower_vals *= get_plt_fact(var_name)

                if self.nl.i_subtract_mean:
                    upper_vals -= plot_var_mean
                    lower_vals -= plot_var_mean

                # if spread interval is shown for difference member, make
                # sure that it still covers the entire spread.
                if member.val_type == 'diff':
                    upper_vals = np.maximum(lower_vals, upper_vals)
                    lower_vals = np.minimum(lower_vals, upper_vals)

                ax.fill_between(member.vars[lower_var_name][time_key],
                                lower_vals, upper_vals,
                                color='{}{}'.format(color,
                                            self.nl.nlp['spread']['opacity']),
                                linewidth=self.nl.nlp['spread']['linewidth'])

            mem_ind += 1

        ### PLOT MEMBER SPREAD INTERVALS
        ######################################################################
        for spread_ind in range(3):
            #print(spread_ind)
            spread_members = {}
            for mem_key,member in members.items():
                if 'spread' in member.mem_dict:
                    if member.mem_dict['spread'][0] == spread_ind:
                        spread_members[member.mem_dict['spread'][1]] = (mem_key,member)

            # if no spread member was found skip this part
            if len(spread_members) == 0:
                break

            agg_var_name = TP.get_agg_var_name(self.nl.var_names[0],
                    self.nl.agg_level,
                    agg_operator='MEAN')

            plot_vals = {}
            for spread_key in ['upper','lower']:
                plot_vals[spread_key] = spread_members[spread_key][1].vars[agg_var_name]
                plot_vals[spread_key] *= get_plt_fact(var_name)

                if self.nl.i_subtract_mean:
                    mem_key = spread_members[spread_key][0]
                    #print(mem_key)
                    ## if this is a percentile (PERC) spread, subtract mean of MEAN member
                    if MEM_OPER_SEP in mem_key:
                        mean_mem_key = ''
                        for s in mem_key.split(MEM_OPER_SEP):
                            if 'endperc' in s:
                                mean_mem_key += 'endmean'
                            elif 'perc' in s:
                                mean_mem_key += 'mean'
                            else:
                                mean_mem_key += s
                            mean_mem_key += MEM_OPER_SEP
                        mean_mem_key = mean_mem_key[:-1]
                        #print(mean_mem_key)
                        plot_vals[spread_key] -= (
                            members[mean_mem_key].vars[agg_var_name].mean() * 
                            get_plt_fact(var_name)
                        )

            # if spread interval is shown for difference member, make
            # sure that it still covers the entire spread.
            if member.val_type == 'diff':
                plot_vals['upper'] = np.maximum(plot_vals['lower'], plot_vals['upper'])
                plot_vals['lower'] = np.minimum(plot_vals['lower'], plot_vals['upper'])

            ax.fill_between(spread_members['lower'][1].vars[agg_var_name][time_key],
                            plot_vals['lower'], 
                            plot_vals['upper'],
                            color='{}{}'.format(self.nl.nlp['mem_spread_colors'][spread_ind],
                                        self.nl.nlp['spread']['opacity']),
                            linewidth=self.nl.nlp['spread']['linewidth']
            )

        ### FINAL FORMAT AXIS
        ##########################################################################

        ## plot legend
        try:
            if self.nl.i_plot_legend:
                ax.legend(handles=PO.handles)
        # if i_plot_legend not specified in namelist, just plot it.
        except AttributeError:
            ax.legend(handles=PO.handles)

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
        ylim = ax.get_ylim()
        ax.set_ylim(ylim)

        if self.nl.i_draw_grid:
            ax.grid(axis='y')
        ax.axhline(y=0, color='k', linewidth=1, zorder=-3)

        #quit()


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


    #def compute_targ_members_for_time_series(self, src_members):
    #    for src_mem_key,src_member in src_members.items():
    #        #print(src_mem_key)
    #        #for var_name in self.nl.var_names:
    #        for var_name in list(src_member.vars.keys()):
    #            var = src_member.vars[var_name]
    #            for agg_operator in self.nl.agg_operators:
    #                #print(agg_operator)
    #                agg_var_name = TP.get_agg_var_name(var_name,
    #                                    self.nl.agg_level, agg_operator)
    #                agg_var = TP.aggregate(var, self.nl.agg_level,
    #                                        agg_operator)
    #                src_members[src_mem_key].vars[agg_var_name] = agg_var
    #            #quit()

    #            ### INDIVIDUAL YEARS FOR ANNUAL CYCLE
    #            if self.nl.agg_level == TP.ANNUAL_CYCLE:
    #                # first compute monthly mean values
    #                monthly_var = TP.run_aggregation_step(var, 
    #                      { TP.ACTION:TP.RESAMPLE, 
    #                        TP.FREQUENCY:'M', 
    #                        TP.OPERATOR:TP.MEAN })
    #                # split up src_member var into multiple vars containing the
    #                # individual years
    #                #print(monthly_var)
    #                #quit()
    #                ymon_vars = TP.run_aggregation_step(monthly_var, 
    #                                      { TP.ACTION:TP.GROUPBY, 
    #                                        TP.FREQUENCY:'Y',
    #                                        TP.OPERATOR:None })
    #                for year,ymon_var in ymon_vars.items():
    #                    ymon_var_name = TP.get_agg_var_name(var_name, 
    #                                        self.nl.agg_level, year)
    #                    # convert datetime to month 
    #                    months = ymon_var['time.month']
    #                    ymon_var = ymon_var.rename(time='month')
    #                    ymon_var = ymon_var.assign_coords(month=months.values)
    #                    ### make sure month 1 is there..
    #                    ##if 1 not in months:
    #                    ##    month_1 = xr.DataArray(np.nan, [('month', [1])])
    #                    ##    var = xr.concat([month_1, var], dim='month')
    #                    src_member.vars[ymon_var_name] = ymon_var

    #            # delete unaggregated variable
    #            del src_members[src_mem_key].vars[var_name]


    def prepare_namelist(self):

        # find all aggregation operators that should be computed
        # this may lead to NotImplementedError in time_processing.py
        agg_operators = []
        agg_operators.extend(self.nl.plot_lines[self.nl.agg_level])
        if self.nl.agg_level in self.nl.plot_spread:
            agg_operators.extend(self.nl.plot_spread[self.nl.agg_level])
        self.nl.agg_operators = list(set(agg_operators))

        # aggregated var names for loading
        self.nl.load_agg_var_names = []
        for var_name in self.nl.var_names:
            for agg_operator in self.nl.agg_operators:
                agg_var_name = TP.get_agg_var_name(var_name, 
                            self.nl.agg_level, agg_operator)
                self.nl.load_agg_var_names.append(agg_var_name)

        self.prepare_namelist_DEFAULT()       

        ## add individual years in time period
        ## to nl.plot_lines list for plotting....
        #if self.nl.agg_level == TP.ANNUAL_CYCLE:
        #    years = np.unique(pd.DatetimeIndex(self.nl.dates).year).astype(str)
        #    self.nl.plot_lines[self.nl.agg_level].extend(years)
        #    # ... and for loading
        #    for var_name in self.nl.var_names:
        #        for year in years:
        #            agg_var_name = TP.get_agg_var_name(var_name,
        #                            self.nl.agg_level, year)
        #            self.nl.load_agg_var_names.append(agg_var_name)

    

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
    import nl_09 as nl_ana_raw
    from nl_plot_09 import nlp
    ana = Analysis_09(nl=SimpleNamespace())
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
        PO.finalize_plot()
        timer.stop('plot')

    timer.print_report()
