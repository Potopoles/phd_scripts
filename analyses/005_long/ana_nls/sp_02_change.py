#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    analysis namelist
author			Christoph Heim
"""
###############################################################################
from datetime import datetime, timedelta
from package.time_processing import Time_Processing as TP
from base.nl_domains import *
from base.nl_time_periods import *
from package.nl_models import models_cmip6, models_cmip6_cldf
from nl_plot_org_ana import nlp
###############################################################################


plot_domain = dom_SA_ana_sea
#plot_domain = dom_SA_ana_land

#agg_level = TP.ANNUAL_CYCLE
agg_level = TP.ALL_TIME

if agg_level == TP.ALL_TIME:
    serial_time_plt_sels = [None]
elif agg_level == TP.ANNUAL_CYCLE:
    serial_time_plt_sels = []
    for month in range(1,13,1):
        serial_time_plt_sels.append({'month':month})
elif agg_level == TP.DIURNAL_CYCLE:
    serial_time_plt_sels = []
    for hour in range(0,23,3):
        serial_time_plt_sels.append({'hour':hour})
else:
    raise NotImplementedError()

#ctrl_12 = 'COSMO_12_ctrl'
#pgw_12 = 'COSMO_12_pgw'
cmip6 = 'cmip6'
ctrl_3 = 'COSMO_3.3_ctrl'
pgw_3 = 'COSMO_3.3_pgw'


i_recompute = {
    'ctrl_3_TQC':               0,
    'ctrl_3_TQI':               0,
    'ctrl_3_CLCW':              0,
    'ctrl_3_CLCI':              0,
    'ctrl_3_CLCL':              1,
    'ctrl_3_CLCM':              0,
    'ctrl_3_CLCH':              1,
    'ctrl_3_CLCT':              0,

    'pgw_3_TQC':                0,
    'pgw_3_TQI':                0,
    'pgw_3_CLCW':               0,
    'pgw_3_CLCI':               0,
    'pgw_3_CLCL':               1,
    'pgw_3_CLCM':               0,
    'pgw_3_CLCH':               1,
    'pgw_3_CLCT':               0,

    'ctrl_pgw_3_CRESWNDTOA':    0,
    'ctrl_pgw_3_CRELWDTOA':     0,
    'ctrl_pgw_3_CRERADNDTOA':   0,

    'MPI':                      0,
    'CMIP6':                    0,


}


models_cmip6 = models_cmip6_cldf
mem_keys_cmip6_hist = ['{}_historical'.format(model) for model in models_cmip6]
mem_keys_cmip6_ssp585 = ['{}_ssp585'.format(model) for model in models_cmip6]
mem_keys_cmip6_change = [{
    'mem_oper':'diff',
    'mem_keys':[
        {
            'mem_key':      '{}_ssp585'.format(model), 
            'time_periods': time_periods_cmip_ssp585,
        },
        {
            'mem_key':      '{}_historical'.format(model), 
            'time_periods': time_periods_cmip_historical,
        },
    ]} for model in models_cmip6
]
cmip_hist = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_hist,
    'time_periods': time_periods_cmip_historical,
    'label':        'CMIP6 HIST',
}
cmip_scen = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_ssp585,
    'time_periods': time_periods_cmip_ssp585,
    'label':        'CMIP6 SCEN',
}
cmip_change = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_change,
    'label':        'CMIP6 SCEN$-$HIST',
}

name_dict = {
    plot_domain['key']:'combined_vars',
    'time':agg_level,
    #'var_type':'TQX',
    'var_type':'CLC',
}

#nrows = 2
nrows = 2
ncols = 5

cfg = {
    'serial_time_plt_sels': serial_time_plt_sels,
    'sub_dir':              'sp_change',
    'name_dict':            name_dict,
    'figsize':              (nlp['figsize_spatial']['{}x{}'.format(
                                    nrows,ncols).format(nrows,ncols)][0],
                             nlp['figsize_spatial']['{}x{}'.format(
                                    nrows,ncols).format(nrows,ncols)][1]),
    'nrows':                nrows,
    'ncols':                ncols,
    'subplots_adjust_spatial':      
                            '{}x{}'.format(nrows,ncols),
    'i_remove_axis_labels': 1,
    'kwargs_remove_axis_labels': {
        'remove_level': 1,
    },
    #'args_subplots_adjust':  {
    #    ### only for nrows = 1
    #    #'wspace':0.25,
    #                        },
    'all_panels':
        {
            'ana_number':   1,
            'agg_level':    agg_level,
            'plot_domain':  plot_domain,
            'plot_ax_cbars':{
                                'abs':  1,
                                'diff': 1,
                            },
            'i_recompute':  0,
            'time_periods': time_periods_ana,
            #'ANA_NATIVE_domain':
            #                ANA_NATIVE_domain,
        },
    'panels':
    {
        '0,0':
        {
            'var_names':    ['CLCL'],
            'i_recompute':  i_recompute['ctrl_3_CLCL'],
            'mem_cfgs':     [ctrl_3],
        },
        '0,1':
        {
            'var_names':    ['CLCL'],
            'i_recompute':  i_recompute['pgw_3_CLCL'],
            'mem_cfgs':     [pgw_3],
            #'i_recompute':  0,
        },
        '0,2':
        {
            'var_names':    ['CLCL'],
            'i_recompute':  0,
            'mem_cfgs':     [
                {
                    'mem_oper': 'diff',
                    'mem_keys': [pgw_3, ctrl_3],
                },
            ],
        },

        #'0,0':
        #{
        #    'var_names':    ['CLCW'],
        #    'i_recompute':  i_recompute['ctrl_3_CLCW'],
        #    'mem_cfgs':     [ctrl_3],
        #},
        #'0,1':
        #{
        #    'var_names':    ['CLCW'],
        #    'i_recompute':  i_recompute['pgw_3_CLCW'],
        #    'mem_cfgs':     [pgw_3],
        #},
        #'0,2':
        #{
        #    'var_names':    ['CLCW'],
        #    'i_recompute':  0,
        #    'mem_cfgs':     [
        #        {
        #            'mem_oper': 'diff',
        #            'mem_keys': [pgw_3, ctrl_3],
        #        },
        #    ],
        #},

        #'0,0':
        #{
        #    'var_names':    ['TQC'],
        #    'i_recompute':  i_recompute['ctrl_3_TQC'],
        #    'mem_cfgs':     [ctrl_3],
        #},
        #'0,1':
        #{
        #    'var_names':    ['TQC'],
        #    'i_recompute':  i_recompute['pgw_3_TQC'],
        #    'mem_cfgs':     [pgw_3],
        #},
        #'0,2':
        #{
        #    'var_names':    ['TQC'],
        #    'i_recompute':  0,
        #    'mem_cfgs':     [
        #        {
        #            'mem_oper': 'diff',
        #            'mem_keys': [pgw_3, ctrl_3],
        #        },
        #    ],
        #},


        '0,3':
        {
            'var_names':    ['CRESWNDTOA'],
            'i_recompute':  i_recompute['ctrl_pgw_3_CRESWNDTOA'],
            'mem_cfgs':     [
                {
                    #'mem_key': pgw_3,
                    'mem_oper': 'diff',
                    'mem_keys': [pgw_3, ctrl_3],
                },
            ],
        },
        #'0,4':
        #{
        #    'var_names':    ['CRESWNDTOA'],
        #    'i_recompute':  i_recompute['MPI'],
        #    'mem_cfgs':     [
        #        {
        #            'mem_oper': 'diff',
        #            'mem_keys': [
        #                {
        #                    'time_periods': time_periods_cmip_ssp585,
        #                    'mem_key': 'MPI-ESM1-2-HR_ssp585',
        #                },
        #                {
        #                    'time_periods': time_periods_cmip_historical,
        #                    'mem_key': 'MPI-ESM1-2-HR_historical',
        #                },
        #            ],
        #            'label':    'MPI-ESM1-2-HR $\Delta$',
        #        },
        #    ],
        #},
        '0,4':
        {
            'var_names':    ['CRESWNDTOA'],
            'i_recompute':  i_recompute['CMIP6'],
            'mem_cfgs':     [cmip_change],
            #'label':        'CMIP6 SCEN$-$HIST',
        },




        #'1,0':
        #{
        #    'var_names':    ['CLCM'],
        #    'i_recompute':  i_recompute['ctrl_3_CLCM'],
        #    'mem_cfgs':     [ctrl_3],
        #},
        #'1,1':
        #{
        #    'var_names':    ['CLCM'],
        #    'i_recompute':  i_recompute['pgw_3_CLCM'],
        #    'mem_cfgs':     [pgw_3],
        #},
        #'1,2':
        #{
        #    'var_names':    ['CLCM'],
        #    'i_recompute':  0,
        #    'mem_cfgs':     [
        #        {
        #            'mem_oper': 'diff',
        #            'mem_keys': [pgw_3, ctrl_3],
        #        },
        #    ],
        #},

        #'1,0':
        #{
        #    'var_names':    ['TQI'],
        #    'i_recompute':  i_recompute['ctrl_3_TQI'],
        #    'mem_cfgs':     [ctrl_3],
        #},
        #'1,1':
        #{
        #    'var_names':    ['TQI'],
        #    'i_recompute':  i_recompute['pgw_3_TQI'],
        #    'mem_cfgs':     [pgw_3],
        #},
        #'1,2':
        #{
        #    'var_names':    ['TQI'],
        #    'i_recompute':  0,
        #    'mem_cfgs':     [
        #        {
        #            'mem_oper': 'diff',
        #            'mem_keys': [pgw_3, ctrl_3],
        #        },
        #    ],
        #},

        #'1,3':
        #{
        #    'var_names':    ['CRESWNDTOA'],
        #    'i_recompute':  i_recompute['ctrl_pgw_3_CRESWNDTOA'],
        #    'mem_cfgs':     [
        #        {
        #            'mem_oper': 'diff',
        #            'mem_keys': [pgw_3, ctrl_3],
        #        },
        #    ],
        #},



        '1,0':
        {
            'var_names':    ['CLCH'],
            'i_recompute':  i_recompute['ctrl_3_CLCH'],
            'mem_cfgs':     [ctrl_3],
        },
        '1,1':
        {
            'var_names':    ['CLCH'],
            'i_recompute':  i_recompute['pgw_3_CLCH'],
            'mem_cfgs':     [pgw_3],
            #'i_recompute':  0,
        },
        '1,2':
        {
            'var_names':    ['CLCH'],
            'i_recompute':  0,
            'mem_cfgs':     [
                {
                    'mem_oper': 'diff',
                    'mem_keys': [pgw_3, ctrl_3],
                },
            ],
        },

        #'2,0':
        #{
        #    'var_names':    ['CLCI'],
        #    'i_recompute':  i_recompute['ctrl_3_CLCI'],
        #    'mem_cfgs':     [ctrl_3],
        #},
        #'2,1':
        #{
        #    'var_names':    ['CLCI'],
        #    'i_recompute':  i_recompute['pgw_3_CLCI'],
        #    'mem_cfgs':     [pgw_3],
        #},
        #'2,2':
        #{
        #    'var_names':    ['CLCI'],
        #    'i_recompute':  0,
        #    'mem_cfgs':     [
        #        {
        #            'mem_oper': 'diff',
        #            'mem_keys': [pgw_3, ctrl_3],
        #        },
        #    ],
        #},

        '1,3':
        {
            'var_names':    ['CRELWDTOA'],
            'i_recompute':  i_recompute['ctrl_pgw_3_CRELWDTOA'],
            'mem_cfgs':     [
                {
                    'mem_oper': 'diff',
                    'mem_keys': [pgw_3, ctrl_3],
                },
            ],
        },
        #'1,4':
        #{
        #    'var_names':    ['CRELWDTOA'],
        #    'i_recompute':  i_recompute['MPI'],
        #    'mem_cfgs':     [
        #        {
        #            'mem_oper': 'diff',
        #            'mem_keys': [
        #                {
        #                    'time_periods': time_periods_cmip_ssp585,
        #                    'mem_key': 'MPI-ESM1-2-HR_ssp585',
        #                },
        #                {
        #                    'time_periods': time_periods_cmip_historical,
        #                    'mem_key': 'MPI-ESM1-2-HR_historical',
        #                },
        #            ],
        #            'label':    'MPI-ESM1-2-HR $\Delta$',
        #        },
        #    ],
        #},
        '1,4':
        {
            'var_names':    ['CRELWDTOA'],
            'i_recompute':  i_recompute['CMIP6'],
            'mem_cfgs':     [cmip_change],
            #'label':        'CMIP6 SCEN$-$HIST',
        },




        #'3,0':
        #{
        #    'var_names':    ['CLCT'],
        #    'i_recompute':  i_recompute['ctrl_3_CLCT'],
        #    'mem_cfgs':     [ctrl_3],
        #},
        #'3,1':
        #{
        #    'var_names':    ['CLCT'],
        #    'i_recompute':  i_recompute['pgw_3_CLCT'],
        #    'mem_cfgs':     [pgw_3],
        #},
        #'3,2':
        #{
        #    'var_names':    ['CLCT'],
        #    'i_recompute':  0,
        #    'mem_cfgs':     [
        #        {
        #            'mem_oper': 'diff',
        #            'mem_keys': [pgw_3, ctrl_3],
        #        },
        #    ],
        #},
        #'3,3':
        #{
        #    'var_names':    ['CRERADNDTOA'],
        #    'i_recompute':  i_recompute['ctrl_pgw_3_CRERADNDTOA'],
        #    'mem_cfgs':     [
        #        {
        #            'mem_oper': 'diff',
        #            'mem_keys': [pgw_3, ctrl_3],
        #        },
        #    ],
        #},
        #'3,4':
        #{
        #    'var_names':    ['CRERADNDTOA'],
        #    'i_recompute':  i_recompute['MPI'],
        #    'mem_cfgs':     [
        #        {
        #            'mem_oper': 'diff',
        #            'mem_keys': [
        #                {
        #                    'time_periods': time_periods_cmip_ssp585,
        #                    'mem_key': 'MPI-ESM1-2-HR_ssp585',
        #                },
        #                {
        #                    'time_periods': time_periods_cmip_historical,
        #                    'mem_key': 'MPI-ESM1-2-HR_historical',
        #                },
        #            ],
        #            'label':    'MPI-ESM1-2-HR $\Delta$',
        #        },
        #    ],
        #},





        #'3,0':
        #{
        #    'time_periods': time_periods_cmip_historical,
        #    'var_names':    ['CLCT'],
        #    'i_recompute':  i_recompute['MPI'],
        #    'mem_cfgs':     ['MPI-ESM1-2-HR_historical'],
        #},
        #'3,1':
        #{
        #    'time_periods': time_periods_cmip_ssp585,
        #    'var_names':    ['CLCT'],
        #    'i_recompute':  i_recompute['MPI'],
        #    'mem_cfgs':     ['MPI-ESM1-2-HR_ssp585'],
        #},
        #'3,2':
        #{
        #    'var_names':    ['CLCT'],
        #    'i_recompute':  0,
        #    'mem_cfgs':     [
        #        {
        #            'mem_oper': 'diff',
        #            'mem_keys': [
        #                {
        #                    'time_periods': time_periods_cmip_ssp585,
        #                    'mem_key': 'MPI-ESM1-2-HR_ssp585',
        #                },
        #                {
        #                    'time_periods': time_periods_cmip_historical,
        #                    'mem_key': 'MPI-ESM1-2-HR_historical',
        #                },
        #            ],
        #            'label':    'MPI-ESM1-2-HR $\Delta$',
        #        },
        #    ],
        #},
        #'3,3':
        #{
        #    'var_names':    ['CRERADNDTOA'],
        #    'i_recompute':  i_recompute['MPI'],
        #    'mem_cfgs':     [
        #        {
        #            'mem_oper': 'diff',
        #            'mem_keys': [
        #                {
        #                    'time_periods': time_periods_cmip_ssp585,
        #                    'mem_key': 'MPI-ESM1-2-HR_ssp585',
        #                },
        #                {
        #                    'time_periods': time_periods_cmip_historical,
        #                    'mem_key': 'MPI-ESM1-2-HR_historical',
        #                },
        #            ],
        #        },
        #    ],
        #},


    }
}
#print(cfg)
#quit()
