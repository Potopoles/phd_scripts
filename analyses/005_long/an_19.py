#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Cloud size distribution
dependencies    
author			Christoph Heim
date changed    14.06.2022
date changed    14.06.2022
usage           args:
"""
###############################################################################
import os, argparse, copy, sys
max_rec = 100000
sys.setrecursionlimit(max_rec)
print(sys.getrecursionlimit())
#quit()
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.lines import Line2D
from numba import jit, njit
from types import SimpleNamespace
from an_super import Analysis
from package.nl_variables import nlv, get_plt_units, get_plt_fact
from package.utilities import Timer, area_weighted_mean_lat_lon
from package.time_processing import Time_Processing as TP
from package.plot_functions import PlotOrganizer
from package.functions import (import_namelist,
    load_member_var, save_member_to_pickle,
    save_member_var_to_netcdf,
    load_member_from_pickle,
    load_member_var_from_netcdf,
    time_periods_to_dates,
    get_comb_mem_key,
    loc_to_var_name,
    create_dates_code,
    create_combined_member,
)
from package.mp import TimeStepMP
from package.member import Member
from package.var_pp import subsel_alt
from package.model_pp import interp_vprof_with_time
###############################################################################

class Analysis_19(Analysis):

    def __init__(self, nl):
        super(Analysis_19, self).__init__(nl)
        self.nl = nl
        self.ana_number = 19


    def draw_axis_contour(self, PO, members, axes):

        if len(members) == 0:
            print('WARNING: No members to plot!')
            return()

        plot_data = {}
        for mem_key, member in members.items():
            print(mem_key)
            mem_dict = copy.copy(member.mem_dict)
            val_type  = member.val_type

            raw_mem_key = mem_key.split('#time#')[0]

            agg_var_name = next(iter(member.vars))
            var_name = TP.get_var_name(agg_var_name)

            ### MEMBER SPECIFIC PROPERTIES
            ##################################################################

            cell_size = self.nl.plot_cfg[var_name]['dx']**2

            bins_sizes = np.concatenate([
                #np.arange(1,10)*cell_size, 
                #np.logspace(1.0,3.0,15)*cell_size,
                #np.logspace(1.0,3.0,5)*cell_size,
                np.logspace(0,3,7)*cell_size,
            ])
            bins_clwcs = np.arange(0,0.41,0.05)
            zlims = dict(
                abs=(1E-7,1E-1),
                rel=(-30,30),
            )
            ctrl_numb_thresh = 30


            vlev = self.nl.vlev
            sizes = member.vars[agg_var_name]['sizes'][vlev] * cell_size
            clwcs = member.vars[agg_var_name]['clwcs'][vlev] * get_plt_fact('QC')
            nclouds = sizes.size
            print(nclouds)
            #quit()

            H,size_edges,clwc_edges = np.histogram2d(
                sizes, clwcs,
                bins=(bins_sizes, bins_clwcs),
                density=True
            )
            H = H.T
            print(H)
            print(H.shape)
            print(size_edges)
            print(clwc_edges)


            X, Y = np.meshgrid(size_edges, clwc_edges)

            plot_data[raw_mem_key] = dict(H=H, X=X, Y=Y)


        ctrl_mem_key = 'COSMO_3.3_ctrl'
        pgw_mem_key = 'COSMO_3.3_pgw'


        ax = axes[0,0]
        ax.set_facecolor('grey')
        self.draw_axis_DEFAULT(ax)
        cmap = 'jet'
        norm = mcolors.LogNorm(vmin=zlims['abs'][0], vmax=zlims['abs'][1])
        im = ax.pcolormesh(
            plot_data[ctrl_mem_key]['X'], 
            plot_data[ctrl_mem_key]['Y'], 
            plot_data[ctrl_mem_key]['H'], 
            cmap=cmap, 
            norm=norm
        )
        fig.colorbar(im, ax=ax)
        ax.set_xscale('log')

        ax = axes[0,1]
        ax.set_facecolor('grey')
        self.draw_axis_DEFAULT(ax)
        cmap = 'RdBu_r'
        norm = mcolors.Normalize(vmin=zlims['rel'][0], vmax=zlims['rel'][1])
        rel_data = (plot_data[pgw_mem_key]['H'] / plot_data[ctrl_mem_key]['H'] - 1)*100
        # mask if number of clouds in CTRL for this bin is too low
        rel_data[plot_data[ctrl_mem_key]['H'] < ctrl_numb_thresh/nclouds] = np.nan
        im = ax.pcolormesh(
            plot_data[ctrl_mem_key]['X'], 
            plot_data[ctrl_mem_key]['Y'], 
            rel_data, 
            cmap=cmap, 
            norm=norm
        )
        fig.colorbar(im, ax=ax)
        ax.set_xscale('log')



    def draw_axis(self, PO, members, ax):
        self.draw_axis_DEFAULT(ax)

        if len(members) == 0:
            print('WARNING: No members to plot!')
            return()

        mem_ind = 0
        mem_keys = []
        for mem_key, member in members.items():
            print(mem_key)
            mem_keys.append(mem_key)
            mem_dict = copy.copy(member.mem_dict)
            val_type  = member.val_type

            raw_mem_key = mem_key.split('#time#')[0]

            agg_var_name = next(iter(member.vars))
            var_name = TP.get_var_name(agg_var_name)

            ### MEMBER SPECIFIC PROPERTIES
            ##################################################################
            ### color
            if self.nl.ref_key is not None and self.nl.ref_key in mem_key: 
                color = self.nl.nlp['ref_color']
            elif self.nl.ref2_key is not None and self.nl.ref2_key in mem_key: 
                color = self.nl.nlp['ref2_color']
            else:
                if raw_mem_key in self.nl.nlp['mem_colors']: 
                    color = self.nl.nlp['mem_colors'][raw_mem_key]
                elif member.mem_dict['label'] in self.nl.nlp['mem_colors']: 
                    color = self.nl.nlp['mem_colors'][member.mem_dict['label']]
                else:
                    color = '#BBBBBB'

            #### linestyle
            #if self.nl.ref_key is not None and self.nl.ref_key in mem_key: 
            #    linestyle = self.nl.nlp['ref_linestyle']
            #elif self.nl.ref2_key is not None and self.nl.ref2_key in mem_key: 
            #    linestyle = self.nl.nlp['ref2_linestyle']
            #elif raw_mem_key in self.nl.nlp['mem_linestyles']: 
            #    linestyle = self.nl.nlp['mem_linestyles'][raw_mem_key]
            #elif member.mem_dict['label'] in self.nl.nlp['mem_linestyles']: 
            #    linestyle = self.nl.nlp['mem_linestyles'][member.mem_dict['label']]
            #else:
            #    linestyle = '-'


            ### linewidth
            linewidth = 1.5

            cell_size = self.nl.plot_cfg[var_name]['dx']**2

            bins = np.concatenate([
                np.arange(1,10)*cell_size, 
                np.logspace(1.0,3.0,15)*cell_size,
            ])
            ylims = (1E-7,1E-2)


            ### DRAW PLOT LINES
            ##################################################################
            for vi,vlev in enumerate(self.nl.plot_cfg[var_name]['vlevs']):
                print(vlev)
                print(member.vars[agg_var_name][vlev].shape)

                linestyle = ['-','--',':'][vi]
                label = '{} {}z/z$_i$'.format(member.mem_dict['label'], vlev)

                #ax.hist(
                #    member.vars[agg_var_name][vlev]*self.nl.plot_cfg[var_name]['dx']**2, 
                #    bins=bins, 
                #    density=True, 
                #    histtype='step',
                #    color=color, 
                #    linestyle = linestyle,
                #    label=label,
                #)

                n, x  = np.histogram(
                    member.vars[agg_var_name][vlev]*cell_size, 
                    bins=bins, 
                    density=True, 
                )
                bin_centers = 0.5*(x[1:]+x[:-1])
                handle, = ax.plot(
                    bin_centers,n,
                    color=color, 
                    linestyle = linestyle,
                    label=label,
                ) 
                PO.handles.append(handle)

            mem_ind += 1

        ### DRAW RATIO LINES
        ##################################################################
        color = 'k'
        ax2 = ax.twinx()
        ax2.set_ylim(0.6,1.4)
        ax2.axhline(y=1, color='grey', linewidth=0.5)
        for vi,vlev in enumerate(self.nl.plot_cfg[var_name]['vlevs']):

            linestyle = ['-','--',':'][vi]

            #ax.hist(
            #    member.vars[agg_var_name][vlev]*self.nl.plot_cfg[var_name]['dx']**2, 
            #    bins=bins, 
            #    density=True, 
            #    histtype='step',
            #    color=color, 
            #    linestyle = linestyle,
            #    label=label,
            #)

            npgw,x  = np.histogram(
                members[mem_keys[1]].vars[agg_var_name][vlev]*cell_size, 
                bins=bins, 
                density=True, 
            )
            nctrl,x  = np.histogram(
                members[mem_keys[0]].vars[agg_var_name][vlev]*cell_size, 
                bins=bins, 
                density=True, 
            )
            handle, = ax2.plot(
                bin_centers,npgw/nctrl,
                color=color, 
                linestyle = linestyle,
            ) 
            #PO.handles.append(handle)

            # number of clouds ratio
            tot_n_ratio_pgw_to_ctrl = (
                len(members[mem_keys[1]].vars[agg_var_name][vlev]) /
                len(members[mem_keys[0]].vars[agg_var_name][vlev])
            )
            # cloud area ratio
            tot_A_ratio_pgw_to_ctrl = (
                np.sum(members[mem_keys[1]].vars[agg_var_name][vlev]) /
                np.sum(members[mem_keys[0]].vars[agg_var_name][vlev])
            )
            ax2.text(
                4E2,0.68-vi*0.05,
                'z/z$_i$={}: n: {:4.3f} A: {:4.3f}'.format(
                    vlev,
                    tot_n_ratio_pgw_to_ctrl,
                    tot_A_ratio_pgw_to_ctrl,
                )
            )

        ### FORMAT AXIS
        ######################################################################
        ## Create new legend handles but use the colors from the existing ones
        #handles, labels = ax.get_legend_handles_labels()
        #new_handles = [Line2D([], [], c=h.get_edgecolor()) for h in handles]
        #ax.legend(handles=new_handles, labels=labels)
        ax.legend(handles=PO.handles, loc='lower left')

        #xlims = (0,100)
        ax.set_yscale('log')
        ax.set_xscale('log')
        ax.set_ylim(ylims)




    def compute_src_members_for_date(self, ts):
        """
        Organize full analysis for a given date (ts).
        ts has to be called ts because compute_for_date is called from TimeStepMP.
        """
        #print(ts)

        if (self.nl.i_debug >= 1) and (ts.day == 1):
            print('Start processing month {:%Y%m}.'.format(ts))

        ######## LOAD MEMBERS
        ##########################################################################
        members = {}
        for mem_key,mem_dict in self.src_mem_dict.items():
            #print(mem_key)
            # create member instance
            members[mem_key] = Member(mem_dict, val_type='abs')
            # set time key
            members[mem_key].time_key = 'time'

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
                        loc_value = float(loc_var_name.split('@')[1].split('=')[1])
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

                    # load variable
                    qc = load_member_var('QCNORMI', mem_dict['freq'],
                                        ts, ts, mem_dict,
                                        self.nl.var_src_dict,
                                        self.nl.mean_var_src_dict,
                                        self.nl.var_src_dict['QCNORMI']['load'],
                                        domain=self.nl.var_dom_map[loc_var_name],
                                        i_debug=self.nl.i_debug,
                                        dask_chunks=self.nl.dask_chunks)
                    #var.to_netcdf('test.nc')
                    #print(qc)
                    #quit()
                if var is not None:
                    # compute variable
                    var = self.compute_var(var, qc)
                    members[mem_key].add_var(loc_var_name, var)

                else:
                    # free up memory
                    try:
                        del members[mem_key].mem_dict 
                    except AttributeError:
                        pass

                    members[mem_key].add_var(loc_var_name, None)

        output = {'members':members}
        return(output)


    def compute_var(self, var, qc=None):
        # only use relative altitude up to inversion
        if 'rel_alt' in var.dims:
            var = var.sel(rel_alt=slice(0.1,1.2))

        nhori_sizes = 100000
        clusters = xr.full_like(var, -1)
        # either find clusters on time/lat/lon or time/alt/lat/lon grid
        if ('alt' in var.dims) or ('rel_alt' in var.dims):
            ## this is a time/alt/horizontal array
            sizes = np.full((var.values.shape[0],var.values.shape[1],nhori_sizes), np.nan)
            if qc is not None:
                clwcs = np.full((var.values.shape[0],var.values.shape[1],nhori_sizes), np.nan)
                use_qc = qc.values
            else:
                clwcs = None
                use_qc = None
            clusters.values,sizes,clwcs = find_clusters_3D(
                var.values, clusters.values, sizes, clwcs, use_qc
            )
            #print(clwcs)
            clusters.to_netcdf('test.nc')
            quit()
            ## flatten time dimension
            sizes_2d = sizes.transpose(1,0,2).reshape(sizes.shape[1],-1)
            clwcs_2d = clwcs.transpose(1,0,2).reshape(clwcs.shape[1],-1)
            # split up into dict with individual vertical levels
            output = dict(sizes={}, clwcs={})
            for i,rel_alt in enumerate(var.rel_alt.values):
                output['sizes'][rel_alt] = sizes_2d[i,:][~np.isnan(sizes_2d[i,:])]
                output['clwcs'][rel_alt] = clwcs_2d[i,:][~np.isnan(clwcs_2d[i,:])]
                #output['clwcs'][rel_alt] = clwcs_2d[i,:]
                #output['clwcs'][rel_alt] = clwcs[rel_alt][~np.isnan(clwcs[rel_alt])]
            #print(output['sizes'][0.2])
            #print(output['clwcs'][0.2])
            #quit()
        else:
            # this is a time/horizontal array
            sizes = np.full((var.values.shape[0],nhori_sizes), np.nan)
            clusters.values,sizes = find_clusters_2D(var.values, clusters.values, sizes)
            ## flatten time dimension
            sizes = sizes.flatten()
            sizes = sizes[~np.isnan(sizes)]
            sizes = dict(lev=sizes)
        return(output)


    def prepare_namelist(self):
        self.nl.pickle_append = ""

        self.prepare_namelist_DEFAULT()


@njit
def add_new_cluster_3D(
        var, qc, clusters, timi, alti, lati, loni, 
        cluster_ind, size, clwc, clwc_sum, rec_count
    ):
    if ~np.isnan(var[timi,alti,lati,loni]):
        if clusters[timi,alti,lati,loni] == -1:
            if var[timi,alti,lati,loni] > 0.5:
                clusters[timi,alti,lati,loni] = cluster_ind
                size += 1
                if clwc is not None:
                    if ~np.isnan(qc[timi,alti,lati,loni]):
                    #if qc[timi,alti,lati,loni] != np.nan:
                        clwc += qc[timi,alti,lati,loni]
                        clwc_sum += 1
                if rec_count <= max_rec:
                    rec_count += 1
                    # look in meridional neighbors
                    for lati2 in [lati-1,lati+1]:
                        # consider boundaries
                        if (lati2 >= 0) and (lati2 < var.shape[2]):
                            size,clwc,clwc_sum,rec_count = add_new_cluster_3D(
                                var, qc, clusters, timi, alti, lati2, loni , 
                                cluster_ind, size, clwc, clwc_sum, rec_count)
                    # look in zonal neighbors
                    for loni2 in [loni-1,loni+1]:
                        # consider boundaries
                        if (loni2 >= 0) and (loni2 < var.shape[3]):
                            size,clwc,clwc_sum,rec_count = add_new_cluster_3D(
                                var, qc, clusters, timi, alti, lati , loni2, 
                                cluster_ind, size, clwc, clwc_sum, rec_count)
                return(size,clwc,clwc_sum,rec_count)
            else:
                clusters[timi,alti,lati,loni] = np.nan
                return(size,clwc,clwc_sum,rec_count)
        else:
            return(size,clwc,clwc_sum,rec_count)
    else:
        clusters[timi,alti,lati,loni] = np.nan
        return(size,clwc,clwc_sum,rec_count)

@njit
def find_clusters_3D(var, clusters, sizes, clwcs=None, qc=None):
    for timi in range(var.shape[0]):
        #print(timi)
        for alti in range(var.shape[1]):
            #print(alti)
            cluster_ind = 0
            for lati in range(var.shape[2]):
                for loni in range(var.shape[3]):
                    if clwcs is not None:
                        clwc_0 = 0
                    else:
                        clwc_0 = None
                    size,clwc,clwc_sum,rec_count = add_new_cluster_3D(
                            var, qc, clusters, timi, alti, lati, loni, 
                            cluster_ind, size=0, clwc=clwc_0, clwc_sum=0, 
                            rec_count=0
                    )
                    if size > 0:
                        sizes[timi,alti,cluster_ind] = size
                        if clwcs is not None:
                            if clwc_sum > 0:
                                clwcs[timi,alti,cluster_ind] = clwc/clwc_sum
                            else:
                                clwcs[timi,alti,cluster_ind] = -1
                        #print('{}: {}'.format(cluster_ind, clwcs[timi,alti,cluster_ind]))
                        cluster_ind += 1
                        #if cluster_ind == 100:
                        #    return(clusters,sizes,clwcs)
    return(clusters,sizes,clwcs)





@njit
def add_new_cluster_2D(var, clusters, timi, lati, loni, cluster_ind, size):
    if ~np.isnan(var[timi,lati,loni]):
        if clusters[timi,lati,loni] == -1:
            if var[timi,lati,loni] > 0.5:
                clusters[timi,lati,loni] = cluster_ind
                size += 1
                # look in meridional neighbors
                for lati2 in [lati-1,lati+1]:
                    # consider boundaries
                    if (lati2 >= 0) and (lati2 < var.shape[1]):
                        size = add_new_cluster_2D(var, clusters, timi, lati2, loni , cluster_ind, size)
                # look in zonal neighbors
                for loni2 in [loni-1,loni+1]:
                    # consider boundaries
                    if (loni2 >= 0) and (loni2 < var.shape[2]):
                        size = add_new_cluster_2D(var, clusters, timi, lati , loni2, cluster_ind, size)
                return(size)
            else:
                clusters[timi,lati,loni] = np.nan
                return(size)
        else:
            return(size)
    else:
        clusters[timi,lati,loni] = np.nan
        return(size)

@njit
def find_clusters_2D(var, clusters, sizes):
    for timi in range(var.shape[0]):
        cluster_ind = 0
        for lati in range(var.shape[1]):
            for loni in range(var.shape[2]):
                size = add_new_cluster_2D(var, clusters, timi, lati, loni, cluster_ind, size=0)
                if size > 0:
                    sizes[timi,cluster_ind] = size
                    cluster_ind += 1
                    #if np.nanmax(clusters) == 20:
                    #    return(clusters)
    return(clusters,sizes)


if __name__ == '__main__':
    # READ INPUT ARGUMENTS
    ###########################################################################
    parser = argparse.ArgumentParser(description = 'Draw skew-T plot.')
    ## variables to plot
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
    import nl_19 as nl_ana_raw
    from nl_plot_19 import nlp
    ana = Analysis_19(nl=SimpleNamespace())
    import_namelist(ana.nl, nl_ana_raw)
    ana.nl.nlp = nlp

    # input arguments
    #ana.nl.var_names = args.var_names.split(',')
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
        first_mem_key,first_mem = next(iter(tsmp.output[0]['members'].items()))
        vlevs = list(first_mem.vars[ana.nl.var_names[0]]['sizes'].keys())
        indiv_targ_members = {}
        for mem_key,member in tsmp.output[0]['members'].items():
            print(mem_key)
            all_vars = {}
            for var_name in ['sizes','clwcs']:
                concat = {}
                for vlev in vlevs:
                    indiv = []
                    for ts_output in tsmp.output:
                        output = ts_output['members'][mem_key].vars[ana.nl.var_names[0]][var_name][vlev]
                        #print(output)
                        indiv.append(output)
                    concat[vlev] = np.concatenate(indiv)
                all_vars[var_name] = concat

            #for var_name,var in all_vars.items():
            #    print(var_name)
            #    for lev,vals in var.items():
            #        print(lev)
            #        print(vals.size)
            #quit()

            member = Member(member.mem_dict, val_type='abs')
            member.dates_code = create_dates_code(ana.iter_dates)
            member.add_var(
                TP.get_agg_var_name(ana.nl.var_names[0], ana.nl.agg_level),
                all_vars)
            indiv_targ_members[mem_key] = member
        timer.stop('daily')

        ## PART OF ANALYSIS FOR ENTIRE TIME SERIES
        #######################################################################
        ## compute aggregation/grouping on entire time series
        #timer.start('all')
        #ana.indiv_targ_members = ana.aggreg_src_members_to_indiv_targ_members(
        #                                src_members)
        #timer.stop('all')


        # SAVE DATA TO PICKLE
        ######################################################################
        ana.save_data(indiv_targ_members, netcdf=False)

    # ... or be reloaded from precomputed pickle files.
    else:
        # LOAD PRECOMPUTED DATA FROM PICKLE
        ######################################################################
        ana.indiv_targ_members = ana.load_data(netcdf=False)

    # PLOTTING
    ##########################################################################
    if ana.nl.i_plot:
        timer.start('prepare')
        #targ_members = ana.prepare_for_plotting(ana.indiv_targ_members)

        #### SET UP TIME SELECTORS FOR PLOTS WITH MULTIPLE TIME STEPS
        ## determine number of time steps to plot
        #dummy_member = targ_members[list(targ_members.keys())[0]]
        #var = dummy_member.vars[list(dummy_member.vars.keys())[0]]
        #if var.attrs['time_key'] != 'None':
        #    nts_plt = len(var[var.attrs['time_key']])
        #    time_plt_sels = []
        #    for tind in range(nts_plt):
        #        time_plt_sels.append({
        #        var.attrs['time_key'] : var[var.attrs['time_key']].isel(
        #                    {var.attrs['time_key']:tind}).values
        #    })
        #else:
        #    time_plt_sels = [None]

        timer.stop('prepare')

        ## SET UP PLOT IO PATH
        ######################################################################
        timer.start('plot')
        name_dict = {}
        #name_dict['cldsize'] = ana.nl.plot_domain['key']
        #name_dict[ana.nl.var_names[0]] = ''
        name_dict['cldsize2D'] = ana.nl.plot_domain['key']
        name_dict[ana.nl.var_names[0]] = ana.nl.vlev
        if ana.nl.plot_append != '':
            name_dict[ana.nl.plot_append] = ''

        ## INITIALIZE PLOT
        ######################################################################
        PO = PlotOrganizer(i_save_fig=ana.nl.i_save_fig,
                          path=os.path.join(ana.nl.plot_base_dir),
                          name_dict=name_dict, nlp=ana.nl.nlp, geo_plot=False)
        fig,axes = PO.initialize_plot(nrows=ana.nl.nrows,
                                      ncols=ana.nl.ncols,
                                      figsize=ana.nl.figsize)
        #PO = None


        ### DRAW AXES
        ######################################################################
        #ana.draw_axis(PO, ana.indiv_targ_members, PO.get_axis(0))
        ana.draw_axis_contour(PO, ana.indiv_targ_members, axes)

        #PO.remove_axis_labels()

        ### FINAL FORMATTING
        ######################################################################
        fig.subplots_adjust(**ana.nl.arg_subplots_adjust)

        #PO.add_panel_labels(order='cols')

        PO.finalize_plot()
        timer.stop('plot')

    timer.print_report()
