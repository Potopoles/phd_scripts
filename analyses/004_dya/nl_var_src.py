#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     All variables that are used in the analyses and how they
                should be treated (derived or directly loaded)
author			Christoph Heim
date created    07.09.2020
date changed    04.02.2021
usage           use in another script
"""
###############################################################################
import os
from package.var_pp import DERIVE, DIRECT
###############################################################################

INPUT = 'INPUT'
ANA_NATIVE = 'ANA_NATIVE'
ANA_REMAPPED_45 = 'ANA_REMAPPED_45'

###############################################################################
## MAIN VARIABLES
###############################################################################
mode_step_1 = DIRECT
mode_step_2 = DIRECT
mode_step_3 = DIRECT
mode_step_5 = DIRECT
var_src = {
    # step 1
    'LWUTOA':           {'load':mode_step_1, 'src':ANA_REMAPPED_45},
    'SWDOTA':           {'load':mode_step_1, 'src':ANA_REMAPPED_45},
    'SWUTOA':           {'load':mode_step_1, 'src':ANA_REMAPPED_45},
    'TQI':              {'load':mode_step_1, 'src':ANA_REMAPPED_45},

    # step 2
    'ALBEDO':           {'load':mode_step_2, 'src':ANA_REMAPPED_45},
    'INVHGT':           {'load':mode_step_2, 'src':ANA_NATIVE},
    'POTT':             {'load':mode_step_2, 'src':ANA_NATIVE},
    'RHO':              {'load':mode_step_2, 'src':ANA_NATIVE},

    # step 3
    'UVFLXDIV':         {'load':mode_step_3, 'src':ANA_NATIVE},
    'ENTR':             {'load':mode_step_3, 'src':ANA_NATIVE},
    'POTTVDIV':         {'load':mode_step_3, 'src':ANA_NATIVE},
    'POTTHDIV':         {'load':mode_step_3, 'src':ANA_NATIVE},
    'TNORMI':           {'load':mode_step_3, 'src':ANA_NATIVE},
    'QCNORMI':          {'load':mode_step_3, 'src':ANA_NATIVE},
    'QVNORMI':          {'load':mode_step_3, 'src':ANA_NATIVE},
    'WNORMI':           {'load':mode_step_3, 'src':ANA_NATIVE},
    'AWNORMI':          {'load':mode_step_3, 'src':ANA_NATIVE},
    'POTTVDIVWPOS':     {'load':mode_step_3, 'src':ANA_NATIVE},
    'POTTVDIVWNEG':     {'load':mode_step_3, 'src':ANA_NATIVE},
    'TQV':              {'load':mode_step_3, 'src':ANA_NATIVE},
    'INVSTR':           {'load':mode_step_3, 'src':ANA_NATIVE},
    'INVSTRV':          {'load':mode_step_3, 'src':ANA_NATIVE},

    # step 4: computation of mean inherits from above

    # now run Reynolds.

    # step 5
    'UVFLXDIVNORMI':    {'load':mode_step_5, 'src':ANA_NATIVE},
    'DIABHNORMI':       {'load':mode_step_5, 'src':ANA_NATIVE},
    'POTTHDIVTURBNORMI':{'load':mode_step_5, 'src':ANA_NATIVE},
    'POTTVDIVTURBNORMI':{'load':mode_step_5, 'src':ANA_NATIVE},
    'POTTDIVTURBNORMI': {'load':mode_step_5, 'src':ANA_NATIVE},
    'POTTHDIVNORMI':    {'load':mode_step_5, 'src':ANA_NATIVE},
    'POTTVDIVNORMI':    {'load':mode_step_5, 'src':ANA_NATIVE},

    ####### remaining variables
    'WTURB':            {'load':DERIVE, 'src':ANA_NATIVE},
    'WTURBNORMI':       {'load':DERIVE, 'src':ANA_NATIVE},
    'WTURBNORMISCI':    {'load':DERIVE, 'src':ANA_NATIVE},
    'WMEAN':            {'load':DIRECT, 'src':ANA_NATIVE},
    'UI':               {'load':DERIVE, 'src':ANA_NATIVE},
    'VI':               {'load':DERIVE, 'src':ANA_NATIVE},
    'WI':               {'load':DERIVE, 'src':ANA_NATIVE},
    'INVSTR':           {'load':DIRECT, 'src':ANA_NATIVE},
    'POTTBL':           {'load':DIRECT, 'src':ANA_NATIVE},
    'POTTFT':           {'load':DIRECT, 'src':ANA_NATIVE},
    'POTTVFT':          {'load':DIRECT, 'src':ANA_NATIVE},
    'QVFT':             {'load':DIRECT, 'src':ANA_NATIVE},
    'LTS':              {'load':DERIVE, 'src':ANA_NATIVE},
    'SUBS':             {'load':DERIVE, 'src':ANA_NATIVE},
    'ENTRV':            {'load':DERIVE, 'src':ANA_NATIVE},
    'ENTRH':            {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTHDIVMBLI':     {'load':DIRECT, 'src':ANA_NATIVE},
    'POTTMBLI':         {'load':DIRECT, 'src':ANA_NATIVE},
    'TQVFT':            {'load':DERIVE, 'src':ANA_NATIVE},
    'LCLDMASK':         {'load':DIRECT, 'src':ANA_NATIVE},
    'LCLDBASE':         {'load':DERIVE, 'src':ANA_NATIVE},
    'LCLDTOP':          {'load':DIRECT, 'src':ANA_NATIVE},
    'LCLDDEPTH':        {'load':DIRECT, 'src':ANA_NATIVE},
    'LCL':              {'load':DIRECT, 'src':ANA_NATIVE},
    'DCLDBASELCL':      {'load':DIRECT, 'src':ANA_NATIVE},
    'DCLDTOPINVHGT':    {'load':DIRECT, 'src':ANA_NATIVE},
    'DINVHGTLCL':       {'load':DIRECT, 'src':ANA_NATIVE},
    'PVAP':             {'load':DERIVE, 'src':ANA_NATIVE},
    'PVAPSATL':         {'load':DERIVE, 'src':ANA_NATIVE},
    'RHL':              {'load':DIRECT, 'src':ANA_NATIVE},
    'RHLNORMI':         {'load':DERIVE, 'src':ANA_NATIVE},
    'HSURF':            {'load':DIRECT, 'src':INPUT},
    'POTTV':            {'load':DERIVE, 'src':ANA_NATIVE},
    'TV':               {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTNORMI':        {'load':DERIVE, 'src':ANA_NATIVE},
    'LCLDBASENORMI':    {'load':DERIVE, 'src':ANA_NATIVE},
    'LCLDTOPNORMI':     {'load':DERIVE, 'src':ANA_NATIVE},
    'TSURF':            {'load':DIRECT, 'src':INPUT},
    'SLHFLX':           {'load':DERIVE, 'src':INPUT},
    'SSHFLX':           {'load':DERIVE, 'src':INPUT},
    'CORREFL':          {'load':DERIVE, 'src':INPUT},
    'DIABH':            {'load':DERIVE, 'src':ANA_NATIVE},
    'AW':               {'load':DERIVE, 'src':ANA_NATIVE},
    'WFLX':             {'load':DERIVE, 'src':ANA_NATIVE},
    'U':                {'load':DERIVE, 'src':INPUT},
    'UNORMI':           {'load':DERIVE, 'src':ANA_NATIVE},
    'V':                {'load':DERIVE, 'src':INPUT},
    'VNORMI':           {'load':DERIVE, 'src':ANA_NATIVE},
    'UV':               {'load':DERIVE, 'src':INPUT},
    'UVNORMI':          {'load':DIRECT, 'src':ANA_NATIVE},
    'UVHCONVMINV':      {'load':DERIVE, 'src':ANA_NATIVE},
    'W':                {'load':DIRECT, 'src':INPUT},
    'WMBLI':            {'load':DERIVE, 'src':ANA_NATIVE},
    'WFLXNORMI':        {'load':DERIVE, 'src':ANA_NATIVE},
    'T':                {'load':DIRECT, 'src':INPUT},
    'POTTHDIVMEAN':     {'load':DIRECT, 'src':ANA_NATIVE},
    'POTTVDIVMEAN':     {'load':DIRECT, 'src':ANA_NATIVE},
    'POTTDIVMEAN':      {'load':DIRECT, 'src':ANA_NATIVE},
    'POTTHDIVMEANNORMI':{'load':DIRECT, 'src':ANA_NATIVE},
    'POTTVDIVMEANNORMI':{'load':DIRECT, 'src':ANA_NATIVE},
    'POTTDIVMEANNORMI': {'load':DIRECT, 'src':ANA_NATIVE},
    'POTTHDIVTURB':     {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTVDIVTURB':     {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTDIVTURB':      {'load':DERIVE, 'src':ANA_NATIVE},
    'DIABHMINV':        {'load':DERIVE, 'src':ANA_NATIVE},
    'P':                {'load':DIRECT, 'src':INPUT},
    'PNORMI':           {'load':DERIVE, 'src':ANA_NATIVE},
    'ALT':              {'load':DERIVE, 'src':INPUT},
    'QV':               {'load':DERIVE, 'src':INPUT},
    'QC':               {'load':DERIVE, 'src':INPUT},
    'AWU':              {'load':DERIVE, 'src':ANA_NATIVE},
    'AWD':              {'load':DERIVE, 'src':ANA_NATIVE},
    #'AWUNORMI':         {'load':DERIVE, 'src':ANA_NATIVE},
    #'AWDNORMI':         {'load':DERIVE, 'src':ANA_NATIVE},
    'AWMBLI':           {'load':DERIVE, 'src':ANA_NATIVE},
    'KEW':              {'load':DIRECT, 'src':ANA_NATIVE},
    'KEWNORMI':         {'load':DERIVE, 'src':ANA_NATIVE},
    'KEWMBLI':          {'load':DERIVE, 'src':ANA_NATIVE},
    'TKEMBLI':          {'load':DERIVE, 'src':ANA_NATIVE},
    'TKE':              {'load':DERIVE, 'src':INPUT},
    'CLCL':             {'load':DERIVE, 'src':INPUT},
    'CLCL2':            {'load':DERIVE, 'src':INPUT},
    'CLCT':             {'load':DIRECT, 'src':INPUT},
    'PS':               {'load':DERIVE, 'src':INPUT},
    'SWNDTOA':          {'load':DIRECT, 'src':ANA_REMAPPED_45},
    'SWDTOA':           {'load':DIRECT, 'src':ANA_REMAPPED_45},
    'INVSTRA':          {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDHGT':           {'load':DERIVE, 'src':ANA_NATIVE},
    'QVFLXZ':           {'load':DERIVE, 'src':ANA_NATIVE},
    'QVFLXZCB':         {'load':DERIVE, 'src':ANA_NATIVE},
    'PP':               {'load':DERIVE, 'src':INPUT},
    'TQC':              {'load':DIRECT, 'src':INPUT},
    'PPCONV':           {'load':DIRECT, 'src':INPUT},
    'PPGRID':           {'load':DIRECT, 'src':INPUT},
    'UV10M':            {'load':DERIVE, 'src':INPUT},
    'U10M_W':           {'load':DERIVE, 'src':INPUT},
    'U10M_E':           {'load':DERIVE, 'src':INPUT},
    'U10M':             {'load':DIRECT, 'src':INPUT},
    'V10M':             {'load':DIRECT, 'src':INPUT},
    #'U10M':             {'load':DIRECT, 'src':ANA_REMAPPED_45},
    #'V10M':             {'load':DIRECT, 'src':ANA_REMAPPED_45},
    'V10M_S':           {'load':DERIVE, 'src':INPUT},
    'V10M_N':           {'load':DERIVE, 'src':INPUT},

    # MEAN VARIABLES
    'U_tmean':          {'load':DIRECT, 'src':ANA_NATIVE},
    'V_tmean':          {'load':DIRECT, 'src':ANA_NATIVE},
    'W_tmean':          {'load':DIRECT, 'src':ANA_NATIVE},
    'POTT_tmean':       {'load':DIRECT, 'src':ANA_NATIVE},
    'INVHGT_tmean':     {'load':DIRECT, 'src':ANA_NATIVE},


    # ANALYSIS BINARY VARIABLES
    'bulk_tend_edge_POTT_below_S':
                        {'load':'bin',  'src':'11'},
    'bulk_tend_edge_POTT_below_E':
                        {'load':'bin',  'src':'11'},
    'bulk_tend_edge_POTT_below_N':
                        {'load':'bin',  'src':'11'},
    'bulk_tend_edge_POTT_below_W':
                        {'load':'bin',  'src':'11'},
}
###############################################################################


def set_up_var_src_dict(inp_base_dir, ana_base_dir):
    for var_key,var_dict in var_src.items():
        if var_dict['src'] == INPUT:
            var_src[var_key]['src'] = inp_base_dir
        elif var_dict['src'] == ANA_NATIVE:
            var_src[var_key]['src'] = os.path.join(ana_base_dir, 'native_grid')
        elif var_dict['src'] == ANA_REMAPPED_45:
            var_src[var_key]['src'] = os.path.join(ana_base_dir, 'remapped_45')
        elif var_dict['src'] in ['11']:
            var_src[var_key]['src'] = os.path.join(ana_base_dir, var_src[var_key]['src'])
        else:
            raise NotImplementedError()
    return(var_src)


if __name__ == '__main__':
    pass
