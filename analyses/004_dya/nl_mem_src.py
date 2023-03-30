#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     collection of model dictionaries (mdicts) that describe
                what members should be used in the analysis. Can be used
                by various analysis namelists.
author			Christoph Heim
date created    07.09.2020
date changed    07.04.2021
usage           use in another script
"""
###############################################################################
import copy
###############################################################################

dya_dom = 'SA'
mem_src = {

###############################################################################
## OBSERVATIONAL DATA SETS
###############################################################################
'obs': {
    'SUOMI_NPP_VIIRS':{
        'mod':'SUOMI_NPP_VIIRS', 'case': 'SA',
        'label':'VIIRS',
    },
    'CM_SAF_MSG_AQUA_TERRA':{
        'mod':'CM_SAF_MSG_AQUA_TERRA',          'case': 'MSG',
        #'label':'CM SAF: MSG, Aqua, Terra',
        'label':'CM SAF',
    },
    'CM_SAF_METEOSAT':{
        'mod':'CM_SAF_METEOSAT',   'case': 'METEOSAT',
        #'label':'CM SAF METEOSAT',
        'label':'CM SAF',
    },
    'CM_SAF_MSG':{
        'mod':'CM_SAF_MSG',          'case': 'MSG',
        #'label':'CM SAF: MSG',
        'label':'CM SAF',
    },
    'CM_SAF_HTOVS':{
        'mod':'CM_SAF_HTOVS',          'case': 'GLOBAL',
        'label':'CM SAF',
    },
    'RADIO_SOUNDING':{
        'mod':'RADIO_SOUNDING',  'case': 'ST_HELENA',
        'label':'Sounding',
    },
    'ERA5_31':{
        'mod':'ERA5',
        'res':31,
        'case': 'ERA5_download',
        'label':'ERA5',
        'color':'k',
    },
    'ERA5_31_OBS':{
        'mod':'ERA5',
        'res':31,
        'case': 'ERA5_download',
        'label':'ERA5',
        'color':'k',
    },
    #'ERA5':{
    #    'mod':'ERA5',            'case': 'SA',
    #    'label':'ERA5',
    #},
    #'SEVIRI_CERES'      :{'mod':'SEVIRI_CERES',    'case': 'SA',
    #                      'label':'CERES',},

    'COSMO_4.4_OBSREF':{
        'mod':'COSMO',
        'res':4.4,
        'case':'SA_DYA_OBSREF',
        'label':'100',
    },
    'COSMO_4.4_CALIB_OBSREF':{
        'mod':'COSMO',
        'res':4.4,
        'case':'SA_DYA_CALIB_OBSREF',
        'label':'150 0.45 2E7',
    },
},



###############################################################################
## IAV MEMBERS
###############################################################################
'iav': {

    'COSMO_3.3_SA_3_long':{
        'mod':'COSMO',
        'res':3.3,
        'case':'SA_3_long',
        'label':'COSMO 3.3',
    },
    'CM_SAF_MSG_AQUA_TERRA':{
        'mod':'CM_SAF_MSG_AQUA_TERRA',          'case': 'MSG',
        #'label':'CM SAF: MSG, Aqua, Terra',
        'label':'CM SAF',
    },

    #'COSMO_4.4':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_long',
    #    'label':'COSMO 4.4',
    #},
    #'COSMO_4.4_2':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_long_2',
    #    'label':'COSMO 4.4 2',
    #},

    #'COSMO_4.4':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_iav',
    #    #'label':'COSMO 4.4 SA',
    #    'label':'C4 SA',
    #},
    #'COSMO_4.4_SSA':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SSA_test',
    #    #'label':'COSMO 4.4 SSA',
    #    'label':'C4 SSA',
    #},
    #'ERA5_31':{
    #    'mod':'ERA5',
    #    'res':31,
    #    'case': 'SA_4km',
    #    'label':'ERA5',
    #},

    #'COSMO_4.4_small':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_iav_old',
    #    'label':'COSMO 4.4',
    #},
    #'COSMO_2.2':{
    #    'mod':'COSMO',
    #    'res':2.2,
    #    'case':'SA_iav_old',
    #    'label':'COSMO 2.2',
    #},
},


###############################################################################
## SENSITIVITY TESTS SIMULATIONS CLOUD SNAPSHOTS
###############################################################################
'sens_clouds': {
    #'COSMO_4.4':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA',
    #    'label':'100',
    #},
    #'COSMO_4.4_calib_7':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_7',
    #    'label':'50',
    #},
    #'COSMO_4.4_calib_29':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_29',
    #    'label':'100 2E7',
    #},

    #'COSMO_4.4_calib_31':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_31',
    #    'label':'150 0.45 2E7',
    #},
    #'COSMO_3.3_test_8':{
    #    'mod':'COSMO',
    #    'res':3.3,
    #    'case':'SA_3_test_8',
    #    'label':'C3 150 0.45 2E7',
    #},
    #'COSMO_4.4_calib_39':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_39',
    #    'label':'150 0.45 2E7 clc1',
    #},

    #'COSMO_4.4_calib_43':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_43',
    #    'label':'200 0.45 2E7 1.0',
    #},
    #'COSMO_4.4_calib_44':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_44',
    #    'label':'150 0.30 2E7 1.0',
    #},
    #'COSMO_4.4_calib_45':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_45',
    #    'label':'150 0.45 5E7 1.0',
    #},

    #'COSMO_4.4_calib_46':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_46',
    #    'label':'200 0.30 2E7 1.0',
    #},
    'COSMO_4.4_calib_44':{
        'mod':'COSMO',
        'res':4.4,
        'case':'SA_DYA_calib_44',
        'label':'150 0.30 2E7 1.0',
    },
    'COSMO_3.3_test_9':{
        'mod':'COSMO',
        'res':3.3,
        'case':'SA_3_test_9',
        'label':'C3 150 0.30 2E7 1.0',
    },
    'COSMO_3.3_test_10':{
        'mod':'COSMO',
        'res':3.3,
        'case':'SA_3_test_10',
        'label':'C3 150 0.20 2E7 1.0',
    },
    'COSMO_3.3_test_11':{
        'mod':'COSMO',
        'res':3.3,
        'case':'SA_3_test_11',
        'label':'C3 200 0.30 2E7 1.0',
    },
    'COSMO_3.3_test_12':{
        'mod':'COSMO',
        'res':3.3,
        'case':'SA_3_test_12',
        'label':'C3 200 0.25 2E7 1.0',
    },
},


###############################################################################
## SENSITIVITY TESTS SIMULATIONS
###############################################################################
'sens_extpar': {
    #'ERA5_31':{
    #    'mod':'ERA5',
    #    'res':31,
    #    'case': 'ERA5_download',
    #    'label':'ERA5',
    #},

    #'COSMO_4.4_calib_31':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_31',
    #    #'label':'150 0.45 2E7',
    #    'label':'REF',
    #},
    #'COSMO_4.4_calib_40':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_40',
    #    #'label':'150 0.45 2E7 alb3',
    #    'label':'alb',
    #},
    #'COSMO_4.4_calib_41':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_41',
    #    #'label':'150 0.45 2E7 sfc',
    #    'label':'soil/landuse',
    #},
    #'COSMO_4.4_calib_42':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_42',
    #    #'label':'150 0.45 2E7 const',
    #    'label':'alb/soil/landuse',
    #},

},




'sensitivity': {

    #'COSMO_2.2':{
    #    'mod':'COSMO',      'res':2.2,  'case':'SA_DYA',
    #    'label':'COSMO 2.2',
    #},
    #'NICAM_3.5':{
    #    'mod':'NICAM',      'res':3.5,  'case':dya_dom,
    #    'label':'NICAM 3.5'                               
    #},
    #'SAM_4':{
    #    'mod':'SAM',        'res':4,    'case':dya_dom,
    #    'label':'SAM 4'                                   
    #},
    #'UM_5':{
    #    'mod':'UM',         'res':5,    'case':dya_dom,
    #    'label':'UM 5'                                    
    #},
    #'IFS_4':{
    #    'mod':'IFS',        'res':4,    'case':dya_dom,
    #    'label':'IFS 4'                                 
    #},
    #'GEOS_3':{
    #    'mod':'GEOS',       'res':3,    'case':dya_dom,
    #    'label':'GEOS 3'                                  
    #},
    #'ARPEGE-NH_2.5':{
    #    'mod':'ARPEGE-NH',  'res':2.5,  'case':dya_dom,
    #    'label':'ARPEGE-NH 2.5'                         
    #},
    #'FV3_3.25':{
    #    'mod':'FV3',
    #    'res':3.25,
    #    'case':dya_dom,
    #    'label':'FV3 3.25'                                
    #},
    #'ICON_2.5':{
    #    'mod':'ICON',       'res':2.5,  'case':dya_dom,
    #    'label':'ICON 2.5'                                
    #},

    #'ERA5_31':{
    #    'mod':'ERA5',
    #    'res':31,
    #    'case': 'ERA5_download',
    #    'label':'ERA5',
    #},


    #'COSMO_4.4':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA',
    #    'label':'100',
    #},
    #'COSMO_4.4_calib_7':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_7',
    #    'label':'50',
    #},
    ##'COSMO_4.4_calib_2':{
    ##    'mod':'COSMO',
    ##    'res':4.4,
    ##    'case':'SA_DYA_calib_2',
    ##    'label':'50 0.5',
    ##},
    #'COSMO_4.4_calib_11':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_11',
    #    'label':'150 0.8',
    #},


    #'COSMO_4.4_calib_13':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_13',
    #    'label':'100 0.4 5E7',
    #},
    ##'COSMO_4.4_calib_37':{
    ##    'mod':'COSMO',
    ##    'res':4.4,
    ##    'case':'SA_DYA_calib_37',
    ##    'label':'200 0.45 1E7',
    ##},
    ##'COSMO_3.3_test_7':{
    ##    'mod':'COSMO',
    ##    'res':3.3,
    ##    'case':'SA_3_test_7',
    ##    'label':'C3 200 0.45 1E7',
    ##},
    #'ERA5_31':{
    #    'mod':'ERA5',
    #    'res':31,
    #    'case': 'ERA5_download',
    #    'label':'ERA5',
    #},

    'COSMO_3.3_test_ens_1':{
        'mod':'COSMO',
        'res':3.3,
        'case':'SA_3_test_ens_1',
        'label':'SA 1',
    },
    'COSMO_3.3_test_ens_2':{
        'mod':'COSMO',
        'res':3.3,
        'case':'SA_3_test_ens_2',
        'label':'SA 2',
    },
    'COSMO_3.3_test_ens_3':{
        'mod':'COSMO',
        'res':3.3,
        'case':'SA_3_test_ens_3',
        'label':'SA 3',
    },

    'COSMO_3.3_SSA_test_ens_1':{
        'mod':'COSMO',
        'res':3.3,
        'case':'SSA_3_test_ens_1',
        'label':'SSA 1',
    },
    'COSMO_3.3_SSA_test_ens_2':{
        'mod':'COSMO',
        'res':3.3,
        'case':'SSA_3_test_ens_2',
        'label':'SSA 2',
    },
    'COSMO_3.3_SSA_test_ens_3':{
        'mod':'COSMO',
        'res':3.3,
        'case':'SSA_3_test_ens_3',
        'label':'SSA 3',
    },

    'COSMO_3.3_test_ens_1_orig_alb':{
        'mod':'COSMO',
        'res':3.3,
        'case':'SA_3_test_ens_1_orig_alb',
        'label':'SA 1 orig alb',
    },


    ##'COSMO_4.4_calib_29':{
    ##    'mod':'COSMO',
    ##    'res':4.4,
    ##    'case':'SA_DYA_calib_29',
    ##    'label':'100 2E7',
    ##},
    #'COSMO_4.4_calib_31':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_31',
    #    'label':'150 0.45 2E7',
    #},
    #'COSMO_3.3_test_8':{
    #    'mod':'COSMO',
    #    'res':3.3,
    #    'case':'SA_3_test_8',
    #    'label':'C3 150 0.45 2E7',
    #},



    ##'COSMO_4.4_calib_38':{
    ##    'mod':'COSMO',
    ##    'res':4.4,
    ##    'case':'SA_DYA_calib_38',
    ##    'label':'150 0.45 2E7 alb1',
    ##},
    #'COSMO_4.4_calib_40':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_40',
    #    'label':'150 0.45 2E7 alb3',
    #},
    #'COSMO_4.4_calib_41':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_41',
    #    'label':'150 0.45 2E7 sfc',
    #},
    #'COSMO_4.4_calib_42':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_42',
    #    'label':'150 0.45 2E7 const',
    #},

    #'COSMO_4.4_calib_39':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_39',
    #    'label':'150 0.45 2E7 clc1',
    #},
    #'COSMO_4.4_calib_43':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_43',
    #    'label':'200 0.45 2E7 1.0',
    #},
    #'COSMO_4.4_calib_45':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_45',
    #    'label':'150 0.45 5E7 1.0',
    #},
    #'COSMO_4.4_calib_44':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_44',
    #    'label':'150 0.30 2E7 1.0',
    #},
    #'COSMO_3.3_test_9':{
    #    'mod':'COSMO',
    #    'res':3.3,
    #    'case':'SA_3_test_9',
    #    'label':'C3 150 0.30 2E7 1.0',
    #},
    #'COSMO_3.3_test_10':{
    #    'mod':'COSMO',
    #    'res':3.3,
    #    'case':'SA_3_test_10',
    #    'label':'C3 150 0.20 2E7 1.0',
    #},
    #'COSMO_3.3_test_11':{
    #    'mod':'COSMO',
    #    'res':3.3,
    #    'case':'SA_3_test_11',
    #    'label':'C3 200 0.30 2E7 1.0',
    #},
    #'COSMO_3.3_test_12':{
    #    'mod':'COSMO',
    #    'res':3.3,
    #    'case':'SA_3_test_12',
    #    'label':'C3 200 0.25 2E7 1.0',
    #},

    ##'COSMO_4.4_calib_46':{
    ##    'mod':'COSMO',
    ##    'res':4.4,
    ##    'case':'SA_DYA_calib_46',
    ##    'label':'200 0.30 2E7 1.0',
    ##},




    #'COSMO_4.4_calib_33':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_33',
    #    'label':'200 0.45 3E7',
    #},
    #'ERA5_31':{
    #    'mod':'ERA5',
    #    'res':31,
    #    'case': 'ERA5_download',
    #    'label':'ERA5',
    #},
    #'COSMO_4.4_calib_30':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_30',
    #    'label':'100 0.5 5E7',
    #},
    #'COSMO_4.4_calib_34':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_34',
    #    'label':'300 0.45 3E7',
    #},
    #'COSMO_4.4_calib_35':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_35',
    #    'label':'300 0.50 2E7',
    #},
    #'COSMO_4.4_calib_36':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_36',
    #    'label':'200 0.50 3E7',
    #},
    #'COSMO_4.4_calib_28':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_28',
    #    'label':'75 5E7',
    #},
    #'COSMO_4.4_calib_5':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_5',
    #    'label':'100 1.0',
    #},
    #'COSMO_4.4_calib_9':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_9',
    #    'label':'100 0.8',
    #},
    #'COSMO_4.4_calib_10':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_10',
    #    'label':'100 0.8 rl0.4',
    #},
    #'COSMO_4.4_calib_11':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_11',
    #    'label':'150 0.8',
    #},
    #'COSMO_4.4_calib_2':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_2',
    #    'label':'50 0.5',
    #},
    #'COSMO_4.4_calib':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib',
    #    'label':'50 0.5 rl0.1',
    #},
    #'COSMO_4.4_calib_3':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_3',
    #    'label':'60 0.5',
    #},
    #'COSMO_4.4_calib_6':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_6',
    #    'label':'10 0.4',
    #},
    #'COSMO_4.4_calib_8':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_8',
    #    'label':'25 0.4',
    #},
    #'COSMO_4.4_calib_7':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_7',
    #    'label':'50 0.4',
    #},
    #'COSMO_4.4':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA',
    #    'label':'100 0.4',
    #},
    #'COSMO_4.4_calib_13':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_13',
    #    'label':'100 0.4 5E7',
    #},
    #'COSMO_4.4_calib_23':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_23',
    #    'label':'100 0.4 1E7',
    #},
    #'COSMO_4.4_calib_27':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_27',
    #    'label':'100 0.3',
    #},
    #'COSMO_4.4_calib_24':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_24',
    #    'label':'100 0.3 rl1.0',
    #},
    #'COSMO_4.4_calib_26':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_26',
    #    'label':'100 0.3 2E8',
    #},
    #'COSMO_4.4_calib_22':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_22',
    #    'label':'100 0.3 5E7',
    #},
    #'COSMO_4.4_calib_25':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_25',
    #    'label':'75 0.3',
    #},
    #'COSMO_4.4_calib_12':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_12',
    #    'label':'200 0.2 1E7',
    #},
    #'COSMO_4.4_calib_18':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_18',
    #    'label':'50 0.2',
    #},
    #'COSMO_4.4_calib_17':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_17',
    #    'label':'50 0.2 1E8',
    #},
    #'COSMO_4.4_calib_21':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_21',
    #    'label':'100 0.2 5E7',
    #},
    #'COSMO_4.4_calib_16':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_16',
    #    'label':'50 0.1 1E8',
    #},
    #'COSMO_4.4_calib_19':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_19',
    #    'label':'50 0.1 1E7',
    #},
    #'COSMO_4.4_calib_20':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_20',
    #    'label':'100 0.1 5E7',
    #},
    #'COSMO_4.4_calib_15':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_15',
    #    'label':'200 0.1 1E7',
    #},
    #'COSMO_4.4_calib_14':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_14',
    #    'label':'200 0.01 1E7',
    #},
    #'COSMO_4.4_calib_29':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_29',
    #    'label':'100 2E7',
    #},
    #'COSMO_4.4_calib_30':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_30',
    #    'label':'100 0.5 5E7',
    #},
    #'COSMO_4.4_calib_31':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_31',
    #    'label':'150 0.45 2E7',
    #},
    #'COSMO_4.4_calib_32':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_32',
    #    'label':'100 5E7 clc',
    #},




    #'C4_bc_1h_1':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_iav',
    #    'label':'1h (1)',
    #    'plot_pos':(0,0),
    #},
    #'C4_bc_1h_2':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_bc_1h_2',
    #    'label':'1h (2)',
    #    'plot_pos':(0,1),
    #},
    #'C4_bc_1h_3':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_bc_1h_3',
    #    'label':'1h (3)',
    #    'plot_pos':(0,2),
    #},
    #'C4_bc_6h_1':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_bc_6h_1',
    #    'label':'6h (1)',
    #    'plot_pos':(1,0),
    #},
    #'C4_bc_6h_2':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_bc_6h_2',
    #    'label':'6h (2)',
    #    'plot_pos':(1,2),
    #},
    #'C4_bc_6h_3':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_bc_6h_3',
    #    'label':'6h (3)',
    #    'plot_pos':(1,1),
    #},

},





###############################################################################
## DYAMOND ANALYSIS MEMBERS
###############################################################################
'dya_all': {
    ### main set of simulations
    'COSMO_2.2':{
        'mod':'COSMO',      'res':2.2,  'case':'SA_DYA',
        'label':'COSMO 2.2',
    },
    'NICAM_3.5':{
        'mod':'NICAM',      'res':3.5,  'case':dya_dom,
        'label':'NICAM 3.5'                               
    },
    'SAM_4':{
        'mod':'SAM',        'res':4,    'case':dya_dom,
        'label':'SAM 4'                                   
    },
    'ICON_2.5':{
        'mod':'ICON',       'res':2.5,  'case':dya_dom,
        'label':'ICON 2.5'                                
    },
    'UM_5':{
        'mod':'UM',         'res':5,    'case':dya_dom,
        'label':'UM 5'                                    
    },
    'MPAS_3.75':{
        'mod':'MPAS',       'res':3.75, 'case':dya_dom,
        'label':'MPAS 3.75'                             
    },
    'IFS_4':{
        'mod':'IFS',        'res':4,    'case':dya_dom,
        'label':'IFS 4'                                 
    },
    'GEOS_3':{
        'mod':'GEOS',       'res':3,    'case':dya_dom,
        'label':'GEOS 3'                                  
    },
    'ARPEGE-NH_2.5':{
        'mod':'ARPEGE-NH',  'res':2.5,  'case':dya_dom,
        'label':'ARPEGE-NH 2.5'                         
    },
    'FV3_3.25':{
        'mod':'FV3',
        'res':3.25,
        'case':dya_dom,
        'label':'FV3 3.25'                                
    },
    'ERA5_31':{
        'mod':'ERA5',
        'res':31,
        #'case': 'SA_4km',
        'case': 'ERA5_download',
        'label':'ERA5',
    },



    #### all others
    'COSMO_12':{
        'mod':'COSMO',      'res':12,   'case':'SA_DYA',
        'label':'COSMO 12',                               
    },
    'COSMO_4.4':{
        'mod':'COSMO',      'res':4.4,  'case':'SA_DYA',
        'label':'COSMO 4.4',
    },
    #'COSMO_4.4_calib_7':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_7',
    #    'label':'COSMO 4.4 tl50m',
    #},
    #'COSMO_4.4_calib_8':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_8',
    #    'label':'COSMO 4.4 tl25m',
    #},
    'COSMO_1.1':{
        'mod':'COSMO',      'res':1.1,  'case':'SA_DYA',
        'label':'COSMO 1.1'                               
    },
    'COSMO_0.5':{
        'mod':'COSMO',      'res':0.5,  'case':'SA_DYA',
        'label':'COSMO 0.5',                              
    },
    'NICAM_7':{
        'mod':'NICAM',      'res':7,    'case':dya_dom,
        'label':'NICAM 7'                                 
    },
    'ICON_10':{
        'mod':'ICON',       'res':10,   'case':dya_dom,
        'label':'ICON 10'                               
    },
    'MPAS_7.5':{
        'mod':'MPAS',       'res':7.5,  'case':dya_dom,
        'label':'MPAS 7.5'                              
    },
    'IFS_9':{
        'mod':'IFS',        'res':9,    'case':dya_dom,
        'label':'IFS 9'                                   
    },
},



'dya_main': {
    ##### main set of simulations
    'COSMO_2.2':{
        'mod':'COSMO',      'res':2.2,  'case':'SA_DYA',
        'label':'COSMO 2.2',
    },
    'NICAM_3.5':{
        'mod':'NICAM',      'res':3.5,  'case':dya_dom,
        'label':'NICAM 3.5'                               
    },
    'SAM_4':{
        'mod':'SAM',        'res':4,    'case':dya_dom,
        'label':'SAM 4'                                   
    },
    'ICON_2.5':{
        'mod':'ICON',       'res':2.5,  'case':dya_dom,
        'label':'ICON 2.5'                                
    },
    'UM_5':{
        'mod':'UM',         'res':5,    'case':dya_dom,
        'label':'UM 5'                                    
    },
    'MPAS_3.75':{
        'mod':'MPAS',       'res':3.75, 'case':dya_dom,
        'label':'MPAS 3.75'                             
    },
    'IFS_4':{
        'mod':'IFS',        'res':4,    'case':dya_dom,
        'label':'IFS 4'                                 
    },
    'GEOS_3':{
        'mod':'GEOS',       'res':3,    'case':dya_dom,
        'label':'GEOS 3'                                  
    },
    'ARPEGE-NH_2.5':{
        'mod':'ARPEGE-NH',  'res':2.5,  'case':dya_dom,
        'label':'ARPEGE-NH 2.5'                         
    },
    'FV3_3.25':{
        'mod':'FV3',        'res':3.25, 'case':dya_dom,
        'label':'FV3 3.25'                                
    },

    'ERA5_31':{
        'mod':'ERA5',
        'res':31,
        'case': 'ERA5_download',
        'label':'ERA5',
        'color':'k',
    },
},



###############################################################################
## COSMO MEMBERS
###############################################################################
'cosmo': {
    'COSMO_12':{
        'mod':'COSMO',      'res':12,   'case':'SA_DYA',
        'label':'COSMO 12',                               
    },
    'COSMO_4.4':{
        'mod':'COSMO',      'res':4.4,  'case':'SA_DYA',
        'label':'COSMO 4.4',
    },
    #'COSMO_4.4_calib_7':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_7',
    #    'label':'COSMO 4.4 tl50m',
    #},
    #'COSMO_4.4_calib_8':{
    #    'mod':'COSMO',
    #    'res':4.4,
    #    'case':'SA_DYA_calib_8',
    #    'label':'COSMO 4.4 tl25m',
    #},
    'COSMO_2.2':{
        'mod':'COSMO',      'res':2.2,  'case':'SA_DYA',
        'label':'COSMO 2.2',
    },
    'COSMO_1.1':{
        'mod':'COSMO',      'res':1.1,  'case':'SA_DYA',
        'label':'COSMO 1.1'                               
    },
    'COSMO_0.5':{
        'mod':'COSMO',      'res':0.5,  'case':'SA_DYA',
        'label':'COSMO 0.5',                              
    },

    'ERA5_31':{
        'mod':'ERA5',
        'res':31,
        'case': 'ERA5_download',
        'label':'ERA5',
        'color':'k',
    },
},





###############################################################################
## COSMO SNAPSHOT MEMBERS
###############################################################################
'cosmo_snapshot': {
    'COSMO_12':{
        'mod':'COSMO',      'res':12,   'case':'SA_DYA',
        'label':'COSMO 12',                               
    },
    'COSMO_4.4':{
        'mod':'COSMO',      'res':4.4,  'case':'SA_DYA',
        'label':'COSMO 4.4',
    },
    'COSMO_2.2':{
        'mod':'COSMO',      'res':2.2,  'case':'SA_DYA',
        'label':'COSMO 2.2',
    },
    'COSMO_1.1':{
        'mod':'COSMO',      'res':1.1,  'case':'SA_DYA',
        'label':'COSMO 1.1'                               
    },
    'COSMO_0.5':{
        'mod':'COSMO',      'res':0.5,  'case':'SA_DYA',
        'label':'COSMO 0.5',                              
    },
},





###############################################################################
## DEBUG SIMULATION
###############################################################################
'debug': {
    'C12':{
        'mod':'COSMO',      'res':12,   'case':'SA_DYA',
        'label':'COSMO 12',                               
    },
},

}

mem_src['all_members'] = copy.copy(mem_src['dya_all'])
# add OBS
mem_src['all_members'].update(copy.copy(mem_src['obs']))
