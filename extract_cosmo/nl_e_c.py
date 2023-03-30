#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description:    Namelist for extract_case.py
author:         Christoph Heim
date created:   24.07.2019
date changed:   10.11.2021
usage:          arguments:
                1st:    n jobs for multiprocessing pool
                2nd:    case dictionary key 
"""
###############################################################################
import os, sys, argparse
from datetime import datetime, timedelta
from dateutil.relativedelta  import relativedelta
from nl_cases import cases
###############################################################################

# GENERAL SETTINGS
###########################################################################
# input and output directories
# TODO temporary
raw_data_dir = os.path.join('/scratch','snx3000','heimc','data','coarse_grain')
raw_data_dir = os.path.join('/scratch','snx3000','heimc','data','compr_cosmo')
raw_data_dir = os.path.join('/scratch','snx3000','heimc','data','compr_cosmo2')
out_base_dir = os.path.join('/scratch','snx3000','heimc',
                            'data','simulations')

## input arguments
parser = argparse.ArgumentParser(description = 'Draw spatial plots.')
# case key
parser.add_argument('case_key', type=str)
# number of parallel processes
parser.add_argument('-p', '--n_par', type=int, default=1)
# year
parser.add_argument('-y', '--year', type=int, default=2016)
# month
parser.add_argument('-m', '--month', type=int, default=None)
# month
parser.add_argument('-v', '--var_names', type=str, default=None)
args = parser.parse_args()


# set case specific values
case_dict       = cases[args.case_key]
model_name      = case_dict['model']
out_sim_name    = case_dict['sim_name']
inp_tag         = case_dict['inp_tag']
inp_sub_folder  = case_dict['sub_dir'] 
res             = case_dict['res'] 
#out_name        = nl_case_key


## box to subselect
#box = domain
#box['lon'] = slice(box['lon'].start, box['lon'].stop)
#box['lat'] = slice(box['lat'].start, box['lat'].stop)
box = None

###############################################################################
# take var_names from input argument
if args.var_names is not None:
    var_names = args.var_names.split(',')

#### 2D varnames
#var_names = ['SWNDTOA','SWDTOA','LWUTOA','CSWNDTOA','CLWUTOA',
#             'U10M','V10M','T2M',
#             'TSURF','SLHFLX','SSHFLX',
#             'CLCL','CLCM','CLCH',
#             'TQC','PP','TQI','TQR','TQG','TQS','TQV']
#### 3D varnames
#var_names = ['QC','QI','QV','T','U','V','W','P','QR','QG','QS']
#var_names = ['WSOIL']
###############################################################################

"""
COSMO 3.3:
    - 2D: 12 works
    - 3D: 12 works for extraction and 6 for compression.
COSMO 12:
    - 2D: 12 works
    - 3D: 12 works
