#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Create spatial plots of various horizontal 2d fields.
                If observations are available, show them along the models
                e.g. validate radiative flux with satellite obs.
author			Christoph Heim
date created    18.11.2019
date changed    30.05.2022
"""
##############################################################################
import os, argparse, copy
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from types import SimpleNamespace
from an_super import Analysis
from package.nl_variables import nlv, get_plt_fact, get_plt_units
from package.constants import CON_RAD_EARTH
from package.utilities import Timer
from package.time_processing import Time_Processing as TP
from package.plot_functions import PlotOrganizer, draw_map
from package.functions import (import_namelist, calc_global_min_max)
from package.mp import TimeStepMP
##############################################################################

class Analysis_01(Analysis):

    def __init__(self, nl):
        super(Analysis_01, self).__init__(nl)
        self.nl = nl
        self.ana_number = 1

    def prepare_for_plotting(self, members):
        members = self.prepare_for_plotting_DEFAULT(members)

        #### COMPUTE/SET PLOT MAX/MIN
        ###########################################################################
        #sym_zero = False
        #diff_members = {}
        #abs_members = {}
        #for mem_key,member in members.items():
        #    if member.val_type in ['diff', 'bias']:
        #        diff_members[mem_key] = member
        #    elif member.val_type == 'abs':
        #        abs_members[mem_key] = member
        #    else:
        #        raise NotImplementedError()
        #if len(diff_members) > 0:
        #    calc_global_min_max(diff_members, sym_zero=True)
        #if len(abs_members) > 0:
        #    calc_global_min_max(abs_members, sym_zero=False)
        #for mem_key,member in members.items():
        #    for agg_var_name in list(member.vars.keys()):
        #        loc_var_name = TP.get_var_name(agg_var_name)
        #        if '@' in loc_var_name:
        #            var_name = loc_var_name.split('@')[0]
        #        else:
        #            var_name = loc_var_name
        #        limits = self.nl.nlp['var_plt_cfgs'][
        #                        var_name]['lims'][member.val_type]
        #        if limits[0] is not None:
        #            member.plot_min_max[agg_var_name][0] = limits[0]
        #        else:
        #            member.plot_min_max[agg_var_name][0] *= get_plt_fact(var_name)
        #        if limits[1] is not None:
        #            member.plot_min_max[agg_var_name][1] = limits[1]
        #        else:
        #            member.plot_min_max[agg_var_name][1] *= get_plt_fact(var_name)

        return(members)


    def draw_axis(self, PO, members, ax):
        """
        plot 2D field for only one member, var, and time.
        """
        self.draw_axis_DEFAULT(ax)


        # multi-member plotting not implemented here.
        if len(members) == 0:
            print('warning. 0 mebmers to plot!!')
            return()
        mem_key = list(members.keys())[0]
        member = members[mem_key]
        # copy mem_dict to manipulate it locally
        mem_dict = copy.copy(member.mem_dict)

        ### COMPUTE/SET PLOT MAX/MIN
        ##########################################################################
        if member.val_type in ['diff', 'bias', 'rel']:
            sym_zero = True
        elif member.val_type == 'abs':
            sym_zero = False
        else:
            raise NotImplementedError()
        calc_global_min_max({mem_key:member}, sym_zero=sym_zero)
        #for agg_var_name in list(member.vars.keys()):
        #    loc_var_name = TP.get_var_name(agg_var_name)
        #    if '@' in loc_var_name:
        #        var_name = loc_var_name.split('@')[0]
        #    else:
        #        var_name = loc_var_name
        #    limits = self.nl.nlp['var_plt_cfgs'][
        #                    var_name]['lims'][member.val_type]
        #    if limits[0] is not None:
        #        member.plot_min_max[agg_var_name][0] = limits[0]
        #    else:
        #        member.plot_min_max[agg_var_name][0] *= get_plt_fact(var_name)
        #    if limits[1] is not None:
        #        member.plot_min_max[agg_var_name][1] = limits[1]
        #    else:
        #        member.plot_min_max[agg_var_name][1] *= get_plt_fact(var_name)
        #    if 'levelscf' in self.nl.nlp['var_plt_cfgs'][var_name]:
        #        if member.val_type in self.nl.nlp['var_plt_cfgs'][var_name]['levelscf']:


        ## statistical values for bias labels
        member.compute_statistics(self.nl.plot_domain)

        # multi-var plotting not implemented here.
        agg_var_name = self.nl.load_agg_var_names[0]
        loc_var_name = TP.get_var_name(agg_var_name)
        if '@' in loc_var_name:
            var_name = loc_var_name.split('@')[0]
        else:
            var_name = loc_var_name

        ## select var to plot and format time label
        if self.nl.time_plt_sel is not None:
            plot_var = member.vars[agg_var_name].sel(self.nl.time_plt_sel)
            mem_dict['label'] += ': {}'.format(TP.format_time_label(
                                                    self.nl.time_plt_sel))
        else:
            plot_var = member.vars[agg_var_name]

        # in case no data is available:
        if plot_var is None:
            ax.set_title(mem_dict['label'])
            return()

        # format for plotting
        if member.val_type != 'rel':
            plot_var = plot_var * get_plt_fact(var_name)
            plt_units = get_plt_units(var_name)
        else:
            plot_var = plot_var * 100
            plt_units = '%'

        ## subtract mean values
        #plot_var = plot_var - 2.25

        ## force max/min values (set all values beyond limits to limit value)
        #plot_var = plot_var.where(
        #    (np.isnan(plot_var)) | (plot_var >= member.plot_min_max[agg_var_name][0]), 
        #    member.plot_min_max[agg_var_name][0])
        #plot_var = plot_var.where(
        #    (np.isnan(plot_var)) | (plot_var <= member.plot_min_max[agg_var_name][1]), 
        #    member.plot_min_max[agg_var_name][1])
        ##print(plot_var)
        ##quit()

        ### if anomalies should be plotted
        #plot_var = plot_var - plot_var.mean()

        ## draw spatial map
        draw_map(ax, self.nl.plot_domain, self.nl.nlp,
                 add_xlabel=True, add_ylabel=True,
                 dticks=self.nl.plot_domain['dticks'])

        ### ADD BIAS LABELS
        ######################################################################
        if (self.nl.add_bias_labels and
             ((member.val_type == 'diff') | 
                (member.val_type == 'bias'))):
                #(member.val_type == 'rel'))):

            ## If time_plot_sel is not none (thus we want to select a certain
            ## time value for plotting only), we need to select the bias
            ## from member.stat based on the index of time_plot_sel in
            ## the member times. This is unfortunate but necessary since
            ## member.stat does not have any time labels.
            if self.nl.time_plt_sel is not None:
                time_plt_sel_ind = np.argwhere(
                    (member.vars[agg_var_name].time == 
                     self.nl.time_plt_sel['time']).values
                ).squeeze()
                stat_val = member.stat[agg_var_name]['mean'][time_plt_sel_ind]
            else:
                ## TODO: this difference suddenly came up...
                try:
                    stat_val = member.stat[agg_var_name]['mean'][0]
                except IndexError:
                    stat_val = member.stat[agg_var_name]['mean']

            ## set label and format with units
            label = '{:7.3f} '.format(stat_val*get_plt_fact(var_name))
            label += plt_units
            pan_lab_x = ax.get_xlim()[0] + (
                            #ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.01
                            ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.03
            pan_lab_y = ax.get_ylim()[0] + (
                            #ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.03
                            ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.06
            ax.text(pan_lab_x, pan_lab_y, label,
                    fontdict={
                        'fontsize':12, 
                        'color':'black',
                        'backgroundcolor':(1,1,1,0.5),
                    })

        ### DRAW LAT LON PLOT
        ######################################################################
        #var_plt_cfg = self.nl.nlp['var_plt_cfgs'][var_name]
        if self.nl.nlp['2D_type'] == 'pcolormesh':
            CF = plot_var.squeeze().\
                    plot.pcolormesh(ax=ax,
                    cmap=self.nl.nlp['cmaps'][member.val_type][var_name],
                    #vmin=(member.plot_min_max[agg_var_name][0]),
                    #vmax=(member.plot_min_max[agg_var_name][1]),
                    levels=self.nl.nlp['levels'][member.val_type][var_name],
                    add_colorbar=self.nl.plot_ax_cbars[member.val_type],
                    add_labels=False)
        elif self.nl.nlp['2D_type'] == 'contourf':
            #if ('levelscf' in var_plt_cfg) and (member.val_type in var_plt_cfg['levelscf']):
            #    levels = var_plt_cfg['levelscf'][member.val_type]
            #    cbar_kwargs['ticks'] = levels
            ##print(var_plt_cfg)
            ##print(var_name)
            #elif ('dlevcf' in var_plt_cfg) and (member.val_type in var_plt_cfg['dlevcf']):
            #    #levels = int((
            #    #    var_plt_cfg['lims'][member.val_type][1] - 
            #    #    var_plt_cfg['lims'][member.val_type][0]
            #    #    ) / var_plt_cfg['dlevcf'][member.val_type])
            #    levels = np.arange(
            #        var_plt_cfg['lims'][member.val_type][0],
            #        var_plt_cfg['lims'][member.val_type][1]*1.01,
            #        var_plt_cfg['dlevcf'][member.val_type]
            #    )
            #    #if member.val_type != 'rel':
            #    #    levels += 1
            #    if member.val_type in ['diff','bias']:
            #        levels = int((
            #            var_plt_cfg['lims'][member.val_type][1] - 
            #            var_plt_cfg['lims'][member.val_type][0]
            #            ) / var_plt_cfg['dlevcf'][member.val_type])
            #        levels = np.arange(
            #            var_plt_cfg['lims'][member.val_type][0]+0.5*var_plt_cfg['dlevcf'][member.val_type],
            #            var_plt_cfg['lims'][member.val_type][1]*1.01-0.5*var_plt_cfg['dlevcf'][member.val_type],
            #            var_plt_cfg['dlevcf'][member.val_type]
            #        )
            #        #print(levels)
            #else:
            #    raise NotImplementedError('dlevcf not implemented for var {}'.format(var_name))

            ## force max/min values (set all values beyond limits to limit value)
            levels = self.nl.nlp['levels'][member.val_type][var_name]
            if np.min(levels) >= 0:
                plot_var = plot_var.where(
                    (np.isnan(plot_var)) | (plot_var >= np.min(levels)), np.min(levels)*1.001)
            else:
                plot_var = plot_var.where(
                    (np.isnan(plot_var)) | (plot_var >= np.min(levels)), np.min(levels)*0.999)
            if np.max(levels) >= 0:
                plot_var = plot_var.where(
                    (np.isnan(plot_var)) | (plot_var <= np.max(levels)), np.max(levels)*0.999)
            else:
                plot_var = plot_var.where(
                    (np.isnan(plot_var)) | (plot_var <= np.max(levels)), np.max(levels)*0.999)
            #print(levels)
            #print(np.min(plot_var))
            #print(np.max(plot_var))

            CF = plot_var.squeeze().\
                    plot.contourf(ax=ax,
                    cmap=self.nl.nlp['cmaps'][member.val_type][var_name],
                    #vmin=(member.plot_min_max[agg_var_name][0]),
                    #vmax=(member.plot_min_max[agg_var_name][1]),
                    extend='neither',
                    #levels=levels,
                    levels=levels,
                    add_labels=False,
                    #add_colorbar=self.nl.plot_ax_cbars[member.val_type],
                    add_colorbar=False)
                    #cbar_kwargs=cbar_kwargs)

        ### COLORBAR
        ######################################################################
        cbar_kwargs = {}
        if self.nl.i_plot_cbar:
            if self.nl.pan_cbar_pos == 'center right':
                height='100%'
                width='5%'
                orientation = 'vertical'
            elif self.nl.pan_cbar_pos == 'lower center':
                height='10%'
                width='100%'
                orientation = 'horizontal'
            else:
                raise NotImplementedError()
            cax = inset_axes(ax, 
                height=height, 
                width=width, 
                loc=self.nl.pan_cbar_pos, 
                borderpad=self.nl.pan_cbar_pad
            )

            ##  format cbar label
            cbar_label = ''
            if self.nl.cbar_label_mode in ['var_name','both']:
                cbar_label += '{} '.format(nlv[var_name]['label'])
                if self.nl.cbar_label_mode in ['both']:
                    if get_plt_units(var_name) != '':
                        cbar_label += '[{}]'.format(get_plt_units(var_name))
            elif self.nl.cbar_label_mode in ['var_units']:
                if get_plt_units(var_name) != '':
                    cbar_label += '{}'.format(get_plt_units(var_name))
            elif self.nl.cbar_label_mode in ['neither']:
                pass
            else:
                raise ValueError()

            ## draw cbar
            cbar_kwargs = {
                'label':cbar_label,
                'ticks':self.nl.nlp['cb_ticks'][member.val_type][var_name],
            }
            if var_name in self.nl.nlp['oom'][member.val_type]:
                if self.nl.nlp['oom'][member.val_type][var_name] != 0:
                    cbar_kwargs['format'] = OOMFormatter(
                        self.nl.nlp['oom'][member.val_type][var_name],
                        mathText=False,
                    )

            cb = PO.fig.colorbar(CF, cax=cax, orientation=orientation, **cbar_kwargs)
            #cb.formatter.set_powerlimits((0, 2))
            #if self.nl.i_add_cbar_label:
            #    pass
            #    #cb.set_label(label=cbar_kwargs['label'], 
            #    #    size=plt.rcParams['axes.labelsize'])
            #else:
            #    cb.set_label(label='')
            #cb.ax.tick_params(labelsize='large')

        ### FORMAT AXIS
        ######################################################################
        if self.nl.title is None:
            ax.set_title(mem_dict['label'])
        else:
            ax.set_title(self.nl.title)


    def compute_var(self, var):
        ## multi-var plotting not implemented here.
        #agg_var_name = self.nl.load_agg_var_names[0]
        #loc_var_name = TP.get_var_name(agg_var_name)
        #if '@' in loc_var_name:
        #    var_name = loc_var_name.split('@')[0]
        #else:
        #    var_name = loc_var_name

        ## average altitude if present
        if 'alt' in var.dims:
            var = var.mean(dim='alt')

        # resample to daily mean values if required.
        if self.nl.agg_level not in [TP.NONE, TP.HOURLY_SERIES, TP.DIURNAL_CYCLE]:
            var = TP.run_aggregation_step(var, 
                      { TP.ACTION:TP.RESAMPLE, 
                        TP.FREQUENCY:'D', 
                        TP.OPERATOR:TP.MEAN  })
            var.attrs['time_key'] = 'time'
            var.attrs['agg_level'] = TP.DAILY_SERIES
            var.attrs['agg_operator'] = TP.MEAN

        # coarse-grain the dataset
        if self.nl.i_coarse_grain > 0:
            print('COARSE GRAIN')
            dx_km = np.abs(np.diff(var.lat.values).mean()/180*np.pi*CON_RAD_EARTH/1000)
            window = int(self.nl.i_coarse_grain/dx_km)
            var = var.coarsen({'lon':window, 'lat':window},
                               boundary='trim').mean()
            #var = var.rename(var_name)
        return(var)


if __name__ == '__main__':

    # READ INPUT ARGUMENTS
    ###########################################################################
    parser = argparse.ArgumentParser(description = 'Draw spatial plots.')
    # variables to plot
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
    import nl_01 as nl_ana_raw
    from nl_plot_01 import nlp
    ana = Analysis_01(nl=SimpleNamespace())
    import_namelist(ana.nl, nl_ana_raw)
    ana.nl.nlp = nlp

    # input args
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
        timer.stop('daily')

        print('concat')

        timer.start('concat')
        tsmp.concat_timesteps()
        src_members = tsmp.concat_output['members']
        timer.stop('concat')

        #print(members['MMPI-ESM1-2-HR_hist'].vars['T2M'])
        #quit()

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
    # quit now if not plotting required
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
        if var.attrs['time_key'] != 'None':
            nts_plt = len(var[var.attrs['time_key']])
            time_plt_sels = []
            for tind in range(nts_plt):
                time_plt_sels.append({
                var.attrs['time_key'] : var[var.attrs['time_key']].isel(
                            {var.attrs['time_key']:tind}).values
            })
        else:
            time_plt_sels = [None]

        #time_plt_sels = [{'month':1}]
        #time_plt_sels = [{'season':'MAM'}]
        #print(time_plt_sels)
        #quit()

        timer.stop('prepare')

        ## SET UP PLOT IO PATH
        ######################################################################
        timer.start('plot')
        name_dict = {}
        name_dict['spatial'] = ana.nl.plot_domain['key']
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
        ### TODO DEBUG START
        #time_plt_sels = time_plt_sels[15:16]
        ### TODO DEBUG END
        for mem_key,member in targ_members.items():
            # draw a new axis for each with each time step
            for time_plt_sel in time_plt_sels:
                # sel time plot selection in namelist
                ana.nl.time_plt_sel = time_plt_sel
                ax = PO.get_axis(ax_ind, order='cols')
                ana.draw_axis(PO, {mem_key:member}, ax)
                ax_ind += 1

        ### COLORBAR
        ######################################################################
        cb_member = targ_members[list(targ_members.keys())[0]]
        #cb_loc_var_name = ana.nl.var_names[0]
        cb_full_agg_var_name = list(cb_member.vars.keys())[0]
        cb_loc_var_name = TP.get_var_name(cb_full_agg_var_name)
        if '@' in cb_loc_var_name:
            cb_var_name = cb_loc_var_name.split('@')[0]
        else:
            cb_var_name = cb_loc_var_name
        #ticks = np.linspace(cb_member.plot_min_max[cb_full_agg_var_name][0],
        #                    cb_member.plot_min_max[cb_full_agg_var_name][1], 5)
        if ana.nl.plot_glob_cbar:
            cax = fig.add_axes(ana.nl.glob_cbar_pos)
            cbar = plt.colorbar(mappable=cb_member.handles[cb_loc_var_name],
                                cax=cax, orientation='horizontal')#,
                                #ticks=ticks)
            #cbar.ax.set_xticklabels(ticks)
            unit = get_plt_units(cb_var_name)
            unit = '' if unit == '' else '[{}]'.format(unit)
            cax.set_xlabel('{} {}'.format(nlv[cb_var_name]['label'], unit))

        ### FINAL FORMATTING
        ######################################################################
        PO.remove_axis_labels()

        #fig.subplots_adjust(**ana.nl.arg_subplots_adjust)
        #fig.suptitle('{:%Y%m%d} {}'.format(date, hour))
        #fig.suptitle('{}'.format(nl.mem_src_dict[mem_key]['label']),
        #            x=0.55)

        if ana.nl.nlp['i_draw_panel_labels']:
            PO.add_panel_labels(order='cols', 
                        fontsize=ana.nl.nlp['panel_labels_fontsize'])

        PO.finalize_plot()
        timer.stop('plot')

    timer.print_report()
