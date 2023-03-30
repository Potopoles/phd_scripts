#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Plot vertical profiles
author			Christoph Heim
date created    02.03.2020
date changed    02.03.2020
usage           args:
"""
###############################################################################
import os
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pathlib import Path
import nl_14 as nl
import nl_plot as nlp
from package.utilities import Timer, calc_mean_diurnal_cycle, dt64_to_dt
from package.plot_functions import PlotOrganizer
from package.MP import TimeStepMP
from package.member import Member
###############################################################################


def process_data(ts, full_domain):
    """
    """
    timer = Timer()
    timer.start('all')

    members = {}
    for res in nl.ress:
        okey = '{}{}'.format('OBS', res) 
        obs_data_dir = os.path.join(nl.sim_base_dir, okey,
                                   'nTOT_PREC.nc')
        obs = xr.open_dataset(obs_data_dir)
        obs = obs.sel(time=ts, x_1=nl.domain['lon'], y_1=nl.domain['lat'])
        obs = obs['TOT_PREC']
        obs_mask = np.isnan(obs.values)
        for stype in nl.model_types:
            skey = '{}{}'.format(stype, res) 

            sim_data_dir = os.path.join(nl.sim_base_dir, skey,
                                   'nTOT_PREC.nc')
            sim = xr.open_dataset(sim_data_dir)
            sim = sim['TOT_PREC']
            sim = sim.sel(time=ts, rlon=nl.domain['lon'], rlat=nl.domain['lat'])

            if not full_domain:
                # mask values that are nan in obs
                sim.values[obs_mask] = np.nan

            sim = sim.mean(dim=['rlon', 'rlat'], skipna=True)

            member = Member(sim, {'label':skey})
            members[skey] = member

        if not full_domain:
            obs = obs.mean(dim=['x_1', 'y_1'])
            member = Member(obs, {'label':okey})
            members[okey] = member


    timer.stop('all')
    output = {'timer':timer, 'members':members}
    return(output)




def draw_plot(all_data):
    name_dict = {'':'prec_diurnal_pub'}
    PO = PlotOrganizer(i_save_fig=nl.i_save_fig, path=nl.plot_base_dir,
                  name_dict=name_dict)
    fig,axes = PO.initialize_plot(nrows=3, ncols=3, figsize=(13,14))
    cI = 0
    for key,pdict in nl.plot_dict.items():
        data = all_data[pdict['meta']['src']]
        ax = axes[pdict['meta']['ax_inds'][0],pdict['meta']['ax_inds'][1]]
        handles = []

        if pdict['meta']['ax_title'] is not None:
            ax.set_title(pdict['meta']['ax_title'])
        ax.set_xlim(pdict['meta']['ax_xlim'])
        ax.set_ylim(pdict['meta']['ax_ylim'])
        if pdict['meta']['ax_xlabel'] is not None:
            ax.set_xlabel(pdict['meta']['ax_xlabel'], fontsize=nl.label_size)
        if pdict['meta']['ax_ylabel'] is not None:
            ax.set_ylabel(pdict['meta']['ax_ylabel'], fontsize=nl.label_size)
        ax.set_xticks(np.arange(0,24.1,6))
        ax.grid()

        rI = 0
        for mkey,mdict in pdict['data'].items():
            if mkey in ['DIFF4', 'DIFF2', 'DIFF1']:
                raw_field = data['RAW{}'.format(mkey[-1])]
                sm_field = data['SM{}'.format(mkey[-1])]
                field = raw_field - sm_field
            else:
                field = data[mkey]
            #print(field)
            field_diurn = calc_mean_diurnal_cycle(field)
            #print(field_diurn)
            vals_diurn = field_diurn.values
            vals = field.values

            sum = str(round(np.sum(vals_diurn),1)) + ' mm' 

            vals_diurn = np.append(vals_diurn, vals_diurn[0])
            hours = np.append(field_diurn.diurnal.values, 24)
            # remove number from obs
            if mkey == 'OBS4':
                mkey = 'OBS'
            # plot mean diurnal cycle
            line, = ax.plot(hours, vals_diurn, color=mdict['col'], label=mkey)
            handles.append(line)


            # if for RAW1 & SM1 plot 
            if mkey in ['RAW1', 'SM1', 'DIFF1']:
                day_range = np.arange(nl.time_sel.start, nl.time_sel.stop+timedelta(days=1),
                                      timedelta(days=1))
                all_days = np.zeros((9,25))
                for dayI in range(len(day_range)-2):
                    this_day = '{:%Y-%m-%d}-00'.format(dt64_to_dt(day_range[dayI]))
                    next_day = '{:%Y-%m-%d}-00'.format(dt64_to_dt(day_range[dayI+1]))
                    day_vals = field.loc[this_day:next_day].values
                    times = field.loc[this_day:next_day].time.values
                    # some datasets do not have 2006071100. Then take next day value
                    if (len(day_vals) == 24) and (dt64_to_dt(times[0]).hour == 1):
                        day_vals = np.append(day_vals[-1], day_vals)
                    all_days[dayI,:] = day_vals
                #for dayI in range(len(day_range)-2):
                #    ax.plot(hours, all_days[dayI,:], color=plot_dict['res_color'][res],
                #            label=mem_res_key, linewidth=0.5)
                quantiles = np.percentile(all_days, nl.percentiles, axis=0)
                ax.fill_between(hours, quantiles[0,:], quantiles[1,:], color='red',
                                alpha=0.2, edgecolor='')
                # significance testing
                #test_type = 'ttest'
                test_type = 'wilcox'
                if test_type == 'ttest':
                    from scipy.stats import ttest_1samp
                if test_type == 'wilcox':
                    from scipy.stats import wilcoxon
                if mkey == 'DIFF1':
                    for hI in range(len(hours)-1):
                        if test_type == 'ttest':
                            pval = ttest_1samp(all_days[:,hI], 0).pvalue
                        elif test_type == 'wilcox':
                            pval = wilcoxon(all_days[:,hI].squeeze()).pvalue
                        #pval = '{:2.2f}'.format(pval)
                        if pval < 0.05:
                            ax.text(hours[hI]+0.15,
                                    ax.get_ylim()[0] + (
                                    ax.get_ylim()[1] - ax.get_ylim()[0])*0.92,
                                    '*', color='red')

            x = 1
            yTop = 0.16
            dy = 0.019
            size = 13

            if pdict['meta']['legend']:
                ax.text(x, yTop-dy*rI, sum, color=mdict['col'], size=size,
                        bbox=dict(boxstyle='square',
                                ec=(1,1,1,0.5),fc=(1,1,1,0.5)))
            rI += 1

        if pdict['meta']['legend']:
            ax.legend(handles=handles, fontsize=12, loc='upper left')
        cI += 1

    PO.add_panel_labels(order='cols')
    #fig.subplots_adjust(left=0.11, right=0.98, bottom=0.15, top=0.91,
    #                        wspace=0.2, hspace=0.1)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.15, top=0.91,
                            wspace=0.25, hspace=0.25)
    PO.finalize_plot()



if __name__ == '__main__':

    timer = Timer(mode='seconds')

    var_name = 'QV'
    members = {}
    for skey in nl.model_keys:
        nc_file = os.path.join(nl.sim_base_dir, skey, 'z{}.nc'.format(var_name))
        ds = xr.open_dataset(nc_file)
        ds = ds.sel(rlon=nl.domain['lon'], rlat=nl.domain['lat'],
                    altitude=slice(0,4000))
        ds = ds.mean(dim=['rlon', 'rlat'])
        field = ds[var_name]
        field = calc_mean_diurnal_cycle(field, aggreg_type='MEAN')
        members[skey] = field

    plot_dir = os.path.join(nl.plot_base_dir)
    Path(plot_dir).mkdir(parents=True, exist_ok=True)

    for hr in range(0,24):
        lines = []
        plt.clf()
        for skey in nl.model_keys:
            field = members[skey]
            hr_field = field.sel(diurnal=hr)
            handle, = plt.plot(hr_field.values, hr_field.altitude,
                                label=skey)
            lines.append(handle)
        plt.legend(handles=lines)
        plt.grid()
        plt.title(hr)
        plt.xlim((0, 0.012))
        plt.xlabel('mean qv [g/kg]')
        plt.ylabel('altitude [m]')
        plt.subplots_adjust(bottom=0.2)
        plt.savefig(os.path.join(plot_dir, 'prof_qv_{}.png'.format(hr)))
    print(field)

    timer.print_report()
