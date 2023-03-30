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
from package.nl_models import models_cmip6
from nl_plot_org_ana import nlp
###############################################################################

time_periods = []
start_year = 2006
end_year = 2006
start_month = 8
end_month = 8
start_day = 1
end_day = 20

time_periods = [{'first_date':datetime(start_year,start_month,start_day),
                 'last_date':datetime(end_year,end_month,end_day)}]

plot_domain = dom_SA_ana_sea
#plot_domain = dom_SA_ana
#plot_domain = dom_SA_ana_land
#plot_domain = dom_ITCZ
#plot_domain = dom_trades

agg_level = TP.ALL_TIME

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

#sat = 'CERES_EBAF'
sat = 'CM_SAF_MSG_AQUA_TERRA'
ctrl = 'ctrl'
pgw = 'pgw'

i_recompute = {
    ctrl:       0,
    pgw:        1,
    #sat:        1,
}

var_name = 'LWUTOA'
#var_name = 'ALBEDO'
#var_name = 'CLWUTOA'
#var_name = 'CRELWUTOA'
#var_name = 'CLWUTOA'

#var_name = 'SWNDTOA'
#var_name = 'RADNDTOA'
#var_name = 'SUBS'


ctrl_mem_types = [
    #'_ref',
    #'_ref',
    #'_ref',
    '_ref',
    #'_ref',
    #'_ref',
    #'_ref',
    #'_ref',
    #'',
    '',

    #'_rdheight2_spubc1',
    #'_rdheight2_spubc1',
]

pgw_mem_types = [
    #'_ref',
    #'5_rdheight2',
    #'9_rdheight2',
    '10_rdheight2',
    #'14_rdheight2',
    #'11_rdheight2',
    #'15_rdheight2',
    #'16_rdheight2',
    #'_final_test',
    #'17',
    '',
]

#ctrl_mem_types = [
#    '_ref',
#    '_rdheight2',
#    '_ref',
#]
#pgw_mem_types = [
#    '_ref',
#    '_rdheight2',
#    '_rdheight2',
#]

name_dict = {
    plot_domain['key']:var_name,
    'time':agg_level,
}

nrows = 3
ncols = max(2,max(len(ctrl_mem_types),len(pgw_mem_types)))

cfg = {
    # TODO: this cannot yet be activated here. hast to be done in nl_01.py
    #'i_coarse_grain' :      100,
    'serial_time_plt_sels': serial_time_plt_sels,
    'sub_dir':              'sp_fix_pgw',
    'name_dict':            name_dict,
    'figsize':              (nlp['figsize_spatial']['{}x{}'.format(
                                    nrows,ncols).format(nrows,ncols)][0],
                             nlp['figsize_spatial']['{}x{}'.format(
                                    nrows,ncols).format(nrows,ncols)][1]),
    'nrows':                nrows,
    'ncols':                ncols,
    'subplots_adjust_spatial':
                            '{}x{}'.format(nrows,ncols),
    'i_remove_axis_labels': 2,
    'arg_subplots_adjust':  {
                            },
    'all_panels':
        {
            'ana_number':   1,
            'var_names':    [var_name],
            'time_periods': time_periods,
            'agg_level':    agg_level,
            'plot_domain':  plot_domain,
            'plot_ax_cbars':{
                                'abs':  1,
                                'diff': 1,
                            },
            'i_recompute':  0,
        },
    'panels':
    {
        #'0,0':
        #{
        #    'i_recompute':  i_recompute[sat],
        #    'mem_keys':     [sat],
        #},


    }
}

i = 0
while i < max(len(ctrl_mem_types),len(pgw_mem_types)-1):
    ### CTRL
    panel_key = '0,{}'.format(i)
    cfg['panels'][panel_key] = {}
    #cfg['panels'][panel_key]['i_recompute'] = 1
    # members
    cfg['panels'][panel_key]['mem_keys'] = []
    mem_key = 'COSMO_3.3_ctrl{}'.format(ctrl_mem_types[i])
    cfg['panels'][panel_key]['mem_keys'].append(
        mem_key
    )

    #### EVAL
    #panel_key = '1,{}'.format(i)
    #cfg['panels'][panel_key] = {}
    #cfg['panels'][panel_key]['i_recompute'] = 1
    ## members
    #cfg['panels'][panel_key]['mem_keys'] = []
    #mem_key = {'diff':['COSMO_3.3_ctrl{}'.format(ctrl_mem_types[i]),
    #                    sat],
    #                    'label':'CTRL - SAT'}
    #cfg['panels'][panel_key]['mem_keys'].append(
    #    mem_key
    #)

    ### PGW
    panel_key = '1,{}'.format(i)
    cfg['panels'][panel_key] = {}
    cfg['panels'][panel_key]['i_recompute'] = 1
    # members
    cfg['panels'][panel_key]['mem_keys'] = []
    mem_key = 'COSMO_3.3_pgw{}'.format(pgw_mem_types[i])
    cfg['panels'][panel_key]['mem_keys'].append(
        mem_key
    )

    ### PGW - CTRL
    panel_key = '2,{}'.format(i)
    cfg['panels'][panel_key] = {}
    # members
    cfg['panels'][panel_key]['mem_keys'] = []
    mem_key = {'diff':['COSMO_3.3_pgw{}'.format(pgw_mem_types[i]),
                        'COSMO_3.3_ctrl{}'.format(ctrl_mem_types[i])],
                        'label':'PGW - CTRL'}
    cfg['panels'][panel_key]['mem_keys'].append(
        mem_key
    )
    
    i += 1

#for mem_type in mem_types2:
#    ### CTRL
#    panel_key = '0,{}'.format(i)
#    cfg['panels'][panel_key] = {}
#    # members
#    cfg['panels'][panel_key]['mem_keys'] = []
#
#    ### EVAL
#    panel_key = '1,{}'.format(i)
#    cfg['panels'][panel_key] = {}
#    # members
#    cfg['panels'][panel_key]['mem_keys'] = []
#
#    ### PGW
#    panel_key = '2,{}'.format(i)
#    cfg['panels'][panel_key] = {}
#    cfg['panels'][panel_key]['i_recompute'] = 1
#    # members
#    cfg['panels'][panel_key]['mem_keys'] = []
#    mem_key = 'COSMO_3.3_pgw{}'.format(mem_type)
#    cfg['panels'][panel_key]['mem_keys'].append(
#        mem_key
#    )
#
#    ### PGW - CTRL
#    panel_key = '3,{}'.format(i)
#    cfg['panels'][panel_key] = {}
#    # members
#    cfg['panels'][panel_key]['mem_keys'] = []
#    mem_key = {'diff':['COSMO_3.3_pgw{}'.format(mem_type),
#                        'COSMO_3.3_ctrl{}'.format(mem_type[1:])],
#                        'label':'PGW - CTRL'}
#    cfg['panels'][panel_key]['mem_keys'].append(
#        mem_key
#    )
#
#    i += 1

#print(cfg['panels'])
#quit()
