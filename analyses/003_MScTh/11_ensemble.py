#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Calculate ensemble statistics for precipitation
author			Christoph Heim
date created    04.11.2019
date changed    04.11.2019
usage           args:
                1st:    number of parallel tasks
"""
###############################################################################
import os, collections
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
import nl_11 as nl
from datetime import timedelta, datetime
from nl_plot import nlp
from package.nl_models import nlm
from package.nl_variables import nlv, dimx, dimy, dimz, dimt
from package.model_pp import preproc_model, subsel_domain
from package.plot_functions import PlotOrganizer
from package.utilities import Timer
from package.member import Member
from package.variable import Variable
from package.MP import TimeStepMP
from package.functions import calc_mean_diurnal_cycle
###############################################################################


def compute(ts):
    """
    """
    timer = Timer()


    members = {}
    for mkey,slist in nl.use_sims.items():
        if nl.i_verbosity:
            print(mkey)
        timer.start(mkey)
        for sdict in slist:
            skey = '{}_{:g}'.format(mkey,sdict['res'])  
            if nl.i_verbosity:
                print('\t {}'.format(skey))

            sim_data_dir = os.path.join(nl.sim_base_dir, skey,
                                 sdict['sim'])
            ds = xr.open_dataset(os.path.join(sim_data_dir,
                                  '{}.nc'.format(nl.var_name)))

            ds = preproc_model(ds, mkey, sim_data_dir, nl,
                                nl.domain, ts,
                               dims=nlv[nl.var_name]['dims'])
            vkey = nlm[mkey]['vkeys'][nl.var_name]
            var = ds[vkey]
            #var = subsel_domain(var, mkey, nl.domain)

            var = var.diff(dim='time')

            #print(var.mean(dim='time'))
            #var = calc_mean_diurnal_cycle(var, aggreg_type='MEAN')
            #print(var.mean(dim='diurnal'))
            #quit()
            #daytime = var.sel(diurnal=[9,10,11,12,13,14,15,16,17,18,19,20]).sum(dim='diurnal')
            #nighttime = var.sel(diurnal=[21,22,23,0,1,2,3,4,5,6,7,8]).sum(dim='diurnal')

            var.to_netcdf('RAW3.nc')
            #var.to_netcdf('SM3.nc')
            #daytime.to_netcdf('RAW1_daytime.nc')
            #nighttime.to_netcdf('RAW1_nighttime.nc')

            #member = Member(var, {'label':skey})
            #members[skey] = member
        timer.stop(mkey)

    output = {'timer':timer, 'members':members}
    return(output)


def make_plot():

    daytime = xr.open_dataset('RAW1_daytime.nc')
    nighttime = xr.open_dataset('RAW1_nighttime.nc')

    nrows = nl.cfg['nrows']
    ncols = nl.cfg['ncols']

    #var = Variable(members)   
    #var.calc_statistics()

    timer.start('plot')
    name_dict = collections.OrderedDict()
    name_dict[''] = 'precip'

    PO = PlotOrganizer(nl.i_save_fig,
                       path=os.path.join(nl.plot_base_dir),
                       name_dict=name_dict, nlp=nlp)
    fig,axes = PO.initialize_plot(nrow=nrows, ncol=ncols)
    ax = axes[0,0] 

    ax.contourf(daytime.lon, daytime.lat, daytime.values)
    plt.show()
    quit()

    for skey,sim in ordered.items():
        print(skey)
        sim.field = sim.field.mean(dim='time')
        line, = ax.plot(sim.field.lon.values, sim.field.values,
                        label=skey)
        PO.handles.append(line)


    plt.title('Height of strongest inversion '+
              '{:%d.%m.%Y} - {:%d.%m.%Y}'.format(
              nl.time_sel.start, nl.time_sel.stop))
    ax.legend(handles=PO.handles)
    ax.set_xlabel('longitude [° East]')
    ax.set_ylabel('altitude [m]')
    ax.set_xlim((sim.field.lon.values[0], sim.field.lon.values[-1]))
    ax.set_ylim((0, 3500))
    #ax.grid()

    ## adjustments
    #fig.subplots_adjust(left=0.07, bottom=0.20, right=0.98, top=0.91,
    #                    wspace=0.03, hspace=0.1)

    stretch = 1.0
    fig.set_size_inches(12.9*stretch,6.5*stretch)

    PO.finalize_plot()
    timer.stop('plot')






if __name__ == '__main__':

    timer = Timer(mode='seconds')

    time_steps = np.arange(nl.time_sel.start,
                           nl.time_sel.stop+nl.time_dt, nl.time_dt).tolist()
    if nl.i_recompute:
        compute(time_steps)
    #tsmp = TimeStepMP(time_steps, njobs=nl.njobs, run_async=False)
    #tsmp.run(compute, fargs={}, step_args=None)
    #tsmp.concat_timesteps()

    ## merge timings from each run with main timer and print report
    #for output in tsmp.output:
    #    timer.merge_timings(output['timer'])

    #make_plot(tsmp.concat_output['members'])
    #make_plot()

    timer.print_report()
