#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     
author			Christoph Heim
date created    18.11.2019
date changed    30.05.2022
"""
##############################################################################
import os, argparse, copy
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from types import SimpleNamespace
from an_super import Analysis
from package.nl_variables import nlv, get_plt_fact, get_plt_units
from package.constants import CON_RAD_EARTH
from package.utilities import Timer, select_common_timesteps
from package.time_processing import Time_Processing as TP
from package.plot_functions import PlotOrganizer, draw_map
from package.functions import (
    import_namelist,
    load_member_var, 
    loc_to_var_name,
    calc_global_min_max,
)
from package.mp import TimeStepMP
from package.member import Member
##############################################################################

class Analysis_22(Analysis):

    def __init__(self, nl):
        super(Analysis_22, self).__init__(nl)
        self.nl = nl
        self.ana_number = 22

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
        ax.set_facecolor("k")


        # multi-member plotting not implemented here.
        if len(members) == 0:
            print('warning. 0 mebmers to plot!!')
            return()
        mem_key = list(members.keys())[0]
        member = members[mem_key]
        # copy mem_dict to manipulate it locally
        mem_dict = copy.copy(member.mem_dict)

        if self.nl.plot_type == 'spatial':
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
                        plot.pcolormesh(ax=ax,
                        cmap=self.nl.nlp['cmaps'][member.val_type][var_name],
                        #vmin=(member.plot_min_max[agg_var_name][0]),
                        #vmax=(member.plot_min_max[agg_var_name][1]),
                        levels=self.nl.nlp['levels'][member.val_type][var_name],
                        extend='neither',
                        add_colorbar=False,
                        add_labels=False)
            elif self.nl.nlp['2D_type'] == 'contourf':
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

        elif self.nl.plot_type == 'corr':
            agg_var_name = TP.get_agg_var_name(self.nl.corr_var,
                                self.nl.agg_level, self.nl.agg_operators[0])
            yvar = member.vars[agg_var_name]
            xvar_name = copy.deepcopy(self.nl.var_names)
            # get actualy target variable
            xvar_name.remove(self.nl.corr_var)
            xvar_name.remove('INVF')
            xvar_name = xvar_name[0]
            agg_var_name = TP.get_agg_var_name(xvar_name,
                                self.nl.agg_level, self.nl.agg_operators[0])
            xvar = member.vars[agg_var_name]

            # get values
            yvar = yvar.values.flatten()
            xvar = xvar.values.flatten()
            yvar = yvar[~np.isnan(yvar)]
            xvar = xvar[~np.isnan(xvar)]
            corr_coef = np.corrcoef(yvar,xvar)[0,1]
            ax.scatter(xvar, yvar)
            ax.axhline(y=0,color='k',linewidth=0.5)
            ax.axvline(x=0,color='k',linewidth=0.5)
            #ax.text(x=0.1,y=0.1, s=str(corr_coef), transform='axes')


        elif self.nl.plot_type == 'corr2d':
            agg_var_name = TP.get_agg_var_name(self.nl.corr_var,
                                self.nl.agg_level, self.nl.agg_operators[0])
            zvar = member.vars[agg_var_name]
            ax_var_names = copy.deepcopy(self.nl.var_names)
            # get actualy target variable
            ax_var_names.remove(self.nl.corr_var)
            ax_var_names.remove('INVF')
            agg_var_name = TP.get_agg_var_name(ax_var_names[0],
                                self.nl.agg_level, self.nl.agg_operators[0])
            xvar = member.vars[agg_var_name]
            agg_var_name = TP.get_agg_var_name(ax_var_names[1],
                                self.nl.agg_level, self.nl.agg_operators[0])
            yvar = member.vars[agg_var_name]

            # get values
            xvar = xvar.values.flatten()
            yvar = yvar.values.flatten()
            zvar = zvar.values.flatten()
            xvar = xvar[~np.isnan(xvar)]
            yvar = yvar[~np.isnan(yvar)]
            zvar = zvar[~np.isnan(zvar)]
            normalize = matplotlib.colors.Normalize(vmin=-20, vmax=20)
            ax.scatter(xvar, yvar, c=zvar, cmap='RdBu_r', norm=normalize)
            ax.axhline(y=0,color='k',linewidth=0.5)
            ax.axvline(x=0,color='k',linewidth=0.5)
            #ax.text(x=0.1,y=0.1, s=str(corr_coef), transform='axes')

        else:
            raise NotImplementedError()

        ### FORMAT AXIS
        ######################################################################
        if self.nl.title is None:
            ax.set_title(mem_dict['label'])
        else:
            ax.set_title(self.nl.title)

        #ax.set_title(f'{self.nl.title} {corr_coef}')



    def compute_src_members_for_date(self, ts):
        """
        Organize full analysis for a given date (ts).
        ts has to be called ts because compute_for_date is called from TimeStepMP.
        """
        #print(ts)

        if (self.nl.i_debug >= 1) and (ts.day == 1):
            print('Start processing month {:%Y%m}.'.format(ts))
        #if (self.nl.i_debug >= 1) and (ts.day == 1):
        #    print('Start processing month {:%Y%m}. Memory: {} MB'.format(ts, 
        #        psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2))

        ######## LOAD MEMBERS
        ##########################################################################
        members = {}
        for mem_key,mem_dict in self.src_mem_dict.items():
            #print(mem_key)
            # create member instance
            members[mem_key] = Member(mem_dict, val_type='abs')
            # set time key
            members[mem_key].time_key = 'time'

            loc_var_name = 'INVF'
            var_name = loc_to_var_name(loc_var_name)
            INVF = load_member_var(var_name, mem_dict['freq'],
                                ts, ts, mem_dict,
                                self.nl.var_src_dict,
                                self.nl.mean_var_src_dict,
                                self.nl.var_src_dict[var_name]['load'],
                                domain=self.nl.var_dom_map[loc_var_name],
                                i_debug=self.nl.i_debug,
                                dask_chunks=self.nl.dask_chunks)

            for loc_var_name in self.nl.var_names:

                # skip any date != first date of the month for
                # members with frequency monthly.
                if (mem_dict['freq'] == 'monthly') and (ts.day != 1):
                    var = None
                # also skip any date for daily member that is not
                # part of its date selection
                elif (mem_dict['freq'] == 'monthly') and (ts not in mem_dict['dates']):
                    var = None
                elif (mem_dict['freq'] == 'daily') and (ts not in mem_dict['dates']):
                    #print('not in date selection')
                    var = None
                else:
                    if self.nl.i_debug >= 2:
                        print('{}: {} for {:%Y%m%d}'.format(mem_key, 
                                                    loc_var_name, ts))

                    # in case of alt specification format accordingly
                    loc_dim = None
                    if '@' in loc_var_name:
                        loc_dim = loc_var_name.split('@')[1].split('=')[0]
                        loc_value = loc_var_name.split('@')[1].split('=')[1]
                        var_name = loc_var_name.split('@{}='.format(loc_dim))[0]
                    else:
                        var_name = loc_var_name

                    # load variable
                    var = load_member_var(var_name, mem_dict['freq'],
                                        ts, ts, mem_dict,
                                        self.nl.var_src_dict,
                                        self.nl.mean_var_src_dict,
                                        self.nl.var_src_dict[var_name]['load'],
                                        domain=self.nl.var_dom_map[loc_var_name],
                                        i_debug=self.nl.i_debug,
                                        dask_chunks=self.nl.dask_chunks)

                    # TODO LOCAL STUFF START
                    # set grid points without inversion to NaN
                    if var_name != 'INVF':
                        var,INVF = select_common_timesteps(var,INVF)
                        # remap to same latlon grid if necessary
                        if not np.array_equal(var.lat.values, INVF.lat.values):
                            var = var.interp(lat=INVF.lat.values, lon=INVF.lon.values)
                        var = var.where(INVF == 1, np.nan)
                    # TODO LOCAL STUFF STOP

                if var is not None:
                    # make sure all monthly data has first date of month
                    # as time stamp (this is assumed later on)
                    if mem_dict['freq'] == 'monthly':
                        new_time = [dt64_to_dt(var.time.values[0]).replace(day=1)]
                        var = var.assign_coords(time=new_time)
                    # optionally subselect specified altitude
                    if loc_dim is not None:
                        if len(loc_value.split('-')) == 1:
                            if float(loc_value) in var[loc_dim].values:
                                var = var.sel({loc_dim:float(loc_value)})
                            else:
                                var = var.interp({loc_dim:float(loc_value)})
                        elif len(loc_value.split('-')) == 2:
                            var = var.sel({loc_dim:slice(
                                float(loc_value.split('-')[0]),
                                float(loc_value.split('-')[1])
                                )
                            })
                            if len(var.alt) == 0:
                                raise ValueError('No altitude values in selected range for member {}.'.format(mem_key))
                        else:
                            raise ValueError()

                    # compute variable
                    var = self.compute_var(var)
                    #if var_name == 'INVF':
                    #    var.to_netcdf('test.nc')
                    #    quit()
                    # optionally load variable
                    if self.nl.computation_mode == 'load':
                        var.load()
                    members[mem_key].add_var(loc_var_name, var)

                    ## print used memory
                    #if self.nl.i_debug >= 3:
                    #    print('{} {}'.format(ts, 
                    #        psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2))
                else:
                    # free up memory
                    try:
                        del members[mem_key].mem_dict 
                    except AttributeError:
                        pass

                    members[mem_key].add_var(loc_var_name, None)

        #print(members['COSMO_3.3_ctrl'].vars)
        #print(members['COSMO_3.3_pgw3'].vars)
        #quit()
        output = {'members':members}
        return(output)


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


    def aggregate_time(self, member):
        # TODO LOCAL STUFF START
        # ensure that INVF is averaged first because
        # its average is used for other variables
        var_names = list(member.vars.keys())
        var_names.remove('INVF')
        var_names.insert(0, 'INVF')
        #print(member.vars)
        # TODO LOCAL STUFF STOP
        for var_name in var_names:
            #print(var_name)
            var = member.vars[var_name]
            for agg_operator in self.nl.agg_operators:
                #print(agg_operator)
                agg_var_name = TP.get_agg_var_name(var_name,
                                    self.nl.agg_level, agg_operator)

                if var is not None:
                    agg_var = TP.aggregate(var, self.nl.agg_level,
                                            agg_operator)
                    # TODO LOCAL STUFF START
                    # set grid points without mean INVF below threshold to NaN
                    if var_name != 'INVF':
                        agg_var = agg_var.where(
                            member.vars[
                                TP.get_agg_var_name('INVF',
                                    self.nl.agg_level, agg_operator)
                            ] >= self.nl.invf_threshold, 
                            np.nan
                        )
                        #agg_var.to_netcdf('test.nc')
                        #quit()
                    # TODO LOCAL STUFF STOP
                else:
                    agg_var = None
                member.vars[agg_var_name] = agg_var
            # delete unaggregated variable
            del member.vars[var_name]
        #quit()


    def prepare_namelist(self):
        self.nl.var_names.append('INVF')
        if (self.nl.plot_type == 'corr') and (self.nl.i_recompute == 0):
            self.nl.var_names.append(self.nl.corr_var)

        self.prepare_namelist_DEFAULT()


if __name__ == '__main__':

    # READ INPUT ARGUMENTS
    ###########################################################################
    parser = argparse.ArgumentParser(description = 'Draw spatial plots.')
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
    import nl_22 as nl_ana_raw
    from nl_plot_22 import nlp
    ana = Analysis_22(nl=SimpleNamespace())
    import_namelist(ana.nl, nl_ana_raw)
    ana.nl.nlp = nlp

    # input args
    ana.nl.i_recompute = args.i_recompute
    ana.nl.i_save_fig = args.i_save_fig
    ana.nl.n_par = args.n_par
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
