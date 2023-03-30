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
start_year = 2007
end_year = 2009
start_month = 1
end_month = 12
start_day = 1
end_day = 31

start_year = 2007
end_year = 2007
start_month = 1
end_month = 10
start_day = 1
end_day = 31

time_periods_cosmo = [{'first_date':datetime(start_year,start_month,start_day),
                       'last_date':datetime(end_year,end_month,end_day)}]

time_periods_cmip6 = [{'first_date':datetime(1985,1,1),
                       'last_date':datetime(2014,12,31)},
                      {'first_date':datetime(2070,1,1),
                       'last_date':datetime(2099,12,31)},
                       ]

#time_periods_ceres = [{'first_date':datetime(2004,1,1),
#                       'last_date':datetime(2014,1,31)},
#                       ]


plot_domain = dom_SA_ana_sea
#plot_domain = dom_SA_ana_land
#plot_domain = dom_global

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



ACCESS_CM2      = 'ACCESS-CM2'
ACCESS_ESM1_5   = 'ACCESS-ESM1-5'
AWI_CM_1_1_MR   = 'AWI-CM-1-1-MR'
CAMS_CSM1_0     = 'CAMS-CSM1-0'
CanESM5         = 'CanESM5'
CESM2           = 'CESM2'
CESM2_WACCM     = 'CESM2-WACCM'
CMCC_ESM2       = 'CMCC-ESM2'
CMCC_CM2_SR5    = 'CMCC-CM2-SR5'
CNRM_CM6_1      = 'CNRM-CM6-1'
CNRM_CM6_1_HR   = 'CNRM-CM6-1-HR'
CNRM_ESM2_1     = 'CNRM-ESM2-1'
E3SM_1_1        = 'E3SM-1-1'
EC_Earth3       = 'EC-Earth3'
EC_Earth3_CC    = 'EC-Earth3-CC'
EC_Earth3_Veg   = 'EC-Earth3-Veg'
FGOALS_f3_L     = 'FGOALS-f3-L'
FGOALS_g3       = 'FGOALS-g3'
GFDL_CM4        = 'GFDL-CM4'
GFDL_ESM4       = 'GFDL-ESM4'
GISS_E2_1_G     = 'GISS-E2-1-G'
HadGEM3_GC31_LL = 'HadGEM3-GC31-LL'
INM_CM4_8       = 'INM-CM4-8'
INM_CM5_0       = 'INM-CM5-0'
IPSL_CM6A_LR    = 'IPSL-CM6A-LR'
MIROC6          = 'MIROC6'
MIROC_ES2L      = 'MIROC-ES2L'
MPI_ESM1_2_HR   = 'MPI-ESM1-2-HR'
MPI_ESM1_2_LR   = 'MPI-ESM1-2-LR'
MRI_ESM2_0      = 'MRI-ESM2-0'
NorESM2_LM      = 'NorESM2-LM'
NorESM2_MM      = 'NorESM2-MM'
TaiESM1         = 'TaiESM1'
UKESM1_0_LL     = 'UKESM1-0-LL'

cosmo           = 'COSMO_3.3_ctrl'
#cosmo           = 'ERA5'


#models_cmip6 = models_cmip6[0]
#if not isinstance(models_cmip6, list):
#    models_cmip6 = [models_cmip6]
#print(models_cmip6)


nmodels = len(models_cmip6) + 2
ncols = int(np.ceil(np.sqrt(nmodels)))
nrows = int(np.ceil(nmodels / ncols))

i = 0
i_recompute = {
    cosmo               :1,
    ACCESS_CM2          :i,
    ACCESS_ESM1_5       :i,
    AWI_CM_1_1_MR       :i,
    CAMS_CSM1_0         :i,
    CanESM5             :i,
    CESM2               :i,
    CESM2_WACCM         :i,
    CMCC_CM2_SR5        :i,
    CMCC_ESM2           :i,
    CNRM_CM6_1          :i,
    CNRM_CM6_1_HR       :i,
    CNRM_ESM2_1         :i,
    E3SM_1_1            :i,
    EC_Earth3           :i,
    EC_Earth3_CC        :i,
    EC_Earth3_Veg       :i,
    FGOALS_f3_L         :i,
    FGOALS_g3           :i,
    GFDL_CM4            :i,
    GFDL_ESM4           :i,
    GISS_E2_1_G         :i,
    HadGEM3_GC31_LL     :i,
    INM_CM5_0           :i,
    INM_CM4_8           :i,
    IPSL_CM6A_LR        :i,
    MIROC_ES2L          :i,
    MIROC6              :i,
    MPI_ESM1_2_HR       :i,
    MPI_ESM1_2_LR       :i,
    MRI_ESM2_0          :i,
    NorESM2_LM          :i,
    NorESM2_MM          :i,
    TaiESM1             :i,
    UKESM1_0_LL         :i,
}


