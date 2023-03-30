#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Compute and plot buoyancy profiles
dependencies    
author			Christoph Heim
date created    21.07.2022
date changed    21.07.2022
usage           args:
"""
###############################################################################
import os, argparse, copy
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.interpolate import interp1d
from types import SimpleNamespace
import metpy.calc as mpcalc
from metpy.units import units

from an_super import Analysis
from package.constants import CON_G,CON_CP_AIR,CON_RD,CON_RV,CON_LH_EVAP
from package.nl_variables import nlv, get_plt_units, get_plt_fact
from package.utilities import Timer, area_weighted_mean_lat_lon
from package.time_processing import Time_Processing as TP
from package.plot_functions import PlotOrganizer
from package.functions import import_namelist
from package.mp import TimeStepMP
from package.var_pp import subsel_alt,compute_QVSAT,compute_virtual_temperature
from package.model_pp import interp_alt_to_plev
###############################################################################

class Analysis_21(Analysis):

    def __init__(self, nl):
        super(Analysis_21, self).__init__(nl)
        self.nl = nl
        self.ana_number = 21


    def draw_axis(self, PO, members, ax):
        self.draw_axis_DEFAULT(ax)

        if len(members) == 0:
            print('WARNING: No members to plot!')
            return()

        mem_ind = 0
        for mem_key, member in members.items():
            print(mem_key)
            mem_dict = copy.copy(member.mem_dict)
            val_type  = member.val_type

            raw_mem_key = mem_key.split('#time#')[0]

            ### MEMBER SPECIFIC PROPERTIES
            ######################################################################
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


            ### linewidth
            linewidth = 1.5

            ### Draw variables
            ##################################################################
            for vi,var_name in enumerate(self.nl.plot_var_names):
                agg_var_name = TP.get_agg_var_name(var_name, 
                                            self.nl.agg_level, 
                                            self.nl.agg_operators[0])

                plot_var = member.vars[agg_var_name]



                ### VARIABLE SPECIFIC PROPERTIES (overwrite member properties)
                ##############################################################
                ### color
                if var_name in self.nl.nlp['var_colors']: 
                    color = self.nl.nlp['var_colors'][var_name]

                ## format member - variable label
                add_to_legend = 0
                if self.nl.legend_type == 'member':
                    label = mem_dict['label']
                    if vi == 0:
                        add_to_legend = 1
                elif self.nl.legend_type == 'variable':
                    label = nlv[var_name]['label'] 
                    if mem_ind == 0:
                        add_to_legend = 1


                ## get and transform variable to plot
                plot_var = plot_var.copy() * get_plt_fact(var_name)

                if 'alt' in plot_var.dims:
                    vdim = 'alt'
                    vdim_key = 'COORD_ALT'
                    # select lowest Xkm (add some padding to make sure
                    # lines do not end within plotting axes limits
                    plot_var = subsel_alt(plot_var, mem_dict['mod'],
                                        slice(self.nl.alt_lims[0],
                                              self.nl.alt_lims[1]*1.2))
                    ylim = (self.nl.alt_lims[0]*get_plt_fact('COORD_ALT'), 
                            self.nl.alt_lims[1]*get_plt_fact('COORD_ALT'))
                elif 'rel_alt' in plot_var.dims:
                    vdim = 'rel_alt'
                    vdim_key = 'COORD_RELALT'
                    ylim = (self.nl.rel_alt_lims[0]*get_plt_fact('COORD_RELALT'), 
                            self.nl.rel_alt_lims[1]*get_plt_fact('COORD_RELALT'))
                else:
                    raise ValueError()


                if self.nl.plot_semilogx:
                    handle, = ax.semilogx(plot_var.values,
                                     plot_var[vdim]*get_plt_fact(vdim_key),
                                     label=label,
                                     linewidth=linewidth,
                                     color=color, linestyle=linestyle)
                else:
                    handle, = ax.plot(plot_var.values,
                                     plot_var[vdim]*get_plt_fact(vdim_key),
                                     label=label,
                                     linewidth=linewidth,
                                     color=color, linestyle=linestyle)

                if add_to_legend:
                    PO.handles.append(handle)

                ## set axis limit and labels
                ax.set_ylim(ylim)
                PO.set_axes_labels(ax, x_var_name=var_name)
                PO.set_axes_labels(ax, y_var_name=vdim_key)

                if var_name in self.nl.nlp['var_plt_cfgs']:
                    ax.set_xlim((self.nl.nlp['var_plt_cfgs'][
                                    var_name]['lims'][val_type][0],
                                 self.nl.nlp['var_plt_cfgs'][
                                    var_name]['lims'][val_type][1]))


            mem_ind += 1

        ## plot legend
        if self.nl.i_plot_legend:
            ax.legend(handles=PO.handles)
        
        ax.yaxis.grid()

        if (ax.get_xlim()[0] < 0) and (ax.get_xlim()[1] > 0):
            ax.axvline(x=0, color='k', linewidth=0.5, zorder=0)


        try:
            ax.set_title(self.nl.title, x=0.50)
        except AttributeError:
            ax.set_title(members[list(members.keys())[0]].mem_dict['label'],
                        x=0.50)



    def compute_var(self, var):
        # average horizontally
        #var = var.mean(dim={'lat','lon'})
        #var = area_weighted_mean_lat_lon(var)

        if self.nl.agg_level not in [TP.HOURLY_SERIES, TP.DIURNAL_CYCLE, TP.NONE]:
            var = TP.run_aggregation_step(var, 
                      { TP.ACTION:TP.RESAMPLE, 
                        TP.FREQUENCY:'D', 
                        TP.OPERATOR:TP.MEAN  })
        return(var)


    def prepare_namelist(self):
        self.nl.pickle_append = ""

        self.nl.var_names = ['TV','UPDTV','P','T','LCL']
        #self.nl.var_names = ['TV','UPDTV','UPDT','UPDTDEW','P','LCL']
        self.nl.var_names = ['TV','UPDTV','UPDT','P','LCL']
        #self.nl.var_names = ['TV']

        self.prepare_namelist_DEFAULT()


    def prepare_for_plotting(self, members):

        ### load from ana_16
        #########################################################################
        import nl_16 as nl_16
        from an_16 import Analysis_16
        #from nl_plot_16 import nlp as nlp_16
        nl_16.time_periods = self.nl.time_periods
        nl_16.mem_cfgs = self.nl.mem_cfgs
        ana_16 = Analysis_16(nl=SimpleNamespace())
        import_namelist(ana_16.nl, nl_16)
        ana_16.nl.nlp = self.nl.nlp
        ana_16.nl.i_recompute = 0
        ana_16.nl.i_save_fig = 0
        ana_16.nl.n_par = 1
        ana_16.nl.computation_mode = self.nl.computation_mode
        ana_16.prepare_namelist()
        ana_16.indiv_targ_members = ana_16.load_data()
        members_16 = ana_16.indiv_targ_members
        #########################################################################

        ### compute updraft buoyancy
        for mem_key,member in members.items():
            print('################################')
            print(mem_key)

            ## domain average
            for var_name,var in member.vars.items():
                #### mask grid points without updrafts ever
                #test_var_name = TP.get_agg_var_name('UPDTV', 
                #                            self.nl.agg_level, 
                #                            self.nl.agg_operators[0])
                #test_var = member.vars[test_var_name]
                #if var_name != test_var_name:
                #    var = var.where(~np.isnan(test_var), np.nan)

                ## delete updraft values at 18km (too few samples)
                #var = var.where((~np.isnan(var)).sum(dim=['lon','lat']) > 100, np.nan)

                # average horizontally
                member.vars[var_name] = area_weighted_mean_lat_lon(var)

            LCL = member.vars[TP.get_agg_var_name('LCL', 
                                            self.nl.agg_level, 
                                            self.nl.agg_operators[0])]
            TV = member.vars[TP.get_agg_var_name('TV', 
                                            self.nl.agg_level, 
                                            self.nl.agg_operators[0])]
            UPDTV = member.vars[TP.get_agg_var_name('UPDTV', 
                                            self.nl.agg_level, 
                                            self.nl.agg_operators[0])]
            UPDT = member.vars[TP.get_agg_var_name('UPDT', 
                                            self.nl.agg_level, 
                                            self.nl.agg_operators[0])]
            #UPDTDEW = member.vars[TP.get_agg_var_name('UPDTDEW', 
            #                                self.nl.agg_level, 
            #                                self.nl.agg_operators[0])]

            ## compute updraft buoyancy
            ## only show updrafts above lcl
            UPDTV = UPDTV.where(UPDTV.alt >= LCL, np.nan)
            UPDBUOYI = CON_G * (UPDTV/TV - 1)

            member.add_var(TP.get_agg_var_name('UPDBUOYI', 
                                            self.nl.agg_level, 
                                            self.nl.agg_operators[0]), UPDBUOYI)

            ## compute parcel quantities
            lapse_rate_dry = CON_G/CON_CP_AIR
            P = member.vars[TP.get_agg_var_name('P', 
                                            self.nl.agg_level, 
                                            self.nl.agg_operators[0])]
            ### temperature of environment
            #tenv = member.vars[TP.get_agg_var_name('T', 
            #                                self.nl.agg_level, 
            #                                self.nl.agg_operators[0])].copy()
            ### temperature of parcel
            #tparc = member.vars[TP.get_agg_var_name('T', 
            #                                self.nl.agg_level, 
            #                                self.nl.agg_operators[0])].copy()

            ##### load from analysis_16
            #####################################################################
            TDEW_plev = members_16[mem_key].vars[TP.get_agg_var_name('TDEW', 
                                        self.nl.agg_level, 
                                        self.nl.agg_operators[0])]
            #TDEW_plev = TDEW_plev.reindex(plev=list(reversed(TDEW_plev.plev)))
            T_plev = members_16[mem_key].vars[TP.get_agg_var_name('T', 
                                        self.nl.agg_level, 
                                        self.nl.agg_operators[0])]
            #T_plev = T_plev.reindex(plev=list(reversed(T_plev.plev)))

            #print(UPDTDEW)
            #print(UPDT)
            #print(UPDTV)
            #quit()
            #print((T_plev.reindex(plev=list(reversed(T_plev.plev))).plev)[4:]*units.Pa)
            #quit()

            PARCT_plev = mpcalc.parcel_profile(
                #(T_plev.reindex(plev=list(reversed(T_plev.plev))).plev)[4:]*units.Pa, 
                #UPDT[4]*units.K, 
                #UPDTDEW[4]*units.degC,
                T_plev.reindex(plev=list(reversed(T_plev.plev))).plev*units.Pa, 
                T_plev[-1]*units.K, 
                TDEW_plev[-1]*units.degC,
            ).metpy.dequantify()
            PARCT_plev = PARCT_plev.reindex(plev=list(reversed(PARCT_plev.plev)))
            #print(PARCT_plev)
            #quit()

            #p_lcl = 95000
            #f = interp1d(np.log(P), UPDT, kind='linear')
            #updt_lcl = f(np.log(p_lcl))
            #print(updt_lcl)
            #print(UPDT)
            ##quit()

            #targ_plevs = np.asarray([
            #    7000,10000,12500,15000,20000,30000,35000,40000,50000,55000,
            #    60000,70000,75000,77500,80000,82500,85000,87500,90000,
            #    92500,95000,97500,100000,101000,
            #],dtype=float)
            #targ_plevs = targ_plevs[targ_plevs <= p_lcl]
            ##targ_plevs = np.append(targ_plevs, p_lcl)
            #PARCP = xr.DataArray(
            #    data = targ_plevs,
            #    dims = ['plev'],
            #    coords = dict(plev=targ_plevs)
            #)
            #parct_plev = mpcalc.moist_lapse(
            #    PARCP*units.Pa, 
            #    updt_lcl*units.K, 
            #    p_lcl*units.Pa, 
            #).magnitude
            #PARCT_plev = PARCP.copy()
            #PARCT_plev[:] = parct_plev
            ##print(PARCT_plev)
            ##quit()

            PARCQV_plev = compute_QVSAT(dict(T=PARCT_plev,P=PARCT_plev.plev)) 
            #PARCQV_plev = compute_QVSAT(dict(T=PARCT_plev,P=PARCP)) 
            # virtual temperature
            PARCTV_plev = compute_virtual_temperature(
                inputs=dict(T=PARCT_plev,QV=PARCQV_plev), var_name='TV'
            )
            ## interpolate to altitude levels
            #PARCTV[:] = np.interp(
            #    np.log(P), 
            #    np.log(PARCTV_plev.plev), 
            #    PARCTV_plev,
            #    #left=np.nan, right=np.nan
            #)
            PARCTV = P.copy().rename('PARCTV')
            f = interp1d(np.log(PARCTV_plev.plev), PARCTV_plev, kind='linear', 
                        fill_value='extrapolate', bounds_error=False)
                        #fill_value=np.nan, bounds_error=False)
            PARCTV[:] = f(np.log(P))
            #PARCTV[:] = np.interp(np.log(P), np.log(PARCTV_plev.plev), PARCTV_plev)
            PARCT = P.copy().rename('PARCT')
            f = interp1d(np.log(PARCT_plev.plev), PARCT_plev, kind='linear', 
                        fill_value='extrapolate', bounds_error=False)
                        #fill_value=np.nan, bounds_error=False)
            PARCT[:] = f(np.log(P))
            #print(PARCT)
            #print(PARCTV)
            #print(UPDT)
            #quit()
            PARCQV = P.copy().rename('PARCQV')
            f = interp1d(np.log(PARCQV_plev.plev), PARCQV_plev, kind='linear', 
                        fill_value='extrapolate', bounds_error=False)
                        #fill_value=np.nan, bounds_error=False)
            PARCQV[:] = f(np.log(P))
            #####################################################################


            #quit()
            ## undiluted parcel buoyancy
            PARCBUOYI = CON_G * (PARCTV/TV - 1)
            ### only show updrafts above lcl
            #tvparc = tvparc.where(tvparc.alt >= lcl, np.nan)

            #print(updbuoyi)
            #print(buoyiparc)
            #buoyi = buoyiparc.where(buoyiparc.alt >= lcl, 0)
            #buoyi = buoyi.where(buoyi >= 0, 0)
            #print(buoyi)
            #cape = buoyi.integrate(coord='alt')
            #print('CAPE')
            #print(cape.values)
            #quit()
            
            member.add_var(TP.get_agg_var_name('PARCT', 
                                            self.nl.agg_level, 
                                            self.nl.agg_operators[0]), PARCT)
            member.add_var(TP.get_agg_var_name('PARCQV', 
                                            self.nl.agg_level, 
                                            self.nl.agg_operators[0]), PARCQV)
            member.add_var(TP.get_agg_var_name('PARCTV', 
                                            self.nl.agg_level, 
                                            self.nl.agg_operators[0]), PARCTV)
            member.add_var(TP.get_agg_var_name('PARCBUOYI', 
                                            self.nl.agg_level, 
                                            self.nl.agg_operators[0]), PARCBUOYI)
            #quit()


        members = self.prepare_for_plotting_DEFAULT(members)
        return(members)



if __name__ == '__main__':
    # READ INPUT ARGUMENTS
    ###########################################################################
    parser = argparse.ArgumentParser(description = 'Draw vertical cross-section.')
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
    import nl_21 as nl_ana_raw
    from nl_plot_21 import nlp
    ana = Analysis_21(nl=SimpleNamespace())
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
        name_dict['cs'] = ana.nl.plot_domain['key']
        name_dict[ana.nl.agg_level] = ana.nl.var_names[0]
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

        ## TODO start tmp
        time_plt_sels = [time_plt_sels[0]]
        ## TODO end tmp

        ### DRAW AXES
        ######################################################################
        ax_ind = 0
        #for mem_key,member in members.items():
        # draw a new axis for each with each time step
        for time_plt_sel in time_plt_sels:
            # sel time plot selection in namelist
            ana.nl.time_plt_sel = time_plt_sel
            ax = PO.get_axis(ax_ind, order='cols')
            #ana.draw_axis(PO, {mem_key:member}, ax)
            ana.draw_axis(PO, targ_members, ax)
            ax_ind += 1

        PO.remove_axis_labels()

        ### FINAL FORMATTING
        ######################################################################
        fig.subplots_adjust(**ana.nl.arg_subplots_adjust)
        #fig.suptitle('{:%Y%m%d} {}'.format(date, hour))
        #fig.suptitle('{}'.format(ana.nl.mem_src_dict[mem_key]['label']),
        #            x=0.55)

        PO.add_panel_labels(order='cols')

        PO.finalize_plot()
        timer.stop('plot')

    timer.print_report()
