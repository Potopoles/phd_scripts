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

start_year = 2006
end_year = 2006
start_month = 8
end_month = 8
start_day = 1
end_day = 5

time_periods = [{'first_date':datetime(start_year,start_month,start_day),
                       'last_date':datetime(end_year,end_month,end_day)}]

time_periods_cmip6 = [{'first_date':datetime(1985,1,1),
                       'last_date':datetime(1985,12,31)},
                       #'last_date':datetime(2014,12,31)},
                       {'first_date':datetime(2070,1,1),
                       'last_date':datetime(2070,12,31)}
                       #'last_date':datetime(2099,12,31)}
                       ]

plot_domain = dom_SA_ana
#plot_domain = dom_SA_ana_sea
plot_domain = dom_ITCZ
plot_domain = dom_ITCZ_all

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


nrows = 4
ncols = 4

cosmo           = 'COSMO_3.3_ctrl'


var_name = 'W'
var_name = 'T'
#var_name = 'P'
#var_name = 'QI'
#var_name = 'POTT'
#var_name = 'QC'
#var_name = 'QV'
#var_name = 'QVFLXZ'
#var_name = 'QS'
#var_name = 'U'
#var_name = 'V'

plot_append = None

i_recompute = 0

bc_var_names = ['P','T','POTT','QV','U','V']

pgw_types = [
    #'pgw',
    #'pgw5',
    #None,
    #None,
    #'pgw10',
    #'pgw14',
    'pgw9',
    #'pgw11',
]


mem_types = {
    'pgw':['rdheight2', 'rdheight2_spubc1'],
    'pgw5':['rdheight2', 'rdheight2_spubc1'],
    #'pgw9':['rdheight2', 'rdheight2_spubc1'],
    'pgw9':['rdheight2_spubc1', 'rdheight2_spubc1_mlev'],
    #'pgw9':['rdheight2_spubc1_mlev'],
    'pgw10':['rdheight2'],
    'pgw11':['rdheight2', 'rdheight2_spubc1'],
    'pgw14':['rdheight2'],
}


print(var_name)

name_dict = {}
if plot_domain is not None:
    name_dict[plot_domain['key']] = var_name
else:
    name_dict['None'] = var_name
if plot_append is not None:
    name_dict[plot_append] = ''

cfg = {
    'serial_time_plt_sels': serial_time_plt_sels,
    'sub_dir':              'pr_eval_change_reduced',
    'name_dict':            name_dict,
    'figsize':              (nlp['figsize_lineplot']['{}x{}'.format(
                                    nrows,ncols).format(nrows,ncols)][0],
                             nlp['figsize_lineplot']['{}x{}'.format(
                                    nrows,ncols).format(nrows,ncols)][1]),
    'nrows':                nrows,
    'ncols':                ncols,
    'subplots_adjust_lineplot': 
                            '{}x{}'.format(nrows,ncols),
    'i_remove_axis_labels': 1,
    'i_add_panel_labels':   0,
    'arg_subplots_adjust':  {
                            },
    'all_panels':
        {
            'plot_append':  plot_append,
            'ana_number':   2,
            'var_names':    [var_name],
            'time_periods': time_periods,
            'agg_level':    agg_level,
            'plot_domain':  plot_domain,
            'i_recompute':  1,
        },
    'panels':
    {
    }
}


### PGW PANELS
row_ind = 0
col_ind = 0
for c,pgw_type in enumerate(pgw_types):
    
    # jump to next 2 columns on the right if this columns are full
    if row_ind > nrows - 1:
        col_ind += 2
        row_ind = 0

    if pgw_type is None:
        row_ind += 1
        continue

    print(pgw_type)

    deviation_members = []
    change_members = []

    mem_key_ctrl_bc = 'COSMO_3.3_ctrl_BC'
    mem_key_pgw_bc = 'COSMO_3.3_{}_BC'.format(pgw_type)



    for mem_type in mem_types[pgw_type]:
        ###### PGW - CTRL
        ##########################################################
        # CTRL member
        if mem_type == 'rdheight2':
            mem_key_ctrl = 'COSMO_3.3_ctrl_ref'
        elif mem_type == 'rdheight2_spubc1':
            mem_key_ctrl = 'COSMO_3.3_ctrl_rdheight2_spubc1'
        elif mem_type == 'rdheight2_spubc1_mlev':
            mem_key_ctrl = 'COSMO_3.3_ctrl_rdheight2_spubc1_mlev'

        # PGW member
        mem_key_pgw = 'COSMO_3.3_{}_{}'.format(pgw_type, mem_type)
        if (pgw_type == 'pgw') and mem_type == ('rdheight2'):
            mem_key_pgw = 'COSMO_3.3_{}_ref'.format(pgw_type)

        # create difference member entry
        diff = {'diff':[mem_key_pgw,mem_key_ctrl],}
        if i_recompute:
            diff = mem_key_pgw
        change_members.append(diff)

        if i_recompute and (c == 0):
            change_members.append(mem_key_ctrl)


        ###### PGW - CTRL - BC(PGW - CTRL)
        ##########################################################
        if var_name in bc_var_names:
            if not i_recompute:
                dev_bc = {'diff':[
                        {'diff':[mem_key_pgw, mem_key_ctrl],},
                        {'diff':[mem_key_pgw_bc, mem_key_ctrl_bc],},
                    ],}
                deviation_members.append(dev_bc)

    ###### BC(PGW - CTRL)
    ##########################################################
    if var_name in bc_var_names:
        diff_bc = {'diff':[mem_key_pgw_bc, mem_key_ctrl_bc],}
        if i_recompute:
            diff_bc = mem_key_pgw_bc
        change_members.append(diff_bc)

        if i_recompute and (c == 0):
            change_members.append(mem_key_ctrl_bc)

    # legend
    if pgw_type in ['pgw', 'pgw9']:
       plot_legend = True 
    else:
       plot_legend = False

    pan_key = '{},{}'.format(row_ind, col_ind)
    pan_dict = {
        #'i_recompute':  1,
        'title':        '$\Delta_{Model}$'+' (= {} - CTRL)'.format(pgw_type),
        'mem_keys':     change_members,
        'i_plot_legend':plot_legend,
    }
    cfg['panels'][pan_key] = pan_dict 

    pan_key = '{},{}'.format(row_ind, col_ind + 1)
    pan_dict = {
        'title':        '$\Delta_{Model}$ - $\Delta_{BC}$',
        'mem_keys':     deviation_members,
        'i_plot_legend':False,
    }
    if not i_recompute:
        cfg['panels'][pan_key] = pan_dict 

    row_ind += 1


for key,value in cfg['panels'].items():
    print(key)
    print(value)
#quit()
