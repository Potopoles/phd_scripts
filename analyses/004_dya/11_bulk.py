#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     
dependencies    
author			Christoph Heim
date created    22.01.2021
date changed    02.02.2021
usage           args:
                1st:    number of parallel tasks
                2nd:    var_name
                3nd:    i_recompute (1: yes, 0: no)
                4th:    pane_label 
                5th:    domain
                6th:    model_keys
"""
###############################################################################
import os, glob, collections, copy
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
from datetime import datetime, timedelta
from pandas.plotting import register_matplotlib_converters
from sklearn.linear_model import LinearRegression
import nl_11 as nl
from package.constants import CON_M_PER_DEG, CON_LH_EVAP, CON_CP_AIR
from package.nl_mem_src import mem_src
from package.nl_variables import nlv
from package.var_pp import var_mapping, compute_variable
from package.utilities import (Timer, pickle_load, pickle_save,
                                select_common_timesteps)
from package.plot_functions import PlotOrganizer, draw_map
from package.functions import (load_member_var, save_member_data_to_pickle,
                               load_member_data_from_pickle,
                               time_periods_to_dates)
from package.mp import TimeStepMP, IterMP
from package.member import Member
from package.comparison import Comparison
from package.var_pp import subsel_alt
###############################################################################

def draw_plot(members):

    if len(nl.integration_volumes) > 1:
        raise NotImplementedError('Only one integration volume implemented')
    vol_key = nl.integration_volumes[0]

    # lists of all used resolutions in each model
    # used to select marker types
    res_lists = {}
    for mem_key,member in members.items():
        if mem_key == 'OBS': continue
        mem_dict = member[nl.target_var_names[0]].mem_dict
        if mem_dict['mod'] not in res_lists:
            res_lists[mem_dict['mod']] = [mem_dict['res']]
        else:
            res_lists[mem_dict['mod']].append(mem_dict['res'])
    for mem_key,res_list in res_lists.items():
        res_list.sort()

    name_dict = {nl.nlp['plot_type']:nl.nlp['computation']}
    name_dict['dom'] = nl.cfg['domain']['code']
    name_dict['var'] = nl.main_var_name
    name_dict['vol'] = vol_key
    PO = PlotOrganizer(i_save_fig=nl.i_save_fig,
                      path=os.path.join(nl.plot_base_dir,
                                        nl.cfg['domain']['code']),
                      name_dict=name_dict, nlp=nl.nlp, geo_plot=False)
    fig,axes = PO.initialize_plot(nrows=nl.nlp['nrows'],
                                  ncols=nl.nlp['ncols'],
                                  figsize=nl.nlp['figsize'])
    #for edge_key,edge_dict in nl.nlp['edges'].items():
    #    ax = axes[edge_dict['axi'], edge_dict['axj']]
    for ax_ind,ax_dict in nl.nlp['axes'].items():
        ax = axes[ax_ind]
        #print(nl.aggregs[ax_dict['var']])
        PO.handles = []

        data = []
        labels = []
        colors = []
        #print(members.items())
        for mem_key,member in members.items():
            #print(mem_key)
            vi = 0
            for var_key,sign in nl.aggregs[ax_dict['var']]['vars'].items():
                #print(var_key)
                if nl.nlp['computation'] == 'tend':
                    if var_key in ['HORI', 'VERT', 'TOT']:
                        nl.bulk_mode = 'vol'
                    else:
                        nl.bulk_mode = 'edge'
                elif nl.nlp['computation'] == 'mean':
                    nl.bulk_mode = 'vol'
                    var_key = 'MEAN'
                var_name = 'bulk_{}_{}_{}_{}_{}'.format(nl.nlp['computation'],
                                nl.bulk_mode, nl.main_var_name,
                                nl.vol_key, var_key)
                #print(var_name)
                mem_dict = member[var_name].mem_dict
                new_contrib = copy.deepcopy(member[var_name].var).squeeze()
                if vi == 0:
                    plot_var = sign * new_contrib
                else:
                    new_contrib, plot_var = select_common_timesteps(
                                                    new_contrib, plot_var)
                    plot_var += sign * new_contrib
                #print(sign * member[var_name].var.mean().values)
                #print(plot_var.mean().values)
                vi += 1

            # make hourly tendency
            if nl.nlp['computation'] == 'tend':
                plot_var *= 3600
            
            ## reample to daily?
            if nl.nlp['i_aggreg_daily']:
                plot_var = plot_var.resample(time='1D').mean()

            #format member
            if mem_key == nl.obs_key:
                linestyle = '-'
                color = 'black'
            else:
                res = mem_dict['res']
                linestyle = nl.nlp['linestyles'][res_lists[mem_dict['mod']].index(res)]

            # either take predefined color or take it from nlp
            if 'color' in mem_dict:
                color = mem_dict['color']
            else:
                color = nl.nlp['colors'][nl.nlp['mod_col_inds'].index(mem_dict['mod'])]


            if nl.nlp['plot_type'] == 'line':
                handle, = ax.plot(plot_var.time.values,
                                 plot_var.values,
                                 label=mem_dict['label'],
                                 linewidth=nl.nlp['mod_linewidth'],
                                 color=color, linestyle=linestyle)
                PO.handles.append(handle)
                date_formatter = mdates.DateFormatter('%m.%d.')
                ax.xaxis.set_major_formatter(date_formatter)

            elif nl.nlp['plot_type'] == 'box':
                data.append(plot_var.values)
                labels.append(mem_dict['label'])
                colors.append(color)

        if nl.nlp['plot_type'] == 'box':
            # sort according to mean value
            #if nl.nlp['sort']:
            means = np.zeros(len(data))
            for i,mem_data in enumerate(data):
                means[i] = np.mean(mem_data)
            sort_inds = np.argsort(means)
            data = [data[i] for i in sort_inds]
            labels = [labels[i] for i in sort_inds]
            colors = [colors[i] for i in sort_inds]

            mean_line_props = dict(linestyle='-', linewidth=2, color='black')
            bplot = ax.boxplot(data, labels=labels, patch_artist=True,
                            showmeans=True, meanline=True,
                            meanprops=mean_line_props)
            for patch, color in zip(bplot['boxes'], colors):
                patch.set_facecolor(color)
            
        # manually setting of ticks
        if 'ylim' in nl.nlp:
            ax.set_ylim(nl.nlp['ylim'][nl.main_var_name][vol_key])
        ax.tick_params(axis='x', labelrotation=90)
        ## ax title
        ax.set_title('{} {} {}'.format(ax_dict['var'],
                                    nl.main_var_name, vol_key))
        ## y labels
        if nl.main_var_name == 'POTT':
            unit = '$K$'
        elif nl.main_var_name == 'QV':
            unit = '$kg$ $kg^{-1}$'
        if nl.nlp['computation'] == 'tend':
            sec = '$hr^{-1}$'
            ylabel = 'bulk tend. {} [{} {}]'.format(
                        nl.main_var_name, unit, sec)
        elif nl.nlp['computation'] == 'mean':
            ylabel = 'mean {} [{}]'.format(
                        nl.main_var_name, unit)
        if ax_ind[1] == 0:
            ax.set_ylabel(ylabel)
        ax.grid()
        # draw horizontal line at y = 0 if it is part of the y domain
        if ax.get_ylim()[0] < 0 and ax.get_ylim()[1] > 0:
            ax.axhline(color='grey')

    ## legend
    #if nl.nlp['plot_type'] == 'line':
    #    ax.legend(handles=PO.handles)
    fig.subplots_adjust(**nl.nlp['arg_subplots_adjust'])

    PO.finalize_plot()


def dim_orientation_factor(var, dim_keys):
    factor = 1
    for dim_key in dim_keys:
        if var[dim_key].values[-1] < var[dim_key].values[0]:
            factor *= -1
    return(factor)

def load_vars(members, date, var_names):
    for mem_key,mem_dict in nl.sim_src_dict.items():
        for var_name in var_names:
            if nl.i_debug >= 2:
                print('member {} load var {}'.format(mem_key, var_name))
            var = load_member_var(var_name, date, date, mem_dict,
                                nl.var_src_dict,
                                nl.var_src_dict[var_name]['load'],
                                domain=nl.cfg['domain'], i_debug=nl.i_debug)
            if var is not None:
                # select altitude domain
                if 'z' in nlv[var_name]['dims']:
                    var = subsel_alt(var, mem_dict['mod'], nl.cfg['domain']['alt'])

                # create member instance
                member = Member(var, mem_dict, comparison=None)

                if mem_key not in members.keys():
                    members[mem_key] = {}
                if members[mem_key] is not None:
                    members[mem_key][var_name] = member
            else:
                if var_name in nl.optional_var_names:
                    pass
                else:
                    members[mem_key] = None
                    


def compute_domain_mass(rho, invhgt, vol_key):
    # set missing values to zero (for integration)
    rho_tot = copy.deepcopy(rho.where(~np.isnan(rho), 0))
    # extract and integrate density for the current volume
    if vol_key == 'above':
        rho_tot = rho_tot.where(rho_tot.alt > invhgt, 0.)
        rho_tot = rho_tot.where(~np.isnan(invhgt), 0.)
    elif vol_key == 'below':
        rho_tot = rho_tot.where(rho_tot.alt <= invhgt, 0.)
        rho_tot = rho_tot.where(~np.isnan(invhgt), 0.)
    # take into account possible wrong orientations of coordinates
    rho_tot *= dim_orientation_factor(rho_tot, nl.integ_dims)
    # integrate over all required dimensions
    # units: [(kg * deg_lon * deg_lat) / (m_lon * m_lat)]
    mass_tot = rho_tot.integrate(dim=nl.integ_dims)
    ### convert deg to m
    # units: [kg]
    mass_tot *= CON_M_PER_DEG**2
    return(mass_tot)


def compute_surface_int(date, members):
    if nl.i_debug >= 1:
        print(date)
    ######## LOAD MEMBERS
    ##########################################################################
    load_vars(members, date, nl.input_var_names)
    
    ######## BULK FLUX COMPUTATION
    ##########################################################################
    for mem_key,mem_dict in nl.sim_src_dict.items():
        if members[mem_key] is None: continue

        #### Gather all variables
        ######################################################################
        var = members[mem_key][nl.main_var_name].var
        rho = members[mem_key]['RHO'].var
        invhgt = members[mem_key]['INVHGT'].var
        u = members[mem_key]['U'].var
        v = members[mem_key]['V'].var
        w = members[mem_key]['W'].var
        # optionally take into account surface fluxes
        if (('SLHFLX' in nl.optional_var_names) and
            ('SLHFLX' in members[mem_key].keys())):
            # units: [kg_w / (s * m_lon * m_lat)]
            sflx = members[mem_key]['SLHFLX'].var / CON_LH_EVAP
            sflx, var = select_common_timesteps(sflx, var)
        elif (('SSHFLX' in nl.optional_var_names) and
              ('SSHFLX' in members[mem_key].keys())):
            # units: [(K * kg_a) / (s * m_lon * m_lat)]
            sflx = members[mem_key]['SSHFLX'].var / CON_CP_AIR
            sflx, var = select_common_timesteps(sflx, var)
        else:
            sflx = None

        var, rho = select_common_timesteps(var, rho)
        var, invhgt = select_common_timesteps(var, invhgt)
        var, u = select_common_timesteps(var, u)
        var, v = select_common_timesteps(var, v)
        var, w = select_common_timesteps(var, w)
        var, rho = select_common_timesteps(var, rho)
        var, invhgt = select_common_timesteps(var, invhgt)

        #### Preprocess to same grid
        ######################################################################
        # interpolate coordinates if necessary
        if not np.array_equal(w.alt.values, rho.alt.values):
            w_top_level_orig = copy.deepcopy(w.isel(alt=-1))
            w = w.interp(alt=rho.alt)
            # bad fix for problem that MPAS 3.75 W field does not reach up to 6km
            # but only to 5740 m
            if ((mem_dict['mod'] == 'MPAS') and 
                (np.sum(np.isnan(w.isel(alt=-1))) > 0)):
                print('Apply MPAS interpolation fix.')
                w.loc[{'alt':rho.alt.isel(alt=-1).values}] = w_top_level_orig

        #### Split up computation into the individual air volumes
        ######################################################################
        # loop over all the volumes that should be computed
        # total: total volume
        # above: volume above the inversion
        # below: volume below the inversion
        fluxes_3D = {}
        fluxes_edges = {}
        for vol_key in nl.integration_volumes:
            #print(vol_key)

            # prepare dicts to store results
            fluxes_3D[vol_key] = {}
            fluxes_edges[vol_key] = {}

            #### Compute total domain mass
            ##################################################################
            mass_tot = compute_domain_mass(rho, invhgt, vol_key)

            #### Compute var Fluxes
            ##################################################################
            # units: [(var * kg) / (m_lat * m_alt * s)]
            fluxes_3D[vol_key]['lon'] = copy.deepcopy(var * rho * u)
            # units: [(var * kg) / (m_lon * m_alt * s)]
            fluxes_3D[vol_key]['lat'] = copy.deepcopy(var * rho * v)
            # units: [(var * kg) / (m_lon * m_lat * s)]
            fluxes_3D[vol_key]['alt'] = copy.deepcopy(var * rho * w)

            ## compute below and above inversion
            for dim_key in ['lon', 'lat', 'alt']:
                flux = fluxes_3D[vol_key][dim_key]
                if vol_key == 'above':
                    flux = flux.where(flux.alt > invhgt, 0.)
                    flux = flux.where(~np.isnan(invhgt), 0.)
                elif vol_key == 'below':
                    flux = flux.where(flux.alt <= invhgt, 0.)
                    flux = flux.where(~np.isnan(invhgt), 0.)
                fluxes_3D[vol_key][dim_key] = flux

            #### Focus on specific borders
            ##################################################################
            domain = nl.cfg['domain']
            for edge_key,edge in nl.edges.items():
                #print(edge_key)
                dim_key = edge['dim']
                integ_dims = copy.copy(nl.integ_dims)
                try:
                    integ_dims.remove(dim_key)
                except ValueError:
                    print('Dimension ERROR!')
                    print('Cannot compute flux at edge {} without'.format(edge_key))
                    print('integrating over its dimension {}.'.format(dim_key))
                    quit()

                if ( ((vol_key == 'above') and (edge_key == 'B')) |
                     ((vol_key == 'below') and (edge_key == 'T')) ):
                    ## TODO this is too slow (and not tested)
                    #flx_edge = fluxes_3D[vol_key][dim_key].interp(
                    #                        {dim_key:invhgt})
                    # for now, set values to zero
                    flx_edge = copy.deepcopy(fluxes_3D[vol_key][dim_key].sel(
                                            {dim_key:0}, method='nearest'))
                    flx_edge.values[:] = 0.
                elif edge_key == 'SFC':
                    if (sflx is not None) and vol_key in ['total', 'below']:
                        #print('take surface flux for SFC and volume {}'.format(vol_key))
                        #print(sflx.mean())
                        flx_edge = sflx
                    else:
                        # set flux to zero if no surface flux exists
                        flx_edge = copy.deepcopy(fluxes_3D[vol_key][dim_key].sel(
                                                {dim_key:0}, method='nearest'))
                        flx_edge.values[:] = 0.
                else:
                    if edge['pos'] == 'start':
                        dim_edge = domain[dim_key].start
                    elif edge['pos'] == 'stop':
                        dim_edge = domain[dim_key].stop
                    flx_edge = fluxes_3D[vol_key][dim_key].sel(
                                            {dim_key:dim_edge}, method='nearest')

                #### integrate over other dimensions
                ######################
                # set missing values to zero (for integration)
                flx_edge = copy.deepcopy(flx_edge.where(~np.isnan(flx_edge), 0))
                # take into account possible wrong orientations of coordinates
                flx_edge *= dim_orientation_factor(flx_edge, integ_dims)
                # x units: [(var * kg * deg_lat) / (m_lat * s)]
                # y units: [(var * kg * deg_lon) / (m_lon * s)]
                # z units: [(var * kg * deg_lon * deg_lat) / (m_lon * m_lat * s)]
                flx_edge = flx_edge.integrate(dim=integ_dims)
                #print(flx_edge.shape)
                # weight according to inflow/outflow boundary
                flx_edge *= edge['orient']

                #### convert degrees to meters
                ######################
                # units: [(var * kg) / s]
                if dim_key in ['lon','lat']: flx_edge *= CON_M_PER_DEG
                if dim_key in ['alt']: flx_edge *= CON_M_PER_DEG**2

                #### divide by total domain mass
                ######################
                # units: [var / s]
                flx_edge, mass_tot = select_common_timesteps(flx_edge, mass_tot)
                flx_edge /= mass_tot

                ###### Daily aggregation
                ########################################################################
                #flx_edge = flx_edge.mean(dim='time')
                #flx_edge = flx_edge.expand_dims({'time':[date]})

                fluxes_edges[vol_key][edge_key] = flx_edge

                var_name = 'bulk_{}_{}_{}_{}_{}'.format(nl.computation,
                                nl.bulk_mode, nl.main_var_name,
                                vol_key, edge_key)

                member = Member(flx_edge, mem_dict, comparison=None)
                members[mem_key][var_name] = member

        ## remove original var_names
        for var_name in nl.input_var_names:
            if var_name in members[mem_key].keys():
                del members[mem_key][var_name]

    return(members)






def compute_volume_int(date, members):
    if nl.i_debug >= 1:
        print(date)
    ######## LOAD MEMBERS
    ##########################################################################
    load_vars(members, date, nl.input_var_names)
    
    ######## BULK FLUX COMPUTATION
    ##########################################################################
    for mem_key,mem_dict in nl.sim_src_dict.items():
        if members[mem_key] is None: continue

        #### Gather all variables
        ######################################################################
        var = members[mem_key][nl.main_var_name].var
        rho = members[mem_key]['RHO'].var
        invhgt = members[mem_key]['INVHGT'].var
        u = members[mem_key]['U'].var
        v = members[mem_key]['V'].var
        w = members[mem_key]['W'].var
        #print('orig shapes {}'.format(rho.shape))

        var, rho = select_common_timesteps(var, rho)
        var, invhgt = select_common_timesteps(var, invhgt)
        var, u = select_common_timesteps(var, u)
        var, v = select_common_timesteps(var, v)
        var, w = select_common_timesteps(var, w)
        var, rho = select_common_timesteps(var, rho)
        var, invhgt = select_common_timesteps(var, invhgt)

        #### Preprocess to same grid
        ######################################################################
        # interpolate coordinates if necessary
        if not np.array_equal(w.alt.values, rho.alt.values):
            w = w.interp(alt=rho.alt)

        #### Split up computation into the individual air volumes
        ######################################################################
        # loop over all the volumes that should be computed
        # total: total volume
        # above: volume above the inversion
        # below: volume below the inversion
        integs = {}
        for vol_key in nl.integration_volumes:
            #print(vol_key)
            integs[vol_key] = {}

            #### Compute total domain mass
            ##################################################################
            mass_tot = compute_domain_mass(rho, invhgt, vol_key)

            ##################################################################
            #### Compute advective tendency
            ##################################################################
            for dim_key in ['lon', 'lat', 'alt']:
                #print(dim_key)
                #### Compute var Fluxes
                ##################################################################
                if dim_key == 'lon':
                    # units: [(var * kg) / (m_lat * m_alt * s)]
                    flux = copy.deepcopy(var * rho * u)
                elif dim_key == 'lat':
                    # units: [(var * kg) / (m_lon * m_alt * s)]
                    flux = copy.deepcopy(var * rho * v)
                elif dim_key == 'alt':
                    # units: [(var * kg) / (m_lon * m_lat * s)]
                    flux = copy.deepcopy(var * rho * w)

                #### Differentiate var fluxes to obtain flux divergence
                ##################################################################
                # x units: [(var * kg) / (deg_lon * m_lat * m_alt * s)]
                # y units: [(var * kg) / (m_lon * deg_lat * m_alt * s)]
                # z units: [(var * kg) / (m_lon * m_lat * m_alt * s)]
                div_flux = flux.differentiate(coord=dim_key)

                #### mask below/above inversion (set to 0 for integration)
                ##################################################################
                if vol_key == 'above':
                    div_flux = div_flux.where(div_flux.alt > invhgt, 0.)
                    div_flux = div_flux.where(~np.isnan(invhgt), 0.)
                elif vol_key == 'below':
                    div_flux = div_flux.where(div_flux.alt <= invhgt, 0.)
                    div_flux = div_flux.where(~np.isnan(invhgt), 0.)

                #### Integrate total flux divergence over domain volume
                ##################################################################
                # set missing values to zero (for integration)
                div_flux = copy.deepcopy(div_flux.where(~np.isnan(div_flux), 0))
                # take into account possible wrong orientations of coordinates
                div_flux *= dim_orientation_factor(div_flux, nl.integ_dims)
                # x units: [(var * kg * deg_lat) / (m_lat * s)]
                # y units: [(var * kg * deg_lon) / (m_lon * s)]
                # z units: [(var * kg * deg_lon * deg_lat) / (m_lon * m_lat * s)]
                int_div_flux = div_flux.integrate(dim=nl.integ_dims)

                ##### convert degrees to meters
                ###################################################################
                ## units: [(var * kg) / s]
                if dim_key in ['lon', 'lat']:
                    int_div_flux *= CON_M_PER_DEG
                elif dim_key == 'alt':
                    int_div_flux *= CON_M_PER_DEG**2

                #### divide by total domain mass and convert to time tendency (*-1)
                ######################
                # units: [(var) / s]
                int_div_flux /= mass_tot
                int_div_flux *= -1

                ###### Daily aggregation
                ##############################################################
                #int_div_flux = int_div_flux.mean(dim='time')
                #int_div_flux = int_div_flux.expand_dims({'time':[date]})

                integs[vol_key][dim_key] = int_div_flux
                #print(int_div_flux.values)

            #### sum up directional components
            ##################################################################
            HORI = integs[vol_key]['lon'] + integs[vol_key]['lat']
            VERT = integs[vol_key]['alt']

            #### store advective tendencies as member 
            ##################################################################
            # ADV_HORI
            var_name = 'bulk_{}_{}_{}_{}_{}'.format(nl.computation,
                            nl.bulk_mode, nl.main_var_name,
                            vol_key, 'HORI')
            member = Member(HORI, mem_dict, comparison=None)
            members[mem_key][var_name] = member
            # ADV_VERT
            var_name = 'bulk_{}_{}_{}_{}_{}'.format(nl.computation,
                            nl.bulk_mode, nl.main_var_name,
                            vol_key, 'VERT')
            member = Member(VERT, mem_dict, comparison=None)
            members[mem_key][var_name] = member


            ##################################################################
            #### Compute total tendency
            ##################################################################

            #### multiply var with mass
            ##################################################################
            # units: [(var * kg) / (m_lon * m_lat * m_alt)]
            tot_tend = copy.deepcopy(var * rho)

            #### mask below/above inversion (set to 0 for integration)
            ##################################################################
            if vol_key == 'above':
                tot_tend = tot_tend.where(tot_tend.alt > invhgt, 0.)
                tot_tend = tot_tend.where(~np.isnan(invhgt), 0.)
            elif vol_key == 'below':
                tot_tend = tot_tend.where(tot_tend.alt <= invhgt, 0.)
                tot_tend = tot_tend.where(~np.isnan(invhgt), 0.)

            #### integrate over domain volume
            ##################################################################
            # set missing values to zero (for tot_tendration)
            tot_tend = copy.deepcopy(tot_tend.where(~np.isnan(tot_tend), 0))
            # take into account possible wrong orientations of coordinates
            tot_tend *= dim_orientation_factor(tot_tend, nl.integ_dims)
            # units: [(var * kg * deg_lon * deg_lat) / (m_lon * m_lat)]
            tot_tend = tot_tend.integrate(dim=nl.integ_dims)

            ##### convert degrees to meters
            ###################################################################
            # units: [var * kg]
            tot_tend *= CON_M_PER_DEG**2

            #### divide by total domain mass
            ######################
            # units: [var]
            tot_tend /= mass_tot

            #### differentiate with respect to time
            ######################
            # units: [var/s]
            #print(tot_tend.mean())
            tot_tend = tot_tend.differentiate(coord='time')*1E9
            #print(tot_tend.mean())
            #fig,ax = plt.subplots(1,1)
            #ax.plot(tot_tend*3600)
            #fig.tight_layout()
            #plt.show()
            #quit()

            # TOT tend
            var_name = 'bulk_{}_{}_{}_{}_{}'.format(nl.computation,
                            nl.bulk_mode, nl.main_var_name,
                            vol_key, 'TOT')
            member = Member(tot_tend, mem_dict, comparison=None)
            members[mem_key][var_name] = member

        ## remove original var_names
        for var_name in nl.input_var_names:
            if var_name in members[mem_key].keys():
                del members[mem_key][var_name]
        #print(members[mem_key].keys())
        #quit()

    return(members)




def compute_mass_weighted_mean(date, members):
    if nl.i_debug >= 1:
        print(date)
    ######## LOAD MEMBERS
    ##########################################################################
    load_vars(members, date, nl.input_var_names)

    ######## BULK FLUX COMPUTATION
    ##########################################################################
    for mem_key,mem_dict in nl.sim_src_dict.items():
        if members[mem_key] is None: continue

        #### Gather all variables
        ######################################################################
        var = members[mem_key][nl.main_var_name].var
        rho = members[mem_key]['RHO'].var
        invhgt = members[mem_key]['INVHGT'].var

        var, rho = select_common_timesteps(var, rho)
        var, invhgt = select_common_timesteps(var, invhgt)

        #### Preprocess to same grid
        ######################################################################

        #### Split up computation into the individual air volumes
        ######################################################################
        # loop over all the volumes that should be computed
        # total: total volume
        # above: volume above the inversion
        # below: volume below the inversion
        integs = {}
        for vol_key in nl.integration_volumes:
            #print(vol_key)

            #### Compute total domain mass
            ##################################################################
            mass_tot = compute_domain_mass(rho, invhgt, vol_key)

            #### Compute domain mean density to store as a result as well
            ##################################################################
            rho_mean = copy.deepcopy(rho)
            if vol_key == 'above':
                rho_mean = rho_mean.where(rho_mean.alt > invhgt, np.nan)
                rho_mean = rho_mean.where(~np.isnan(invhgt), np.nan)
            elif vol_key == 'below':
                rho_mean = rho_mean.where(rho_mean.alt <= invhgt, np.nan)
                rho_mean = rho_mean.where(~np.isnan(invhgt), np.nan)
            rho_mean = rho_mean.mean(dim=['lon', 'lat', 'alt'])
            #print(rho_mean.values)

            #### Compute mass weighted quantity
            ##################################################################
            # units: [(var * kg) / (m_lon * m_lat * m_alt)]
            integ = copy.deepcopy(var * rho)

            #### mask below/above inversion (set to 0 for integration)
            ##################################################################
            if vol_key == 'above':
                integ = integ.where(integ.alt > invhgt, 0.)
                integ = integ.where(~np.isnan(invhgt), 0.)
            elif vol_key == 'below':
                integ = integ.where(integ.alt <= invhgt, 0.)
                integ = integ.where(~np.isnan(invhgt), 0.)

            #### Integrate over domain volume
            ##################################################################
            # set missing values to zero (for integration)
            integ = copy.deepcopy(integ.where(~np.isnan(integ), 0))
            # take into account possible wrong orientations of coordinates
            integ *= dim_orientation_factor(integ, nl.integ_dims)
            # units: [(var * kg * deg_lon * deg_lat) / (m_lon * m_lat)]
            integ = integ.integrate(dim=nl.integ_dims)

            ##### convert degrees to meters
            ###################################################################
            # units: [var * kg]
            integ *= CON_M_PER_DEG**2

            #### divide by total domain mass
            ######################
            # units: [var]
            integ /= mass_tot

            ###### Daily aggregation
            ##############################################################
            #integ = integ.mean(dim='time')
            #integ = integ.expand_dims({'time':[date]})

            #### store as member 
            ##################################################################
            var_name = 'bulk_{}_{}_{}_{}_{}'.format(nl.computation,
                                    nl.bulk_mode, nl.main_var_name,
                                                vol_key, 'MEAN')
            member = Member(integ, mem_dict, comparison=None)
            members[mem_key][var_name] = member

            var_name = 'bulk_{}_{}_{}_{}_{}'.format(nl.computation,
                                    nl.bulk_mode, 'RHO',
                                                vol_key, 'MEAN')
            member = Member(rho_mean, mem_dict, comparison=None)
            #member = Member(mass_tot, mem_dict, comparison=None)
            members[mem_key][var_name] = member

        ## remove original var_names
        for var_name in nl.input_var_names:
            if var_name in members[mem_key].keys():
                del members[mem_key][var_name]

    return(members)





def run_for_date(ts):
    """
    Organize full analysis for a given date (ts).
    ts has to be called ts because run_for_date is called from TimeStepMP.
    """
    timer = Timer(mode='seconds')
    members = {}
    
    # compute profiles
    if nl.computation == 'tend':
        if nl.bulk_mode == 'edge':
            members = compute_surface_int(ts, members)
        elif nl.bulk_mode == 'vol':
            members = compute_volume_int(ts, members)
    elif nl.computation == 'mean':
        members = compute_mass_weighted_mean(ts, members)
    else: raise ValueError()

    output = {'timer':timer, 'members':members}
    return(output)


if __name__ == '__main__':

    ###########################################################################
    # PREPARATION STEPS
    timer = Timer(mode='seconds')
    Path(nl.ana_base_dir).mkdir(parents=True, exist_ok=True)
    dates = time_periods_to_dates(nl.time_periods)

    ###########################################################################
    # PART OF ANALYSIS SPECIFIC FOR EACH DAY
    # should files be computed...
    if nl.i_recompute:
        tsmp = TimeStepMP(dates, njobs=nl.njobs, run_async=False)
        fargs = {}
        timer.start('compute')
        tsmp.run(run_for_date, fargs=fargs, step_args=None)
        tsmp.concat_timesteps()
        members = tsmp.concat_output['members']
        timer.stop('compute')
        # save precomputed data
        Path(nl.pickle_dir).mkdir(exist_ok=True, parents=True)
        for mem_key,member in members.items():
            #var_names = list(member.keys())
            save_member_data_to_pickle(nl.pickle_dir, member,
                            nl.cfg['domain'], list(member.keys()),
                            nl.time_periods)

    # ... or be reloaded from precomputed pickle files.
    else:
        # load precomputed data
        members = {}
        iter_mem_keys = list(nl.sim_src_dict.keys())
        for mem_key in iter_mem_keys:
            mem_dict = nl.sim_src_dict[mem_key] 
            members[mem_key] = load_member_data_from_pickle(nl.pickle_dir,
                            mem_dict, nl.cfg['domain'], nl.target_var_names,
                            nl.time_periods, nl.i_skip_missing)


    # If no member available abort
    any_data = False
    for mem_key,member in members.items():
        if len(member) > 0:
            any_data = True
    if not any_data:
        raise ValueError('No member contains data. '+
                        'Maybe recompute? Wrong dates?')


    ###########################################################################
    # PART OF ANALYSIS FOR ENTIRE TIME SERIES
    timer.start('all')
    if nl.i_aggreg_days:
        for mem_key,member in members.items():
            for var_name in member.keys():
                member[var_name].var = member[var_name].var.mean(dim='time')
    timer.stop('all')

    ###########################################################################
    # PLOTTING
    if nl.i_plot:
        timer.start('plot')
        draw_plot(members)
        #if nl.nlp['plot_type'] == 'box':
        #    draw_box_plot(members)
        #elif nl.nlp['plot_type'] == 'line':
        #    draw_line_plot(members)
        timer.stop('plot')

    timer.print_report()
