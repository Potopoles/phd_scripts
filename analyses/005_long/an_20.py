#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Cloud 3D structure
dependencies    
author			Christoph Heim
date changed    14.06.2022
date changed    22.06.2022
usage           args:
"""
###############################################################################
import os, argparse, copy, sys, numba
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
#from numba  import int32
from types import SimpleNamespace
from an_super import Analysis
from package.nl_variables import nlv, get_plt_units, get_plt_fact
from package.utilities import Timer
from package.time_processing import Time_Processing as TP
from package.plot_functions import PlotOrganizer
from package.functions import (import_namelist,
    load_member_var, save_member_to_pickle,
    save_member_var_to_netcdf,
    load_member_from_pickle,
    load_member_var_from_netcdf,
    create_dates_code,
)
from package.mp import TimeStepMP
from package.member import Member
from package.model_pp import interp_vprof_with_time
from an_20_functions import (
    compute_and_save_clusters,
    load_clusters,
    cloud_statistics,
)
###############################################################################



def filter_rel_alt(var, filter_type):
    size_before = np.sum(~np.isnan(var))
    if filter_type == 'deep_clouds':
        must_have = [0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
        must_not_have = []
        for ra in must_have:
            var = var.where(~np.isnan(var.sel(rel_alt=ra, method='nearest')))
        for ra in must_not_have:
            var = var.where(np.isnan(var.sel(rel_alt=ra, method='nearest')))
    elif filter_type == 'shallow_clouds':
        must_have = []
        must_not_have = [0.7,0.8,0.9,1.0,1.1]
        for ra in must_have:
            var = var.where(~np.isnan(var.sel(rel_alt=ra, method='nearest')))
        for ra in must_not_have:
            var = var.where(np.isnan(var.sel(rel_alt=ra, method='nearest')))
    elif filter_type == 'inversion_clouds':
        must_have = [0.7,0.8,0.9,1.0,1.1]
        must_not_have = [0.0,0.1,0.2,0.3,0.4,0.5,0.6]
        for ra in must_have:
            var = var.where(~np.isnan(var.sel(rel_alt=ra, method='nearest')))
        for ra in must_not_have:
            var = var.where(np.isnan(var.sel(rel_alt=ra, method='nearest')))
    elif filter_type == 'all_clouds':
        pass
    else:
        raise NotImplementedError()
    size_after = np.sum(~np.isnan(var))
    print('filtered to {:d}.'.format(int((size_after/size_before*100).values)))
    return(var)

class Analysis_20(Analysis):

    def __init__(self, nl):
        super(Analysis_20, self).__init__(nl)
        self.nl = nl
        self.ana_number = 20


    def plot_lines(self, members, ax, PO):
        for mem_key,member in members.items():
            val_type = 'abs'

            var_name = 'CORE_CLOUD_AREA'
            var = filter_rel_alt(member.vars[var_name], self.nl.filter_type)
            var = np.sqrt(var.mean(dim='cli')/np.pi)
            handle, = ax.plot(
                var.values,
                var.rel_alt*get_plt_fact('COORD_RELALT'),
                zorder=2,
                color=self.nl.nlp['mem_colors'][member.mem_dict['label']],
                label=member.mem_dict['label']
            )
            PO.handles.append(handle)

            var_name = 'BOTH_CLOUD_AREA'
            var = filter_rel_alt(member.vars[var_name], self.nl.filter_type)
            var = np.sqrt(var.mean(dim='cli')/np.pi)
            ax.plot(
                var.values,
                var.rel_alt*get_plt_fact('COORD_RELALT'),
                zorder=2,
                color=self.nl.nlp['mem_colors'][member.mem_dict['label']],
            )

            var = filter_rel_alt(member.vars[var_name], self.nl.filter_type)
            var = np.sqrt(var.quantile(dim='cli', q=0.9)/np.pi)
            ax.plot(
                var.values,
                var.rel_alt*get_plt_fact('COORD_RELALT'),
                zorder=2,
                linestyle='--',
                color=self.nl.nlp['mem_colors'][member.mem_dict['label']],
            )

            var = filter_rel_alt(member.vars[var_name], self.nl.filter_type)
            var = np.sqrt(var.quantile(dim='cli', q=0.99)/np.pi)
            ax.plot(
                var.values,
                var.rel_alt*get_plt_fact('COORD_RELALT'),
                zorder=2,
                linestyle=':',
                color=self.nl.nlp['mem_colors'][member.mem_dict['label']],
            )

    def draw_axis(self, PO, members, axes):

        ctrl_mem_key = 'COSMO_3.3_ctrl#time#{}'.format(
            create_dates_code(self.iter_dates))
        pgw_mem_key = 'COSMO_3.3_pgw#time#{}'.format(
            create_dates_code(self.iter_dates))
        ctrl_member = members[ctrl_mem_key]
        pgw_member = members[pgw_mem_key]

        ### LEFT AND MIDDLE AXES
        ######################################################################
        for mem_ind,mem_key in enumerate([ctrl_mem_key, pgw_mem_key]):
            ax = axes[0,mem_ind]
            self.draw_axis_DEFAULT(ax)
            ax.set_xlim(0,66)
            #ax.set_xlim(0,0.5)
            ax.set_ylim(0,1.2)

            ### plot vertical cloud shape lines
            self.plot_lines(members, ax, PO)

            member = members[mem_key]
            val_type = 'abs'
            var_name = self.nl.main_var_name 
            #plot_var = member.vars['CORE_TANGMEAN_{}'.format(self.nl.main_var_name)]
            #plot_var = member.vars['STRAT_TANGMEAN_{}'.format(self.nl.main_var_name)]
            plot_var = member.vars['BOTH_TANGMEAN_{}'.format(self.nl.main_var_name)]
            plot_var = filter_rel_alt(plot_var, self.nl.filter_type).mean(dim='cli')
            plot_var = plot_var.assign_coords(
                {'rel_alt':plot_var.rel_alt.values*get_plt_fact('COORD_RELALT')})
            plot_var = plot_var * get_plt_fact(var_name)
            plot_var = plot_var.where(np.isnan(plot_var) | (plot_var >= 
                            np.min(self.nl.nlp['levels']['cf'][val_type][var_name])),
                            0.99*np.min(self.nl.nlp['levels']['cf'][val_type][var_name]))
            plot_var = plot_var.where(np.isnan(plot_var) | (plot_var <= 
                            np.max(self.nl.nlp['levels']['cf'][val_type][var_name])),
                            0.99*np.max(self.nl.nlp['levels']['cf'][val_type][var_name]))

            plot_var.plot.contourf(
                ax=ax,
                zorder=1,
                cmap=self.nl.nlp['cmaps']['cf'][val_type][var_name],
                levels=self.nl.nlp['levels']['cf'][val_type][var_name],
            )

            if mem_ind == 0:
                ax.legend(handles=PO.handles)


        ### RIGHT AXIS
        ######################################################################
        ax = axes[0,2]
        self.draw_axis_DEFAULT(ax)
        ax.set_xlim(0,66)
        #ax.set_xlim(0,0.5)
        ax.set_ylim(0,1.2)

        ### plot vertical cloud shape lines
        self.plot_lines(members, ax, PO)
        
        val_type = 'diff'
        var_name = self.nl.main_var_name 
        plot_var = (
            filter_rel_alt(
                pgw_member.vars[
                    'BOTH_TANGMEAN_{}'.format(self.nl.main_var_name)], 
                self.nl.filter_type
            ).mean(dim='cli')
            -
            filter_rel_alt(
                ctrl_member.vars[
                    'BOTH_TANGMEAN_{}'.format(self.nl.main_var_name)], 
                self.nl.filter_type
            ).mean(dim='cli')
        )
        plot_var = plot_var.assign_coords(
            {'rel_alt':plot_var.rel_alt.values*get_plt_fact('COORD_RELALT')})
        plot_var = plot_var * get_plt_fact(var_name)
        plot_var = plot_var.where(np.isnan(plot_var) | (plot_var >= 
                        np.min(self.nl.nlp['levels']['cf'][val_type][var_name])),
                        0.99*np.min(self.nl.nlp['levels']['cf'][val_type][var_name]))
        plot_var = plot_var.where(np.isnan(plot_var) | (plot_var <= 
                        np.max(self.nl.nlp['levels']['cf'][val_type][var_name])),
                        0.99*np.max(self.nl.nlp['levels']['cf'][val_type][var_name]))

        plot_var.plot.contourf(
            ax=ax,
            zorder=1,
            cmap=self.nl.nlp['cmaps']['cf'][val_type][var_name],
            levels=self.nl.nlp['levels']['cf'][val_type][var_name],
        )




    def prepare_namelist(self):
        self.nl.pickle_append = ""

        if 'QC' not in self.nl.var_names:
            self.nl.var_names.append('QC')
        if 'W' not in self.nl.var_names:
            self.nl.var_names.append('W')

        self.prepare_namelist_DEFAULT()

        # add manually defined variables
        for var_name in self.nl.comp_var_names:
            self.nl.var_dom_map[var_name] = self.nl.plot_domain
            self.nl.load_agg_var_names.append(var_name)




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
                if var is not None:
                    # make sure all monthly data has first date of month
                    # as time stamp (this is assumed later on)
                    if mem_dict['freq'] == 'monthly':
                        new_time = [dt64_to_dt(var.time.values[0]).replace(day=1)]
                        var = var.assign_coords(time=new_time)
                    # optionally subselect specified altitude
                    if loc_dim is not None:
                        if loc_value in var[loc_dim]:
                            var = var.sel({loc_dim:loc_value})
                        else:
                            var = var.interp({loc_dim:loc_value})
                    # compute variable
                    var = self.compute_var(var)
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

            # compute clustering for convective cores
            if self.nl.i_recompute_clusters:
                compute_and_save_clusters(self, members[mem_key], ts)
            else:
                load_clusters(self, members[mem_key], ts)

            ### compute all cloud statistics
            if self.nl.i_recompute_statistics:
                print('compute statistics')
                self.compute_cloud_statistics(members[mem_key])

            ### delete raw data because it is huge
            del_var_names = []
            for var_name,var in members[mem_key].vars.items():
                if var_name not in self.nl.comp_var_names:
                    del_var_names.append(var_name)
            for var_name in del_var_names:
                del members[mem_key].vars[var_name]

        output = {'members':members}
        return(output)


    def compute_var(self, var):
        # consider only lower troposphere
        if 'alt' in var.dims:
            var = var.sel(alt=slice(0,4000))
        return(var)


    def compute_cloud_statistics(self, member):

        norm_inv = 1
        rel_alt_coord = np.arange(0.0,1.1*1.01,0.1)
        alt_coord = member.vars[self.nl.main_var_name].alt.values
        if norm_inv:
            vert_coord_use = rel_alt_coord
            vert_dim_name = 'rel_alt'
        else:
            vert_coord_use = alt_coord
            vert_dim_name = 'alt'

        rad_min = 0
        rad_max = 66
        drad = 6.6
        radbins = np.arange(rad_min,rad_max*1.01,drad)

        CORES = member.vars['CORES']
        STRATS = member.vars['STRATS']

        ### DEFINE XARRAY DATAARRAYS FOR OUTPUT VARIABLES
        ######################################################################
        CORE_TANGMEAN_VAR = xr.DataArray(
            data=np.full((len(vert_coord_use),len(radbins),len(CORES)), np.nan), 
            coords={
                vert_dim_name:  rel_alt_coord,
                'rad':          radbins,
                'cli':          np.arange(len(CORES)),
            },
        )
        CORE_CLOUD_AREA = xr.DataArray(
            data=np.full((len(vert_coord_use),len(CORES)), np.nan), 
            coords={
                vert_dim_name:  rel_alt_coord,
                'cli':          np.arange(len(CORES)),
            },
        )

        STRAT_TANGMEAN_VAR = CORE_TANGMEAN_VAR.copy()
        BOTH_TANGMEAN_VAR = CORE_TANGMEAN_VAR.copy()

        STRAT_CLOUD_AREA = CORE_CLOUD_AREA.copy()
        BOTH_CLOUD_AREA = CORE_CLOUD_AREA.copy()

        for cli in range(len(CORES)):
            #print('################# {:4.2f}'.format(cli/len(CORES)))

            c_inds = CORES[cli]
            s_inds = STRATS[cli]
            ## combine cores and strats together to cores&strats (both)
            b_inds = dict()
            for dim in ['timi','alti','lati','loni']:
                b_inds[dim] = xr.concat([c_inds[dim], s_inds[dim]], dim='gp')

            # compute merged latlon index for each vertical column
            c_latloni = numba.typed.List()
            s_latloni = numba.typed.List()
            b_latloni = numba.typed.List()
            ll = list(set([i for i in zip(c_inds['lati'].values,c_inds['loni'].values)]))
            [c_latloni.append(x) for x in ll]
            # this is necessary because s_latoni can be empty and thus data type
            # cannot be determined from fill elements
            # thus use data type from c_latloni
            s_latloni.append(ll[0])
            ll = list(set([i for i in zip(s_inds['lati'].values,s_inds['loni'].values)]))
            [s_latloni.append(x) for x in ll]
            s_latloni.pop(0)
            ll = list(set([i for i in zip(b_inds['lati'].values,b_inds['loni'].values)]))
            [b_latloni.append(x) for x in ll]

            (
                c_cloud_area,
                s_cloud_area,
                b_cloud_area,
                c_tangmean_qc,
                s_tangmean_qc,
                b_tangmean_qc,
            ) = cloud_statistics(
                c_inds['timi'].values, 
                c_inds['alti'].values, 
                c_inds['lati'].values, 
                c_inds['loni'].values, 
                c_latloni,

                s_inds['timi'].values, 
                s_inds['alti'].values, 
                s_inds['lati'].values, 
                s_inds['loni'].values, 
                s_latloni,

                b_inds['timi'].values, 
                b_inds['alti'].values, 
                b_inds['lati'].values, 
                b_inds['loni'].values, 
                b_latloni,

                norm_inv,
                alt_coord,
                rel_alt_coord,
                radbins,
                self.nl.model_dx,

                member.vars[self.nl.main_var_name].values,
                member.vars['W'].values,
                member.vars['INVHGT'].values,
            )
            #if cli == 0:
            #    quit()

            loc_dict = dict(cli=cli)
            CORE_CLOUD_AREA.loc[loc_dict] = c_cloud_area
            STRAT_CLOUD_AREA.loc[loc_dict] = s_cloud_area
            BOTH_CLOUD_AREA.loc[loc_dict] = b_cloud_area
            CORE_TANGMEAN_VAR.loc[loc_dict] = c_tangmean_qc
            STRAT_TANGMEAN_VAR.loc[loc_dict] = s_tangmean_qc
            BOTH_TANGMEAN_VAR.loc[loc_dict] = b_tangmean_qc

        #print(CORE_TANGMEAN_VAR.mean(dim='cli'))
        #print(STRAT_TANGMEAN_VAR.mean(dim='cli'))
        #CORE_TANGMEAN_VAR.mean(dim='cli').to_netcdf('test.nc')
        #quit()

        member.add_var('CORE_TANGMEAN_{}'.format(self.nl.main_var_name),CORE_TANGMEAN_VAR)
        member.add_var('CORE_CLOUD_AREA',CORE_CLOUD_AREA)
        member.add_var('STRAT_TANGMEAN_{}'.format(self.nl.main_var_name),STRAT_TANGMEAN_VAR)
        member.add_var('STRAT_CLOUD_AREA',STRAT_CLOUD_AREA)
        member.add_var('BOTH_TANGMEAN_{}'.format(self.nl.main_var_name),BOTH_TANGMEAN_VAR)
        member.add_var('BOTH_CLOUD_AREA',BOTH_CLOUD_AREA)




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
    parser.add_argument('-r', '--i_recompute_statistics', type=int, default=0)
    # recompute?
    parser.add_argument('-R', '--i_recompute_clusters', type=int, default=0)
    # computation mode? (normal, load, dask)
    parser.add_argument('-c', '--computation_mode', type=str, default='load')
    args = parser.parse_args()

    # PREPARATION STEPS
    ###########################################################################
    timer = Timer(mode='seconds')
    import nl_20 as nl_ana_raw
    from nl_plot_20 import nlp
    ana = Analysis_20(nl=SimpleNamespace())
    import_namelist(ana.nl, nl_ana_raw)
    ana.nl.nlp = nlp

    # input arguments
    #ana.nl.var_names = args.var_names.split(',')
    ana.nl.i_recompute_statistics = args.i_recompute_statistics
    ana.nl.i_recompute_clusters = args.i_recompute_clusters
    ana.nl.i_save_fig = args.i_save_fig
    ana.nl.n_par = args.n_par
    ana.nl.computation_mode = args.computation_mode

    ana.prepare_namelist()
    if ana.nl.i_recompute_statistics or ana.nl.i_recompute_clusters:
        ana.nl.i_plot = 0

    # should files be computed...
    if ana.nl.i_recompute_statistics or ana.nl.i_recompute_clusters:
        # PART OF ANALYSIS SPECIFIC FOR EACH DAY
        ######################################################################
        timer.start('daily')
        tsmp = TimeStepMP(ana.iter_dates, njobs=ana.nl.n_par, run_async=True)
        fargs = {}
        tsmp.run(ana.compute_src_members_for_date, fargs=fargs, step_args=None)

        if not ana.nl.i_recompute_statistics:
            timer.stop('daily')
            print('Finished computing clusters. End now.')
            timer.print_report()
            quit()

        first_mem_key,first_mem = next(iter(tsmp.output[0]['members'].items()))
        indiv_targ_members = {}
        for mem_key,member in tsmp.output[0]['members'].items():

            out_member = Member(member.mem_dict, val_type='abs')
            out_member.dates_code = create_dates_code(ana.iter_dates)

            for var_name in ana.nl.comp_var_names:
                daily_data = []
                cli = 0
                for ts_output in tsmp.output:
                    dd = ts_output['members'][mem_key].vars[var_name]
                    ## continuously increase cli to merge them later
                    dd = dd.assign_coords(dict(cli=np.arange(cli,cli+len(dd.cli))))
                    cli = np.max(dd.cli)+1
                    daily_data.append(dd)

                all_days = xr.concat(daily_data, dim='cli').rename(var_name)
                out_member.add_var(var_name, all_days)

            indiv_targ_members[mem_key] = out_member
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
        ana.save_data(indiv_targ_members, netcdf=True)

    # ... or be reloaded from precomputed pickle files.
    else:
        # LOAD PRECOMPUTED DATA FROM PICKLE
        ######################################################################
        ana.indiv_targ_members = ana.load_data(netcdf=True)

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
        name_dict['cld3d'] = ana.nl.plot_domain['key']
        name_dict[ana.nl.main_var_name] = ana.nl.filter_type
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
        ana.draw_axis(PO, ana.indiv_targ_members, axes)

        #PO.remove_axis_labels()

        ### FINAL FORMATTING
        ######################################################################
        fig.subplots_adjust(**ana.nl.arg_subplots_adjust)

        #PO.add_panel_labels(order='cols')

        PO.finalize_plot()
        timer.stop('plot')

    timer.print_report()
