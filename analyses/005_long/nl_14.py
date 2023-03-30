
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 14_anim:
author			Christoph Heim
date created    29.07.2021
date changed    29.04.2022
usage			import in another script
"""
###############################################################################
import os, subprocess, sys, argparse, dask
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import *
from base.nl_global import (plot_glob_base_dir, inp_glob_base_dir,
                               ana_glob_base_dir)
from base.nl_domains import *
from package.time_processing import Time_Processing as TP
#from package.functions import Var_Def
from nl_mem_src import *
from nl_var_src import set_up_var_src_dict, set_up_mean_var_src_dict
from nl_plot_14 import nlp
###############################################################################
## input arguments
parser = argparse.ArgumentParser(description = 'Draw spatial plots.')
## variable to plot
#parser.add_argument('var_name', type=str)
# number of parallel processes
parser.add_argument('-p', '--n_par', type=int, default=1)
# save or not? (0: show, 1: png, 2: pdf, 3: jpg)
parser.add_argument('-s', '--i_save_fig', type=int, default=3)
## recompute?
#parser.add_argument('-r', '--i_recompute', type=int, default=0)
args = parser.parse_args()

## paths
ana_name        = '005_long'
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name, '14_anim')
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)
pickle_dir      = os.path.join(ana_base_dir, '14')

## run settings
i_debug = 2
#i_plot = 1
#if args.i_recompute: i_plot = 0
#ref_mem_key = 'COSMO_3.3_large2'
#ref_src_dict = mem_src['pgw_ref']
i_skip_missing = 1

ANA_NATIVE_domain = dom_SA_3km_large3
plot_domain = dom_SA_3km_large3
#plot_domain = dom_SA_anim2
#plot_domain = dom_trades
##plot_domain = dom_lm_24_soil_spinup
##plot_domain = dom_SA_anim
##plot_domain = dom_gulf_anim
##plot_domain = dom_gulf_2

add_domain_boundaries = [
    #{'dom':dom_sim_tuning,          'color':'k',            'linestyle':'-'},
    #{'dom':dom_tuning,              'color':'red',         'linestyle':'-'},

    #{'dom':dom_SA_ana_sea,          'color':'black',        'linestyle':'-'},
    #{'dom':dom_SA_ana_merid_cs,     'color':'red',          'linestyle':'-'},

    #{'dom':dom_SA_ana_sea,          'color':'black',        'linestyle':'-'},
    #{'dom':dom_ITCZ,                'color':'red',          'linestyle':'-'},
    #{'dom':dom_trades_deep,         'color':'darkorange',   'linestyle':'-'},
    #{'dom':dom_trades_shallow,      'color':'yellow',       'linestyle':'-'},
    #{'dom':dom_SA_ana_merid_cs,     'color':'deepskyblue',  'linestyle':'-'},
    #{'dom':dom_SA_ana_merid_cs_afr, 'color':'deepskyblue',  'linestyle':'--'},

    {'dom':dom_SA_ana_sea,          'color':'black',        'linestyle':'-'},
    {'dom':dom_SA_ana_merid_cs,     'color':'red',          'linestyle':'-'},
    {'dom':dom_SA_ana_merid_cs_2,   'color':'darkorange',   'linestyle':'-'},
    {'dom':dom_trades_NA,           'color':'deepskyblue',  'linestyle':'--'},
    {'dom':dom_trades_full,         'color':'yellow',       'linestyle':'--'},
    #{'dom':dom_test,                'color':'yellow',       'linestyle':'--'},
    #{'dom':dom_trades_merid,        'color':'blue',         'linestyle':'-'},


    #{'dom':dom_ITCZ_feedback,       'color':'red',          'linestyle':'-'},
    #{'dom':dom_trades_west,         'color':'orange',       'linestyle':'-'},
    #{'dom':dom_trades_east,         'color':'yellow',       'linestyle':'-'},
]
#add_domain_boundaries = []

time_delta = timedelta(hours=0.5)
time_delta = timedelta(hours=24)

max_delta_search = timedelta(hours=24)
dt_initial_skip = timedelta(hours=0)

time_periods = []

#### domains papers
start_year = 2007
end_year = 2007
start_month = 6
end_month = 6
first_day = 3
last_day = 3

#start_year = 2006
#end_year = 2006
#start_month = 9
#end_month = 9
#first_day = 4
#last_day = 30


time_periods = [{'first_date':datetime(start_year,start_month,first_day),
                 'last_date':datetime(end_year,end_month,last_day)}]

plot_type = 'pcolormesh'

mem_keys = ['COSMO_3.3_ctrl']
#mem_keys = ['COSMO_3.3_pgw']
#mem_keys = ['COSMO_3.3_ctrl', 'COSMO_3.3_pgw3']
#mem_keys = ['COSMO_50_ctrl']
#mem_keys = ['COSMO_50_ctrl','COSMO_3.3_ctrl']

anim_name = '_domain_paper1'
anim_name = '_domain_paper2'
#anim_name = '_domain_diss_ChA'
#anim_name = ''

i_remove_axes = 0

i_plot_vars = 1
var_names = ['WSOIL','TQC','TQI','TQV','PP']
#var_names = ['WSOIL']
#var_names = ['WSOIL', 'QV2M']
#var_names = []

dask_chunks = None
#dask_chunks = {'lon':100,'lat':100}
#dask.config.set(num_workers=1, num_threads=1)

saturation = {
    0.005:  0.005,
    0.025:  0.014,
    0.07 :  0.028,
    0.16 :  0.057,
    0.34 :  0.114,
    0.7  :  0.228,
    1.47 :  0.504,
    2.86 :  0.850,
    5.74 :  2.010,
   11.5  :  3.720,
}
all_soil_levels = [0.005, 0.025, 0.07, 0.16, 0.34, 0.7, 1.47, 2.86, 5.74, 11.5]

soil_levels_grass = [0.005, 0.025, 0.07, 0.16, 0.34, 0.7]
#soil_levels_forest = [0.005, 0.025, 0.07, 0.16, 0.34, 0.7, 1.47, 2.86]
soil_levels_forest = [0.005, 0.025, 0.07, 0.16, 0.34, 0.7, 1.47, 2.86, 5.74]

land_plant_max_growth_sat_soil = 0.6
forest_plant_max_growth_sat_soil = 0.2 # 0.3

min_forest_greenness = 0.4

### set up var_src
var_src_dict = set_up_var_src_dict(inp_base_dir, ana_base_dir,
                                    ANA_NATIVE_domain)
mean_var_src_dict = set_up_mean_var_src_dict(inp_base_dir, ana_base_dir,
                                    ANA_NATIVE_domain)

var_cfgs = {
    'TQC':{
        'min_max':      (0,0.25), # orig
        'min_max':      (0,0.05), # TODO test
        'min_max':      (0,0.15), # TODO test2
        'min_max':      (0,0.15), # TODO test3
        #'min_max':      (0,0.10), # TODO test4
        #'min_max':      (0,0.10), # TODO test5
        #'min_max':      (0,0.10), # 
    },
    'TQV':{
        'min_max':      (0,50),
    },
    'TQI':{
        'min_max':      (0,0.2), # orig
        'min_max':      (0,0.1), # TODO test
        'min_max':      (0,0.15), # TODO test2
        'min_max':      (0,0.1), # TODO test3
        #'min_max':      (0,0.05), # TODO test4
        #'min_max':      (0,0.15), # TODO test5
    },
    'PP':{
        'min_max':      (0,50),
    },
    'WSOIL':{
        #'min_max'   :   (0,1.5),
        'min_max':      (None,None),
    },

    'QV2M':{
        'min_max':      (0,0.025),
    },
}

subplts = nlp['subplts_cfgs']['1x1']
nrows = 1
ncols = 1

#subplts = nlp['subplts_cfgs']['1x2']
#nrows = 1
#ncols = 2

## old plot size
#domain_aspect_ratio = 0.9505*plot_domain['nlon']/plot_domain['nlat']
##domain_aspect_ratio = 0.9515*plot_domain['nlon']/plot_domain['nlat']
#figsize = (3*domain_aspect_ratio,3)

## new plot size
fact = 1/600 # for 1 COSMO 3.3 simulation on full domain
figsize = (fact * (ncols * 1.00) * plot_domain['nlon'], 
           fact * nrows * plot_domain['nlat'])
## THIS IS FOR SERIOUS ANIMATION:
#figsize = (2560/600,1440/600)
#figsize = (3840/600,2160/600)

if int(figsize[0]*nlp['dpi']) % 2 != 0:
    #raise ValueError('figwidth is uneven number')
    figsize = (figsize[0]+1*fact, figsize[1])
if int(figsize[1]*nlp['dpi']) % 2 != 0:
    #raise ValueError('figheight is uneven number')
    figsize = (figsize[0], figsize[1]+1*fact)

print('figure width: {} px; figure height: {} px'.format(
                int(figsize[0]*nlp['dpi']),
                int(figsize[1]*nlp['dpi'])))


# get members dict
mem_src_dict = {}
for mem_key in mem_keys:
    mem_src_dict[mem_key] = mem_src[mem_key]

# update nlp
nlp['figsize']  = figsize 
