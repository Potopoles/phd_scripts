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
from package.nl_variables import nlv
from package.functions import loc_to_var_name
###############################################################################


plot_domain = dom_SA_ana
#plot_domain = dom_SA_ana_sea
#plot_domain = dom_SA_ana_land

agg_level = TP.ANNUAL_CYCLE
agg_level = TP.ALL_TIME
#agg_level = TP.SEASONAL_CYCLE

if agg_level == TP.ALL_TIME:
    serial_time_plt_sels = [None]
elif agg_level == TP.ANNUAL_CYCLE:
    serial_time_plt_sels = []
    for month in range(1,13,1):
        serial_time_plt_sels.append({'month':month})
elif agg_level == TP.SEASONAL_CYCLE:
    serial_time_plt_sels = []
    for season in ['DJF', 'MAM', 'JJA', 'SON']:
        serial_time_plt_sels.append({'season':season})
elif agg_level == TP.DIURNAL_CYCLE:
    serial_time_plt_sels = []
    for hour in range(0,23,3):
        serial_time_plt_sels.append({'hour':hour})
else:
    raise NotImplementedError()

models_cmip6 = models_cmip6_cldf#[0:11]
#print(models_cmip6)
#quit()
mem_keys_cmip6 = ['{}_historical'.format(model) for model in models_cmip6]

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
mem_keys_cmip6_rel_change = [{
    'mem_oper':'rel2',
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

cmip6_change = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_change,
    'label':        'SCEN$-$HIST',
}
cmip6_rel_change = {
    'mem_oper':     'mean',
    'mem_keys':     mem_keys_cmip6_rel_change,
    'label':        '(SCEN$-$HIST)/HIST',
}
mpi_change = {
    'mem_oper':'diff',
    'mem_keys':[
        {
            'mem_key':      '{}_ssp585'.format('MPI-ESM1-2-HR'), 
            'time_periods': time_periods_cmip_ssp585,
        },
        {
            'mem_key':      '{}_historical'.format('MPI-ESM1-2-HR'), 
            'time_periods': time_periods_cmip_historical,
        },
    ],
    'label':        'SCEN$-$HIST',
}
mpi_rel_change = {
    'mem_oper':'rel2',
    'mem_keys':[
        {
            'mem_key':      '{}_ssp585'.format('MPI-ESM1-2-HR'), 
            'time_periods': time_periods_cmip_ssp585,
        },
        {
            'mem_key':      '{}_historical'.format('MPI-ESM1-2-HR'), 
            'time_periods': time_periods_cmip_historical,
        },
    ],
    'label':        '(SCEN$-$HIST)/HIST',
}
cosmo_change = {
    'mem_oper':         'diff',
    'mem_keys':[
        {
            'mem_key':  'COSMO_3.3_pgw',
        },
        {
            'mem_key':  'COSMO_3.3_ctrl',
        },
    ],
    'label':        'PGW$-$CTRL',
}
cosmo_rel_change = {
    'mem_oper':         'rel2',
    'mem_keys':[
        {
            'mem_key':  'COSMO_3.3_pgw',
        },
        {
            'mem_key':  'COSMO_3.3_ctrl',
        },
    ],
    'label':        '(PGW$-$CTRL)/CTRL',
}
cosmo_rdheight2_change = {
    'mem_oper':         'diff',
    'mem_keys':[
        {
            'mem_key':  'COSMO_3.3_pgw_300hPa_rdheight2',
        },
        {
            'mem_key':  'COSMO_3.3_ctrl_rdheight2',
        },
    ],
    'label':        'PGW$-$CTRL',
}
cosmo_rdheight2_rel_change = {
    'mem_oper':         'rel2',
    'mem_keys':[
        {
            'mem_key':  'COSMO_3.3_pgw_300hPa_rdheight2',
        },
        {
            'mem_key':  'COSMO_3.3_ctrl_rdheight2',
        },
    ],
    'label':        '(PGW$-$CTRL)/CTRL',
}


def get_cmip6_scen(var_name=None):
    if var_name is not None:
        label = '{} CMIP6-EM SCEN'.format(nlv[loc_to_var_name(var_name)]['label'])
    else:
        label = 'CMIP6-EM SCEN'
    return(
        {
            'mem_oper':     'mean',
            'mem_keys':[
                {
                    'mem_key':      '{}_ssp585'.format(model), 
                    'time_periods': time_periods_cmip_ssp585,
                } for model in models_cmip6
            ],
            'label':        label,
        }
    )


obs_dict = {
    'PP':{
        'mem_key':'GPM_IMERG',
        'cmip6_bias_mem_cfg':{
            'mem_oper':         'bias',
            'mem_keys':[
                get_cmip6_hist(),
                {
                    'mem_key':          'GPM_IMERG',
                    'time_periods':     time_periods_gpm_imerg,
                },
            ],
        },
    },
}
for var_name in ['ALBEDO','LWDTOA','LWUTOA']:
    obs_dict[var_name] = {
            #'mem_key':'CERES_EBAF',
            #'cmip6_bias_mem_cfg':{
            #    'mem_oper':         'bias',
            #    'mem_keys':[
            #        get_cmip6_hist(),
            #        {
            #            'mem_key':          'CERES_EBAF',
            #            'time_periods':     time_periods_ceres_ebaf,
            #        },
            #    ],
            #},
            'mem_key':'CM_SAF_MSG_AQUA_TERRA',
            'cmip6_bias_mem_cfg':{
                'mem_oper':         'bias',
                'mem_keys':[
                    get_cmip6_hist(),
                    {
                        'mem_key':'CM_SAF_MSG_AQUA_TERRA',
                        'time_periods_full':time_periods_cm_saf_msg_aqua_terra,
                    },
                ],
            }
        }

default_time_periods = time_periods_ana 
#default_time_periods = get_time_periods_for_month(2006, 8)
#default_time_periods = time_periods_ana_old

run_cfgs = {
    'test_pgw_eval':  {
        'panel_cfgs': [
            {
                'mem_cfgs':[
                    {
                        'mem_key':  'COSMO_3.3_ctrl',
                        'label':    '{} CTRL'.format(nlv['ALBEDO']['label']),
                    }
                ],
                'var_name':     'ALBEDO',
                'time_periods': time_periods_2006,
            },
            {
                'mem_cfgs':[
                    {
                        'mem_oper':         'bias',
                        'mem_keys':[
                            {
                                'mem_key':  'COSMO_3.3_ctrl',
                            },
                            {
                                'mem_key':  obs_dict['ALBEDO']['mem_key'],
                            },
                        ],
                    },
                ],
                'var_name':     'ALBEDO',
                'time_periods': time_periods_2006,
            },
            {
                'mem_cfgs':[
                    {
                        'mem_key':  'COSMO_3.3_ctrl_rdheight2',
                        'label':    '{} CTRL'.format(nlv['ALBEDO']['label']),
                    }
                ],
                'var_name':     'ALBEDO',
                'time_periods': time_periods_2006,
            },
            {
                'mem_cfgs':[
                    {
                        'mem_oper':         'bias',
                        'mem_keys':[
                            {
                                'mem_key':  'COSMO_3.3_ctrl_rdheight2',
                            },
                            {
                                'mem_key':  obs_dict['ALBEDO']['mem_key'],
                            },
                        ],
                    },
                ],
                'var_name':     'ALBEDO',
                'time_periods': time_periods_2006,
            },



            {
                'mem_cfgs':[
                    {
                        'mem_key':  'COSMO_3.3_ctrl',
                        'label':    '{} CTRL'.format(nlv['PP']['label']),
                    }
                ],
                'var_name':     'PP',
                'time_periods': time_periods_2006,
            },
            {
                'mem_cfgs':[
                    {
                        'mem_oper':         'bias',
                        'mem_keys':[
                            {
                                'mem_key':  'COSMO_3.3_ctrl',
                            },
                            {
                                'mem_key':  obs_dict['PP']['mem_key'],
                            },
                        ],
                    },
                ],
                'var_name':     'PP',
                'time_periods': time_periods_2006,
            },
            {
                'mem_cfgs':[
                    {
                        'mem_key':  'COSMO_3.3_ctrl_rdheight2',
                        'label':    '{} CTRL'.format(nlv['PP']['label']),
                    }
                ],
                'var_name':     'PP',
                'time_periods': time_periods_2006,
            },
            {
                'mem_cfgs':[
                    {
                        'mem_oper':         'bias',
                        'mem_keys':[
                            {
                                'mem_key':  'COSMO_3.3_ctrl_rdheight2',
                            },
                            {
                                'mem_key':  obs_dict['PP']['mem_key'],
                            },
                        ],
                    },
                ],
                'var_name':     'PP',
                'time_periods': time_periods_2006,
            },



            {
                'mem_cfgs':[
                    {
                        'mem_key':  'COSMO_3.3_ctrl',
                        'label':    '{} CTRL'.format(nlv['LWUTOA']['label']),
                    }
                ],
                'var_name':     'LWUTOA',
                'time_periods': time_periods_2006,
            },
            {
                'mem_cfgs':[
                    {
                        'mem_oper':         'bias',
                        'mem_keys':[
                            {
                                'mem_key':  'COSMO_3.3_ctrl',
                            },
                            {
                                'mem_key':  obs_dict['LWUTOA']['mem_key'],
                            },
                        ],
                    },
                ],
                'var_name':     'LWUTOA',
                'time_periods': time_periods_2006,
            },
            {
                'mem_cfgs':[
                    {
                        'mem_key':  'COSMO_3.3_ctrl_rdheight2',
                        'label':    '{} CTRL'.format(nlv['LWUTOA']['label']),
                    }
                ],
                'var_name':     'LWUTOA',
                'time_periods': time_periods_2006,
            },
            {
                'mem_cfgs':[
                    {
                        'mem_oper':         'bias',
                        'mem_keys':[
                            {
                                'mem_key':  'COSMO_3.3_ctrl_rdheight2',
                            },
                            {
                                'mem_key':  obs_dict['LWUTOA']['mem_key'],
                            },
                        ],
                    },
                ],
                'var_name':     'LWUTOA',
                'time_periods': time_periods_2006,
            },
        ],
        'nrows':        3,
        'ncols':        4,
    },
    'test_pgw_change':  {
        'panel_cfgs': [
            {
                'mem_cfgs':[
                    {
                        'mem_key':  'COSMO_3.3_ctrl',
                        'label':    '{} CTRL'.format(nlv['PP']['label']),
                    }
                ],
                'var_name':     'PP',
                'time_periods': time_periods_2006,
            },
            {
                'mem_cfgs':[
                    cosmo_change,
                ],
                'var_name':     'PP',
                'time_periods': time_periods_2006,
            },
            {
                'mem_cfgs':[
                    {
                        'mem_key':  'COSMO_3.3_ctrl_rdheight2',
                        'label':    '{} CTRL'.format(nlv['PP']['label']),
                    }
                ],
                'var_name':     'PP',
                'time_periods': time_periods_2006,
            },
            {
                'mem_cfgs':[
                    cosmo_rdheight2_change,
                ],
                'var_name':     'PP',
                'time_periods': time_periods_2006,
            },

            {
                'mem_cfgs':[
                    {
                        'mem_key':  'COSMO_3.3_ctrl',
                        'label':    '{} CTRL'.format(nlv['ALBEDO']['label']),
                    }
                ],
                'var_name':     'ALBEDO',
                'time_periods': time_periods_2006,
            },
            {
                'mem_cfgs':[
                    cosmo_change,
                ],
                'var_name':     'ALBEDO',
                'time_periods': time_periods_2006,
            },
            {
                'mem_cfgs':[
                    {
                        'mem_key':  'COSMO_3.3_ctrl_rdheight2',
                        'label':    '{} CTRL'.format(nlv['ALBEDO']['label']),
                    }
                ],
                'var_name':     'ALBEDO',
                'time_periods': time_periods_2006,
            },
            {
                'mem_cfgs':[
                    cosmo_rdheight2_change,
                ],
                'var_name':     'ALBEDO',
                'time_periods': time_periods_2006,
            },

            {
                'mem_cfgs':[
                    {
                        'mem_key':  'COSMO_3.3_ctrl',
                        'label':    '{} CTRL'.format(nlv['LWUTOA']['label']),
                    }
                ],
                'var_name':     'LWUTOA',
                'time_periods': time_periods_2006,
            },
            {
                'mem_cfgs':[
                    cosmo_change,
                ],
                'var_name':     'LWUTOA',
                'time_periods': time_periods_2006,
            },
            {
                'mem_cfgs':[
                    {
                        'mem_key':  'COSMO_3.3_ctrl_rdheight2',
                        'label':    '{} CTRL'.format(nlv['LWUTOA']['label']),
                    }
                ],
                'var_name':     'LWUTOA',
                'time_periods': time_periods_2006,
            },
            {
                'mem_cfgs':[
                    cosmo_rdheight2_change,
                ],
                'var_name':     'LWUTOA',
                'time_periods': time_periods_2006,
            },
        ],
        'nrows':        3,
        'ncols':        4,
    },

    'change_1':  {
        'panel_cfgs': [
            {
                'mem_cfgs':[
                    {
                        'mem_key':  'COSMO_3.3_ctrl',
                        'label':    '{} CTRL'.format(nlv['PP']['label']),
                    }
                ],
                'var_name':     'PP',
            },
            {
                'mem_cfgs':[
                    {
                        'mem_key':  'COSMO_3.3_ctrl',
                        'label':    '{} CTRL'.format(nlv[loc_to_var_name('UV@alt=500')]['label']),
                    }
                ],
                'var_name':     'UV@alt=500',
            },
            {
                'mem_cfgs':[
                    {
                        'mem_key':  'COSMO_3.3_ctrl',
                        'label':    '{} CTRL'.format(nlv[loc_to_var_name('T@alt=5500')]['label']),
                    }
                ],
                'var_name':     'T@alt=5500',
            },


            {
                'mem_cfgs':[
                    cosmo_change,
                ],
                'var_name':     'PP',
            },
            {
                'mem_cfgs':[
                    cosmo_change,
                ],
                'var_name':     'UV@alt=500',
            },
            {
                'mem_cfgs':[
                    cosmo_change,
                ],
                'var_name':     'T@alt=5500',
            },


            {
                'mem_cfgs':[
                    {
                        'mem_key':      'MPI-ESM1-2-HR_historical',
                        'time_periods': time_periods_cmip_historical,
                        'label':    '{} MPI-ESM HIST'.format(nlv['PP']['label']),
                    },
                ],
                'var_name':     'PP',
            },
            {
                'mem_cfgs':[
                    {
                        'mem_key':      'MPI-ESM1-2-HR_historical',
                        'time_periods': time_periods_cmip_historical,
                        'label':    '{} MPI-ESM HIST'.format(nlv[loc_to_var_name('UV@alt=500')]['label']),
                    },
                ],
                'var_name':     'UV@alt=500',
            },
            {
                'mem_cfgs':[
                    {
                        'mem_key':      'MPI-ESM1-2-HR_historical',
                        'time_periods': time_periods_cmip_historical,
                        'label':    '{} MPI-ESM HIST'.format(nlv[loc_to_var_name('T@alt=5500')]['label']),
                    },
                ],
                'var_name':     'T@alt=5500',
            },



            {
                'mem_cfgs':[
                    mpi_change,
                ],
                'var_name':     'PP',
            },
            {
                'mem_cfgs':[
                    mpi_change,
                ],
                'var_name':     'UV@alt=500',
            },
            {
                'mem_cfgs':[
                    mpi_change,
                ],
                'var_name':     'T@alt=5500',
            },



            {
                'mem_cfgs':[
                    get_cmip6_hist('PP'),
                ],
                'var_name':     'PP',
            },
            {
                'mem_cfgs':[
                    get_cmip6_hist('UV@alt=500'),
                ],
                'var_name':     'UV@alt=500',
            },
            {
                'mem_cfgs':[
                    get_cmip6_hist('T@alt=5500'),
                ],
                'var_name':     'T@alt=5500',
            },



            {
                'mem_cfgs':[
                    cmip6_change,
                ],
                'var_name':     'PP',
            },
            {
                'mem_cfgs':[
                    cmip6_change,
                ],
                'var_name':     'UV@alt=500',
            },
            {
                'mem_cfgs':[
                    cmip6_change,
                ],
                'var_name':     'T@alt=5500',
            },
        ],
        'nrows':        6,
        'ncols':        3,
    },


    'change_2':  {
        'panel_cfgs': [
            {
                'mem_cfgs':[
                    {
                        'mem_key':  'COSMO_3.3_ctrl',
                        'label':    '{} CTRL'.format(nlv['PP']['label']),
                    }
                ],
                'var_name':     'PP',
            },
            {
                'mem_cfgs':[
                    cosmo_change,
                ],
                'var_name':     'PP',
            },
            {
                'mem_cfgs':[
                    get_cmip6_hist('PP'),
                ],
                'var_name':     'PP',
            },
            {
                'mem_cfgs':[
                    cmip6_change,
                ],
                'var_name':     'PP',
            },



            {
                'mem_cfgs':[
                    {
                        'mem_key':  'COSMO_3.3_ctrl',
                        'label':    '{} CTRL'.format(nlv['ALBEDO']['label']),
                    }
                ],
                'var_name':     'ALBEDO',
            },
            {
                'mem_cfgs':[
                    cosmo_change,
                ],
                'var_name':     'ALBEDO',
            },
            {
                'mem_cfgs':[
                    get_cmip6_hist('ALBEDO'),
                ],
                'var_name':     'ALBEDO',
            },
            {
                'mem_cfgs':[
                    cmip6_change,
                ],
                'var_name':     'ALBEDO',
            },



            {
                'mem_cfgs':[
                    {
                        'mem_key':  'COSMO_3.3_ctrl',
                        'label':    '{} CTRL'.format(nlv['LWUTOA']['label']),
                    }
                ],
                'var_name':     'LWUTOA',
            },
            {
                'mem_cfgs':[
                    cosmo_change,
                ],
                'var_name':     'LWUTOA',
            },
            {
                'mem_cfgs':[
                    get_cmip6_hist('LWUTOA'),
                ],
                'var_name':     'LWUTOA',
            },
            {
                'mem_cfgs':[
                    cmip6_change,
                ],
                'var_name':     'LWUTOA',
            },
        ],
        'nrows':        3,
        'ncols':        4,
    },



    'eval':  {
        'panel_cfgs': [
            {
                'mem_cfgs':[
                    {
                        'mem_key':  'COSMO_3.3_ctrl',
                        'label':    '{} CTRL'.format(nlv['ALBEDO']['label']),
                    }
                ],
                'var_name':     'ALBEDO',
            },
            {
                'mem_cfgs':[
                    {
                        'mem_oper':         'bias',
                        'mem_keys':[
                            {
                                'mem_key':  'COSMO_3.3_ctrl',
                            },
                            {
                                'mem_key':  obs_dict['ALBEDO']['mem_key'],
                            },
                        ],
                    },
                ],
                'var_name':     'ALBEDO',
            },
            {
                'mem_cfgs':[
                    get_cmip6_hist('ALBEDO'),
                ],
                'var_name':     'ALBEDO',
            },
            {
                'mem_cfgs':[
                    obs_dict['ALBEDO']['cmip6_bias_mem_cfg']
                ],
                'var_name':     'ALBEDO',
            },



            {
                'mem_cfgs':[
                    {
                        'mem_key':  'COSMO_3.3_ctrl',
                        'label':    '{} CTRL'.format(nlv['PP']['label']),
                    }
                ],
                'var_name':     'PP',
                #'pickle_append':'cg50',
            },
            {
                'mem_cfgs':[
                    {
                        'mem_oper':         'bias',
                        'mem_keys':[
                            {
                                'mem_key':  'COSMO_3.3_ctrl',
                            },
                            {
                                'mem_key':  obs_dict['PP']['mem_key'],
                            },
                        ],
                    },
                ],
                'var_name':     'PP',
                #'pickle_append':'cg50',
            },
            {
                'mem_cfgs':[
                    get_cmip6_hist('PP'),
                ],
                'var_name':     'PP',
            },
            {
                'mem_cfgs':[
                    obs_dict['PP']['cmip6_bias_mem_cfg']
                ],
                'var_name':     'PP',
            },



            {
                'mem_cfgs':[
                    {
                        'mem_key':  'COSMO_3.3_ctrl',
                        'label':    '{} CTRL'.format(nlv['LWUTOA']['label']),
                    }
                ],
                'var_name':     'LWUTOA',
            },
            {
                'mem_cfgs':[
                    {
                        'mem_oper':         'bias',
                        'mem_keys':[
                            {
                                'mem_key':  'COSMO_3.3_ctrl',
                            },
                            {
                                'mem_key':  obs_dict['LWUTOA']['mem_key'],
                            },
                        ],
                    },
                ],
                'var_name':     'LWUTOA',
            },
            {
                'mem_cfgs':[
                    get_cmip6_hist('LWUTOA'),
                ],
                'var_name':     'LWUTOA',
            },
            {
                'mem_cfgs':[
                    obs_dict['LWUTOA']['cmip6_bias_mem_cfg']
                ],
                'var_name':     'LWUTOA',
            },
        ],
        'nrows':        3,
        'ncols':        4,
    },

    'change_3':  {
        'panel_cfgs': [
            {
                'mem_cfgs':[
                    {
                        'mem_key':  'COSMO_3.3_ctrl',
                        'label':    'CTRL',
                    }
                ],
                'var_name':     'PP',
                'pickle_append':'cg50',
            },
            {
                'mem_cfgs':[
                    {
                        'mem_key':  'COSMO_3.3_pgw',
                        'label':    'PGW',
                    }
                ],
                'var_name':     'PP',
                'pickle_append':'cg50',
            },
            {
                'mem_cfgs':[
                    cosmo_change,
                ],
                'var_name':     'PP',
                'pickle_append':'cg50',
            },
            {
                'mem_cfgs':[
                    cosmo_rel_change,
                ],
                'var_name':     'PP',
                'pickle_append':'cg50',
            },


            {
                'mem_cfgs':[
                    get_cmip6_hist(),
                ],
                'var_name':     'PP',
            },
            {
                'mem_cfgs':[
                    get_cmip6_scen(),
                ],
                'var_name':     'PP',
            },
            {
                'mem_cfgs':[
                    cmip6_change,
                ],
                'var_name':     'PP',
            },
            {
                'mem_cfgs':[
                    cmip6_rel_change,
                ],
                'var_name':     'PP',
            },


            {
                'mem_cfgs':[
                    {
                        'mem_key':      'MPI-ESM1-2-HR_historical',
                        'time_periods': time_periods_cmip_historical,
                        'label':    'MPI-ESM HIST',
                    },
                ],
                'var_name':     'PP',
            },
            {
                'mem_cfgs':[
                    {
                        'mem_key':      'MPI-ESM1-2-HR_ssp585',
                        'time_periods': time_periods_cmip_ssp585,
                        'label':    'MPI-ESM SCEN',
                    },
                ],
                'var_name':     'PP',
            },
            {
                'mem_cfgs':[
                    mpi_change,
                ],
                'var_name':     'PP',
            },
            {
                'mem_cfgs':[
                    mpi_rel_change,
                ],
                'var_name':     'PP',
            },
        ],
        'nrows':        3,
        'ncols':        4,
    },
}

use_cfg = 'test_pgw_eval'
use_cfg = 'test_pgw_change'

use_cfg = 'eval'
#use_cfg = 'change_3'

## OLD CONFIGS
#use_cfg = 'change_2'
#use_cfg = 'change_1'

run_cfg = run_cfgs[use_cfg]

nrows = run_cfg['nrows']
ncols = run_cfg['ncols']

name_dict = {
    plot_domain['key']:use_cfg,
    'time':agg_level,
    '200608':'',
}


cfg = {
    'serial_time_plt_sels': serial_time_plt_sels,
    'sub_dir':              'sp_paper',
    'name_dict':            name_dict,
    'figsize':              (nlp['figsize_spatial']['{}x{}'.format(
                                    nrows,ncols).format(nrows,ncols)][0],
                             nlp['figsize_spatial']['{}x{}'.format(
                                    nrows,ncols).format(nrows,ncols)][1]),
    'nrows':                nrows,
    'ncols':                ncols,
    'subplots_adjust_spatial':
                            '{}x{}'.format(nrows, ncols),
    'arg_subplots_adjust':  {
                            },
    'i_remove_axis_labels': 2,
    'kwargs_remove_axis_labels': {
        'remove_level': 2,
    },
    'kwargs_panel_labels' : {
        'shift_up': 0.05,
        'shift_right': -0.05,
    },
    'all_panels':
        {
            'ana_number':   1,
            'agg_level':    agg_level,
            'plot_domain':  plot_domain,
            'i_recompute':  1,
        },
    'panels':
    {
    }
}

mi = 0
for panel_cfg in run_cfg['panel_cfgs']:
    #print(mem_cfg)
    col_ind = mi % ncols
    row_ind = int(mi/ncols)
    pan_key = '{},{}'.format(row_ind, col_ind)

    if panel_cfg is not None:
        #print(panel_cfg)
        
        if 'time_periods' in panel_cfg:
            time_periods = panel_cfg['time_periods']
        else:
            time_periods = default_time_periods

        pan_dict = {
            'var_names':    [panel_cfg['var_name']],
            'mem_cfgs':     panel_cfg['mem_cfgs'],
            'time_periods': time_periods
        }

        if 'pickle_append' in panel_cfg:
            pan_dict['pickle_append'] = panel_cfg['pickle_append']

        cfg['panels'][pan_key] = pan_dict

    mi += 1
#print(cfg['panels'])
#quit()


