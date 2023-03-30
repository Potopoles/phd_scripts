#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Namelist for analysis of models
author			Christoph Heim
date created    09.07.2019
date changed    11.04.2022
usage           use in another script
"""
###############################################################################
import os, copy
###############################################################################

nlm = {
###############################################################################
################### MODELS
###############################################################################

'COSMO' :{
    'vkeys'     :{
        'HSURF'     :'HSURF', 
        'FRLAND'    :'FR_LAND', 
        'ALBSURF'   :'ALB_RAD', 

        'TSOIL'     :'T_SO',       
        'WSOIL'     :'W_SO',       
        'RUNOFFG'   :'RUNOFF_G',       
        'RUNOFFS'   :'RUNOFF_S',       
        'TSURF'     :'T_S',       
        'QVSURF'    :'QV_S',      

        'U'         :'U', 
        'V'         :'V', 
        'W'         :'W', 
        'T'         :'T', 
        'P'         :'P', 
        'QC'        :'QC', 
        'QV'        :'QV', 
        'QI'        :'QI', 
        'QR'        :'QR', 
        'QG'        :'QG', 
        'QS'        :'QS', 
        'TKE'       :'TKE', 

        'U10M'      :'U_10M',
        'V10M'      :'V_10M',
        'T2M'       :'T_2M',
        'RH2M'      :'RELHUM_2M', 
        'QV2M'      :'QV_2M', 
        'PS'        :'PS', 
        'GUST10M'   :'VMAX_10M',       
        'TMAX2M'    :'TMAX_2M',       
        'TMIN2M'    :'TMIN_2M',       
        'CAPE'      :'CAPE_ML',       
        'CIN'       :'CIN_ML',       

        'SWNDTOA'   :'ASOB_T',    
        'SWDTOA'    :'ASOD_T',    
        'LWUTOA'    :'ATHB_T',    
        'CSWNDTOA'  :'ASOBC_T',   
        'CLWUTOA'   :'ATHBC_T',   
        'SWNDSFC'   :'ASOB_S',    
        'SWDIFDSFC' :'ASWDIFD_S',    
        'SWDIRDSFC' :'ASWDIR_S',    
        'SWDIFUSFC' :'ASWDIFU_S',    
        'LWNDSFC'   :'ATHB_S',    
        'LWDSFC'    :'ATHD_S',    
        'CSWNDSFC'  :'ASOBC_S',   
        'CLWNDSFC'  :'ATHBC_S',   

        'SLHFLX'    :'ALHFL_S',
        'SSHFLX'    :'ASHFL_S',
        'SUMFLX'    :'AUMFL_S',
        'SVMFLX'    :'AVMFL_S',

        'CLCL'      :'CLCL',      
        'CLCM'      :'CLCM',      
        'CLCH'      :'CLCH',      
        'CLCT'      :'CLCT',      

        'TQC'       :'TQC', 
        'TQI'       :'TQI',       
        'TQR'       :'TQR',       
        'TQV'       :'TQV',       
        'TQG'       :'TQG',       
        'TQS'       :'TQS',       
        'PP'        :'TOT_PREC', 
        'TWATER'    :'TWATER',       
        'TWATFLXU'  :'TWATFLXU',       
        'TWATFLXV'  :'TWATFLXV',       
    },
    'vert_coord':   'alt',
    'dep' : {
        #'U'         :['HSURF'],
        #'V'         :['HSURF'],
        #'W'         :['HSURF'],
        #'T'         :['HSURF'],
        #'P'         :['HSURF'],
        #'QV'        :['HSURF'],
        #'QC'        :['HSURF'],
        #'QI'        :['HSURF'],
        #'QS'        :['HSURF'],
        #'QG'        :['HSURF'],
        #'QR'        :['HSURF'],
    }
},
'COSMO_ML' :{
    'vkeys'     :{
        'VCOORD'    :'vcoord', 
        'HSURF'     :'HSURF', 
        'FRLAND'    :'FR_LAND', 
        'W'         :'W', 
        'T'         :'T', 
        'P'         :'P', 
    },
    'dep' : {
        'W'         :['VCOORD'],
        'T'         :['VCOORD'],
        'P'         :['VCOORD'],
    },
},
'INT2LM' :{
    'vkeys'     :{
        'VCOORD'    :'vcoord', 
        'HSURF'     :'HSURF', 
        'FRLAND'    :'FR_LAND', 

        'U'         :'U', 
        'V'         :'V', 
        'T'         :'T', 
        'P'         :'PP', 
        #'PPERT'     :'PP', 
        'QV'        :'QV', 
    },
    'dep' : {
        'U'         :['VCOORD'],
        'V'         :['VCOORD'],
        'T'         :['VCOORD'],
        'QV'        :['VCOORD'],
        'P'         :['HSURF','VCOORD'],
    },
},


'NICAM' :{
    'vkeys'     :{
        'U'         :'ms_u', 
        'V'         :'ms_v', 
        'W'         :'ms_w', 
        'T'         :'ms_tem', 
        'P'         :'ms_pres', 
        'ALT'       :None,
        'QC'        :'ms_qc', 
        'QV'        :'ms_qv', 

        'U10M'      :'ss_u10m',
        'V10M'      :'ss_v10m',
        'T2M'       :'ss_t2m',
        'MSLP'      :'ss_slp',

        'LWUTOA'    :'sa_lwu_toa', 
        'SWUTOA'    :'ss_swu_toa', 
        'SWDTOA'    :'ASOD_T', # from COSMO

        #'SST'       :'oa_sst',
        'SST'       :'var34', # from IFS
        'SLHFLX'    :'ss_lh_sfc',
        'SSHFLX'    :'ss_sh_sfc',

        'CLCT'      :None,
        'CLCL'      :None,

        'TQC'       :'sa_cldw', 
        'TQI'       :'sa_cldi', 
        'TQV'       :None,
        'PP'        :'sa_tppn', 
    },
},

'SAM' :{
    'vkeys'     :{
        'U'         :'U', 
        'V'         :'V', 
        'W'         :'W', 
        'T'         :'TABS', 
        'P'         :'PP', 
        'ALT'       :None,
        'QC'        :'QC', 
        'QV'        :'QV', 

        'U10M'      :'U10m',
        'V10M'      :'V10m',
        'T2M'       :'T2m',
        'PS'        :'PSFC',

        'LWUTOA'    :'LWNTA', 
        'SWNDTOA'   :'SWNTA', 
        'SWDTOA'    :'ASOD_T', # from COSMO

        'SST'       :'var34', # from IFS
        'SLHFLX'    :'LHF',
        'SSHFLX'    :'SHF',

        'CLCT'      :None,
        'CLCL'      :None,

        'TQC'       :'CWP', 
        'TQI'       :'IWP', 
        'TQV'       :None,
        'PP'        :'Precac', 
    },
},

'ICON'  :{
    'vkeys'     :{
        'U'         :'U', 
        'V'         :'V', 
        'W'         :'W', 
        'T'         :'T', 
        'P'         :'P', 
        'ALT'       :None,
        'QV'        :'QV', 
        'QC'        :'QC_DIA', 

        'U10M'      :'U_10M',
        'V10M'      :'V_10M',
        'T2M'       :'T_2M',
        'PS'        :'PS',

        'LWUTOA'    :'ATHB_T', 
        'SWNDTOA'   :'ASOB_T', 
        'SWDTOA'    :'ASOD_T', # from COSMO

        'SST'       :'var34', # from IFS
        'SLHFLX'    :'LHFL_S',
        'SSHFLX'    :'SHFL_S',

        'CLCT'      :'CLCT',
        'CLCL'    :None,

        'TQC'       :'TQC_DIA', 
        'TQI'       :'TQI_DIA', 
        'TQV'       :'TQV_DIA', 
        'PP'        :'TOT_PREC', 
    },
    'vgrid'     :os.path.join('model_specific','ICON_hgt.txt'),
},

'UM' :{
    'vkeys'     :{
        'U'         :'eastward_wind', 
        'V'         :'northward_wind', 
        'W'         :'upward_air_velocity', 
        'T'         :'air_temperature', 
        'P'         :'air_pressure', 
        'ALT'       :None,
        'QC'        :'mass_fraction_of_cloud_liquid_water_in_air', 
        'QV'        :'specific_humidity', 

        'U10M'      :'eastward_wind',
        'V10M'      :'northward_wind',
        'T2M'       :'air_temperature',
        'PS'        :'surface_air_pressure', 

        'LWUTOA'    :'toa_outgoing_longwave_flux', 
        'SWUTOA'    :'toa_outgoing_shortwave_flux', 
        'SWDTOA'    :'ASOD_T', # from COSMO

        'SST'       :'var34', # from IFS
        'SLHFLX'    :'surface_upward_latent_heat_flux',
        'SSHFLX'    :'surface_upward_sensible_heat_flux',

        'CLCT'      :'cloud_area_fraction',
        'CLCL'    :None,

        'TQC'       :'atmosphere_mass_content_of_cloud_condensed_water', 
        'TQI'       :'atmosphere_mass_content_of_cloud_ice', 
        'TQV'       :'atmosphere_water_vapor_content', 
        'PP'        :'precipitation_flux', 
    },
    'vgrid'     :os.path.join('model_specific','UM_hgt.txt'),
},

'MPAS' :{
    'vkeys' :{
        'U'         :'uReconstructZonal', 
        'V'         :'uReconstructMeridional', 
        'W'         :'w', 
        'T'         :'temperature', 
        'P'         :'pressure', 
        'ALT'       :None,
        'QC'        :'qc', 
        'QV'        :'qv', 

        'U10M'      :'u10',
        'V10M'      :'v10',
        'T2M'       :'t2m',
        'MSLP'      :'mslp',

        'LWUTOA'    :'olrtoa', 
        'SWNDTOA'   :'acswnett', 
        'SWDTOA'    :'ASOD_T', # from COSMO

        'SST'       :None,
        'SLHFLX'    :None,
        'SSHFLX'    :None,

        'CLCT'      :'cldcvr',
        'CLCL'      :None,

        'TQC'       :'vert_int_qc', 
        'TQI'       :'vert_int_qi', 
        'TQV'       :'vert_int_qv',
        'PPGRID'    :'rainnc', 
        'PPCONV'    :'rainc', 
    },
    'vgrid'     :os.path.join('model_specific','MPAS_hgt.txt'),
},

'IFS' :{
    'vkeys'     :{
        'U'         :'u',
        'V'         :'v',
        'W'         :'param120.128.192',
        'T'         :'t', 
        'P'         :'P', # from preproc
        'ALT'       :'ALT', # from preproc
        'QC'        :'clwc', 
        'QV'        :'q', 

        'U10M'      :'var165',
        'V10M'      :'var166',
        'T2M'       :'var167',
        'PS'        :'var151',

        'LWUTOA'    :'var179', 
        'SWNDTOA'   :'var178', 
        'SWDTOA'    :'ASOD_T', # from COSMO

        'SST'       :'var34',
        'SLHFLX'    :'var147',
        'SSHFLX'    :'var146',

        'CLCT'      :'var164',
        'CLCL'      :'var186',

        'TQC'       :'var78', 
        'TQI'       :'var79', 
        'TQV'       :'var137',
        'PPGRID'    :'var219', 
        'PPCONV'    :'var218', 
    },
    'dep' : {
        'U'         :['ALT'],
        'V'         :['ALT'],
        'W'         :['ALT'],
        'T'         :['ALT'],
        'P'         :['ALT'],
        'QV'        :['ALT'],
        'QC'        :['ALT'],
    }
    #'vgrid'     :os.path.join('model_specific','IFS_hgt.txt'),
},

'GEOS' :{
    'vkeys'     :{
        'U'         :'U',
        'V'         :'V',
        'W'         :'W', 
        'T'         :'T', 
        'P'         :'P',
        'ALT'       :'H', 
        'QC'        :'QL', 
        'QV'        :'QV', 

        'U10M'      :'U10M',
        'V10M'      :'V10M',
        'T2M'       :'T2M',
        'PS'        :'PS',

        'LWUTOA'    :'OLR', 
        'SWNDTOA'   :'SWTNET', 
        'SWDTOA'    :'ASOD_T', # from COSMO

        'SST'       :'var34', # from IFS
        'SLHFLX'    :'EFLUX',
        'SSHFLX'    :'HFLUX',

        'CLCT'      :None,
        'CLCL'      :None,

        'TQC'       :'CWP', 
        'TQI'       :'IWP', 
        'TQV'       :'TQV',
        'PP'        :'PRECTOT', 
    },
    'dep' : {
        'U'         :['ALT'],
        'V'         :['ALT'],
        'W'         :['ALT'],
        'T'         :['ALT'],
        'P'         :['ALT'],
        'QV'        :['ALT'],
        'QC'        :['ALT'],
    }
},

'ARPEGE-NH' :{
    'vkeys'     :{
        'U'         :'u',
        'V'         :'v',
        'W'         :'wz', 
        'T'         :'t', 
        'P'         :None,
        'ALT'       :'z', 
        'QC'        :'clwc', 
        'QV'        :'q', 

        'U10M'      :'10u',
        'V10M'      :'10v',
        'T2M'       :'2t',
        'PS'        :'sp',

        'LWUTOA'    :'ttr', 
        'SWNDTOA'   :'nswrf', 
        'SWDTOA'    :'ASOD_T', # from COSMO

        'SST'       :'var34', # from IFS
        'SLHFLX'    :'lhtfl',
        'SSHFLX'    :'shtfl',

        'CLCT'      :'tcc',
        'CLCL'      :'lcc',

        'TQC'       :'tclw', 
        'TQI'       :'tciw', 
        'TQV'       :'tciwv',
        'PP'        :'param8.1.0', 
    },
    'dep' : {
        'U'         :['ALT'],
        'V'         :['ALT'],
        'W'         :['ALT'],
        'T'         :['ALT'],
        'P'         :['ALT'],
        'QV'        :['ALT'],
        'QC'        :['ALT'],
    }
},

'FV3' :{
    'vkeys'     :{
        'U'         :'u',
        'V'         :'v',
        'W'         :'w', 
        'T'         :'temp', 
        'P'         :None,
        #'ALT'       :'h_plev', 
        'ALT'       :'ALT',  # preprocessing
        'QC'        :'ql_plev', 
        'QV'        :'q_plev', 

        'U10M'      :'u10m',
        'V10M'      :'v10m',
        'T2M'       :'t2m',
        'PS'        :'ps',

        'LWUTOA'    :'flut', 
        'SWUTOA'    :'fsut', 
        'SWDTOA'    :'fsdt', 

        'SST'       :'var34', # from IFS
        'SLHFLX'    :'lhflx',
        'SSHFLX'    :'shflx',

        'CLCT'      :'cldc',
        'CLCL'      :None,

        'TQC'       :'intql', 
        'TQI'       :'intqi', 
        'TQV'       :'intqv',
        'PP'        :'pr', 
    },
    'dep' : {
        'U'         :['ALT'],
        'V'         :['ALT'],
        'W'         :['ALT'],
        'T'         :['ALT'],
        'P'         :['ALT'],
        'QV'        :['ALT'],
        'QC'        :['ALT'],
    }
},

###############################################################################
################### REANALYSIS
###############################################################################
'ERA5_download' :{
    'vkeys' :{
        'HSURF'     :'z', 
        'FRLAND'    :'land_sea_mask', 

        'U'         :'u', 
        'V'         :'v', 
        'W'         :'w', 
        'T'         :'t', 
        'ALT'       :'z', 
        'QV'        :'specific_humidity', 
        'QC'        :'specific_cloud_liquid_water_content', 
        'QI'        :'specific_cloud_ice_water_content', 
        'QR'        :'specific_rain_water_content', 
        'QS'        :'specific_snow_water_content', 
        'CLDF'      :'fraction_of_cloud_cover', 

        'PS'        :'surface_pressure', 
        'PMSL'      :'mean_sea_level_pressure', 
        'CLCM'      :'mcc',
        'CLCH'      :'hcc',
        'CLCL'      :'lcc',
        'CLCT'      :'tcc',

        'U10M'      :'10m_u_component_of_wind', # for cds download
        'V10M'      :'10m_v_component_of_wind', # for cds download
        'T2M'       :'2m_temperature', 
        'TD2M'      :'2m_dewpoint_temperature', 

        'LWUTOA'    :'ttr', 
        'SWDTOA'    :'tisr', 
        'SWNDTOA'   :'top_net_solar_radiation', 
        'CSWNDTOA'  :'top_net_solar_radiation_clear_sky', 
        'SWNDSFC'   :'surface_net_solar_radiation', 
        'CSWNDSFC'  :'surface_net_solar_radiation_clear_sky', 
        'LWNDSFC'   :'surface_net_thermal_radiation', 

        'SLHFLX'    :'mean_surface_latent_heat_flux', # for cds download
        'SSHFLX'    :'mean_surface_sensible_heat_flux', # for cds download
        'SST'       :'sea_surface_temperature',
        'TSURF'     :'skin_temperature',

        'TQC'       :'tclw', 
        'TQI'       :'tciw', 
        'TQV'       :'tcwv', 
        'PP'        :'tp', 

    },
},
'ERA5' :{
    'vkeys' :{
        'HSURF'     :'z', 
        'FRLAND'    :'lsm', 

        'U'         :'u', 
        'V'         :'v', 
        'W'         :'w', 
        'T'         :'t', 
        'P'         :'P', # from preprocess_mod
        'ALT'       :'z', 
        'QV'        :'q', 
        'QC'        :'clwc', 
        'QI'        :'ciwc', 
        'QR'        :'crwc', 
        'QS'        :'cswc', 
        'CLDF'      :'cc', 

        'PS'        :'sp', 
        'PMSL'      :'', 
        'CLCM'      :'mcc',
        'CLCH'      :'hcc',
        'CLCL'      :'lcc',
        'CLCT'      :'tcc',

        'U10M'      :'u10',
        'V10M'      :'v10',
        'T2M'       :'t2m', 

        'LWUTOA'    :'ttr', 
        'SWDTOA'    :'tisr', 
        'SWNDTOA'   :'tsr', 
        'SWNDSFC'   :'ssr', 
        'LWNDSFC'   :'str', 

        'SLHFLX'    :'mslhf',
        'SSHFLX'    :'msshf',
        'SST'       :'sst',
        'TSURF'     :'skt',

        'TQC'       :'tclw', 
        'TQI'       :'tciw', 
        'TQV'       :'tcwv', 
        'PP'        :'tp', 

    },
    'vert_coord':   'plev',
    'dep' : {
        #'U'         :['ALT'],
        #'V'         :['ALT'],
        #'W'         :['ALT','P'],
        #'T'         :['ALT'],
        #'P'         :['ALT'],
        #'QV'        :['ALT'],
        #'QC'        :['ALT'],
        #'QI'        :['ALT'],
        #'QS'        :['ALT'],

        'U'         :['ALT','HSURF'],
        'V'         :['ALT','HSURF'],
        'W'         :['ALT','P','HSURF'],
        'T'         :['ALT','HSURF'],
        'P'         :['ALT','HSURF'],
        'QV'        :['ALT','HSURF'],
        'QC'        :['ALT','HSURF'],
        'QI'        :['ALT','HSURF'],
        'QS'        :['ALT','HSURF'],
        'CLDF'      :['ALT','HSURF'],
    }
},


'MPI-ESM1-2-HR' :{
    'vkeys' :{
        'FRLAND'    :'sftlf', 
        'HSURF'     :'orog', 
        'SWUTOA'    :'rsut', 
        'CSWUTOA'   :'rsutcs', 
        'SWUSFC'    :'rsus', 
        'SWDTOA'    :'rsdt', 
        'SWDSFC'    :'rsds', 

        'LWUTOA'    :'rlut', 
        'CLWUTOA'   :'rlutcs', 
        'LWUSFC'    :'rlus', 
        'LWDSFC'    :'rlds', 

        'SLHFLX'    :'hfls', 
        'SSHFLX'    :'hfss', 

        'PS'        :'ps', 
        'T2M'       :'tas', 
        'TSURF'     :'ts', 
        'U10M'      :'uas', 
        'V10M'      :'vas', 
        'PP'        :'pr', 

        'CLDF'      :'cl', 
        'U'         :'ua', 
        'V'         :'va', 
        #'WP'        :'wap', 
        'W'         :'wap', 
        'T'         :'ta', 
        'RH'        :'hur', 
        'QV'        :'hus', 
        'ALT'       :'zg', 
        'P'         :'P', # preprocessed in advance

        'CLCT'      :'clt', 

    },
    #'dep' : {
    #    'U10M'      :['SWDTOA'],
    #    'V10M'      :['SWDTOA'],
    #    'W'         :['SWDTOA'],
    #    'T'         :['SWDTOA'],
    #    'RH'        :['SWDTOA'],
    #},
    'vert_coord':   'plev',
    'dep' : {
        'W'         :['P'],
        #'CLDF'      :['ALT','HSURF','PS'],
        #'T'         :['ALT','HSURF','PS',],
        #'P'         :['ALT','HSURF','PS',],
        ##'WP'        :['ALT_Amon','HSURF','PS'],
        #'W'         :['ALT','P','HSURF','PS'],
        #'RH'        :['ALT','HSURF','PS'],
        #'QV'        :['ALT','HSURF','PS'],
        #'U'         :['ALT','HSURF','PS'],
        #'V'         :['ALT','HSURF','PS'],
    },
},


###############################################################################
################### OBSERVATIONS
###############################################################################

'CERES_EBAF' :{
    'vkeys' :{
        'FRLAND':       'FR_LAND', 
        'SWUTOA':       'toa_sw_all_mon', 
        'CSWUTOA':      'toa_sw_clr_c_mon', 
        'SWDTOA':       'solar_mon',
        'LWUTOA':       'toa_lw_all_mon', 
        'CLWUTOA':      'toa_lw_clr_c_mon', 
        'CLCT':         'cldarea_total_daynight_mon', 
    },
    'vert_coord':   None,
},

'CM_SAF_MSG_AQUA_TERRA' :{
    'vkeys' :{
        'FRLAND'    :'FR_LAND', 

        'SWUTOA':'Data1', 
        'SWDTOA'    :'ASOD_T', # from COSMO
        #'SWDTOA'    :'tisr', # from ERA5
        #'SWDTOA'    :'solar_mon', # from CERES EBAF
        'LWUTOA':'Data1', 
    },
    'vert_coord':   None,
},
'CM_SAF_MSG' :{
    'vkeys' :{
        'TQI':'iwp', 
        'CLCL'  :'cfc_low', 
        'CLCL2' :'cfc_low', 
    },
},
'CM_SAF_METEOSAT' :{
    'vkeys' :{
        'SWUTOA':'rsut', 
        'LWUTOA':'rlut', 
    },
},
'CM_SAF_HTOVS' :{
    'vkeys' :{
        'TQV':'HTW_TPWm', 
    },
},
'SUOMI_NPP_VIIRS' :{
    'vkeys' :{
        'CORREFL':'CORREFL', 
    },
},
'RADIO_SOUNDING' :{
    'vkeys' :{
        'INVHGT':'INVHGT', 
    },
},
'DARDAR_CLOUD' :{
    'vkeys' :{
        'CLDMASK'   :'CLDMASK', 
        'T'         :'T', 
    },
},
'GPM_IMERG' :{
    'vkeys' :{
        'HSURF'     :'HSURF', 
        'FRLAND'    :'FR_LAND', 
        'PP'        :'precipitationCal', 
        #'PP'        :'HQprecipitation',  # this one has gaps but higher resolution/quality/whatsoever
    },
    'vert_coord':   None,
},
'CMORPH' :{
    'vkeys' :{
        'HSURF'     :'HSURF', 
        'FRLAND'    :'FR_LAND', 
        'PP'        :'cmorph', 
    },
},

}



models_cmip6 = [
    'ACCESS-CM2',
    'ACCESS-ESM1-5',
    #'AWI-ESM-1-1-LR',   # no data for ssp585, ssp245
    'AWI-CM-1-1-MR',
    ###'BCC-CSM2-MR',   # no const file
    ###'BCC-ESM1',      # no data for ssp585, ssp245
    'CAMS-CSM1-0',
    'CanESM5',
    ###'CAS-ESM2-0',    # no const file
    'CESM2',            
    ###'CESM2-FV2',     # no data for ssp*
    'CESM2-WACCM',
    ###'CESM2-WACCM-FV2',# no data for ssp*
    ###'CIESM',         # data very incomplete (const in Ofx)
    'CMCC-CM2-SR5', 
    'CMCC-ESM2',
    'CNRM-CM6-1',
    'CNRM-CM6-1-HR',
    'CNRM-ESM2-1',
    'E3SM-1-1',         # no data for ssp245
    'EC-Earth3',
    ###'EC-Earth3-CC',  # no const file
    'EC-Earth3-Veg',
    ###'EC-Earth3-Veg-LR',# very similar to EC-Earth3
    'FGOALS-f3-L',
    'FGOALS-g3',
    ###'FIO-ESM-2-0',   # no const file
    'GFDL-CM4',
    'GFDL-ESM4',
    'GISS-E2-1-G',
    ###'GISS-E2-1-H',   # no data for ssp245, ssp585 (but for others)
    'HadGEM3-GC31-LL',
    ###'HadGEM3-GC31-MM',# no data for ssp245
    ###'IITM-ESM',      # no  const file
    'INM-CM4-8',    
    'INM-CM5-0',
    'IPSL-CM6A-LR',
    ###'KACE-1-0-G',    # no const file
    ###'KIOST-ESM',     # no const file
    ###'MCM-UA-1-0',    # no const file
    'MIROC6',
    'MIROC-ES2L',
    'MPI-ESM1-2-HR',
    'MPI-ESM1-2-LR',
    'MRI-ESM2-0',
    ####'NESM3',        # no const file
    'NorESM2-LM',       
    'NorESM2-MM',
    'TaiESM1',
    'UKESM1-0-LL',
]
for model in models_cmip6:
    nlm[model] = copy.deepcopy(nlm['MPI-ESM1-2-HR'])
nlm['MPI-ESM1-2-HR_delta'] = copy.deepcopy(nlm['MPI-ESM1-2-HR'])



models_cmip6_cldf = [
    'ACCESS-CM2',
    'ACCESS-ESM1-5',
    #'AWI-ESM-1-1-LR',   # no data for ssp585, ssp245
    # no data 'AWI-CM-1-1-MR',
    ####'BCC-CSM2-MR',   # no const file
    ####'BCC-ESM1',      # no data for ssp585, ssp245
    'CAMS-CSM1-0',
    'CanESM5',
    ####'CAS-ESM2-0',    # no const file
    'CESM2',            
    ####'CESM2-FV2',     # no data for ssp*
    'CESM2-WACCM',
    ####'CESM2-WACCM-FV2',# no data for ssp*
    ####'CIESM',         # data very incomplete (const in Ofx)
    'CMCC-CM2-SR5', 
    'CMCC-ESM2',
    'CNRM-CM6-1',
    #'CNRM-CM6-1-HR',     # no cloud data for ssp585
    'CNRM-ESM2-1',
    'E3SM-1-1',         # no data for ssp245
    #'EC-Earth3',         # no cloud data
    #'EC-Earth3-CC',     # no cloud data
    #'EC-Earth3-Veg',   # no cloud data
    ####'EC-Earth3-Veg-LR',# very similar to EC-Earth3
    'FGOALS-f3-L',
    'FGOALS-g3',
    ####'FIO-ESM-2-0',   # no const file
    'GFDL-CM4',
    'GFDL-ESM4',
    'GISS-E2-1-G',
    ####'GISS-E2-1-H',   # no data for ssp245, ssp585 (but for others)
    'HadGEM3-GC31-LL',
    ####'HadGEM3-GC31-MM',# no data for ssp245
    ####'IITM-ESM',      # no  const file
    #'INM-CM4-8',       # no cloud data
    #'INM-CM5-0',       # no cloud data
    # TODO: difficulty with vertical coordinate: 'IPSL-CM6A-LR',
    ####'KACE-1-0-G',    # no const file
    ####'KIOST-ESM',     # no const file
    ####'MCM-UA-1-0',    # no const file
    'MIROC6',
    'MIROC-ES2L',
    'MPI-ESM1-2-LR',
    'MRI-ESM2-0',
    #####'NESM3',        # no const file
    'NorESM2-LM',       
    'NorESM2-MM',
    'TaiESM1',
    'UKESM1-0-LL',


    'MPI-ESM1-2-HR',
]


models_cmip6_pgw = [
    'CESM2-WACCM',
    'GFDL-CM4',
    'IPSL-CM6A-LR',
    'MIROC6',
    'MPI-ESM1-2-HR',
    'MPI-ESM1-2-LR',
    'MRI-ESM2-0',
    'NorESM2-LM',       
    'NorESM2-MM',
    'TaiESM1',
]
