#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Create cloud radiative feedback plot
author			Christoph Heim
date created    04.03.2022
date changed    11.05.2022
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

class Analysis_17(Analysis):

    def __init__(self, nl):
        super(Analysis_17, self).__init__(nl)
        self.nl = nl
        self.ana_number = 17


    def draw_axis(self, PO, members, ax):
        self.draw_axis_DEFAULT(ax)

        vars_values = {}

        ### SCALE VARIABLES BY SCALING VARIABLE
        ##########################################################################
        for mem_key,member in members.items():
            #print(mem_key)
            # find scale var value
            scale_val = None
            for agg_var_name,var in member.vars.items():
                var_name = TP.get_var_name(agg_var_name)

                if var_name == self.nl.scale_var_name:
                    scale_val = var.mean(dim='time').values * get_plt_fact(var_name)
                    print(mem_key)
                    print('dT: {}'.format(scale_val))

            # ensure scale value is found
            if scale_val is None:
                raise ValueError()

            #for agg_var_name,var in member.vars.items():
            #    var_name = TP.get_var_name(agg_var_name)
            #    print('{} {}'.format(var_name, member.vars[agg_var_name].mean().values))

            # get other variables and scale them
            for agg_var_name,var in member.vars.items():
                var_name = TP.get_var_name(agg_var_name)
                if var_name != self.nl.scale_var_name:
                    member.vars[agg_var_name] /= scale_val 
                    #print(member.vars[agg_var_name])

            # delete scaling variable
            for agg_var_name,var in member.vars.items():
                var_name = TP.get_var_name(agg_var_name)
                if var_name == self.nl.scale_var_name:
                    del members[mem_key].vars[agg_var_name]
                    break


        #quit()

        ### FORMAT MEMBERS FOR PLOTTING
        ##########################################################################
        # aggregate data for boxplots
        #print(members['|diff|COSMO_3.3_pgw#time#20070101-20101231-gap0#+++#COSMO_3.3_ctrl#time#20070101-20101231-gap0|enddiff|'].vars.keys())
        #print(members.items())
        #quit()
        for mem_key,member in members.items():

            # is this a cmip6 member?
            is_cmip6_member = False
            for mod_key in self.nl.models_cmip6:
                if mod_key in mem_key:
                    is_cmip6_member = True
                    break

            # only aggregate data for cmip6 members 
            if is_cmip6_member:
                # get variables 
                for agg_var_name,var in member.vars.items():
                    var_name = TP.get_var_name(agg_var_name)

                    value = var.mean(dim='time').values * get_plt_fact(var_name)
                    if var_name not in vars_values.keys():
                        vars_values[var_name] = [value]
                    else:
                        vars_values[var_name].append(value)


        ### make boxplot
        ######################################################################
        if len(vars_values) > 0:
            data_list = []
            var_labels = []
            for var_name,values in vars_values.items():
                data_list.append(values)
                #var_labels.append(nlv[var_name]['label'])
                if var_name in ['SWNDTOA', 'CSWNDTOA', 'CRESWNDTOA']:
                    var_labels.append('SW')
                elif var_name in ['LWDTOA', 'CLWDTOA', 'CRELWDTOA']:
                    var_labels.append('LW')
                elif var_name in ['RADNDTOA', 'CRADNDTOA', 'CRERADNDTOA']:
                    var_labels.append('TOT')
                elif var_name in ['PP']:
                    var_labels.append('precip.')
                else:
                    raise ValueError()
            boxplot_result = ax.boxplot(data_list, labels=var_labels,
                whis=[5,95],
                meanline=True,
                showmeans=True,
                medianprops=dict(color='k', linewidth=0),
                meanprops=dict(color='k', linewidth=1.25, linestyle='-'),
                )
            print('#############################################################')
            print('CMIP6-EM:')
            print('#############################################################')
            #print(boxplot_result)
            print([np.mean(var) for var in data_list])
            print('#############################################################')

        ### add individual lines for some members
        ######################################################################
        line_width = 1./4.
        for mem_key,member in members.items():
            print(mem_key)
            # is this a line member?
            is_line_member = False
            for line_mem_key,line_cfg in self.nl.line_mem_cfg.items():
                if line_mem_key in mem_key:
                    is_line_member = True
                    label = line_cfg['label']
                    is_yearly_line_member = line_cfg['yearly']
                    break

            if is_line_member:
                var_ind = 1
                for agg_var_name,var in member.vars.items():
                    var_name = TP.get_var_name(agg_var_name)

                    alltime_mean = var.mean(dim='time').values * get_plt_fact(var_name)
                    yearly_means = var.values * get_plt_fact(var_name)

                    print(var_name, '{:4.2f}'.format(alltime_mean))

                    ### plot all-time mean value
                    handle, = ax.plot(
                        [var_ind-line_width,var_ind+line_width], 
                        [alltime_mean, alltime_mean], color=line_cfg['color'],
                        label=label)
                    if var_ind == 1:
                        PO.handles.append(handle)

                    ### plot yearly mean values
                    if is_yearly_line_member:
                        for yearly_mean in yearly_means:
                            ax.plot(
                                [var_ind-line_width,var_ind+line_width], 
                                [yearly_mean, yearly_mean], color=line_cfg['color'],
                                linewidth=0.5,
                                label=label)

                    var_ind += 1



        ### format axis
        ######################################################################
        ax.legend(handles=PO.handles)
        unit = '[W $m^{-2}$ $K^{-1}$]'
        label = 'feedback {}'.format(unit)
        ax.set_ylabel(label)

        ax.axhline(y=0, color='k', linewidth=0.5)


        ## add lines after var groups
        member = members[list(members.keys())[0]]
        var_ind = 1
        for agg_var_name,var in member.vars.items():
            var_name = TP.get_var_name(agg_var_name)
            if var_name in self.nl.var_group_cfg.keys():
                ax.axvline(x=var_ind - 1/2, color='k', linewidth=0.5)
                ax.text(x=var_ind - 1/4, y = 1.7, s=self.nl.var_group_cfg[var_name])
            var_ind += 1

        ## add horizontal auxiliary lines
        for y in range(-5,5):
            ax.axhline(y=y, linewidth=0.2, zorder=-1, color='k')

        ## ylimit
        ax.set_ylim((-1.8,2.2))


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
        
        #if self.nl.i_recompute == 0:
        self.nl.var_names = [
            'SWNDTOA',
            'LWDTOA', 
            'RADNDTOA',
            'CSWNDTOA', 
            'CLWDTOA', 
            'CRADNDTOA',
            'CRESWNDTOA', 
            'CRELWDTOA', 
            'CRERADNDTOA',
        ]

        # add scale variable to var_name
        if self.nl.scale_var_name is not None:
            if self.nl.i_recompute == 0:
                self.nl.var_names.append(self.nl.scale_var_name)

        ### TODO tmp
        #self.nl.var_names = [self.nl.scale_var_name]

        self.prepare_namelist_DEFAULT()       

        ## ATTENTION: has to be run after prepare_namelist_DEFAULT!
        for var_name in self.nl.var_names:
            self.nl.var_dom_map[var_name] = self.nl.overwrite_var_dom_map[var_name]


    

if __name__ == '__main__':

    # READ INPUT ARGUMENTS
    ###########################################################################
    parser = argparse.ArgumentParser(description = 'Draw timeline plots.')
    ## variable to plot
    #parser.add_argument('var_names', type=str)
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
    import nl_17 as nl_ana_raw
    from nl_plot_17 import nlp
    ana = Analysis_17(nl=SimpleNamespace())
    import_namelist(ana.nl, nl_ana_raw)
    ana.nl.nlp = nlp

    # input arguments
    ana.nl.i_recompute = args.i_recompute
    ana.nl.i_save_fig = args.i_save_fig
    ana.nl.n_par = args.n_par
    #ana.nl.var_names = args.var_names.split(',')
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
        #print(ana.indiv_targ_members['COSMO_3.3_pgw#time#20070101-20101231-gap0'].vars.keys())
        #quit()

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
        fig,axes = PO.initialize_plot(
            nrows=ana.nl.nrows, 
            ncols=ana.nl.ncols,
            figsize=ana.nl.figsize,
            args_subplots_adjust=ana.nl.arg_subplots_adjust
        )

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
        #fig.subplots_adjust(**ana.nl.arg_subplots_adjust)
        PO.finalize_plot()
        timer.stop('plot')

    timer.print_report()
