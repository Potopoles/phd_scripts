#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Plot skew T
dependencies    
author			Christoph Heim
date changed    13.06.2022
date changed    13.06.2022
usage           args:
"""
###############################################################################
import os, argparse, copy
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from types import SimpleNamespace
from an_super import Analysis
from package.nl_variables import nlv, get_plt_units, get_plt_fact
from package.utilities import Timer, area_weighted_mean_lat_lon, dt64_to_dt
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
from package.model_pp import interp_vprof_with_time,interp_alt_to_plev
import metpy.calc as mpcalc
from metpy.plots import SkewT
from metpy.units import units
from metpy.cbook import get_test_data
###############################################################################

class Analysis_16(Analysis):

    def __init__(self, nl):
        super(Analysis_16, self).__init__(nl)
        self.nl = nl
        self.ana_number = 16


    def draw_axis(self, PO, members, ax):
        #self.draw_axis_DEFAULT(ax)

        if len(members) == 0:
            print('WARNING: No members to plot!')
            return()

        # close defualt figure
        #plt.close(PO.fig)
        # create new one
        #PO.fig = plt.figure(figsize=(6, 9))
        #fig = plt.figure(figsize=(7, 7))
        if ax == 0:
            skew = SkewT(PO.fig, subplot=121, rotation=45)
        elif ax == 1:
            skew = SkewT(PO.fig, subplot=122, rotation=45)

        mem_ind = 0
        for mem_key, member in members.items():
            print(mem_key)
            mem_dict = copy.copy(member.mem_dict)
            val_type  = member.val_type

            raw_mem_key = mem_key.split('#time#')[0]

            #### MEMBER SPECIFIC PROPERTIES
            #######################################################################
            #### color
            #if self.nl.ref_key is not None and self.nl.ref_key in mem_key: 
            #    color = self.nl.nlp['ref_color']
            #elif self.nl.ref2_key is not None and self.nl.ref2_key in mem_key: 
            #    color = self.nl.nlp['ref2_color']
            #else:
            #    if raw_mem_key in self.nl.nlp['mem_colors']: 
            #        color = self.nl.nlp['mem_colors'][raw_mem_key]
            #    elif member.mem_dict['label'] in self.nl.nlp['mem_colors']: 
            #        color = self.nl.nlp['mem_colors'][member.mem_dict['label']]
            #    else:
            #        color = '#BBBBBB'

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


            ### Set units
            ##################################################################
            vars = {}
            for vi,var_name in enumerate(self.nl.var_names):
                print(var_name)
                agg_var_name = TP.get_agg_var_name(var_name, 
                                            self.nl.agg_level, 
                                            self.nl.agg_operators[0])
                if var_name == 'T':
                    vars[var_name] = np.flip(member.vars[agg_var_name].values) * units.K
                elif var_name == 'TDEW':
                    vars[var_name] = np.flip(member.vars[agg_var_name].values) * units.degC
                else:
                    raise NotImplementedError()

                if 'p' not in vars:
                    vars['p'] = np.flip(member.vars[agg_var_name].plev.values) * units.Pa
                #print(member.vars[agg_var_name])
                #quit()

            ### Compute variables
            ##################################################################
            vars['p_lcl'],vars['T_lcl'] = mpcalc.lcl(
                vars['p'][0],   
                vars['T'][0], 
                vars['TDEW'][0]
            )

            vars['parcel'] = mpcalc.parcel_profile(
                vars['p'], vars['T'][0], vars['TDEW'][0],
            ).to('degC')

            vars['p_el'],vars['T_el'] = mpcalc.el(
                vars['p'], 
                vars['T'], 
                vars['TDEW'],
                vars['parcel'],
            )

            print(vars)
            quit()

            cape,cin = mpcalc.cape_cin(
                vars['p'], 
                vars['T'], 
                vars['TDEW'],
                vars['parcel'],
            )
            cape2_plev_top = 80000
            mask = vars['p'].magnitude >= cape2_plev_top
            cape2,cin = mpcalc.cape_cin(
                vars['p'][mask], 
                vars['T'][mask], 
                vars['TDEW'][mask],
                vars['parcel'][mask],
            )


            ### Draw variables
            ##################################################################

            #col_names = ['pressure', 'height', 'temperature', 'dewpoint', 'direction', 'speed']

            #df = pd.read_fwf(get_test_data('may4_sounding.txt', as_file_obj=False),
            #                 skiprows=5, usecols=[0, 1, 2, 3, 6, 7], names=col_names)

            ## Drop any rows with all NaN values for T, Td, winds
            #df = df.dropna(subset=('temperature', 'dewpoint', 'direction', 'speed'), how='all'
            #               ).reset_index(drop=True)
            #p = df['pressure'].values * units.hPa
            #T = df['temperature'].values * units.degC
            #Td = df['dewpoint'].values * units.degC

            #print(p)
            #print(vars['p'])
            #print(T)
            #print(vars['T'])
            #quit()

            #print(plot_var.values)
            skew.plot(vars['p'], vars['T'], 'r')
            skew.plot(vars['p'], vars['TDEW'], 'g')
            #skew.plot(p, T, 'r')
            skew.ax.set_ylim(1010, 100)
            skew.ax.set_xlim(-40, 60)

            skew.plot(vars['p_lcl'], vars['T_lcl'], 'ko', 
                markerfacecolor='black', markersize=1,
            )

            skew.plot(vars['p'], vars['parcel'], 'k', linewidth=2)
            skew.shade_cape(vars['p'], vars['T'], vars['parcel'])
        
            skew.plot_dry_adiabats()
            skew.plot_moist_adiabats()
            #plt.show()


            ##### altitude labels
            #for p,T in zip(vars['p'],vars['T']):
            #    if p.magnitude % 10000 == 0:
            #        z = mpcalc.pressure_to_height_std(p).magnitude*units.km
            #        skew.ax.text(T+20*units.K,p*1.04, 
            #            '{:3.1f} km'.format(z.magnitude),
            #            fontsize=10)

            #### special labels
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
            skew.ax.text(0.02, 0.18, 
                'LCL: {:3.2f} km; {:3.1f}°C'.format(
                    mpcalc.pressure_to_height_std(vars['p_lcl']).magnitude,
                    vars['T_lcl'].to('degC').magnitude), 
                transform=skew.ax.transAxes,
                fontsize=10, verticalalignment='top', bbox=props)
            skew.ax.text(0.02, 0.08, 
                'LNB: {:3.1f} km; {:3.1f}°C'.format(
                    mpcalc.pressure_to_height_std(vars['p_el']).magnitude,
                    vars['T_el'].to('degC').magnitude), 
                transform=skew.ax.transAxes,
                fontsize=10, verticalalignment='top', bbox=props)

            skew.ax.text(0.60, 0.95, 
                'CAPE: {:3.0f}'.format(
                    cape.magnitude)+' J kg$^{-1}$', 
                transform=skew.ax.transAxes,
                fontsize=10, verticalalignment='top', bbox=props)
            skew.ax.text(0.60, 0.75, 
                'CAPE: {:3.0f}'.format(
                    cape2.magnitude)+' J kg$^{-1}$', 
                transform=skew.ax.transAxes,
                fontsize=10, verticalalignment='top', bbox=props)


            skew.ax.set_xlabel('temperature [°C]')
            skew.ax.set_ylabel('pressure [hPa]')

            mem_ind += 1




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
                                        dask_chunks=self.nl.dask_chunks,
                                        )
                                        #targ_vert_coord='plev')
                                        #targ_vert_coord='alt')

                    #print(var)
                    #var.to_netcdf('test_plev.nc')
                    #quit()

                    # load variable
                    P = load_member_var('P', mem_dict['freq'],
                                        ts, ts, mem_dict,
                                        self.nl.var_src_dict,
                                        self.nl.mean_var_src_dict,
                                        self.nl.var_src_dict['P']['load'],
                                        domain=self.nl.var_dom_map[loc_var_name],
                                        i_debug=self.nl.i_debug,
                                        dask_chunks=self.nl.dask_chunks)

                    targ_plevs = [
                        10000,12500,15000,20000,30000,35000,40000,50000,55000,
                        60000,70000,75000,77500,80000,82500,85000,87500,90000,
                        92500,95000,97500,100000,101000,
                    ]
                    var = interp_alt_to_plev(var_name, var, P, targ_plevs,
                                                vdim_name='alt')

                    ##if self.nl.hour_of_the_day is not None:
                    ##    raise NotImplementedError()
                    ##    var = var[(var.time.dt.hour>=self.nl.hour_of_the_day) &
                    ##             (var.time.dt.hour<=self.nl.hour_of_the_day)]
                    ##    print(var)
                    ##    quit()


                if var is not None:
                    # make sure all monthly data has first date of month
                    # as time stamp (this is assumed later on)
                    if mem_dict['freq'] == 'monthly':
                        new_time = [dt64_to_dt(var.time.values[0]).replace(day=1)]
                        var = var.assign_coords(time=new_time)

                    #print(var)
                    #print(var.plev)
                    #quit()

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

                else:
                    # free up memory
                    try:
                        del members[mem_key].mem_dict 
                    except AttributeError:
                        pass

                    members[mem_key].add_var(loc_var_name, None)

        output = {'members':members}
        return(output)


    def compute_var(self, var):
        ## average horizontally
        ### TODO: this currently gives an error because of temperature offset
        #var = area_weighted_mean_lat_lon(var)
        var = var.mean(dim=['lon','lat'])

        # resample to daily mean values if required.
        if self.nl.agg_level not in [TP.NONE, TP.HOURLY_SERIES, TP.DIURNAL_CYCLE]:
            var = TP.run_aggregation_step(var, 
                      { TP.ACTION:TP.RESAMPLE, 
                        TP.FREQUENCY:'D', 
                        TP.OPERATOR:TP.MEAN  })
            var.attrs['time_key'] = 'time'
            var.attrs['agg_level'] = TP.DAILY_SERIES
            var.attrs['agg_operator'] = TP.MEAN
        return(var)


    def prepare_namelist(self):
        self.nl.pickle_append = ""

        self.nl.var_names = ['T','TDEW']

        self.prepare_namelist_DEFAULT()






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
    import nl_16 as nl_ana_raw
    from nl_plot_16 import nlp
    ana = Analysis_16(nl=SimpleNamespace())
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

        timer.stop('prepare')

        ## SET UP PLOT IO PATH
        ######################################################################
        timer.start('plot')
        name_dict = {}
        name_dict['skewT'] = ana.nl.plot_domain['key']
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
                #ax = PO.get_axis(ax_ind, order='cols')
                ana.draw_axis(PO, {mem_key:member}, ax_ind)
                #ana.draw_axis(PO, targ_members, ax)
                ax_ind += 1

        #PO.remove_axis_labels()

        ### FINAL FORMATTING
        ######################################################################
        fig.subplots_adjust(**ana.nl.arg_subplots_adjust)

        #PO.add_panel_labels(order='cols')

        PO.finalize_plot()
        timer.stop('plot')

    timer.print_report()