var_name = 'SWNDTOA'
var_name = 'LWUTOA'
var_name = 'CSWNDTOA'
var_name = 'CLWUTOA'
var_name = 'CRELWUTOA'
var_name = 'CRESWNDTOA'
var_name = 'CRERADNDTOA'
var_name = 'T2M'
var_name = 'UV10M'
var_name = 'SUBSOMEGA'
#var_name = 'LTS'
#var_name = 'QVFT'

mode = 'abs'
mode = 'eval'

if mode == 'eval':
    time_periods_cmip6 = time_periods_cosmo

###TODO
#time_periods_cmip6 = time_periods_cosmo

print(var_name)


if var_name in [
    'SWNDTOA',
    'LWUTOA',
    'CSWNDTOA',
    'CLWUTOA',
    'CRELWUTOA',
    'CRESWNDTOA',
    'CRERADNDTOA']:
    obs             = 'CERES_EBAF'
else:
    obs             = 'ERA5'

name_dict = {}
if plot_domain is not None:
    name_dict[plot_domain['key']] = var_name
else:
    name_dict['None'] = var_name
name_dict[agg_level] = mode

cfg = {
    'serial_time_plt_sels': serial_time_plt_sels,
    'sub_dir':              'sp_eval_cmip6',
    'name_dict':            name_dict,
    'figsize':              (nlp['figsize_spatial']['{}x{}'.format(
                                    nrows,ncols).format(nrows,ncols)][0],
                             nlp['figsize_spatial']['{}x{}'.format(
                                    nrows,ncols).format(nrows,ncols)][1]),
    'nrows':                nrows,
    'ncols':                ncols,
    'subplots_adjust':      '{}x{}'.format(nrows,ncols),
    'i_remove_axis_labels': 2,
    'i_add_panel_labels':   0,
    'arg_subplots_adjust':  {
                            },
    'all_panels':
        {
            'ana_number':   1,
            'var_names':    [var_name],
            'time_periods': time_periods_cmip6,
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
        '0,0':
        {
            'i_recompute':  i_recompute[cosmo],
            'time_periods': time_periods_cosmo,
        },
    }
}

mod_ind = 0
for row_ind in range(nrows):
    for col_ind in range(ncols):
        if (col_ind == 0) and (row_ind == 0):
            if mode == 'abs':
                cfg['panels']['0,0']['mem_keys'] = [cosmo]
            elif mode == 'eval':
                cfg['panels']['0,0']['mem_keys'] = [{'diff':[cosmo,obs]}]
            else:
                raise NotImplementedError()

        elif (col_ind == 1) and (row_ind == 0):
            diffs = []
            for model_key in models_cmip6:
                if mode == 'abs':
                    diffs.append('{}_historical'.format(model_key))
                elif mode == 'eval':
                    diffs.append({'diff':['{}_historical'.format(model_key),
                                          obs]})
                else:
                    raise NotImplementedError()


            cfg['panels']['{},{}'.format(row_ind, col_ind)] = {
                'mem_keys':     [{'mean':diffs}]
            }
        else:
            if mod_ind < len(models_cmip6):
                model_key = models_cmip6[mod_ind]
                panel = {}
                panel['i_recompute'] = i_recompute[model_key]
                if mode == 'abs':
                    panel['mem_keys'] = ['{}_historical'.format(model_key)]
                elif mode == 'eval':
                    panel['mem_keys'] = [{'diff':['{}_historical'.format(model_key),
                                              obs]}]
                else:
                    raise NotImplementedError()
                cfg['panels']['{},{}'.format(row_ind, col_ind)] = panel

                mod_ind += 1


#print(cfg['panels'])
#quit()
