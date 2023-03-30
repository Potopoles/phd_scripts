#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Create specific plot using a namelist
author			Christoph Heim
date created    25.08.2021
date changed    07.05.2022
"""
##############################################################################
import os, argparse, copy, psutil, time, gc
from importlib import import_module, reload
from pathlib import Path
from types import SimpleNamespace
import nl_org_ana as nl_glob
from nl_plot_org_ana import nlp
from package.utilities import Timer
from package.plot_functions import PlotOrganizer#, draw_map
from package.time_processing import Time_Processing as TP
from package.functions import (load_member_var, save_member_to_pickle,
                               save_member_var_to_netcdf,
                               load_member_from_pickle,
                               load_member_var_from_netcdf,
                               time_periods_to_dates,
                               import_namelist)
from package.mp import TimeStepMP
from package.member import Member
##############################################################################



    

if __name__ == '__main__':

    ##########################################################################
    # PREPARATION STEPS
    timer = Timer(mode='seconds')

    ## input arguments
    parser = argparse.ArgumentParser(description = 'Analysis.')
    # analysis namelist
    parser.add_argument('namelist', type=str)
    # number of parallel processes
    parser.add_argument('-p', '--n_par', type=int, default=1)
    # save or not? (0: show, 1: png, 2: pdf, 3: jpg)
    parser.add_argument('-s', '--i_save_fig', type=int, default=3)
    # recompute?
    parser.add_argument('-r', '--i_recompute', type=int, default=0)
    # computation mode? (normal, load, dask)
    parser.add_argument('-c', '--computation_mode', type=str, default='load')
    # first namelist argument
    parser.add_argument('-z', '--dummy', type=str, default='')
    args = parser.parse_args()


    nl_glob.i_recompute = args.i_recompute
    if nl_glob.i_recompute: nl_glob.i_plot = 0
    nl_glob.n_par = args.n_par
    nl_glob.i_save_fig = args.i_save_fig
    nl_glob.computation_mode = args.computation_mode
    # plotting namelist
    nl_glob.nlp = nlp

    ## import configuration dict from ana_org namelist
    #nl_ana_org_case = import_module('ana_nls.{}'.format(args.namelist))
    nl_ana_org_case = import_module(args.namelist.replace('/','.')[:-3])
    setattr(nl_glob, 'cfg', getattr(nl_ana_org_case, 'cfg'))

    ### add attributes applying to all panels to the individual panels
    ### if they are not set individually already.
    #for key,value in nl_glob.cfg['all_panels'].items():
    #    for pan_key,pan_dict in nl_glob.cfg['panels'].items():
    #        if key not in nl_glob.cfg['panels'][pan_key]:
    #            nl_glob.cfg['panels'][pan_key][key] = value

    Path(nl_glob.ana_base_dir).mkdir(parents=True, exist_ok=True)

    ## if recompute, only do this once
    #if nl_glob.i_recompute:
    #    nl_glob.cfg['serial_time_plt_sels'] = [None]

    #for serial_time_plt_sel in nl_glob.cfg['serial_time_plt_sels']:

    if nl_glob.i_plot:
        name_dict = copy.copy(nl_glob.cfg['name_dict'])
        #if serial_time_plt_sel is not None:
        #    name_dict.update({list(serial_time_plt_sel.keys())[0]:
        #            TP.format_time_code(serial_time_plt_sel)})

        PO = PlotOrganizer(
            i_save_fig=nl_glob.i_save_fig,
            path=os.path.join(nl_glob.plot_base_dir, 
                nl_glob.cfg['sub_dir']),
            name_dict=name_dict,
            nlp=nl_glob.nlp, 
            geo_plot=False,
        )
        fig,axes = PO.initialize_plot(
            nrows=nl_glob.cfg['fig']['nrows'],
            ncols=nl_glob.cfg['fig']['ncols'],
            figsize=nl_glob.cfg['fig']['figsize'],
            grid_spec=nl_glob.cfg['fig']['grid_spec'],
            args_subplots_adjust=nl_glob.cfg['fig']['args_subplots_adjust'],
            #pan_cfgs=nl_glob.cfg['panels'],
        )


    # ITERATE OVER ALL PANELS
    ######################################################################
    for pan_key,pan_dict in nl_glob.cfg['panels'].items():

        print('Panel {} ana number {}'.format(pan_key, pan_dict['ana_number']))
        #print(pan_dict)

        # INITIALIZE ANALYSIS OBJECT
        ##################################################################
        Analysis = getattr(import_module(
                            'an_{:02d}'.format(pan_dict['ana_number'])),
                            'Analysis_{:02d}'.format(pan_dict['ana_number']))
        ana = Analysis(nl=SimpleNamespace())

        # PREPARE NAMELIST
        ##################################################################
        nl_ana_raw = import_module('nl_{:02d}'.format(pan_dict['ana_number']))
        # make sure namelist is reloaded from scratch without modifications
        # from last panel
        reload(nl_ana_raw)
        import_namelist(ana.nl, nl_ana_raw)
        ## copy serial selector
        #ana.nl.time_plt_sel = serial_time_plt_sel
        ana.nl.time_plt_sel = None

        # copy attributes from analysis plotting namelist 
        nl_ana_plot_raw = import_module('nl_plot_{:02d}'.format(pan_dict['ana_number']))
        setattr(ana.nl, 'nlp', getattr(nl_ana_plot_raw, 'nlp'))
        #print(ana.nl.nlp['var_plt_cfgs']['P'])
        #quit()

        ana.nl.i_debug = nl_glob.i_debug
        ana.nl.ANA_NATIVE_domain = nl_glob.ANA_NATIVE_domain
        ana.nl.computation_mode = nl_glob.computation_mode
        ana.nl.n_par = nl_glob.n_par

        # TODO, not needed any more, right?
        ## set up member source dictionary
        #if 'mem_keys' in pan_dict:
        #    ana.nl.mem_keys = pan_dict['mem_keys']
        ##print(ana.nl.mem_keys)

        # copy attributes from panel dict (pan_dict) to analysis namelist (ana_nl)
        for attr_key,attr in pan_dict.items():
            #print(attr_key)
            setattr(ana.nl, attr_key, attr)
        #quit()

        ana.prepare_namelist()

        #print(ana.src_mem_dict)
        #print(ana.targ_mem_list)

        # skip if no members to compute
        if len(ana.targ_mem_list) == 0:
            continue

        # should files be computed...
        if nl_glob.i_recompute:
            
            # PART OF ANALYSIS SPECIFIC FOR EACH DAY
            ##############################################################
            timer.start('daily')
            # skip recomputing if indicated
            if not pan_dict['i_recompute']:
                continue
            print('recompute')

            tsmp = TimeStepMP(ana.iter_dates, njobs=ana.nl.n_par,
                              run_async=True)
            fargs = {}
            tsmp.run(ana.compute_src_members_for_date, fargs=fargs,
                    step_args=None)
            timer.stop('daily')
            timer.start('concat')
            ## merge timings from each run with main timer
            #for output in tsmp.output:
            #    timer.merge_timings(output['timer'])
            tsmp.concat_timesteps()
            src_members = tsmp.concat_output['members']
            timer.stop('concat')



            # PART OF ANALYSIS FOR ENTIRE TIME SERIES
            ##############################################################
            # compute aggregation/grouping on entire time series
            timer.start('all')
            ana.indiv_targ_members = ana.aggreg_src_members_to_indiv_targ_members(
                                            src_members)
            timer.stop('all')

            # SAVE DATA TO PICKLE
            ##############################################################
            ana.save_data(ana.indiv_targ_members)
        
        # ... or be reloaded from precomputed pickle files.
        else:
            # LOAD PRECOMPUTED DATA FROM PICKLE
            ##############################################################
            ana.indiv_targ_members = ana.load_data()



        ##################################################################
        ####### PLOTTING
        ##################################################################
        # continue with next panel if not plotting required
        if nl_glob.i_plot:
            # reset plot organizer
            PO.handles = []

            timer.start('prepare')
            #print(ana.indiv_targ_members.keys())
            targ_members = ana.prepare_for_plotting(ana.indiv_targ_members)
            #print(targ_members.keys())
            #quit()
            timer.stop('prepare')

            timer.start('plot')
            ax_rind = int(pan_key.split(',')[0])
            ax_cind = int(pan_key.split(',')[1])
            ## for grid_spec take into account axes in between panels
            ax_rind_tot = 2 * ax_rind
            ax_cind_tot = 2 * ax_cind
            ax_ind_tot = ax_rind_tot*PO.ncols_tot + ax_cind_tot + 1
            # in case of a geo_plot, change projection
            if ana.nl.nlp['geo_plot']:
                PO.axes[ax_rind, ax_cind].remove()
                ax = PO.fig.add_subplot(
                                #nl_glob.cfg['fig']['nrows'], nl_glob.cfg['fig']['ncols'],
                                PO.nrows_tot, PO.ncols_tot,
                                ax_ind_tot, 
                                projection=ana.nl.nlp['projection'])
                PO.axes[ax_rind, ax_cind] = ax
            else:
                ax = PO.axes[ax_rind, ax_cind]

            ax = PO.axes[ax_rind, ax_cind]
            ana.draw_axis(PO, targ_members, ax)

            timer.stop('plot')

        #else:
        #    print('no plotting')
        #    print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
        #    time.sleep(5)
        #    #quit()


    ### FINAL FORMATTING
    ######################################################################
    if nl_glob.i_plot:
        timer.start('plot')

        ## panel labels
        i_add_panel_labels = nlp['i_add_panel_labels']
        # overwrite default
        if 'i_add_panel_labels' in nl_glob.cfg:
            i_add_panel_labels = nl_glob.cfg['i_add_panel_labels']
        if i_add_panel_labels:
            kwargs_panel_labels = nlp['kwargs_panel_labels']
            # overwrite default
            if 'kwargs_panel_labels' in nl_glob.cfg:
                kwargs_panel_labels.update(
                                nl_glob.cfg['kwargs_panel_labels'])
            PO.add_panel_labels(
                order='cols', 
                **kwargs_panel_labels,
            )

        ### format subplot positions
        #if 'subplots_adjust_lineplot' in nl_glob.cfg:
        #    #print(nl_glob.cfg['subplots_adjust'])
        #    #print(nl_glob.nlp[
        #    #            'args_subplots_adjust_dict'])
        #    args_subplots_adjust = nl_glob.nlp[
        #                'args_subplots_adjust_dict_lineplot'][
        #                        nl_glob.cfg['subplots_adjust_lineplot']]
        #elif 'subplots_adjust_spatial' in nl_glob.cfg:
        #    #print(nl_glob.cfg['subplots_adjust'])
        #    #print(nl_glob.nlp[
        #    #            'args_subplots_adjust_dict'])
        #    args_subplots_adjust = nl_glob.nlp[
        #                'args_subplots_adjust_dict_spatial'][
        #                        nl_glob.cfg['subplots_adjust_spatial']]
        #else:
        #    raise ValueError()

        ### overwrite default settings for subplot positions
        #if 'args_subplots_adjust' in nl_glob.cfg:
        #    for key,val in nl_glob.cfg['args_subplots_adjust'].items():
        #        args_subplots_adjust[key] = val

        ##print(args_subplots_adjust)
        ##quit()
        #PO.fig.subplots_adjust(**args_subplots_adjust)

        PO.remove_axis_labels(**nl_glob.cfg['fig']['kwargs_remove_axis_labels'])
        for label_cfg in nl_glob.cfg['fig']['label_cfgs']:
            PO.add_text_label(**label_cfg)
        PO.finalize_plot()
        timer.stop('plot')

    timer.print_report()
