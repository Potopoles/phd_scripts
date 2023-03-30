#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     All variables that are used in the analyses and how they
                should be treated (derived or directly loaded)
author			Christoph Heim
date created    07.09.2020
date changed    22.04.2022
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
mode_step_1 = DERIVE
mode_step_2 = DERIVE
mode_step_3 = DERIVE
mode_step_5 = DIRECT

input_1 = INPUT
###input_1 = ANA_NATIVE
derive_1 = DERIVE
derive_1 = DIRECT

input_2 = INPUT
input_2 = ANA_NATIVE
derive_2 = DERIVE
derive_2 = DIRECT

derive_3 = DERIVE
derive_3 = DIRECT

derive_4 = DERIVE
#derive_4 = DIRECT

var_src = {
    'W':                    {'load':DIRECT,     'src':INPUT},

    ## CMIP6
    'T':                    {'load':derive_1,   'src':input_1},
    #'WP':                   {'load':derive_1,   'src':input_1},
    'U':                    {'load':derive_1,   'src':input_1},
    'V':                    {'load':derive_1,   'src':input_1},
    'P':                    {'load':derive_1,   'src':input_1},
    'QV':                   {'load':DERIVE,     'src':input_1},

    'INVHGT':               {'load':derive_2,   'src':ANA_NATIVE},
    'RH':                   {'load':derive_2,   'src':input_2},
    'LCL':                  {'load':derive_2,   'src':ANA_NATIVE},
    'POTT':                 {'load':derive_2,   'src':ANA_NATIVE},
    'EQPOTT':               {'load':derive_2,   'src':ANA_NATIVE},
    'RHO':                  {'load':derive_2,   'src':ANA_NATIVE},

    'LTS':                  {'load':derive_3,   'src':ANA_NATIVE},
    'EIS':                  {'load':DERIVE,     'src':ANA_NATIVE},
    'INVSTR':               {'load':derive_3,   'src':ANA_NATIVE},
    'INVSTRV':              {'load':derive_3,   'src':ANA_NATIVE},
    'BUOYIFLX':             {'load':derive_3,   'src':ANA_NATIVE},
    'DQVINV':               {'load':derive_3,   'src':ANA_NATIVE},
    'ZCPTPP':               {'load':derive_3,   'src':ANA_NATIVE},
    'PCPTPP':               {'load':derive_3,   'src':ANA_NATIVE},
    'ENTR':                 {'load':derive_3,   'src':ANA_NATIVE},

    'BVFNORMI':             {'load':derive_4,   'src':ANA_NATIVE},
    'LCLNORMI':             {'load':derive_4,   'src':ANA_NATIVE},
    'RHNORMI':              {'load':derive_4,   'src':ANA_NATIVE},
    'TNORMI':               {'load':derive_4,   'src':ANA_NATIVE},
    'QCNORMI':              {'load':derive_4,   'src':ANA_NATIVE},
    'QVNORMI':              {'load':derive_4,   'src':ANA_NATIVE},
    'WNORMI':               {'load':derive_4,   'src':ANA_NATIVE},
    'UNORMI':               {'load':derive_4,   'src':ANA_NATIVE},
    'VNORMI':               {'load':derive_4,   'src':ANA_NATIVE},
    'UVNORMI':              {'load':derive_4,   'src':ANA_NATIVE},
    'CLDFNORMI':            {'load':derive_4,   'src':ANA_NATIVE},
    'BUOYIFLXNORMI':        {'load':DERIVE, 'src':ANA_NATIVE},


    'dRHdt':                {'load':DERIVE, 'src':ANA_NATIVE},
    'dRHdt_MBL_FLX':        {'load':DERIVE, 'src':ANA_NATIVE},
    'dQVdt_MBL_LH':         {'load':DERIVE, 'src':ANA_NATIVE},
    'dTdt_MBL_SH':          {'load':DERIVE, 'src':ANA_NATIVE},
    'BVF':                  {'load':DERIVE, 'src':ANA_NATIVE},
    'TDEW':                 {'load':DERIVE, 'src':ANA_NATIVE},
    'UVDIV':                {'load':DERIVE, 'src':ANA_NATIVE},
    'CSUVDIV':              {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDUVDIV':             {'load':DERIVE, 'src':ANA_NATIVE},
    'AQV':                  {'load':DERIVE, 'src':ANA_NATIVE},
    'AQI':                  {'load':DERIVE, 'src':ANA_NATIVE},
    'INVF':                 {'load':DERIVE, 'src':ANA_NATIVE},
    'UV':                   {'load':DERIVE, 'src':ANA_NATIVE},
    'DIABH':                {'load':DERIVE, 'src':ANA_NATIVE},
    'LATH':                 {'load':DERIVE, 'src':ANA_NATIVE},
    'LATHNORMI':            {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDLATH':              {'load':DERIVE, 'src':ANA_NATIVE},
    'CSLATH':               {'load':DERIVE, 'src':ANA_NATIVE},
    'DIABM':                {'load':DERIVE, 'src':ANA_NATIVE},
    'LCLDF1E-3':            {'load':DERIVE, 'src':ANA_NATIVE},
    'LCLDF5E-4':            {'load':DERIVE, 'src':ANA_NATIVE},
    'LCLDF2E-4':            {'load':DERIVE, 'src':ANA_NATIVE},
    'LCLDF1E-4':            {'load':DERIVE, 'src':ANA_NATIVE},
    'LCLDF5E-5':            {'load':DERIVE, 'src':ANA_NATIVE},
    'LCLDF2E-5':            {'load':DERIVE, 'src':ANA_NATIVE},
    'LCLDF1E-5':            {'load':DERIVE, 'src':ANA_NATIVE},
    'ICLDF1E-3':            {'load':DERIVE, 'src':ANA_NATIVE},
    'ICLDF5E-4':            {'load':DERIVE, 'src':ANA_NATIVE},
    'ICLDF2E-4':            {'load':DERIVE, 'src':ANA_NATIVE},
    'ICLDF1E-4':            {'load':DERIVE, 'src':ANA_NATIVE},
    'ICLDF5E-5':            {'load':DERIVE, 'src':ANA_NATIVE},
    'ICLDF2E-5':            {'load':DERIVE, 'src':ANA_NATIVE},
    'ICLDF1E-5':            {'load':DERIVE, 'src':ANA_NATIVE},
    'LCLDF1E-3NORMI':       {'load':DERIVE, 'src':ANA_NATIVE},
    'LCLDF5E-4NORMI':       {'load':DERIVE, 'src':ANA_NATIVE},
    'LCLDF2E-4NORMI':       {'load':DERIVE, 'src':ANA_NATIVE},
    'LCLDF1E-4NORMI':       {'load':DERIVE, 'src':ANA_NATIVE},
    'LCLDF5E-5NORMI':       {'load':DERIVE, 'src':ANA_NATIVE},
    'LCLDF2E-5NORMI':       {'load':DERIVE, 'src':ANA_NATIVE},
    'LCLDF1E-5NORMI':       {'load':DERIVE, 'src':ANA_NATIVE},
    'ICLDF1E-3NORMI':       {'load':DERIVE, 'src':ANA_NATIVE},
    'ICLDF5E-4NORMI':       {'load':DERIVE, 'src':ANA_NATIVE},
    'ICLDF2E-4NORMI':       {'load':DERIVE, 'src':ANA_NATIVE},
    'ICLDF1E-4NORMI':       {'load':DERIVE, 'src':ANA_NATIVE},
    'ICLDF5E-5NORMI':       {'load':DERIVE, 'src':ANA_NATIVE},
    'ICLDF2E-5NORMI':       {'load':DERIVE, 'src':ANA_NATIVE},
    'ICLDF1E-5NORMI':       {'load':DERIVE, 'src':ANA_NATIVE},

    'POTTDIV':              {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTVDIV':             {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTHDIV':             {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTXDIV':             {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTYDIV':             {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTDIV2':             {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTVDIV2':            {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTHDIV2':            {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTDIV3':             {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTVDIV3':            {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTHDIV3':            {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTDIV4':             {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTVDIV4':            {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTHDIV4':            {'load':DERIVE, 'src':ANA_NATIVE},

    'DIABMNORMI':           {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTHDIVNORMI':        {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTVDIVNORMI':        {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTDIVNORMI':         {'load':DERIVE, 'src':ANA_NATIVE},
    'EQPOTTDIVNORMI':       {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTHDIV3NORMI':       {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTVDIV3NORMI':       {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTDIV3NORMI':        {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTHDIVTURBNORMI':    {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTVDIVTURBNORMI':    {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTDIVTURBNORMI':     {'load':DERIVE, 'src':ANA_NATIVE},

    'CLDPOTTDIV':           {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDPOTTVDIV':          {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDPOTTHDIV':          {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDPOTTDIV3':          {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDPOTTVDIV3':         {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDPOTTHDIV3':         {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDPOTTDIV3':          {'load':DERIVE, 'src':ANA_NATIVE},

    'CLDPOTTDIVNORMI':      {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDPOTTDIV3NORMI':     {'load':DERIVE, 'src':ANA_NATIVE},

    'CSPOTTDIV':            {'load':DERIVE, 'src':ANA_NATIVE},
    'CSPOTTVDIV':           {'load':DERIVE, 'src':ANA_NATIVE},
    'CSPOTTHDIV':           {'load':DERIVE, 'src':ANA_NATIVE},
    'CSPOTTDIV3':           {'load':DERIVE, 'src':ANA_NATIVE},
    'CSPOTTVDIV3':          {'load':DERIVE, 'src':ANA_NATIVE},
    'CSPOTTHDIV3':          {'load':DERIVE, 'src':ANA_NATIVE},

    'CSPOTTDIVNORMI':       {'load':DERIVE, 'src':ANA_NATIVE},
    'CSPOTTDIV3NORMI':      {'load':DERIVE, 'src':ANA_NATIVE},
     
    'NCOLIPOTTDIV3':        {'load':DERIVE, 'src':ANA_NATIVE},
    'NCOLIPOTTDIV':         {'load':DERIVE, 'src':ANA_NATIVE},
    'NCOLIQV':              {'load':DERIVE, 'src':ANA_NATIVE},

    'RH0LCSPOTTDIV3':       {'load':DERIVE, 'src':ANA_NATIVE},
    'RH1LCSPOTTDIV3':       {'load':DERIVE, 'src':ANA_NATIVE},
    'RH2LCSPOTTDIV3':       {'load':DERIVE, 'src':ANA_NATIVE},
    'RH0GCSPOTTDIV3':       {'load':DERIVE, 'src':ANA_NATIVE},
    'RH1GCSPOTTDIV3':       {'load':DERIVE, 'src':ANA_NATIVE},
    'RH2GCSPOTTDIV3':       {'load':DERIVE, 'src':ANA_NATIVE},

    'EQPOTTDIV':            {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDEQPOTTDIV':         {'load':DERIVE, 'src':ANA_NATIVE},
    'CSEQPOTTDIV':          {'load':DERIVE, 'src':ANA_NATIVE},
    'EQPOTTHDIV':           {'load':DERIVE, 'src':ANA_NATIVE},
    'EQPOTTVDIV':           {'load':DERIVE, 'src':ANA_NATIVE},
    'EQPOTTDIV3':           {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDEQPOTTDIV3':        {'load':DERIVE, 'src':ANA_NATIVE},
    'CSEQPOTTDIV3':         {'load':DERIVE, 'src':ANA_NATIVE},
    'EQPOTTHDIV3':          {'load':DERIVE, 'src':ANA_NATIVE},
    'EQPOTTVDIV3':          {'load':DERIVE, 'src':ANA_NATIVE},
    'QCHDIV':               {'load':DERIVE, 'src':ANA_NATIVE},
    'QCVDIV':               {'load':DERIVE, 'src':ANA_NATIVE},
    'QCDIV':                {'load':DERIVE, 'src':ANA_NATIVE},
    'QIHDIV3':              {'load':DERIVE, 'src':ANA_NATIVE},
    'QIVDIV3':              {'load':DERIVE, 'src':ANA_NATIVE},
    'QIDIV3':               {'load':DERIVE, 'src':ANA_NATIVE},
    'AQVHDIV3':             {'load':DERIVE, 'src':ANA_NATIVE},
    'WVPHCONV':             {'load':DERIVE, 'src':ANA_NATIVE},
    'AQIHDIV3':             {'load':DERIVE, 'src':ANA_NATIVE},
    'IWPHCONV':             {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTHDIVMEAN':         {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTVDIVMEAN':         {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTDIVMEAN':          {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTHDIVTURB':         {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTVDIVTURB':         {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTDIVTURB':          {'load':DERIVE, 'src':ANA_NATIVE},
    'TKE':                  {'load':DERIVE, 'src':ANA_NATIVE},
    'TKEV':                 {'load':DERIVE, 'src':ANA_NATIVE},


    'TKENORMI':             {'load':DERIVE, 'src':ANA_NATIVE},
    'TKEVNORMI':            {'load':DERIVE, 'src':ANA_NATIVE},

    'QVDIV':                {'load':DERIVE, 'src':ANA_NATIVE},
    'QVXDIV':               {'load':DERIVE, 'src':ANA_NATIVE},
    'QVYDIV':               {'load':DERIVE, 'src':ANA_NATIVE},
    'QVHDIV':               {'load':DERIVE, 'src':ANA_NATIVE},
    'QVVDIV':               {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVDIV':              {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVVDIV':             {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVHDIV':             {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVDIV':             {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVVDIV':            {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVHDIV':            {'load':DERIVE, 'src':ANA_NATIVE},

    'QVDIV2':               {'load':DERIVE, 'src':ANA_NATIVE},
    'QVHDIV2':              {'load':DERIVE, 'src':ANA_NATIVE},
    'QVVDIV2':              {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVDIV2':             {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVVDIV2':            {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVHDIV2':            {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVDIV2':            {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVVDIV2':           {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVHDIV2':           {'load':DERIVE, 'src':ANA_NATIVE},

    'QVDIV3':               {'load':DERIVE, 'src':ANA_NATIVE},
    'QVHDIV3':              {'load':DERIVE, 'src':ANA_NATIVE},
    'QVVDIV3':              {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVDIV3':             {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVVDIV3':            {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVHDIV3':            {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVDIV3':            {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVVDIV3':           {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVHDIV3':           {'load':DERIVE, 'src':ANA_NATIVE},

    'QVDIVNORMI':           {'load':DERIVE, 'src':ANA_NATIVE},
    'QVVDIVNORMI':          {'load':DERIVE, 'src':ANA_NATIVE},
    'QVHDIVNORMI':          {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVDIVNORMI':         {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVVDIVNORMI':        {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVHDIVNORMI':        {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVDIVNORMI':        {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVVDIVNORMI':       {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVHDIVNORMI':       {'load':DERIVE, 'src':ANA_NATIVE},

    'QVDIV2NORMI':          {'load':DERIVE, 'src':ANA_NATIVE},
    'QVVDIV2NORMI':         {'load':DERIVE, 'src':ANA_NATIVE},
    'QVHDIV2NORMI':         {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVDIV2NORMI':        {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVVDIV2NORMI':       {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVHDIV2NORMI':       {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVDIV2NORMI':       {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVVDIV2NORMI':      {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVHDIV2NORMI':      {'load':DERIVE, 'src':ANA_NATIVE},

    'QVDIV3NORMI':          {'load':DERIVE, 'src':ANA_NATIVE},
    'QVVDIV3NORMI':         {'load':DERIVE, 'src':ANA_NATIVE},
    'QVHDIV3NORMI':         {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVDIV3NORMI':        {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVVDIV3NORMI':       {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVHDIV3NORMI':       {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVDIV3NORMI':       {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVVDIV3NORMI':      {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVHDIV3NORMI':      {'load':DERIVE, 'src':ANA_NATIVE},

    'QVDIVMEAN':            {'load':DERIVE, 'src':ANA_NATIVE},
    'QVVDIVMEAN':           {'load':DERIVE, 'src':ANA_NATIVE},
    'QVHDIVMEAN':           {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVDIVMEAN':          {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVVDIVMEAN':         {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVHDIVMEAN':         {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVDIVMEAN':         {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVVDIVMEAN':        {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVHDIVMEAN':        {'load':DERIVE, 'src':ANA_NATIVE},

    'QVDIV2MEAN':           {'load':DERIVE, 'src':ANA_NATIVE},
    'QVVDIV2MEAN':          {'load':DERIVE, 'src':ANA_NATIVE},
    'QVHDIV2MEAN':          {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVDIV2MEAN':         {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVVDIV2MEAN':        {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVHDIV2MEAN':        {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVDIV2MEAN':        {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVVDIV2MEAN':       {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVHDIV2MEAN':       {'load':DERIVE, 'src':ANA_NATIVE},

    'QVDIV3MEAN':           {'load':DERIVE, 'src':ANA_NATIVE},
    'QVVDIV3MEAN':          {'load':DERIVE, 'src':ANA_NATIVE},
    'QVHDIV3MEAN':          {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVDIV3MEAN':         {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVVDIV3MEAN':        {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVHDIV3MEAN':        {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVDIV3MEAN':        {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVVDIV3MEAN':       {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVHDIV3MEAN':       {'load':DERIVE, 'src':ANA_NATIVE},

    'QVDIVMEANNORMI':       {'load':DERIVE, 'src':ANA_NATIVE},
    'QVVDIVMEANNORMI':      {'load':DERIVE, 'src':ANA_NATIVE},
    'QVHDIVMEANNORMI':      {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVDIVMEANNORMI':     {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVVDIVMEANNORMI':    {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVHDIVMEANNORMI':    {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVDIVMEANNORMI':    {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVVDIVMEANNORMI':   {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVHDIVMEANNORMI':   {'load':DERIVE, 'src':ANA_NATIVE},

    'QVDIV2MEANNORMI':      {'load':DERIVE, 'src':ANA_NATIVE},
    'QVVDIV2MEANNORMI':     {'load':DERIVE, 'src':ANA_NATIVE},
    'QVHDIV2MEANNORMI':     {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVDIV2MEANNORMI':    {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVVDIV2MEANNORMI':   {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVHDIV2MEANNORMI':   {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVDIV2MEANNORMI':   {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVVDIV2MEANNORMI':  {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVHDIV2MEANNORMI':  {'load':DERIVE, 'src':ANA_NATIVE},

    'QVDIV3MEANNORMI':      {'load':DERIVE, 'src':ANA_NATIVE},
    'QVVDIV3MEANNORMI':     {'load':DERIVE, 'src':ANA_NATIVE},
    'QVHDIV3MEANNORMI':     {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVDIV3MEANNORMI':    {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVVDIV3MEANNORMI':   {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVHDIV3MEANNORMI':   {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVDIV3MEANNORMI':   {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVVDIV3MEANNORMI':  {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVHDIV3MEANNORMI':  {'load':DERIVE, 'src':ANA_NATIVE},

    'QVDIVTURB':            {'load':DERIVE, 'src':ANA_NATIVE},
    'QVVDIVTURB':           {'load':DERIVE, 'src':ANA_NATIVE},
    'QVUVDIVTURB':          {'load':DERIVE, 'src':ANA_NATIVE},
    'QVDVDIVTURB':          {'load':DERIVE, 'src':ANA_NATIVE},
    'QVHDIVTURB':           {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVDIVTURB':          {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVVDIVTURB':         {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVDVDIVTURB':        {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVUVDIVTURB':        {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVHDIVTURB':         {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVDIVTURB':         {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVVDIVTURB':        {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVUVDIVTURB':       {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVDVDIVTURB':       {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVHDIVTURB':        {'load':DERIVE, 'src':ANA_NATIVE},

    'QVDIV2TURB':           {'load':DERIVE, 'src':ANA_NATIVE},
    'QVVDIV2TURB':          {'load':DERIVE, 'src':ANA_NATIVE},
    'QVUVDIV2TURB':         {'load':DERIVE, 'src':ANA_NATIVE},
    'QVDVDIV2TURB':         {'load':DERIVE, 'src':ANA_NATIVE},
    'QVHDIV2TURB':          {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVDIV2TURB':         {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVVDIV2TURB':        {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVDVDIV2TURB':       {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVUVDIV2TURB':       {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVHDIV2TURB':        {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVDIV2TURB':        {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVVDIV2TURB':       {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVUVDIV2TURB':      {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVDVDIV2TURB':      {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVHDIV2TURB':       {'load':DERIVE, 'src':ANA_NATIVE},

    'QVDIV3TURB':           {'load':DERIVE, 'src':ANA_NATIVE},
    'QVVDIV3TURB':          {'load':DERIVE, 'src':ANA_NATIVE},
    'QVUVDIV3TURB':         {'load':DERIVE, 'src':ANA_NATIVE},
    'QVDVDIV3TURB':         {'load':DERIVE, 'src':ANA_NATIVE},
    'QVHDIV3TURB':          {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVDIV3TURB':         {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVVDIV3TURB':        {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVDVDIV3TURB':       {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVUVDIV3TURB':       {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVHDIV3TURB':        {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVDIV3TURB':        {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVVDIV3TURB':       {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVUVDIV3TURB':      {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVDVDIV3TURB':      {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVHDIV3TURB':       {'load':DERIVE, 'src':ANA_NATIVE},

    'QVDIVTURBNORMI':       {'load':DERIVE, 'src':ANA_NATIVE},
    'QVVDIVTURBNORMI':      {'load':DERIVE, 'src':ANA_NATIVE},
    'QVUVDIVTURBNORMI':     {'load':DERIVE, 'src':ANA_NATIVE},
    'QVDVDIVTURBNORMI':     {'load':DERIVE, 'src':ANA_NATIVE},
    'QVHDIVTURBNORMI':      {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVDIVTURBNORMI':     {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVVDIVTURBNORMI':    {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVUVDIVTURBNORMI':   {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVDVDIVTURBNORMI':   {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVHDIVTURBNORMI':    {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVDIVTURBNORMI':    {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVVDIVTURBNORMI':   {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVUVDIVTURBNORMI':  {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVDVDIVTURBNORMI':  {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVHDIVTURBNORMI':   {'load':DERIVE, 'src':ANA_NATIVE},

    'QVDIV2TURBNORMI':      {'load':DERIVE, 'src':ANA_NATIVE},
    'QVVDIV2TURBNORMI':     {'load':DERIVE, 'src':ANA_NATIVE},
    'QVUVDIV2TURBNORMI':    {'load':DERIVE, 'src':ANA_NATIVE},
    'QVDVDIV2TURBNORMI':    {'load':DERIVE, 'src':ANA_NATIVE},
    'QVHDIV2TURBNORMI':     {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVDIV2TURBNORMI':    {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVVDIV2TURBNORMI':   {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVUVDIV2TURBNORMI':  {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVDVDIV2TURBNORMI':  {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVHDIV2TURBNORMI':   {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVDIV2TURBNORMI':   {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVVDIV2TURBNORMI':  {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVUVDIV2TURBNORMI': {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVDVDIV2TURBNORMI': {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVHDIV2TURBNORMI':  {'load':DERIVE, 'src':ANA_NATIVE},

    'QVDIV3TURBNORMI':      {'load':DERIVE, 'src':ANA_NATIVE},
    'QVVDIV3TURBNORMI':     {'load':DERIVE, 'src':ANA_NATIVE},
    'QVUVDIV3TURBNORMI':    {'load':DERIVE, 'src':ANA_NATIVE},
    'QVDVDIV3TURBNORMI':    {'load':DERIVE, 'src':ANA_NATIVE},
    'QVHDIV3TURBNORMI':     {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVDIV3TURBNORMI':    {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVVDIV3TURBNORMI':   {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVUVDIV3TURBNORMI':  {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVDVDIV3TURBNORMI':  {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVHDIV3TURBNORMI':   {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVDIV3TURBNORMI':   {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVVDIV3TURBNORMI':  {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVUVDIV3TURBNORMI': {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVDVDIV3TURBNORMI': {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVHDIV3TURBNORMI':  {'load':DERIVE, 'src':ANA_NATIVE},


    'POTTHDIVMEANNORMI':    {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTVDIVMEANNORMI':    {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTDIVMEANNORMI':     {'load':DERIVE, 'src':ANA_NATIVE},

    'CLDQVSATDEF':          {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQV':                {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDW':                 {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDRH':                {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDTKEV':              {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDBVF':               {'load':DERIVE, 'src':ANA_NATIVE},

    'CSQVSATDEF':           {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQV':                 {'load':DERIVE, 'src':ANA_NATIVE},
    'CSW':                  {'load':DERIVE, 'src':ANA_NATIVE},
    'CSRH':                 {'load':DERIVE, 'src':ANA_NATIVE},
    'CSTKEV':               {'load':DERIVE, 'src':ANA_NATIVE},
    'CSBVF':                {'load':DERIVE, 'src':ANA_NATIVE},

    'CLDQVSATDEFNORMI':     {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQVNORMI':           {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDWNORMI':            {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDRHNORMI':           {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDTKEVNORMI':         {'load':DERIVE, 'src':ANA_NATIVE},

    'CSQVSATDEFNORMI':      {'load':DERIVE, 'src':ANA_NATIVE},
    'CSQVNORMI':            {'load':DERIVE, 'src':ANA_NATIVE},
    'CSWNORMI':             {'load':DERIVE, 'src':ANA_NATIVE},
    'CSRHNORMI':            {'load':DERIVE, 'src':ANA_NATIVE},
    'CSTKEVNORMI':          {'load':DERIVE, 'src':ANA_NATIVE},


    # radiation 1
    'CLCW':                 {'load':DERIVE, 'src':ANA_NATIVE},
    'CLCI':                 {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDQX':                {'load':DERIVE, 'src':ANA_NATIVE},

    'CLDF':                 {'load':DERIVE, 'src':INPUT},
    'SWUTOA':               {'load':DERIVE, 'src':INPUT},
    'CSWUTOA':              {'load':DERIVE, 'src':INPUT},
    'SWUSFC':               {'load':DERIVE, 'src':INPUT},
    'SWDIFUSFC':            {'load':DIRECT, 'src':INPUT},
    'SWDTOA':               {'load':DIRECT, 'src':INPUT},
    'SWDSFC':               {'load':DERIVE, 'src':INPUT},
    'SWDIFDSFC':            {'load':DIRECT, 'src':INPUT},
    'SWDIRDSFC':            {'load':DIRECT, 'src':INPUT},
    'SWNUSFC':              {'load':DERIVE, 'src':INPUT},
    'SWNDTOA':              {'load':DERIVE, 'src':INPUT},
    'CSWNDTOA':             {'load':DERIVE, 'src':INPUT},
    'CRESWNDTOA':           {'load':DERIVE, 'src':INPUT},
    'SWNDSFC':              {'load':DERIVE, 'src':INPUT},
    'CSWNDSFC':             {'load':DIRECT, 'src':INPUT},
    'CRESWNDSFC':           {'load':DERIVE, 'src':INPUT},
    'LWUTOA':               {'load':DERIVE, 'src':INPUT},
    'CLWUTOA':              {'load':DERIVE, 'src':INPUT},
    'CRELWUTOA':            {'load':DERIVE, 'src':INPUT},
    'LWUSFC':               {'load':DERIVE, 'src':INPUT},
    'LWDTOA':               {'load':DERIVE, 'src':INPUT},
    'CLWDTOA':              {'load':DERIVE, 'src':INPUT},
    'CRELWDTOA':            {'load':DERIVE, 'src':INPUT},
    'LWNUSFC':              {'load':DERIVE, 'src':INPUT},
    'LWDSFC':               {'load':DIRECT, 'src':INPUT},
    'CLWDSFC':              {'load':DERIVE, 'src':INPUT},
    'LWNDSFC':              {'load':DERIVE, 'src':INPUT},
    'CLWNDSFC':             {'load':DIRECT, 'src':INPUT},
    'CRELWNDSFC':           {'load':DERIVE, 'src':INPUT},
    'LWDIVATM':             {'load':DERIVE, 'src':INPUT},
    'CLWDIVATM':            {'load':DERIVE, 'src':INPUT},
    'CRELWDIVATM':          {'load':DERIVE, 'src':INPUT},
    'RADNDTOA':             {'load':DERIVE, 'src':INPUT},
    'CRADNDTOA':            {'load':DERIVE, 'src':INPUT},
    'CRERADNDTOA':          {'load':DERIVE, 'src':INPUT},
    'QV2M':                 {'load':DIRECT, 'src':INPUT},
    'T2M':                  {'load':DIRECT, 'src':INPUT},

    'CLDMASK':              {'load':DERIVE, 'src':ANA_NATIVE},
    'SUBS':                 {'load':DERIVE, 'src':ANA_NATIVE},
    'SUBSOMEGA':            {'load':DERIVE, 'src':ANA_NATIVE},
    'TQV':                  {'load':DIRECT, 'src':INPUT},
    'WSOIL':                {'load':DIRECT, 'src':INPUT},
    'TSOIL':                {'load':DIRECT, 'src':INPUT},

    # step 2
    'ALBEDO':               {'load':DERIVE, 'src':INPUT},

    'TV':                   {'load':DERIVE, 'src':ANA_NATIVE},
    'UPDTV':                {'load':DERIVE, 'src':ANA_NATIVE},
    'UPDT':                 {'load':DERIVE, 'src':ANA_NATIVE},
    'UPDTDEW':              {'load':DERIVE, 'src':ANA_NATIVE},
    'UPD2TV':                {'load':DERIVE, 'src':ANA_NATIVE},
    'UPD2T':                 {'load':DERIVE, 'src':ANA_NATIVE},
    'UPD2TDEW':              {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTV':                {'load':DERIVE, 'src':ANA_NATIVE},
    'ENTRV':                {'load':DERIVE, 'src':ANA_NATIVE},
    'ENTRH':                {'load':DERIVE, 'src':ANA_NATIVE},
    'ENTRSCL':              {'load':DERIVE, 'src':ANA_NATIVE},
    'ENTRVSCL':             {'load':DIRECT, 'src':ANA_NATIVE},
    'ENTRHSCL':             {'load':DIRECT, 'src':ANA_NATIVE},
    'LOWCLDBASE':           {'load':DIRECT, 'src':ANA_NATIVE},

    # step 3
    'UVFLXDIV':             {'load':mode_step_3, 'src':ANA_NATIVE},
    'AWNORMI':              {'load':mode_step_3, 'src':ANA_NATIVE},
    'POTTVDIVWPOS':         {'load':mode_step_3, 'src':ANA_NATIVE},
    'POTTVDIVWNEG':         {'load':mode_step_3, 'src':ANA_NATIVE},

    # step 4: computation of mean inherits from above

    # now run Reynolds.

    # step 5
    'UVFLXDIVNORMI':        {'load':mode_step_5, 'src':ANA_NATIVE},
    'CLDMASKNORMI':         {'load':DERIVE, 'src':ANA_NATIVE},


    'WTURB':                {'load':DERIVE, 'src':ANA_NATIVE},
    'WTURBNORMI':           {'load':DERIVE, 'src':ANA_NATIVE},
    'WTURBNORMISCI':        {'load':DERIVE, 'src':ANA_NATIVE},
    'UI':                   {'load':DERIVE, 'src':ANA_NATIVE},
    'VI':                   {'load':DERIVE, 'src':ANA_NATIVE},
    'WI':                   {'load':DERIVE, 'src':ANA_NATIVE},
    'RHOI':                 {'load':DERIVE, 'src':ANA_NATIVE},
    'INVSTR':               {'load':DIRECT, 'src':ANA_NATIVE},
    'POTTBL':               {'load':DIRECT, 'src':ANA_NATIVE},
    'POTTFT':               {'load':DIRECT, 'src':ANA_NATIVE},
    'POTTVFT':              {'load':DIRECT, 'src':ANA_NATIVE},
    'ENTRDRY':              {'load':DERIVE, 'src':ANA_NATIVE},
    'QVFT':                 {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTHDIVMBLI':         {'load':DIRECT, 'src':ANA_NATIVE},
    'POTTMBLI':             {'load':DIRECT, 'src':ANA_NATIVE},
    'TQVFT':                {'load':DERIVE, 'src':ANA_NATIVE},
    'LOWCLDF':              {'load':DERIVE, 'src':ANA_NATIVE},
    'LCLDDEPTH':            {'load':DIRECT, 'src':ANA_NATIVE},
    'DCLDBASELCL':          {'load':DIRECT, 'src':ANA_NATIVE},
    'DINVHGTLCL':           {'load':DERIVE, 'src':ANA_NATIVE},
    'DINVHGTLOWCLDBASE':    {'load':DERIVE, 'src':ANA_NATIVE},
    'PVAP':                 {'load':DERIVE, 'src':ANA_NATIVE},
    'PVAPSATL':             {'load':DERIVE, 'src':ANA_NATIVE},
    'PVAPSATS':             {'load':DERIVE, 'src':ANA_NATIVE},
    'QVSAT':                {'load':DERIVE, 'src':ANA_NATIVE},
    'QVSATDEF':             {'load':DERIVE, 'src':ANA_NATIVE},
    'QVSATDEFNORMI':        {'load':DERIVE, 'src':ANA_NATIVE},
    'RHLNORMI':             {'load':DERIVE, 'src':ANA_NATIVE},
    'HSURF':                {'load':DIRECT, 'src':INPUT},
    'POTTNORMI':            {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTVNORMI':           {'load':DERIVE, 'src':ANA_NATIVE},
    'LOWCLDBASENORMI':      {'load':DERIVE, 'src':ANA_NATIVE},
    'SST':                  {'load':DERIVE, 'src':INPUT},
    'TSURF':                {'load':DIRECT, 'src':INPUT},
    'SLHFLX':               {'load':DERIVE, 'src':INPUT},
    'SSHFLX':               {'load':DERIVE, 'src':INPUT},
    'SBUOYIFLX':            {'load':DERIVE, 'src':INPUT},
    'ENFLXNUSFC':           {'load':DERIVE, 'src':INPUT},
    'CORREFL':              {'load':DERIVE, 'src':INPUT},
    'AW':                   {'load':DERIVE, 'src':ANA_NATIVE},
    'UFLX':                 {'load':DERIVE, 'src':ANA_NATIVE},
    'VFLX':                 {'load':DERIVE, 'src':ANA_NATIVE},
    'WFLX':                 {'load':DERIVE, 'src':ANA_NATIVE},
    'WFLXI':                {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDWFLX':              {'load':DERIVE, 'src':ANA_NATIVE},
    'CSWFLX':               {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDWFLXLCL':           {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDWTURBFLXLOWCLDBASE':{'load':DERIVE, 'src':ANA_NATIVE},
    'CLDWFLXLOWCLDBASE':    {'load':DERIVE, 'src':ANA_NATIVE},
    'CSWFLXLOWCLDBASE':     {'load':DERIVE, 'src':ANA_NATIVE},
    'UVHCONVMINV':          {'load':DERIVE, 'src':ANA_NATIVE},
    'WMBLI':                {'load':DERIVE, 'src':ANA_NATIVE},
    'WFLXNORMI':            {'load':DERIVE, 'src':ANA_NATIVE},
    'DIABHMINV':            {'load':DERIVE, 'src':ANA_NATIVE},
    'PPERT':                {'load':DIRECT, 'src':INPUT},
    'PNORMI':               {'load':DERIVE, 'src':ANA_NATIVE},
    'ALT':                  {'load':DIRECT, 'src':INPUT},
    'ALT_Amon':             {'load':DIRECT, 'src':INPUT},
    'QC':                   {'load':DIRECT, 'src':INPUT},
    'QI':                   {'load':DIRECT, 'src':INPUT},
    'QR':                   {'load':DIRECT, 'src':INPUT},
    'QG':                   {'load':DIRECT, 'src':INPUT},
    'QS':                   {'load':DIRECT, 'src':INPUT},
    'AWU':                  {'load':DERIVE, 'src':ANA_NATIVE},
    'AWD':                  {'load':DERIVE, 'src':ANA_NATIVE},
    #'AWUNORMI':             {'load':DERIVE, 'src':ANA_NATIVE},
    #'AWDNORMI':             {'load':DERIVE, 'src':ANA_NATIVE},
    'AWMBLI':               {'load':DERIVE, 'src':ANA_NATIVE},
    'KEW':                  {'load':DIRECT, 'src':ANA_NATIVE},
    'KEWNORMI':             {'load':DERIVE, 'src':ANA_NATIVE},
    'KEWMBLI':              {'load':DERIVE, 'src':ANA_NATIVE},
    'TKEMBLI':              {'load':DERIVE, 'src':ANA_NATIVE},
    'CAPE':                 {'load':DIRECT, 'src':INPUT},
    'CIN':                  {'load':DIRECT, 'src':INPUT},
    'CLCL':                 {'load':DERIVE, 'src':INPUT},
    'CLCL2':                {'load':DERIVE, 'src':INPUT},
    'CLCM':                 {'load':DIRECT, 'src':INPUT},
    'CLCH':                 {'load':DIRECT, 'src':INPUT},
    'CLCT':                 {'load':DERIVE, 'src':INPUT},
    'PS':                   {'load':DERIVE, 'src':INPUT},
    'SWDTOA':               {'load':DIRECT, 'src':INPUT},
    'INVSTRA':              {'load':DERIVE, 'src':ANA_NATIVE},
    'CLDHGT':               {'load':DERIVE, 'src':ANA_NATIVE},
    'QVVFLX':               {'load':DERIVE, 'src':ANA_NATIVE},
    'QVWFLX':               {'load':DERIVE, 'src':ANA_NATIVE},
    'QVWFLXINV':            {'load':DERIVE, 'src':ANA_NATIVE},
    #'QVFLXZCB':             {'load':DERIVE, 'src':ANA_NATIVE},
    'PP':                   {'load':DERIVE, 'src':INPUT},
    'TQC':                  {'load':DIRECT, 'src':INPUT},
    'TQI':                  {'load':DIRECT, 'src':INPUT},
    'TQR':                  {'load':DIRECT, 'src':INPUT},
    'TQG':                  {'load':DIRECT, 'src':INPUT},
    'TQS':                  {'load':DIRECT, 'src':INPUT},
    'PPCONV':               {'load':DIRECT, 'src':INPUT},
    'PPGRID':               {'load':DIRECT, 'src':INPUT},
    'U10M':                 {'load':DIRECT, 'src':INPUT},
    'V10M':                 {'load':DIRECT, 'src':INPUT},
    'UV10M':                {'load':DERIVE, 'src':INPUT},
    'U10M_W':               {'load':DERIVE, 'src':INPUT},
    'U10M_E':               {'load':DERIVE, 'src':INPUT},
    'V10M_S':               {'load':DERIVE, 'src':INPUT},
    'V10M_N':               {'load':DERIVE, 'src':INPUT},



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


mean_var_src = {
    'POTTV':            {'load':DIRECT, 'src':ANA_NATIVE},
    'POTT':             {'load':DIRECT, 'src':ANA_NATIVE},
    'QV':               {'load':DIRECT, 'src':ANA_NATIVE},
    'W':                {'load':DIRECT, 'src':ANA_NATIVE},
    'U':                {'load':DIRECT, 'src':ANA_NATIVE},
    'V':                {'load':DIRECT, 'src':ANA_NATIVE},

    'INVHGT':           {'load':DIRECT, 'src':ANA_NATIVE},

    'POTTHDIV':         {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTVDIV':         {'load':DERIVE, 'src':ANA_NATIVE},
    'POTTDIV':          {'load':DERIVE, 'src':ANA_NATIVE},
    'QVHDIV':           {'load':DERIVE, 'src':ANA_NATIVE},
    'QVVDIV':           {'load':DERIVE, 'src':ANA_NATIVE},
    'QVDIV':            {'load':DERIVE, 'src':ANA_NATIVE},
    'QVHDIV2':          {'load':DERIVE, 'src':ANA_NATIVE},
    'QVVDIV2':          {'load':DERIVE, 'src':ANA_NATIVE},
    'QVDIV2':           {'load':DERIVE, 'src':ANA_NATIVE},
    'QVHDIV3':          {'load':DERIVE, 'src':ANA_NATIVE},
    'QVVDIV3':          {'load':DERIVE, 'src':ANA_NATIVE},
    'QVDIV3':           {'load':DERIVE, 'src':ANA_NATIVE},
}

def set_up_var_src_dict(inp_base_dir, ana_base_dir, ANA_NATIVE_domain):
    for var_key,var_dict in var_src.items():
        if var_dict['src'] == INPUT:
            var_src[var_key]['src_path'] = inp_base_dir
            var_src[var_key]['dom_key'] = None
        elif var_dict['src'] == ANA_NATIVE:
            var_src[var_key]['src_path'] = os.path.join(ana_base_dir, 'native_grid')
            var_src[var_key]['dom_key'] = ANA_NATIVE_domain['key']
        elif var_dict['src'] == ANA_REMAPPED_45:
            var_src[var_key]['src_path'] = os.path.join(ana_base_dir, 'remapped_45')
            raise NotImplementedError()
        elif var_dict['src'] in ['11']:
            var_src[var_key]['src_path'] = os.path.join(ana_base_dir, var_src[var_key]['src'])
        else:
            raise NotImplementedError()
    return(var_src)


def set_up_mean_var_src_dict(inp_base_dir, ana_base_dir, ANA_NATIVE_domain):
    for var_key,var_dict in mean_var_src.items():
        if var_dict['src'] == INPUT:
            mean_var_src[var_key]['src_path'] = inp_base_dir
            mean_var_src[var_key]['dom_key'] = None
        elif var_dict['src'] == ANA_NATIVE:
            mean_var_src[var_key]['src_path'] = os.path.join(ana_base_dir, 'native_grid')
            mean_var_src[var_key]['dom_key'] = ANA_NATIVE_domain['key']
        elif var_dict['src'] == ANA_REMAPPED_45:
            mean_var_src[var_key]['src_path'] = os.path.join(ana_base_dir, 'remapped_45')
            raise NotImplementedError()
        elif var_dict['src'] in ['11']:
            mean_var_src[var_key]['src_path'] = os.path.join(ana_base_dir, 
                                                        mean_var_src[var_key]['src'])
        else:
            raise NotImplementedError()
    return(mean_var_src)

if __name__ == '__main__':
    pass
