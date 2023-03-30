#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     - comparison of COSMO@4km runs nested into COSMO@12km for 
                different domains
                - comparison of COSMO@2km runs nested either directly into
                COSMO@12km or nested into COSMO@4km
author			Christoph Heim
date created    16.09.2019
date changed    08.10.2019
args            1st - njobs (not used currently)
                2nd - run_mode (see nl_01)
                3rd - var_name (see nl_01)
"""
###############################################################################
import sys, os, collections, copy, glob
import xarray as xr
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import nl_01 as nl
import matplotlib
if nl.i_save_fig == 1:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt
from cdo import Cdo
from package.nl_models import nlm, nld
from package.nl_variables import nlv, dimx, dimy, dimz, dimt
from package.model_pp import preproc_model, subsel_domain
from package.plot_functions import PlotOrganizer, draw_map, draw_domain
from package.utilities import Timer, write_grid_file
from package.member import Member
from package.variable import Variable
from package.MP import TimeStepMP
###############################################################################


def remap_sat(domain, time_sel):
    print('remap {}'.format('sat'))
    sat_dts = np.arange(time_sel.start, time_sel.stop+timedelta(days=1),
                        timedelta(days=1)).tolist()
    write_grid_file(domain, nl.grid_file_path, nl.grid_dx) 
    out_folder = os.path.join(nl.ana_base_dir, 'obs', 'seviri_ceres')
    Path(out_folder).mkdir(parents=True, exist_ok=True)
    # if recompute, first remove all files
    if nl.recompute_sat:
        for file in os.listdir(out_folder):
            os.remove(os.path.join(out_folder,file))

    for sat_dt in sat_dts:
        #print('TRSdm{:%Y%m%d}*'.format(sat_dt))
        inp_file_path = os.path.join(nl.obs_data_dir, 'seviri_ceres', 'trs',
                                 'TRSdm{:%Y%m%d}*'.format(sat_dt))
        inp_file_path = glob.glob(inp_file_path)[0]
        out_file_path = os.path.join(out_folder, 
                            'SWUTOA_{:%Y%m%d}.nc'.format(sat_dt))
        if (not os.path.exists(out_file_path)) or nl.recompute_sat:
            cdo.remapbil(nl.grid_file_path, input=inp_file_path,
                        output=out_file_path)
    
    # merge files
    inp_files = glob.glob(os.path.join(out_folder, 'SWUTOA_*'))
    out_file = os.path.join(out_folder, 'SWUTOA.nc')
    if (not os.path.exists(out_file)) or nl.recompute_sat:
        cdo.mergetime(input=inp_files, output=out_file)
    return(out_file)




def remap_model(domain, time_sel, sim_dict, sim_key, var_name):
    print('remap var {} for sim {}'.format(var_name, sim_key))
    write_grid_file(domain, nl.grid_file_path, nl.grid_dx) 

    out_folder = os.path.join(nl.ana_base_dir, 'model', sim_key)
    Path(out_folder).mkdir(parents=True, exist_ok=True)

    inp_file_path = os.path.join(nl.cosmo_data_dir,
                                '{}_{}'.format(sim_dict['mkey'],
                                               sim_dict['res']),
                                sim_dict['sim'],var_name+'.nc') 
    out_file_path = os.path.join(out_folder, var_name+'.nc')
    if (not os.path.exists(out_file_path)) or nl.recompute_mod:
        cdo.remapbil(nl.grid_file_path, input=inp_file_path, output=out_file_path)
    return(out_file_path)



def load_var(nl, mkey, sdict, var_name, time_sel, inp_file_path=None):
    # open dataset and preprocess
    if inp_file_path is None:
        inp_file_path = os.path.join(nl.cosmo_data_dir,
                                    '{}_{}'.format(sdict['mkey'],
                                                   sdict['res']),
                                    sdict['sim'],var_name+'.nc') 
    ds = xr.open_dataset(inp_file_path)#, chunks={'time':1})
    print(var_name)
    dims = nlv[var_name]['dims']
    ds = preproc_model(ds, mkey, sdict['res'], 
                       nl, nl.domain, dim=dims)
                       
    ds = subsel_domain(ds, mkey, nl.domain)
    ds = ds.sel(time=time_sel)
    print(ds.dims)

    # select variable
    vkey = nlm[mkey]['vkeys'][var_name]
    var = ds[vkey]
    var = var.mean('time')

    #plt.contourf(var.values[:,:].squeeze())
    #plt.colorbar()
    #plt.show()
    #quit()

    return(var)



    


def draw_mean_diff_map(time_sel):
    """
    compute time mean difference of two fields and draw map
    """
    #timer = Timer()

    members = {}
    diff_members = {}

    # load satellite
    if nl.run_mode == 'eval_seviri':
        timer.start('satellite')
        sat_path = remap_sat(nl.domain, time_sel)

        # open dataset and preprocess
        ds = xr.open_dataset(sat_path)
        ds = ds.sel(time=time_sel)
        vkey = nld['SEVIRI']['vkeys']['SWUTOA']
        var = ds[vkey]
        var = var.mean('time')
        member_label = '{}'.format('OBS: SEVIRI')
        member = Member(var, {'label':member_label}, variable=None)
        members['SEVIRI'] = member
        timer.stop('satellite')

        ## load model downard shortwave radiation for all simulations
        #model_path = remap_model(nl.domain, time_sel, nl.noland12_config,
        #                         'noland12', 'SWDTOA')
        #ds = xr.open_dataset(model_path)
        #ds = subsel_domain(ds, 'COSMO', nl.domain)
        #ds = ds.sel(time=time_sel)
        #vkey = nlm['COSMO']['vkeys']['SWDTOA']
        #var = ds[vkey]
        #var_SWDTOA = var.mean('time')


    # load models
    for skey,sdict in nl.use_sims.items():
        mkey = sdict['mkey']
        print(skey)
        timer.start(skey)

        if nl.run_mode == 'eval_seviri':
            # remap SWNDTOA onto satellite domain and load
            this_var_name = 'SWNDTOA'
            model_path = remap_model(nl.domain, time_sel, sdict, skey,
                                     this_var_name)
            SWNDTOA = load_var(nl, mkey, sdict, this_var_name, time_sel, inp_file_path=model_path)
            # remap SWDTOA onto satellite domain and load
            this_var_name = 'SWDTOA'
            model_path = remap_model(nl.domain, time_sel, sdict, skey,
                                     this_var_name)
            SWDTOA = load_var(nl, mkey, sdict, this_var_name, time_sel, inp_file_path=model_path)
            # compute reflected shortwave at TOA
            var = SWDTOA - SWNDTOA

            # compute difference
            diff = var - members['SEVIRI'].field
            member_label = '{}    {} - SEVIRI'.format(
                                    nlv[nl.var_name]['lo_name'],
                                    nl.use_sims[skey]['label'] )
            member = Member(diff, {'label':member_label}, variable=None)
            diff_members[skey] = member
        else:
            # open dataset and preprocess
            var = load_var(nl, mkey, sdict, nl.var_name, time_sel)

        member_label = '{}    {}'.format(nlv[nl.var_name]['lo_name'],
                                      nl.use_sims[skey]['label'])
        member = Member(var, {'label':member_label,
                              'sim_key':skey}, variable=None)
        members[skey] = member

        timer.stop(skey)

    # compute differences for run_mode == 'var'
    if 'diffs' in nl.cfg.keys():
        for diff in nl.cfg['diffs']:
            diff1_key = diff[0]
            diff2_key = diff[1]
            diff = copy.deepcopy(members[diff1_key].field)
            diff = diff - members[diff2_key].field
            member_label = '{} "{}" - "{}"'.format(
                                nlv[nl.var_name]['lo_name'],
                                diff1_key, diff2_key)
            member = Member(diff, {'label':member_label}, variable=None)
            diff_key = '{}-{}'.format(members[diff1_key].mem_dict['sim_key'],
                                      members[diff2_key].mem_dict['sim_key'])
            diff_members[diff_key] = member


    nrows = nl.cfg['nrows']
    ncols = nl.cfg['ncols']

    # compute maximum and minimum values
    Variable(members).calc_statistics()
    Variable(diff_members).calc_statistics(True)

    # differentiate between plotting values or differences
    if nl.run_mode in ['eval_seviri']:
        use_members = diff_members
    else:
        members.update(diff_members)
        use_members = members

    ### PLOT
    timer.start('plot')
    for mkey,member in use_members.items():
        print('plot {}'.format(mkey))
        name_dict = collections.OrderedDict()
        name_dict[nl.run_mode] = nl.var_name
        name_dict['sim'] = mkey
        
        PO = PlotOrganizer(nl.i_save_fig,
                           path=os.path.join(nl.plot_base_dir, nl.cfg['subpath']),
                           name_dict=name_dict, nlp=nl.nlp,
                           geo_plot=True)
        fig,axes = PO.initialize_plot(nrow=nrows, ncol=ncols)
        ax = axes[0,0]

        draw_map(ax, nl.domain, nl.nlp, add_xlabel=True, add_ylabel=True,
                 dticks=10)
        timer.start('latlon')
        member.plot_lat_lon(ax, nlp=nl.nlp)
        timer.stop('latlon')
        mean_label = 'abs: {:0.1f}'.format(np.mean(np.abs(member.field.values)))
        ax.legend(loc='lower left', labels=[mean_label])
        #line = draw_domain(PO.ax, nl.dom2, nl.nlp, color='red',
        #                   linestyle='-', linewidth=2, zorder=1) 

        cax = fig.add_axes([0.14, 0.12, 0.80, 0.04])
        colorbar = plt.colorbar(mappable=member.mappable, cax=cax, 
                                orientation='horizontal')
        cax.set_xlabel('{} [{}]'.format(nlv[nl.var_name]['label'],
                                        nlv[nl.var_name]['unit']))
        fig.subplots_adjust(left=0.11, bottom=0.26, right=0.98, top=0.95,
                            wspace=0.03, hspace=0.1)
        fig.set_size_inches(8,5.5)

        timer.start('finalize')
        PO.finalize_plot()
        timer.stop('finalize')
    timer.stop('plot')

    output = {'timer':timer}
    return(output)







if __name__ == '__main__':
    print('################################')
    print(nl.run_mode)
    print(nl.var_name)
    print('################################')

    timer = Timer(mode='seconds')

    ## PREPARATIONS
    Path(nl.ana_base_dir).mkdir(parents=True, exist_ok=True)
    cdo = Cdo()

    output = draw_mean_diff_map(nl.time_sel)
    timer.merge_timings(output['timer'])

    timer.print_report()
