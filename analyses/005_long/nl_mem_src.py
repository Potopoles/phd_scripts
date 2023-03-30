#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     collection of model dictionaries (mdicts) that describe
                what members should be used in the analysis. Can be used
                by various analysis namelists.
author			Christoph Heim
date created    07.09.2020
date changed    29.11.2021
usage           use in another script
"""
###############################################################################
import copy
from package.nl_models import models_cmip6
###############################################################################

mem_src = {

###############################################################################
## OBSERVATIONAL DATA SETS
###############################################################################
'obs': {
    'DARDAR_CLOUD':{
        'mod':'DARDAR_CLOUD',
        'sim':'DARDAR_CLOUD',
        'case': 'DARDAR_CLOUD',
        'dom_key':'dom_trades',
        'label':'DARDAR',
    },
    'CM_SAF_HTOVS':{
        'mod':'CM_SAF_HTOVS',
        'sim':'CM_SAF_HTOVS',
        'case': 'GLOBAL',
        'dom_key': 'dom_global',
        'label':'CM SAF',
    },

    #'SUOMI_NPP_VIIRS':{
    #    'mod':'SUOMI_NPP_VIIRS', 'case': 'SA',
    #    'label':'VIIRS',
    #},
    #'CM_SAF_MSG':{
    #    'mod':'CM_SAF_MSG',          'case': 'MSG',
    #    #'label':'CM SAF: MSG',
    #    'label':'CM SAF',
    #},
    #'RADIO_SOUNDING':{
    #    'mod':'RADIO_SOUNDING',  'case': 'ST_HELENA',
    #    'label':'Sounding',
    #},
},




'CM_SAF_METEOSAT':{
    'mod':'CM_SAF_METEOSAT',
    'sim':'CM_SAF_METEOSAT',
    'case': 'METEOSAT',
    'dom_key': 'METEOSAT',
    'label':'CM SAF',
    'freq':'daily',
},


'CM_SAF_MSG_AQUA_TERRA':{
    'mod':'CM_SAF_MSG_AQUA_TERRA',
    'sim':'CM_SAF_MSG_AQUA_TERRA',
    'case': 'MSG',
    'dom_key':'dom_meteosat_disk',
    'label':'CM SAF',
    #'freq':'daily',
    'freq':'monthly',
},

'CM_SAF_MSG_AQUA_TERRA_DAILY':{
    'mod':'CM_SAF_MSG_AQUA_TERRA',
    'sim':'CM_SAF_MSG_AQUA_TERRA',
    'case': 'MSG',
    'dom_key':'dom_meteosat_disk',
    'label':'CM SAF',
    'freq':'daily',
},

'CERES_EBAF':{
    'mod':'CERES_EBAF',
    'sim':'CERES_EBAF',
    'case': 'ed4_1',
    'dom_key':'SA',
    'label':'CERES',
    'freq':'monthly',
},

'ERA5':{
    'mod':'ERA5',
    'sim':'ERA5_31',
    'case': 'plev',
    'dom_key':'dom_ERA5_download',
    'label':'ERA5',
    'freq':'daily',
},
'ERA5_gulf':{
    'mod':'ERA5',
    'sim':'ERA5_31',
    'case': 'plev',
    'dom_key':'dom_ERA5_gulf',
    'label':'ERA5',
    'freq':'daily',
},

'GPM_IMERG':{
    'mod':'GPM_IMERG',
    'sim':'GPM_IMERG',
    'case': 'daily',
    'dom_key':'SA',
    'label':'GPM',
    'freq':'daily',
},

'CMORPH':{
    'mod':'CMORPH',
    'sim':'CMORPH',
    'case': 'daily',
    'dom_key':'SA',
    'label':'CMORPH',
    'freq':'daily',
},


'COSMO_4.4_test_01':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_01',
    'dom_key':'dom_native',
    'label':'01',
    'freq':'daily',
},
'COSMO_4.4_test_02':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_02',
    'dom_key':'dom_native',
    'label':'02',
    'freq':'daily',
},
'COSMO_4.4_test_03':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_03',
    'dom_key':'dom_native',
    'label':'03',
    'freq':'daily',
},
'COSMO_4.4_test_04':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_04',
    'dom_key':'dom_native',
    'label':'04',
    'freq':'daily',
},
'COSMO_4.4_test_05':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_05',
    'dom_key':'dom_native',
    'label':'05',
    'freq':'daily',
},
'COSMO_4.4_test_06':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_06',
    'dom_key':'dom_native',
    'label':'06',
    'freq':'daily',
},
'COSMO_4.4_test_07':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_07',
    'dom_key':'dom_native',
    'label':'02',
    'freq':'daily',
},
'COSMO_4.4_test_08':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_08',
    'dom_key':'dom_native',
    'label':'08',
    'freq':'daily',
},
'COSMO_4.4_test_09':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_09',
    'dom_key':'dom_native',
    'label':'09',
    'freq':'daily',
},
'COSMO_4.4_test_10':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_10',
    'dom_key':'dom_native',
    'label':'10',
    'freq':'daily',
},
'COSMO_4.4_test_01':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_01',
    'dom_key':'dom_native',
    'label':'01',
    'freq':'daily',
},
'COSMO_4.4_test_02':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_02',
    'dom_key':'dom_native',
    'label':'02',
    'freq':'daily',
},
'COSMO_4.4_test_03':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_03',
    'dom_key':'dom_native',
    'label':'03',
    'freq':'daily',
},
'COSMO_4.4_test_04':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_04',
    'dom_key':'dom_native',
    'label':'04',
    'freq':'daily',
},
'COSMO_4.4_test_05':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_05',
    'dom_key':'dom_native',
    'label':'05',
    'freq':'daily',
},
'COSMO_4.4_test_06':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_06',
    'dom_key':'dom_native',
    'label':'06',
    'freq':'daily',
},
'COSMO_4.4_test_07':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_07',
    'dom_key':'dom_native',
    'label':'02',
    'freq':'daily',
},
'COSMO_4.4_test_08':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_08',
    'dom_key':'dom_native',
    'label':'08',
    'freq':'daily',
},
'COSMO_4.4_test_09':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_09',
    'dom_key':'dom_native',
    'label':'09',
    'freq':'daily',
},
'COSMO_4.4_test_10':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_10',
    'dom_key':'dom_native',
    'label':'10',
    'freq':'daily',
},
'COSMO_4.4_test_11':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_11',
    'dom_key':'dom_native',
    'label':'11',
    'freq':'daily',
},
'COSMO_4.4_test_12':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_12',
    'dom_key':'dom_native',
    'label':'12',
    'freq':'daily',
},
'COSMO_4.4_test_13':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_13',
    'dom_key':'dom_native',
    'label':'13',
    'freq':'daily',
},
'COSMO_4.4_test_14':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_14',
    'dom_key':'dom_native',
    'label':'14',
    'freq':'daily',
},
'COSMO_4.4_test_15':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_15',
    'dom_key':'dom_native',
    'label':'15',
    'freq':'daily',
},
'COSMO_4.4_test_16':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_16',
    'dom_key':'dom_native',
    'label':'16',
    'freq':'daily',
},
'COSMO_4.4_test_17':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_17',
    'dom_key':'dom_native',
    'label':'12',
    'freq':'daily',
},
'COSMO_4.4_test_18':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_18',
    'dom_key':'dom_native',
    'label':'18',
    'freq':'daily',
},
'COSMO_4.4_test_19':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_19',
    'dom_key':'dom_native',
    'label':'19',
    'freq':'daily',
},
'COSMO_4.4_test_20':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_20',
    'dom_key':'dom_native',
    'label':'20',
    'freq':'daily',
},
'COSMO_4.4_test_21':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_21',
    'dom_key':'dom_native',
    'label':'21',
    'freq':'daily',
},
'COSMO_4.4_test_22':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_22',
    'dom_key':'dom_native',
    'label':'22',
    'freq':'daily',
},
'COSMO_4.4_test_23':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_23',
    'dom_key':'dom_native',
    'label':'23',
    'freq':'daily',
},
'COSMO_4.4_test_24':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_24',
    'dom_key':'dom_native',
    'label':'24',
    'freq':'daily',
},
'COSMO_4.4_test_25':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_25',
    'dom_key':'dom_native',
    'label':'25',
    'freq':'daily',
},
'COSMO_4.4_test_26':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_26',
    'dom_key':'dom_native',
    'label':'26',
    'freq':'daily',
},
'COSMO_4.4_test_27':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_27',
    'dom_key':'dom_native',
    'label':'22',
    'freq':'daily',
},
'COSMO_4.4_test_28':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_28',
    'dom_key':'dom_native',
    'label':'28',
    'freq':'daily',
},
'COSMO_4.4_test_29':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_29',
    'dom_key':'dom_native',
    'label':'29',
    'freq':'daily',
},
'COSMO_4.4_test_30':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_30',
    'dom_key':'dom_native',
    'label':'30',
    'freq':'daily',
},
'COSMO_4.4_test_31':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_31',
    'dom_key':'dom_native',
    'label':'31',
    'freq':'daily',
},
'COSMO_4.4_test_32':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_32',
    'dom_key':'dom_native',
    'label':'32',
    'freq':'daily',
},
'COSMO_4.4_test_33':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_33',
    'dom_key':'dom_native',
    'label':'33',
    'freq':'daily',
},
'COSMO_4.4_test_34':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_34',
    'dom_key':'dom_native',
    'label':'34',
    'freq':'daily',
},
'COSMO_4.4_test_35':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_35',
    'dom_key':'dom_native',
    'label':'35',
    'freq':'daily',
},
'COSMO_4.4_test_36':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_36',
    'dom_key':'dom_native',
    'label':'36',
    'freq':'daily',
},
'COSMO_4.4_test_37':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_37',
    'dom_key':'dom_native',
    'label':'32',
    'freq':'daily',
},
'COSMO_4.4_test_38':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_38',
    'dom_key':'dom_native',
    'label':'38',
    'freq':'daily',
},
'COSMO_4.4_test_39':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_39',
    'dom_key':'dom_native',
    'label':'39',
    'freq':'daily',
},
'COSMO_4.4_test_40':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_40',
    'dom_key':'dom_native',
    'label':'40',
    'freq':'daily',
},
'COSMO_4.4_test_41':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_41',
    'dom_key':'dom_native',
    'label':'41',
    'freq':'daily',
},
'COSMO_4.4_test_42':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_42',
    'dom_key':'dom_native',
    'label':'42',
    'freq':'daily',
},
'COSMO_4.4_test_43':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_43',
    'dom_key':'dom_native',
    'label':'43',
    'freq':'daily',
},
'COSMO_4.4_test_44':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_44',
    'dom_key':'dom_native',
    'label':'44',
    'freq':'daily',
},
'COSMO_4.4_test_45':{
    'mod':'COSMO',
    'sim':'COSMO_4.4',
    'case':'test_45',
    'dom_key':'dom_native',
    'label':'45',
    'freq':'daily',
},











'COSMO_12_ctrl':{
    'mod':'COSMO',
    'sim':'COSMO_12',
    'case':'SA_12_ctrl',
    'dom_key':'dom_native',
    'label':'CTRL 12',
    'freq':'daily',
},
'COSMO_12_pgw':{
    'mod':'COSMO',
    'sim':'COSMO_12',
    'case':'SA_12_pgw',
    'dom_key':'dom_native',
    'label':'PGW 12',
    'freq':'daily',
},

'COSMO_3.3_ctrl':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_ctrl',
    'dom_key':'dom_native',
    #'label':'COSMO 3 CTRL',
    'label':'CTRL',
    'freq':'daily',
},
'COSMO_3.3_pgw':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw',
    'dom_key':'dom_native',
    'label':'PGW',
    'freq':'daily',
},
'COSMO_3.3_pgw2':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw2',
    'dom_key':'dom_native',
    'label':'PGW2',
    'freq':'daily',
},
'COSMO_3.3_pgw3':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw3',
    'dom_key':'dom_native',
    'label':'PGW3',
    'freq':'daily',
},
'COSMO_3.3_itcz_pgw':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_itcz_pgw',
    'dom_key':'dom_native',
    'label':'PGW ITCZ',
    'freq':'daily',
},
'COSMO_3.3_itcz_pgw2':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_itcz_pgw2',
    'dom_key':'dom_native',
    'label':'PGW2 ITCZ',
    'freq':'daily',
},
'COSMO_3.3_itcz_pgw_OLD':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_itcz_pgw_OLD',
    'dom_key':'dom_native',
    'label':'PGW ITCZ OLD',
    'freq':'daily',
},
'COSMO_3.3_pgw_Amon':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw_Amon',
    'dom_key':'dom_native',
    'label':'PGW Amon',
    'freq':'daily',
},
'COSMO_3.3_pgw_300hPa':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw_300hPa',
    'dom_key':'dom_native',
    #'label':'COSMO 3 PGW',
    'label':'PGW 300hPa',
    'freq':'daily',
},
'COSMO_3.3_pgw_300hPa_rdheight2':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw_300hPa_rdheight2',
    'dom_key':'dom_native',
    'label':'PGW 300hPa RDH2',
    'freq':'daily',
},
'COSMO_3.3_pgw_100hPa':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw_100hPa',
    'dom_key':'dom_native',
    #'label':'COSMO 3 PGW',
    'label':'PGW 100hPa',
    'freq':'daily',
},
'COSMO_3.3_pgw_500hPa':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw_500hPa',
    'dom_key':'dom_native',
    #'label':'COSMO 3 PGW',
    'label':'PGW 500hPa',
    'freq':'daily',
},
'COSMO_3.3_pgw_200hPa':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw_200hPa',
    'dom_key':'dom_native',
    #'label':'COSMO 3 PGW',
    'label':'PGW 200hPa',
    'freq':'daily',
},
'COSMO_3.3_pgw_final_test':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw_final_test',
    'dom_key':'dom_native',
    'label':'final test',
    'freq':'daily',
},
'COSMO_3.3_pgw_OLD':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw_OLD',
    'dom_key':'dom_native',
    'label':'COSMO 3 OLD PGW',
    'freq':'daily',
},

'COSMO_3.3_ctrl_BC':{
    'mod':'INT2LM',
    'sim':'INT2LM_3.3',
    'case':'SA_3_ctrl',
    'dom_key':'dom_native',
    'label':'CTRL BC',
    'freq':'daily',
},
'COSMO_3.3_pgw_BC':{
    'mod':'INT2LM',
    'sim':'INT2LM_3.3',
    'case':'SA_3_pgw',
    'dom_key':'dom_native',
    'label':'PGW BC',
    'freq':'daily',
},
'COSMO_3.3_pgwnp_BC':{
    'mod':'INT2LM',
    'sim':'INT2LM_3.3',
    'case':'SA_3_pgwnp',
    'dom_key':'dom_native',
    'label':'no P INT2LM',
    'freq':'daily',
},
'COSMO_3.3_pgw5_BC':{
    'mod':'INT2LM',
    'sim':'INT2LM_3.3',
    'case':'SA_3_pgw5',
    'dom_key':'dom_native',
    'label':'PGW5 BC',
    'freq':'daily',
},
'COSMO_3.3_pgw6_BC':{
    'mod':'INT2LM',
    'sim':'INT2LM_3.3',
    'case':'SA_3_pgw6',
    'dom_key':'dom_native',
    'label':'PGW6 BC',
    'freq':'daily',
},
'COSMO_3.3_pgw9_BC':{
    'mod':'INT2LM',
    'sim':'INT2LM_3.3',
    'case':'SA_3_pgw9',
    'dom_key':'dom_native',
    'label':'PGW9 BC',
    'freq':'daily',
},
'COSMO_3.3_pgw10_BC':{
    'mod':'INT2LM',
    'sim':'INT2LM_3.3',
    'case':'SA_3_pgw10',
    'dom_key':'dom_native',
    'label':'PGW10 BC',
    'freq':'daily',
},
'COSMO_3.3_pgw11_BC':{
    'mod':'INT2LM',
    'sim':'INT2LM_3.3',
    'case':'SA_3_pgw11',
    'dom_key':'dom_native',
    'label':'PGW11 BC',
    'freq':'daily',
},
'COSMO_3.3_pgw12_BC':{
    'mod':'INT2LM',
    'sim':'INT2LM_3.3',
    'case':'SA_3_pgw12',
    'dom_key':'dom_native',
    'label':'PGW12 BC',
    'freq':'daily',
},
'COSMO_3.3_pgw14_BC':{
    'mod':'INT2LM',
    'sim':'INT2LM_3.3',
    'case':'SA_3_pgw14',
    'dom_key':'dom_native',
    'label':'PGW14 BC',
    'freq':'daily',
},


'COSMO_3.3_ctrl_ref':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_ctrl_ref',
    'dom_key':'dom_native',
    'label':'CTRL KD 13.5km',
    'freq':'daily',
},
'COSMO_3.3_ctrl_rdheight':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_ctrl_rdheight',
    'dom_key':'dom_native',
    'label':'KD 18km',
    'freq':'daily',
},
'COSMO_3.3_ctrl_rdheight2':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_ctrl_rdheight2',
    'dom_key':'dom_native',
    'label':'CTRL RD24km',
    'freq':'daily',
},
'COSMO_3.3_ctrl_spubc1':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_ctrl_spubc1',
    'dom_key':'dom_native',
    'label':'BC1 13.5km',
    'freq':'daily',
},
'COSMO_3.3_ctrl_rdheight_spubc1':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_ctrl_rdheight_spubc1',
    'dom_key':'dom_native',
    'label':'BC1 18km',
    'freq':'daily',
},
'COSMO_3.3_ctrl_rdheight2_spubc1':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_ctrl_rdheight2_spubc1',
    'dom_key':'dom_native',
    'label':'CTRL RD24km BC1',
    'freq':'daily',
},
'COSMO_3.3_ctrl_rdheight2_spubc1_mlev':{
    'mod':'COSMO_ML',
    'sim':'COSMO_3.3',
    'case':'SA_3_ctrl_rdheight2_spubc1_mlev',
    'dom_key':'dom_native',
    'label':'CTRL BC1 ml',
    'freq':'daily',
},
'COSMO_3.3_ctrl_qi0':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_ctrl_qi0',
    'dom_key':'dom_native',
    'label':'qi0',
    'freq':'daily',
},
'COSMO_3.3_ctrl_nodamp':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_ctrl_nodamp',
    'dom_key':'dom_native',
    'label':'no damp',
    'freq':'daily',
},
'COSMO_3.3_ctrl_cloudnum':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_ctrl_cloudnum',
    'dom_key':'dom_native',
    'label':'clodnum',
    'freq':'daily',
},




'COSMO_3.3_pgw_ref':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw_ref',
    'dom_key':'dom_native',
    'label':'PGW KD 13.5km',
    'freq':'daily',
},
'COSMO_3.3_pgw_rdheight':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw_rdheight',
    'dom_key':'dom_native',
    'label':'PGW KD 18km',
    'freq':'daily',
},
'COSMO_3.3_pgw_rdheight2':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw_rdheight2',
    'dom_key':'dom_native',
    'label':'PGW RD24',
    'freq':'daily',
},
'COSMO_3.3_pgw_spubc1':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw_spubc1',
    'dom_key':'dom_native',
    'label':'PGW BC1 13.5km',
    'freq':'daily',
},
'COSMO_3.3_pgw_rdheight_spubc1':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw_rdheight_spubc1',
    'dom_key':'dom_native',
    'label':'PGW BC1 18km',
    'freq':'daily',
},
'COSMO_3.3_pgw_rdheight2_spubc1':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw_rdheight2_spubc1',
    'dom_key':'dom_native',
    'label':'PGW BC1',
    'freq':'daily',
},
'COSMO_3.3_pgw_qi0':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw_qi0',
    'dom_key':'dom_native',
    'label':'PGW qi0',
    'freq':'daily',
},
'COSMO_3.3_pgw_nodamp':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw_nodamp',
    'dom_key':'dom_native',
    'label':'PGW no damp',
    'freq':'daily',
},
'COSMO_3.3_pgw_cloudnum':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw_cloudnum',
    'dom_key':'dom_native',
    'label':'PGW cloudnum',
    'freq':'daily',
},




'COSMO_3.3_pgwnp_ref':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgwnp_ref',
    'dom_key':'dom_native',
    'label':'no P KD 13.5km',
    'freq':'daily',
},
'COSMO_3.3_pgwnp_rdheight2_spubc1':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgwnp_rdheight2_spubc1',
    'dom_key':'dom_native',
    'label':'no P BC1 24km',
    'freq':'daily',
},




'COSMO_3.3_pgw5_rdheight2':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw5_rdheight2',
    'dom_key':'dom_native',
    'label':'PGW5 KD',
    'freq':'daily',
},
'COSMO_3.3_pgw5_rdheight2_spubc1':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw5_rdheight2_spubc1',
    'dom_key':'dom_native',
    'label':'PGW5 BC1',
    'freq':'daily',
},



'COSMO_3.3_pgw6_rdheight2':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw6_rdheight2',
    'dom_key':'dom_native',
    'label':'PGW6 KD',
    'freq':'daily',
},
'COSMO_3.3_pgw6_rdheight2_spubc1':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw6_rdheight2_spubc1',
    'dom_key':'dom_native',
    'label':'PGW6 BC1',
    'freq':'daily',
},




#'COSMO_3.3_pgw7_rdheight2':{
#    'mod':'COSMO',
#    'sim':'COSMO_3.3',
#    'case':'SA_3_pgw7_rdheight2',
#    'dom_key':'dom_native',
#    'label':'PGW7 KD',
#    'freq':'daily',
#},
'COSMO_3.3_pgw6_rdheight2_2':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw6_rdheight2_2',
    'dom_key':'dom_native',
    'label':'PGW7 KD',
    'freq':'daily',
},


#'COSMO_3.3_pgw8_rdheight2':{
#    'mod':'COSMO',
#    'sim':'COSMO_3.3',
#    'case':'SA_3_pgw8_rdheight2',
#    'dom_key':'dom_native',
#    'label':'PGW8 KD',
#    'freq':'daily',
#},
'COSMO_3.3_pgw6_rdheight2_3':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw6_rdheight2_3',
    'dom_key':'dom_native',
    'label':'PGW8 KD',
    'freq':'daily',
},




'COSMO_3.3_pgw9_rdheight2_spubc1':{
    'mod':'COSMO_ML',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw9_rdheight2_spubc1',
    'dom_key':'dom_native',
    'label':'PGW9 BC1',
    'freq':'daily',
},
'COSMO_3.3_pgw9_rdheight2_spubc1_mlev':{
    'mod':'COSMO_ML',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw9_rdheight2_spubc1_mlev',
    'dom_key':'dom_native',
    'label':'PGW9 BC1 ml',
    'freq':'daily',
},
'COSMO_3.3_pgw9_rdheight2':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw9_rdheight2',
    'dom_key':'dom_native',
    'label':'PGW9 KD',
    'freq':'daily',
},

'COSMO_3.3_pgw10_rdheight2_spubc1':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw10_rdheight2_spubc1',
    'dom_key':'dom_native',
    'label':'PGW10 BC1',
    'freq':'daily',
},
'COSMO_3.3_pgw10_rdheight2':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw10_rdheight2',
    'dom_key':'dom_native',
    'label':'PGW10 KD',
    'freq':'daily',
},


'COSMO_3.3_pgw11_rdheight2_spubc1':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw11_rdheight2_spubc1',
    'dom_key':'dom_native',
    'label':'PGW11 BC1',
    'freq':'daily',
},
'COSMO_3.3_pgw11_rdheight2':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw11_rdheight2',
    'dom_key':'dom_native',
    'label':'PGW11 KD',
    'freq':'daily',
},

'COSMO_3.3_pgw12_rdheight2_spubc1':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw12_rdheight2_spubc1',
    'dom_key':'dom_native',
    'label':'PGW12 BC1',
    'freq':'daily',
},
'COSMO_3.3_pgw12_rdheight2':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw12_rdheight2',
    'dom_key':'dom_native',
    'label':'PGW12 KD',
    'freq':'daily',
},

'COSMO_3.3_pgw13_rdheight2_spubc1':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw13_rdheight2_spubc1',
    'dom_key':'dom_native',
    'label':'PGW13 BC1',
    'freq':'daily',
},
'COSMO_3.3_pgw13_rdheight2':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw13_rdheight2',
    'dom_key':'dom_native',
    'label':'PGW13 KD',
    'freq':'daily',
},

'COSMO_3.3_pgw14_rdheight2_spubc1':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw14_rdheight2_spubc1',
    'dom_key':'dom_native',
    'label':'PGW14 BC1',
    'freq':'daily',
},
'COSMO_3.3_pgw14_rdheight2':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw14_rdheight2',
    'dom_key':'dom_native',
    'label':'PGW14 KD',
    'freq':'daily',
},


'COSMO_3.3_pgw15_rdheight2':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw15_rdheight2',
    'dom_key':'dom_native',
    'label':'PGW15 KD',
    'freq':'daily',
},

'COSMO_3.3_pgw16_rdheight2':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw16_rdheight2',
    'dom_key':'dom_native',
    'label':'PGW16 KD',
    'freq':'daily',
},

'COSMO_3.3_pgw17':{
    'mod':'COSMO',
    'sim':'COSMO_3.3',
    'case':'SA_3_pgw17',
    'dom_key':'dom_native',
    'label':'PGW17 KD 13.5',
    'freq':'daily',
},



'COSMO_12_ref':{
    'mod':'COSMO',
    'sim':'COSMO_12',
    'case':'SA_12_ref',
    'dom_key':'dom_native',
    'label':'HYMET',
},
'COSMO_12_tuned':{
    'mod':'COSMO',
    'sim':'COSMO_12',
    'case':'SA_12_tuned',
    'dom_key':'dom_native',
    'label':'tuned',
},
'COSMO_12_roshyd':{
    'mod':'COSMO',
    'sim':'COSMO_12',
    'case':'SA_12_roshyd',
    'dom_key':'dom_native',
    'label':'Roshydromet',
},
'COSMO_12_dwd7':{
    'mod':'COSMO',
    'sim':'COSMO_12',
    'case':'SA_12_dwd7',
    'dom_key':'dom_native',
    'label':'DWD testsuite',
},
'COSMO_12_afr':{
    'mod':'COSMO',
    'sim':'COSMO_12',
    'case':'SA_12_afr',
    'dom_key':'dom_native',
    'label':'CORDEX AFR',
},
'COSMO_12_expl':{
    'mod':'COSMO',
    'sim':'COSMO_12',
    'case':'SA_12_expl',
    'dom_key':'dom_native',
    'label':'EXPL',
},


'COSMO_12_ctrl_sens1':{
    'mod':'COSMO',
    'sim':'COSMO_12',
    'case':'SA_12_ctrl_sens1',
    'dom_key':'dom_native',
    'label':'SENS 1',
},
'COSMO_12_ctrl_sens2':{
    'mod':'COSMO',
    'sim':'COSMO_12',
    'case':'SA_12_ctrl_sens2',
    'dom_key':'dom_native',
    'label':'SENS 2',
},
'COSMO_12_ctrl_sens3':{
    'mod':'COSMO',
    'sim':'COSMO_12',
    'case':'SA_12_ctrl_sens3',
    'dom_key':'dom_native',
    'label':'SENS 3',
},
'COSMO_12_ctrl_sens4':{
    'mod':'COSMO',
    'sim':'COSMO_12',
    'case':'SA_12_ctrl_sens4',
    'dom_key':'dom_native',
    'label':'SENS 4',
},
'COSMO_12_ctrl_sens5':{
    'mod':'COSMO',
    'sim':'COSMO_12',
    'case':'SA_12_ctrl_sens5',
    'dom_key':'dom_native',
    'label':'SENS 4',
},
'COSMO_12_ctrl_sens6':{
    'mod':'COSMO',
    'sim':'COSMO_12',
    'case':'SA_12_ctrl_sens4',
    'dom_key':'dom_native',
    'label':'SENS 6',
},



'COSMO_50_ref':{
    'mod':'COSMO',
    'sim':'COSMO_50',
    'case':'SA_50_ref',
    'dom_key':'dom_native',
    'label':'HYMET',
},
'COSMO_50_tuned':{
    'mod':'COSMO',
    'sim':'COSMO_50',
    'case':'SA_50_tuned',
    'dom_key':'dom_native',
    'label':'tuned',
},
'COSMO_50_roshyd':{
    'mod':'COSMO',
    'sim':'COSMO_50',
    'case':'SA_50_roshyd',
    'dom_key':'dom_native',
    'label':'Roshydromet',
},
'COSMO_50_dwd7':{
    'mod':'COSMO',
    'sim':'COSMO_50',
    'case':'SA_50_dwd7',
    'dom_key':'dom_native',
    'label':'DWD testsuite',
},
'COSMO_50_afr':{
    'mod':'COSMO',
    'sim':'COSMO_50',
    'case':'SA_50_afr',
    'dom_key':'dom_native',
    'label':'CORDEX AFR',
},
'COSMO_50_expl':{
    'mod':'COSMO',
    'sim':'COSMO_50',
    'case':'SA_50_expl',
    'dom_key':'dom_native',
    'label':'EXPL',
},

'COSMO_50_ctrl':{
    'mod':'COSMO',
    'sim':'COSMO_50',
    'case':'SA_50_ctrl',
    'dom_key':'dom_native',
    'label':'COSMO 50',
    'freq':'daily',
},


'gulf_12':{
    'mod':'COSMO',
    'sim':'COSMO_12',
    'case':'gulf_12',
    'dom_key':'dom_native',
    'label':'COSMO 12',
    'freq':'daily',
},
'gulf_2':{
    'mod':'COSMO',
    'sim':'COSMO_2.2',
    'case':'gulf_2',
    'dom_key':'dom_native',
    'label':'COSMO 2.2',
    'freq':'daily',
},





# soil spinup
'COSMO_24_soil':{
    'mod':'COSMO',
    'sim':'COSMO_24',
    'case':'soil_spinup',
    'dom_key':'dom_native',
    'label':'SOIL',
},




### climate deltas
##############################################################################
'MPI-ESM1-2-HR_delta':{
    'mod':'MPI-ESM1-2-HR_delta',
    'sim':'MPI-ESM1-2-HR_delta',
    'case':'historical_r1i1p1f1_to_ssp585_r1i1p1f1',
    'dom_key':'dom_native',
    'label':'climate \delta',
    'freq':'monthly',
},

}

## add CMIP6 models
##############################################################################
for model_key in models_cmip6:
    for experiment_key,experiment_label in zip(['historical', 'ssp585', 'ssp245'], 
                                               ['HIST', 'SSP5-8.5', 'SSP2-4.5']):
        if model_key in ['CNRM-CM6-1','CNRM-CM6-1-HR','CNRM-ESM2-1',
                        'GISS-E2-1-G', 'GISS-E2-1-H', 'MIROC-ES2L',
                        'UKESM1-0-LL',]:
            mem_src['{}_{}'.format(model_key,experiment_key)] = {
                'mod':model_key,
                'sim':model_key,
                'case':'{}_r1i1p1f2'.format(experiment_key),
                'dom_key':'dom_native',
                'label':'{} {}'.format(model_key, experiment_label),
                'freq':'monthly',
            }
        elif model_key in ['HadGEM3-GC31-LL','HadGEM3-GC31-MM',]:
            mem_src['{}_{}'.format(model_key,experiment_key)] = {
                'mod':model_key,
                'sim':model_key,
                'case':'{}_r1i1p1f3'.format(experiment_key),
                'dom_key':'dom_native',
                'label':'{} {}'.format(model_key, experiment_label),
                'freq':'monthly',
            }
        else:
            mem_src['{}_{}'.format(model_key,experiment_key)] = {
                'mod':model_key,
                'sim':model_key,
                'case':'{}_r1i1p1f1'.format(experiment_key),
                'dom_key':'dom_native',
                'label':'{} {}'.format(model_key, experiment_label),
                'freq':'monthly',
            }

