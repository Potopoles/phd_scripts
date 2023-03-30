#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     comparison of COSMO-12 run at single or double
                compute and plot time average difference for fields
author			Christoph Heim
date created    10.09.2019
date changed    12.09.2019
"""
###############################################################################
import sys, os, collections, copy
import nl_00 as nl
from nl_plot import nlp
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
from package.nl_models import nlm
from package.nl_variables import nlv
from package.model_pp import preproc_model, subsel_domain, dim2D
from package.plot_functions import PlotOrganizer, draw_map
from package.utilities import Timer
from package.member import Member
from package.variable import Variable
from package.MP import TimeStepMP
###############################################################################



def draw_mean_diff_map(time_sel):
    """
    compute time mean difference of two fields and draw map
    """
    timer = Timer()

    members = {}
    for skey,sdict in nl.use_sims.items():
        mkey = sdict['mkey']
        print(skey)
        timer.start(skey)

        # open dataset and preprocess
        ds = xr.open_dataset(os.path.join(nl.data_base_dir,
                                sdict['sim'],nl.var_name+'.nc'),)
                                #chunks={'time':5})
        ds = preproc_model(ds, mkey, sdict['res'], 
                           nl, nl.domain, dim=dim2D)
        ds = subsel_domain(ds, mkey, nl.domain)
        ds = ds.sel(time=time_sel)

        # select variable
        vkey = nlm[mkey]['vkeys'][nl.var_name]
        var = ds[vkey]
        var = var.mean('time')

        member_label = '{}    {}'.format(nlv[nl.var_name]['lo_name'],
                                      nl.use_sims[skey]['label'])
        member = Member(var, {}, label=member_label, variable=None)
        members[skey] = member
        timer.stop(skey)


    # average all members in float and double
    #print()
    for prec in ['float', 'double']:
    #for prec in ['float']:
        print(prec)
        main = members[prec]
        print('initial')
        print(main.field.mean().values)
        #print()
        n_average = 1
        for skey,sdict in nl.use_sims.items():
            if (sdict['prec'] == prec) and (skey != prec):
                n_average += 1
                #print(skey)
                #print(members[skey].field.mean().values)
                main.field += members[skey].field
                #print(main.field.mean().values)

        main.field /= n_average
        print('final')
        print(main.field.mean().values)

    #quit()

    nrows = nl.cfg['nrows']
    ncols = nl.cfg['ncols']

    var = Variable(members)   
    var.calc_statistics()
    #var.stats['max'] = 0.10

    # compute difference and create new member
    diff = copy.deepcopy(members['float'].field)
    diff.values -= members['double'].field.values
    diff_label = '{}    COSMO-12 float - double'.format(
                            nlv[nl.var_name]['lo_name'])
    diff = Member(diff, {}, label=diff_label, variable=None)
    members['diff'] = diff

    ### PLOT
    timer.start('plot')
    name_dict = collections.OrderedDict()
    name_dict['var']    = nl.var_name
    name_dict['mem'] = nl.run_mode

    PO = PlotOrganizer(nl.i_save_fig,
                       path=os.path.join(nl.plot_base_dir, nl.cfg['subpath']),
                       name_dict=name_dict, nlp=nlp,
                       geo_plot=True)
    fig,ax = PO.initialize_plot(nrow=nrows, ncol=ncols)

    plot_member = members[nl.run_mode]

    draw_map(ax, nl.domain, nlp, add_xlabel=True, add_ylabel=True,
             dticks=20)
    plot_member.plot_lat_lon(ax, nlp=nlp)

    #cax = fig.add_axes([0.07, 0.09, 0.90, 0.03])
    cax = fig.add_axes([0.14, 0.09, 0.80, 0.03])
    colorbar = plt.colorbar(mappable=plot_member.mappable, cax=cax, 
                            orientation='horizontal')
    cax.set_xlabel('{} [{}]'.format(nlv[nl.var_name]['label'],
                                    nlv[nl.var_name]['unit']))
    fig.subplots_adjust(left=0.10, bottom=0.22, right=0.98, top=0.95,
                        wspace=0.03, hspace=0.1)
    fig.set_size_inches(8.5,7)

    PO.finalize_plot()
    timer.stop('plot')

    output = {'timer':timer}
    return(output)







if __name__ == '__main__':

    timer = Timer(mode='seconds')

    output = draw_mean_diff_map(nl.time_sel)
    timer.merge_timings(output['timer'])

    timer.print_report()
