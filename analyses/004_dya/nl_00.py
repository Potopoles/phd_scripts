#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 004_00_compute_fields:
author			Christoph Heim
date created    18.02.2020
date changed    23.03.2021
usage			import in another script
"""
###############################################################################
import os, subprocess, sys, warnings
from datetime import datetime, timedelta
from base.nl_global import (plot_glob_base_dir, inp_glob_base_dir,
                               ana_glob_base_dir)
from base.nl_domains import *
from nl_mem_src import *
from nl_var_src import set_up_var_src_dict
###############################################################################
## paths
ana_name        = '004_dyamond'
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)

## computation
njobs = 1
if len(sys.argv) > 1:
    njobs = int(sys.argv[1])

## analysis members
obs_src_dict = mem_src['obs']
sim_group = 'all_members'
#sim_group = 'cosmo'
#sim_group = 'sensitivity'
#sim_group = 'iav'
sim_src_dict = mem_src[sim_group]

## input arguments
## variable to compute
if len(sys.argv) > 2:
    var_name = sys.argv[2]
else:
    raise ValueError('second argument var_name not given.')
    pass
    #var_name = 'POTT'
i_use_obs   = 1
if len(sys.argv) > 3:
    use_sim_key = sys.argv[3]
    if use_sim_key == 'OBS':
        i_use_obs   = 1
        sim_src_dict = {}
    else:
        i_use_obs   = 0
        sim_src_dict = {use_sim_key:sim_src_dict[use_sim_key]}

####
#warnings.filterwarnings('error')
## do remapping step
i_remap     = 0
# do computation step
i_compute   = 1
i_debug     = 1
i_compress  = 2
time_mode = 'daily'
#time_mode = 'tmean'
if len(sys.argv) > 4:
    time_mode = sys.argv[4]
#i_coarse_grain = 50

## time
year=2016
if len(sys.argv) > 5:
    year = int(sys.argv[5])
first_date = datetime(year,8,1)
#first_date = datetime(year,8,6)
last_date = datetime(year,9,9)
#last_date = datetime(year,8,1)

#first_date = datetime(year,8,23)
#last_date = datetime(year,8,23)
#first_date = datetime(year,8,3)
#last_date = datetime(year,8,3)

#first_date = datetime(2006,8,1)
#last_date = datetime(2006,9,30)
#last_date = datetime(2006,12,31)


if i_remap:
    domain = dom_DYA_4km
    #domain = dom_SA_3km
else:
    domain = dom_SEA_Sc
    #domain = dom_iav_trades
    #domain = dom_DYA_4km
    #domain = dom_SA_3km
    #domain = dom_ERA5
#domain = dom_SEA_Sc_low
#domain = dom_SEA_Sc_high
#domain = dom_test

# remapping
#remap_padding = 3.0
remap_padding = 0.0
remap_dx = 45
#remap_dx = 100

### set up var_src
var_src_dict = set_up_var_src_dict(inp_base_dir, ana_base_dir)

var_cfg = {
    'U':                {'remap':0, 'obs':False},
    'V':                {'remap':0, 'obs':False},
    'UV':               {'remap':0, 'obs':False},
    'W':                {'remap':0, 'obs':False},
    'WTURB':            {'remap':0, 'obs':'ERA5_31'},
    #'WMEAN':            {'remap':0, 'obs':'ERA5_31'},
    'UVFLXDIV':         {'remap':0, 'obs':False},
    'UVFLXDIVNORMI':    {'remap':0, 'obs':False},
    'UVHCONV':          {'remap':0, 'obs':False},
    'UVHCONVMINV':      {'remap':0, 'obs':False},
    'WMBLI':            {'remap':0, 'obs':False},
    'WFLX':             {'remap':0, 'obs':False},
    'WFLXI':            {'remap':0, 'obs':False},
    'ENTR':             {'remap':0, 'obs':False},
    'ENTRH':            {'remap':0, 'obs':False},
    'ENTRV':            {'remap':0, 'obs':False},
    'UI':               {'remap':0, 'obs':False},
    'VI':               {'remap':0, 'obs':False},
    'WI':               {'remap':0, 'obs':False},
    'RHOI':             {'remap':0, 'obs':False},
    'UNORMI':           {'remap':0, 'obs':False},
    'VNORMI':           {'remap':0, 'obs':False},
    'UVNORMI':          {'remap':0, 'obs':False},
    'WNORMI':           {'remap':0, 'obs':False},
    'WTURBNORMI':       {'remap':0, 'obs':False},
    'WTURBNORMISCI':    {'remap':0, 'obs':False},
    'UVHCONVNORMI':     {'remap':0, 'obs':False},
    'WFLXMBLI':         {'remap':0, 'obs':False},
    'WFLXNORMI':        {'remap':0, 'obs':False},
    'LCLDMASK':         {'remap':0, 'obs':'ERA5_31'},
    'LCLDBASE':         {'remap':0, 'obs':'ERA5_31'},
    'LCLDBASENORMI':    {'remap':0, 'obs':'ERA5_31'},
    'LCLDTOP':          {'remap':0, 'obs':'ERA5_31'},
    'LCLDTOPNORMI':     {'remap':0, 'obs':'ERA5_31'},
    'LCLDDEPTH':        {'remap':0, 'obs':'ERA5_31'},
    'QV':               {'remap':0, 'obs':'ERA5_31'},
    'QVFT':             {'remap':0, 'obs':'ERA5_31'},
    'QVHDIV':           {'remap':0, 'obs':'ERA5_31'},
    'QVVDIV':           {'remap':0, 'obs':'ERA5_31'},
    'QC':               {'remap':0, 'obs':'ERA5_31'},
    'T':                {'remap':0, 'obs':'ERA5_31'},
    'P':                {'remap':0, 'obs':'ERA5_31'},
    'PNORMI':           {'remap':0, 'obs':'ERA5_31'},
    'H':                {'remap':0, 'obs':'ERA5_31'},
    'RHO':              {'remap':0, 'obs':'ERA5_31'},
    'TNORMI':           {'remap':0, 'obs':'ERA5_31'},
    'POTT':             {'remap':0, 'obs':'ERA5_31'},
    'POTTV':            {'remap':0, 'obs':'ERA5_31'},
    'POTTBL':           {'remap':0, 'obs':'ERA5_31'},
    'POTTFT':           {'remap':0, 'obs':'ERA5_31'},
    'POTTVFT':          {'remap':0, 'obs':'ERA5_31'},
    'POTTNORMI':        {'remap':0, 'obs':'ERA5_31'},
    'POTTMBLI':         {'remap':0, 'obs':'ERA5_31'},
    'POTTHDIV':         {'remap':0, 'obs':'ERA5_31'},
    'POTTHDIVNORMI':    {'remap':0, 'obs':'ERA5_31'},
    'POTTVDIV':         {'remap':0, 'obs':'ERA5_31'},
    'POTTVDIVNORMI':    {'remap':0, 'obs':'ERA5_31'},
    'DIABH':            {'remap':0, 'obs':'ERA5_31'},
    'DIABHNORMI':       {'remap':0, 'obs':'ERA5_31'},
    'POTTDIVMEAN':      {'remap':0, 'obs':'ERA5_31'},
    'POTTHDIVTURB':     {'remap':0, 'obs':'ERA5_31'},
    'POTTVDIVTURB':     {'remap':0, 'obs':'ERA5_31'},
    'POTTDIVTURB':      {'remap':0, 'obs':'ERA5_31'},
    'POTTHDIVTURBNORMI':{'remap':0, 'obs':'ERA5_31'},
    'POTTVDIVTURBNORMI':{'remap':0, 'obs':'ERA5_31'},
    'POTTDIVTURBNORMI': {'remap':0, 'obs':'ERA5_31'},
    'POTTHDIVMBLI':     {'remap':0, 'obs':'ERA5_31'},
    'POTTVDIVWPOS':     {'remap':0, 'obs':'ERA5_31'},
    'POTTVDIVWNEG':     {'remap':0, 'obs':'ERA5_31'},
    'DIABHMINV':        {'remap':0, 'obs':'ERA5_31'},
    'QVNORMI':          {'remap':0, 'obs':'ERA5_31'},
    'QCNORMI':          {'remap':0, 'obs':'ERA5_31'},
    'AW':               {'remap':0, 'obs':'ERA5_31'},
    'AWU':              {'remap':0, 'obs':'ERA5_31'},
    'AWD':              {'remap':0, 'obs':'ERA5_31'},
    'AWNORMI':          {'remap':0, 'obs':'ERA5_31'},
    'AWUNORMI':         {'remap':0, 'obs':'ERA5_31'},
    'AWDNORMI':         {'remap':0, 'obs':'ERA5_31'},
    'AWMBLI':           {'remap':0, 'obs':'ERA5_31'},
    'KEW':              {'remap':0, 'obs':'ERA5_31'},
    'KEWNORMI':         {'remap':0, 'obs':'ERA5_31'},
    'KEWMBLI':          {'remap':0, 'obs':'ERA5_31'},
    'TKE':              {'remap':0, 'obs':'ERA5_31'},
    'TKEMBLI':          {'remap':0, 'obs':'ERA5_31'},
    'SUBS':             {'remap':0, 'obs':'ERA5_31'},
    # for remapping of SWDTOA reference (for comp. of SWUTOA from SWNDTOA)
    'SWDTOA':           {'remap':1, 'obs':'CM_SAF_MSG_AQUA_TERRA'},
    'SWUTOA':           {'remap':1, 'obs':'CM_SAF_MSG_AQUA_TERRA'},
    'LWUTOA':           {'remap':1, 'obs':'CM_SAF_MSG_AQUA_TERRA'},
    'ALBEDO':           {'remap':1, 'obs':'CM_SAF_MSG_AQUA_TERRA'},
    #'SWDTOA':           {'remap':1, 'obs':'CM_SAF_METEOSAT'},
    #'SWUTOA':           {'remap':1, 'obs':'CM_SAF_METEOSAT'},
    #'LWUTOA':           {'remap':1, 'obs':'CM_SAF_METEOSAT'},
    #'ALBEDO':           {'remap':1, 'obs':'CM_SAF_METEOSAT'},
    #'INVHGT':           {'remap':0, 'obs':'RADIO_SOUNDING'},
    'INVHGT':           {'remap':0, 'obs':'ERA5_31'},
    'LTS':              {'remap':0, 'obs':'ERA5_31'},
    'LCL':              {'remap':0, 'obs':'ERA5_31'},
    'DCLDBASELCL':      {'remap':0, 'obs':'ERA5_31'},
    'DCLDTOPINVHGT':    {'remap':0, 'obs':'ERA5_31'},
    'DINVHGTLCL':       {'remap':0, 'obs':'ERA5_31'},
    'PVAPSATL':         {'remap':0, 'obs':'ERA5_31'},
    'PVAP':             {'remap':0, 'obs':'ERA5_31'},
    'RHL':              {'remap':0, 'obs':'ERA5_31'},
    'INVSTR':           {'remap':0, 'obs':'ERA5_31'},
    'INVSTRV':          {'remap':0, 'obs':'ERA5_31'},
    'INVSTRA':          {'remap':0, 'obs':'ERA5_31'},
    'CLDHGT':           {'remap':0, 'obs':'ERA5_31'},
    'TQV':              {'remap':0, 'obs':'CM_SAF_HTOVS'},
    'TQVFT':            {'remap':0, 'obs':'ERA5_31'},
    'DTQVI':            {'remap':0, 'obs':'ERA5_31'},
    'QVFLXZ':           {'remap':0, 'obs':False},
    'QVFLXZI':           {'remap':0, 'obs':False},
    'QVFLXZCB':         {'remap':0, 'obs':False},
    'PP':               {'remap':0, 'obs':False},
    'CLCL':             {'remap':0, 'obs':'CM_SAF'},
    'CLCL2':            {'remap':0, 'obs':'CM_SAF'},
    #'TQC':              {'remap':1, 'obs':False},
    'TQI':              {'remap':1, 'obs':'CM_SAF_MSG'},
    'V10M_S':           {'remap':0, 'obs':'ERA5_31'},
    'U10M':             {'remap':1, 'obs':'ERA5_31'},
    'V10M':             {'remap':1, 'obs':'ERA5_31'},
}



# check for bad namelist settings
if (len(sim_src_dict) > 1) or (len(sim_src_dict) == 1 and i_use_obs):
    if time_mode == 'tmean':
        raise NotImplementedError('time_mode tmean not implemented for '+
                                'multiple simulations at the same time.')
