#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Preprocess (or derive) variables specific for different models
author			Christoph Heim
date created    25.11.2019
date changed    12.07.2022
usage           use from another script.
"""
###############################################################################
import copy, os
import numpy as np
import xarray as xr
import metpy.calc as mpcalc
from metpy.units import units
from numba import jit, njit
import matplotlib.pyplot as plt
from package.constants import (
    CON_M_PER_DEG,CON_G,CON_RD,CON_RV,CON_CP_AIR,CON_LH_EVAP,
    )
from base.nl_global import model_specifics_path
from package.model_pp import MODEL_PP, MODEL_PP_DONE, interp_logp_4d
from package.utilities import Timer, select_common_timesteps, dt64_to_dt
from package.nl_variables import add_var_attributes
from package.external.lcl import lcl
from package.nl_models import models_cmip6
###############################################################################

DIRECT = 'direct'
DERIVE = 'derive'

VAR_PP        = 'var_pp'
VAR_PP_DONE   = 'done'

CON_RE = 6371000

## "model key" for reference fields that should be used for
## computations of fields in other simulations
## (e.g. SWDTOA to compute SWUTOA from SWNDTOA in other fields)
#__REF = '__REFERENCE'

#####
direct_vars = [
    'QC', 'QI', 'QR', 'QG', 'QS', 
    'T', 'P', 'W', 'PS', #'SWUTOA',
    'SWDTOA', 
    'SWDIFDSFC', 'SWDIRDSFC',
    'LWUTOA', 'CLWUTOA', 'LWDTOA', 'CLWDTOA',
    'TSURF', 'QV2M', 'TQV',
]
equally_derived_vars = {
    'dRHdt':                ['QVDIV','POTTDIV','T','QV','P'],
    'dRHdt_MBL_FLX':        ['dQVdt_MBL_LH','dTdt_MBL_SH','T','QV','P'],
    'SWNUSFC':              ['SWNDSFC'],
    'CRESWNDTOA':           ['SWNDTOA', 'CSWNDTOA'],
    'CRESWNDSFC':           ['SWNDSFC', 'CSWNDSFC'],

    'LWDTOA':               ['LWUTOA'],
    'LWNUSFC':              ['LWNDSFC'],
    'CLWDTOA':              ['CLWUTOA'],
    'CRELWUTOA':            ['LWUTOA', 'CLWUTOA'],
    'CRELWDTOA':            ['LWDTOA', 'CLWDTOA'],
    'CRELWNDSFC':           ['LWNDSFC', 'CLWNDSFC'],
    'LWDIVATM':             ['LWUTOA', 'LWNDSFC'],
    'CLWDIVATM':            ['CLWUTOA', 'CLWNDSFC'],
    'CRELWDIVATM':          ['LWUTOA','CLWUTOA','LWNDSFC','CLWNDSFC'],

    'RADNDTOA':             ['SWNDTOA', 'LWDTOA'],
    'CRADNDTOA':            ['CSWNDTOA', 'CLWDTOA'],
    'CRERADNDTOA':          ['RADNDTOA', 'CRADNDTOA'],

    'BUOYIFLX':             ['W','POTTV','TV'],
    'BUOYIFLXNORMI':        ['BUOYIFLX', 'INVHGT'],
    'AQV':                  ['QV', 'RHO'],
    'AQI':                  ['QI', 'RHO'],
    'CLDQX':                ['QC', 'QI'],
    'UV':                   ['U', 'V'],
    'UVDIV':                ['U', 'V'],
    'CSUVDIV':              ['UVDIV', 'CLDF'],
    'CLDUVDIV':             ['UVDIV', 'CLDF'],
    'UVFLXDIV':             ['U', 'V', 'RHO'],
    'UVFLXDIVNORMI':        ['UVFLXDIV', 'INVHGT'],
    'UNORMI':               ['U', 'INVHGT'],
    'VNORMI':               ['V', 'INVHGT'],
    'UVNORMI':              ['UV', 'INVHGT'],
    'UFLX':                 ['U', 'RHO'],
    'VFLX':                 ['V', 'RHO'],
    'WFLX':                 ['W', 'RHO'],
    'CLDWFLX':              ['WFLX','CLDF'],
    'CSWFLX':               ['WFLX','CLDF'],
    'CLDWFLXLCL':           ['CLDWFLX','LCL'],
    'CLDWFLXLOWCLDBASE':    ['CLDWFLX','LOWCLDBASE'],
    'CSWFLXLOWCLDBASE':     ['CSWFLX','LOWCLDBASE'],
    'WFLXI':                ['WFLX', 'INVHGT'],
    'WTURB':                ['W'],
    'WTURBNORMI':           ['WTURB', 'INVHGT'],
    'WTURBNORMISCI':        ['WTURBNORMI', 'INVHGT'],
    'ENTR':                 ['ENTRH', 'ENTRV'],
    'ENTRV':                ['W','INVHGT'],
    'ENTRH':                ['U', 'V', 'INVHGT'],
    'ENTRSCL':              ['ENTRHSCL', 'ENTRVSCL'],
    'ENTRVSCL':             ['W', 'LCL'],
    'ENTRHSCL':             ['U', 'V', 'LCL'],
    'UI':                   ['U', 'INVHGT'],
    'VI':                   ['V', 'INVHGT'],
    'WI':                   ['W', 'INVHGT'],
    'WNORMI':               ['W', 'INVHGT'],
    'WMBLI':                ['W', 'INVHGT'],
    'AW':                   ['W'],
    'AWU':                  ['W'],
    'AWD':                  ['W'],
    'AWNORMI':              ['AW', 'INVHGT'],
    'AWUNORMI':             ['AWU', 'INVHGT'],
    'AWDNORMI':             ['AWD', 'INVHGT'],
    'AWMBLI':               ['AW', 'INVHGT'],
    'KEW':                  ['W', 'RHO'],
    'KEWNORMI':             ['KEW', 'INVHGT'],
    'KEWMBLI':              ['KEW', 'INVHGT'],
    'TKE':                  ['U', 'V', 'W'],
    'TKEV':                 ['W'],
    'TKENORMI':             ['TKE', 'INVHGT'],
    'TKEVNORMI':            ['TKEV', 'INVHGT'],
    'WFLXNORMI':            ['WFLX', 'INVHGT'],
    'QVNORMI':              ['QV', 'INVHGT'],
    'QVVFLX':               ['QV', 'V', 'RHO'],
    'QVWFLX':               ['QV', 'W', 'RHO'],
    'QVWFLXINV':            ['QVWFLX','INVHGT'],
    #'QVUFLX':               ['QV', 'U', 'RHO'],
    #'QVVFLX':               ['QV', 'V', 'RHO'],
    'QCNORMI':              ['QC', 'INVHGT'],
    'TV':                   ['T', 'QV'],
    'UPDTV':                ['TV','CLDF','W'],
    'UPDT':                 ['T','CLDF','W'],
    'UPDTDEW':              ['TDEW','CLDF','W'],
    'UPD2TV':               ['TV','CLDF','W'],
    'UPD2T':                ['T','CLDF','W'],
    'UPD2TDEW':             ['TDEW','CLDF','W'],
    'POTT':                 ['T', 'P'],
    'POTTV':                ['POTT', 'QV'],
    'TDEW':                 ['T', 'P', 'RH'],
    'EQPOTT':               ['T', 'P', 'RH'],
    'POTTHDIVMBLI':         ['POTTHDIV', 'INVHGT', 'RHO'],
    'POTTMBLI':             ['POTT', 'INVHGT', 'RHO'],
    'POTTVDIVWPOS':         ['POTT', 'W'],
    'POTTVDIVWNEG':         ['POTT', 'W'],
    'BVF':                  ['POTTV'],
    'BVFNORMI':             ['BVF', 'INVHGT'],
    'LTS':                  ['POTT', 'P'],
    'EIS':                  ['LTS','T','P','LCL'],
    'LCL':                  ['RH', 'T', 'P'],
    'LCLNORMI':             ['LCL', 'INVHGT'],
    'DCLDBASELCL':          ['LCL', 'LOWCLDBASE'],
    'DCLDTOPINVHGT':        ['INVHGT', 'LCLDTOP'],
    'DINVHGTLCL':           ['INVHGT', 'LCL'],
    'DINVHGTLOWCLDBASE':    ['INVHGT', 'LOWCLDBASE'],
    'PVAPSATL':             ['T'],
    'PVAPSATS':             ['T'],
    'QVSAT':                ['T','P'],
    'QVSATDEF':             ['T','P','QV'],
    'QVSATDEFNORMI':        ['QVSATDEF', 'INVHGT'],
    'PVAP':                 ['P', 'QV'],
    'RHNORMI':              ['RH', 'INVHGT'],
    'DIABH':                ['POTTHDIV', 'POTTVDIV'],
    'DIABHNORMI':           ['DIABH', 'INVHGT'],
    'DIABM':                ['QVHDIV', 'QVVDIV'],
    'DIABMNORMI':           ['DIABM', 'INVHGT'],

    'POTTHDIV':             ['POTT','U','V'],
    'POTTXDIV':             ['POTT','U'],
    'POTTYDIV':             ['POTT','V'],
    'POTTVDIV':             ['POTT','W'],
    'POTTDIV':              ['POTTHDIV', 'POTTVDIV'],
    'POTTHDIV2':            ['POTT', 'U', 'V'],
    'POTTVDIV2':            ['POTT', 'W'],
    'POTTDIV2':             ['POTTHDIV2', 'POTTVDIV2'],
    'POTTHDIV3':            ['POTT', 'U', 'V'],
    'POTTVDIV3':            ['POTT', 'W'],
    'POTTDIV3':             ['POTTHDIV3', 'POTTVDIV3'],
    'POTTHDIV4':            ['POTT','UFLX','VFLX','RHO'],
    'POTTVDIV4':            ['POTT','WFLX','RHO'],
    'POTTDIV4':             ['POTTHDIV4', 'POTTVDIV4'],
    'EQPOTTHDIV':           ['EQPOTT', 'U', 'V'],
    'EQPOTTVDIV':           ['EQPOTT', 'W'],
    'EQPOTTDIV':            ['EQPOTTHDIV', 'EQPOTTVDIV'],
    'EQPOTTHDIV3':          ['EQPOTT', 'U', 'V'],
    'EQPOTTVDIV3':          ['EQPOTT', 'W'],
    'EQPOTTDIV3':           ['EQPOTTHDIV3', 'EQPOTTVDIV3'],
    'LATH':                 ['EQPOTTDIV', 'POTTDIV'],
    'QVHDIV':               ['QV','U','V'],
    'QVXDIV':               ['QV','U',],
    'QVYDIV':               ['QV','V'],
    'QVVDIV':               ['QV','W'],
    'QVDIV':                ['QVHDIV', 'QVVDIV'],
    'QVHDIV2':              ['QV', 'U', 'V'],
    'QVVDIV2':              ['QV', 'W'],
    'QVDIV2':               ['QVHDIV2', 'QVVDIV2'],
    'QVHDIV3':              ['QV', 'U', 'V'],
    'QVVDIV3':              ['QV', 'W'],
    'QVDIV3':               ['QVHDIV3', 'QVVDIV3'],
    'QCHDIV':               ['QC', 'U', 'V'],
    'QCVDIV':               ['QC', 'W'],
    'QCDIV':                ['QCHDIV', 'QCVDIV'],
    'QIHDIV3':              ['QI', 'U', 'V'],
    'QIVDIV3':              ['QI', 'W'],
    'QIDIV3':               ['QIHDIV3', 'QIVDIV3'],
    'AQVHDIV3':             ['AQV', 'U', 'V'],
    'WVPHCONV':             ['AQVHDIV3'],
    'AQIHDIV3':             ['AQI', 'U', 'V'],
    'IWPHCONV':             ['AQIHDIV3'],

    'POTTHDIVNORMI':        ['POTTHDIV', 'INVHGT'],
    'POTTVDIVNORMI':        ['POTTVDIV', 'INVHGT'],
    'POTTDIVNORMI':         ['POTTDIV', 'INVHGT'],
    'POTTHDIV3NORMI':       ['POTTHDIV3', 'INVHGT'],
    'POTTVDIV3NORMI':       ['POTTVDIV3', 'INVHGT'],
    'POTTDIV3NORMI':        ['POTTDIV3', 'INVHGT'],
    'EQPOTTDIVNORMI':       ['EQPOTTDIV', 'INVHGT'],
    'LATHNORMI':            ['LATH', 'INVHGT'],
    'QVHDIVNORMI':          ['QVHDIV', 'INVHGT'],
    'QVVDIVNORMI':          ['QVVDIV', 'INVHGT'],
    'QVDIVNORMI':           ['QVDIV', 'INVHGT'],
    'QVHDIV2NORMI':         ['QVHDIV2', 'INVHGT'],
    'QVVDIV2NORMI':         ['QVVDIV2', 'INVHGT'],
    'QVDIV2NORMI':          ['QVDIV2', 'INVHGT'],
    'QVHDIV3NORMI':         ['QVHDIV3', 'INVHGT'],
    'QVVDIV3NORMI':         ['QVVDIV3', 'INVHGT'],
    'QVDIV3NORMI':          ['QVDIV3', 'INVHGT'],
    'QCHDIVNORMI':          ['QCHDIV', 'INVHGT'],
    'QCVDIVNORMI':          ['QCVDIV', 'INVHGT'],
    'QCDIVNORMI':           ['QCDIV', 'INVHGT'],

    'CLDPOTTHDIV':          ['POTTHDIV', 'CLDF'],
    'CLDPOTTVDIV':          ['POTTVDIV', 'CLDF'],
    'CLDPOTTDIV':           ['POTTDIV', 'CLDF'],
    'CLDPOTTHDIV3':         ['POTTHDIV3', 'CLDF'],
    'CLDPOTTVDIV3':         ['POTTVDIV3', 'CLDF'],
    'CLDPOTTDIV3':          ['POTTDIV3', 'CLDF'],
    'CLDEQPOTTDIV':         ['EQPOTTDIV', 'CLDF'],
    'CLDEQPOTTDIV3':        ['EQPOTTDIV3', 'CLDF'],
    'CLDLATH':              ['LATH', 'CLDF'],
    'CLDQVHDIV':            ['QVHDIV', 'CLDF'],
    'CLDQVVDIV':            ['QVVDIV', 'CLDF'],
    'CLDQVDIV':             ['QVDIV', 'CLDF'],
    'CLDQVHDIV2':           ['QVHDIV2', 'CLDF'],
    'CLDQVVDIV2':           ['QVVDIV2', 'CLDF'],
    'CLDQVDIV2':            ['QVDIV2', 'CLDF'],
    'CLDQVHDIV3':           ['QVHDIV3', 'CLDF'],
    'CLDQVVDIV3':           ['QVVDIV3', 'CLDF'],
    'CLDQVDIV3':            ['QVDIV3', 'CLDF'],
    'CLDQCHDIV':            ['QCHDIV', 'CLDF'],
    'CLDQCVDIV':            ['QCVDIV', 'CLDF'],
    'CLDQCDIV':             ['QCDIV', 'CLDF'],

    'CLDPOTTHDIVNORMI':     ['CLDPOTTHDIV', 'INVHGT'],
    'CLDPOTTVDIVNORMI':     ['CLDPOTTVDIV', 'INVHGT'],
    'CLDPOTTDIVNORMI':      ['CLDPOTTDIV', 'INVHGT'],
    'CLDPOTTDIV3NORMI':     ['CLDPOTTDIV3', 'INVHGT'],
    'CLDEQPOTTDIVNORMI':    ['CLDEQPOTTDIV', 'INVHGT'],
    'CLDLATHNORMI':         ['CLDLATH', 'INVHGT'],
    'CLDQVHDIVNORMI':       ['CLDQVHDIV', 'INVHGT'],
    'CLDQVVDIVNORMI':       ['CLDQVVDIV', 'INVHGT'],
    'CLDQVDIVNORMI':        ['CLDQVDIV', 'INVHGT'],
    'CLDQVHDIV2NORMI':      ['CLDQVHDIV2', 'INVHGT'],
    'CLDQVVDIV2NORMI':      ['CLDQVVDIV2', 'INVHGT'],
    'CLDQVDIV2NORMI':       ['CLDQVDIV2', 'INVHGT'],
    'CLDQVHDIV3NORMI':      ['CLDQVHDIV3', 'INVHGT'],
    'CLDQVVDIV3NORMI':      ['CLDQVVDIV3', 'INVHGT'],
    'CLDQVDIV3NORMI':       ['CLDQVDIV3', 'INVHGT'],
    'CLDQCHDIVNORMI':       ['CLDQCHDIV', 'INVHGT'],
    'CLDQCVDIVNORMI':       ['CLDQCVDIV', 'INVHGT'],
    'CLDQCDIVNORMI':        ['CLDQCDIV', 'INVHGT'],

    'CSPOTTHDIV':           ['POTTHDIV', 'CLDF'],
    'CSPOTTVDIV':           ['POTTVDIV', 'CLDF'],
    'CSPOTTDIV':            ['POTTDIV', 'CLDF'],
    'CSPOTTHDIV3':          ['POTTHDIV3', 'CLDF'],
    'CSPOTTVDIV3':          ['POTTVDIV3', 'CLDF'],
    'CSPOTTDIV3':           ['POTTDIV3', 'CLDF'],
    'NCOLIPOTTDIV':         ['POTTDIV', 'TQI'],
    'NCOLIPOTTDIV3':        ['POTTDIV3', 'TQI'],
    'NCOLIQV':              ['QV', 'TQI'],
    'RH0LCSPOTTDIV3':       ['POTTDIV3','CLDF','RH'],
    'RH1LCSPOTTDIV3':       ['POTTDIV3','CLDF','RH'],
    'RH2LCSPOTTDIV3':       ['POTTDIV3','CLDF','RH'],
    'RH0GCSPOTTDIV3':       ['CSPOTTDIV3','RH'],
    'RH1GCSPOTTDIV3':       ['CSPOTTDIV3','RH'],
    'RH2GCSPOTTDIV3':       ['CSPOTTDIV3','RH'],
    'CSEQPOTTDIV':          ['EQPOTTDIV', 'CLDF'],
    'CSEQPOTTDIV3':         ['EQPOTTDIV3', 'CLDF'],
    'CSLATH':               ['LATH', 'CLDF'],
    'CSQVHDIV':             ['QVHDIV', 'CLDF'],
    'CSQVVDIV':             ['QVVDIV', 'CLDF'],
    'CSQVDIV':              ['QVDIV', 'CLDF'],
    'CSQVHDIV2':            ['QVHDIV2', 'CLDF'],
    'CSQVVDIV2':            ['QVVDIV2', 'CLDF'],
    'CSQVDIV2':             ['QVDIV2', 'CLDF'],
    'CSQVHDIV3':            ['QVHDIV3', 'CLDF'],
    'CSQVVDIV3':            ['QVVDIV3', 'CLDF'],
    'CSQVDIV3':             ['QVDIV3', 'CLDF'],
    'CSQCHDIV':             ['QCHDIV', 'CLDF'],
    'CSQCVDIV':             ['QCVDIV', 'CLDF'],
    'CSQCDIV':              ['QCDIV', 'CLDF'],

    'CSPOTTHDIVNORMI':      ['CSPOTTHDIV', 'INVHGT'],
    'CSPOTTVDIVNORMI':      ['CSPOTTVDIV', 'INVHGT'],
    'CSPOTTDIVNORMI':       ['CSPOTTDIV', 'INVHGT'],
    'CSPOTTDIV3NORMI':      ['CSPOTTDIV3', 'INVHGT'],
    'CSEQPOTTDIVNORMI':     ['CSEQPOTTDIV', 'INVHGT'],
    'CSLATHNORMI':          ['CSLATH', 'INVHGT'],
    'CSQVHDIVNORMI':        ['CSQVHDIV', 'INVHGT'],
    'CSQVVDIVNORMI':        ['CSQVVDIV', 'INVHGT'],
    'CSQVDIVNORMI':         ['CSQVDIV', 'INVHGT'],
    'CSQVHDIV2NORMI':       ['CSQVHDIV2', 'INVHGT'],
    'CSQVVDIV2NORMI':       ['CSQVVDIV2', 'INVHGT'],
    'CSQVDIV2NORMI':        ['CSQVDIV2', 'INVHGT'],
    'CSQVHDIV3NORMI':       ['CSQVHDIV3', 'INVHGT'],
    'CSQVVDIV3NORMI':       ['CSQVVDIV3', 'INVHGT'],
    'CSQVDIV3NORMI':        ['CSQVDIV3', 'INVHGT'],
    'CSQCHDIVNORMI':        ['CSQCHDIV', 'INVHGT'],
    'CSQCVDIVNORMI':        ['CSQCVDIV', 'INVHGT'],
    'CSQCDIVNORMI':         ['CSQCDIV', 'INVHGT'],

    'POTTHDIVMEAN':         [],
    'POTTVDIVMEAN':         [],
    'POTTDIVMEAN':          [],
    'QVHDIVMEAN':           [],
    'QVVDIVMEAN':           [],
    'QVDIVMEAN':            [],
    'QCHDIVMEAN':           [],
    'QCVDIVMEAN':           [],
    'QCDIVMEAN':            [],

    'POTTHDIVMEANNORMI':    [],
    'POTTVDIVMEANNORMI':    [],
    'POTTDIVMEANNORMI':     [],
    'QVHDIVMEANNORMI':      [],
    'QVVDIVMEANNORMI':      [],
    'QVDIVMEANNORMI':       [],
    'QVHDIV2MEANNORMI':     [],
    'QVVDIV2MEANNORMI':     [],
    'QVDIV2MEANNORMI':      [],
    'QVHDIV3MEANNORMI':     [],
    'QVVDIV3MEANNORMI':     [],
    'QVDIV3MEANNORMI':      [],
    'QCHDIVMEANNORMI':      [],
    'QCVDIVMEANNORMI':      [],
    'QCDIVMEANNORMI':       [],

    'POTTHDIVTURB':         ['POTTHDIV'],
    'POTTVDIVTURB':         ['POTTVDIV'],
    'POTTDIVTURB':          ['POTTDIV'],
    'QVHDIVTURB':           ['QVHDIV'],
    'QVVDIVTURB':           ['QVVDIV'],
    'QVUVDIVTURB':          ['QVVDIV','W'],
    'QVDVDIVTURB':          ['QVVDIV','W'],
    'QVDIVTURB':            ['QVDIV'],
    'QVHDIV2TURB':          ['QVHDIV2'],
    'QVVDIV2TURB':          ['QVVDIV2'],
    'QVDIV2TURB':           ['QVDIV2'],
    'QVHDIV3TURB':          ['QVHDIV3'],
    'QVVDIV3TURB':          ['QVVDIV3'],
    'QVDIV3TURB':           ['QVDIV3'],
    'QCHDIVTURB':           ['QCHDIV'],
    'QCVDIVTURB':           ['QCVDIV'],
    'QCDIVTURB':            ['QCDIV'],

    'POTTHDIVTURBNORMI':    ['POTTHDIVTURB', 'INVHGT'],
    'POTTVDIVTURBNORMI':    ['POTTVDIVTURB', 'INVHGT'],
    'POTTDIVTURBNORMI':     ['POTTDIVTURB', 'INVHGT'],
    'QVHDIVTURBNORMI':      ['QVHDIVTURB', 'INVHGT'],
    'QVVDIVTURBNORMI':      ['QVVDIVTURB', 'INVHGT'],
    'QVHDIV2TURBNORMI':     ['QVHDIV2TURB', 'INVHGT'],
    'QVVDIV2TURBNORMI':     ['QVVDIV2TURB', 'INVHGT'],
    'QVHDIV3TURBNORMI':     ['QVHDIV3TURB', 'INVHGT'],
    'QVVDIV3TURBNORMI':     ['QVVDIV3TURB', 'INVHGT'],
    'QVUVDIVTURBNORMI':     ['QVUVDIVTURB', 'INVHGT'],
    'QVDVDIVTURBNORMI':     ['QVDVDIVTURB', 'INVHGT'],
    'QVDIVTURBNORMI':       ['QVDIVTURB', 'INVHGT'],
    'QVDIV2TURBNORMI':      ['QVDIV2TURB', 'INVHGT'],
    'QVDIV3TURBNORMI':      ['QVDIV3TURB', 'INVHGT'],
    'QCHDIVTURBNORMI':      ['QCHDIVTURB', 'INVHGT'],
    'QCVDIVTURBNORMI':      ['QCVDIVTURB', 'INVHGT'],
    'QCDIVTURBNORMI':       ['QCDIVTURB', 'INVHGT'],

    'CLDPOTTHDIVTURB':      ['POTTHDIVTURB', 'CLDF'],
    'CLDPOTTVDIVTURB':      ['POTTVDIVTURB', 'CLDF'],
    'CLDPOTTDIVTURB':       ['POTTDIVTURB', 'CLDF'],
    'CLDQVHDIVTURB':        ['QVHDIVTURB', 'CLDF'],
    'CLDQVVDIVTURB':        ['QVVDIVTURB', 'CLDF'],
    'CLDQVHDIV2TURB':       ['QVHDIV2TURB', 'CLDF'],
    'CLDQVVDIV2TURB':       ['QVVDIV2TURB', 'CLDF'],
    'CLDQVHDIV3TURB':       ['QVHDIV3TURB', 'CLDF'],
    'CLDQVVDIV3TURB':       ['QVVDIV3TURB', 'CLDF'],
    'CLDQVUVDIVTURB':       ['QVUVDIVTURB', 'CLDF'],
    'CLDQVDVDIVTURB':       ['QVDVDIVTURB', 'CLDF'],
    'CLDQVDIVTURB':         ['QVDIVTURB', 'CLDF'],
    'CLDQVDIV2TURB':        ['QVDIV2TURB', 'CLDF'],
    'CLDQVDIV3TURB':        ['QVDIV3TURB', 'CLDF'],
    'CLDQCHDIVTURB':        ['QCHDIVTURB', 'CLDF'],
    'CLDQCVDIVTURB':        ['QCVDIVTURB', 'CLDF'],
    'CLDQCDIVTURB':         ['QCDIVTURB', 'CLDF'],

    'CLDPOTTHDIVTURBNORMI': ['CLDPOTTHDIVTURB', 'INVHGT'],
    'CLDPOTTVDIVTURBNORMI': ['CLDPOTTVDIVTURB', 'INVHGT'],
    'CLDPOTTDIVTURBNORMI':  ['CLDPOTTDIVTURB', 'INVHGT'],
    'CLDQVHDIVTURBNORMI':   ['CLDQVHDIVTURB', 'INVHGT'],
    'CLDQVVDIVTURBNORMI':   ['CLDQVVDIVTURB', 'INVHGT'],
    'CLDQVHDIV2TURBNORMI':  ['CLDQVHDIV2TURB', 'INVHGT'],
    'CLDQVVDIV2TURBNORMI':  ['CLDQVVDIV2TURB', 'INVHGT'],
    'CLDQVHDIV3TURBNORMI':  ['CLDQVHDIV3TURB', 'INVHGT'],
    'CLDQVVDIV3TURBNORMI':  ['CLDQVVDIV3TURB', 'INVHGT'],
    'CLDQVUVDIVTURBNORMI':  ['CLDQVUVDIVTURB', 'INVHGT'],
    'CLDQVDVDIVTURBNORMI':  ['CLDQVDVDIVTURB', 'INVHGT'],
    'CLDQVDIVTURBNORMI':    ['CLDQVDIVTURB', 'INVHGT'],
    'CLDQVDIV2TURBNORMI':   ['CLDQVDIV2TURB', 'INVHGT'],
    'CLDQVDIV3TURBNORMI':   ['CLDQVDIV3TURB', 'INVHGT'],
    'CLDQCHDIVTURBNORMI':   ['CLDQCHDIVTURB', 'INVHGT'],
    'CLDQCVDIVTURBNORMI':   ['CLDQCVDIVTURB', 'INVHGT'],
    'CLDQCDIVTURBNORMI':    ['CLDQCDIVTURB', 'INVHGT'],

    'CSPOTTHDIVTURB':       ['POTTHDIVTURB', 'CLDF'],
    'CSPOTTVDIVTURB':       ['POTTVDIVTURB', 'CLDF'],
    'CSPOTTDIVTURB':        ['POTTDIVTURB', 'CLDF'],
    'CSQVHDIVTURB':         ['QVHDIVTURB', 'CLDF'],
    'CSQVVDIVTURB':         ['QVVDIVTURB', 'CLDF'],
    'CSQVHDIV2TURB':        ['QVHDIV2TURB', 'CLDF'],
    'CSQVVDIV2TURB':        ['QVVDIV2TURB', 'CLDF'],
    'CSQVHDIV3TURB':        ['QVHDIV3TURB', 'CLDF'],
    'CSQVVDIV3TURB':        ['QVVDIV3TURB', 'CLDF'],
    'CSQVUVDIVTURB':        ['QVUVDIVTURB', 'CLDF'],
    'CSQVDVDIVTURB':        ['QVDVDIVTURB', 'CLDF'],
    'CSQVDIVTURB':          ['QVDIVTURB', 'CLDF'],
    'CSQVDIV2TURB':         ['QVDIV2TURB', 'CLDF'],
    'CSQVDIV3TURB':         ['QVDIV3TURB', 'CLDF'],
    'CSQCHDIVTURB':         ['QCHDIVTURB', 'CLDF'],
    'CSQCVDIVTURB':         ['QCVDIVTURB', 'CLDF'],
    'CSQCDIVTURB':          ['QCDIVTURB', 'CLDF'],

    'CSPOTTHDIVTURBNORMI':  ['CSPOTTHDIVTURB', 'INVHGT'],
    'CSPOTTVDIVTURBNORMI':  ['CSPOTTVDIVTURB', 'INVHGT'],
    'CSPOTTDIVTURBNORMI':   ['CSPOTTDIVTURB', 'INVHGT'],
    'CSQVHDIVTURBNORMI':    ['CSQVHDIVTURB', 'INVHGT'],
    'CSQVVDIVTURBNORMI':    ['CSQVVDIVTURB', 'INVHGT'],
    'CSQVHDIV2TURBNORMI':   ['CSQVHDIV2TURB', 'INVHGT'],
    'CSQVVDIV2TURBNORMI':   ['CSQVVDIV2TURB', 'INVHGT'],
    'CSQVHDIV3TURBNORMI':   ['CSQVHDIV3TURB', 'INVHGT'],
    'CSQVVDIV3TURBNORMI':   ['CSQVVDIV3TURB', 'INVHGT'],
    'CSQVUVDIVTURBNORMI':   ['CSQVUVDIVTURB', 'INVHGT'],
    'CSQVDVDIVTURBNORMI':   ['CSQVDVDIVTURB', 'INVHGT'],
    'CSQVDIVTURBNORMI':     ['CSQVDIVTURB', 'INVHGT'],
    'CSQVDIV2TURBNORMI':    ['CSQVDIV2TURB', 'INVHGT'],
    'CSQVDIV3TURBNORMI':    ['CSQVDIV3TURB', 'INVHGT'],
    'CSQCHDIVTURBNORMI':    ['CSQCHDIVTURB', 'INVHGT'],
    'CSQCVDIVTURBNORMI':    ['CSQCVDIVTURB', 'INVHGT'],
    'CSQCDIVTURBNORMI':     ['CSQCDIVTURB', 'INVHGT'],

    'CLDQVSATDEF':          ['QVSATDEF', 'CLDF'],
    'CLDQV':                ['QV', 'CLDF'],
    'CLDW':                 ['W', 'CLDF'],
    'CLDRH':                ['RH', 'CLDF'],
    'CLDTKEV':              ['TKEV', 'CLDF'],
    'CLDBVF':               ['BVF', 'CLDF'],

    'CLDQVSATDEFNORMI':     ['CLDQVSATDEF', 'INVHGT'],
    'CLDQVNORMI':           ['CLDQV', 'INVHGT'],
    'CLDWNORMI':            ['CLDW', 'INVHGT'],
    'CLDRHNORMI':           ['CLDRH', 'INVHGT'],
    'CLDTKEVNORMI':         ['CLDTKEV', 'INVHGT'],

    'CSQVSATDEF':           ['QVSATDEF', 'CLDF'],
    'CSQV':                 ['QV', 'CLDF'],
    'CSW':                  ['W', 'CLDF'],
    'CSRH':                 ['RH', 'CLDF'],
    'CSTKEV':               ['TKEV', 'CLDF'],
    'CSBVF':                ['BVF', 'CLDF'],

    'CSQVSATDEFNORMI':      ['CSQVSATDEF', 'INVHGT'],
    'CSQVNORMI':            ['CSQV', 'INVHGT'],
    'CSWNORMI':             ['CSW', 'INVHGT'],
    'CSRHNORMI':            ['CSRH', 'INVHGT'],
    'CSTKEVNORMI':          ['CSTKEV', 'INVHGT'],

    'DIABHMINV':            ['DIABH', 'INVHGT'],
    'TNORMI':               ['T', 'INVHGT'],
    'CLDFNORMI':            ['CLDF', 'INVHGT'],
    'POTTNORMI':            ['POTT', 'INVHGT'],
    'POTTVNORMI':           ['POTTV', 'INVHGT'],
    'PNORMI'   :            ['P', 'INVHGT'],
    'RHO':                  ['TV', 'P'],
    'RHOI':                 ['RHO', 'INVHGT'],
    'TKEMBLI':              ['TKE','INVHGT'],
    'SUBS':                 ['W'],
    'UV10M' :               ['U10M', 'V10M'],
    'U10M_W' :              ['U10M'],
    'U10M_E' :              ['U10M'],
    'V10M_S' :              ['V10M'],
    'V10M_N' :              ['V10M'],
    'ZCPTPP':               ['T'], 
    'PCPTPP':               ['P','T'], 
    'INVHGT':               ['TV'], 
    'INVF':                 ['INVHGT'], 
    'LCLDF1E-3':            ['QC'], 
    'LCLDF5E-4':            ['QC'], 
    'LCLDF2E-4':            ['QC'], 
    'LCLDF1E-4':            ['QC'], 
    'LCLDF5E-5':            ['QC'], 
    'LCLDF2E-5':            ['QC'], 
    'LCLDF1E-5':            ['QC'], 
    'ICLDF1E-3':            ['QI'], 
    'ICLDF5E-4':            ['QI'], 
    'ICLDF2E-4':            ['QI'], 
    'ICLDF1E-4':            ['QI'], 
    'ICLDF5E-5':            ['QI'], 
    'ICLDF2E-5':            ['QI'], 
    'ICLDF1E-5':            ['QI'], 
    'LCLDF1E-3NORMI':       ['LCLDF1E-3', 'INVHGT'], 
    'LCLDF5E-4NORMI':       ['LCLDF5E-4', 'INVHGT'], 
    'LCLDF2E-4NORMI':       ['LCLDF2E-4', 'INVHGT'], 
    'LCLDF1E-4NORMI':       ['LCLDF1E-4', 'INVHGT'], 
    'LCLDF5E-5NORMI':       ['LCLDF5E-5', 'INVHGT'], 
    'LCLDF2E-5NORMI':       ['LCLDF2E-5', 'INVHGT'], 
    'LCLDF1E-5NORMI':       ['LCLDF1E-5', 'INVHGT'], 
    'ICLDF1E-3NORMI':       ['ICLDF1E-3', 'INVHGT'], 
    'ICLDF5E-4NORMI':       ['ICLDF5E-4', 'INVHGT'], 
    'ICLDF2E-4NORMI':       ['ICLDF2E-4', 'INVHGT'], 
    'ICLDF1E-4NORMI':       ['ICLDF1E-4', 'INVHGT'], 
    'ICLDF5E-5NORMI':       ['ICLDF5E-5', 'INVHGT'], 
    'ICLDF2E-5NORMI':       ['ICLDF2E-5', 'INVHGT'], 
    'ICLDF1E-5NORMI':       ['ICLDF1E-5', 'INVHGT'], 
    'CLDMASKNORMI':         ['CLDMASK', 'INVHGT'], 
    'LOWCLDF':              ['CLDF', 'INVHGT'], 
    'LOWCLDBASE':           ['LOWCLDF'], 
    'LOWCLDBASENORMI':      ['LOWCLDBASE', 'INVHGT'], 
    'LCLDDEPTH':            ['INVHGT', 'LOWCLDBASE'], 
    'INVSTR':               ['T', 'POTT', 'INVHGT'], 
    'INVSTRV':              ['TV', 'POTTV', 'INVHGT'], 
    'INVSTRA':              ['T', 'POTT', 'INVHGT'], 
    'ALBEDO':               ['SWUTOA', 'SWDTOA'],
    'SLHFLX':               ['SLHFLX'],
    'dQVdt_MBL_LH':         ['SLHFLX','INVHGT'],
    'dTdt_MBL_SH':          ['SSHFLX','INVHGT'],
    'SSHFLX':               ['SSHFLX'],
    'SBUOYIFLX':            ['SLHFLX','SSHFLX'],
    'ENFLXNUSFC':           ['SSHFLX', 'SLHFLX', 'LWNUSFC', 'SWNUSFC'],
    'TQC':                  ['TQC'],
    'TQI':                  ['TQI'],
    #'QVFLXZCB':             ['CLDBASE', 'QVWFLX'],
    'CLCW':                 ['TQC'], 
    'CLCI':                 ['TQI'], 
}
members = [
        # MODELS
        'COSMO', 'INT2LM',
        'NICAM', 'SAM', 'ICON', 'UM', 'MPAS',
        'IFS' ,'GEOS', 'ARPEGE-NH', 'FV3',
        'cmip6', 
        # OBSERVATIONS
        'SUOMI_NPP_VIIRS', 'RADIO_SOUNDING',
        'CM_SAF_METEOSAT', 'CM_SAF_MSG_AQUA_TERRA', 
        'CM_SAF_MSG', 'CERES_EBAF', 'GPM_IMERG', 'CMORPH',
        'ERA5', 'MPI-ESM1-2-HR']


# specifically dervied variables
var_mapping = {
    ###### MODELS
    'COSMO':{
        'RH':               ['PVAP', 'PVAPSATL', 'PVAPSATS', 'T'],
        'CLDF'  :           ['CLDQX'],
        'U'     :           ['U'],
        'V'     :           ['V'],
        #'P'     :           ['P'],
        'QV'    :           ['QV'],
        'SWUTOA':           ['SWNDTOA', 'SWDTOA'],
        'CSWUTOA':          ['SWDTOA', 'CSWNDTOA'],
        'SWUSFC':           ['SWDIFUSFC'],
        'SWNDTOA':          ['SWNDTOA'],
        'CSWNDTOA':         ['CSWNDTOA'],
        'SWNDSFC':          ['SWNDSFC'],
        'SWDSFC':           ['SWDIFDSFC', 'SWDIRDSFC'],
        'LWUSFC':           ['LWNDSFC', 'LWDSFC'],
        'CLWDSFC':          ['CLWNDSFC', 'LWUSFC'],
        'LWNDSFC':          ['LWNDSFC'],
        'PP'    :           ['PP'],
        'CORREFL':          ['TQC'],
        #'CLCL':            ['CLCL', 'CLCM', 'CLCH', 'TQI'],
        'CLCL':             ['CLCL'],
        'CLCL2':            ['TQC'], 
        'CLCT':             ['CLCL', 'CLCM', 'CLCH'], 
        #'TQV':              ['QV', 'RHO'],
        'DQVINV':           ['QVNORMI'],
        #'ENTRDRY':          ['DQVINV','ENTR','INVHGT'],
        'ENTRDRY':          ['DQVINV','ENTR','RHOI'],
        'TQVFT':            ['QV', 'RHO', 'INVHGT'],
        'SST':              ['TSURF'],
        'SUBSOMEGA':        ['W','P'],
    },
    'INT2LM':{
        'U'     :       ['U'],
        'V'     :       ['V'],
        #'P'     :       ['PPERT'],
        'QV'    :       ['QV'],
    },
    'NICAM':{
        'U'     :['U'],
        'V'     :['V'],
        'P'     :['P'],
        'SWUTOA':['SWUTOA'],
        'PP'    :['PP'],
        'CORREFL':  ['TQC'],
        'CLCL':     ['CLCL'], # not available
        'CLCL2':    ['TQC'], 
        'TQV':          ['QV', 'RHO'],
        'TQVFT':        ['QV', 'RHO', 'INVHGT'],
    },
    'SAM':{
        'U'     :['U'],
        'V'     :['V'],
        'P'     :['P'],
        'SWUTOA':['SWNDTOA','SWDTOA'],
        'PP'    :['PP'],
        'CORREFL':  ['TQC'],
        'CLCL':     ['CLCL'], # not available
        'CLCL2':    ['TQC'], 
        'TQV':          ['QV', 'RHO'],
        'TQVFT':        ['QV', 'RHO', 'INVHGT'],
    },
    'ICON':{
        'U'     :['U'],
        'V'     :['V'],
        'P'     :['P'],
        'SWUTOA':['SWNDTOA','SWDTOA'],
        'PP'    :['PP'],
        'CORREFL':  ['TQC'],
        'CLCL':     ['CLCT', 'TQI'], 
        'CLCL2':    ['TQC'], 
        'TQV':          ['QV', 'RHO'],
        'TQVFT':        ['QV', 'RHO', 'INVHGT'],
    },
    'UM':{
        'U'     :['U', 'TQC'],
        'V'     :['V', 'TQC'],
        'P'     :['P'],
        'SWUTOA':['SWUTOA'],
        'PP'    :['PP'],
        'CORREFL':  ['TQC'],
        'CLCL':     ['CLCT', 'TQI'], 
        'CLCL2':    ['TQC'], 
        'TQV':          ['QV', 'RHO'],
        'TQVFT':        ['QV', 'RHO', 'INVHGT'],
    },
    'MPAS':{
        'U'     :['U'],
        'V'     :['V'],
        'P'     :['P'],
        'SWUTOA':['SWNDTOA','SWDTOA'],
        'PP'    :['PPGRID', 'PPCONV'],
        'CORREFL':  ['TQC'],
        'CLCL':     ['CLCT', 'TQI'],
        'CLCL2':    ['TQC'], 
        'TQV':          ['QV', 'RHO'],
        'TQVFT':        ['QV', 'RHO', 'INVHGT'],
    },
    'IFS':{
        'U'     :['U'],
        'V'     :['V'],
        'P'     :['QV', 'T', 'PS'],
        'H'     :['QV', 'T', 'PS'],
        'SWUTOA':['SWNDTOA','SWDTOA'],
        'PP'    :['PPGRID', 'PPCONV'],
        'CORREFL':  ['TQC'],
        'CLCL':     ['CLCL'],
        'CLCL2':    ['TQC'], 
        'TQV':          ['QV', 'RHO'],
        'TQVFT':        ['QV', 'RHO', 'INVHGT'],
    },
    'GEOS':{
        'U'     :['U'],
        'V'     :['V'],
        'P'     :['P'],
        'SWUTOA':['SWNDTOA','SWDTOA'],
        'PP'    :['PP'],
        'CORREFL':  ['TQC'],
        'CLCL':     ['CLCL'], # not available
        'CLCL2':    ['TQC'], 
        'TQV':          ['QV', 'RHO'],
        'TQVFT':        ['QV', 'RHO', 'INVHGT'],
    },
    'ARPEGE-NH':{
        'U'     :['U'],
        'V'     :['V'],
        'P'     :['QV', 'PS'],
        'SWUTOA':['SWNDTOA','SWDTOA'],
        'PP'    :['PP'],
        'CORREFL':  ['TQC'],
        #'CLCL':     ['CLCL', 'CLCT', 'TQI'], 
        'CLCL':     ['CLCL'], 
        'CLCL2':    ['TQC'], 
        'TQV':          ['QV', 'RHO'],
        'TQVFT':        ['QV', 'RHO', 'INVHGT'],
    },
    'FV3':{
        'U'     :['U'],
        'V'     :['V'],
        'P'     :['T'],
        'SWUTOA':['SWUTOA'],
        'PP'    :['PP'],
        'CORREFL':  ['TQC'],
        'CLCL':         ['CLCT', 'TQI'], 
        'CLCL2':        ['TQC'], 
        'TQV':          ['QV', 'RHO'],
        'TQVFT':        ['QV', 'RHO', 'INVHGT'],
    },
    ###### OBSERVATIONS
    'CM_SAF_MSG':{
        'SWUTOA':       ['SWUTOA'],
        'CLCL'  :       ['CLCL'],
        'CLCL2' :       ['CLCL2'],
    },
    'CM_SAF_MSG_AQUA_TERRA':{
        'SWUTOA':       ['SWUTOA'],
        'SWNDTOA':      ['SWDTOA', 'SWUTOA'],
    },
    'CERES_EBAF':{
        'SWUTOA':       ['SWUTOA'],
        'CSWUTOA':      ['CSWUTOA'],
        'SWNDTOA':      ['SWDTOA', 'SWUTOA'],
        'CSWNDTOA':     ['SWDTOA', 'CSWUTOA'],
        'CLCT':         ['CLCT'], 
    },
    'CM_SAF_METEOSAT':{
        'SWUTOA':       ['SWUTOA'],
    },
    'CM_SAF_HTOVS':{
        'TQV'   :       ['TQV'],
    },
    'ERA5':{
        'CLDF'     :    ['CLDF'],
        'U'     :       ['U'],
        'V'     :       ['V'],
        #'P'     :       ['P'],
        'QV'    :       ['QV'],
        'RH':               ['PVAP', 'PVAPSATL', 'PVAPSATS', 'T'],
        #'H'     :       ['QV', 'T', 'PS'],
        'SWUTOA':       ['SWNDTOA','SWDTOA'],
        'SWNDTOA':      ['SWNDTOA'],
        'SWNDSFC':      ['SWNDSFC'],
        'LWNDSFC':      ['LWNDSFC'],
        'PP'    :       ['PP'],
        'CLCL2':        ['TQC'], 
        'CORREFL':      ['TQC'],
        #'TQV':          ['QV', 'RHO'],
        'TQV':          ['QV', 'RHO'],
        'TQVFT':        ['QV', 'RHO', 'INVHGT'],
        'SST':          ['SST'],
        'CLCT':         ['CLCT'], 
        'CLCL':         ['CLCL'],
        'SUBSOMEGA':    ['W','P'],
    },
    'SUOMI_NPP_VIIRS':{
        'CORREFL':      ['CORREFL'],
    },
    'GPM_IMERG':{
        'PP'     :      ['PP'],
    },
    'CMORPH':{
        'PP'     :      ['PP'],
    },
    'MPI-ESM1-2-HR':{
        'CLDF'     :    ['CLDF'],
        'U'     :       ['U'],
        'V'     :       ['V'],
        'QV':           ['QV'],
        #'RH':           ['PVAP', 'PVAPSATL'],
        'RH':           ['PVAP', 'PVAPSATL', 'PVAPSATS', 'T'],
        'SWUTOA':       ['SWUTOA'],
        'CSWUTOA':      ['CSWUTOA'],
        'SWUSFC':       ['SWUSFC'],
        'SWNDTOA':      ['SWDTOA', 'SWUTOA'],
        'CSWNDTOA':     ['SWDTOA', 'CSWUTOA'],
        'SWNDSFC':      ['SWDSFC', 'SWUSFC'],
        'LWUSFC':       ['LWUSFC'],
        'LWNDSFC':      ['LWDSFC', 'LWUSFC'],
        'CLCT':         ['CLCT'], 
        'SUBSOMEGA':    ['W'],
        'PP':           ['PP'],
    },
    'cmip6':{
        'CLDF'     :    ['CLDF'],
        'U'     :       ['U'],
        'V'     :       ['V'],
        'RH'     :      ['RH'],
        'QV':           ['RH', 'T', 'P'],
        #'QV':           ['QV'],
        'SWUTOA':       ['SWUTOA'],
        'CSWUTOA':      ['CSWUTOA'],
        'SWUSFC':       ['SWUSFC'],
        'SWNDTOA':      ['SWDTOA', 'SWUTOA'],
        'CSWNDTOA':     ['SWDTOA', 'CSWUTOA'],
        'SWNDSFC':      ['SWDSFC', 'SWUSFC'],
        'LWUSFC':       ['LWUSFC'],
        'LWNDSFC':      ['LWDSFC', 'LWUSFC'],
        'CLCT':         ['CLCT'], 
        'SUBSOMEGA':    ['W'],
        'PP':           ['PP'],
    },
}
# add variables that do not need to be derived and can
# be loaded directly
for var_name in direct_vars:
    for mkey in members:
        #print(mkey)
        if mkey not in var_mapping:
            var_mapping[mkey] = {}
        var_mapping[mkey][var_name] = [var_name]
# add variables that do have to be derived but based on
# the same input variables (equally_derived_vars)
for var_name,inp_vars in equally_derived_vars.items():
    for mkey in members:
        if mkey not in var_mapping:
            var_mapping[mkey] = {}
        var_mapping[mkey][var_name] = inp_vars


# for all cmip6 simulations, take var_mapping from MPI-ESM
for mod_key in models_cmip6:
    # special treatment for Emon models
    if mod_key == 'MPI-ESM1-2-HR':
        var_mapping[mod_key] = var_mapping[mod_key]
    else:
        var_mapping[mod_key] = var_mapping['cmip6']


mean_var_mapping = {
    'COSMO':{
        'POTTHDIVMEAN':     ['POTTHDIV'],
        'POTTVDIVMEAN':     ['POTTVDIV'],
        'POTTDIVMEAN':      ['POTTDIV'],
        'QVHDIVMEAN':       ['QVHDIV'],
        'QVVDIVMEAN':       ['QVVDIV'],
        'QVDIVMEAN':        ['QVDIV'],
        'QVHDIV2MEAN':      ['QVHDIV2'],
        'QVVDIV2MEAN':      ['QVVDIV2'],
        'QVDIV2MEAN':       ['QVDIV2'],
        'QVHDIV3MEAN':      ['QVHDIV3'],
        'QVVDIV3MEAN':      ['QVVDIV3'],
        'QVDIV3MEAN':       ['QVDIV3'],
        'POTTHDIVMEANNORMI':['POTTHDIV', 'INVHGT'],
        'POTTVDIVMEANNORMI':['POTTVDIV', 'INVHGT'],
        'POTTDIVMEANNORMI': ['POTTDIV', 'INVHGT'],
        'QVHDIVMEANNORMI':  ['QVHDIV', 'INVHGT'],
        'QVVDIVMEANNORMI':  ['QVVDIV', 'INVHGT'],
        'QVDIVMEANNORMI':   ['QVDIV', 'INVHGT'],
        'QVHDIV2MEANNORMI': ['QVHDIV2', 'INVHGT'],
        'QVVDIV2MEANNORMI': ['QVVDIV2', 'INVHGT'],
        'QVDIV2MEANNORMI':  ['QVDIV2', 'INVHGT'],
        'QVHDIV3MEANNORMI': ['QVHDIV3', 'INVHGT'],
        'QVVDIV3MEANNORMI': ['QVVDIV3', 'INVHGT'],
        'QVDIV3MEANNORMI':  ['QVDIV3', 'INVHGT'],

        'POTTVDIVTURB':     ['POTTVDIV'],
        'POTTHDIVTURB':     ['POTTHDIV'],
        'POTTDIVTURB':      ['POTTDIV'],
        'QVVDIVTURB':       ['QVVDIV'],
        'QVVDIV2TURB':      ['QVVDIV2'],
        'QVVDIV3TURB':      ['QVVDIV3'],
        'QVUVDIVTURB':      ['QVVDIV','W'],
        'QVDVDIVTURB':      ['QVVDIV','W'],
        'QVHDIVTURB':       ['QVHDIV'],
        'QVDIVTURB':        ['QVDIV'],
        'QVHDIV2TURB':      ['QVHDIV2'],
        'QVDIV2TURB':       ['QVDIV2'],
        'QVHDIV3TURB':      ['QVHDIV3'],
        'QVDIV3TURB':       ['QVDIV3'],

        'TKE':              ['U', 'V', 'W'],
        'TKEV':             ['W'],
        'WTURB':            ['W'],
        'BUOYIFLX':         ['W','POTTV'],
    },

    'MPI-ESM1-2-HR':{
    },
    'ERA5':{
    },
    'CM_SAF_MSG_AQUA_TERRA':{
    },
    'CERES_EBAF':{
    },
    'GPM_IMERG':{
    },
    'CMORPH':{
    },
}

# for all cmip6 simulations, take var_mapping from MPI-ESM
for mod_key in models_cmip6:
    # special treatment for Emon models
    if mod_key != 'MPI-ESM1-2-HR':
        mean_var_mapping[mod_key] = mean_var_mapping['MPI-ESM1-2-HR']



def compute_variable(var_name, mkey, inputs, mean_inputs, domain=None):
    """
    Compute derived variable var_name based on data stored in inputs.
    ARGS:
        var_name:   name of variable (e.g. SWUTOA)
        mkey:       key of model to look up how to compute the variable.
        inputs:     dict -  contains name of input variables as keys and arrays
                            as values.
    OUT:
        out_var:    computed variable
    """
    #if var_name == 'P':
    #    out_var = compute_P(mkey, inputs) 
    if var_name in ['U','V']:
        out_var = compute_U_V(mkey, inputs, var_name) 
    elif var_name in ['UV']:
        out_var = compute_UV(mkey, inputs) 
    elif var_name in [
        'BUOYIFLXNORMI',
        'TNORMI', 'POTTNORMI','POTTVNORMI',
        'QCNORMI','CLDFNORMI',
        'PNORMI', 'WFLXNORMI',
        'AWNORMI', 'AWDNORMI', 'AWUNORMI',
        'KEWNORMI',
        'UNORMI', 'VNORMI', 'UVNORMI', 'UVFLXDIVNORMI',
        'DIABHNORMI', 'DIABMNORMI',
        'LOWCLDBASENORMI',
        'WTURBNORMI', 'LCLNORMI',
        'BVFNORMI',
        'TKENORMI',
        'QVSATDEFNORMI','CSQVSATDEFNORMI','CLDQVSATDEFNORMI',
        'QVNORMI','CLDQVNORMI','CSQVNORMI',
        'WNORMI','CLDWNORMI','CSWNORMI',
        'RHNORMI','CLDRHNORMI','CSRHNORMI',
        'TKEVNORMI','CLDTKEVNORMI','CSTKEVNORMI',
        'LCLDF1E-3NORMI', 
        'LCLDF5E-4NORMI', 
        'LCLDF2E-4NORMI', 
        'LCLDF1E-4NORMI', 
        'LCLDF5E-5NORMI', 
        'LCLDF2E-5NORMI', 
        'LCLDF1E-5NORMI', 
        'ICLDF1E-3NORMI', 
        'ICLDF5E-4NORMI', 
        'ICLDF2E-4NORMI', 
        'ICLDF1E-4NORMI', 
        'ICLDF5E-5NORMI', 
        'ICLDF2E-5NORMI', 
        'ICLDF1E-5NORMI', 
        'ICLDF1E-5NORMI', 
        'CLDMASKNORMI', 

        'POTTHDIVNORMI','POTTVDIVNORMI','POTTDIVNORMI',
        'POTTDIV3NORMI',
        'EQPOTTDIVNORMI','LATHNORMI',
        'QVHDIVNORMI','QVVDIVNORMI','QVDIVNORMI',
        'QVHDIV2NORMI','QVVDIV2NORMI','QVDIV2NORMI',
        'QVHDIV3NORMI','QVVDIV3NORMI','QVDIV3NORMI',
        'QCHDIVNORMI','QCVDIVNORMI','QCDIVNORMI',

        'CLDPOTTHDIVNORMI','CLDPOTTVDIVNORMI','CLDPOTTDIVNORMI',
        'CLDPOTTDIV3NORMI',
        'CLDEQPOTTDIVNORMI','CLDLATHNORMI',
        'CLDQVHDIVNORMI','CLDQVVDIVNORMI','CLDQVDIVNORMI',
        'CLDQVHDIV2NORMI','CLDQVVDIV2NORMI','CLDQVDIV2NORMI',
        'CLDQVHDIV3NORMI','CLDQVVDIV3NORMI','CLDQVDIV3NORMI',
        'CLDQCHDIVNORMI','CLDQCVDIVNORMI','CLDQCDIVNORMI',

        'CSPOTTHDIVNORMI','CSPOTTVDIVNORMI','CSPOTTDIVNORMI',
        'CSPOTTDIV3NORMI',
        'CSEQPOTTDIVNORMI','CSLATHNORMI',
        'CSQVHDIVNORMI','CSQVVDIVNORMI','CSQVDIVNORMI',
        'CSQVHDIV2NORMI','CSQVVDIV2NORMI','CSQVDIV2NORMI',
        'CSQVHDIV3NORMI','CSQVVDIV3NORMI','CSQVDIV3NORMI',
        'CSQCHDIVNORMI','CSQCVDIVNORMI','CSQCDIVNORMI',

        'POTTHDIVMEANNORMI','POTTVDIVMEANNORMI','POTTDIVMEANNORMI',
        'QVHDIVMEANNORMI','QVVDIVMEANNORMI','QVDIVMEANNORMI',
        'QVHDIV2MEANNORMI','QVVDIV2MEANNORMI','QVDIV2MEANNORMI',
        'QVHDIV3MEANNORMI','QVVDIV3MEANNORMI','QVDIV3MEANNORMI',
        'QCHDIVMEANNORMI','QCVDIVMEANNORMI','QCDIVMEANNORMI',

        'POTTHDIVTURBNORMI','POTTVDIVTURBNORMI','POTTDIVTURBNORMI',
        'QVHDIVTURBNORMI','QVVDIVTURBNORMI','QVUVDIVTURBNORMI','QVDVDIVTURBNORMI','QVDIVTURBNORMI',
        'QVHDIV2TURBNORMI','QVVDIV2TURBNORMI','QVDIV2TURBNORMI',
        'QVHDIV3TURBNORMI','QVVDIV3TURBNORMI','QVDIV3TURBNORMI',
        'QCHDIVTURBNORMI','QCVDIVTURBNORMI','QCDIVTURBNORMI',

        'CLDPOTTHDIVTURBNORMI','CLDPOTTVDIVTURBNORMI','CLDPOTTDIVTURBNORMI',
        'CLDQVHDIVTURBNORMI','CLDQVVDIVTURBNORMI','CLDQVUVDIVTURBNORMI','CLDQVDVDIVTURBNORMI','CLDQVDIVTURBNORMI',
        'CLDQVHDIV2TURBNORMI','CLDQVVDIV2TURBNORMI','CLDQVDIV2TURBNORMI',
        'CLDQVHDIV3TURBNORMI','CLDQVVDIV3TURBNORMI','CLDQVDIV3TURBNORMI',
        'CLDQCHDIVTURBNORMI','CLDQCVDIVTURBNORMI','CLDQCDIVTURBNORMI',

        'CSPOTTHDIVTURBNORMI','CSPOTTVDIVTURBNORMI','CSPOTTDIVTURBNORMI',
        'CSQVHDIVTURBNORMI','CSQVVDIVTURBNORMI','CSQVUVDIVTURBNORMI','CSQVDVDIVTURBNORMI','CSQVDIVTURBNORMI',
        'CSQVHDIV2TURBNORMI','CSQVVDIV2TURBNORMI','CSQVDIV2TURBNORMI',
        'CSQVHDIV3TURBNORMI','CSQVVDIV3TURBNORMI','CSQVDIV3TURBNORMI',
        'CSQCHDIVTURBNORMI','CSQCVDIVTURBNORMI','CSQCDIVTURBNORMI',
        ]:
        out_var = compute_VARNORMI(mkey, inputs, mean_inputs, var_name)
    elif var_name in ['WTURBNORMISCI']:
        out_var = compute_VARSCI(mkey, inputs, var_name)
    elif var_name == 'ALT':
        out_var = compute_ALT(mkey, inputs) 
    elif var_name in ['TV', 'POTTV']:
        out_var = compute_virtual_temperature(inputs, var_name) 
    elif var_name == 'POTT':
        out_var = compute_POTT(mkey, inputs) 
    elif var_name == 'TDEW':
        out_var = compute_TDEW(mkey, inputs) 
    elif var_name == 'EQPOTT':
        out_var = compute_EQPOTT(mkey, inputs) 
    elif var_name == 'RHO':
        out_var = compute_RHO(mkey, inputs) 
    elif var_name in ['AQV','AQI']:
        out_var = compute_absolute_from_specific(inputs, var_name) 
    elif var_name in ['TKE','TKEV']:
        out_var = compute_TKE(mkey, inputs, mean_inputs, var_name) 
    elif var_name in [
        'UVDIV', 'UVFLXDIV',
        'POTTXDIV', 'POTTYDIV',
        'POTTHDIV', 'POTTVDIV',
        'EQPOTTHDIV', 'EQPOTTVDIV',
        'QVXDIV', 'QVYDIV',
        'QVHDIV', 'QVVDIV',
        'QCHDIV', 'QCVDIV',
        'POTTVDIVWPOS', 'POTTVDIVWNEG'
    ]:
        out_var = compute_DIV(mkey, inputs, var_name) 
    elif var_name in [
        'POTTHDIV2', 'POTTVDIV2',
        'QVHDIV2','QVVDIV2',
    ]:
        out_var = compute_DIV2(mkey, inputs, var_name) 
    elif var_name in [
        'POTTHDIV3', 'POTTVDIV3',
        'EQPOTTHDIV3', 'EQPOTTVDIV3',
        'QVHDIV3','QVVDIV3','AQVHDIV3','AQIHDIV3',
        'QIHDIV3', 'QIVDIV3',
    ]:
        out_var = compute_DIV3(mkey, inputs, var_name) 
    elif var_name in [
        'POTTHDIV4', 'POTTVDIV4',
    ]:
        out_var = compute_DIV4(mkey, inputs, var_name) 
    elif var_name in [
        'WVPHCONV','IWPHCONV',
    ]:
        out_var = compute_vertical_integral(inputs, var_name) 
    elif var_name in [
        'CLDBVF',
        'CLDWFLX',
        'CLDQVSATDEF','CLDQV','CLDW','CLDRH','CLDTKEV',

        'NCOLIQV',

        'CSBVF',
        'CSWFLX',
        'CSQVSATDEF','CSQV','CSW','CSRH','CSTKEV',

        'UPDTV','UPDT','UPDTDEW',

        'UPD2TV','UPD2T','UPD2TDEW',
    ]:
        out_var = compute_categorization(mkey, inputs, var_name, np.nan) 
    elif var_name in [
        'RH0LCSPOTTDIV3','RH1LCSPOTTDIV3','RH2LCSPOTTDIV3',
    ]:
        intermediate = compute_categorization(mkey, inputs, var_name[4:], np.nan) 
        inputs[var_name[4:]] = intermediate
        out_var = compute_categorization(mkey, inputs, var_name, np.nan) 
    elif var_name in [
        'RH0GCSPOTTDIV3','RH1GCSPOTTDIV3','RH2GCSPOTTDIV3',
    ]:
        out_var = compute_categorization(mkey, inputs, var_name, 0) 
    elif var_name in [
        'CLDUVDIV', 
        'CLDPOTTHDIV','CLDPOTTVDIV','CLDPOTTDIV',
        'CLDPOTTHDIV3','CLDPOTTVDIV3','CLDPOTTDIV3',
        'CLDEQPOTTDIV','CLDLATH',
        'CLDEQPOTTDIV3',
        'CLDQVHDIV','CLDQVVDIV','CLDQVDIV',
        'CLDQVHDIV2','CLDQVVDIV2','CLDQVDIV2',
        'CLDQVHDIV3','CLDQVVDIV3','CLDQVDIV3',
        'CLDQCHDIV','CLDQCVDIV','CLDQCDIV',

        'CSUVDIV', 
        'CSPOTTHDIV','CSPOTTVDIV','CSPOTTDIV',
        'CSPOTTHDIV3','CSPOTTVDIV3','CSPOTTDIV3',
        'CSEQPOTTDIV','CSLATH',
        'CSEQPOTTDIV3',
        'CSQVHDIV','CSQVVDIV','CSQVDIV',
        'CSQVHDIV2','CSQVVDIV2','CSQVDIV2',
        'CSQVHDIV3','CSQVVDIV3','CSQVDIV3',
        'CSQCHDIV','CSQCVDIV','CSQCDIV',

        'NCOLIPOTTDIV','NCOLIPOTTDIV3',

        'CLDPOTTHDIVTURB','CLDPOTTVDIVTURB','CLDPOTTDIVTURB',
        'CLDQVHDIVTURB','CLDQVVDIVTURB','CLDQVUVDIVTURB','CLDQVDVDIVTURB','CLDQVDIVTURB',
        'CLDQVHDIV2TURB','CLDQVVDIV2TURB','CLDQVDIV2TURB',
        'CLDQVHDIV3TURB','CLDQVVDIV3TURB','CLDQVDIV3TURB',
        'CLDQCHDIVTURB','CLDQCVDIVTURB','CLDQCDIVTURB',

        'CSPOTTHDIVTURB','CSPOTTVDIVTURB','CSPOTTDIVTURB',
        'CSQVHDIVTURB','CSQVVDIVTURB','CSQVUVDIVTURB','CSQVDVDIVTURB','CSQVDIVTURB',
        'CSQVHDIV2TURB','CSQVVDIV2TURB','CSQVDIV2TURB',
        'CSQVHDIV3TURB','CSQVVDIV3TURB','CSQVDIV3TURB',
        'CSQCHDIVTURB','CSQCVDIVTURB','CSQCDIVTURB',
    ]:
        out_var = compute_categorization(mkey, inputs, var_name, 0) 
    elif var_name in [
        'DIABH', 'LATH',
        'POTTDIV','POTTDIV2','POTTDIV3','POTTDIV4','EQPOTTDIV','EQPOTTDIV3',
        'QVDIV','QVDIV2','QVDIV3','QCDIV','QIDIV3',
        'POTTHDIVMEAN', 'POTTVDIVMEAN', 'POTTDIVMEAN',
        'QVHDIVMEAN', 'QVVDIVMEAN', 'QVDIVMEAN',
        'QVHDIV2MEAN', 'QVVDIV2MEAN', 'QVDIV2MEAN',
        'QVHDIV3MEAN', 'QVVDIV3MEAN', 'QVDIV3MEAN',
        'POTTHDIVTURB', 'POTTVDIVTURB', 'POTTDIVTURB',
        'QVHDIVTURB','QVVDIVTURB','QVUVDIVTURB','QVDVDIVTURB','QVDIVTURB',
        'QVHDIV2TURB','QVVDIV2TURB','QVDIV2TURB',
        'QVHDIV3TURB','QVVDIV3TURB','QVDIV3TURB',
    ]:
        out_var = compute_scalar_flux_divergences(mkey, inputs, mean_inputs, var_name) 
    elif var_name in ['DIABM']:
        out_var = compute_DIABM(mkey, inputs, var_name) 
    elif var_name in ['BVF']:
        out_var = compute_brunt_vaisala_frequency(inputs, var_name) 
    elif var_name in ['AW', 'AWU', 'AWD']:
        out_var = compute_AUVW(mkey, inputs, var_name) 
    elif var_name in ['KEW']:
        out_var = compute_KE(mkey, inputs, var_name) 
    elif var_name in ['UFLX','VFLX','WFLX','QVVFLX','QVWFLX']:
        out_var = compute_FLX(mkey, inputs, var_name) 
    elif var_name in ['AWMBLI', 'KEWMBLI', 'WMBLI', 
                      'TKEMBLI', 'DIABHMINV', 'POTTHDIVMBLI',
                      'POTTMBLI']:
        out_var = compute_vertical_integ_or_mean(mkey, inputs, var_name) 
    elif var_name in ['SUBS', 'SUBSOMEGA']:
        out_var = compute_SUBS(mkey, inputs, var_name)
    elif var_name in [
                'SWUTOA', 'CSWUTOA', 'SWUSFC',
                'SWDSFC',
                'SWNUSFC',
                'SWNDTOA', 'CSWNDTOA', 'CRESWNDTOA', 'SWNDSFC', 'CRESWNDSFC',
                'CLWUTOA', 'CRELWUTOA', 'LWUSFC',
                'LWDTOA', 'CLWDTOA', 'CRELWDTOA', 'CLWDSFC',
                'LWNUSFC', 'LWNDSFC', 'CRELWNDSFC','LWDIVATM','CLWDIVATM','CRELWDIVATM',
                'RADNDTOA', 'CRADNDTOA', 'CRERADNDTOA']:
        out_var = compute_RAD(mkey, inputs, var_name)
    elif var_name == 'ALBEDO':
        out_var = compute_ALBEDO(mkey, inputs)
    elif var_name in ['UV10M']:
        out_var = compute_UV10M(mkey, inputs, var_name)
    elif var_name in ['U10M_W', 'U10M_E', 'V10M_S', 'V10M_N']:
        out_var = compute_UV_domain_boundaries(mkey, inputs, var_name, domain)
    elif var_name in ['ZCPTPP','PCPTPP']:
        out_var = compute_CPTPP(mkey, inputs, var_name)
    elif var_name == 'INVHGT':
        out_var = compute_INVHGT(mkey, inputs)
    elif var_name == 'LTS':
        out_var = compute_LTS(mkey, inputs)
    elif var_name == 'EIS':
        out_var = compute_EIS(mkey, inputs)
    elif var_name == 'LCL':
        out_var = compute_LCL(mkey, inputs)
    elif var_name == 'TQI':
        out_var = compute_TQI(mkey, inputs)
    elif var_name == 'DCLDBASELCL':
        out_var = compute_level_diff(mkey, inputs, 'LOWCLDBASE', 'LCL')
    elif var_name == 'DINVHGTLCL':
        out_var = compute_level_diff(mkey, inputs, 'INVHGT', 'LCL')
    elif var_name == 'DINVHGTLOWCLDBASE':
        out_var = compute_level_diff(mkey, inputs, 'INVHGT', 'LOWCLDBASE')
    elif var_name == 'PVAPSATL':
        out_var = compute_PVAPSATL(inputs)
    elif var_name == 'PVAPSATS':
        out_var = compute_PVAPSATS(inputs)
    elif var_name == 'PVAP':
        out_var = compute_PVAP(inputs)
    elif var_name == 'RH':
        out_var = compute_RH(inputs)
    elif var_name in ['dRHdt','dRHdt_MBL_FLX']:
        out_var = compute_dRHdt(inputs, var_name)
    elif var_name in ['dQVdt_MBL_LH', 'dTdt_MBL_SH']:
        out_var = compute_dQVdt_MBL(inputs, var_name)
    elif var_name == 'QV':
        out_var = compute_QV(mkey, inputs) 
    elif var_name == 'QVSAT':
        out_var = compute_QVSAT(inputs)
    elif var_name == 'QVSATDEF':
        out_var = compute_QVSATDEF(mkey, inputs)
    elif var_name == 'INVF':
        out_var = ~np.isnan(inputs['INVHGT'])
    elif var_name in ['CLDF', 'CLDQX', 'CLDMASK', 'LOWCLDF', 'LOWCLDBASE', 'LCLDDEPTH',
        'LCLDF1E-3', 'LCLDF5E-4', 'LCLDF2E-4', 'LCLDF1E-4', 'LCLDF5E-5', 'LCLDF2E-5', 'LCLDF1E-5', 
        'ICLDF1E-3', 'ICLDF5E-4', 'ICLDF2E-4', 'ICLDF1E-4', 'ICLDF5E-5', 'ICLDF2E-5', 'ICLDF1E-5']:
        out_var = compute_CLD(mkey, inputs, var_name)
    #elif var_name in ['CLDHGT', 'CLDBASE', 'CLDTOP', 'CLDBASENORMI']:
    #    out_var = compute_CLDHGT(mkey, inputs, var_name)
    elif var_name in ['INVSTR', 'INVSTRV', 'INVSTRA']:
        out_var = compute_INVSTR(mkey, inputs, var_name)
    elif var_name in ['SLHFLX', 'SSHFLX']:
        out_var = compute_SHFLX(mkey, inputs, var_name)
    elif var_name == 'SBUOYIFLX':
        out_var = compute_SBUOYIFLX(inputs)
    elif var_name in ['ENFLXNUSFC']:
        out_var = compute_ENFLX(mkey, inputs, var_name)
    elif var_name == 'PP':
        out_var = compute_PP(mkey, inputs)
    elif var_name in ['CORREFL']:
        out_var = compute_CORREFL(mkey, inputs) 
    elif var_name in ['CLCL', 'CLCL2', 'CLCM', 'CLCH', 'CLCT', 'CLCW', 'CLCI']:
        out_var = compute_CLC(mkey, inputs, var_name) 
    elif var_name in ['TQV', 'TQVFT']:
        out_var = compute_TQV(mkey, inputs, var_name) 
    elif var_name == 'DQVINV':
        out_var = compute_DQVINV(inputs) 
    elif var_name == 'ENTRDRY':
        out_var = compute_ENTRDRY(inputs) 
    elif var_name in ['WFLXI']:
        # this one is deprecated in favor of 
        raise NotImplementedError()
        out_var = compute_VARI(mkey, inputs, var_name) 
    elif var_name in [
        'CLDWFLXLCL','CLDWFLXLOWCLDBASE','CSWFLXLOWCLDBASE','QVWFLXINV',
        'UI','VI','WI','RHOI',
        ]:
        out_var = compute_var_at_level(mkey, inputs, var_name)
    elif var_name in ['ENTR','ENTRV','ENTRH','ENTRSCL','ENTRVSCL','ENTRHSCL']:
        out_var = compute_ENTR(mkey, inputs, var_name) 
    #elif var_name in ['QVWFLXCB']:
    #    out_var = compute_VARCB(mkey, inputs, var_name) 
    elif var_name == 'SST':
        out_var = compute_SST(mkey, inputs) 
    elif var_name == 'WMEAN':
        out_var = compute_WMEAN(mkey, inputs) 
    elif var_name == 'WTURB':
        out_var = compute_variance(mkey, inputs, mean_inputs, var_name) 
    elif var_name == 'BUOYIFLX':
        out_var = compute_buoyancy_flux(inputs, mean_inputs) 
    #elif ( (var_name in equally_derived_vars) or
    #       (var_name in direct_vars) ):
    elif (var_name in direct_vars):
        #print(inputs.keys())
        out_var = inputs[var_name]
    else:
        raise NotImplementedError(var_name)

    # rename variable and add attributes
    #out_var = out_var.rename(var_name)
    out_var = add_var_attributes(out_var, var_name)

    # set "var_pp done" flag 
    out_var.attrs[VAR_PP] = VAR_PP_DONE

    # make sure MODEL_PP flag is set and set in derived variable
    model_pp_done = False
    for var_name,var in inputs.items():
        if MODEL_PP in var.attrs:
            if var.attrs[MODEL_PP] == MODEL_PP_DONE:
                model_pp_done = True
    if model_pp_done:
        out_var.attrs[MODEL_PP] = MODEL_PP_DONE
    else:
        out_var.attrs[MODEL_PP] = MODEL_PP_DONE
        #raise ValueError()

    return(out_var)


#def compute_P(mkey, inputs):
#    if 'P' in inputs:
#        return(inputs['P'])
#    elif 'PPERT' in inputs:
#        if mkey == 'INT2LM':
#            pref = getpref(17827)
#            print(pref)
#            quit()


def compute_U_V(mkey, inputs, var_name):
    wind = inputs[var_name]
    # unstagger UM
    #if mkey in ['COSMO', 'UM']:
    if mkey in ['UM']:
        ref = inputs['TQC']
        out_var = wind.interp(lon=ref.lon, lat=ref.lat)
        #print(out_var.isel(lon=0).values)
        # quick fix for missing-value-at-boundary problem
        # (this probelm arised for U wind in COSMO_12)
        # simply take next staggered value
        #print(out_var.loc[{'lon':out_var.lon[0]}].values.shape)
        #print(wind.isel(lon=0).values.shape)
        #print(out_var.loc[{'lon':out_var.lon[0]}].lon.values)
        #print(wind.isel(lon=0).lon.values)
        if var_name == 'U':
            out_var.loc[{'lon':out_var.lon[0]}].values[:] = wind.isel(lon=0).values[:]
            out_var.loc[{'lon':out_var.lon[-1]}].values[:] = wind.isel(lon=-1).values[:]
        elif var_name == 'V':
            out_var.loc[{'lat':out_var.lat[0]}].values[:] = wind.isel(lat=0).values[:]
            out_var.loc[{'lat':out_var.lat[-1]}].values[:] = wind.isel(lat=-1).values[:]
    else:
        out_var = wind
    return(out_var)

def compute_UV(mkey, inputs):
    out_var = np.sqrt(inputs['U']**2 + inputs['V']**2)
    return(out_var)

#def compute_P(mkey, inputs):
#    if mkey in ['IFS', 'ARPEGE-NH']:
#        # hybrid pressure coordinates
#        # compute pressure at mid-levels based on hyam + hybm*PS
#        alt_inds = {'IFS':93, 'ARPEGE-NH':15}
#        hyam = xr.DataArray(np.loadtxt(os.path.join(model_specifics_path,
#                        '{}_hyam.txt'.format(mkey)))[alt_inds[mkey]:],
#                        dims=('alt',),
#                        coords={'alt':inputs['QV'].alt.values})
#        hybm = xr.DataArray(np.loadtxt(os.path.join(model_specifics_path,
#                        '{}_hybm.txt'.format(mkey)))[alt_inds[mkey]:],
#                        dims=('alt',),
#                        coords={'alt':inputs['QV'].alt.values})
#        P = inputs['PS'].load()
#        P = P.sel(time=inputs['QV'].time)
#        P = P.expand_dims(alt=inputs['QV'].alt, axis=1)
#        P = hyam + P*hybm
#        P = P.transpose('time', 'alt', 'lat', 'lon')
#        out_var = P
#    elif mkey == 'FV3':
#        # pressure coordinates
#        # take pressure from vertical coordinate (
#        P = inputs['T']
#        P.values[:] = 100. # hPa --> Pa
#        plev = xr.DataArray(np.loadtxt(os.path.join(model_specifics_path,
#                        'FV3_pfull.txt')),
#                        dims=('alt',),
#                        coords={'alt':inputs['T'].alt.values})
#        P = P * plev
#        P = P.transpose('time', 'alt', 'lat', 'lon')
#        out_var = P
#    elif mkey in ['COSMO', 'NICAM', 'SAM', 'ICON', 'UM', 'MPAS', 'GEOS']:
#        out_var = inputs['P']
#        #if 'fmissing_value' in out_var.attrs:
#        #    del out_var.attrs['fmissing_value']
#    else:
#        raise NotImplementedError
#    out_var.attrs[MODEL_PP] = MODEL_PP_DONE
#    return(out_var)


#def compute_ALT(mkey, inputs):
#    if mkey in ['IFS', 'ERA5']:
#        # hybrid pressure coordinates
#        # compute pressure at interfaces based on hyai + hybi*PS
#        #alt_inds = {'IFS':93}
#        hyai = xr.DataArray(np.loadtxt(os.path.join(model_specifics_path,
#                        '{}_hyai.txt'.format(mkey))),
#                        dims=('hlev',), coords={'hlev':range(138)})
#        hybi = xr.DataArray(np.loadtxt(os.path.join(model_specifics_path,
#                        '{}_hybi.txt'.format(mkey))),
#                        dims=('hlev',), coords={'hlev':range(138)})
#        PS = inputs['PS']
#        # indices to select hybi/hyai values
#        hlev_inds = np.arange(137, 137-len(inputs['QV'].lev.values)-1,-1)
#        # indices to select from model variables at full levels
#        lev_inds = np.arange(len(inputs['QV'].lev.values)-1, -1,-1)
#        # height at full levels (vertical mass points)
#        H_full = xr.full_like(inputs['QV'], fill_value=0.)
#        # height at half levels (vertical interfaces)
#        H_half = xr.full_like(inputs['PS'], fill_value=0.)
#        Rd = 287.06
#        # integrate upward
#        for k in range(len(lev_inds)):
#            # pressure at lower (altitudewise) half level
#            pbelow = hyai[hlev_inds[k  ]] + hybi[hlev_inds[k  ]] * PS
#            # pressure at upper (altitudewise) half level
#            pabove = hyai[hlev_inds[k+1]] + hybi[hlev_inds[k+1]] * PS
#            dlogp   = np.log(pbelow/pabove)
#            dp      = pbelow - pabove
#            alpha   = 1. - ( (pabove/dp) * dlogp )
#            # virtual temperature
#            Tv_lev = ( inputs['T'].isel(lev=lev_inds[k]) *
#                       (1. + 0.609133 * inputs['QV'].isel(lev=lev_inds[k])) )
#            # compute geopotential at this full level from half level below
#            H_full.loc[{'lev':H_full.lev.isel(lev=lev_inds[k]).values}] = (
#                    H_half + Tv_lev * Rd * alpha )
#            #print(H_full.isel(lev=lev_inds[k]).mean().values)
#            # compute geopotential at next half level
#            H_half = H_half + Tv_lev * Rd * dlogp
#
#        # convert geopotential to height
#        H_full /= CON_G
#        out_var = H_full
#        #print(H_full.mean(dim=['time', 'lon', 'lat']).values)
#    else:
#        raise NotImplementedError
#    return(out_var)

def compute_RHO(mkey, inputs):
    out_var = inputs['P']/(inputs['TV']*CON_RD)
    return(out_var)

def compute_absolute_from_specific(inputs, var_name):
    raw_var_name = var_name[1:]
    out_var = inputs[raw_var_name] * inputs['RHO']
    return(out_var)

def compute_TKE(mkey, inputs, mean_inputs, var_name):
    if var_name == 'TKE':
        out_var = 0.5 * (
                np.power(inputs['U'] - mean_inputs['U'].isel(time=0), 2.) +
                np.power(inputs['V'] - mean_inputs['V'].isel(time=0), 2.) +
                np.power(inputs['W'] - mean_inputs['W'].isel(time=0), 2.)
            )
    elif var_name == 'TKEV':
        out_var = (
                np.power(inputs['W'] - mean_inputs['W'].isel(time=0), 2.)
            )
    else:
        raise NotImplementedError()
    return(out_var)

def compute_DIV(mkey, inputs, var_name):
    if var_name == 'UVDIV':
        u = inputs['U']
        v = inputs['V']
        # compute divergences  [m/s / degree]
        udiv = u.differentiate(coord='lon')
        vdiv = v.differentiate(coord='lat')
        # divide by m/degree to convert to [1/s]
        udiv = udiv / (1/180*np.pi*CON_RE)
        vdiv = vdiv / (1/180*np.pi*CON_RE)
        # compute horizontal divergence in [1/s]
        out_var = udiv + vdiv

    elif var_name == 'UVFLXDIV':
        u = inputs['U']
        v = inputs['V']
        rho = inputs['RHO']
        # compute fluxes
        # FV3 needs interpolation here because of slightly different alt
        # values
        if np.any(rho.alt.values != u.alt.values):
            u = u.interp(alt=rho.alt)
        if np.any(rho.alt.values != v.alt.values):
            v = v.interp(alt=rho.alt)
        uflx = u * rho
        vflx = v * rho
        # compute divergences  [m/s / degree]
        uflxdiv = uflx.differentiate(coord='lon')
        vflxdiv = vflx.differentiate(coord='lat')
        # divide by m/degree to convert to [1/s]
        uflxdiv = uflxdiv / (1/180*np.pi*CON_RE)
        vflxdiv = vflxdiv / (1/180*np.pi*CON_RE)
        # compute horizontal divergence in [1/s]
        out_var = uflxdiv + vflxdiv

    elif var_name in [
        'QVXDIV','QVYDIV',
        'POTTXDIV','POTTYDIV',
    ]:
        if var_name in ['QVXDIV','POTTXDIV']:
            wind = inputs['U']
            diff_coord = 'lon'
        elif var_name in ['QVYDIV','POTTYDIV']:
            wind = inputs['V']
            diff_coord = 'lat'
        else:
            raise NotImplementedError()
        var = inputs[var_name[:-4]]
        # Some models need interpolation here because of different coordinates
        if np.any(var.alt.values != wind.alt.values):
            wind = wind.interp(alt=var.alt)
        if np.any(var.lon.values != wind.lon.values):
            wind = wind.interp(lon=var.lon)
        if np.any(var.lat.values != wind.lat.values):
            wind = wind.interp(lat=var.lat)

        # horizontal gradients of var [VAR/m]
        dvardcoord = var.differentiate(coord=diff_coord) / (1/180*np.pi*CON_RE)
        # horizontal divergence of var in diff_coord direction [VAR/s]
        out_var = wind * dvardcoord


    elif var_name in [
        'POTTHDIV','EQPOTTHDIV',
        'QVHDIV','QVHDIV2','QCHDIV'
    ]:
        u = inputs['U']
        v = inputs['V']
        var = inputs[var_name[:-4]]
        # Some models need interpolation here because of different coordinates
        if np.any(var.alt.values != u.alt.values):
            u = u.interp(alt=var.alt)
        if np.any(var.lon.values != u.lon.values):
            u = u.interp(lon=var.lon)
        if np.any(var.lat.values != u.lat.values):
            u = u.interp(lat=var.lat)
        if np.any(var.alt.values != v.alt.values):
            v = v.interp(alt=var.alt)
        if np.any(var.lon.values != v.lon.values):
            v = v.interp(lon=var.lon)
        if np.any(var.lat.values != v.lat.values):
            v = v.interp(lat=var.lat)

        # horizontal gradients of var [VAR/m]
        dvardx = var.differentiate(coord='lon') / (1/180*np.pi*CON_RE)
        dvardy = var.differentiate(coord='lat') / (1/180*np.pi*CON_RE)
        # horizontal divergence of var in [VAR/s]
        out_var = u * dvardx + v * dvardy

    elif var_name in ['POTTVDIV', 'EQPOTTVDIV', 'QVVDIV', 'QCVDIV']:
        var = inputs[var_name[:-4]]
        w = inputs['W']
        # if W is staggered, interpolate W onto full levels
        if np.any(var.alt.values != w.alt.values):
            w = w.interp(alt=var.alt)
        # make sure the two arrays have the same times
        w, var = select_common_timesteps(w, var)
        # compute vertical gradient of potential temperature [K/m]
        dvardz = var.differentiate(coord='alt')
        # vertical divergence of POTT in [K/s]
        out_var = w * dvardz

    #elif var_name in ['POTTVDIVWPOS', 'POTTVDIVWNEG']:
    #    var = inputs['POTT']
    #    w = inputs['W']
    #    # if W is staggered, interpolate W onto full levels
    #    if np.any(var.alt.values != w.alt.values):
    #        w = w.interp(alt=var.alt)
    #    # select only updrafts or downdrafts
    #    if var_name == 'POTTVDIVWPOS':
    #        w = w.where(w > 0, np.nan)
    #    elif var_name == 'POTTVDIVWPOS':
    #        w = w.where(w < 0, np.nan)
    #    # make sure the two arrays have the same times
    #    w, var = select_common_timesteps(w, var)
    #    # compute vertical gradient of potential temperature [K/m]
    #    dvardz = var.differentiate(coord='alt')
    #    # vertical divergence of POTT in [K/s]
    #    out_var = w * dvardz

    else: raise NotImplementedError()
    return(out_var)


def compute_DIV2(mkey, inputs, var_name):
    if var_name in ['QVHDIV2','POTTHDIV2']:
        u = inputs['U']
        v = inputs['V']
        var = inputs[var_name[:-5]]

        # Some models need interpolation here because of different coordinates
        if np.any(var.alt.values != u.alt.values):
            u = u.interp(alt=var.alt)
        if np.any(var.lon.values != u.lon.values):
            u = u.interp(lon=var.lon)
        if np.any(var.lat.values != u.lat.values):
            u = u.interp(lat=var.lat)
        if np.any(var.alt.values != v.alt.values):
            v = v.interp(alt=var.alt)
        if np.any(var.lon.values != v.lon.values):
            v = v.interp(lon=var.lon)
        if np.any(var.lat.values != v.lat.values):
            v = v.interp(lat=var.lat)

        # horizontal gradients of velocity [1/s]
        dudx = u.differentiate(coord='lon') / (1/180*np.pi*CON_RE)
        dvdy = v.differentiate(coord='lat') / (1/180*np.pi*CON_RE)
        # horizontal divergence of var in [VAR/s]
        out_var = var * dudx + var * dvdy

    elif var_name in ['QVVDIV2','POTTVDIV2']:
        var = inputs[var_name[:-5]]
        w = inputs['W']
        # if W is staggered, interpolate W onto full levels
        if np.any(var.alt.values != w.alt.values):
            w = w.interp(alt=var.alt)
        # make sure the two arrays have the same times
        w, var = select_common_timesteps(w, var)
        # compute vertical gradient of vertical wind [1/s]
        dwdz = w.differentiate(coord='alt')
        # vertical divergence of POTT in [K/s]
        out_var = var * dwdz

    else: raise NotImplementedError()
    return(out_var)


def compute_DIV3(mkey, inputs, var_name):
    if var_name in [
        'QVHDIV3','AQVHDIV3','AQIHDIV3',
        'POTTHDIV3','EQPOTTHDIV3',
        'QIHDIV3',
    ]:
        u = inputs['U']
        v = inputs['V']
        var = inputs[var_name[:-5]]

        # Some models need interpolation here because of different coordinates
        if np.any(var.alt.values != u.alt.values):
            u = u.interp(alt=var.alt)
        if np.any(var.lon.values != u.lon.values):
            u = u.interp(lon=var.lon)
        if np.any(var.lat.values != u.lat.values):
            u = u.interp(lat=var.lat)
        if np.any(var.alt.values != v.alt.values):
            v = v.interp(alt=var.alt)
        if np.any(var.lon.values != v.lon.values):
            v = v.interp(lon=var.lon)
        if np.any(var.lat.values != v.lat.values):
            v = v.interp(lat=var.lat)

        # horizontal gradients of velocity [1/s]
        duvardx = (u*var).differentiate(coord='lon') / (1/180*np.pi*CON_RE)
        dvvardy = (v*var).differentiate(coord='lat') / (1/180*np.pi*CON_RE)
        # horizontal divergence of var in [VAR/s]
        out_var = duvardx + dvvardy

    elif var_name in ['QVVDIV3','POTTVDIV3','EQPOTTVDIV3','QIVDIV3']:
        var = inputs[var_name[:-5]]
        w = inputs['W']
        # if W is staggered, interpolate W onto full levels
        if np.any(var.alt.values != w.alt.values):
            w = w.interp(alt=var.alt)
        # make sure the two arrays have the same times
        w, var = select_common_timesteps(w, var)
        # compute vertical gradient of vertical wind [K/s]
        dwvardz = (w*var).differentiate(coord='alt')
        # vertical divergence of POTT in [K/s]
        out_var = dwvardz

    else: raise NotImplementedError()
    return(out_var)


def compute_DIV4(mkey, inputs, var_name):
    if var_name in [
        'POTTHDIV4'
    ]:
        u = inputs['UFLX']
        v = inputs['VFLX']
        var = inputs[var_name[:-5]]

        # Some models need interpolation here because of different coordinates
        if np.any(var.alt.values != u.alt.values):
            u = u.interp(alt=var.alt)
        if np.any(var.lon.values != u.lon.values):
            u = u.interp(lon=var.lon)
        if np.any(var.lat.values != u.lat.values):
            u = u.interp(lat=var.lat)
        if np.any(var.alt.values != v.alt.values):
            v = v.interp(alt=var.alt)
        if np.any(var.lon.values != v.lon.values):
            v = v.interp(lon=var.lon)
        if np.any(var.lat.values != v.lat.values):
            v = v.interp(lat=var.lat)

        # horizontal gradients of velocity [1/s]
        duvardx = (u*var).differentiate(coord='lon') / (1/180*np.pi*CON_RE)
        dvvardy = (v*var).differentiate(coord='lat') / (1/180*np.pi*CON_RE)
        # horizontal divergence of var in [VAR/s]
        out_var = (duvardx + dvvardy) / inputs['RHO']

    elif var_name in ['POTTVDIV4']:
        var = inputs[var_name[:-5]]
        w = inputs['WFLX']
        # if W is staggered, interpolate W onto full levels
        if np.any(var.alt.values != w.alt.values):
            w = w.interp(alt=var.alt)
        # make sure the two arrays have the same times
        w, var = select_common_timesteps(w, var)
        # compute vertical gradient of vertical wind [K/s]
        dwvardz = (w*var).differentiate(coord='alt')
        # vertical divergence of POTT in [K/s]
        out_var = dwvardz / inputs['RHO']

    else: raise NotImplementedError()
    return(out_var)


def compute_categorization(mkey, inputs, var_name, fill_val):
    if var_name[0:2] == 'CS':
        category = 'CS'
        raw_var = inputs[var_name[2:]]
        weight_var_names = ['CLDF']
    elif var_name[0:3] == 'CLD':
        category = 'CLD'
        raw_var = inputs[var_name[3:]]
        weight_var_names = ['CLDF']
    elif var_name[0:5] == 'NCOLI':
        category = 'NCOLI'
        raw_var = inputs[var_name[5:]]
        weight_var_names = ['TQI']
    elif var_name[0:4] in ['RH0L','RH1L','RH2L','RH0G','RH1G','RH2G']:
        category = var_name[0:4]
        raw_var = inputs[var_name[4:]]
        weight_var_names = ['RH']
    elif var_name[0:3] == 'UPD':
        category = 'UPD'
        raw_var = var_name[3:]
        weight_var_names = ['CLDF','W']
    #elif var_name[0:4] == 'UPD2':
    #    category = 'UPD2'
    #    raw_var_name = var_name[4:]
    else:
        raise ValueError()

    #print(category)
    #print(weight_var_names)
    #print(raw_var)
    #print(fill_val)
    #quit()

    ## preprocess weight variables
    for weight_var_name in weight_var_names:
        ## make sure raw_var and weight_var can be combined/compared
        if np.any(raw_var.lon.values != inputs[weight_var_name].lon.values):
            inputs[weight_var_name] = inputs[weight_var_name].interp(lon=raw_var.lon)
        if np.any(raw_var.lat.values != inputs[weight_var_name].lat.values):
            inputs[weight_var_name] = inputs[weight_var_name].interp(lat=raw_var.lat)
        if 'alt' in inputs[weight_var_name].dims:
            if np.any(raw_var.alt.values != inputs[weight_var_name].alt.values):
                inputs[weight_var_name] = inputs[weight_var_name].interp(alt=raw_var.alt)
        else:
            inputs[weight_var_name] = inputs[weight_var_name].expand_dims(dict(alt=raw_var.alt.values), axis=1)

        inputs[weight_var_name],raw_var = select_common_timesteps(inputs[weight_var_name],raw_var)

        ### make sure weight has valid range
        #inputs[weight_var_name] = inputs[weight_var_name].where(inputs[weight_var_name] <= 1, 1)
        #inputs[weight_var_name] = inputs[weight_var_name].where(inputs[weight_var_name] >= 0, 0)

        #print(raw_var)
        #print(inputs[weight_var_name])
        #inputs[weight_var_name].to_netcdf('test.nc')
        #quit()

    if category in ['RH0L','RH1L','RH2L','RH0G','RH1G','RH2G']:
        if category in ['RH0L','RH0G']:
            thresh0 = 0
            thresh1 = 0.333
        elif category in ['RH1L','RH1G']:
            thresh0 = 0.333
            thresh1 = 0.666
        elif category in ['RH2L','RH2G']:
            thresh0 = 0.666
            thresh1 = 5
        else:
            raise NotImplementedError()
        out_var = raw_var.where((inputs['RH'] >= thresh0) & (inputs['RH'] < thresh1), fill_val)

    elif category == 'CS':
        out_var = raw_var.where(inputs['CLDF'] < 0.5, fill_val)

    elif category == 'CLD':
        out_var = raw_var.where(inputs['CLDF'] >= 0.5, fill_val)

    elif category == 'NCOLI':
        out_var = raw_var.where(inputs['TQI'] < 1E-5, fill_val)
        #out_var.to_netcdf('test.nc')
        #quit()

    elif category == 'UPD2':
        out_var = raw_var.where((inputs['CLDF'] >= 0.5) & (inputs['W'] >= 1), fill_val)
    else:
        raise ValueError()
        
    return(out_var)


def compute_scalar_flux_divergences(mkey, inputs, mean_inputs, var_name):
    if var_name in ['DIABH']:
        out_var = inputs['POTTHDIV'] + inputs['POTTVDIV']
    elif var_name in ['LATH']:
        out_var = inputs['POTTDIV'] - inputs['EQPOTTDIV']
    elif var_name in ['POTTDIV']:
        out_var = inputs['POTTHDIV'] + inputs['POTTVDIV']
    elif var_name in ['POTTDIV2']:
        out_var = inputs['POTTHDIV2'] + inputs['POTTVDIV2']
    elif var_name in ['POTTDIV3']:
        out_var = inputs['POTTHDIV3'] + inputs['POTTVDIV3']
    elif var_name in ['POTTDIV4']:
        out_var = inputs['POTTHDIV4'] + inputs['POTTVDIV4']
    elif var_name in ['EQPOTTDIV']:
        out_var = inputs['EQPOTTHDIV'] + inputs['EQPOTTVDIV']
    elif var_name in ['EQPOTTDIV3']:
        out_var = inputs['EQPOTTHDIV3'] + inputs['EQPOTTVDIV3']
    elif var_name in ['QVDIV']:
        out_var = inputs['QVHDIV'] + inputs['QVVDIV']
    elif var_name in ['QVDIV2']:
        out_var = inputs['QVHDIV2'] + inputs['QVVDIV2']
    elif var_name in ['QVDIV3']:
        out_var = inputs['QVHDIV3'] + inputs['QVVDIV3']
    elif var_name in ['QCDIV']:
        out_var = inputs['QCHDIV'] + inputs['QCVDIV']
    elif var_name in ['QIDIV3']:
        out_var = inputs['QIHDIV3'] + inputs['QIVDIV3']
    elif var_name == 'POTTHDIVMEAN':
        out_var = mean_inputs['POTTHDIV']
    elif var_name == 'POTTVDIVMEAN':
        out_var = mean_inputs['POTTVDIV']
    elif var_name == 'POTTDIVMEAN':
        out_var = mean_inputs['POTTDIV']
    elif var_name == 'QVHDIVMEAN':
        out_var = mean_inputs['QVHDIV']
    elif var_name == 'QVVDIVMEAN':
        out_var = mean_inputs['QVVDIV']
    elif var_name == 'QVDIVMEAN':
        out_var = mean_inputs['QVDIV']
    elif var_name == 'QVHDIV2MEAN':
        out_var = mean_inputs['QVHDIV2']
    elif var_name == 'QVVDIV2MEAN':
        out_var = mean_inputs['QVVDIV2']
    elif var_name == 'QVDIV2MEAN':
        out_var = mean_inputs['QVDIV2']
    elif var_name == 'QVHDIV3MEAN':
        out_var = mean_inputs['QVHDIV3']
    elif var_name == 'QVVDIV3MEAN':
        out_var = mean_inputs['QVVDIV3']
    elif var_name == 'QVDIV3MEAN':
        out_var = mean_inputs['QVDIV3']

    elif var_name == 'POTTHDIVTURB':
        out_var =  inputs['POTTHDIV'] - mean_inputs['POTTHDIV'].isel(time=0)
    elif var_name == 'POTTVDIVTURB':
        out_var =  inputs['POTTVDIV'] - mean_inputs['POTTVDIV'].isel(time=0)
    elif var_name == 'POTTDIVTURB':
        out_var =  inputs['POTTDIV'] - mean_inputs['POTTDIV'].isel(time=0)
    elif var_name == 'QVHDIVTURB':
        out_var =  inputs['QVHDIV'] - mean_inputs['QVHDIV'].isel(time=0)
    elif var_name == 'QVVDIVTURB':
        out_var =  inputs['QVVDIV'] - mean_inputs['QVVDIV'].isel(time=0)
    elif var_name == 'QVHDIV2TURB':
        out_var =  inputs['QVHDIV2'] - mean_inputs['QVHDIV2'].isel(time=0)
    elif var_name == 'QVVDIV2TURB':
        out_var =  inputs['QVVDIV2'] - mean_inputs['QVVDIV2'].isel(time=0)
    elif var_name == 'QVHDIV3TURB':
        out_var =  inputs['QVHDIV3'] - mean_inputs['QVHDIV3'].isel(time=0)
    elif var_name == 'QVVDIV3TURB':
        out_var =  inputs['QVVDIV3'] - mean_inputs['QVVDIV3'].isel(time=0)
    elif var_name in ['QVUVDIVTURB','QVDVDIVTURB']:
        w_pert = inputs['W'] - mean_inputs['W'].isel(time=0)
        out_var =  inputs['QVVDIV'] - mean_inputs['QVVDIV'].isel(time=0)
        if var_name == 'QVUVDIVTURB':
            out_var = out_var.where(w_pert >= 0, 0)
        elif var_name == 'QVDVDIVTURB':
            out_var = out_var.where(w_pert < 0, 0)
        else:
            raise NotImplementedError()
    elif var_name == 'QVDIVTURB':
        out_var =  inputs['QVDIV'] - mean_inputs['QVDIV'].isel(time=0)
    elif var_name == 'QVDIV2TURB':
        out_var =  inputs['QVDIV2'] - mean_inputs['QVDIV2'].isel(time=0)
    elif var_name == 'QVDIV3TURB':
        out_var =  inputs['QVDIV3'] - mean_inputs['QVDIV3'].isel(time=0)

    else: raise NotImplementedError(var_name)
    return(out_var)

def compute_DIABM(mkey, inputs, var_name):
    if var_name in ['DIABM']:
        out_var = inputs['QVHDIV'] + inputs['QVVDIV']
    else: raise NotImplementedError(var_name)
    return(out_var)


def compute_brunt_vaisala_frequency(inputs, var_name):
    out_var = (
        inputs['POTTV'].differentiate(coord='alt') /
        inputs['POTTV'] * CON_G
    )
    #out_var.to_netcdf('test.nc')
    #quit()
    return(out_var)


def compute_virtual_temperature(inputs, var_name):
    """
    Compute the virtual (potential) temperature using T and QV as input.
    """
    if var_name == 'TV': inp_var_name = 'T'
    elif var_name == 'POTTV': inp_var_name = 'POTT'
    else: raise NotImplemtedError()
    out_var = inputs[inp_var_name] * (1. + 0.609133 * inputs['QV'])
    return(out_var)

def compute_POTT(mkey, inputs):
    Rd = 287.1
    cp = 1005.
    #if 'alt' in inputs['T'].dims:

    T = inputs['T']
    p = inputs['P']
    if np.any(p.alt.values != T.alt.values):
        # if differences are only due to differences in numeric precision
        # simply replace alt values
        if np.mean(np.abs(p.alt.values - T.alt.values)) < 1E-3:
            p.alt.values = T.alt.values
        # if differences are real, run interpolation
        else:
            p = p.interp(alt=T.alt)
    # compute potential temperature
    out_var = T*(100000/p)**(Rd/cp)

    #elif 'plev' in inputs['T'].dims:
    #    out_var = inputs['T']*(100000/inputs['T'].plev)**(Rd/cp)
    return(out_var)


def compute_TDEW(mkey, inputs):
    """
    Dewpoint temperature.
    """
    RH = inputs['RH']
    # force RH to valid values for dewpoint computation
    RH = RH.where(RH <= 1.19, 1.19)
    RH = RH.where(RH >= 0.01, 0.01)
    out_var = mpcalc.dewpoint_from_relative_humidity(
        inputs['T']*units.kelvin, 
        RH
    )
    #print(out_var.mean())
    #out_var = out_var.metpy.dequantify()
    #print(out_var.mean())
    #out_var.to_netcdf('test.nc')
    #quit()
    return(out_var)

def compute_EQPOTT(mkey, inputs):
    """
    Equivalent potential temperature.
    """
    RH = inputs['RH']
    # force RH to valid values for dewpoint computation
    RH = RH.where(RH <= 1.19, 1.19)
    RH = RH.where(RH >= 0.01, 0.01)
    TDEW = mpcalc.dewpoint_from_relative_humidity(
        inputs['T']*units.kelvin, 
        RH
    )
    out_var = mpcalc.equivalent_potential_temperature(
        inputs['P']*units.pascal, 
        inputs['T']*units.kelvin, 
        TDEW
    )
    return(out_var)


def compute_AUVW(mkey, inputs, var_name):
    if var_name == 'AW':
        out_var = np.abs(inputs['W'])
    elif var_name == 'AWU':
        out_var = inputs['W'].where(inputs['W'] > 0, np.nan)
    elif var_name == 'AWD':
        out_var = inputs['W'].where(inputs['W'] < 0, np.nan)
    else:
        raise NotImplementedError()
    return(out_var)

def compute_KE(mkey, inputs, var_name):
    if var_name == 'KEW':
        out_var = inputs['W']**2
    rho = inputs['RHO']
    # if W is staggered, interpolate onto full levels
    if np.any(out_var.alt.values != rho.alt.values):
        out_var = out_var.interp(alt=rho.alt)
    # make sure the two arrays have the same times
    rho, out_var = select_common_timesteps(rho, out_var)
    # compute KE per unit volume
    out_var *= 0.5 * rho
    return(out_var)

def compute_FLX(mkey, inputs, var_name):
    if var_name in ['UFLX','QVUFLX']:
        out_var = inputs['U']
    elif var_name in ['VFLX','QVVFLX']:
        out_var = inputs['V']
    elif var_name in ['WFLX','QVWFLX']:
        out_var = inputs['W']
    else:
        raise NotImplementedError()
    rho = inputs['RHO']
    # if W is staggered, interpolate RHO onto full levels
    if np.any(out_var.alt.values != rho.alt.values):
        rho = rho.interp(alt=out_var.alt)
    # make sure the two arrays have the same times
    rho, out_var = select_common_timesteps(rho, out_var)
    # compute flux FLX in kg/m^2/s
    out_var *= rho
    if var_name in ['QVUFLX','QVVFLX','QVWFLX']:
        qv = inputs['QV']
        # if WFLX is staggered, interpolate QV onto half levels
        if np.any(out_var.alt.values != qv.alt.values):
            qv = qv.interp(alt=out_var.alt)
        # make sure the two arrays have the same times
        qv, out_var = select_common_timesteps(qv, out_var)
        # compute QVFLXZ in kg/m^2/s
        out_var *= qv
    return(out_var)


def compute_SUBS(mkey, inputs, var_name):
    targ_plev = 50000
    targ_alt = 5800
    if var_name == 'SUBS':
        if mkey == 'COSMO':
            # 1.* removes a warning of serialization issue while saving to netCDF file.
            ## this was used for DYAMOND paper
            #out_var = 1.*inputs['W'].sel(alt=3000, method='nearest')
            if targ_alt in inputs['W'].alt:
                out_var = inputs['W'].sel(alt=targ_alt)
            else:
                out_var = inputs['W'].interp(alt=targ_alt)
        else:
            raise NotImplementedError()
    elif var_name == 'SUBSOMEGA':
        if 'alt' in inputs['W'].dims:
            #print(inputs['P'].mean(dim=['lon','lat','time']))
            #print(inputs['P'].differentiate(coord='alt').mean(dim=['lon','lat','time']))
            if targ_alt in inputs['W'].alt:
                out_var = (
                    inputs['W'].sel(alt=targ_alt) *
                    inputs['P'].differentiate(coord='alt').sel(alt=targ_alt)
                    )
            else:
                out_var = inputs['W'].interp(alt=targ_alt)
                out_var = (
                    inputs['W'].interp(alt=targ_alt) *
                    inputs['P'].differentiate(coord='alt').interp(alt=targ_alt)
                    )
        elif 'plev' in inputs['W'].dims:
            if targ_plev in inputs['W'].plev:
                out_var = inputs['W'].sel(plev=targ_plev)
            else:
                out_var = inputs['W'].interp(plev=targ_plev)
    return(out_var)


@njit()
def interp_vprof_no_time(orig_array, src_vprof_vals_array,
                targ_vprof_vals, interp_array,
                nlat, nlon):
    """
    Helper function for compute_VARNORMI. Speedup of ~100 time
    compared to pure python code!
    """
    for lat_ind in range(nlat):
        for lon_ind in range(nlon):
            qv_col = orig_array[:, lat_ind, lon_ind]
            rel_alts_col = src_vprof_vals_array[:, lat_ind, lon_ind]
            interp_col = np.interp(targ_vprof_vals, rel_alts_col, qv_col)
            interp_array[:, lat_ind, lon_ind] = interp_col
    return(interp_array)

@njit()
def interp_vprof_with_time(orig_array, src_vprof_vals_array,
                targ_vprof_vals, interp_array,
                ntime, nlat, nlon):
    """
    Helper function for compute_VARNORMI. Speedup of ~100 time
    compared to pure python code!
    """
    for time_ind in range(ntime):
        for lat_ind in range(nlat):
            for lon_ind in range(nlon):
                qv_col = orig_array[time_ind, :, lat_ind, lon_ind]
                rel_alts_col = src_vprof_vals_array[time_ind, :, lat_ind, lon_ind]
                interp_col = np.interp(targ_vprof_vals, rel_alts_col, qv_col)
                interp_array[time_ind, :, lat_ind, lon_ind] = interp_col
    return(interp_array)

def compute_VARNORMI(mkey, inputs, mean_inputs, var_name):
    #interp_rel_alts = np.arange(0.1, 3.1, 0.1)
    interp_rel_alts = np.asarray( 
                      [0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95,
                       1.0, 1.05, 1.1, 1.2, 1.3, 1.4, 1.5, 1.75, 2.0, 2.5, 3.0])
    sel_alt = 6000

    # determine if MEAN variable is used or normal one
    if 'MEANNORMI' in var_name:
        raw_var_name = var_name[:-9]
        use_inputs = mean_inputs
    else:
        raw_var_name = var_name[:-5]
        use_inputs = inputs

    out_var = use_inputs[raw_var_name]

    # if alt is not in the coordinates it means that
    # the field itself is the altitude value (e.g. LOWCLDBASE)
    # simply divide by local inversion height
    if 'alt' not in use_inputs[raw_var_name].coords:
        out_var /= use_inputs['INVHGT']

    # alt is part of coordinates which means that the field is 3D (at least)
    # and its coordinate should be transformed to relative height.
    else:

        # subselect altitude
        var = subsel_alt(use_inputs[raw_var_name], mkey, slice(0,sel_alt))
        invhgt = use_inputs['INVHGT']
        var, invhgt = select_common_timesteps(var, invhgt)

        # vertical axis should be with ascending altitude. else sort
        if var.alt[-1] < var.alt[0]:
            #print('sort')
            var = var.sortby('alt', ascending=True)

        # time is part of the data set
        if 'time' in var.dims:
            if ( (list(var.dims) != ['time', 'alt', 'lat', 'lon']) or
                 (list(invhgt.dims) != ['time', 'lat', 'lon']) ):
                print(invhgt)
                quit()
                raise ValueError()
                # transpose to make sure to have same order of dimensions 
                # irrespective of model
                #var = var.transpose('time', 'alt', 'lat', 'lon')
                #invhgt = invhgt.transpose('time', 'lat', 'lon')

            # create array of altitudes (the same in every column)
            alts = var.alt
            alts = alts.expand_dims(lat=var.lat, axis=1)
            alts = alts.expand_dims(lon=var.lon, axis=2)
            alts = alts.expand_dims(time=var.time, axis=0)
            # create array for interpolated var values
            interp_var = xr.full_like(invhgt, np.nan).expand_dims(
                            rel_alt=interp_rel_alts, axis=1)
            interp_var_array = np.full((alts.shape[0], len(interp_rel_alts),
                                       alts.shape[2], alts.shape[3]),
                                      np.nan)
            # convert altitude array to relative altitude (with respect to invhgt)
            rel_alts = alts / invhgt
            # interpolate abs heights to relative heights along (time), lon and lat.
            interp_var.values = interp_vprof_with_time(var.values,
                            rel_alts.values,
                            interp_rel_alts, interp_var_array,
                            len(var.time.values), len(var.lat.values),
                            len(var.lon.values))
        # time is not part of the data set
        else:
            if ( (list(var.dims) != ['alt', 'lat', 'lon']) or
                 (list(invhgt.dims) != ['lat', 'lon']) ):
                raise ValueError()


            # create array of altitudes (the same in every column)
            alts = var.alt
            alts = alts.expand_dims(lat=var.lat, axis=1)
            alts = alts.expand_dims(lon=var.lon, axis=2)
            # create array for interpolated var values
            interp_var = xr.full_like(invhgt, np.nan).expand_dims(
                            rel_alt=interp_rel_alts, axis=0)
            interp_var_array = np.full((len(interp_rel_alts),
                                       alts.shape[1], alts.shape[2]),
                                      np.nan)

            # convert altitude array to relative altitude (with respect to invhgt)
            rel_alts = alts / invhgt
            #print(rel_alts.shape)
            #print(interp_var.shape)
            #print(interp_var_array.shape)
            #print(invhgt.shape)
            #print(var.shape)
            #quit()
            # interpolate abs heights to relative heights along (time), lon and lat.
            interp_var.values = interp_vprof_no_time(var.values,
                            rel_alts.values,
                            interp_rel_alts, interp_var_array,
                            len(var.lat.values),
                            len(var.lon.values))
        out_var = interp_var

    #out_var.to_netcdf('test.nc')
    #quit()
    return(out_var)

def compute_VARSCI(mkey, inputs, var_name):
    # scale with inversion height and convert to per hours
    if var_name == 'WTURBNORMISCI':
        out_var = inputs['WTURBNORMI'] / inputs['INVHGT']**2. * 3600**2
    return(out_var)
    

#def compute_SWUTOA(mkey, inputs):
#    # more or equally frequent than hourly output
#    if mkey in ['COSMO', 'SAM', 'ICON', 'MPAS', 'IFS',
#               'GEOS', 'ARPEGE-NH', 'ERA5']:
#        out_var = inputs['SWDTOA'] - inputs['SWNDTOA']
#        out_var = out_var.resample(time='1h').mean(
#                                        dim='time', skipna=False)
#    # more or equally frequent than hourly output
#    elif mkey in ['FV3', 'NICAM', 'UM',
#                  'CM_SAF_MSG_AQUA_TERRA', 'CM_SAF_METEOSAT']:
#        out_var = inputs['SWUTOA'].resample(time='1h').mean(
#                                        dim='time', skipna=False)
#    elif mkey in ['CERES_EBAF', 'MPI-ESM1-2-HR']:
#        out_var = inputs['SWUTOA']
#    else:
#        raise NotImplementedError()
#    ## THIS DOES NOT WORK FOR UM..
#    ## take orig time dim to retain time encoding
#    #vkey = 'SWNDTOA' if 'SWNDTOA' in inputs else 'SWUTOA'
#    #inputs[vkey], out_var = select_common_timesteps(inputs[vkey], out_var)
#    #out_var['time'] = inputs[vkey].time
#    return(out_var)

def compute_ALBEDO(mkey, inputs):
    ##if mkey not in ['ERA5', 'COSMO']:
    ##    print('implement daily mean again for DYAMOND sims.')
    ##    raise NotImplementedError()

    # aggregate to daily means because SWDTOA (which may come from COSMO)
    # and SWNDTOA do not necessarily have the same time resolution.
    date = np.datetime64(dt64_to_dt(inputs['SWUTOA'].time.isel(time=0)).date())
    inputs['SWUTOA'] = inputs['SWUTOA'].mean(dim='time')
    inputs['SWUTOA'] = inputs['SWUTOA'].expand_dims({'time':[date]})
    inputs['SWDTOA'] = inputs['SWDTOA'].mean(dim='time')
    inputs['SWDTOA'] = inputs['SWDTOA'].expand_dims({'time':[date]})

    out_var = inputs['SWUTOA'] / inputs['SWDTOA']
    return(out_var)

#def compute_LWUTOA(mkey, inputs):
#    out_var = inputs['LWUTOA']
#    if mkey in ['COSMO', 'ICON', 'ARPEGE-NH', 'ERA5']:
#        out_var *= -1
#        out_var = out_var.resample(time='1h').mean(
#                                        dim='time', skipna=False)
#    elif mkey in ['NICAM', 'SAM', 'UM', 'MPAS', 'IFS', 'FV3']:
#        out_var = out_var.resample(time='1h').mean(
#                                        dim='time', skipna=False)
#    elif mkey in ['GEOS', 'CM_SAF_MSG_AQUA_TERRA',
#                  'CERES_EBAF', 'CM_SAF_METEOSAT', 'MPI-ESM1-2-HR']:
#        pass
#    else:
#        raise ValueError()
#    # pass along attributes
#    out_var.attrs = inputs['LWUTOA'].attrs
#    ## take orig time dim to retain time encoding
#    #out_var, inputs['LWUTOA'] = select_common_timesteps(
#    #                                out_var, inputs['LWUTOA'])
#    #out_var['time'] = inputs['LWUTOA'].time
#    return(out_var)

def compute_RAD(mkey, inputs, var_name):
    #print(var_name)
    if var_name in ['SWUTOA', 'CSWUTOA', 'SWUSFC',
                    'LWUTOA', 'CLWUTOA', 'LWUSFC', 'CLWUSFC',]:
        D = var_name.split('U')[0] + 'D' + var_name.split('U')[1] 
        ND = var_name.split('U')[0] + 'ND' + var_name.split('U')[1] 
        DIFU = var_name.split('U')[0] + 'DIFU' + var_name.split('U')[1] 
        if var_name in inputs:
            out_var = inputs[var_name]
        elif DIFU in inputs:
            out_var = inputs[DIFU]
        else:
            out_var = inputs[D] - inputs[ND]
    elif var_name in ['SWDSFC']:
        U = var_name.split('D')[0] + 'U' + var_name.split('D')[1] 
        ND = var_name.split('D')[0] + 'ND' + var_name.split('D')[1] 
        DIFD = var_name.split('D')[0] + 'DIFD' + var_name.split('D')[1] 
        DIRD = var_name.split('D')[0] + 'DIRD' + var_name.split('D')[1] 
        if var_name in inputs:
            out_var = inputs[var_name]
        elif (DIFD in inputs) and (DIFD in inputs):
            out_var = inputs[DIFD] + inputs[DIRD]
        else:
            out_var = inputs[ND] + inputs[U]
    elif var_name == 'CLWDSFC':
        out_var = inputs['CLWNDSFC'] + inputs['LWUSFC']
    elif var_name == 'SWNUSFC':
        out_var = inputs['SWNDSFC'] * -1.
    elif var_name in ['SWNDTOA', 'CSWNDTOA', 'SWNDSFC', 'LWNDSFC']:
        if var_name == 'CSWNDTOA':
            down_flx_name = var_name[1:3] + var_name[4:]
            up_flx_name = var_name[0:3] + 'U' + var_name[5:]
        else:
            down_flx_name = var_name[0:2] + var_name[3:]
            up_flx_name = var_name[0:2] + 'U' + var_name[4:]
        if ( (mkey in ['CM_SAF_MSG_AQUA_TERRA', 'CERES_EBAF']) or 
             (mkey in models_cmip6) ):
            if mkey == 'CM_SAF_MSG_AQUA_TERRA':
                down_flux = inputs[down_flx_name]
                down_flux = down_flux.mean(dim='time')
            if (mkey in ['CERES_EBAF']) or (mkey in models_cmip6):
                down_flux = inputs[down_flx_name]
            out_var = down_flux - inputs[up_flx_name]
        else:
            out_var = inputs[var_name]
    elif var_name in ['CRESWNDTOA', 'CRESWNDSFC', 
                      'CRELWUTOA', 'CRELWDTOA', 'CRELWNDSFC',
                      'CRERADNDTOA']:
        flux = var_name.split('CRE')[1]
        cs_flux = 'C' + var_name.split('CRE')[1]
        out_var = inputs[flux] - inputs[cs_flux]

    elif var_name == 'RADNDTOA':
        out_var = inputs['SWNDTOA'] + inputs['LWDTOA']
    elif var_name == 'CRADNDTOA':
        out_var = inputs['CSWNDTOA'] + inputs['CLWDTOA']

    #elif var_name in ['LWUTOA', 'CLWUTOA']:
    #    out_var = inputs[var_name] * -1.
    elif var_name == 'LWDTOA':
        out_var = inputs['LWUTOA'] * -1.
    elif var_name == 'CLWDTOA':
        out_var = inputs['CLWUTOA'] * -1.
    elif var_name == 'LWNUSFC':
        out_var = inputs['LWNDSFC'] * -1.
    elif var_name == 'LWDIVATM':
        out_var = inputs['LWUTOA'] + inputs['LWNDSFC']
    elif var_name == 'CLWDIVATM':
        out_var = inputs['CLWUTOA'] + inputs['CLWNDSFC']
    elif var_name == 'CRELWDIVATM':
        out_var = (inputs['LWUTOA'] - inputs['CLWUTOA']) + (inputs['LWNDSFC'] - inputs['CLWNDSFC'])

    else:
        raise NotImplementedError()
    #print(out_var.mean().values)
    #quit()
    return(out_var)

def compute_UV10M(mkey, inputs, var_name):
    out_var = np.sqrt(inputs['U10M']**2 + inputs['V10M']**2)
    return(out_var)

def compute_UV_domain_boundaries(mkey, inputs, var_name, domain):
    if var_name == 'V10M_S':
        out_var = inputs['V10M'].sel(lat=domain['lat'].start, method='nearest')
    elif var_name == 'V10M_N':
        out_var = inputs['V10M'].sel(lat=domain['lat'].stop, method='nearest')
    elif var_name == 'U10M_W':
        out_var = inputs['U10M'].sel(lon=domain['lon'].start, method='nearest')
    elif var_name == 'U10M_E':
        out_var = inputs['U10M'].sel(lon=domain['lon'].stop, method='nearest')
        #print(out_var.shape)
    else: raise NotImplementedError
    return(out_var)


def compute_CPTPP(mkey, inputs, var_name):
    """
    compute altitude and pressure of cold-point tropopause
    """
    cold_point_ind = inputs['T'].argmin(dim='alt')
    if var_name == 'ZCPTPP':
        out_var = inputs['T'].isel(dict(alt=cold_point_ind)).alt 
    elif var_name == 'PCPTPP':
        inputs['P'], cold_point_ind = select_common_timesteps(
            inputs['P'],cold_point_ind 
        )
        out_var = inputs['P'].isel(dict(alt=cold_point_ind)) 
    else:
        raise NotImplementedError()
    return out_var

    
def compute_INVHGT(mkey, inputs):
    """
    compute inversion height
    works irrespective of the orientation of the vertical model grid.
    This function sould be made more efficient..
    """
    temp = inputs['TV']
    #print(temp.time)
    # make sure to only get inversion at the top of the marine boundary layer
    # not an inversion aloft
    temp = subsel_alt(temp, mkey, slice(0,5000))
    # results are basically identical for 5km and 3km in the regions where
    # an inversion is important
    #temp = subsel_alt(temp, mkey, slice(0,3000))
    height = temp['alt'].values

    temp = temp.differentiate(coord='alt')
    #temp = temp.transpose('time', 'alt', 'lat', 'lon')

    # set (weak or) no inversions below threshold to very negative value
    # argmax will definitely not choose it unless all are -99999.
    temp.values[temp.values < 0.000] = -99999.
    #print(nan_mask.mean(dim='alt'))
    # count number of non-inversion related nan (e.g. due to land-sea mask)
    n_nan = np.sum(np.isnan(temp).mean(dim='alt'))
    # set missing values (e.g. land-sea mask) to -99999 to run argmax
    temp.values[np.isnan(temp.values)] = -99999.
    # find location where temperature gradient is maximum
    max_ind = temp.argmax(dim='alt')
    # set those places where the inversion is at the surface
    # (and thus inexistent) to negative values such that aux_compute_heights
    # will set it to np.nan.
    #max_ind[max_ind == 0] = -1
    max_ind = max_ind.where(max_ind > 0, -1)
    if np.sum(max_ind < 0):
        ngp = 1
        for dim in np.shape(max_ind): ngp *= dim
        print('{}: found {:06.3f}% of grid points without inversion.'.format(
                        mkey, (np.sum(max_ind == -1)-n_nan).values/ngp*100))

    inv_hgt = np.zeros_like(max_ind).astype(np.float)
    #aux_compute_heights(max_ind, height, inv_hgt)
    aux_vind_to_height(max_ind.values, height, inv_hgt,
                        len(max_ind.time.values),
                        len(max_ind.lat.values),
                        len(max_ind.lon.values),
                        mode='centred')
    out_var = temp.mean(dim='alt')
    out_var.values = inv_hgt 
    return(out_var)

def compute_LTS(mkey, inputs):
    """
    compute lower-tropospheric stability index
    """
    # model with alt
    if 'alt' in inputs['POTT'].dims:

        inputs['POTT'], inputs['P'] = select_common_timesteps(
            inputs['POTT'], inputs['P']
        )

        # select lowest non-NaN POTT values
        lowest_ind = (~np.isnan(inputs['POTT'])).argmax(dim='alt')
        POTT_sfc = inputs['POTT'].isel(alt=lowest_ind)
        # set values to nan where altitude is above 700 hPa
        POTT_sfc = POTT_sfc.where(POTT_sfc.alt < 3200, np.nan)
        # compute 700hPa POTT
        targ_P = inputs['P'].isel(alt=slice(0,1)).copy()
        targ_P.values[:] = 70000
        POTT_700hPa = interp_logp_4d(
            inputs['POTT'].reindex(alt=list(reversed(inputs['POTT'].alt))), 
            inputs['P'].reindex(alt=list(reversed(inputs['P'].alt))), 
            targ_P,
            'time', 'lat', 'lon', extrapolate='off'
        )
        ## 700 hPa temperature
        #POTT_700hPa_2 = inputs['POTT'].interp(alt=3200)
        # compute lts index
        out_var = POTT_700hPa - POTT_sfc
        ## convert to lapser rate [K/100m]
        #out_var /= (pott_700hPa.alt - pott_surf.alt) / 100

    # model with plev
    elif 'plev' in inputs['POTT'].dims:
        pott_surf = inputs['POTT'].sel(plev=100000, method='nearest')
        pott_700hPa = inputs['POTT'].interp(plev=70000)
        # compute lts index
        out_var = pott_700hPa - pott_surf
    return(out_var)

def compute_EIS(mkey, inputs):
    """
    compute estimated inversion strength
    """
    # model with alt
    if 'alt' in inputs['T'].dims:
        # compute 850hPa POTT
        targ_P = inputs['P'].isel(alt=slice(0,1)).copy()
        targ_P.values[:] = 85000
        T_850hPa = interp_logp_4d(
            inputs['T'].reindex(alt=list(reversed(inputs['T'].alt))), 
            inputs['P'].reindex(alt=list(reversed(inputs['P'].alt))), 
            targ_P,
            'time', 'lat', 'lon', extrapolate='off'
        )
        QVSAT_850hPa = compute_QVSAT(dict(T=T_850hPa, P=targ_P))
        lapse_moist_850hPa = (
            CON_G / CON_CP_AIR *
            (
                (1 + CON_LH_EVAP     * QVSAT_850hPa / (CON_RD * T_850hPa)) /
                (1 + CON_LH_EVAP**2. * QVSAT_850hPa / (CON_CP_AIR * CON_RV * np.power(T_850hPa,2.)))
            )
        )
        # select lowest non-NaN T values
        lowest_ind = (~np.isnan(inputs['T'])).argmax(dim='alt')
        T_sfc = inputs['T'].isel(alt=lowest_ind)
        P_sfc = inputs['P'].isel(alt=lowest_ind)
        z_700hPa = (CON_RD * T_sfc / CON_G) * np.log(P_sfc / 70000)

        out_var = inputs['LTS'] - lapse_moist_850hPa * (z_700hPa - inputs['LCL'])

    # model with plev
    elif 'plev' in inputs['T'].dims:
        raise NotImplementedError()
    return(out_var)

def compute_LCL(mkey, inputs):
    """
    compute lifting condensation level.
    """
    # make sure vertical dimension is increasing
    if inputs['P'].alt.values[-1] < inputs['P'].alt.values[0]:
        raise ValueError('Vertical dimension is not increasing')
    # select lowest vertical level
    P = inputs['P'].isel(alt=0)
    T = inputs['T'].isel(alt=0)
    RH = inputs['RH'].isel(alt=0)
    # TODO:
    # if lowest model level is nan (e.g. in orography),
    # currently the lcl values for these grid points are set to nan
    # as a quick "fix". However it would be better to start with
    # the computation of lcl at the first model level that is not nan.
    #
    P, T = select_common_timesteps(P, T)
    P, RH = select_common_timesteps(P, RH)
    P, T = select_common_timesteps(P, T)
    # compute LCL
    out_var = xr.zeros_like(P)
    out_var_arr = lcl(P.values,
                  T.values,
                  RH.values)
    out_var.values = out_var_arr
    # add altitude of lowest model level because LCL is computed
    # relative to lowest model level
    out_var += RH.alt.values
    # set LCL values below 0 (->fog) to zero.
    out_var = out_var.where(out_var > 0, 0)
    #
    # set LCL values to nan if RH/T/P values are nan (within orography)
    # TODO: this should be done nicer. See TODO above.
    out_var = out_var.where(~np.isnan(RH), np.nan)

    # remove unused altitude coordinate
    out_var = out_var.drop_vars('alt')
    return(out_var)

def compute_TQI(mkey, inputs):
    """
    compute vertically integrated ice.
    """
    out_var = inputs['TQI']
    if mkey == 'CM_SAF_MSG':
        out_var = out_var.where(~np.isnan(out_var), 0)
    return(out_var)

def compute_var_at_alt(mkey, inputs, var_name, alt=None, plev=None):
    """
    compute variable value at specific alt.
    """
    if 'alt' in inputs[var_name].dims:
        out_var = inputs[var_name].interp(alt=alt)
    elif 'plev' in inputs[var_name].dims:
        out_var = inputs[var_name].interp(plev=plev)
    return(out_var)

def compute_level_diff(mkey, inputs, var_name_ref, var_name_sub):
    """
    compute difference between var_name_sub and var_name_ref.
    Thus var_name_ref - var_name_sub
    """
    out_var = inputs[var_name_ref] - inputs[var_name_sub]
    #out_var.to_netcdf('test.nc')
    #quit()
    return(out_var)

def compute_PVAP(inputs):
    """
    Compute vapor pressure
    https://cran.r-project.org/web/packages/humidity/vignettes/humidity-measures.html
    """
    eps = 0.622 # ratio of molecular mass between water and dry air
    out_var = inputs['QV'] * inputs['P'] / (eps + 0.378 * inputs['QV'])
    return(out_var)

def compute_PVAPSATL(inputs):
    """
    The saturation vapor pressure over liquid water (after package.external.lcl)
    """
    Ttrip = 273.16     # K
    ptrip = 611.65     # Pa
    E0v   = 2.3740e6   # J/kg
    cvv   = 1418       # J/kg/K 
    cvl   = 4119       # J/kg/K 
    rgasv = 461        # J/kg/K 
    cpv   = cvv + rgasv
    T = inputs['T']
    return ptrip * (T/Ttrip)**((cpv-cvl)/rgasv) * \
        np.exp( (E0v - (cvv-cvl)*Ttrip) / rgasv * (1/Ttrip - 1/T) )

    ## wrong
    #T_use = T.copy() - 273.15
    #return 6.112*np.exp(17.67*T/(T+243.5))

def compute_PVAPSATS(inputs):
    """
    The saturation vapor pressure over ice (after package.external.lcl)
    """
    Ttrip = 273.16     # K
    ptrip = 611.65     # Pa
    E0v   = 2.3740e6   # J/kg
    E0s   = 0.3337e6   # J/kg
    cvv   = 1418       # J/kg/K 
    cvs   = 1861       # J/kg/K 
    rgasv = 461        # J/kg/K 
    cpv   = cvv + rgasv
    T = inputs['T']
    return ptrip * (T/Ttrip)**((cpv-cvs)/rgasv) * \
        np.exp( (E0v + E0s - (cvv-cvs)*Ttrip) / rgasv * (1/Ttrip - 1/T) )


def compute_RH(inputs):
    """
    Relative humidity (0-1) with respect to liquid water if T >= 273.15 K,
    else with respect to ice.
    """
    if 'RH' in inputs:
        return(inputs['RH'])
    else:
        inputs['PVAP'],inputs['PVAPSATL'] = select_common_timesteps(
            inputs['PVAP'],inputs['PVAPSATL']
        )
        inputs['PVAP'],inputs['PVAPSATS'] = select_common_timesteps(
            inputs['PVAP'],inputs['PVAPSATS']
        )
        inputs['PVAP'],inputs['T'] = select_common_timesteps(
            inputs['PVAP'],inputs['T']
        )
        inputs['PVAP'],inputs['PVAPSATL'] = select_common_timesteps(
            inputs['PVAP'],inputs['PVAPSATL']
        )
        inputs['PVAP'],inputs['PVAPSATS'] = select_common_timesteps(
            inputs['PVAP'],inputs['PVAPSATS']
        )
        out_var = (inputs['PVAP'] / inputs['PVAPSATL']).where(
            inputs['T'] >= 273.15,
            inputs['PVAP'] / inputs['PVAPSATS']
        )
        return(out_var) 


def compute_dRHdt(inputs, var_name):
    """

    """
    if var_name == 'dRHdt':
        QV_0 = inputs['QV']
        QV_1 = QV_0 - inputs['QVDIV']
        T_0 = inputs['T']
        T_1 = T_0 - inputs['POTTDIV']
    elif var_name == 'dRHdt_MBL_FLX':
        QV_0 = inputs['QV'].sel(alt=100)
        QV_1 = QV_0 + inputs['dQVdt_MBL_LH']
        T_0 = inputs['T'].sel(alt=100)
        T_1 = T_0 + inputs['dTdt_MBL_SH']
    else:
        raise ValueError()

    PVAP_0 = compute_PVAP(dict(P=inputs['P'], QV=QV_0))
    PVAP_1 = compute_PVAP(dict(P=inputs['P'], QV=QV_1))

    PVAPSATL_0 = compute_PVAPSATL(dict(T=T_0))
    PVAPSATL_1 = compute_PVAPSATL(dict(T=T_1))

    RH_0 = (PVAP_0 / PVAPSATL_0)
    RH_1 = (PVAP_1 / PVAPSATL_1)
    
    out_var = RH_1 - RH_0

    #print(PVAP_0.mean())
    #print(PVAP_1.mean())
    #print(PVAPSATL_0.mean())
    #print(PVAPSATL_1.mean())
    #print(RH_0.mean())
    #print(RH_1.mean())
    #print(out_var.mean())
    #quit()
    return(out_var) 

def compute_dQVdt_MBL(inputs, var_name):
    if var_name == 'dQVdt_MBL_LH':
        # assume density of 1 kg/kg
        out_var = inputs['SLHFLX'] / CON_LH_EVAP / 1 / inputs['INVHGT']
    elif var_name == 'dTdt_MBL_SH':
        # assume density of 1 kg/kg
        out_var = inputs['SSHFLX'] / CON_CP_AIR / 1 / inputs['INVHGT']
    else:
        raise ValueError()
    return(out_var) 

def compute_QV(mkey, inputs):
    """
    Compute QV from RH
    """
    if 'QV' in inputs:
        out_var = inputs['QV']
    elif 'RH' in inputs:
        PVAPSATL = compute_PVAPSATL(inputs)
        PVAPSATS = compute_PVAPSATS(inputs)
        QVSATL = 0.622 * PVAPSATL / inputs['P']
        QVSATS = 0.622 * PVAPSATS / inputs['P']
        out_var = (inputs['RH'] * QVSATL).where(
            inputs['T'] >= 273.15,
            inputs['RH'] * QVSATS
        )
    return( out_var ) 

def compute_QVSAT(inputs):
    """
    Compute saturation specific humidity
    """
    PVAPSATL = compute_PVAPSATL(inputs)
    PVAPSATS = compute_PVAPSATS(inputs)
    QVSATL = 0.622 * PVAPSATL / inputs['P']
    QVSATS = 0.622 * PVAPSATS / inputs['P']

    out_var = QVSATL.where(
        inputs['T'] >= 273.15,
        QVSATS
    )
    return(out_var) 

def compute_QVSATDEF(mkey, inputs):
    """
    Compute QV saturation deficite
    """
    PVAPSATL = compute_PVAPSATL(inputs)
    PVAPSATS = compute_PVAPSATS(inputs)
    QVSATL = 0.622 * PVAPSATL / inputs['P']
    QVSATS = 0.622 * PVAPSATS / inputs['P']

    out_var = (QVSATL - inputs['QV']).where(
        inputs['T'] >= 273.15,
        QVSATS - inputs['QV']
    )
    return(out_var) 

def compute_moist_adiabatic_profile(inputs):
    """
    Compute moist adiatatic profile starting from LCL.
    """
    raise NotImplementedError()

def compute_CLD(mkey, inputs, var_name):
    """
    compute 3D cloud properties based on 3D QC field:
        - CLDMASK either 0 or 1 depending if QC > cloud_qc_thresh
        - LOWCLDF either 0 or 1 depending if QC > cloud_qc_thresh &
          cloud is rooted in MBL (below INVHGT)
        - height of low cloud base (LOWCLDBASE)
        - depth of low cloud layer (LCLDDEPTH = INVHGT - LOWCLDBASE)
    works irrespective of the orientation of the vertical model grid.
    """
    cloud_qx_thresh = 1E-5
    #cloud_qx_thresh = 2E-5
    #cloud_qx_thresh = 1E-4
    #cloud_qx_thresh = 5E-4
    if var_name in ['CLDQX']:
        out_var = inputs['QC'] + inputs['QI']
    elif var_name in ['CLDF']:
        if 'CLDF' in inputs:
            out_var = inputs['CLDF']
        elif 'CLDQX' in inputs:
            out_var = xr.where(inputs['CLDQX'] >= cloud_qx_thresh, 1, 0)
    elif var_name in ['LOWCLDF']:
        # factor of 1.2 to account for discretization inaccuracy
        inputs['CLDF'],inputs['INVHGT'] = select_common_timesteps(inputs['CLDF'],inputs['INVHGT'])
        out_var = inputs['CLDF'].where(
            inputs['CLDF'].alt <= inputs['INVHGT']*1.2, 0)
        #aux_filter_MBL_base(out_var.values, out_var.alt.values,
        #                    inputs['INVHGT'].values,
        #                    len(out_var.time.values),
        #                    len(out_var.alt.values),
        #                    len(out_var.lat.values),
        #                    len(out_var.lon.values))

    elif var_name == 'LOWCLDBASE':
        cldf = inputs['LOWCLDF']
        cldf2d = cldf.sum(dim='alt') > 0
        height = cldf['alt'].values
        # find altitude of cloud base
        vind = cldf.argmax(dim='alt')

        # mask grid points that do not have clouds
        # (mask means set to negative because function
        # aux_compute_heights will assume colums with negatives are masked)
        vind = vind.where(cldf2d > 0, -1)
        vind_height = xr.zeros_like(vind, dtype=float)
        aux_vind_to_height(vind.values, height, vind_height.values,
                            len(vind.time.values), len(vind.lat.values),
                            len(vind.lon.values),
                            mode='below')
        out_var = vind_height
        #out_var.to_netcdf('test.nc')
        #quit()


    else:
        raise NotImplementedError()

    #elif var_name in ['LCLDDEPTH']:
    #    out_var = inputs['LCLDTOP'] - inputs['LOWCLDBASE']

    #elif var_name in ['LCLDF1E-3', 'LCLDF5E-4', 'LCLDF2E-4', 'LCLDF1E-4', 
    #                    'LCLDF5E-5', 'LCLDF2E-5', 'LCLDF1E-5']:
    #    thresh = float(var_name[-4:])
    #    q = inputs['QC']
    #    #out_var = q / thresh
    #    #out_var = xr.ufuncs.minimum(out_var, 1.)
    #    out_var = xr.where(q >= thresh, 1, 0)

    #elif var_name in ['ICLDF1E-3', 'ICLDF5E-4', 'ICLDF2E-4', 'ICLDF1E-4', 
    #                    'ICLDF5E-5', 'ICLDF2E-5', 'ICLDF1E-5']:
    #    thresh = float(var_name[-4:])
    #    q = inputs['QI']
    #    #out_var = q / thresh
    #    #out_var = xr.ufuncs.minimum(out_var, 1.)
    #    out_var = xr.where(q >= thresh, 1, 0)

    #if var_name == 'CLDF':
    #    out_var.to_netcdf('test.nc')
    #    quit()
    return(out_var)

def compute_CLDHGT(mkey, inputs, var_name):
    """
    compute:
        - height of maximum cloud liquid water content (CLDHGT)
        - height of cloud base (CLDBASE)
        - height of cloud top (CLDTOP)
        - the above variables normalised by inversion height (...NORMI)
    works irrespective of the orientation of the vertical model grid.
    """
    qc = inputs['QC']
    qc = subsel_alt(qc, mkey, slice(0,4000))
    height = qc['alt'].values
    # if alt is reversed (starting from the top)
    # flip dataset. This is computing intensive
    # but the cloud base is selected according to first cloud level.
    # if dim is reversed, the cloud top is selected


    ## TODO very bad fix for COSMO_2.2 which contains missing values
    #if (mkey == 'COSMO') and (np.sum(np.isnan(qc)) > 0):
    #    qc.values[:,:,-1] = qc.values[:,:,-2]

    # generate cloud mask
    binary_cloud = xr.where(qc > 1E-5, 1, 0)
    cloud_mask = binary_cloud.sum(dim='alt') > 0
    if var_name == 'CLDHGT':
        # find altitude of max qc
        vind = qc.argmax(dim='alt')
    elif var_name in ['CLDBASE', 'CLDBASENORMI']:
        # vertical axis should be with ASCENDING altitude. else sort
        if height[-1] < height[0]:
            qc = qc.sortby('alt', ascending=True)
            height = qc['alt'].values
        # find altitude of cloud base
        qc = xr.where(qc > 1E-5, 1, 0)
        vind = qc.argmax(dim='alt')
    elif var_name in ['CLDTOP', 'CLDTOPNORMI']:
        # vertical axis should be with DESCENDING altitude. else sort
        if height[-1] > height[0]:
            qc = qc.sortby('alt', ascending=False)
            height = qc['alt'].values
        # find altitude of cloud top
        qc = xr.where(qc > 1E-5, 1, 0)
        vind = qc.argmax(dim='alt')
    else:
        raise NotImplementedError
    # mask grid points that do not have clouds
    # (mask means set to zero because function
    # aux_compute_heights will assume colums with zeroj are masked) 
    vind = vind.where(cloud_mask, 0)
    vind_height = xr.zeros_like(vind, dtype=np.float)
    aux_compute_heights(vind, height, vind_height.values)
    #plt.contourf(vind_height.isel(time=7))
    #plt.colorbar()
    #plt.show()
    #quit()
    out_var = vind_height

    # if necessary, normalise by inversion height
    if var_name == 'CLDBASENORMI':
        # make sure invhgt and out_var have same time steps
        out_var, invhgt = select_common_timesteps(out_var, inputs['INVHGT'])
        out_var /= inputs['INVHGT']
        # remove thos with rel_alt > 1.0 because
        # they are not rooted in the MBL
        out_var = out_var.where(out_var <= 1.0)
    return(out_var)

def compute_INVSTR(mkey, inputs, var_name):
    """
    compute absolute or average inversion strength
    either including (INVSTRV) or excluding (INVSTR) QV effect (virtual temperature)
    var_names to compute:
    INVSTR & INVSTRA
    """
    # select virtual temperatures or normal temperatures
    # depending on how it should be computed.
    if var_name in ['INVSTR', 'INVSTRA']:
        T = inputs['T']
        POTT = inputs['POTT']
    elif var_name in ['INVSTRV', 'INVSTRVA']:
        T = inputs['TV']
        POTT = inputs['POTTV']
    else: raise NotImplementedError()
        
    T.load()
    POTT.load()
    # vertical axis should be with ascending altitude.
    if T.alt.values[-1] < T.alt.values[0]:
        raise ValueError()
        #T = T.sortby('alt', ascending=True)
    if POTT.alt.values[-1] < POTT.alt.values[0]:
        raise ValueError()
        #POTT = POTT.sortby('alt', ascending=True)
    T_BL = T.where(T.alt <= inputs['INVHGT'], 1000)
    T_BL = T_BL.where(~np.isnan(inputs['INVHGT']), 1000)
    T_FT = T.where(T.alt >  inputs['INVHGT'], 0)

    ind_T_max_FT = T_FT.argmax(dim='alt')
    ind_T_min_BL = T_BL.argmin(dim='alt')
    alt_T_min_BL = T_BL.alt.isel(alt=ind_T_min_BL)
    alt_T_max_FT = T_FT.alt.isel(alt=ind_T_max_FT)

    #T_min_BL = T_BL.isel(alt=ind_T_min_BL)
    #T_max_FT = T_FT.isel(alt=ind_T_max_FT)
    #dT = T_max_FT - T_min_BL
    #dT = dT.where(~np.isnan(inputs['INVHGT']), np.nan)
    POTT_min_BL = POTT.isel(alt=ind_T_min_BL)
    POTT_max_FT = POTT.isel(alt=ind_T_max_FT)
    dPOTT = POTT_max_FT - POTT_min_BL
    dPOTT = dPOTT.where(~np.isnan(inputs['INVHGT']), np.nan)
    if var_name in ['INVSTRA', 'INVSTRVA']:
        dalt = alt_T_max_FT - alt_T_min_BL
        dalt = dalt.where(~np.isnan(inputs['INVHGT']), np.nan)
        if np.sum(dalt <= 0):
            print('INVSTRA: {}: {} negative dalt values!'.format(mkey,
                    np.sum(dalt <= 0).values))
            dalt = dalt.where(dalt > 0, np.nan)
        #dT = dT.where(dalt > 0, np.nan)
        dPOTT_dalt = dPOTT/dalt
        if np.sum(dPOTT_dalt <= 0):
            print('INVSTRA: {}: {} negative dPOTT_dalt values!'.format(mkey,
                    np.sum(dT_dalt <= 0).values))
            dPOTT_dalt = dPOTT_dalt.where(dPOTT_dalt > 0, np.nan)
        #plt.contourf(dT_dalt.mean(dim='time').squeeze())
        #plt.colorbar()
        #plt.show()
        #quit()
        out_var = dPOTT_dalt
    elif var_name in ['INVSTR', 'INVSTRV']:
        out_var = dPOTT
    else: raise ValueError()
    return(out_var)


def compute_SHFLX(mkey, inputs, var_name):
    if mkey in ['COSMO', 'ICON', 'ARPEGE-NH', 'IFS', 'ERA5']:
        out_var = inputs[var_name] * -1
    elif mkey in ['NICAM', 'SAM', 'UM', 'MPAS', 'GEOS', 'FV3']:
        out_var = inputs[var_name]
    elif mkey in models_cmip6:
        out_var = inputs[var_name]
    else: raise ValueError()
    return(out_var)

def compute_SBUOYIFLX(inputs):
    out_var = inputs['SSHFLX'] + 0.07*inputs['SLHFLX']
    return(out_var)

def compute_ENFLX(mkey, inputs, var_name):
    if var_name == 'ENFLXNUSFC':
        out_var = (
                inputs['SSHFLX'] +
                inputs['SLHFLX'] +
                inputs['SWNUSFC'] +
                inputs['LWNUSFC'])
    else: raise ValueError()
    return(out_var)


def compute_PP(mkey, inputs):
    if mkey in ['COSMO', 'NICAM', 'SAM', 'ICON', 'UM',
                'GEOS', 'ARPEGE-NH', 'GPM_IMERG', 'CMORPH']:
        out_var = inputs['PP']
    elif mkey in ['ERA5']:
        out_var = inputs['PP']*1000
    elif mkey in ['MPAS', 'IFS']:
        out_var = inputs['PPCONV'] + inputs['PPGRID']
    elif mkey == 'FV3':
        # convert kg/m2/s precip to mm/h
        out_var = inputs['PP'] * 3600
    elif mkey in models_cmip6:
        # convert kg/m2/s precip to mm/h
        out_var = inputs['PP'] * 3600
    else:
        raise ValueError
    return(out_var)

def compute_CORREFL(mkey, inputs):
    if mkey == 'SUOMI_NPP_VIIRS':
        out_var = inputs['CORREFL'] * 0.10
    else:
        out_var = inputs['TQC']
        #out_var.values[out_var.values < 0.0001] = 0.
        #out_var.values = out_var.values**(1/2)
    return(out_var)

def compute_CLC(mkey, inputs, var_name):
    if var_name == 'CLCL':
        if mkey == 'ARPEGE-NH':
            # TEST: CLCL
            out_var = inputs['CLCL'] / 100
            # TEST: CLCT
            #out_var = inputs['CLCT'] / 100
            # TEST: CLCT but mask with TQI
            #out_var = inputs['CLCT'] / 100
            #out_var = out_var.where(inputs['TQI'] < 1E-5, np.nan)
        elif mkey in ['COSMO','ERA5']:
            # TEST: CLCL
            out_var = inputs['CLCL']
            # TEST: CLCT
            #out_var = np.minimum(inputs['CLCL'] + 
            #                     inputs['CLCM'] + 
            #                     inputs['CLCH'], 1)
            # TEST: CLCT but mask with TQI
            #out_var = np.minimum(inputs['CLCL'] + 
            #                     inputs['CLCM'] + 
            #                     inputs['CLCH'], 1)
            #out_var = out_var.where(inputs['TQI'] < 1E-5, np.nan)
        elif mkey in ['IFS']:
            out_var = inputs['CLCL']
        elif mkey in ['UM', 'MPAS']:
            out_var = inputs['CLCT']
            tqi, out_var = select_common_timesteps(inputs['TQI'], out_var)
            out_var = out_var.where(tqi < 1E-5, np.nan)
        elif mkey in ['ICON']:
            out_var = inputs['CLCT'] / 100
            tqi, out_var = select_common_timesteps(inputs['TQI'], out_var)
            out_var = out_var.where(tqi < 1E-5, np.nan)
        elif mkey in ['FV3']:
            out_var = inputs['CLCT'] / 100
            # this takes very long but is necessary....
            tqi = inputs['TQI'].interp_like(out_var)
            out_var = out_var.where(tqi < 1E-5, np.nan)
        elif mkey in ['NICAM', 'SAM', 'GEOS']:
            pass
            # not CLCL data
        elif mkey in ['CM_SAF']:
            out_var = inputs['CLCL'] / 100
        else:
            raise ValueError()
    elif var_name == 'CLCL2':
        if mkey in ['CM_SAF_MSG']:
            out_var = inputs['CLCL2'] / 100
        else:
            tqc = inputs['TQC']
            out_var = xr.where(tqc > 0.001, 1., 0.)
    elif var_name == 'CLCT':
        if 'CLCT' not in inputs:
            # take maximum of low, mid, and high cloud fraction.
            #out_var = xr.ufuncs.maximum(inputs['CLCL'], inputs['CLCM'])
            #out_var = xr.ufuncs.maximum(inputs['CLCH'], out_var)

            # take sum of low, mid, and high cloud fraction.
            out_var = inputs['CLCL'] + inputs['CLCM'] + inputs['CLCH']
            out_var = out_var.where(out_var <= 1., 1.)
        else:
            out_var = inputs['CLCT'] / 100
    elif var_name == 'CLCW':
        ## Wood 2012 Sc climatological LWP: 40-150 g m-2.
        ## Actual water water path should be somewhat higher
        thresh = 5E-3
        #thresh = 1E-1
        out_var = inputs['TQC'] / thresh
        out_var = xr.ufuncs.minimum(out_var, 1.)
        #out_var.to_netcdf('test.nc')
        #quit()
    elif var_name == 'CLCI':
        thresh = 5E-3
        out_var = inputs['TQI'] / thresh
        out_var = xr.ufuncs.minimum(out_var, 1.)
    else:
        raise NotImplementedError()
    return(out_var)

def compute_TQV(mkey, inputs, var_name):
    """
    Compute vertical integral of QV*RHO between specific heights.
    """
    if mkey == 'CM_SAF_HTOVS':
        return(inputs['TQV'])

    qv = inputs['QV']
    rho = inputs['RHO']
    qv, rho = select_common_timesteps(qv, rho)

    # set missing values to zero (for integration)
    qv = qv.where(~np.isnan(qv), 0)
    rho = rho.where(~np.isnan(rho), 0)

    # select specific altitude slice
    if var_name == 'TQV':
        alt_slice = slice(0,6000)
    elif var_name == 'TQVFT':
        alt_slice = slice(3000,6000)
    else: raise NotImplementedError()
    qv = subsel_alt(qv, mkey, alt_slice)
    rho = subsel_alt(rho, mkey, alt_slice)

    if var_name == 'TQVFT':
        # select above inversion
        qv = qv.where(qv.alt > inputs['INVHGT'], 0)
        rho = rho.where(rho.alt > inputs['INVHGT'], 0)

    # convert to kg_water / m^3 air
    #print(qv.alt)
    #print(rho.alt)
    #quit()
    qv *= rho

    # take into account possible wrong orientations of coordinates
    factor = 1
    if qv.alt.values[-1] < qv.alt.values[0]:
        factor *= -1
    qv *= factor

    # integrate over vertical extent
    out_var = qv.integrate(dim=['alt'])

    if var_name == 'TQVFT':
        # set locations without inversion to missing
        out_var = out_var.where(~np.isnan(inputs['INVHGT']), np.nan)
    return(out_var)


def compute_DQVINV(inputs):
    out_var = inputs['QVNORMI'].sel(rel_alt=0.5) - inputs['QVNORMI'].sel(rel_alt=1.5)
    return(out_var)

def compute_ENTRDRY(inputs):
    #out_var = inputs['DQVINV'] * inputs['ENTR'] / inputs['INVHGT']
    out_var = - inputs['DQVINV'] * inputs['ENTR'] * inputs['RHOI'] / 1000
    #out_var.to_netcdf('test.nc')
    #quit()
    return(out_var)

def compute_vertical_integral(inputs, var_name):
    """
    Compute vertical integral of quantity.
    """
    if var_name == 'WVPHCONV':
        raw_var = -inputs['AQVHDIV3']
    elif var_name == 'IWPHCONV':
        raw_var = -inputs['AQIHDIV3']
    else:
        raise NotImplementedError()

    # set missing values to zero before vertical integral
    raw_var = raw_var.where(~np.isnan(raw_var), 0)

    out_var = raw_var.integrate(coord='alt')
    #out_var.to_netcdf('test.nc')
    #quit()

    return(out_var)

def compute_vertical_integ_or_mean(mkey, inputs, var_name):
    """
    """
    if var_name == 'KEWMBLI':
        raise NotImplementedError()
        out_var = inputs['KEW']
        rel_alt = (0, 1)
        abs_alt = None
        compute_mean = 1
        density_weight = 0
    elif var_name == 'AWMBLI':
        raise NotImplementedError()
        out_var = inputs['AW']
        rel_alt = (0, 1)
        abs_alt = None
        compute_mean = 1
        density_weight = 0
    elif var_name == 'TKEMBLI':
        out_var = inputs['TKE']
        rel_alt = (0, 1)
        abs_alt = None
        density_weight = 0
    elif var_name == 'DIABHMINV':
        raise NotImplementedError()
        out_var = inputs['DIABH']
        rel_alt = (0.75, 1.25)
        abs_alt = None
        compute_mean = 1
        density_weight = 0
    elif var_name == 'POTTHDIVMBLI':
        out_var = inputs['POTTHDIV']
        rel_alt = None
        #rel_alt = (0.00, 1.00)
        #abs_alt = None
        abs_alt = (0, 500)
        weight = 'density'
        weight = 'volume'
    elif var_name == 'POTTMBLI':
        out_var = inputs['POTT']
        rel_alt = None
        #rel_alt = (0.00, 1.00)
        #abs_alt = None
        abs_alt = (0, 500)
        weight = 'density'
        weight = 'volume'
    else:
        raise NotImplementedError()
    if weight == 'volume':
        weight = xr.ones_like(out_var)
    elif weight == 'density':
        weight = inputs['RHO']
    else: raise ValueError('no weight given')
    if not np.array_equal(weight.alt.values, out_var.alt.values):
        weight = weight.interp(alt=out_var.alt)
    # set missing values to zero for integration
    # (e.g. nicam has nan for topography points)
    out_var.values[np.isnan(out_var.values)] = 0.
    weight.values[np.isnan(out_var.values)] = 0.
    # get altitude values that limit vertical integration domain
    invhgt = inputs['INVHGT']
    # make sure the two arrays have the same times
    invhgt, out_var = select_common_timesteps(invhgt, out_var)
    weight, out_var = select_common_timesteps(weight, out_var)
    if rel_alt is not None and abs_alt is not None:
        raise ValueError('both rel_alt and abs_alt given')
    if rel_alt is not None:
        lower_limit = copy.deepcopy(invhgt) * rel_alt[0]
        upper_limit = copy.deepcopy(invhgt) * rel_alt[1]
    elif abs_alt is not None:
        lower_limit = xr.full_like(invhgt, abs_alt[0])
        upper_limit = xr.full_like(invhgt, abs_alt[1])
    # weight variable
    out_var *= weight
    # set values above inversion to 0 (again not to nan becuase of integration)
    out_var = out_var.where(((out_var.alt >= lower_limit) &
                             (out_var.alt <= upper_limit)), 0.)
    weight = weight.where(((weight.alt >= lower_limit) &
                           (weight.alt <= upper_limit)), 0.)
    # check if vertical dimension needs to be flipped
    # this is necessary for integration
    if np.diff(out_var.isel(alt=[0,-1]).alt.values) < 0:
        raise ValueError()
        #out_var = out_var.sel(alt=slice(None, None, -1))
    # vertically integrate variable
    out_var = out_var.integrate(dim='alt')
    weight = weight.integrate(dim='alt')
    out_var /= weight

    # in case of relative height selection,
    # set grid points with no inversion to nan
    if rel_alt is not None:
        out_var = out_var.where(invhgt != np.nan, np.nan)
    return(out_var)



def compute_VARI(mkey, inputs, var_name):
    var = inputs[var_name[:-1]]
    # reverse altitude if necessary
    if var.alt[-1] < var.alt[0]:
        raise ValueError()
        var = var.sortby('alt', ascending=True)
    invhgt = inputs['INVHGT']
    var, invhgt = select_common_timesteps(var, invhgt)
    # in case the lowest invhgt is below the lowest level of var (IFS_4)
    invhgt_tmp = invhgt.where(invhgt >= np.min(var.alt.values), np.min(var.alt.values))

    if invhgt_tmp.shape[1:3] != var.shape[2:4]:
        print('ERROR: INVHGT is not on same grid as VAR')
        quit()
    var.load()
    invhgt_tmp.load()
    invhgt.load()
    if var_name in ['WI']:
        # does not work for some models because of inaccurate vertical coord.
        # (TODO: why exactly?)
        try:
            out_var = var.sel(alt=invhgt_tmp, method='pad')
        except KeyError:
            print('take method nearest for {}'.format(mkey))
            out_var = var.sel(alt=invhgt_tmp, method='nearest')
    elif var_name in ['UI', 'VI']:
        try:
            out_var = var.sel(alt=invhgt_tmp, method='backfill')
        except KeyError:
            print('take method nearest for {}'.format(mkey))
            out_var = var.sel(alt=invhgt_tmp, method='nearest')
    else:
        raise ValueError()
    out_var.load()
    ## set to negative because flux should point into MBL
    #out_var = - out_var
    # if no inversion, set var to np.nan
    out_var = out_var.where(~np.isnan(invhgt), np.nan)
    #out_var.to_netcdf('test.nc')
    #quit()
    #quit()
    return(out_var)


def compute_var_at_level(mkey, inputs, var_name, method='pad'):
    if var_name in ['CLDWFLXLCL']:
        level_var_name = 'LCL'
        var_name_3d = 'CLDWFLX'
        fill_value = 0
    elif var_name in ['CLDWFLXLOWCLDBASE']:
        level_var_name = 'LOWCLDBASE'
        var_name_3d = 'CLDWFLX'
        fill_value = 0
    elif var_name in ['CSWFLXLOWCLDBASE']:
        level_var_name = 'LOWCLDBASE'
        var_name_3d = 'CSWFLX'
        fill_value = 0
    elif var_name in ['QVWFLXINV']:
        level_var_name = 'INVHGT'
        var_name_3d = 'QVWFLX'
        fill_value = np.nan
    elif var_name in ['UI','VI','WI','RHOI']:
        level_var_name = 'INVHGT'
        var_name_3d = var_name[:-1]
        fill_value = np.nan
    elif var_name in ['ULCL','VLCL','WLCL']:
        level_var_name = 'LCL'
        var_name_3d = var_name[0]
        fill_value = np.nan
    else:
        raise NotImplementedError()
    level_var = inputs[level_var_name]
    # take this to select lowest index for regions where level_var is np.nan
    nonan_level_var = level_var.where(~np.isnan(level_var), 10000)

    # find closest value below or equal to level
    if method == 'pad':
        out_var = inputs[var_name_3d].sel(
            alt=nonan_level_var*1.1,
            method='pad'
        )
    elif method == 'nearest':
        out_var = inputs[var_name_3d].sel(
            alt=nonan_level_var,
            method='nearest'
        )

    #out_var = inputs[var_name_3d].interp(
    #    alt=inputs[level_var_name],
    #    method='linear'
    #)

    # put regions where level_var is np.nan back to np.nan
    out_var = out_var.where(~np.isnan(level_var), fill_value)
    #out_var.to_netcdf('test.nc')
    #quit()
    return(out_var)

def compute_ENTR(mkey, inputs, var_name):
    """
    Entrainment velocity is compute according to Stevens TCFD 2006 Eq. 18
    """
    if var_name == 'ENTRHSCL':
        ulev = compute_var_at_level(mkey, inputs, 'ULCL', method='nearest')
        vlev = compute_var_at_level(mkey, inputs, 'VLCL', method='nearest')
        level_var_name = 'LCL'
        entr_var_name = 'ENTRH'
    elif var_name == 'ENTRVSCL':
        wlev = compute_var_at_level(mkey, inputs, 'WLCL', method='nearest')
        level_var_name = 'LCL'
        entr_var_name = 'ENTRV'
    elif var_name == 'ENTRSCL':
        hori_var_name = 'ENTRHSCL'
        vert_var_name = 'ENTRVSCL'
        entr_var_name = 'ENTR'
    elif var_name == 'ENTRH':
        ulev = compute_var_at_level(mkey, inputs, 'UI', method='pad')
        vlev = compute_var_at_level(mkey, inputs, 'VI', method='pad')
        level_var_name = 'INVHGT'
        entr_var_name = 'ENTRH'
    elif var_name == 'ENTRV':
        wlev = compute_var_at_level(mkey, inputs, 'WI', method='pad')
        level_var_name = 'INVHGT'
        entr_var_name = 'ENTRV'
    elif var_name == 'ENTR':
        hori_var_name = 'ENTRH'
        vert_var_name = 'ENTRV'
        entr_var_name = 'ENTR'
    else:
        raise NotImplementedError()
        ui = inputs['UI']
        vi = inputs['VI']
        wi = inputs['WI']
        level_var_name = 'INVHGT'


    if entr_var_name  == 'ENTRH':
        ulev, vlev = select_common_timesteps(ulev, vlev)
        dlevdx = inputs[level_var_name].differentiate(coord='lon') / CON_M_PER_DEG
        dlevdy = inputs[level_var_name].differentiate(coord='lat') / CON_M_PER_DEG
        out_var = ulev * dlevdx + vlev * dlevdy

    elif entr_var_name == 'ENTRV':
        out_var = - wlev

    elif entr_var_name == 'ENTR':
        entrh, entrv = select_common_timesteps(inputs[hori_var_name], inputs[vert_var_name])
        out_var = entrh + entrv
        #out_var.to_netcdf('test.nc')
        #quit()
    else:
        raise NotImplementedError()


    return(out_var)

def compute_VARCB(mkey, inputs, var_name):
    out_var = inputs[var_name[:-2]]
    # vertical axis should be with ascending altitude. else sort
    if out_var.alt.values[-1] < out_var.alt.values[0]:
        out_var = out_var.sortby('alt', ascending=True)
    cldbase = inputs['CLDBASE']
    out_var, cldbase = select_common_timesteps(out_var, cldbase)
    # make temporary cldbase field with missing values
    # artificially set to 1000 m. These locations will be
    # overwritten afterwards.
    cldbase_tmp = cldbase.where(~np.isnan(cldbase), 1000)
    out_var = out_var.sel(alt=cldbase_tmp, method='pad')
    # if no cloudbase, set out_var to np.nan
    out_var = out_var.where(~np.isnan(cldbase), np.nan)
    out_var['alt'] = out_var.alt.where(~np.isnan(cldbase), np.nan)
    ## if no cloudbase, set var to np.nan
    #out_var = out_var.where(~np.isnan(cldbase), np.nan)
    #out_var = out_var.sel(alt=cldbase, method='pad')
    return(out_var)


def compute_SST(mkey, inputs):
    if mkey == 'COSMO':
        # TODO! Attention! Currently no land-sea mask is used to differentiate
        # between land and sea.
        out_var = inputs['TSURF']
    elif mkey == 'ERA5':
        out_var = inputs['SST']
    return(out_var)

def compute_WMEAN(mkey, inputs):
    out_var = inputs['W'] # assumes W is tmean
    return(out_var)

def compute_variance(mkey, inputs, mean_inputs, var_name):
    if var_name in 'WTURB':
        out_var = inputs['W']
        out_var.values = (out_var.values - mean_inputs['W'].values)**2
        #out_var = ( inputs['W'] - mean_inputs['W'] )**2
    return(out_var)


def compute_buoyancy_flux(inputs, mean_inputs):
    out_var = inputs['W'].copy()
    out_var.values = (
        (inputs['W'].values - mean_inputs['W'].values) *
        (inputs['POTTV'].values - mean_inputs['POTTV'].values)
    ) * CON_G / inputs['TV']
    #out_var.to_netcdf('test.nc')
    #quit()
    return(out_var)




@njit()
def aux_filter_MBL_base(cldmask, alts, invhgt,
                        ntime, nalt, nlat, nlon):
    """
    set in cldmask(time,alt,lat,lon) all grid boxes to zero (= no cloud)
    which demark a cloud base that is above the inversion height.
    This is to select only low clouds that are rooted in the MBL.
    """
    for time_ind in range(ntime):
        for lat_ind in range(nlat):
            for lon_ind in range(nlon):
                mask_below = 1
                for alt_ind in range(nalt):
                    # remove clouds that are above the inversion and
                    # do not have a cloud in the cell below.
                    if (
                        (mask_below == 0) &
                        (cldmask[time_ind, alt_ind, lat_ind, lon_ind] == 1) &
                        (invhgt[time_ind, lat_ind, lon_ind] < alts[alt_ind])
                       ):
                        cldmask[time_ind, alt_ind, lat_ind, lon_ind] = 0
                    mask_below = cldmask[time_ind, alt_ind, lat_ind, lon_ind]



@njit()
def aux_vind_to_height(vinds, heights,
            out_height, ntime, nlat, nlon, mode='centred'):
    """
    Select from heights(alt) the index vinds(time,lat,lon)
    and insert it in out_height(time,lat,lon).
    mode:
        'centred':
            assume that the height index should be taken at vind
        'below':
            assume that the height index should be taken between
            vind and vind-1 (staggered)
        'above':
            assume that the height index should be taken between
            vind and vind+1 (staggered)
    """
    for time_ind in range(ntime):
        for lat_ind in range(nlat):
            for lon_ind in range(nlon):
                vind = vinds[time_ind,lat_ind,lon_ind]
                if vind > 0:
                    if mode == 'centred':
                        out_height[time_ind,lat_ind,lon_ind
                                    ] = heights[vind]
                    elif mode == 'below':
                        out_height[time_ind,lat_ind,lon_ind
                                    ] = 0.5*(heights[vind] + heights[vind-1])
                    elif mode == 'above':
                        out_height[time_ind,lat_ind,lon_ind
                                    ] = 0.5*(heights[vind] + heights[vind+1])
                    else:
                        raise NotImplementedError()
                else:
                    out_height[time_ind,lat_ind,lon_ind] = np.nan



def subsel_alt(ds, mkey, alt):
    """
    Subselect in xarray Dataset (or DataArray) ds, the altitude alt
    (if alt is slice, it is assumed to increase from start to stop!!)
    """
    if isinstance(alt, slice):
        ds = ds.sel(alt=alt)
    else:
        raise NotImplementedError()
    return(ds)



