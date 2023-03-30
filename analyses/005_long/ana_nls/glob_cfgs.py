#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    global configs for ana_nls
author			Christoph Heim
"""
###############################################################################
from package.nl_models import models_cmip6, models_cmip6_cldf
from base.nl_time_periods import *
###############################################################################
models_cmip6 = models_cmip6_cldf#[5:7]

def get_cmip6_hist(var_name=None):
    if var_name is not None:
        label = '{} CMIP6-EM HIST'.format(nlv[loc_to_var_name(var_name)]['label'])
    else:
        label = 'CMIP6-EM HIST'
    return(
        {
            'mem_oper':     'mean',
            'mem_keys':[
                {
                    'mem_key':      '{}_historical'.format(model), 
                    'time_periods': time_periods_cmip6_hist,
                } for model in models_cmip6
            ],
            'label':        label,
        }
    )


mem_keys_cmip6_hist = ['{}_historical'.format(model) for model in models_cmip6]
mem_keys_cmip6_scen = ['{}_ssp585'.format(model) for model in models_cmip6]
mem_keys_cmip6_change = [{
    'mem_oper':'diff',
    'mem_keys':[
        {
            'mem_key':      '{}_ssp585'.format(model), 
            'time_periods': time_periods_cmip6_scen,
        },
        {
            'mem_key':      '{}_historical'.format(model), 
            'time_periods': time_periods_cmip6_hist,
        },
    ]} for model in models_cmip6
]
mem_keys_cmip6_change_JFM = [{
    'mem_oper':'diff',
    'mem_keys':[
        {
            'mem_key':      '{}_ssp585'.format(model), 
            'time_periods': time_periods_cmip6_scen_JFM,
        },
        {
            'mem_key':      '{}_historical'.format(model), 
            'time_periods': time_periods_cmip6_hist_JFM,
        },
    ]} for model in models_cmip6
]
mem_keys_cmip6_change_FMA = [{
    'mem_oper':'diff',
    'mem_keys':[
        {
            'mem_key':      '{}_ssp585'.format(model), 
            'time_periods': time_periods_cmip6_scen_FMA,
        },
        {
            'mem_key':      '{}_historical'.format(model), 
            'time_periods': time_periods_cmip6_hist_FMA,
        },
    ]} for model in models_cmip6
]
mem_keys_cmip6_change_AMJ = [{
    'mem_oper':'diff',
    'mem_keys':[
        {
            'mem_key':      '{}_ssp585'.format(model), 
            'time_periods': time_periods_cmip6_scen_AMJ,
        },
        {
            'mem_key':      '{}_historical'.format(model), 
            'time_periods': time_periods_cmip6_hist_AMJ,
        },
    ]} for model in models_cmip6
]
mem_keys_cmip6_change_MJJ = [{
    'mem_oper':'diff',
    'mem_keys':[
        {
            'mem_key':      '{}_ssp585'.format(model), 
            'time_periods': time_periods_cmip6_scen_MJJ,
        },
        {
            'mem_key':      '{}_historical'.format(model), 
            'time_periods': time_periods_cmip6_hist_MJJ,
        },
    ]} for model in models_cmip6
]
mem_keys_cmip6_change_JAS = [{
    'mem_oper':'diff',
    'mem_keys':[
        {
            'mem_key':      '{}_ssp585'.format(model), 
            'time_periods': time_periods_cmip6_scen_JAS,
        },
        {
            'mem_key':      '{}_historical'.format(model), 
            'time_periods': time_periods_cmip6_hist_JAS,
        },
    ]} for model in models_cmip6
]
mem_keys_cmip6_change_ASO = [{
    'mem_oper':'diff',
    'mem_keys':[
        {
            'mem_key':      '{}_ssp585'.format(model), 
            'time_periods': time_periods_cmip6_scen_ASO,
        },
        {
            'mem_key':      '{}_historical'.format(model), 
            'time_periods': time_periods_cmip6_hist_ASO,
        },
    ]} for model in models_cmip6
]
mem_keys_cmip6_change_MJ = [{
    'mem_oper':'diff',
    'mem_keys':[
        {
            'mem_key':      '{}_ssp585'.format(model), 
            'time_periods': time_periods_cmip6_scen_MJ,
        },
        {
            'mem_key':      '{}_historical'.format(model), 
            'time_periods': time_periods_cmip6_hist_MJ,
        },
    ]} for model in models_cmip6
]
mem_keys_cmip6_change_OND = [{
    'mem_oper':'diff',
    'mem_keys':[
        {
            'mem_key':      '{}_ssp585'.format(model), 
            'time_periods': time_periods_cmip6_scen_OND,
        },
        {
            'mem_key':      '{}_historical'.format(model), 
            'time_periods': time_periods_cmip6_hist_OND,
        },
    ]} for model in models_cmip6
]
mem_keys_cmip6_change_ONDJ = [{
    'mem_oper':'diff',
    'mem_keys':[
        {
            'mem_key':      '{}_ssp585'.format(model), 
            'time_periods': time_periods_cmip6_scen_ONDJ,
        },
        {
            'mem_key':      '{}_historical'.format(model), 
            'time_periods': time_periods_cmip6_hist_ONDJ,
        },
    ]} for model in models_cmip6
]
mem_keys_cmip6_change_NDJ = [{
    'mem_oper':'diff',
    'mem_keys':[
        {
            'mem_key':      '{}_ssp585'.format(model), 
            'time_periods': time_periods_cmip6_scen_NDJ,
        },
        {
            'mem_key':      '{}_historical'.format(model), 
            'time_periods': time_periods_cmip6_hist_NDJ,
        },
    ]} for model in models_cmip6
]
mem_keys_cmip6_rel_change = [{
    'mem_oper':'rel0.00001',
    'mem_keys':[
        {
            'mem_key':      '{}_ssp585'.format(model), 
            'time_periods': time_periods_cmip6_scen,
        },
        {
            'mem_key':      '{}_historical'.format(model), 
            'time_periods': time_periods_cmip6_hist,
        },
    ]} for model in models_cmip6
]
mem_keys_cmip6_bias = [{
    'mem_oper':'bias',
    'mem_keys':[
        {
            'mem_key':      '{}_historical'.format(model), 
            'time_periods': time_periods_cmip6_hist,
        },
        {
            'mem_key':      'ERA5', 
            #'time_periods': time_periods_ana,
            'time_periods': time_periods_cmip6_hist,
        },
    ]} for model in models_cmip6
]

ctrl = {
    'mem_key':      'COSMO_3.3_ctrl', 
}
ctrl_rdheight2_spubc1 = {
    'mem_key':      'COSMO_3.3_ctrl_rdheight2_spubc1', 
}
ctrl_rdheight2 = {
    'mem_key':      'COSMO_3.3_ctrl_rdheight2', 
}
pgw = {
    #'mem_key':      'COSMO_3.3_pgw', 
    'mem_key':      'COSMO_3.3_pgw3', 
}
pgw_rdheight2 = {
    'mem_key':      'COSMO_3.3_pgw_rdheight2', 
}
era = {
    'mem_key':      'ERA5', 
}
mpi_hist = {
    'mem_key':      'MPI-ESM1-2-HR_historical', 
    #'time_periods': time_periods_cmip6_hist,
}
mpi_hist_JFM = {
    'mem_key':      'MPI-ESM1-2-HR_historical', 
    'time_periods': time_periods_cmip6_hist_JFM,
}
mpi_hist_AMJ = {
    'mem_key':      'MPI-ESM1-2-HR_historical', 
    'time_periods': time_periods_cmip6_hist_AMJ,
}
mpi_hist_JAS = {
    'mem_key':      'MPI-ESM1-2-HR_historical', 
    'time_periods': time_periods_cmip6_hist_JAS,
}
mpi_hist_OND = {
    'mem_key':      'MPI-ESM1-2-HR_historical', 
    'time_periods': time_periods_cmip6_hist_OND,
}
mpi_scen = {
    'mem_key':      'MPI-ESM1-2-HR_ssp585', 
    #'time_periods': time_periods_cmip6_scen,
}
cmip6_hist = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_hist,
    #'time_periods': time_periods_cmip6_hist,
}
cmip6_hist_JFM = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_hist,
    'time_periods': time_periods_cmip6_hist_JFM,
}
cmip6_hist_FMA = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_hist,
    'time_periods': time_periods_cmip6_hist_FMA,
}
cmip6_hist_AMJ = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_hist,
    'time_periods': time_periods_cmip6_hist_AMJ,
}
cmip6_hist_MJJ = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_hist,
    'time_periods': time_periods_cmip6_hist_MJJ,
}
cmip6_hist_JAS = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_hist,
    'time_periods': time_periods_cmip6_hist_JAS,
}
cmip6_hist_ASO = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_hist,
    'time_periods': time_periods_cmip6_hist_ASO,
}
cmip6_hist_OND = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_hist,
    'time_periods': time_periods_cmip6_hist_OND,
}
cmip6_hist_NDJ = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_hist,
    'time_periods': time_periods_cmip6_hist_NDJ,
}
cmip6_scen = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_scen,
    #'time_periods': time_periods_cmip6_scen,
}
cmip6_change = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_change,
}
cmip6_change_JFM = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_change_JFM,
}
cmip6_change_FMA = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_change_FMA,
}
cmip6_change_AMJ = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_change_AMJ,
}
cmip6_change_MJ = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_change_MJ,
}
cmip6_change_MJJ = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_change_MJJ,
}
cmip6_change_JAS = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_change_JAS,
}
cmip6_change_ASO = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_change_ASO,
}
cmip6_change_OND = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_change_OND,
}
cmip6_change_ONDJ = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_change_ONDJ,
}
cmip6_change_NDJ = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_change_NDJ,
}
cmip6_rel_change = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_rel_change,
}
ctrl_bias = {
    'mem_oper':     'bias',
    'mem_keys':     [ctrl, era],
}
ctrl_rel_bias = {
    'mem_oper':     'rel0.0001',
    'mem_keys':     [ctrl, era],
}
#bias_mpi = {
#    'mem_oper':     'bias',
#    'mem_keys':     [
#        {
#            'mem_key':      'MPI-ESM1-2-HR_historical', 
#            'time_periods': time_periods_cmip6_hist,
#        },
#        {
#            'mem_key':      'ERA5', 
#            'time_periods': time_periods_default,
#        },
#    ],
#}
cosmo_change = {
    'mem_oper':     'diff',
    'mem_keys':     [pgw, ctrl],
}
cosmo_rel_change = {
    'mem_oper':     'rel0.00001',
    'mem_keys':     [pgw, ctrl],
}
cosmo_rdheight2_change = {
    'mem_oper':     'diff',
    'mem_keys':     [
        {
            'mem_key':      'COSMO_3.3_pgw_300hPa_rdheight2', 
        },
        {
            'mem_key':      'COSMO_3.3_ctrl_rdheight2', 
        },
    ],
}
mpi_change = {
    'mem_oper':     'diff',
    'mem_keys':     [
        {
            'mem_key':      'MPI-ESM1-2-HR_ssp585', 
            'time_periods': time_periods_cmip6_scen,
        },
        {
            'mem_key':      'MPI-ESM1-2-HR_historical', 
            'time_periods': time_periods_cmip6_hist,
        },
    ],
}
mpi_change_JFM = {
    'mem_oper':     'diff',
    'mem_keys':     [
        {
            'mem_key':      'MPI-ESM1-2-HR_ssp585', 
            'time_periods': time_periods_cmip6_scen_JFM,
        },
        {
            'mem_key':      'MPI-ESM1-2-HR_historical', 
            'time_periods': time_periods_cmip6_hist_JFM,
        },
    ],
}
mpi_change_FMA = {
    'mem_oper':     'diff',
    'mem_keys':     [
        {
            'mem_key':      'MPI-ESM1-2-HR_ssp585', 
            'time_periods': time_periods_cmip6_scen_FMA,
        },
        {
            'mem_key':      'MPI-ESM1-2-HR_historical', 
            'time_periods': time_periods_cmip6_hist_FMA,
        },
    ],
}
mpi_change_MAM = {
    'mem_oper':     'diff',
    'mem_keys':     [
        {
            'mem_key':      'MPI-ESM1-2-HR_ssp585', 
            'time_periods': time_periods_cmip6_scen_MAM,
        },
        {
            'mem_key':      'MPI-ESM1-2-HR_historical', 
            'time_periods': time_periods_cmip6_hist_MAM,
        },
    ],
}
mpi_change_AMJ = {
    'mem_oper':     'diff',
    'mem_keys':     [
        {
            'mem_key':      'MPI-ESM1-2-HR_ssp585', 
            'time_periods': time_periods_cmip6_scen_AMJ,
        },
        {
            'mem_key':      'MPI-ESM1-2-HR_historical', 
            'time_periods': time_periods_cmip6_hist_AMJ,
        },
    ],
}
mpi_change_MJJ = {
    'mem_oper':     'diff',
    'mem_keys':     [
        {
            'mem_key':      'MPI-ESM1-2-HR_ssp585', 
            'time_periods': time_periods_cmip6_scen_MJJ,
        },
        {
            'mem_key':      'MPI-ESM1-2-HR_historical', 
            'time_periods': time_periods_cmip6_hist_MJJ,
        },
    ],
}
mpi_change_JJA = {
    'mem_oper':     'diff',
    'mem_keys':     [
        {
            'mem_key':      'MPI-ESM1-2-HR_ssp585', 
            'time_periods': time_periods_cmip6_scen_JJA,
        },
        {
            'mem_key':      'MPI-ESM1-2-HR_historical', 
            'time_periods': time_periods_cmip6_hist_JJA,
        },
    ],
}
mpi_change_JAS = {
    'mem_oper':     'diff',
    'mem_keys':     [
        {
            'mem_key':      'MPI-ESM1-2-HR_ssp585', 
            'time_periods': time_periods_cmip6_scen_JAS,
        },
        {
            'mem_key':      'MPI-ESM1-2-HR_historical', 
            'time_periods': time_periods_cmip6_hist_JAS,
        },
    ],
}
mpi_change_ASO = {
    'mem_oper':     'diff',
    'mem_keys':     [
        {
            'mem_key':      'MPI-ESM1-2-HR_ssp585', 
            'time_periods': time_periods_cmip6_scen_ASO,
        },
        {
            'mem_key':      'MPI-ESM1-2-HR_historical', 
            'time_periods': time_periods_cmip6_hist_ASO,
        },
    ],
}
mpi_change_SON = {
    'mem_oper':     'diff',
    'mem_keys':     [
        {
            'mem_key':      'MPI-ESM1-2-HR_ssp585', 
            'time_periods': time_periods_cmip6_scen_SON,
        },
        {
            'mem_key':      'MPI-ESM1-2-HR_historical', 
            'time_periods': time_periods_cmip6_hist_SON,
        },
    ],
}
mpi_change_OND = {
    'mem_oper':     'diff',
    'mem_keys':     [
        {
            'mem_key':      'MPI-ESM1-2-HR_ssp585', 
            'time_periods': time_periods_cmip6_scen_OND,
        },
        {
            'mem_key':      'MPI-ESM1-2-HR_historical', 
            'time_periods': time_periods_cmip6_hist_OND,
        },
    ],
}
mpi_change_NDJ = {
    'mem_oper':     'diff',
    'mem_keys':     [
        {
            'mem_key':      'MPI-ESM1-2-HR_ssp585', 
            'time_periods': time_periods_cmip6_scen_NDJ,
        },
        {
            'mem_key':      'MPI-ESM1-2-HR_historical', 
            'time_periods': time_periods_cmip6_hist_NDJ,
        },
    ],
}
mpi_change_DJF = {
    'mem_oper':     'diff',
    'mem_keys':     [
        {
            'mem_key':      'MPI-ESM1-2-HR_ssp585', 
            'time_periods': time_periods_cmip6_scen_DJF,
        },
        {
            'mem_key':      'MPI-ESM1-2-HR_historical', 
            'time_periods': time_periods_cmip6_hist_DJF,
        },
    ],
}
cmip6_change = {
    'mem_oper':     'diff',
    'mem_keys':     [
        {
            'mem_oper':     'mean',
            'mem_keys':     mem_keys_cmip6_scen,
            'time_periods': time_periods_cmip6_scen,
        },
        {
            'mem_oper':     'mean',
            'mem_keys':     mem_keys_cmip6_hist,
            'time_periods': time_periods_cmip6_hist,
        },
    ],
}
cmip6_bias = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_bias,
}
cmip6_rel = {
    'mem_oper':     'rel0.0001',
    'mem_keys':     mem_keys_cmip6_bias,
}



cosmo_bias_cm_saf = {
    'mem_oper':         'bias',
    'mem_keys':[
        {
            'mem_key':  'COSMO_3.3_ctrl',
        },
        {
            'mem_key':  'CM_SAF_MSG_AQUA_TERRA',
        },
    ],
}

cmip6_hist_bias_cm_saf = {
    'mem_oper':         'bias',
    'mem_keys':[
        get_cmip6_hist(),
        {
            'mem_key':'CM_SAF_MSG_AQUA_TERRA',
            'time_periods_full':time_periods_cm_saf_msg_aqua_terra,
        },
    ],
}



cosmo_bias_gpm_imerg = {
    'mem_oper':         'bias',
    'mem_keys':[
        {
            'mem_key':  'COSMO_3.3_ctrl',
        },
        {
            'mem_key':  'GPM_IMERG',
        },
    ],
}

cmip6_hist_bias_gpm_imerg = {
    'mem_oper':         'bias',
    'mem_keys':[
        get_cmip6_hist(),
        {
            'mem_key':'GPM_IMERG',
            'time_periods_full':time_periods_gpm_imerg,
        },
    ],
}
