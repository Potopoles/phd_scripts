#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Plot altitude lat/lon cross-sections of certain quantities
dependencies    depends on:
author			Christoph Heim
date created    29.01.2021
date changed    01.06.2022
"""
###############################################################################
import os, argparse, copy
import numpy as np

import matplotlib
#matplotlib.use('ps')
#from matplotlib import rc
#
#rc('text',usetex=True)
#rc('text.latex', preamble=r'\usepackage{color}')


import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker
#from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from types import SimpleNamespace
from an_super import Analysis
from package.nl_variables import nlv, get_plt_units, get_plt_fact
from package.utilities import Timer, area_weighted_mean_lat_lon
from package.time_processing import Time_Processing as TP
from package.plot_functions import PlotOrganizer
from package.functions import import_namelist
from package.mp import TimeStepMP
from package.nl_models import models_cmip6
###############################################################################

class OOMFormatter(matplotlib.ticker.ScalarFormatter):
    def __init__(self, order=0, fformat="%1.1f", offset=True, mathText=True):
        self.oom = order
        self.fformat = fformat
        matplotlib.ticker.ScalarFormatter.__init__(self,useOffset=offset,useMathText=mathText)
    def _set_order_of_magnitude(self):
        self.orderOfMagnitude = self.oom
    def _set_format(self, vmin=None, vmax=None):
        self.format = self.fformat
        if self._useMathText:
             self.format = r'$\mathdefault{%s}$' % self.format


def multicolor_ylabel(ax,list_of_strings,list_of_colors,axis='x',anchorpad=0,**kw):
    """this function creates axes labels with multiple colors
    ax specifies the axes object where the labels should be drawn
    list_of_strings is a list of all of the text items
    list_if_colors is a corresponding list of colors for the strings
    axis='x', 'y', or 'both' and specifies which label(s) should be drawn"""
    from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, HPacker, VPacker

    # x-axis label
    if axis=='x' or axis=='both':
        boxes = [TextArea(text, textprops=dict(color=color, ha='left',va='bottom',**kw)) 
                    for text,color in zip(list_of_strings,list_of_colors) ]
        xbox = HPacker(children=boxes,align="center",pad=0, sep=5)
        anchored_xbox = AnchoredOffsetbox(loc=3, child=xbox, pad=anchorpad,frameon=False,bbox_to_anchor=(0.2, -0.09),
                                          bbox_transform=ax.transAxes, borderpad=0.)
        ax.add_artist(anchored_xbox)

    # y-axis label
    if axis=='y' or axis=='both':
        boxes = [TextArea(text, textprops=dict(color=color, ha='left',va='bottom',rotation=90,**kw)) 
                     for text,color in zip(list_of_strings[::-1],list_of_colors) ]
        ybox = VPacker(children=boxes,align="center", pad=0, sep=5)
        anchored_ybox = AnchoredOffsetbox(loc=3, child=ybox, pad=anchorpad, frameon=False, bbox_to_anchor=(-0.10, 0.2), 
                                          bbox_transform=ax.transAxes, borderpad=0.)
        ax.add_artist(anchored_ybox)


class Analysis_04(Analysis):

    def __init__(self, nl):
        super(Analysis_04, self).__init__(nl)
        self.nl = nl
        self.ana_number = 4


    def draw_axis(self, PO, members, ax):
        self.draw_axis_DEFAULT(ax)


        for mem_key, member in members.items():
            print(mem_key)
            mem_dict = copy.copy(member.mem_dict)
            val_type  = member.val_type

            #member.compute_statistics(self.nl.plot_domain)



            ### filled contour variables
            ##################################################################
            for vi,var_name in enumerate(self.nl.cf_var_names):
                # only plot if required
                if val_type == 'abs':
                    if var_name not in self.nl.cf_abs_var_names:
                        continue
                elif val_type in ['diff','bias','rel']:
                    if var_name not in self.nl.cf_diff_var_names:
                        continue
                else:
                    raise NotImplementedError()

                agg_var_name = TP.get_agg_var_name(var_name, 
                                            self.nl.agg_level, 
                                            self.nl.agg_operators[0])
                ## select var to plot and format time label
                if self.nl.time_plt_sel is not None:
                    plot_var = member.vars[agg_var_name].sel(
                                            self.nl.time_plt_sel)
                    mem_dict['label'] += ' {}'.format(
                                            TP.format_time_label(
                                                    self.nl.time_plt_sel))
                else:
                    plot_var = member.vars[agg_var_name]
                # skip if variable does not exist for this member
                if plot_var is None:
                    continue
                print('cf: {}'.format(agg_var_name))
                #if self.nl.agg_level in [self.nl.MONTHLY_SERIES]:
                #    plot_var = member[var_name].var
                #elif self.nl.agg_level == self.nl.HOURLY_SERIES:
                #    try:
                #        plot_var = member[var_name].var.loc[
                #                    {'time':'{:%Y-%m-%d}'.format(date)}]
                #    except KeyError:
                #        continue
                #    try:
                #        plot_var = plot_var.isel(time=time_ind)
                #    except IndexError:
                #        continue
                #else:
                #    raise NotImplementedError()

                ## get and transform variable to plot
                if 'rel' not in val_type:
                    plot_var = plot_var.copy() * get_plt_fact(var_name)
                else:
                    pass
                    #self.nl.nlp['levels']['cf'][val_type][var_name] = np.arange(-1.70,1.70,0.30)
                    #self.nl.nlp['cb_ticks']['cf'][val_type][var_name] = (
                    #    self.nl.nlp['levels']['cf'][val_type][var_name] 
                    #)
                    #self.nl.nlp['cmaps']['cf'][val_type][var_name] = 'RdBu_r'

                if (var_name in self.nl.norm_var_cfg) and (member.val_type == 'rel'):
                    raise NotImplementedError()
                    norm_var_name = self.nl.norm_var_cfg[var_name]
                    agg_norm_var_name = TP.get_agg_var_name(norm_var_name, 
                                                self.nl.agg_level, 
                                                self.nl.agg_operators[0])
                    norm_var = member.vars[agg_norm_var_name].sel(
                                            self.nl.time_plt_sel)
                    print(norm_var)
                    quit()
                    #plot_var /= 

                plot_var = plot_var.where(np.isnan(plot_var) | (plot_var >= 
                                np.min(self.nl.nlp['levels']['cf'][val_type][var_name])),
                                0.99*np.min(self.nl.nlp['levels']['cf'][val_type][var_name]))
                plot_var = plot_var.where(np.isnan(plot_var) | (plot_var <= 
                                np.max(self.nl.nlp['levels']['cf'][val_type][var_name])),
                                0.99*np.max(self.nl.nlp['levels']['cf'][val_type][var_name]))

                ### format coordinates
                plot_var = plot_var.assign_coords({
                    self.nl.line_along:plot_var[self.nl.line_along].values *
                    get_plt_fact(self.nl.cs_x_coord)
                })
                if 'alt' in plot_var.dims:
                    plot_var = plot_var.assign_coords({
                        'alt':plot_var['alt'].values *
                        get_plt_fact('COORD_ALT')
                    })

                CF = plot_var.squeeze().plot.contourf(
                            cmap=self.nl.nlp['cmaps']['cf'][val_type][var_name],
                            levels=self.nl.nlp['levels']['cf'][val_type][var_name],
                            antialiased=True,
                            #cbar_kwargs=cbar_kwargs,
                            add_colorbar=False,
                            ax=ax)
                member.handles[var_name] = CF

                #divider = make_axes_locatable(PO.cax)
                #cax = divider.append_axes('right', size='5%', pad=0.05)
                #cax = divider.append_axes('right', size='100%')

                #cax = ax.inset_axes([1.0, 0.0, 0.2, 1.0])
                #cb = plt.colorbar(CF, ax=cax, **cbar_kwargs, 
                #    fraction=1.0,
                #    aspect=10
                #)

                ### COLORBAR
                ##############################################################
                if self.nl.i_plot_cbar:
                    if self.nl.pan_cbar_pos == 'center right':
                        height='100%'
                        width='4%'
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
                            cbar_label += '[{}]'.format(get_plt_units(var_name))
                    elif self.nl.cbar_label_mode in ['neither']:
                        pass
                    else:
                        raise ValueError()

                    ## draw plot
                    cbar_kwargs = {
                        'label':cbar_label,
                        'ticks':self.nl.nlp['cb_ticks']['cf'][val_type][var_name],
                    }
                    if var_name in self.nl.nlp['oom']['cf'][val_type]:
                        if self.nl.nlp['oom']['cf'][val_type][var_name] != 0:
                            cbar_kwargs['format'] = OOMFormatter(
                                self.nl.nlp['oom']['cf'][val_type][var_name],
                                mathText=False,
                            )

                    cb = PO.fig.colorbar(CF, cax=cax, orientation=orientation, **cbar_kwargs)
                    #cb.formatter.set_powerlimits((0, 2))

                    #if self.nl.i_add_cbar_label:
                    #    cb.set_label(label=cbar_kwargs['label'], 
                    #        size=plt.rcParams['axes.labelsize'])
                    #else:
                    #    cb.set_label(label='')
                    ##cb.ax.tick_params(labelsize='large')



            ### specific height lines
            #############################################################
            if val_type == 'abs':
                for vi,var_name in enumerate(self.nl.alt_line_var_names):
                    agg_var_name = TP.get_agg_var_name(var_name,
                                    self.nl.agg_level, self.nl.agg_operators[0])
                    print('cl: {}'.format(agg_var_name))
                    plot_var = member.vars[agg_var_name]
                    # skip if variable does not exist for this member
                    if plot_var is None:
                        continue
                    plot_var = plot_var.sel(self.nl.time_plt_sel)

                    ## get and transform variable to plot
                    plot_var = plot_var.copy() * get_plt_fact(var_name)
                    # m to km
                    if not self.nl.norm_inv:
                        plot_var /= 1000
                    #print(plot_var)
                    #quit()

                    handle, = ax.plot(plot_var[self.nl.line_along],
                                     plot_var.values,
                                     label='test',
                                     linewidth=self.nl.nlp['linewidths'][vi],
                                     color=self.nl.nlp['colors'][vi],
                                     linestyle=self.nl.nlp['linestyles'][vi])
                    PO.handles.append(handle)



            ### line contour variables
            #############################################################
            for vi,var_name in enumerate(self.nl.cl_var_names):

                # only plot if required
                if val_type == 'abs':
                    if var_name not in self.nl.cl_abs_var_names:
                        continue
                #elif val_type == 'diff':
                #    if var_name not in self.nl.cl_diff_var_names:
                #        continue
                #elif val_type == 'bias':
                #    continue
                elif val_type in ['diff', 'bias']:
                    if var_name not in self.nl.cl_diff_var_names:
                        continue
                elif val_type in ['rel']:
                    continue
                else:
                    raise NotImplementedError()

                agg_var_name = TP.get_agg_var_name(var_name,
                                self.nl.agg_level, self.nl.agg_operators[0])
                print('cl: {}'.format(agg_var_name))
                #var_name = self.nl.var_names_3d_lc[0]
                #plot_var = member[var_name].var.loc[{'time':'{:%Y-%m-%d}'.format(date)}]
                #try:
                #    plot_var = plot_var.isel(time=time_ind)
                #except IndexError:
                #    continue

                ## select var to plot and format time label
                if self.nl.time_plt_sel is not None:
                    plot_var = member.vars[agg_var_name].sel(self.nl.time_plt_sel)
                    #mem_dict['label'] += ' {}'.format(TP.format_time_label(
                    #                                        self.nl.time_plt_sel))
                else:
                    plot_var = member.vars[agg_var_name]

                # skip if variable does not exist for this member
                if plot_var is None:
                    continue

                ## get and transform variable to plot
                plot_var = plot_var.copy() * get_plt_fact(var_name)

                if 'alt' in plot_var.dims:
                    alt_coord_name = 'alt'
                    plot_var = plot_var.assign_coords({
                        'alt':plot_var['alt'].values *
                        get_plt_fact('COORD_ALT')
                    })
                elif 'rel_alt' in plot_var.dims:
                    alt_coord_name = 'rel_alt'

                CL = ax.contour(
                        (plot_var[self.nl.line_along].values * 
                            get_plt_fact(self.nl.cs_x_coord)),
                        plot_var[alt_coord_name].values, 
                        plot_var.values.squeeze(), 
                        #cmap=self.nl.nlp['cmaps']['cl'][val_type][var_name],
                        colors='k',
                        levels=self.nl.nlp['levels']['cl'][val_type][var_name],
                        #linewidths=0.5)
                        linewidths=self.nl.nlp['contour_linewidths'][val_type])
                ## add numbers to contour lines
                #ax.clabel(CL, inline=1, fontsize=10)


            ### y2 vars
            #############################################################
            if val_type == 'abs':
                for vi,var_name in enumerate(self.nl.y2_abs_line_var_names):
                    agg_var_name = TP.get_agg_var_name(var_name,
                                    self.nl.agg_level, self.nl.agg_operators[0])
                    print('cl: {}'.format(agg_var_name))
                    plot_var = member.vars[agg_var_name]
                    # skip if variable does not exist for this member
                    if plot_var is None:
                        continue
                    plot_var = plot_var.sel(self.nl.time_plt_sel)

                    ## get and transform variable to plot
                    plot_var = plot_var.copy() * get_plt_fact(var_name)
                    #print(plot_var)
                    #quit()
                    
                    try:
                        print(ax2)
                        linestyle = self.nl.nlp['linestyles'][1]
                    except UnboundLocalError:
                        ax2 = ax.twinx()
                        for ri in range(PO.axes.shape[0]):
                            for ci in range(PO.axes.shape[1]):
                                if PO.axes[ri,ci] == ax:
                                    PO.axes_twinx[ri,ci] = ax2
                        linestyle = self.nl.nlp['linestyles'][0]

                    if var_name == 'PP':
                        color = self.nl.nlp['colors'][vi]
                        linewidth = self.nl.nlp['linewidths'][vi]
                        zorder = -1
                        ax2.set_ylim(0,18)
                        raise_ax1 = True
                    elif var_name == 'TSURF':
                        color = 'orange' 
                        linewidth = 1.5
                        zorder = 2
                        ax2.set_ylim(290,308)
                        raise_ax1 = False
                    else:
                        raise NotImplementedError()

                    #handle, = ax.plot(plot_var[self.nl.line_along],
                    handle, = ax2.plot(plot_var[self.nl.line_along],
                                     plot_var.values,
                                     label='test',
                                     linewidth=linewidth,
                                     color=color,
                                     linestyle=linestyle,
                                     zorder=zorder)
                    PO.handles.append(handle)

                    #if len(self.nl.y2_line_var_names) > 0:
                    PO.set_axes_labels(ax2, y_var_name=self.nl.y2_abs_line_var_names[0],
                                        kwargs=dict(color=color), 
                                        labelsize=plt.rcParams['axes.labelsize'])
                    ax2.tick_params(axis='y', colors=color)

                    if raise_ax1:
                        ax.set_zorder(ax2.get_zorder()+1)
                    ax.patch.set_visible(False)

            elif val_type == 'diff':
                for vi,var_name in enumerate(self.nl.y2_diff_line_var_names):
                    agg_var_name = TP.get_agg_var_name(var_name,
                                    self.nl.agg_level, self.nl.agg_operators[0])
                    print('cl: {}'.format(agg_var_name))
                    plot_var = member.vars[agg_var_name]
                    # skip if variable does not exist for this member
                    if plot_var is None:
                        continue
                    plot_var = plot_var.sel(self.nl.time_plt_sel)

                    ## get and transform variable to plot
                    plot_var = plot_var.copy() * get_plt_fact(var_name)
                    #print(plot_var)
                    #quit()
                    
                    try:
                        print(ax2)
                        linestyle = self.nl.nlp['linestyles'][1]
                    except UnboundLocalError:
                        ax2 = ax.twinx()
                        for ri in range(PO.axes.shape[0]):
                            for ci in range(PO.axes.shape[1]):
                                if PO.axes[ri,ci] == ax:
                                    PO.axes_twinx[ri,ci] = ax2
                        #ax2.set_ylim(-2,2)
                        linestyle = self.nl.nlp['linestyles'][0]


                    if var_name == 'PP':
                        color = self.nl.nlp['colors'][vi]
                        linewidth = self.nl.nlp['linewidths'][vi]
                        zorder = -1
                        ax2.set_ylim(-2.5,6.5)
                        raise_ax1 = True
                    elif var_name == 'TSURF':
                        color = 'orange' 
                        linewidth = 1.5
                        zorder = 2
                        ax2.set_ylim(0,7.2)
                        raise_ax1 = False
                    else:
                        raise NotImplementedError()

                    #handle, = ax.plot(plot_var[self.nl.line_along],
                    handle, = ax2.plot(plot_var[self.nl.line_along],
                                     plot_var.values,
                                     label='test',
                                     linewidth=linewidth,
                                     color=color,
                                     linestyle=linestyle,
                                     zorder=zorder)
                    PO.handles.append(handle)

                    #if len(self.nl.y2_line_var_names) > 0:
                    PO.set_axes_labels(ax2, y_var_name=self.nl.y2_diff_line_var_names[0],
                                        kwargs=dict(color=color), 
                                        labelsize=plt.rcParams['axes.labelsize'])
                    ax2.tick_params(axis='y', colors=color)

                    #ax.set_zorder(ax2.get_zorder()+1)
                    ax.patch.set_visible(False)


            ### vertical line
            #############################################################
            if self.nl.vertical_line is not None:
                ax.axvline(
                    x=self.nl.vertical_line, 
                    color='grey', 
                    linestyle='--', 
                    linewidth=1.2
                )


            if self.nl.norm_inv:
                ax.set_ylim((0,2))
                PO.set_axes_labels(ax, self.nl.cs_x_coord, 'COORD_RELALT', 
                                        labelsize=plt.rcParams['axes.labelsize'])
            else:
                ax.set_ylim((self.nl.alt_lims[0]*get_plt_fact('COORD_ALT'),
                             self.nl.alt_lims[1]*get_plt_fact('COORD_ALT')))

                #if len(self.nl.y2_line_var_names) > 0:
                #    #ax.set_ylabel(r'\textcolor{red}{Today} '+
                #    #           r'\textcolor{green}{is}')
                #    #multicolor_ylabel(ax,('Line1','and'),('k','r'),axis='y',size=15,weight='bold')
                #else:
                PO.set_axes_labels(ax, self.nl.cs_x_coord, 'COORD_ALT', 
                                        labelsize=plt.rcParams['axes.labelsize'])
                ## Special feature: add precipitation to plot
                #if 'PP' in self.nl.alt_line_var_names:
                #    PO.set_axes_labels(ax, y_var_name='PP', 
                #        overwrite=False, same_units=False)



            ax.set_xlim((self.nl.plot_domain[self.nl.line_along].start,
                         self.nl.plot_domain[self.nl.line_along].stop))
            #ax.set_xlabel(self.nl.line_along)

            # plot grid
            #ax.grid(color='k', linewidth=0.5)
            ax.grid(zorder=-1)


            if self.nl.i_show_title:
                if self.nl.title is not None:
                    ax.set_title(self.nl.title, x=0.50)
                else:
                    ax.set_title(mem_dict['label'], x=0.50)
            ##ax.set_ylabel(r'height [$m$]')
            ## manually add the desired panel label
            #pan_lab_x = ax.get_xlim()[0] - (
            #                ax.get_xlim()[1] - ax.get_xlim()[0]) * \
            #                self.nl.self.nlp['panel_label_x_left_shift'] 
            #pan_lab_y = ax.get_ylim()[0] + (
            #                ax.get_ylim()[1] - ax.get_ylim()[0]) * \
            #                self.nl.self.nlp['panel_label_y_pos'] 
            #ax.text(pan_lab_x, pan_lab_y,
            #        self.nl.self.nlp['panel_labels'][mem_ind],
            #        fontsize=self.nl.self.nlp['panel_label_size'], weight='bold')

        #return(handles)


    def compute_var(self, var):
        if self.nl.line_along == 'lat':
            at_dim = 'lon' 
            if self.nl.line_at is None:
                self.nl.line_at = slice(self.nl.plot_domain['lon'].start+1,
                                        self.nl.plot_domain['lon'].stop-1)
        elif self.nl.line_along == 'lon':
            at_dim = 'lat' 
            if self.nl.line_at is None:
                self.nl.line_at = slice(self.nl.plot_domain['lat'].start+1,
                                        self.nl.plot_domain['lat'].stop-1)
        # select either range or individual values
        if type(self.nl.line_at) == slice:
            var = var.sel({at_dim:self.nl.line_at})
        else:
            var = var.sel({at_dim:self.nl.line_at}, method='nearest')

        ## TODO attention! this does not work with "masked" arrays containing nans!!!
        ## mask line_along entries where at_dim without missing values
        ## spans less distance than nl.min_dlonlat
        #if var[at_dim].size > 1:
        #    dx_at_dim = np.median(np.diff(var[at_dim]))
        #    mask = ((~np.isnan(var)).sum(dim=at_dim)*dx_at_dim
        #                    > self.nl.min_dlonlat).expand_dims(
        #                                    {at_dim:var[at_dim]},
        #                                    axis=var.dims.index(at_dim))
        #    var = var.where(mask, np.nan)

        # average accross at_dim
        if var[at_dim].values.size > 1:
            var = area_weighted_mean_lat_lon(var, [at_dim])
            #var = var.mean(dim=at_dim)

        ## subsel altitude slice for 3d vars
        #if 'z' in nlv[var.name]['dims']:
        #    var = var.sel(alt=slice(self.nl.alt_lims[0],
        #                            self.nl.alt_lims[1]*1.2))
        #    ## find alt index that is above upper limit given by user
        #    ## (to prevent missing values in plot)
        #    #var = var.sel(alt=slice(self.nl.alt_lims[0],100000))
        #    #alt_ind = 0
        #    #while var.alt.isel(alt=alt_ind) <= self.nl.alt_lims[1]:
        #    #    alt_ind += 1
        #    #alt_ind += 1
        #    #var = var.isel(alt=slice(0,alt_ind))


        if self.nl.agg_level not in [TP.HOURLY_SERIES, TP.DIURNAL_CYCLE, TP.NONE]:
            var = TP.run_aggregation_step(var, 
                      { TP.ACTION:TP.RESAMPLE, 
                        TP.FREQUENCY:'D', 
                        TP.OPERATOR:TP.MEAN  })
        return(var)


    def prepare_namelist(self):

        if self.nl.norm_inv:
            alt_line_var_names = ['LCL']
        else:
            alt_line_var_names = ['LCL', 'INVHGT']

        if self.nl.plot_append in models_cmip6:
            alt_line_var_names = []

        alt_line_var_names = []
        y2_abs_line_var_names = []
        y2_diff_line_var_names = []

        cf_abs_var_names = []
        cf_diff_var_names = []
        cl_abs_var_names = [] 
        cl_diff_var_names = [] 

        if self.nl.var_type == 'QX':
            cf_abs_var_names = ['QI', 'QC']
        elif self.nl.var_type == 'XCLDF':
            #cf_abs_var_names = ['LCLDF1E-5']
            #cf_abs_var_names = ['ICLDF1E-5']
            cf_abs_var_names = ['LCLDF1E-5', 'ICLDF1E-5']
            #cl_abs_var_names = ['LCLDF1E-5', 'ICLDF1E-5'] 
        elif self.nl.var_type == 'CLDF':
            cf_abs_var_names = ['CLDF']
            cf_diff_var_names = ['CLDF']
        elif self.nl.var_type == 'CLDF_CLDF':
            cf_abs_var_names = ['CLDF']
            cf_diff_var_names = ['CLDF']
            cl_abs_var_names = ['CLDF'] 
            cl_diff_var_names = ['CLDF'] 
        elif self.nl.var_type == 'CLDF_CLDF_PP':
            cf_abs_var_names = ['CLDF']
            cf_diff_var_names = ['CLDF']
            cl_abs_var_names = ['CLDF'] 
            cl_diff_var_names = ['CLDF'] 
            y2_abs_line_var_names = ['PP']
            y2_diff_line_var_names = ['PP']
        elif self.nl.var_type == 'WFLX_CLDF_TSURF':
            cf_abs_var_names = ['WFLX']
            cf_diff_var_names = ['WFLX']
            cl_abs_var_names = ['CLDF'] 
            cl_diff_var_names = ['CLDF'] 
            y2_abs_line_var_names = ['TSURF']
            y2_diff_line_var_names = ['TSURF']
        elif self.nl.var_type == 'VFLX_CLDF_TSURF':
            cf_abs_var_names = ['VFLX']
            cf_diff_var_names = ['VFLX']
            cl_abs_var_names = ['CLDF'] 
            cl_diff_var_names = ['CLDF'] 
            y2_abs_line_var_names = ['TSURF']
            y2_diff_line_var_names = ['TSURF']
        elif self.nl.var_type == 'RH_CLDF_TSURF':
            cf_abs_var_names = ['RH']
            cf_diff_var_names = ['RH']
            cl_abs_var_names = ['CLDF'] 
            cl_diff_var_names = ['CLDF'] 
            y2_abs_line_var_names = ['TSURF']
            y2_diff_line_var_names = ['TSURF']
        elif self.nl.var_type == 'QV_CLDF_SLHFLX':
            cf_abs_var_names = ['QV']
            cf_diff_var_names = ['QV']
            cl_abs_var_names = ['CLDF'] 
            cl_diff_var_names = ['CLDF'] 
            y2_line_var_names = ['SLHFLX']
        #elif '_QCI' in self.nl.var_type:
        #    cf_var_name = self.nl.var_type.split('_QCI')[0]
        #    cf_abs_var_names = [cf_var_name]
        #    cf_diff_var_names = [cf_var_name]
        #    cl_abs_var_names = [] 
        #    cl_diff_var_names = [] 
        #    if self.nl.plot_append not in models_cmip6:
        #        cl_abs_var_names = ['QC'] 
        #        cl_diff_var_names = ['QC'] 
        #        if not self.nl.norm_inv:
        #            cl_abs_var_names.append('QI') 
        #            cl_diff_var_names.append('QI') 
        #    else:
        #        cl_abs_var_names = ['CLDF'] 
        #        cl_diff_var_names = ['CLDF'] 
        #elif '_CLDW' in self.nl.var_type:
        #    cf_var_name = self.nl.var_type.split('_CLDW')[0]
        #    cf_abs_var_names = [cf_var_name]
        #    cf_diff_var_names = [cf_var_name]
        #    cl_abs_var_names = [] 
        #    cl_diff_var_names = [] 
        #    if self.nl.plot_append not in models_cmip6:
        #        cl_abs_var_names = ['CLDW'] 
        #        cl_diff_var_names = ['CLDW'] 
        #    else:
        #        cl_abs_var_names = ['CLDF'] 
        #        cl_diff_var_names = ['CLDF'] 
        elif '_CLDF' in self.nl.var_type:
            cf_var_name = self.nl.var_type.split('_CLDF')[0]
            cf_abs_var_names = [cf_var_name]
            cf_diff_var_names = [cf_var_name]
            cl_abs_var_names = ['CLDF'] 
            cl_diff_var_names = ['CLDF'] 
        #elif self.nl.var_type in ['U', 'V', 'W', 'QV', 'T', 'RH', 'QC', 'CLDMASK',
        #    'POTTHDIV', 'POTTVDIV', 'QVHDIV', 'QVVDIV', 'DIABH', 'DIABM']:
        #    cf_abs_var_names = [self.nl.var_type]
        #    cf_diff_var_names = [self.nl.var_type]
        #    cl_abs_var_names = [self.nl.var_type] 
        #    cl_diff_var_names = [self.nl.var_type] 
        #    #cl_abs_var_names = [] 
        #    #cl_diff_var_names = [] 

        #    alt_line_var_names = []
        elif self.nl.var_type == 'compute':
            cf_abs_var_names = [
                'T', 'QV', 'RH',
                'W', 'U', 'V',
                'QC', #'QI',
                'LCLDF1E-3', 'LCLDF5E-4', 'LCLDF2E-4', 'LCLDF1E-4', 'LCLDF5E-5', 'LCLDF2E-5', 'LCLDF1E-5',
                #'ICLDF1E-3', 'ICLDF5E-4', 'ICLDF2E-4', 'ICLDF1E-4', 'ICLDF5E-5', 'ICLDF2E-5', 'ICLDF1E-5',
                'DIABH', 'POTTHDIV', 'POTTVDIV',
                'DIABM', 'QVHDIV', 'QVVDIV',
            ]
            cf_abs_var_names = [

                #'CLDF',
                #'PP',
                #'TSURF',
                #'RH',
                #'T',
                #'WFLX',
                'VFLX',
                #'POTTDIV',
                #'W',

                #'POTT',
                #'BVF',
                #'QV',

                #'QVDIV3MEAN',
                #'QVHDIV3MEAN',
                #'QVVDIV3MEAN',
                #'QV',
                #'BUOYIFLX',
                #'QVDIV3',
                #'QVDIV3TURB',
                #'CSPOTTDIV3',
                #'CSPOTTDIV',
                #'CLDPOTTDIV',
                #'CSUVDIV',
                #'CLDUVDIV',
                #'CLDPOTTDIV',
                #'CLDQVDIV3TURB',
                #'CSQVDIV3TURB',



                #'EQPOTTDIV3',
                #'CSEQPOTTDIV3',
                #'CLDEQPOTTDIV3',
                #'LATH',
                #'POTTDIV3',
                #'POTTDIV4',
                #'POTTVDIV',
                #'POTTHDIV',
                #'CLDPOTTDIV3',
                #'NCOLIPOTTDIV3',
                #'NCOLIPOTTDIV',

                #'QIDIV3',

                #'RH',
                #'QI',
                #'QC',
                #'CLDW',
                #'CSW',
                #'NCOLIQV',
                #'T',
                #'UVDIV',
                ##'CSUVDIV',
                ##'CLDUVDIV',
                #'U',
                #'V',
                #'W',
                #'TKE',

            ]
            cl_abs_var_names = [] 
            cf_diff_var_names = []
            cl_diff_var_names = [] 

            #alt_line_var_names = ['LCL', 'INVHGT']
            ###y2_line_var_names = ['SLHFLX']
            #alt_line_var_names = ['SLHFLX']
        else:
            raise NotImplementedError()


        if self.nl.norm_inv:
            self.nl.cf_abs_var_names = ['{}NORMI'.format(var_name) for var_name in cf_abs_var_names]
            self.nl.cf_diff_var_names = ['{}NORMI'.format(var_name) for var_name in cf_diff_var_names]
            self.nl.cl_abs_var_names = ['{}NORMI'.format(var_name) for var_name in cl_abs_var_names]
            self.nl.cl_diff_var_names = ['{}NORMI'.format(var_name) for var_name in cl_diff_var_names]
            self.nl.alt_line_var_names = ['{}NORMI'.format(var_name) for var_name in alt_line_var_names]
        else:
            self.nl.cf_abs_var_names = cf_abs_var_names
            self.nl.cf_diff_var_names = cf_diff_var_names
            self.nl.cl_abs_var_names = cl_abs_var_names
            self.nl.cl_diff_var_names = cl_diff_var_names
            self.nl.alt_line_var_names = alt_line_var_names
        self.nl.y2_abs_line_var_names = y2_abs_line_var_names
        self.nl.y2_diff_line_var_names = y2_diff_line_var_names

        # all variable names
        self.nl.var_names = copy.copy(self.nl.cf_abs_var_names)
        self.nl.var_names.extend(self.nl.cf_diff_var_names)
        self.nl.var_names.extend(self.nl.cl_abs_var_names)
        self.nl.var_names.extend(self.nl.cl_diff_var_names)
        self.nl.var_names.extend(self.nl.alt_line_var_names)
        self.nl.var_names.extend(self.nl.y2_abs_line_var_names)
        self.nl.var_names.extend(self.nl.y2_diff_line_var_names)

        # add normalization vars
        for vn,norm_vn in self.nl.norm_var_cfg.items():
            self.nl.var_names.append(norm_vn)

        # contourf variable names
        self.nl.cf_var_names = copy.copy(self.nl.cf_abs_var_names)
        self.nl.cf_var_names.extend(self.nl.cf_diff_var_names)

        # contour variable names
        self.nl.cl_var_names = copy.copy(self.nl.cl_abs_var_names)
        self.nl.cl_var_names.extend(self.nl.cl_diff_var_names)

        # only use unique var_names
        self.nl.var_names = list(set(self.nl.var_names))
        self.nl.cf_var_names = list(set(self.nl.cf_var_names))
        self.nl.cl_var_names = list(set(self.nl.cl_var_names))

        if self.nl.line_along == 'lat':
            self.nl.cs_x_coord = 'COORD_LAT'
        elif self.nl.line_along == 'lon':
            self.nl.cs_x_coord = 'COORD_LON'

        self.nl.pickle_append = self.nl.line_along

        self.prepare_namelist_DEFAULT()



if __name__ == '__main__':
    # READ INPUT ARGUMENTS
    ###########################################################################
    parser = argparse.ArgumentParser(description = 'Draw vertical cross-section.')
    # variable to plot
    parser.add_argument('var_type', type=str)
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
    import nl_04 as nl_ana_raw
    from nl_plot_04 import nlp
    ana = Analysis_04(nl=SimpleNamespace())
    import_namelist(ana.nl, nl_ana_raw)
    ana.nl.nlp = nlp

    # input arguments
    ana.nl.var_type = args.var_type
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
        tsmp = TimeStepMP(ana.iter_dates, njobs=ana.nl.n_par, run_async=False)
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
        #time_plt_sels = [time_plt_sels[0]]

        timer.stop('prepare')

        ## SET UP PLOT IO PATH
        ######################################################################
        timer.start('plot')
        name_dict = {}
        name_dict['cs'] = ana.nl.agg_level 
        name_dict[ana.nl.plot_domain['key']] = ana.nl.line_along
        if ana.nl.norm_inv:
            name_dict['norm_inv'] = ana.nl.var_type
        else:
            name_dict[ana.nl.alt_lims[1]] = ana.nl.var_type
        if ana.nl.plot_append != '':
            name_dict[ana.nl.plot_append] = ''
        #name_dict['month'] = '{:02d}'.format(time_plt_sels[0]['month'])

        ## INITIALIZE PLOT
        ######################################################################
        PO = PlotOrganizer(i_save_fig=ana.nl.i_save_fig,
                          path=os.path.join(ana.nl.plot_base_dir),
                          name_dict=name_dict, nlp=ana.nl.nlp, geo_plot=False)
        fig,axes = PO.initialize_plot(nrows=ana.nl.nrows,
                                      ncols=ana.nl.ncols,
                                      figsize=ana.nl.figsize)

        ## TODO start tmp
        time_plt_sels = [time_plt_sels[0]]
        ## TODO end tmp

        ### DRAW AXES
        ######################################################################
        ax_ind = 0
        for mem_key,member in targ_members.items():
            # draw a new axis for each with each time step
            for time_plt_sel in time_plt_sels:
                # sel time plot selection in namelist
                ana.nl.time_plt_sel = time_plt_sel
                ax = PO.get_axis(ax_ind, order='cols')
                ana.draw_axis(PO, {mem_key:member}, ax)
                ax_ind += 1

        PO.remove_axis_labels(completely=False)

        #### COLORBAR
        ######################################################################
        if ana.nl.plot_glob_cbar:
            cb_member = targ_members[list(targ_members.keys())[0]]
            cb_var_name = ana.nl.cf_var_names[0]
            ticks = ana.nl.nlp['cb_ticks']['cf']['abs'][cb_var_name]
            cax = fig.add_axes(ana.nl.colorbar_pos)
            cbar = plt.colorbar(mappable=cb_member.handles[cb_var_name],
                                cax=cax, orientation='horizontal',
                                ticks=ticks)
            cbar.ax.set_xticklabels(ticks)
            unit = get_plt_units(cb_var_name)
            unit = '' if unit == '' else '[{}]'.format(unit)
            cax.set_xlabel('{} {}'.format(nlv[cb_var_name]['label'], unit))

        ### FINAL FORMATTING
        ######################################################################
        fig.subplots_adjust(**ana.nl.arg_subplots_adjust)
        #fig.suptitle('{:%Y%m%d} {}'.format(date, hour))
        #fig.suptitle('{}'.format(ana.nl.mem_src_dict[mem_key]['label']),
        #            x=0.55)

        PO.add_panel_labels(order='cols', **nlp['panel_label_kwargs'])

        PO.finalize_plot()
        timer.stop('plot')

    timer.print_report()
