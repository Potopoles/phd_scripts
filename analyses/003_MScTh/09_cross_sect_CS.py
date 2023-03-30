#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Compute cross-sections of QC and QI
author			Christoph Heim
date created    10.10.2019
date changed    11.10.2019 
usage           args:
                1st:    number of parallel tasks
"""
###############################################################################
import os, collections
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
import nl_09 as nl
from nl_plot import nlp
from package.nl_models import nlm
from package.nl_variables import nlv, dimx, dimy, dimz, dimt
from package.model_pp import preproc_model, subsel_domain
from package.plot_functions import PlotOrganizer
from package.utilities import Timer
from package.member import Member
from package.variable import Variable
from package.MP import TimeStepMP
###############################################################################


###############################################################################
# compute a cross-section
###############################################################################
def compute_cross_sections(ts):
    """
    """

    timer = Timer()

    ts_string = '{:%Y-%m-%d %H:%M}'.format(ts)
    ts_code = '{:%Y%m%d_%H%M}'.format(ts)

    vars = {}
    for var_name in nl.var_names:
        print(var_name)
        dims = nlv[var_name]['dims']

        sims = {}
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
                                                  '{}.nc'.format(var_name)))
                ds = preproc_model(ds, mkey, sim_data_dir, nl,
                                   nl.domain, dims=dims)
                
                if dimt in  dims:
                    ds = ds.sel(time=ts)
                #ds = subsel_domain(ds, mkey, nl.domain)
                ds = ds.sel(lat=nl.cfg['lat_slice'])
                ds = ds.sel(lon=nl.cfg['lon_slice'])
                ds = ds.max(dim='lon')
                if dimz in  dims:
                    ds = ds.sortby('alt')
                    ds = ds.sel(alt=slice(0,10000))
                vkey = nlm[mkey]['vkeys'][var_name]
                var = ds[vkey]

                member = Member(var, {'label':skey})
                sims[skey] = member
            timer.stop(mkey)

        var = Variable(sims)   
        var.calc_statistics()

        vars[var_name] = var


    timer.start('plot')
    nrows = nl.cfg['nrows']
    ncols = nl.cfg['ncols']

    name_dict = collections.OrderedDict()
    name_dict[''] = ts_code

    PO = PlotOrganizer(nl.i_save_fig,
                       path=os.path.join(nl.plot_base_dir,'test'),
                       name_dict=name_dict, nlp=nlp)
    fig,axes = PO.initialize_plot(nrow=nrows, ncol=ncols)

    col_ind = 0
    row_ind = 0
    for mkey,slist in nl.use_sims.items():
        for sdict in slist:
            skey = '{}_{:g}'.format(mkey,sdict['res'])  
            print(skey)
            ax = axes[row_ind, col_ind]

            HSURF   = vars['HSURF'].members[skey]
            QC      = vars['QC'].members[skey]
            lat = HSURF.field.lat.values
            alt = QC.field.alt.values
            #print(sim.field.values)
            #quit()
            QC.mappable = ax.contourf(lat, alt, QC.field.values, cmap=nlp['cmap'])
            #plt.colorbar()
            ax.fill_between(lat, 0, HSURF.field.values.squeeze(), color='k')
            ax.set_ylim((0,10000))

            #if col_ind > 0:
            #   ax.set_yticklabels([]) 
            #   ax.set_ylabel('')
            #if row_ind < nrows-1:
            #   ax.set_xticklabels([]) 
            #   ax.set_xlabel('')

            #plt.suptitle(ts_string)

            col_ind += 1

    #quit()

    # adjustments
    cax = fig.add_axes([0.15, 0.10, 0.70, 0.03])
    fig.subplots_adjust(left=0.07, bottom=0.20, right=0.98, top=0.91,
                        wspace=0.03, hspace=0.1)
    stretch = 1.2
    fig.set_size_inches(12.9*stretch,6.5*stretch)

    ## colorbar
    #colorbar = plt.colorbar(mappable=var.mappable, cax=cax, 
    #                        orientation='horizontal')
    #cax.set_xlabel('QC [kg kg$^{-1}$]')

    PO.finalize_plot()
    timer.stop('plot')

    output = {'timer':timer}
    return(output)





if __name__ == '__main__':

    timer = Timer(mode='seconds')

    time_steps = np.arange(nl.time_sel.start,
                           nl.time_sel.stop, nl.time_dt).tolist()

    tsmp = TimeStepMP(time_steps, njobs=nl.njobs, run_async=False)
    tsmp.run(compute_cross_sections, fargs={}, step_args=None)

    # merge timings from each run with main timer and print report
    for output in tsmp.output:
        timer.merge_timings(output['timer'])

    timer.print_report()