"""

## date range
if args.month is None:
    start_month = 1
    end_month = 12
else:
    start_month = args.month
    end_month = args.month

####### TODO: tmp
if (args.year == 2006) and (args.month is None):
    start_month = 8
#end_month = 12

first_date = datetime(args.year,start_month,1)
last_date = datetime(args.year,end_month,1) + relativedelta(months=1) - timedelta(days=1)
#last_date = datetime(args.year,8,31)


#first_date = datetime(2008,1,1)
#last_date = datetime(2008,1,1)
#
#first_date = datetime(2006,9,1)
#last_date = datetime(2006,9,11)


print(args.month)
print(first_date)
print(last_date)
#quit()

i_debug=0


# options for computation
options = {}
# 03 COMPUTE VARS ON NATIVE TIME GRID
options['i_compute_native']         = 1
options['i_compute_daily']          = 1
options['i_compress']               = 2
# NOTE if not using full simulation range, don't apply lossy compression!
# lossy compression does so based on max/min values of the entire time
# series. If max/min change strongly between compression segments,
# there will be jumps in the values between segments (see e.g. TQC).
# i_compress = 1: conserving compression
# i_compress = 2: lossy compression

options['i_overwrite_native']       = 1
options['i_coarse_grain']           = 0
options['coarse_grid']              = os.path.join('grids','grid_SA_3_to_0.060')
options['fine_grid']                = os.path.join('grids','grid_SA_3')
#options['coarse_grid']              = os.path.join('grids','grid_SA_3_itcz_to_0.060')
#options['fine_grid']                = os.path.join('grids','grid_SA_3_itcz')
options['i_overwrite_daily']        = 1

## VARIABLE SETTINGS
############################################################################
coarse_grain_var_dict = {
    'on':[
        'SWNDTOA','SWDTOA','LWUTOA','CSWNDTOA','CLWUTOA',
        'LWNDSFC','LWDSFC','CLWDNSFC',
        'U10M','V10M','T2M',
        'TSURF','SLHFLX','SSHFLX',
        'CAPE','CIN',

        'QV','T','U','V','W','P',
        'QC','QI',
        ],
    'off':[
        'CLCL','CLCM','CLCH','CLCT',
        'TQC','PP','TQI','TQR','TQG','TQS','TQV',
        'WSOIL','TSOIL', # WSOIL needed for animation, and TSOIL problems with coarse graining

        #'QV','T','U','V','W','P',
        #'QC','QR','QG','QS','QI',
        #'QC','QI',
        ],
}

compress_var_dict = {
    '2':[
        'SWNDTOA','SWDTOA','LWUTOA','CSWNDTOA','CLWUTOA',
        'LWNDSFC','LWDSFC','CLWNDSFC',
        'U10M','V10M','T2M',
        'TSURF','SLHFLX','SSHFLX',
        'CAPE','CIN',
        'CLCL','CLCM','CLCH','CLCT',
        'TQC','PP','TQI','TQR','TQG','TQS','TQV',
        'QC','QI','T','U','V','W','QR','QG','QS',
        'TSOIL',
        ],
    '1':[
        'WSOIL','QV','P'
        ],

}

var_dict = {
    ### 3h_3D_zlev
    'U'         :{'folder':'3h_3D',         'dim':'3D', 'nc_end':'z'}, 
    'V'         :{'folder':'3h_3D',         'dim':'3D', 'nc_end':'z'}, 
    'W'         :{'folder':'3h_3D',         'dim':'3D', 'nc_end':'z'}, 
    'T'         :{'folder':'3h_3D',         'dim':'3D', 'nc_end':'z'}, 
    'P'         :{'folder':'3h_3D',         'dim':'3D', 'nc_end':'z'}, 
    'QV'        :{'folder':'3h_3D',         'dim':'3D', 'nc_end':'z'}, 
    'QG'        :{'folder':'3h_3D',         'dim':'3D', 'nc_end':'z'}, 
    'QS'        :{'folder':'3h_3D',         'dim':'3D', 'nc_end':'z'}, 
    'QR'        :{'folder':'3h_3D',         'dim':'3D', 'nc_end':'z'}, 
    'TKE'       :{'folder':'3h_3D',         'dim':'3D', 'nc_end':'z'}, 

    ### this is only for the BC files
    #'U'         :{'folder':'3h_3D_mlev',    'dim':'3D', 'nc_end':'z'}, 
    #'V'         :{'folder':'3h_3D_mlev',    'dim':'3D', 'nc_end':'z'}, 
    #'T'         :{'folder':'3h_3D_mlev',    'dim':'3D', 'nc_end':''}, 
    #'P'         :{'folder':'3h_3D_mlev',    'dim':'3D', 'nc_end':''}, 
    #'QV'        :{'folder':'3h_3D_mlev',    'dim':'3D', 'nc_end':'z'}, 
    #'W'         :{'folder':'3h_3D_mlev',    'dim':'3D', 'nc_end':'z'}, 

    ### 3h_3D_cloud
    'QC'        :{'folder':'3h_3D_cloud',   'dim':'3D', 'nc_end':'z'}, 
    'QI'        :{'folder':'3h_3D_cloud',   'dim':'3D', 'nc_end':'z'}, 

    ### 1h_2D_cg
    'U10M'      :{'folder':'1h_2D_cg',      'dim':'2D', 'nc_end':''}, 
    'V10M'      :{'folder':'1h_2D_cg',      'dim':'2D', 'nc_end':''}, 
    'T2M'       :{'folder':'1h_2D_cg',      'dim':'2D', 'nc_end':''}, 
    'RH2M'      :{'folder':'1h_2D_cg',      'dim':'2D', 'nc_end':''}, 
    'QV2M'      :{'folder':'1h_2D_cg',      'dim':'2D', 'nc_end':''}, 
    'PS'        :{'folder':'1h_2D_cg',      'dim':'2D', 'nc_end':''}, 
    'PMSL'      :{'folder':'1h_2D_cg',      'dim':'2D', 'nc_end':''}, 
    'TSURF'     :{'folder':'1h_2D_cg',      'dim':'2D', 'nc_end':''}, 
    'CAPE'      :{'folder':'1h_2D_cg',      'dim':'2D', 'nc_end':''}, 
    'CIN'       :{'folder':'1h_2D_cg',      'dim':'2D', 'nc_end':''}, 

    'SLHFLX'    :{'folder':'1h_2D_cg',      'dim':'2D', 'nc_end':''}, 
    'SSHFLX'    :{'folder':'1h_2D_cg',      'dim':'2D', 'nc_end':''}, 
    'SUMFLX'    :{'folder':'1h_2D_cg',      'dim':'2D', 'nc_end':''}, 
    'SVMFLX'    :{'folder':'1h_2D_cg',      'dim':'2D', 'nc_end':''}, 

    'SWNDTOA'   :{'folder':'1h_2D_cg',      'dim':'2D', 'nc_end':''}, 
    'SWDTOA'    :{'folder':'1h_2D_cg',      'dim':'2D', 'nc_end':''}, 
    'LWUTOA'    :{'folder':'1h_2D_cg',      'dim':'2D', 'nc_end':''}, 
    'CSWNDTOA'  :{'folder':'1h_2D_cg',      'dim':'2D', 'nc_end':''}, 
    'CLWUTOA'   :{'folder':'1h_2D_cg',      'dim':'2D', 'nc_end':''}, 
    'SWNDSFC'   :{'folder':'1h_2D_cg',      'dim':'2D', 'nc_end':''}, 
    'SWDIFDSFC' :{'folder':'1h_2D_cg',      'dim':'2D', 'nc_end':''}, 
    'SWDIRDSFC' :{'folder':'1h_2D_cg',      'dim':'2D', 'nc_end':''}, 
    #'SWDIFUSFC' :{'folder':'1h_2D_cg',      'dim':'2D', 'nc_end':''},  # not needed, can be derived from other vars
    'LWNDSFC'   :{'folder':'1h_2D_cg',      'dim':'2D', 'nc_end':''}, 
    'LWDSFC'    :{'folder':'1h_2D_cg',      'dim':'2D', 'nc_end':''}, 
    'CSWNDSFC'  :{'folder':'1h_2D_cg',      'dim':'2D', 'nc_end':''}, 
    'CLWNDSFC'  :{'folder':'1h_2D_cg',      'dim':'2D', 'nc_end':''}, 

    ### 1h_2D
    'TQR'       :{'folder':'1h_2D',         'dim':'2D', 'nc_end':''}, 
    'TQV'       :{'folder':'1h_2D',         'dim':'2D', 'nc_end':''}, 
    'TQG'       :{'folder':'1h_2D',         'dim':'2D', 'nc_end':''}, 
    'TQS'       :{'folder':'1h_2D',         'dim':'2D', 'nc_end':''}, 
    #'TQI'       :{'folder':'1h_2D',         'dim':'2D', 'nc_end':''}, 
    #'SWNDTOA'   :{'folder':'1h_2D',         'dim':'2D', 'nc_end':''}, 
    #'SWDTOA'    :{'folder':'1h_2D',         'dim':'2D', 'nc_end':''}, 
    #'LWUTOA'    :{'folder':'1h_2D',         'dim':'2D', 'nc_end':''}, 

    'CLCL'      :{'folder':'1h_2D',         'dim':'2D', 'nc_end':''}, 
    'CLCM'      :{'folder':'1h_2D',         'dim':'2D', 'nc_end':''}, 
    'CLCH'      :{'folder':'1h_2D',         'dim':'2D', 'nc_end':''}, 
    'CLCT'      :{'folder':'1h_2D',         'dim':'2D', 'nc_end':''}, 

    ### 30min_water
    'TQC'       :{'folder':'30min_water',   'dim':'2D', 'nc_end':''}, 
    'PP'        :{'folder':'30min_water',   'dim':'2D', 'nc_end':''}, 
    'TQI'       :{'folder':'30min_water',   'dim':'2D', 'nc_end':''}, 

    ### 24h
    'WSOIL'     :{'folder':'24h',           'dim':'2D', 'nc_end':''}, 
    'TSOIL'     :{'folder':'24h',           'dim':'2D', 'nc_end':''}, 
    'ALBSURF'   :{'folder':'24h',           'dim':'2D', 'nc_end':''}, 
    'RUNOFFG'   :{'folder':'24h',           'dim':'2D', 'nc_end':''}, 
    'RUNOFFS'   :{'folder':'24h',           'dim':'2D', 'nc_end':''}, 
    'TWATER'    :{'folder':'24h',           'dim':'2D', 'nc_end':''}, 
    'TWATFLXU'  :{'folder':'24h',           'dim':'2D', 'nc_end':''}, 
    'TWATFLXV'  :{'folder':'24h',           'dim':'2D', 'nc_end':''}, 
    'GUST10M'   :{'folder':'24h',           'dim':'2D', 'nc_end':''}, 
    'TMAX2M'    :{'folder':'24h',           'dim':'2D', 'nc_end':''}, 
    'TMIN2M'    :{'folder':'24h',           'dim':'2D', 'nc_end':''}, 

    ## soil spinup
    #'TQV'       :{'folder':'24h',           'dim':'2D', 'nc_end':''}, 
    #'TQC'       :{'folder':'24h',           'dim':'2D', 'nc_end':''}, 
    #'PP'        :{'folder':'24h',           'dim':'2D', 'nc_end':''}, 
}



inc_min = {
            # COSMO
            '3h_3D':180, '3h_3D_zlev':180, '3h_3D_cloud':180,
            '3h_3D_mlev':180, 
            '3h_2D':180,
            '1h_2D':60, '1h_2D_cg':60,
            '30min_water':30, '1h_water':60, 'mlev':60, '24h':1440,
            # ERA5
            'vars_ERA5':180}
###########################################################################

