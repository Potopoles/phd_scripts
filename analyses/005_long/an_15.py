#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Plot quantity along latlon_sects.
dependencies    depends on:
author			Christoph Heim
date created    09.09.2021
date changed    23.09.2021
"""
###############################################################################
import os, argparse, copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from types import SimpleNamespace
from an_super import Analysis
from package.constants import CON_RAD_EARTH
from package.nl_variables import nlv, get_plt_units, get_plt_fact
from package.utilities import Timer
from package.time_processing import Time_Processing as TP
from package.plot_functions import PlotOrganizer
from package.functions import import_namelist, loc_to_var_name
from package.mp import TimeStepMP
###############################################################################

class Analysis_15(Analysis):

    def __init__(self, nl):
        super(Analysis_15, self).__init__(nl)
        self.nl = nl
        self.ana_number = 15


    def draw_axis(self, PO, members, ax):
        self.draw_axis_DEFAULT(ax)

        ### ITERATE LINE AXES
        ######################################################################
        handles = []
        ax_count = 0
        for ax_key,loc_var_names in self.nl.plot_dict.items():
            #print(ax_key)
            ### SELECT AND FORMAT LINE AXIS
            ##################################################################
            if ax_key == 'l1':
                cur_ax = ax
            elif ax_key == 'r1':
                cur_ax = ax.twinx()
            elif ax_key == 'r2':
                cur_ax = ax.twinx()
                cur_ax.spines["right"].set_position(("axes", 1.28))

            ax_color = self.nl.nlp['line_axes_colors'][ax_key][0]

            cur_ax.yaxis.label.set_color(ax_color)
            cur_ax.spines['right'].set_edgecolor(ax_color)
            cur_ax.tick_params(axis='y', colors=ax_color)

            cur_ax.axhline(y=0, color=ax_color, linewidth=0.5)
            #if member.val_type == 'abs':
            #    cur_ax.axhline(y=0, color=color, linewidth=0.5)

            ax.set_xlim((self.nl.plot_domain[self.nl.line_along].start,
                         self.nl.plot_domain[self.nl.line_along].stop))

            PO.set_axes_labels(ax, x_var_name=self.nl.cs_x_coord)

            ### DRAW PLOT LINES
            ##################################################################
            ax_var_count = 0
            p90_rel = 0.1
            for loc_var_name in loc_var_names:
                var_name = loc_to_var_name(loc_var_name)
                mem_count = 0
                for mem_key,member in members.items():
                    mem_dict = copy.copy(members[mem_key].mem_dict)
                    agg_loc_var_name = TP.get_agg_var_name(loc_var_name,
                                                self.nl.agg_level,
                                                self.nl.agg_operators[0])

                    if member.vars[agg_loc_var_name] is not None:
                        if 'rel' not in member.val_type:
                            plot_var = (
                                member.vars[agg_loc_var_name] *
                                get_plt_fact(var_name)
                            )
                        else:
                            plot_var = member.vars[agg_loc_var_name] 

                        #print(loc_var_name)
                        #print(member.val_type)
                        #print(plot_var)

                        if var_name in self.nl.coarse_grain.keys():

                            dx_km = np.abs(np.diff(
                                plot_var[self.nl.line_along].values
                                ).mean()/180*np.pi*CON_RAD_EARTH/1000)
                            window = int(self.nl.coarse_grain[var_name]/dx_km)
                            plot_var = plot_var.coarsen({self.nl.line_along:window},
                                               #boundary='trim').mean()
                                               boundary='pad').mean()

                        ### format plot line
                        if 'linestyle' in mem_dict:
                            linestyle = mem_dict['linestyle']
                        else:
                            #linestyle = self.nl.nlp['linestyles'][mem_count]
                            #linestyle = self.nl.nlp['linestyles'][ax_var_count]
                            linestyle = self.nl.nlp['linestyles'][ax_count]

                        if 'color' in mem_dict:
                            color = mem_dict['color']
                        else:
                            color = self.nl.nlp['line_axes_colors'][ax_key][ax_var_count]

                        if 'linewidth' in mem_dict:
                            linewidth = mem_dict['linewidth']
                        else:
                            linewidth = 1


                        if 'label' in mem_dict:
                            label = mem_dict['label']
                        else:
                            if '@alt' in loc_var_name:
                                if len(loc_var_name.split(':')) == 1:
                                    label='{} {:2.1f}km'.format(
                                        nlv[var_name]['label'],
                                        float(loc_var_name.split('@alt=')[1])/1000
                                    )
                                else:
                                    label='{} {:2.1f}-{:2.1f}km'.format(
                                        nlv[var_name]['label'],
                                        float(loc_var_name.split('@alt=')[1].split(':')[0])/1000,
                                        float(loc_var_name.split('@alt=')[1].split(':')[1])/1000
                                    )
                            else:
                                label=nlv[var_name]['label']

                        ## draw plot line
                        #print(var_name)
                        #print(plot_var.values)
                        handle, = \
                                cur_ax.plot(
                                    (plot_var[self.nl.line_along] * 
                                        get_plt_fact(self.nl.cs_x_coord)),
                                    plot_var.squeeze().values,
                                    color=color,
                                    linewidth=linewidth,
                                    linestyle=linestyle,
                                    label=label)

                        p90_rel = max(np.nanquantile(np.abs(plot_var.values),0.92), p90_rel)

                        #if (len(loc_var_names) > 1) & (mem_count == 0):
                        #if mem_count == 0:
                        handles.append(handle)

                    mem_count += 1

                if ax_var_count == 0:
                    ax.grid(axis='y')

                ax_var_count += 1

                ### VAR SPECIFIC AXIS FORMATTING
                ##############################################################
                ## set y limits
                if 'rel' in member.val_type:
                    #pass
                    cur_ax.set_ylim(-0.6,0.6)
                    for prel in [0.1,0.2,0.3,0.4,0.5]:
                        if p90_rel <= prel:
                            cur_ax.set_ylim(-prel,prel)
                            break
                    for vn in [var_name,loc_var_name]:
                        if vn in self.nl.nlp['var_plt_cfgs']:
                            if 'rel' in self.nl.nlp['var_plt_cfgs'][vn]['lims']:
                                cur_ax.set_ylim(self.nl.nlp['var_plt_cfgs'][
                                        vn]['lims']['rel'])
                elif var_name in self.nl.nlp['var_plt_cfgs']:
                    for vn in [var_name,loc_var_name]:
                        if vn in self.nl.nlp['var_plt_cfgs']:
                            cur_ax.set_ylim(self.nl.nlp['var_plt_cfgs'][
                                    vn]['lims'][member.val_type])
                    #if loc_var_name in self.nl.nlp['var_plt_cfgs']:
                    #    cur_ax.set_ylim(self.nl.nlp['var_plt_cfgs'][
                    #                loc_var_name]['lims'][member.val_type])
                    #elif var_name in self.nl.nlp['var_plt_cfgs']:
                    #    cur_ax.set_ylim(self.nl.nlp['var_plt_cfgs'][
                    #                var_name]['lims'][member.val_type])

                if 'glabel' in nlv[var_name]:
                    PO.set_axes_labels(cur_ax, y_var_name=var_name, 
                                        y_val_type=member.val_type,
                                        overwrite=True,
                                        use_name='glabel')
                else:
                    PO.set_axes_labels(cur_ax, y_var_name=var_name, 
                                        y_val_type=member.val_type,
                                        overwrite=False)

                ### FORMAT AXIS
                ######################################################################
                if self.nl.title is None:
                    ax.set_title(mem_dict['label'])
                else:
                    ax.set_title(self.nl.title)

            ax_count += 1


        ### LEGEND
        ##################################################################
        if self.nl.i_plot_legend:
            ax.legend(handles=handles)

        try:
            ax.set_title(self.nl.title, x=0.50)
        except AttributeError:
            pass



    def compute_var(self, var):
        if self.nl.line_along == 'lat':
            at_dim = 'lon' 
        elif self.nl.line_along == 'lon':
            at_dim = 'lat' 

        # select either range or individual values
        if type(self.nl.line_at) == slice:
            var = var.sel({at_dim:self.nl.line_at})
        else:
            var = var.sel({at_dim:self.nl.line_at}, method='nearest')

        if 'alt' in var.dims:
            var = var.mean(dim='alt')

        # average accross at_dim
        if var[at_dim].values.size > 1:
            var = var.mean(dim=at_dim)

        if self.nl.agg_level not in [TP.HOURLY_SERIES, TP.DIURNAL_CYCLE]:
            var = TP.run_aggregation_step(var, 
                      { TP.ACTION:TP.RESAMPLE, 
                        TP.FREQUENCY:'D', 
                        TP.OPERATOR:TP.MEAN  })
        return(var)


    def prepare_namelist(self):
        if self.nl.line_along == 'lat':
            self.nl.cs_x_coord = 'COORD_LAT'
        elif self.nl.line_along == 'lon':
            self.nl.cs_x_coord = 'COORD_LON'

        self.nl.pickle_append = self.nl.line_along

        # determine var_names based on plot_dict given by user
        all_var_names = []
        for ax_key,var_names in self.nl.plot_dict.items():
            for var_name in var_names:
                if var_name not in all_var_names:
                    all_var_names.append(var_name)
        self.nl.var_names = all_var_names

        self.prepare_namelist_DEFAULT()



if __name__ == '__main__':
    # READ INPUT ARGUMENTS
    ###########################################################################
    parser = argparse.ArgumentParser(description = 'Draw line along lat/lon.')
    ## variables to plot
    #parser.add_argument('var_names', type=str)
    # number of parallel processes
    parser.add_argument('-p', '--n_par', type=int, default=1)
    # save or not? (0: show, 1: png, 2: pdf, 3: jpg)
    parser.add_argument('-s', '--i_save_fig', type=int, default=0)
    # recompute?
    parser.add_argument('-r', '--i_recompute', type=int, default=0)
    # computation mode? (normal, load, dask)
    parser.add_argument('-c', '--computation_mode', type=str, default='load')
    args = parser.parse_args()

    # PREPARATION STEPS
    ###########################################################################
    timer = Timer(mode='seconds')
    import nl_15 as nl_ana_raw
    from nl_plot_15 import nlp
    ana = Analysis_15(nl=SimpleNamespace())
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
        timer.stop('daily')

        print('concat')

        timer.start('concat')
        tsmp.concat_timesteps()
        src_members = tsmp.concat_output['members']
        timer.stop('concat')

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

        ### SET UP TIME SELECTORS FOR PLOTS WITH MULTIPLE TIME STEPS
        # determine number of time steps to plot
        dummy_member = targ_members[list(targ_members.keys())[0]]
        var = dummy_member.vars[list(dummy_member.vars.keys())[0]]

        time_plt_sels = [None]

        timer.stop('prepare')

        ## SET UP PLOT IO PATH
        ######################################################################
        timer.start('plot')
        name_dict = {'lline':'test'}

        ## INITIALIZE PLOT
        ######################################################################
        PO = PlotOrganizer(i_save_fig=ana.nl.i_save_fig,
                          path=os.path.join(ana.nl.plot_base_dir),
                          name_dict=name_dict, nlp=ana.nl.nlp, geo_plot=False)
        fig,axes = PO.initialize_plot(nrows=ana.nl.nrows,
                                      ncols=ana.nl.ncols,
                                      figsize=ana.nl.figsize,
                                      args_subplots_adjust=ana.nl.arg_subplots_adjust)

        ### DRAW AXES
        ######################################################################
        ax_ind = 0
        # draw a new axis for each with each time step
        for time_plt_sel in time_plt_sels:
            # sel time plot selection in namelist
            ana.nl.time_plt_sel = time_plt_sel
            ax = PO.get_axis(ax_ind, order='cols')
            ana.draw_axis(PO, targ_members, ax)
            ax_ind += 1

        PO.remove_axis_labels()

        ### FINAL FORMATTING
        ######################################################################
        #fig.subplots_adjust(**ana.nl.arg_subplots_adjust)
        #fig.suptitle('{:%Y%m%d} {}'.format(date, hour))
        #fig.suptitle('{}'.format(ana.nl.mem_src_dict[mem_key]['label']),
        #            x=0.55)

        PO.add_panel_labels(order='cols')

        PO.finalize_plot()
        timer.stop('plot')

    timer.print_report()
