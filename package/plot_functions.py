#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    Functions to automate plotting, drawing spatial maps.
                Class PlotOrganizer: Helps setting up and finalizing plots.
author			Christoph Heim
date created    20.04.2019
date changed    01.06.2022
usage			no args
"""
###############################################################################
import os, cartopy
import numpy as np
import cartopy.crs as ccrs
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from pathlib import Path
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from package.nl_variables import nlv, get_plt_units, get_plt_fact
###############################################################################

#def get_twin(ax):
#    twin_ax = None
#    for other_ax in ax.figure.axes:
#        if other_ax is ax:
#            continue
#        if other_ax.bbox.bounds == ax.bbox.bounds:
#            twin_ax = other_ax
#    return(twin_ax)

class PlotOrganizer:

    def __init__(self, i_save_fig=0, path=None, name_dict=None, nlp=None,
                 geo_plot=False):
        """
        ARGS:
        i_save_fig: int - 0: show, 1: png, 2: pdf, 3: jpg
        path:       str - path to output directory (if i_save_fig > 0).
        name_dict:  OrderedDict - contains key/value pairs that should enter
                    the plot name. Examples:
                    simple name: name_dict = {'':'psurf'}
                                 --> 'path'/psurf.png
                    more complex: name_dict = {'':'p_surf', 'time':12}
                                 --> 'path'/psurf_time_12.png
        nlp:        dict - namelist with few plotting attributes.
                    If it is None, the default nlp setting will be used.
        geo_plot:   log - should the plot become a map with projection using
                    cartopy?
        """
        self.i_save_fig = i_save_fig
        self.path = path
        self.name_dict = name_dict
        if nlp is None:
            self.nlp = {}
        else:
            self.nlp = nlp
        self.geo_plot = geo_plot
        self.handles = []

        # None array indicating for each main axis whether
        # a twinx axis object exists. This is used to remove axis labels later on
        # if a twinx axis exist, it is later on set in this array
        axes_twinx = None


        ## generate plot name and directory
        if (self.path is None) or (name_dict is None):
            raise ValueError('Plot output path or name_dict not given')
        else:
            plot_name = ''
            for key,value in name_dict.items():
                if value != '':
                    plot_name += str(key).replace(' ','_') + '_' + \
                                    str(value).replace(' ','_') + '_'
                else:
                    plot_name += str(key).replace(' ','_') + '_'
            plot_name = plot_name[:-1] 

            # create plotting directory if it does not exist
            Path(path).mkdir(parents=True, exist_ok=True)

            # join plotting directory and plot name
            self.path = os.path.join(path,plot_name)

        if i_save_fig == 0:
            pass
        elif i_save_fig == 1:
            self.path += '.png'
        elif i_save_fig == 2:
            self.path += '.pdf'
        elif i_save_fig == 3:
            self.path += '.jpg'
        else:
            raise ValueError('Wrong argument for i_save_fig.')


    def plot_exists(self):
        """
        Check whether this plot already exists.
        OUT:
            True if plot exists, else False.
        """
        if os.path.exists(self.path):
            return(True)
        else:
            return(False)


    def initialize_plot(self, 
        nrows=1, 
        ncols=1, 
        figsize=None, 
        grid_spec=None,
        args_subplots_adjust=None,
    ):
        """
        Set up plot basic structure
        ARGS:
            nrows:       int - number of rows
            ncols:       int - number of columns
            figsize:    tuple - size of figure
        """
        if grid_spec is None:
            if (nrows == 1) and (ncols == 1):
                self.nrows = nrows
                self.ncols = ncols
                if figsize is None:
                    figsize=(12,12)
                self.fig = plt.figure(figsize=figsize)
                if self.geo_plot:
                    self.axes = np.asarray(plt.axes(
                                    projection=self.nlp['projection']))
                else:
                    self.axes = np.asarray(plt.gca())
            else:
                self.nrows = nrows
                self.ncols = ncols
                if figsize is None:
                    figsize=(ncols*6+2,nrows*6)
                if self.geo_plot:
                    self.fig,self.axes = plt.subplots(
                                nrows,ncols, figsize=figsize,
                                subplot_kw={'projection':self.nlp['projection']})
                else:
                    self.fig,self.axes = plt.subplots( nrows,ncols, figsize=figsize)

            # expand dimensions to always have a 2D axes array
            if nrows < 2:
                self.axes = np.expand_dims(self.axes,axis=0)
            if ncols < 2:
                self.axes = np.expand_dims(self.axes,axis=-1)

            # hide all axes to later only show those with a member
            for axs in self.axes:
                for ax in axs:
                    ax.set_visible(False)

            self.fig.subplots_adjust(**args_subplots_adjust)

        else:
            self.fig = plt.figure(figsize=figsize)
            nrows_tot = nrows*2 - 1
            ncols_tot = ncols*2 - 1
            self.nrows_tot = nrows_tot
            self.ncols_tot = ncols_tot
            if 'widths' not in grid_spec:
                widths = [1 for i in range(ncols)]
            if 'heights' not in grid_spec:
                heights = [1 for i in range(nrows)]
            width_ratios = []
            height_ratios = []
            for coli in range(ncols):
                width_ratios.append(widths[coli])
                if coli < ncols - 1:
                    width_ratios.append(grid_spec['wspaces'][coli])
            for rowi in range(nrows):
                height_ratios.append(heights[rowi])
                if rowi < nrows - 1:
                    height_ratios.append(grid_spec['hspaces'][rowi])
            #print(width_ratios)
            #print(height_ratios)
            gs = GridSpec(
                nrows_tot,
                ncols_tot,
                self.fig, 
                width_ratios=width_ratios, 
                height_ratios=height_ratios, 
            )
            gs.update(**args_subplots_adjust)
            ## manually create axis array
            self.axes = np.full((nrows,ncols),fill_value=None)
            for rowi in range(nrows_tot):
                for coli in range(ncols_tot):
                    #ana_number = pan_cfgs['{},{}'.format(rowi,coli)]['ana_number']
                    ##print(ana_number)
                    #if ana_number in [1]:
                    #    projection = cartopy.crs.PlateCarree()
                    #    ax = self.fig.add_subplot(gs[rowi,coli], projection=projection)
                    #elif ana_number in [4]:
                    #    ax = self.fig.add_subplot(gs[rowi,coli])
                    #else: 
                    #    raise NotImplementedError()
                    ax = self.fig.add_subplot(gs[rowi,coli])
                    ax.set_visible(False)
                    if (rowi % 2 == 0) & (coli % 2 == 0):
                        ri = int((rowi - (rowi % 2))/2)
                        ci = int((coli - (coli % 2))/2)
                        self.axes[ri,ci] = ax

        # create twin x-axis container from axes
        self.axes_twinx = np.full_like(self.axes, None)
        #print(self.axes_twinx)
        #quit()

        return(self.fig, self.axes)


    def get_axis(self, mem_ind, order='cols'):
        """
        Get the axis at the right position depending on the index mem_ind.
        If order=='cols': counting starts in column direction.
        If order=='rows': counting starts in row direction.
        """
        if order == 'cols':
            col_ind = mem_ind % self.ncols
            row_ind = int((mem_ind - col_ind) / self.ncols)
        elif order == 'rows':
            row_ind = mem_ind % self.nrows
            col_ind = int((mem_ind - row_ind) / self.nrows)
        ax = self.axes[row_ind, col_ind]
        return(ax)

    #def has_twin(ax):
    #    for other_ax in ax.figure.axes:
    #        if other_ax is ax:
    #            continue
    #        if other_ax.bbox.bounds == ax.bbox.bounds:
    #            return True
    #    return False

    def remove_axis_labels(self, 
        remove_level=0, 
        xaxis=1, 
        yaxis=1,
        xexcept=[],
        yexcept=[],
        ):
        """
        Remove axis labels if the are not at the outer border
        of the plotting grid.
        remove level:
            0: remove nothing
            1: remove axis labels
            2: remove axis labels and tick labels
        """
        for row_ind in range(self.axes.shape[0]):
            for col_ind in range(self.axes.shape[1]):
                pan_key = '{},{}'.format(row_ind,col_ind)
                #print(pan_key)
                ax = self.axes[row_ind,col_ind]
                ax_twinx = self.axes_twinx[row_ind,col_ind]

                ## y-axes
                if pan_key not in yexcept:

                    ## main y-axis
                    if yaxis and (col_ind > 0):
                        # only remove it if panel left is shown (visible)
                        if self.axes[row_ind, col_ind-1].get_visible():
                            if remove_level >= 1:
                                ax.set_ylabel("")
                            if remove_level == 2:
                                ax.axes.yaxis.set_ticklabels([])

                    ## twinx y-axis
                    if ax_twinx is not None:
                        if yaxis and (col_ind < self.axes.shape[1] - 1):
                            # only remove it if panel left is shown (visible)
                            if self.axes[row_ind, col_ind+1].get_visible():
                                if remove_level >= 1:
                                    ax_twinx.set_ylabel("")
                                if remove_level == 2:
                                    ax_twinx.axes.yaxis.set_ticklabels([])

                else:
                    if isinstance(yexcept[pan_key], dict):
                        axes_exceptions = yexcept[pan_key]
                    else:
                        axes_exceptions = {'main':yexcept[pan_key]}
                    for ax_key,excpt in axes_exceptions.items():
                        ## main y-axis
                        if ax_key == 'main':
                            if excpt >= 1:
                                ax.set_ylabel("")
                            if excpt == 2:
                                ax.axes.yaxis.set_ticklabels([])
                        ## twinx y-axis
                        elif ax_key == 'twinx':
                            if excpt >= 1:
                                ax_twinx.set_ylabel("")
                            if excpt == 2:
                                ax_twinx.axes.yaxis.set_ticklabels([])
                        else:
                            raise ValueError()

                ## main x-axis
                if pan_key not in xexcept:
                    if xaxis and (row_ind < self.axes.shape[0] - 1):
                        # only remove it if panel below is shown (visible)
                        if self.axes[row_ind+1, col_ind].get_visible():
                            if remove_level >= 1:
                                ax.set_xlabel("")
                            if remove_level == 2:
                                ax.axes.xaxis.set_ticklabels([])
                else:
                    if xexcept[pan_key] >= 1:
                        ax.set_xlabel("")
                    if xexcept[pan_key] == 2:
                        ax.axes.xaxis.set_ticklabels([])


    def add_panel_labels(self, order='cols', start_ind=0,
                        shift_right=0.00, shift_up=0.06,
                        fontsize=10):
        """
        Add alphabetic labels to each panel in plot.
        If order=='cols': a b c .. starts in column direction.
        If order=='rows': a b c .. starts in row direction.
        """
        panel_labels = ['a.', 'b.', 'c.', 'd.',
                        'e.', 'f.', 'g.', 'h.',
                        'i.', 'j.', 'k.', 'l.',
                        'm.', 'n.', 'o.', 'p.', 'q.',
                        'r.', 's.', 't.', 'u.',
                        'v.', 'w.', 'x.', 'y.', 'z.',
                        'aa.', 'ab.', 'ac.', 'ad.',
                        'ae.', 'af.', 'ag.', 'ah.',
                        'ai.', 'aj.', 'ak.', 'al.',]
        row_inds = range(self.axes.shape[0])
        col_inds = range(self.axes.shape[1])
        c = start_ind
        for i in row_inds:
            for j in col_inds:
                if order == 'cols':
                    ax = self.axes[i,j]
                elif order == 'rows':
                    ax = self.axes[j,i]
                # only consider visible axes.
                if ax.get_visible():
                    # make panel label
                    pan_lab_x = ax.get_xlim()[0] + (
                                    ax.get_xlim()[1] - ax.get_xlim()[0]) * shift_right
                    pan_lab_y = ax.get_ylim()[1] + (
                                    ax.get_ylim()[1] - ax.get_ylim()[0]) * shift_up
                    ax.text(pan_lab_x, pan_lab_y,
                            panel_labels[c], weight='bold',
                            fontsize=fontsize)
                    c += 1

    #def format_axes(xlabel='', ylabel='', xticks=None, yticks=None,
    #                force_label=False):
    #    if col_ind > 0:
    #        ax.set_yticklabels([]) 
    #        ax.set_ylabel('')
    #    else:

    def add_text_label(self,
        xrel,
        yrel,
        text,
        fontsize=18,
        rotation=0,
        ):
        plt.text(
            xrel, yrel, text, 
            fontsize=fontsize, 
            rotation=rotation, 
            transform=plt.gcf().transFigure,
        )



    def set_axes_labels(self, ax, x_var_name=None,
                                  y_var_name=None,
                                  x_val_type='abs',
                                  y_val_type='abs',
                                  overwrite=True,
                                  same_units=True,
                                  use_name='label',
                                  labelsize=13,
                                  kwargs={}):
        """
        Set axes labels for x and y axis of the given variables
        """
        if x_var_name is not None:
            if ((not overwrite) and (ax.get_xlabel() != '') and same_units):
                append_to = ax.get_xlabel().split(' [')[0] + ', '
            elif ((not overwrite) and (ax.get_xlabel() != '')):
                append_to = ax.get_xlabel() + ', '
            else:
                append_to = ''
            unit = get_plt_units(x_var_name)
            unit = '' if unit == '' else '[{}]'.format(unit)
            if x_val_type == 'diff':
                var_name = '∆{}'.format(nlv[x_var_name][use_name])
            else:
                var_name = '{}'.format(nlv[x_var_name][use_name])
            xlabel = '{}{} {}'.format(append_to, var_name, unit)
            ax.set_xlabel(xlabel, fontsize=labelsize, **kwargs)
        if  y_var_name is not None:
            if ((not overwrite) and (ax.get_ylabel() != '') and same_units):
                append_to = ax.get_ylabel().split(' [')[0] + ', '
            elif ((not overwrite) and (ax.get_ylabel() != '')):
                append_to = ax.get_ylabel() + ', '
            else:
                append_to = ''
            unit = get_plt_units(y_var_name)
            unit = '' if unit == '' else '[{}]'.format(unit)
            if y_val_type == 'diff':
                var_name = '∆{}'.format(nlv[y_var_name][use_name])
            else:
                var_name = '{}'.format(nlv[y_var_name][use_name])
            ylabel = '{}{} {}'.format(append_to, var_name, unit)
            ax.set_ylabel(ylabel, fontsize=labelsize, **kwargs)


    def finalize_plot(self, fig=None):
        """
        Either show, save as png, save as pdf figure.
        ARGS:
            fig:    - matplotlib figure object
        """
        print('finish figure {}'.format(self.path))
        if fig is None:
            fig = self.fig

        if self.i_save_fig == 0:
            img_format = 'png'
            plt.show()
        elif self.i_save_fig == 1:
            img_format = 'png'
        elif self.i_save_fig == 2:
            img_format = 'pdf'
        elif self.i_save_fig == 3:
            img_format = 'jpeg'
        if self.i_save_fig > 0:
            if ('black_bg' in self.nlp) and (self.nlp['black_bg']):
                plt.savefig(self.path, format=img_format,
                            dpi=self.nlp['dpi'],
                            facecolor='black', edgecolor='none')
            elif 'transparent_bg' in self.nlp:
                plt.savefig(self.path, format=img_format,
                            transparent=self.nlp['transparent_bg'],
                            dpi=self.nlp['dpi'])
            else:
                plt.savefig(self.path, format=img_format,
                            dpi=self.nlp['dpi'])
            plt.close(fig.number)
###############################################################################



def get_levels_sym_zero(range, increment):
    return(np.append(np.arange(-range,0,increment),
                    np.arange(increment,range*1.001,increment)))


def draw_map(ax, dom, nlp, add_xlabel=True, add_ylabel=True, dticks=10):
    """
    Draw a nice background map.
    ARGS:
        dom:            dict - domain dictionary from package.domains.py
        add_x/y_label:  log - Should x and y labels be added?
    """
    coastline_resolution = '50m' # '110m', '50m', '10m'

    ax.set_xticks(np.arange(-180,180,dticks), crs=nlp['projection'])
    ax.set_yticks(np.arange(-80,90,dticks), crs=nlp['projection'])
    lon_formatter = LongitudeFormatter(degree_symbol='°',
                                        dateline_direction_label=True)
    ax.xaxis.set_major_formatter(lon_formatter)
    lat_formatter = LatitudeFormatter(degree_symbol='°')
    ax.yaxis.set_major_formatter(lat_formatter)

    xlim = (dom['lon'].start-nlp['map_margin'][0],
            dom['lon'].stop +nlp['map_margin'][1])
    ylim = (dom['lat'].start-nlp['map_margin'][2],
            dom['lat'].stop +nlp['map_margin'][3])
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    if add_xlabel:
        #ax.set_xlabel(nlv['COORD_LON']['label'])
        PlotOrganizer.set_axes_labels(PlotOrganizer, ax, x_var_name='COORD_LON')
    if add_ylabel:
        #ax.set_ylabel(nlv['COORD_LAT']['label'])
        PlotOrganizer.set_axes_labels(PlotOrganizer, ax, y_var_name='COORD_LAT')

    #ax.stock_img()
    ax.coastlines(resolution=coastline_resolution, linewidth=0.2)
    ax.add_feature(cartopy.feature.LAND, color=nlp['land_color'])
    #ax.add_feature(cartopy.feature.OCEAN, color=nlp['ocean_color'])
    #ax.add_feature(cartopy.feature.RIVERS, edgecolor=nlp['river_color'])

    #ax.stock_img()





def draw_domain(ax, dom, nlp, **kwargs):
    """
    Draw a rectangle onto Basemap plot.
    ARGS:
        dom:        dict - domain dictionary from package.domains.py
    OUT:
        handle:     Legend handle for this rectangle.
    """
    if (isinstance(dom['lon'], slice) and 
        isinstance(dom['lat'], slice)):
        lons = [[dom['lon'].start, dom['lon'].stop ],
                [dom['lon'].start, dom['lon'].stop ],
                [dom['lon'].start, dom['lon'].start],
                [dom['lon'].stop , dom['lon'].stop ],
                ]
        lats = [[dom['lat'].start, dom['lat'].start],
                [dom['lat'].stop , dom['lat'].stop ],
                [dom['lat'].start, dom['lat'].stop ],
                [dom['lat'].start, dom['lat'].stop ],
                ]
    elif (isinstance(dom['lon'], slice) and 
          not isinstance(dom['lat'], slice)):
        lons = [[dom['lon'].start, dom['lon'].stop ],
                ]
        lats = [[dom['lat']      , dom['lat']      ],
                ]
    else:
        raise NotImplementedError()
    for i in range(len(lons)):
        handle, = ax.plot(lons[i], lats[i], transform=nlp['projection'],
                          label=dom['label'], **kwargs)

        #ax.plot(np.repeat(dom['lon'][i],2), dom['lat'],
        #            transform=nlp['projection'],
        #            color=color, linestyle=linestyle,
        #            linewidth=linewidth, zorder=zorder)

    return(handle)
