import os, sys
import numpy as np
from pathlib import Path
from datetime import datetime,timedelta
from package.domains import dom_alpine_region, dom_northern_italy

base_dir = os.path.join('/net','o3','hymet_nobackup','heimc')
data_inp_dir = os.path.join(base_dir, 'MScTh', '01_rawData', 'topocut')
# BASE PATHS
ana_dir     = os.path.join(base_dir, 'analyses', '003_MScTh')
plot_dir    = os.path.join(base_dir, 'plots', '003_MScTh') 
inp_dir     = os.path.join(ana_dir, 'inp_data')
out_dir     = os.path.join(ana_dir, 'out_data')


    

update_steps = {}

sim_name = 'MScTh'

use_members = ['RAW4', 'SM4', 'RAW2', 'SM2', 'RAW1', 'SM1']
#use_members = ['RAW2', 'SM2', 'RAW1', 'SM1']
#use_members = ['RAW2', 'SM2', 'RAW1', 'SM1']
#use_members = ['SM2', 'RAW1', 'SM1']
#use_members = ['RAW4', 'RAW2', 'RAW1']
#use_members = ['SM4', 'SM2', 'SM1']
#use_members = ['RAW4', 'SM4']
#use_members = ['RAW1', 'SM1']
#use_members = ['RAW4']

i_save_fig = 0
i_debug = 0
i_plot = 0

first_date = datetime(2006,7,11,0)
last_date = datetime(2006,7,20,00)
#last_date = datetime(2006,7,11,1)

######### 02 calc wvp
calc_var = 'WVP'
#calc_var = 'LWP'
#height_lims = (0,10000)
#height_lims = (0,2000)
#height_lims = (0,4000)
#height_lims = (2000,4000)
height_lims = (2000,10000)
#height_lims = (4000,10000)
#########

######### 03 calc spectra
# CALCULATE SPECTRA
var_names = ['QC', 'W']
var_names = ['W']
#diurn_hrs = np.arange(10,15,1)
#title_time = '1000-1500 UTC'
#diurn_hrs = np.append(np.arange(10,24,1),0) 
#title_time = '1000-2400 UTC'
#diurn_hrs = np.arange(0,5,1)
#title_time = '0000-0500 UTC'
#diurn_hrs = np.arange(5,10,1)
#title_time = '0500-1000 UTC'
diurn_hrs = np.arange(0,24,1)
title_time = '0000-2400 UTC'
altitudes = [1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]
altitudes = [4000]
domain_03 = dom_alpine_region
i_recompute = 0
# PLOT SPECTRA
plot_var = 'W'
cols = {4400:'black',2200:'blue',1100:'red'}
#########

######### 05 plot EQPOTT
_05 = {
    #'domain':       dom_alpine_region,
    #'day_time':     [10,11,12],
    'domain':       dom_northern_italy,
    'day_time':     [10,11,12],
}
#########

######### 06 FQV
_06 = {
    'direction':'x',
    'direction':'y'
    #'direction':'z'
}
#########


######### 08 calc bulk tendencies
_08 = {
    'domain':       dom_alpine_region,
    'altitudes':    slice(0,2500),
    #'altitudes':    slice(0,8000),
}
#########



## TEST: 12 cores: 1 ts / 4 ts 01_RHO -- 1/4 ts 02_WVP
# 15/54 -- /8.75 s:

#chunks={'rlat':500,'rlon':500}
# 18 sec s:
#chunks={'rlat':300,'rlon':300}
# 24 sec s:
#chunks={'rlat':200,'rlon':200}
# 42 sec s:
#chunks={'rlat':100,'rlon':100}
# 11.5/15.7 -- 7.2 s:
#chunks={'time':1}
# 12.5/15.0 -- /7 s:
chunks={}



# ANALYSIS MEMBERS
member_dicts = {
    'RAW4': {
        'label':    'RAW4',
        'smooth':   False,
        #'inp_path': os.path.join(base_dir, 'data','cosmo_out',
        #                'MScTh','01_rawData','topocut','RAW4'),
        'inp_path': os.path.join(data_inp_dir,'RAW4'),
        'dt':       'hourly',
        'dx':       4400,
    },

    'SM4': {
        'label':    'SM4',
        'smooth':   True,
        #'inp_path': os.path.join(base_dir, 'data','cosmo_out',
        #                'MScTh','01_rawData','topocut','SM4'),
        'inp_path': os.path.join(data_inp_dir,'SM4'),
        'dt':       'hourly',
        'dx':       4400,
    },

    'RAW2': {
        'label':    'RAW2',
        'smooth':   False,
        #'inp_path': os.path.join(base_dir, 'data','cosmo_out',
        #                'MScTh','01_rawData','topocut','RAW2'),
        'inp_path': os.path.join(data_inp_dir,'RAW2'),
        'dt':       'hourly',
        'dx':       2200,
    },

    'SM2': {
        'label':    'SM2',
        'smooth':   True,
        #'inp_path': os.path.join(base_dir, 'data','cosmo_out',
        #                'MScTh','01_rawData','topocut','SM2'),
        'inp_path': os.path.join(data_inp_dir,'SM2'),
        'dt':       'hourly',
        'dx':       2200,
    },

    'RAW1': {
        'label':    'RAW1',
        'smooth':   False,
        #'inp_path': os.path.join(base_dir, 'data','cosmo_out',
        #                'MScTh','01_rawData','topocut','RAW1'),
        'inp_path': os.path.join(data_inp_dir,'RAW1'),
        'dt':       'hourly',
        'dx':       1100,
    },

    'SM1': {
        'label':    'SM1',
        'smooth':   True,
        #'inp_path': os.path.join(base_dir, 'data','cosmo_out',
        #                'MScTh','01_rawData','topocut','SM1'),
        'inp_path': os.path.join(data_inp_dir,'SM1'),
        'dt':       'hourly',
        'dx':       1100,
    },

}


# CREATE MEMBER SUBDIRECTORIES
for key in member_dicts:
    member_dicts[key]['inp_dir'] = Path(os.path.join(inp_dir,key))
    member_dicts[key]['inp_dir'].mkdir(parents=True, exist_ok=True)
    member_dicts[key]['out_dir'] = Path(os.path.join(out_dir,key))
    member_dicts[key]['out_dir'].mkdir(parents=True, exist_ok=True)
