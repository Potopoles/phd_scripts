#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    analysis namelist
author			Christoph Heim
"""
###############################################################################
import copy
from datetime import datetime, timedelta
from package.time_processing import Time_Processing as TP
from base.nl_domains import *
from base.nl_time_periods import *
from nl_plot_org_ana import nlp
from package.nl_variables import nlv
from ana_nls.glob_cfgs import *
###############################################################################
args_subplots_adjust = {
    '5x3': {
        'left':0.11,
        'bottom':0.11,
        'right':0.92,
        'top':0.95,
        'wspace':0,
        'hspace':0,
    },
    '6x3': {
        'left':0.06,
        'bottom':0.09,
        'right':0.95,
        'top':0.95,
        'wspace':0,
        'hspace':0,
    },
}


#models_cmip6 = models_cmip6_cldf#[5:7]
#mem_keys_cmip6_hist = ['{}_historical'.format(model) for model in models_cmip6]
#mem_keys_cmip6_scen = ['{}_ssp585'.format(model) for model in models_cmip6]
#mem_keys_cmip6_change = [{
#    'mem_oper':'diff',
#    'mem_keys':[
#        {
#            'mem_key':      '{}_ssp585'.format(model), 
#            'time_periods': time_periods_cmip6_scen,
#        },
#        {
#            'mem_key':      '{}_historical'.format(model), 
#            'time_periods': time_periods_cmip6_hist,
#        },
#    ]} for model in models_cmip6
#]
#mem_keys_cmip6_bias = [{
#    'mem_oper':'bias',
#    'mem_keys':[
#        {
#            'mem_key':      '{}_historical'.format(model), 
#            'time_periods': time_periods_cmip6_hist,
#        },
#        {
#            'mem_key':      'ERA5', 
#            'time_periods': time_periods_default,
#        },
#    ]} for model in models_cmip6
#]
#
#ctrl = {
#    'mem_key':      'COSMO_3.3_ctrl', 
#}
#ctrl_rdheight2_spubc1 = {
#    'mem_key':      'COSMO_3.3_ctrl_rdheight2_spubc1', 
#}
#ctrl_rdheight2 = {
#    'mem_key':      'COSMO_3.3_ctrl_rdheight2', 
#}
#pgw = {
#    'mem_key':      'COSMO_3.3_pgw', 
#}
#pgw_rdheight2 = {
#    'mem_key':      'COSMO_3.3_pgw_rdheight2', 
#}
#era = {
#    'mem_key':      'ERA5', 
#}
#mpi_hist = {
#    'mem_key':      'MPI-ESM1-2-HR_historical', 
#}
#mpi_scen = {
#    'mem_key':      'MPI-ESM1-2-HR_ssp585', 
#}
#cmip_hist = {
#    'mem_oper':     'mean',
#    'mem_keys':     mem_keys_cmip6_hist,
#}
#cmip_scen = {
#    'mem_oper':     'mean',
#    'mem_keys':     mem_keys_cmip6_scen,
#}
#cmip_change = {
#    'mem_oper':     'mean',
#    'mem_keys':     mem_keys_cmip6_change,
#}
#cosmo_bias = {
#    'mem_oper':     'bias',
#    'mem_keys':     [ctrl, era],
#}
#cosmo_rel = {
#    'mem_oper':     'rel0.0001',
#    'mem_keys':     [ctrl, era],
#}
##bias_mpi = {
##    'mem_oper':     'bias',
##    'mem_keys':     [
##        {
##            'mem_key':      'MPI-ESM1-2-HR_historical', 
##            'time_periods': time_periods_cmip_hist,
##        },
##        {
##            'mem_key':      'ERA5', 
##            'time_periods': time_periods_default,
##        },
##    ],
##}
#cosmo_change = {
#    'mem_oper':     'diff',
#    'mem_keys':     [pgw, ctrl],
#    #'time_periods': time_periods_default,
#}
#cosmo_rdheight2_change = {
#    'mem_oper':     'diff',
#    'mem_keys':     [
#        {
#            'mem_key':      'COSMO_3.3_pgw_300hPa_rdheight2', 
#        },
#        {
#            'mem_key':      'COSMO_3.3_ctrl_rdheight2', 
#        },
#    ],
#}
#mpi_change = {
#    'mem_oper':     'diff',
#    'mem_keys':     [
#        {
#            'mem_key':      'MPI-ESM1-2-HR_ssp585', 
#            'time_periods': time_periods_cmip6_scen,
#        },
#        {
#            'mem_key':      'MPI-ESM1-2-HR_historical', 
#            'time_periods': time_periods_cmip6_hist,
#        },
#    ],
#}
#cmip_change = {
#    'mem_oper':     'diff',
#    'mem_keys':     [
#        {
#            'mem_oper':     'mean',
#            'mem_keys':     mem_keys_cmip6_scen,
#            'time_periods': time_periods_cmip6_scen,
#        },
#        {
#            'mem_oper':     'mean',
#            'mem_keys':     mem_keys_cmip6_hist,
#            'time_periods': time_periods_cmip6_hist,
#        },
#    ],
#}
#cmip_bias = {
#    'mem_oper':     'mean',
#    'mem_keys':     mem_keys_cmip6_bias,
#}
#cmip_rel = {
#    'mem_oper':     'rel0.0001',
#    'mem_keys':     mem_keys_cmip6_bias,
#}



run_cfgs = {
    #'test_pgw_clouds':  {
    #    'pan_cfgs':    [
    #        {
    #            'mem_cfgs':     [era],
    #            'title':        'ERA5 07-10 Jan-Dec', 
    #            'time_periods': time_periods_2006,
    #        },
    #        None,
    #        None,

    #        {
    #            'mem_cfgs':     ['COSMO_3.3_ctrl'],
    #            'title':        'CTRL Jan-Dec', 
    #            'time_periods': time_periods_2006,
    #        },
    #        {
    #            'mem_cfgs':     ['COSMO_3.3_pgw'],
    #            'title':        'PGW Jan-Dec', 
    #            'time_periods': time_periods_2006,
    #        },
    #        {
    #            'mem_cfgs':     [cosmo_change],
    #            'title':        'PGW$-$CTRL', 
    #            'var_type':     'CLDF_CLDF',
    #            'time_periods': time_periods_2006,
    #        },

    #        {
    #            'mem_cfgs':     ['COSMO_3.3_ctrl_rdheight2'],
    #            'title':        'CTRL RD Jan-Dec', 
    #            'time_periods': time_periods_2006,
    #        },
    #        {
    #            'mem_cfgs':     ['COSMO_3.3_pgw_300hPa_rdheight2'],
    #            'title':        'PGW RD Jan-Dec', 
    #            'time_periods': time_periods_2006,
    #        },
    #        {
    #            'mem_cfgs':     [cosmo_rdheight2_change],
    #            'title':        'PGW$-$CTRL', 
    #            'var_type':     'CLDF_CLDF',
    #            'time_periods': time_periods_2006,
    #        },
    #    ],
    #    'default_var_type': 'CLDF_CLDF_PP',
    #    'line_along':       'lat',
    #    'figsize':          (12, 14),
    #    'nrows':            4,
    #    'ncols':            3,
    #    'adjust_key':       '4x3_twinx',
    #    'plot_domain':      dom_SA_ana_merid_cs,
    #    'pan_cbar_pos':     'bottom',
    #    'pan_cbar_pad':     0.2,
    #    'kwargs_remove_axis_labels': {
    #        'remove_level': 0,
    #    },
    #},
    #'paper_clouds_afr':  {
    #    'pan_cfgs':    [
    #        #{
    #        #    'mem_cfgs':     ['COSMO_3.3_ctrl'],
    #        #    'title':        'CTRL Jan-Dec', 
    #        #},
    #        #{
    #        #    'mem_cfgs':     ['COSMO_3.3_ctrl'],
    #        #    'time_periods': time_periods_ana_DJF,
    #        #    'title':        'CTRL Dec-Feb', 
    #        #},
    #        #{
    #        #    'mem_cfgs':     ['COSMO_3.3_ctrl'],
    #        #    'time_periods': time_periods_ana_JJA,
    #        #    'title':        'CTRL June-Aug', 
    #        #},


    #        {
    #            'mem_cfgs':     [era],
    #            'title':        'ERA5 07-10 Jan-Dec', 
    #        },
    #        {
    #            'mem_cfgs':['ERA5'],
    #            'time_periods':time_periods_ana_DJF,
    #            'title':        'ERA5 07-10 Dec-Feb', 
    #        },
    #        {
    #            'mem_cfgs':['ERA5'],
    #            'time_periods': time_periods_ana_JJA,
    #            'title':        'ERA5 07-10 June-Aug', 
    #        },


    #        #{
    #        #    'mem_cfgs':     [era],
    #        #    'time_periods': time_periods_cmip6_hist,
    #        #    'title':        'ERA5 85-14 Jan-Dec', 
    #        #},
    #        #{
    #        #    'mem_cfgs':['ERA5'],
    #        #    'time_periods': time_periods_cmip6_hist_DJF,
    #        #    'title':        'ERA5 85-14 Dec-Feb', 
    #        #},
    #        #{
    #        #    'mem_cfgs':['ERA5'],
    #        #    'time_periods': time_periods_cmip6_hist_JJA,
    #        #    'title':        'ERA5 85-14 June-Aug', 
    #        #},


    #        #{
    #        #    'mem_cfgs':     [cmip_hist],
    #        #    'time_periods': time_periods_cmip6_hist,
    #        #    'title':        'CMIP6-EM Jan-Dec', 
    #        #},
    #        #{
    #        #    'mem_cfgs':     [cmip_hist],
    #        #    'time_periods': time_periods_cmip6_hist_DJF,
    #        #    'title':        'CMIP6-EM Dec-Feb', 
    #        #},
    #        #{
    #        #    'mem_cfgs':     [cmip_hist],
    #        #    'time_periods': time_periods_cmip6_hist_JJA,
    #        #    'title':        'CMIP6-EM June-Aug', 
    #        #},


    #        #{
    #        #    'mem_cfgs':     [mpi_hist],
    #        #    'time_periods': time_periods_cmip6_hist,
    #        #    'title':        'MPI-ESM Jan-Dec', 
    #        #},
    #        #{
    #        #    'mem_cfgs':     [mpi_hist],
    #        #    'time_periods': time_periods_cmip6_hist_DJF,
    #        #    'title':        'MPI-ESM Dec-Feb', 
    #        #},
    #        #{
    #        #    'mem_cfgs':     [mpi_hist],
    #        #    'time_periods': time_periods_cmip6_hist_JJA,
    #        #    'title':        'MPI-ESM June-Aug', 
    #        #},
    #    ],
    #    'default_var_type': 'CLDF_CLDF_PP',
    #    'line_along':       'lat',
    #    'figsize':          (12, 17),
    #    'nrows':            5,
    #    'ncols':            3,
    #    'adjust_key':       '5x3_twinx',
    #    'plot_domain':      dom_SA_ana_merid_cs_afr,
    #    'pan_cbar_pos':     'bottom',
    #    'pan_cbar_pad':     0.2,
    #    'kwargs_remove_axis_labels': {
    #        'remove_level': 0,
    #    },
    #},


    #'change_1':  {
    #    'pan_cfgs':    [
    #        {
    #            'mem_cfgs':     ['COSMO_3.3_ctrl'],
    #            'var_type':     'T_CLDF', 
    #            'title':        '{} CTRL'.format(nlv['T']['label']), 
    #        },
    #        {
    #            'mem_cfgs':     [cosmo_change],
    #            'var_type':     'T_CLDF', 
    #            'title':        '{} PGW$-$CTRL'.format(nlv['T']['label']), 
    #        },
    #        {
    #            'mem_cfgs':     ['COSMO_3.3_ctrl'],
    #            'var_type':     'RH_CLDF', 
    #            'title':        '{} CTRL'.format(nlv['RH']['label']), 
    #        },
    #        {
    #            'mem_cfgs':     [cosmo_change],
    #            'var_type':     'RH_CLDF', 
    #            'title':        '{} PGW$-$CTRL'.format(nlv['RH']['label']), 
    #        },

    #        {
    #            'mem_cfgs':     [cmip_hist],
    #            'time_periods': time_periods_cmip6_hist,
    #            'var_type':     'T_CLDF', 
    #            'title':        'CMIP6-EM HIST', 
    #        },
    #        {
    #            'mem_cfgs':     [cmip_change],
    #            'var_type':     'T_CLDF', 
    #            'title':        'CMIP6-EM SCEN$-$HIST', 
    #        },
    #        {
    #            'mem_cfgs':     [cmip_hist],
    #            'time_periods': time_periods_cmip6_hist,
    #            'var_type':     'RH_CLDF', 
    #            'title':        'CMIP6-EM HIST', 
    #        },
    #        {
    #            'mem_cfgs':     [cmip_change],
    #            'var_type':     'RH_CLDF', 
    #            'title':        'CMIP6-EM SCEN$-$HIST', 
    #        },

    #        {
    #            'mem_cfgs':     [mpi_hist],
    #            'time_periods': time_periods_cmip6_hist,
    #            'var_type':     'T_CLDF', 
    #            'title':        'MPI-ESM HIST', 
    #        },
    #        {
    #            'mem_cfgs':     [mpi_change],
    #            'var_type':     'T_CLDF', 
    #            'title':        'MPI-ESM SCEN$-$HIST', 
    #        },
    #        {
    #            'mem_cfgs':     [mpi_hist],
    #            'time_periods': time_periods_cmip6_hist,
    #            'var_type':     'RH_CLDF', 
    #            'title':        'MPI-ESM HIST', 
    #        },
    #        {
    #            'mem_cfgs':     [mpi_change],
    #            'var_type':     'RH_CLDF', 
    #            'title':        'MPI-ESM SCEN$-$HIST', 
    #        },

    #    ],
    #    'default_var_type': 'CLDF',
    #    'line_along':       'lat',
    #    'figsize':          (16, 7.5),
    #    'nrows':            3,
    #    'ncols':            4,
    #    'adjust_key':       '3x4',
    #    'plot_domain':      dom_SA_ana_merid_cs,
    #},



    #'paper_clouds':  {
    #    'pan_cfgs':    [
    #        {
    #            'mem_cfgs':     ['COSMO_3.3_ctrl'],
    #            'title':        'CTRL Jan-Dec', 
    #        },
    #        {
    #            'mem_cfgs':     ['COSMO_3.3_ctrl'],
    #            'time_periods': time_periods_ana_FMA,
    #            'title':        'CTRL Feb-Apr', 
    #        },
    #        {
    #            'mem_cfgs':     ['COSMO_3.3_ctrl'],
    #            'time_periods': time_periods_ana_JAS,
    #            'title':        'CTRL July-Sep', 
    #        },


    #        {
    #            'mem_cfgs':     [era],
    #            'title':        'ERA5 07-10 Jan-Dec', 
    #        },
    #        {
    #            'mem_cfgs':['ERA5'],
    #            'time_periods':time_periods_ana_FMA,
    #            'title':        'ERA5 07-10 Feb-Apr', 
    #        },
    #        {
    #            'mem_cfgs':['ERA5'],
    #            'time_periods':time_periods_ana_JAS,
    #            'title':        'ERA5 07-10 July-Sep', 
    #        },


    #        {
    #            'mem_cfgs':     [era],
    #            'time_periods': time_periods_cmip6_hist,
    #            'title':        'ERA5 85-14 Jan-Dec', 
    #        },
    #        {
    #            'mem_cfgs':['ERA5'],
    #            'time_periods': time_periods_cmip6_hist_FMA,
    #            'title':        'ERA5 85-14 Feb-Apr', 
    #        },
    #        {
    #            'mem_cfgs':['ERA5'],
    #            'time_periods': time_periods_cmip6_hist_JAS,
    #            'title':        'ERA5 85-14 July-Sep', 
    #        },


    #        {
    #            'mem_cfgs':     [cmip_hist],
    #            'time_periods': time_periods_cmip6_hist,
    #            'title':        'CMIP6-EM Jan-Dec', 
    #        },
    #        {
    #            'mem_cfgs':     [cmip_hist],
    #            'time_periods': time_periods_cmip6_hist_FMA,
    #            'title':        'CMIP6-EM Feb-Apr', 
    #        },
    #        {
    #            'mem_cfgs':     [cmip_hist],
    #            'time_periods': time_periods_cmip6_hist_JAS,
    #            'title':        'CMIP6-EM July-Sep', 
    #        },


    #        {
    #            'mem_cfgs':     [mpi_hist],
    #            'time_periods': time_periods_cmip6_hist,
    #            'title':        'MPI-ESM Jan-Dec', 
    #        },
    #        {
    #            'mem_cfgs':     [mpi_hist],
    #            'time_periods': time_periods_cmip6_hist_FMA,
    #            'title':        'MPI-ESM Feb-Apr', 
    #        },
    #        {
    #            'mem_cfgs':     [mpi_hist],
    #            'time_periods': time_periods_cmip6_hist_JAS,
    #            'title':        'MPI-ESM July-Sep', 
    #        },
    #    ],
    #    'default_var_type': 'CLDF_CLDF_PP',
    #    'line_along':       'lat',
    #    #'figsize':          (12, 14),
    #    #'nrows':            4,
    #    #'ncols':            3,
    #    #'adjust_key':       '4x3_twinx',
    #    'figsize':          (12, 17),
    #    'nrows':            5,
    #    'ncols':            3,
    #    'adjust_key':       '5x3_twinx',
    #    'plot_domain':      dom_SA_ana_merid_cs,
    #    'pan_cbar_pos':     'bottom',
    #    'pan_cbar_pad':     0.2,
    #    'kwargs_remove_axis_labels': {
    #        'remove_level': 0,
    #    },
    #},
    #'paper_clouds_afr':  {
    #    'pan_cfgs':    [
    #        {
    #            'mem_cfgs':     ['COSMO_3.3_ctrl'],
    #            'title':        'CTRL Jan-Dec', 
    #        },
    #        {
    #            'mem_cfgs':     ['COSMO_3.3_ctrl'],
    #            'time_periods': time_periods_ana_DJF,
    #            'title':        'CTRL Dec-Feb', 
    #        },
    #        {
    #            'mem_cfgs':     ['COSMO_3.3_ctrl'],
    #            'time_periods': time_periods_ana_JJA,
    #            'title':        'CTRL June-Aug', 
    #        },


    #        {
    #            'mem_cfgs':     [era],
    #            'title':        'ERA5 07-10 Jan-Dec', 
    #        },
    #        {
    #            'mem_cfgs':['ERA5'],
    #            'time_periods':time_periods_ana_DJF,
    #            'title':        'ERA5 07-10 Dec-Feb', 
    #        },
    #        {
    #            'mem_cfgs':['ERA5'],
    #            'time_periods': time_periods_ana_JJA,
    #            'title':        'ERA5 07-10 June-Aug', 
    #        },


    #        {
    #            'mem_cfgs':     [era],
    #            'time_periods': time_periods_cmip6_hist,
    #            'title':        'ERA5 85-14 Jan-Dec', 
    #        },
    #        {
    #            'mem_cfgs':['ERA5'],
    #            'time_periods': time_periods_cmip6_hist_DJF,
    #            'title':        'ERA5 85-14 Dec-Feb', 
    #        },
    #        {
    #            'mem_cfgs':['ERA5'],
    #            'time_periods': time_periods_cmip6_hist_JJA,
    #            'title':        'ERA5 85-14 June-Aug', 
    #        },


    #        {
    #            'mem_cfgs':     [cmip_hist],
    #            'time_periods': time_periods_cmip6_hist,
    #            'title':        'CMIP6-EM Jan-Dec', 
    #        },
    #        {
    #            'mem_cfgs':     [cmip_hist],
    #            'time_periods': time_periods_cmip6_hist_DJF,
    #            'title':        'CMIP6-EM Dec-Feb', 
    #        },
    #        {
    #            'mem_cfgs':     [cmip_hist],
    #            'time_periods': time_periods_cmip6_hist_JJA,
    #            'title':        'CMIP6-EM June-Aug', 
    #        },


    #        {
    #            'mem_cfgs':     [mpi_hist],
    #            'time_periods': time_periods_cmip6_hist,
    #            'title':        'MPI-ESM Jan-Dec', 
    #        },
    #        {
    #            'mem_cfgs':     [mpi_hist],
    #            'time_periods': time_periods_cmip6_hist_DJF,
    #            'title':        'MPI-ESM Dec-Feb', 
    #        },
    #        {
    #            'mem_cfgs':     [mpi_hist],
    #            'time_periods': time_periods_cmip6_hist_JJA,
    #            'title':        'MPI-ESM June-Aug', 
    #        },
    #    ],
    #    'default_var_type': 'CLDF_CLDF_PP',
    #    'line_along':       'lat',
    #    'figsize':          (12, 17),
    #    'nrows':            5,
    #    'ncols':            3,
    #    'adjust_key':       '5x3_twinx',
    #    'plot_domain':      dom_SA_ana_merid_cs_afr,
    #    'pan_cbar_pos':     'bottom',
    #    'pan_cbar_pad':     0.2,
    #    'kwargs_remove_axis_labels': {
    #        'remove_level': 0,
    #    },
    #},
    #'eval_2':  {
    #    'pan_cfgs':    [
    #        {
    #            'mem_cfgs':     ['COSMO_3.3_ctrl'],
    #            'var_type':     'V_CLDF', 
    #            'title':        '{} CTRL'.format(nlv['V']['label']),
    #        },
    #        {
    #            'mem_cfgs':     ['COSMO_3.3_ctrl'],
    #            'var_type':     'W_CLDF', 
    #            'title':        '{} CTRL'.format(nlv['W']['label']),
    #        },
    #        {
    #            'mem_cfgs':     ['COSMO_3.3_ctrl'],
    #            'var_type':     'T_CLDF', 
    #            'title':        '{} CTRL'.format(nlv['T']['label']),
    #        },
    #        {
    #            'mem_cfgs':     ['COSMO_3.3_ctrl'],
    #            'var_type':     'RH_CLDF', 
    #            'title':        '{} CTRL'.format(nlv['RH']['label']),
    #        },


    #        #{
    #        #    'mem_cfgs':     ['ERA5'],
    #        #    'var_type':     'V_CLDF', 
    #        #    'title':        '{} ERA5'.format(nlv['V']['label']),
    #        #},
    #        #{
    #        #    'mem_cfgs':     ['ERA5'],
    #        #    'var_type':     'W_CLDF', 
    #        #    'title':        '{} ERA5'.format(nlv['W']['label']),
    #        #},
    #        #{
    #        #    'mem_cfgs':     ['ERA5'],
    #        #    'var_type':     'T_CLDF', 
    #        #    'title':        '{} ERA5'.format(nlv['T']['label']),
    #        #},
    #        #{
    #        #    'mem_cfgs':     ['ERA5'],
    #        #    'var_type':     'RH_CLDF', 
    #        #    'title':        '{} ERA5'.format(nlv['RH']['label']),
    #        #},


    #        #{
    #        #    'mem_cfgs':     [cmip_hist],
    #        #    'time_periods': time_periods_cmip6_hist,
    #        #    'var_type':     'V_CLDF', 
    #        #    'title':        '{} CMIP6-EM'.format(nlv['V']['label']),
    #        #},
    #        #{
    #        #    'mem_cfgs':     [cmip_hist],
    #        #    'time_periods': time_periods_cmip6_hist,
    #        #    'var_type':     'W_CLDF', 
    #        #    'title':        '{} CMIP6-EM'.format(nlv['W']['label']),
    #        #},
    #        #{
    #        #    'mem_cfgs':     [cmip_hist],
    #        #    'time_periods': time_periods_cmip6_hist,
    #        #    'var_type':     'T_CLDF', 
    #        #    'title':        '{} CMIP6-EM'.format(nlv['T']['label']),
    #        #},
    #        #{
    #        #    'mem_cfgs':     [cmip_hist],
    #        #    'time_periods': time_periods_cmip6_hist,
    #        #    'var_type':     'RH_CLDF', 
    #        #    'title':        '{} CMIP6-EM'.format(nlv['RH']['label']),
    #        #},


    #        #{
    #        #    'mem_cfgs':     [cosmo_bias],
    #        #    'var_type':     'V_CLDF', 
    #        #    'title':        '{} CTRL - ERA5'.format(nlv['V']['label']),
    #        #},
    #        #{
    #        #    'mem_cfgs':     [cosmo_bias],
    #        #    'var_type':     'W_CLDF', 
    #        #    'title':        '{} CTRL - ERA5'.format(nlv['W']['label']),
    #        #},
    #        #{
    #        #    'mem_cfgs':     [cosmo_bias],
    #        #    'var_type':     'T_CLDF', 
    #        #    'title':        '{} CTRL - ERA5'.format(nlv['T']['label']),
    #        #},
    #        #{
    #        #    'mem_cfgs':     [cosmo_bias],
    #        #    'var_type':     'RH_CLDF', 
    #        #    'title':        '{} CTRL - ERA5'.format(nlv['RH']['label']),
    #        #},


    #        #{
    #        #    'mem_cfgs':     [cmip_bias],
    #        #    'var_type':     'V_CLDF', 
    #        #    'title':        '{} CMIP6-EM - ERA5'.format(nlv['V']['label']),
    #        #},
    #        #{
    #        #    'mem_cfgs':     [cmip_bias],
    #        #    'var_type':     'W_CLDF', 
    #        #    'title':        '{} CMIP6-EM - ERA5'.format(nlv['W']['label']),
    #        #},
    #        #{
    #        #    'mem_cfgs':     [cmip_bias],
    #        #    'var_type':     'T_CLDF', 
    #        #    'title':        '{} CMIP6-EM - ERA5'.format(nlv['T']['label']),
    #        #},
    #        #{
    #        #    'mem_cfgs':     [cmip_bias],
    #        #    'var_type':     'RH_CLDF', 
    #        #    'title':        '{} CMIP6-EM - ERA5'.format(nlv['RH']['label']),
    #        #},


    #    ],
    #    'line_along':       'lat',
    #    'figsize':          (16, 13),
    #    'nrows':            5,
    #    'ncols':            4,
    #    'adjust_key':       '5x4',
    #    'plot_domain':      dom_SA_ana_merid_cs,
    #},
    #'change_clouds':  {
    #    'pan_cfgs':    [
    #        {
    #            'mem_cfgs':     ['COSMO_3.3_ctrl'],
    #            'title':        'CTRL', 
    #        },
    #        {
    #            'mem_cfgs':     ['COSMO_3.3_pgw'],
    #            'title':        'PGW', 
    #        },
    #        {
    #            'mem_cfgs':     [cosmo_change],
    #            'title':        'PGW$-$CTRL', 
    #            'var_type':     'CLDF_CLDF',
    #        },

    #        {
    #            'mem_cfgs':     [cmip_hist],
    #            'time_periods': time_periods_cmip6_hist,
    #            'title':        'CMIP6-EM HIST', 
    #        },
    #        {
    #            'mem_cfgs':     [cmip_scen],
    #            'time_periods': time_periods_cmip6_scen,
    #            'title':        'CMIP6-EM SCEN', 
    #        },
    #        {
    #            'mem_cfgs':     [cmip_change],
    #            'title':        'CMIP6-EM SCEN$-$HIST', 
    #            'var_type':     'CLDF_CLDF',
    #        },

    #        {
    #            'mem_cfgs':     [mpi_hist],
    #            'time_periods': time_periods_cmip6_hist,
    #            'title':        'MPI-ESM HIST', 
    #        },
    #        {
    #            'mem_cfgs':     [mpi_scen],
    #            'time_periods': time_periods_cmip6_scen,
    #            'title':        'MPI-ESM SCEN', 
    #        },
    #        {
    #            'mem_cfgs':     [mpi_change],
    #            'title':        'MPI-ESM SCEN$-$HIST', 
    #            'var_type':     'CLDF_CLDF',
    #        },

    #    ],
    #    'default_var_type': 'CLDF_CLDF_PP',
    #    'line_along':       'lat',
    #    'figsize':          (12, 11),
    #    'nrows':            3,
    #    'ncols':            3,
    #    'adjust_key':       '3x3_twinx',
    #    'plot_domain':      dom_SA_ana_merid_cs,
    #    'pan_cbar_pos':     'bottom',
    #    'pan_cbar_pad':     0.2,
    #    'kwargs_remove_axis_labels': {
    #        'remove_level': 0,
    #    },
    #},

    #'subtr_cooling':  {
    #    'pan_cfgs':    [
    #        {
    #            'mem_cfgs':     ['ERA5'],
    #            'title':        'ERA5', 
    #        },
    #        None,
    #        None,
    #        {
    #            'mem_cfgs':     [cmip_hist],
    #            'time_periods': time_periods_cmip6_hist,
    #            'title':        'CMIP6-EM HIST', 
    #        },
    #        {
    #            'mem_cfgs':     [cmip_scen],
    #            'time_periods': time_periods_cmip6_scen,
    #            'title':        'CMIP6-EM SCEN', 
    #        },
    #        {
    #            'mem_cfgs':     [cmip_change],
    #            'title':        'CMIP6-EM SCEN$-$HIST', 
    #        },

    #        {
    #            'mem_cfgs':     [mpi_hist],
    #            'time_periods': time_periods_cmip6_hist,
    #            'title':        'MPI-ESM HIST', 
    #        },
    #        {
    #            'mem_cfgs':     [mpi_scen],
    #            'time_periods': time_periods_cmip6_scen,
    #            'title':        'MPI-ESM SCEN', 
    #        },
    #        {
    #            'mem_cfgs':     [mpi_change],
    #            'title':        'MPI-ESM SCEN$-$HIST', 
    #        },

    #        {
    #            'mem_cfgs':     ['COSMO_3.3_ctrl'],
    #            'title':        'CTRL', 
    #        },
    #        {
    #            'mem_cfgs':     ['COSMO_3.3_pgw'],
    #            'title':        'PGW', 
    #        },
    #        {
    #            'mem_cfgs':     [cosmo_change],
    #            'title':        'PGW$-$CTRL', 
    #        },


    #        {
    #            'mem_cfgs':     ['COSMO_3.3_ctrl'],
    #            'title':        'CTRL', 
    #            'var_type':     'NCOLIPOTTDIV_CLDF',
    #        },
    #        {
    #            'mem_cfgs':     ['COSMO_3.3_pgw'],
    #            'title':        'PGW', 
    #            'var_type':     'NCOLIPOTTDIV_CLDF',
    #        },
    #        {
    #            'mem_cfgs':     [cosmo_change],
    #            'title':        'PGW$-$CTRL', 
    #            'var_type':     'NCOLIPOTTDIV_CLDF',
    #        },
    #    ],
    #    'default_var_type': 'POTTDIV_CLDF',
    #    'line_along':       'lat',
    #    #'figsize':          (12, 10),
    #    #'nrows':            4,
    #    #'ncols':            3,
    #    #'adjust_key':       '4x3',
    #    'figsize':          (12, 12.5),
    #    'nrows':            5,
    #    'ncols':            3,
    #    'adjust_key':       '5x3',
    #    'plot_domain':      dom_SA_ana_merid_cs,
    #    'kwargs_remove_axis_labels': {
    #        'remove_level': 2,
    #    },
    #},

    #'subtr_subs':  {
    #    'pan_cfgs':    [
    #        {
    #            'mem_cfgs':     [cmip_hist],
    #            'time_periods': time_periods_cmip6_hist,
    #            'title':        'CMIP6-EM HIST', 
    #        },
    #        {
    #            'mem_cfgs':     [cmip_scen],
    #            'time_periods': time_periods_cmip6_scen,
    #            'title':        'CMIP6-EM SCEN', 
    #        },
    #        {
    #            'mem_cfgs':     [cmip_change],
    #            'title':        'CMIP6-EM SCEN$-$HIST', 
    #        },

    #        {
    #            'mem_cfgs':     [mpi_hist],
    #            'time_periods': time_periods_cmip6_hist,
    #            'title':        'MPI-ESM HIST', 
    #        },
    #        {
    #            'mem_cfgs':     [mpi_scen],
    #            'time_periods': time_periods_cmip6_scen,
    #            'title':        'MPI-ESM SCEN', 
    #        },
    #        {
    #            'mem_cfgs':     [mpi_change],
    #            'title':        'MPI-ESM SCEN$-$HIST', 
    #        },

    #        {
    #            'mem_cfgs':     ['COSMO_3.3_ctrl'],
    #            'title':        'CTRL', 
    #        },
    #        {
    #            'mem_cfgs':     ['COSMO_3.3_pgw'],
    #            'title':        'PGW', 
    #        },
    #        {
    #            'mem_cfgs':     [cosmo_change],
    #            'title':        'PGW$-$CTRL', 
    #        },
    #    ],
    #    'default_var_type': 'W_CLDF',
    #    'line_along':       'lat',
    #    'figsize':          (12, 8),
    #    'nrows':            3,
    #    'ncols':            3,
    #    'adjust_key':       '3x3',
    #    'plot_domain':      dom_SA_ana_merid_cs,
    #    'kwargs_remove_axis_labels': {
    #        'remove_level': 2,
    #    },
    #},


    'change_2':  {
        'fig': {
            'figsize':              (10, 15),
            'nrows':                6,
            'ncols':                3,
            'args_subplots_adjust': args_subplots_adjust['{}x{}'.format(6,3)],
            'grid_spec':            dict(
                                        wspaces=[0.08,0.08],
                                        hspaces=[0.2,0.2,1.2,0.2,0.2],
                                    ),
            'kwargs_remove_axis_labels': {
                'remove_level':     2,
                'xexcept':          [(2,0),(2,1),(2,2)],
            },
            'label_cfgs': [
                {'xrel':0.02,'yrel':0.97,'text':nlv['VFLX']['label'],'fontsize':24},
                {'xrel':0.02,'yrel':0.49,'text':nlv['WFLX']['label'],'fontsize':24},
            ],
        },
        'glob_pan_cfg':   {
            'ana_number':       4,
            'agg_level':        TP.ALL_TIME,
            'line_at':          None,
            'alt_lims':         (0,18000),
            'line_along':       'lat',
            'plot_domain':      dom_SA_ana_merid_cs,
            'norm_inv':         0,
            'time_periods':     time_periods_ana,
            'i_plot_cbar':      False,
        },
        'pan_cfgs':    [
            {
                'mem_cfgs':         ['COSMO_3.3_ctrl'],
                'var_type':         'VFLX_CLDF', 
                'title':            'CTRL', 
            },
            {
                'mem_cfgs':         ['COSMO_3.3_pgw'],
                'var_type':         'VFLX_CLDF', 
                'title':            'PGW', 
            },
            {
                'mem_cfgs':         [cosmo_change],
                'var_type':         'VFLX_CLDF', 
                'title':            'PGW$-$CTRL', 
            },

            {
                'mem_cfgs':         [cmip6_hist],
                'time_periods':     time_periods_cmip6_hist,
                'var_type':         'VFLX_CLDF', 
                'title':            'CMIP6-EM HIST', 
            },
            {
                'mem_cfgs':         [cmip6_scen],
                'time_periods':     time_periods_cmip6_scen,
                'var_type':         'VFLX_CLDF', 
                'title':            'CMIP6-EM SCEN', 
            },
            {
                'mem_cfgs':         [cmip6_change],
                'var_type':         'VFLX_CLDF', 
                'title':            'CMIP6-EM SCEN$-$HIST', 
            },

            {
                'mem_cfgs':         [mpi_hist],
                'time_periods':     time_periods_cmip6_hist,
                'var_type':         'VFLX_CLDF', 
                'title':            'MPI-ESM HIST', 
                'i_plot_cbar':      1,
            },
            {
                'mem_cfgs':         [mpi_scen],
                'time_periods':     time_periods_cmip6_scen,
                'var_type':         'VFLX_CLDF', 
                'title':            'MPI-ESM SCEN', 
                'i_plot_cbar':      1,
            },
            {
                'mem_cfgs':         [mpi_change],
                'var_type':         'VFLX_CLDF', 
                'title':            'MPI-ESM SCEN$-$HIST', 
                'i_plot_cbar':      1,
            },




            {
                'mem_cfgs':         ['COSMO_3.3_ctrl'],
                'var_type':         'WFLX_CLDF', 
                'title':            'CTRL', 
            },
            {
                'mem_cfgs':         ['COSMO_3.3_pgw'],
                'var_type':         'WFLX_CLDF', 
                'title':            'PGW', 
            },
            {
                'mem_cfgs':         [cosmo_change],
                'var_type':         'WFLX_CLDF', 
                'title':            'PGW$-$CTRL', 
            },

            {
                'mem_cfgs':         [cmip6_hist],
                'time_periods':     time_periods_cmip6_hist,
                'var_type':         'WFLX_CLDF', 
                'title':            'CMIP6-EM HIST', 
            },
            {
                'mem_cfgs':         [cmip6_scen],
                'time_periods':     time_periods_cmip6_scen,
                'var_type':         'WFLX_CLDF', 
                'title':            'CMIP6-EM SCEN', 
            },
            {
                'mem_cfgs':         [cmip6_change],
                'var_type':         'WFLX_CLDF', 
                'title':            'CMIP6-EM SCEN$-$HIST', 
            },

            {
                'mem_cfgs':         [mpi_hist],
                'time_periods':     time_periods_cmip6_hist,
                'var_type':         'WFLX_CLDF', 
                'title':            'MPI-ESM HIST', 
                'i_plot_cbar':      1,
            },
            {
                'mem_cfgs':         [mpi_scen],
                'time_periods':     time_periods_cmip6_scen,
                'var_type':         'WFLX_CLDF', 
                'title':            'MPI-ESM SCEN', 
                'i_plot_cbar':      1,
            },
            {
                'mem_cfgs':         [mpi_change],
                'var_type':         'WFLX_CLDF', 
                'title':            'MPI-ESM SCEN$-$HIST', 
                'i_plot_cbar':      1,
            },

        ],
    },



    'paper_clouds':  {
        'fig': {
            'figsize':              (10, 12),
            'nrows':                5,
            'ncols':                3,
            'args_subplots_adjust': args_subplots_adjust['{}x{}'.format(5,3)],
            'grid_spec':            dict(
                                        wspaces=[0.11,0.11],
                                        hspaces=[0.2,0.2,0.2,0.2,0.2],
                                    ),
            'kwargs_remove_axis_labels': {
                'remove_level':     2,
                #'xexcept':          [(2,0),(2,1),(2,2)],
            },
            'label_cfgs': [
                {'xrel':0.20,'yrel':0.97,   'text':'Jan-Dec'},
                {'xrel':0.47,'yrel':0.97,   'text':'Feb-Apr'},
                {'xrel':0.74,'yrel':0.97,   'text':'July-Sep'},
                {'xrel':0.01,'yrel':0.855,  'text':'CTRL',         'rotation':90},
                {'xrel':0.01,'yrel':0.65,   'text':'ERA5 07-10',   'rotation':90},
                {'xrel':0.01,'yrel':0.47,   'text':'ERA5 85-15',   'rotation':90},
                {'xrel':0.01,'yrel':0.305,  'text':'CMIP6-EM',     'rotation':90},
                {'xrel':0.01,'yrel':0.14,   'text':'MPI-ESM',      'rotation':90},
            ],
        },
        'glob_pan_cfg':   {
            'ana_number':       4,
            'agg_level':        TP.ALL_TIME,
            'line_at':          None,
            'alt_lims':         (0,18000),
            'line_along':       'lat',
            'plot_domain':      dom_SA_ana_merid_cs,
            'norm_inv':         0,
            'time_periods':     time_periods_ana,
            'i_plot_cbar':      False,
            'var_type':         'CLDF_CLDF_PP', 
            'title':            '', 
        },
        'pan_cfgs':    [
            {
                'mem_cfgs':         ['COSMO_3.3_ctrl'],
            },
            {
                'mem_cfgs':         ['COSMO_3.3_ctrl'],
                'time_periods':     time_periods_ana_FMA,
            },
            {
                'mem_cfgs':         ['COSMO_3.3_ctrl'],
                'time_periods':     time_periods_ana_JAS,
            },

            {
                'mem_cfgs':         [era,'GPM_IMERG'],
            },
            {
                'mem_cfgs':         [era,'GPM_IMERG'],
                'time_periods':     time_periods_ana_FMA,
            },
            {
                'mem_cfgs':         [era,'GPM_IMERG'],
                'time_periods':     time_periods_ana_JAS,
            },

            {
                'mem_cfgs':         [era],
                'time_periods':     time_periods_cmip6_hist,
            },
            {
                'mem_cfgs':         [era],
                'time_periods':     time_periods_cmip6_hist_FMA,
            },
            {
                'mem_cfgs':         [era],
                'time_periods':     time_periods_cmip6_hist_JAS,
            },

            {
                'mem_cfgs':         [cmip6_hist],
                'time_periods':     time_periods_cmip6_hist,
            },
            {
                'mem_cfgs':         [cmip6_hist],
                'time_periods':     time_periods_cmip6_hist_FMA,
            },
            {
                'mem_cfgs':         [cmip6_hist],
                'time_periods':     time_periods_cmip6_hist_JAS,
            },

            {
                'mem_cfgs':         [mpi_hist],
                'time_periods':     time_periods_cmip6_hist,
                'i_plot_cbar':      1,
            },
            {
                'mem_cfgs':         [mpi_hist],
                'time_periods':     time_periods_cmip6_hist_FMA,
                'i_plot_cbar':      1,
            },
            {
                'mem_cfgs':         [mpi_hist],
                'time_periods':     time_periods_cmip6_hist_JAS,
                'i_plot_cbar':      1,
            },
        ],
    },

}

use_cfg = 'paper_clouds'
#use_cfg = 'paper_clouds_afr'
#use_cfg = 'eval_2'

#use_cfg = 'change_clouds'
#use_cfg = 'change_1'
#use_cfg = 'change_2'

#use_cfg = 'subtr_cooling'
#use_cfg = 'subtr_subs'

#use_cfg = 'test_pgw_clouds'

i_recompute = 1

run_cfg = run_cfgs[use_cfg]

name_dict = {
    'cfg':use_cfg,
    'norm':run_cfg['glob_pan_cfg']['norm_inv'],
    #'FMA':'',
    #'JAS':'',
    #'sep':'',
    #'nov':'',
    #'10':'',
}

nrows = run_cfg['fig']['nrows']
ncols = run_cfg['fig']['ncols']

cfg = {
    'sub_dir':              'alcs_paper',
    'name_dict':            name_dict,
    'fig':                  run_cfg['fig'],
    #'subplots_adjust_spatial':
    #                        '1x1', # dummy
    #'args_subplots_adjust': args_subplots_adjust[run_cfg['fig']['adjust_key']],
    'kwargs_pan_labels' : {
        'shift_right':  -0.18,
        'shift_up':     0.06,
    },

    'panels':
    {
    }
}


### global optional user-specified arguments
for attr in [
    'kwargs_remove_axis_labels',
    'kwargs_pan_labels',
    'grid_spec',
    ]:
    if attr in run_cfg:
        cfg[attr] = run_cfg[attr]

for pan_ind,pan_cfg in enumerate(run_cfg['pan_cfgs']):
    #print(mem_cfg)
    col_ind = pan_ind % ncols
    row_ind = int(pan_ind/ncols)
    pan_key = '{},{}'.format(row_ind, col_ind)

    if pan_cfg is not None:
        use_pan_cfg = copy.deepcopy(run_cfg['glob_pan_cfg'])
        for key,val in pan_cfg.items():
            use_pan_cfg[key] = val

        if i_recompute == 0:
            use_pan_cfg['i_recompute'] = 0
        else:
            if 'i_recompute' not in use_pan_cfg:
                use_pan_cfg['i_recompute'] = 0

        cfg['panels'][pan_key] = use_pan_cfg


#print(cfg['pans']['0,0'])
#quit()
