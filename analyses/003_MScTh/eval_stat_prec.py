#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Validate model with station observations for precipitation
author			Christoph Heim
date created    07.11.2019
date changed    02.03.2020
usage           no args
"""
###############################################################################
import os
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import nl_eval_stat_prec as nl
import nl_plot as nlp
from package.utilities import Timer, calc_mean_diurnal_cycle
from package.plot_functions import PlotOrganizer
###############################################################################


def preproc_station_data():

    # station meta data
    stat_meta_path = os.path.join(nl.obs_base_dir, nl.stat_meta_name)
    stat_meta = np.genfromtxt(stat_meta_path, dtype=np.str, delimiter='\t')
    stat_keys = []
    stat_lat = np.zeros(len(stat_meta))
    stat_lon = np.zeros(len(stat_meta))
    for rI,row in enumerate(stat_meta):
        splits = row.split(' ')
        stat_key = splits[0]
        latlon = splits[-1].split('/')
        lon_deg_min = latlon[0].split('deg')
        lat_deg_min = latlon[1].split('deg')
        stat_lon[rI] = float(lon_deg_min[0]) + float(lon_deg_min[1][0:2])/60
        stat_lat[rI] = float(lat_deg_min[0]) + float(lat_deg_min[1][0:2])/60
        stat_keys.append(stat_key)

    print('N STATIONS')
    print(len(stat_keys))

    stat_data_path = os.path.join(nl.obs_base_dir, nl.stat_data_name)
    stat_data_in = np.genfromtxt(stat_data_path, dtype=np.str, delimiter=';', skip_header=1)
    dts = [datetime.strptime(dt, '%Y%m%d%H') for dt in \
                stat_data_in[np.ix_(stat_data_in[:,0] == stat_keys[0]),(1,)][0]]
    # station data
    stat_data = {}
    for stat_key in stat_keys:
        stat_data[stat_key] = pd.to_numeric(stat_data_in[np.ix_(
                                stat_data_in[:,0] == stat_key),(2)][0],
                                errors='coerce')

    # wrapper for entire data and meta data
    data = {'stat_keys':stat_keys, 'stat_data':stat_data, 'stat_dts':dts,
            'stat_lon':stat_lon, 'stat_lat':stat_lat}

    ## create grid description to remap rotated COSMO grid
    #for dlon in [0.01, 0.02, 0.04]:
    #nlat = (max(stat_lat)-min(stat_lat))/dx
    #nlon = (max(stat_lat)-min(stat_lat))/dx
    ##print(stat_lon[0])
    ##print(stat_lat[0])
    ##quit()

    ##dx = 0.04
    ##print('{} {}'.format(min(stat_lon),max(stat_lon)))
    ##print((max(stat_lon)-min(stat_lon))/dx)
    ##print('{} {}'.format(min(stat_lat),max(stat_lat)))
    ##quit()
    return(data)




def preproc_model_data(data, model_key):
    print(model_key)

    model_data_path = os.path.join('PP_latlon_{}.nc'.format(model_key))
    model_data = xr.open_dataset(model_data_path)['TOT_PREC']
    grid_lon = model_data.longitude.values
    grid_lat = model_data.latitude.values
    model_dts = model_data.time

    proc_model_data = {}
    for si,stat_key in enumerate(data['stat_keys']):
        #print(stat_key)
        lon = data['stat_lon'][si]
        lat = data['stat_lat'][si]
        lon_ind = np.argmin(np.abs(grid_lon - lon))
        lat_ind = np.argmin(np.abs(grid_lat - lat))
        precip = model_data.values[:,lat_ind,lon_ind]
        proc_model_data[stat_key] = precip

    data['model_dts'] = pd.to_datetime(model_dts.values, unit='us')
    data['{}_data'.format(model_key)] = proc_model_data
    return(data)


#def aggregate_stations_and_diurnal(data):
def aggregate_stations(data):
    # determin indices in time to use for obs and model data
    stat_dts = np.asarray([np.datetime64(dt) for dt in data['stat_dts']])
    use_inds_stat = (stat_dts >= nl.time_sel.start) & (stat_dts <= nl.time_sel.stop)
    model_dts = data['model_dts']
    use_inds_model = (model_dts >= nl.time_sel.start) & (model_dts <= nl.time_sel.stop)
    dts = stat_dts[use_inds_stat]
    # determine size of output arrays
    nstat = len(data['stat_keys'])
    ndt = np.sum(use_inds_model)
    obs = np.zeros((ndt, nstat))
    for si,stat_key in enumerate(data['stat_keys']):
        obs[:,si] = data['stat_data'][stat_key][use_inds_stat]
    obs = np.nanmean(obs,axis=1)
    obs = xr.DataArray(obs, coords=[dts], dims=['time'])
    #obs = calc_mean_diurnal_cycle(obs, aggreg_type='MEAN')
    diurnal = {}
    diurnal['OBS'] = obs

    for model_key in nl.model_keys:
        model = np.zeros((ndt, nstat))
        for si,stat_key in enumerate(data['stat_keys']):
            model[:,si] = data['{}_data'.format(model_key)][stat_key][use_inds_model]
        model = np.nanmean(model,axis=1)
        model = xr.DataArray(model, coords=[dts], dims=['time'])
        #model = calc_mean_diurnal_cycle(model, aggreg_type='MEAN')
        diurnal[model_key] = model
    #data = xr.Dataset(diurnal)
    return(diurnal)
    

def draw_plot(data):
    name_dict = {'':'prec_domAv_stat'}
    PO = PlotOrganizer(i_save_fig=nl.i_save_fig, path=nl.plot_base_dir,
                  name_dict=name_dict)
    fig,axes = PO.initialize_plot(nrows=1, ncols=2, figsize=(9,4))
    cI = 0
    for key,pdict in nl.plot_dict.items():
        ax = axes[pdict['meta']['ax_inds'][0],pdict['meta']['ax_inds'][1]]
        handles = []
        rI = 0
        for mkey,mdict in pdict['data'].items():
            print(mkey)
            values = data[mkey].values

            sum = str(round(np.sum(values),1)) + ' mm' 

            values = np.append(values, values[0])
            hours = np.append(data.diurnal.values, 24)
            line, = ax.plot(hours, values, color=mdict['col'], label=mkey)
            handles.append(line)

            x = 1
            yTop = 0.16
            dy = 0.019
            size = 13
            ax.text(x, yTop-dy*rI, sum, color=mdict['col'], size=size,
                    bbox=dict(boxstyle='square',ec=(1,1,1,0.5),fc=(1,1,1,0.5)))
            rI += 1

        ax.legend(handles=handles, fontsize=12, loc='upper left')
        ax.set_title(pdict['meta']['ax_title'])
        ax.set_xlim(pdict['meta']['ax_xlim'])
        ax.set_ylim(pdict['meta']['ax_ylim'])
        ax.set_xlabel(pdict['meta']['ax_xlabel'])
        if cI == 0:
            ax.set_ylabel(pdict['meta']['ax_ylabel'])
        ax.set_xticks(np.arange(0,24.1,6))
        ax.grid()
        cI += 1


        panel_labels = ['e)', 'f)']
        lind = 0
        for ax in axes[0,:]:
            # make panel label
            pan_lab_x = ax.get_xlim()[0]
            pan_lab_y = ax.get_ylim()[1] + (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.04
            ax.text(pan_lab_x,pan_lab_y,panel_labels[lind], fontsize=15, weight='bold')
            lind += 1


    fig.subplots_adjust(left=0.11, right=0.98, bottom=0.15, top=0.91,
                            wspace=0.2, hspace=0.1)
    PO.finalize_plot()
    



if __name__ == '__main__':

    timer = Timer(mode='seconds')

    timer.start('statpp')
    data = preproc_station_data()
    timer.stop('statpp')
    timer.start('modelpp')
    for model_key in nl.model_keys:
        data = preproc_model_data(data, model_key)
    timer.stop('modelpp')
    timer.start('aggreg')
    data = aggregate_stations_and_diurnal(data)
    timer.stop('aggreg')
    timer.start('plot')
    draw_plot(data)
    timer.stop('plot')

    time_steps = np.arange(nl.time_sel.start,
                           nl.time_sel.stop, nl.time_dt).tolist()

    timer.print_report()
