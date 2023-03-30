#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     namelist of model variables
author			Christoph Heim
date created    09.09.2019
date changed    15.03.2021
usage           use in another script
"""
###############################################################################
import os
###############################################################################

dimx = 'x'
dimy = 'y'
dimz = 'z'
dimt = 't'
# diurnal
dimd = 'd'

nlv = {

###############################################################################
## COORDINATE VARIABLES
'COORD_ALT' :{
    'lo_name'   :'height',
    'label'     :'z',
    'units'      :'$m$',
    'dims'      :[dimz],
},
'COORD_RELALT' :{
    'lo_name'   :'height relative to inversion height',
    'label'     :'z/z$_{i}$',
    'units'      :'',
    'dims'      :[dimz],
},
'COORD_LON' :{
    'lo_name'   :'longitude',
    'label'     :'longitude',
    #'units'      :'$°$ East',
    'units'      :'',
    'dims'      :[dimx],
},
'COORD_LAT' :{
    'lo_name'   :'latitude',
    'label'     :'latitude',
    #'units'      :'$°$ East',
    'units'      :'',
    'dims'      :[dimy],
},
'COORD_YEAR' :{
    'lo_name'   :'year',
    'label'     :'year',
    'units'      :'',
    'dims'      :[dimt],
},
'COORD_DATETIME' :{
    'lo_name'   :'date and time',
    'label'     :'date',
    'units'      :'',
    'dims'      :[dimd],
},
'COORD_DIURN' :{
    'lo_name'   :'day time',
    'label'     :'time',
    'units'      :'UTC',
    'dims'      :[dimd],
},

###############################################################################
## NORMAL VARIABLES
'HSURF' :{
    'lo_name'   :'surface elevation',
    'label'     :'elevation',
    'units'      :'$m$',
    'dims'      :[dimx,dimy],
},


'U' :{
    'lo_name'   :'x wind',
    'label'     :'zonal wind speed',
    'units'      :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'UI' :{
    'lo_name'   :'x wind at inversion',
    'label'     :'zonal wind speed',
    'units'      :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimt],
},
'V' :{
    'lo_name'   :'y wind',
    'label'     :'meridional wind speed',
    'units'      :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'VI' :{
    'lo_name'   :'y wind at inversion',
    'label'     :'meridional wind speed',
    'units'      :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimt],
},
'UV' :{
    'lo_name'   :'horizontal wind speed',
    'label'     :'horizontal wind',
    'units'      :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'UVFLXDIV' :{
    'lo_name'   :'divergence of the horizontal mass flux',
    'label'     :r"$\nabla _{h} (v_{h} \rho)$",
    'units'      :'$kg$ $m^{-3}$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'UVFLXDIVNORMI' :{
    'lo_name'   :'divergence of the horizontal mass flux',
    'label'     :r"$\nabla _{h} (v_{h} \rho)$",
    'units'      :'$kg$ $m^{-3}$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'W' :{
    'lo_name'   :'vertical wind speed',
    'label'     :'vertical wind',
    'units'      :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'WI' :{
    'lo_name'   :'vertical wind speed at inversion',
    'label'     :'vertical wind',
    'units'      :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimt],
},
'WMEAN' :{
    'lo_name'   :'mean vertical wind speed ',
    'label'     :r"$\overline{w}$",
    'units'      :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz],
},
'WTURB' :{
    'lo_name'   :'turbulent vertical velocity',
    'label'     :r"$\sigma_{w}$",
    'units'      :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'WTURBNORMI' :{
    'lo_name'   :'turbulent vertical velocity',
    'label'     :r"$\sigma_{w}$",
    'units'      :'$m$ $s^{-1}$',
    #'units'      :'$s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'WTURBNORMISCI' :{
    'lo_name'   :'turbulent vertical velocity',
    'label'     :r"$\sigma_{w/z_{i}}$",
    #'units'      :'$m$ $s^{-1}$',
    'units'      :'$h^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'WFLX' :{
    'lo_name'   :'vertical mass flux',
    'label'     :'vertical mass flux',
    'units'      :'$kg$ $m^{-2}$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'WFLXI' :{
    'lo_name'   :'vertical mass flux into the MBL',
    'label'     :'$F^{z}_{MBL}$',
    'units'      :'$kg$ $m^{-2}$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimt],
},
'ENTR' :{
    'lo_name'   :'entrainment velocity',
    'label'     :'$entrainment$',
    'units'      :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimt],
},
'ENTRH' :{
    'lo_name'   :'entrainment velocity diagnosed horizontally',
    'label'     :'$entrainment$',
    'units'      :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimt],
},
'ENTRV' :{
    'lo_name'   :'entrainment velocity diagnosed vertically',
    'label'     :'$entrainment$',
    'units'      :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimt],
},
'AW' :{
    'lo_name'   :'velocity of vertical circulations',
    'label'     :'|w|',
    'units'      :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'AWD' :{
    'lo_name'   :'downward velocity of vertical circulations',
    'label'     :'w up',
    'units'      :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'AWU' :{
    'lo_name'   :'upward velocity of vertical circulations',
    'label'     :'w down',
    'units'      :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'KEW' :{
    'lo_name'   :'grid-scale vertical kinetic energy',
    'label'     :'grid-scale vertical kinetic energy',
    'units'      :'$J$ $m^{-3}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'T' :{
    'lo_name'   :'temperature',
    'label'     :'temperature',
    'units'      :'$K$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'TV' :{
    'lo_name'   :'virtual temperature',
    'label'     :'virtual temperature',
    'units'      :'$K$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'POTT' :{
    'lo_name'   :'potential temperature',
    'label'     :'potential temperature',
    'units'      :'$K$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'POTTV' :{
    'lo_name'   :'virtual potential temperature',
    'label'     :r'$\theta_v$',
    'units'      :'$K$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'POTTVFT' :{
    'lo_name'   :'virtual potential temperature in free troposphere',
    'label'     :r'$\theta_v$ at 3km',
    'units'     :'$K$',
    'dims'      :[dimx,dimy,dimt],
},
'POTTBL' :{
    'lo_name'   :'potential temperature in MBL',
    'label'     :r'$\theta$ at 300m',
    'units'     :'$K$',
    'dims'      :[dimx,dimy,dimt],
},
'POTTFT' :{
    'lo_name'   :'potential temperature in free troposphere',
    'label'     :r'$\theta$ at 3km',
    'units'     :'$K$',
    'dims'      :[dimx,dimy,dimt],
},
'POTTMBLI' :{
    'lo_name'   :'mean potential temperature in MBL',
    'label'     :r"$\theta |_{MBL}$",
    'units'      :'$K$',
    'dims'      :[dimx,dimy,dimt],
},
'P' :{
    'lo_name'   :'pressure',
    'label'     :'pressure',
    'units'      :'$Pa$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'ALT' :{
    'lo_name'   :'altitude',
    'label'     :'altitude',
    'units'      :'$m$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'RHO' :{
    'lo_name'   :'density',
    'label'     :'density',
    'units'      :'$kg$ $m^{-3}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'RHOI' :{
    'lo_name'   :'density at inversion',
    'label'     :'density',
    'units'      :'$kg$ $m^{-3}$',
    'dims'      :[dimx,dimy,dimt],
},
'QV' :{
    'lo_name'   :'specific water vapor content',
    'label'     :'$q_v$',
    'units'      :'$kg$ $kg^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'QVFT' :{
    'lo_name'   :'specific humidity in free troposphere',
    'label'     :'specific humidity at 3km',
    'units'      :'$kg$ $kg^{-1}$',
    'dims'      :[dimx,dimy,dimt],
},
'QVVDIV' :{
    'lo_name'   :'vertical divergence of specific water vapor content',
    'label'     :r"$w\frac{\partial q_{v}}{\partial z}$",
    'units'      :'$kg$ $kg^{-1}$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'QVHDIV' :{
    'lo_name'   :'horizontal divergence of specific water vapor content',
    'label'     :r"$v_{h}\nabla _{h} \q_{v}$",
    'units'      :'$kg$ $kg^{-1}$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'QC' :{
    'lo_name'   :'specific cloud water content',
    'label'     :'$q_c$',
    'units'      :'$kg$ $kg^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'QVFLXZ' :{
    'lo_name'   :'vertical moisture flux',
    'label'     :'qv flux',
    'units'      :'$kg$ $m^{-2}$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'QI' :{
    'lo_name'   :'specific cloud ice content',
    'label'     :'$q_i$',
    'units'      :'$kg$ $kg^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'DIABH' :{
    'lo_name'   :'diabatic heating',
    'label'     :'diabatic heating',
    'units'      :'$K$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'UNORMI' :{
    'lo_name'   :'x wind',
    'label'     :'zonal wind speed',
    'units'      :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'VNORMI' :{
    'lo_name'   :'y wind',
    'label'     :'meridional wind speed',
    'units'      :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'UVNORMI' :{
    'lo_name'   :'horizontal wind speed',
    'label'     :'horizontal wind',
    'units'      :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'WNORMI' :{
    'lo_name'   :'vertical wind speed',
    'label'     :'vertical wind',
    'units'     :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'TNORMI' :{
    'lo_name'   :'temperature',
    'label'     :'temperature',
    'units'     :'$K$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'POTTNORMI' :{
    'lo_name'   :'potential temperature',
    'label'     :'potential temperature',
    'units'     :'$K$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'PNORMI' :{
    'lo_name'   :'pressure',
    'label'     :'pressure',
    'units'     :'$Pa$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'QVNORMI' :{
    'lo_name'   :'specific water vapor content',
    'label'     :'$q_v$',
    'units'     :'$kg$ $kg^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'QCNORMI' :{
    'lo_name'   :'specific cloud water content',
    'label'     :'$q_c$',
    'units'     :'$kg$ $kg^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'DIABHNORMI' :{
    'lo_name'   :'diabatic heating',
    'label'     :'diabatic heating',
    'units'      :'$K$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'POTTVDIV' :{
    'lo_name'   :'vertical divergence of potential temperature',
    'label'     :r"$w\frac{\partial \theta}{\partial z}$",
    'units'      :'$K$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'POTTHDIV' :{
    'lo_name'   :'horizontal divergence of potential temperature',
    'label'     :r"$v_{h}\nabla _{h} \theta$",
    'units'      :'$K$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'POTTVDIVNORMI' :{
    'lo_name'   :'vertical convergence of potential temperature',
    'label'     :r"$w\frac{\partial \theta}{\partial z}$",
    'units'     :'$K$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'POTTHDIVNORMI' :{
    'lo_name'   :'horziontal convergence of potential temperature',
    'label'     :r"$v_{h}\nabla _{h} \theta$",
    'units'     :'$K$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'POTTHDIVMEAN' :{
    'lo_name'   :'horizontal mean flow divergence of potential temperature',
    'label'     :r"$\overline{v_{h}}$ $\nabla _{h} \overline{\theta}$",
    'units'      :'$K$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz],
},
'POTTHDIVMEANNORMI' :{
    'lo_name'   :'horizontal mean flow divergence of potential temperature',
    'label'     :r"$\overline{v_{h}}$ $\nabla _{h} \overline{\theta}$",
    'units'      :'$K$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz],
},
'POTTHDIVMBLI' :{
    'lo_name'   :'mean horizontal divergence of potential temperature in MBL',
    'label'     :r"$v_{h}\nabla _{h} \theta |_{MBL}$",
    'units'      :'$K$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimt],
},
'POTTVDIVMEAN' :{
    'lo_name'   :'vertical mean flow divergence of potential temperature',
    'label'     :r"$\overline{w}$ $\frac{\partial \overline{\theta}}{\partial z}$",
    'units'      :'$K$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz],
},
'POTTVDIVMEANNORMI' :{
    'lo_name'   :'vertical mean flow divergence of potential temperature',
    'label'     :r"$\overline{w}$ $\frac{\partial \overline{\theta}}{\partial z}$",
    'units'      :'$K$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz],
},
'POTTDIVMEAN' :{
    'lo_name'   :'mean flow divergence of potential temperature',
    'label'     :r"$\overline{v}$ $\nabla \overline{\theta}$",
    'units'      :'$K$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz],
},
'POTTDIVMEANNORMI' :{
    'lo_name'   :'mean flow divergence of potential temperature',
    'label'     :r"$\overline{v}$ $\nabla \overline{\theta}$",
    'units'      :'$K$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz],
},
'POTTHDIVTURB' :{
    'lo_name'   :'horiz. flux divergence of potential temperature',
    'label'     :r"$\overline{v_{h}'\nabla _{h} \theta'}$",
    'units'      :'$K$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'POTTHDIVTURBNORMI' :{
    'lo_name'   :'horiz. flux divergence of potential temperature',
    'label'     :r"$\overline{v_{h}'\nabla _{h} \theta'}$",
    'units'      :'$K$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'POTTVDIVTURB' :{
    'lo_name'   :'vert. flux divergence of potential temperature',
    'label'     :r"$\overline{w'\frac{\partial \theta'}{\partial z}}$",
    'units'      :'$K$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'POTTVDIVTURBNORMI' :{
    'lo_name'   :'vert. flux divergence of potential temperature',
    'label'     :r"$\overline{w'\frac{\partial \theta'}{\partial z}}$",
    'units'      :'$K$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'POTTDIVTURB' :{
    'lo_name'   :'flux divergence of potential temperature',
    'label'     :r"$\overline{v'\nabla \theta'}$",
    'units'      :'$K$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'POTTDIVTURBNORMI' :{
    'lo_name'   :'flux divergence of potential temperature',
    'label'     :r"$\overline{v'\nabla \theta'}$",
    'units'      :'$K$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'POTTVFLXWPOS' :{
    'lo_name'   :'vertical flux of potential temperature in updrafts',
    'label'     :r"$w_{+} \rho \theta$",
    'units'      :'$K$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'POTTVFLXWPOS' :{
    'lo_name'   :'vertical flux of potential temperature in downdrafts',
    'label'     :r"$w_{-} \rho \theta$",
    'units'      :'$K$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'DIABHMINV' :{
    'lo_name'   :'mean MBL top diabatic heating',
    'label'     :'mean MBL top diabatic heating',
    'units'      :'$K$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimt],
},
'TKE' :{
    'lo_name'   :'specific turbulent kinetic energy',
    'label'     :'TKE',
    'units'      :'$m^{2}$ $s^{-2}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'TKEMBLI' :{
    'lo_name'   :'mean specific turbulent kinetic energy within BL',
    'label'     :'TKE',
    'units'      :'$m^{2}$ $s^{-2}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'FQVZ' :{
    'lo_name'   :'vertical water vapor flux',
    'label'     :'vapor flux',
    'units'      :'$kg$ $m^{-2}$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'WMBLI' :{
    'lo_name'   :'mean w BL',
    'label'     :'mean vertical wind below BL inversion',
    'units'      :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimt],
},
'WFLXNORMI' :{
    'lo_name'   :'resolved vertical mass flux',
    'label'     :'vertical mass flux',
    'units'      :'$kg$ $m^{-2}$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'AWNORMI' :{
    'lo_name'   :'velocity of vertical circulations',
    'label'     :'|w|',
    'units'      :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'AWDNORMI' :{
    'lo_name'   :'downward velocity of vertical circulations',
    'label'     :'w up',
    'units'      :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'AWUNORMI' :{
    'lo_name'   :'upward velocity of vertical circulations',
    'label'     :'w down',
    'units'      :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'KEWNORMI' :{
    'lo_name'   :'grid-scale vertical kinetic energy',
    'label'     :'grid-scale vertical kinetic energy',
    'units'      :'$J$ $m^{-3}$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'AWMBLI' :{
    'lo_name'   :'mean velocity of vertical circulations',
    'label'     :'|w|$_{MBL}$',
    'units'      :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimt],
},
'KEWMBLI' :{
    'lo_name'   :'mean vertical resolved kinetic energy below BL inversion',
    'label'     :'grid-scale vertical kinetic energy',
    'units'      :'$J$ $m^{-3}$',
    'dims'      :[dimx,dimy,dimt],
},
'SUBS' :{
    'lo_name'   :'subsidence strength',
    'label'     :'subsidence strength',
    'units'      :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimt],
},


'INVHGT' :{
    'lo_name'   :'height of maximum inversion strength',
    'label'     :'inversion height',
    'units'      :'$m$',
    'dims'      :[dimx,dimy,dimt],
},
'LTS' :{
    #'lo_name'   :'lower tropospheric stability',
    'lo_name'   :'lower tropospheric lapse rate',
    'label'     :'LTS',
    #'units'      :'$K$',
    'units'      :'$K/100m$',
    'dims'      :[dimx,dimy,dimt],
},
'LCL' :{
    'lo_name'   :'lifting condensation level',
    'label'     :'LCL',
    'units'     :'$m$',
    'dims'      :[dimx,dimy,dimt],
},
'DCLDBASELCL' :{
    'lo_name'   :'difference between cloud base and lifting condensation level',
    'label'     :'cloud base - LCL',
    'units'     :'$m$',
    'dims'      :[dimx,dimy,dimt],
},
'DCLDTOPINVHGT' :{
    'lo_name'   :'difference between cloud top and inversion height',
    'label'     :'cloud top - inversion height',
    'units'     :'$m$',
    'dims'      :[dimx,dimy,dimt],
},
'DINVHGTLCL' :{
    'lo_name'   :'difference between inversion height and lifting condensation level',
    'label'     :'inversion height - LCL',
    'units'     :'$m$',
    'dims'      :[dimx,dimy,dimt],
},
'PVAP' :{
    'lo_name'   :'vapor pressure',
    'label'     :'$e$',
    'units'     :'$Pa$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'PVAPSATL' :{
    'lo_name'   :'saturation vapor pressure with respect to liquid water',
    'label'     :'$e_{s,l}$',
    'units'     :'$Pa$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'RHL' :{
    'lo_name'   :'relative humidity with respect to liquid water',
    'label'     :'$RH_{l}$',
    'units'     :'',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'RHLNORMI' :{
    'lo_name'   :'relative humidity with respect to liquid water',
    'label'     :'$RH_{l}$',
    'units'     :'',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'NOINVF' :{
    'lo_name'   :'frequency without inversion',
    'label'     :'occurrence of no inversion',
    'units'     :'',
    'dims'      :[dimx,dimy,dimt],
},
'INVSTRA' :{
    'lo_name'   :'average inversion strength',
    'label'     :'inversion strength',
    'units'     :'$K$ $m^{-1}$',
    'dims'      :[dimx,dimy,dimt],
},
'INVSTR' :{
    'lo_name'   :'inversion strength',
    'label'     :'inversion strength',
    'units'     :'$K$',
    'dims'      :[dimx,dimy,dimt],
},
'INVSTRV' :{
    'lo_name'   :'inversion strength using virtual potential temperature',
    'label'     :'inversion strength',
    'units'     :'$K$',
    'dims'      :[dimx,dimy,dimt],
},
'CLDHGT' :{
    'lo_name'   :'height of maximum cloud water content',
    'label'     :'cloud height',
    'units'     :'$m$',
    'dims'      :[dimx,dimy,dimt],
},
'LCLDMASK' :{
    'lo_name'   :'low cloud mask',
    'label'     :'low cloud mask',
    'units'     :'$$',
    'dims'      :[dimx,dimy,dimz,dimt],
},
'LCLDBASE' :{
    'lo_name'   :'height of low cloud base',
    'label'     :'cloud base height',
    'units'     :'$m$',
    'dims'      :[dimx,dimy,dimt],
},
'LCLDBASENORMI' :{
    'lo_name'   :'height of low cloud base normalised by inversion height',
    'label'     :'relative cloud base height',
    'units'     :'',
    'dims'      :[dimx,dimy,dimt],
},
'LCLDTOP' :{
    'lo_name'   :'height of low cloud top',
    'label'     :'cloud top height',
    'units'     :'$m$',
    'dims'      :[dimx,dimy,dimt],
},
'LCLDDEPTH' :{
    'lo_name'   :'thickness of low cloud top',
    'label'     :'cloud depth',
    'units'     :'$m$',
    'dims'      :[dimx,dimy,dimt],
},


'LWUTOA' :{
    'lo_name'   :'outgoing longwave flux at TOA',
    'label'     :'OLR',
    'units'     :'$W$ $m^{-2}$',
    'dims'      :[dimx,dimy,dimt],
},
'SWDSFC' :{
    'lo_name'   :'downward SW at surface',
    'label'     :'Flux',
    'units'     :'$W$ $m^{-2}$',
    'dims'      :[dimx,dimy,dimt],
},
'SWUTOA' :{
    'lo_name'   :'reflected SW at TOA',
    'label'     :'OSR',
    'units'     :'$W$ $m^{-2}$',
    'dims'      :[dimx,dimy,dimt],
},
'ALBEDO' :{
    'lo_name'   :'albedo SW',
    'label'     :'albedo',
    'units'     :'',
    'dims'      :[dimx,dimy,dimt],
},
'SWDTOA' :{
    'lo_name'   :'downward SW at TOA',
    'label'     :'flux',
    'units'     :'$W$ $m^{-2}$',
    'dims'      :[dimx,dimy,dimt],
},
'SWNDTOA' :{
    'lo_name'   :'net downward SW at TOA',
    'label'     :'flux',
    'units'     :'$W$ $m^{-2}$',
    'dims'      :[dimx,dimy,dimt],
},


'U10M' :{
    'lo_name'   :'U wind at 10m',
    'label'     :'u wind',
    'units'     :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimt],
},
'U10M_W' :{
    'lo_name'   :'U wind at 10m at western domain boundary',
    'label'     :'u wind',
    'units'     :'$m$ $s^{-1}$',
    'dims'      :[dimy,dimt],
},
'U10M_E' :{
    'lo_name'   :'U wind at 10m at eastern domain boundary',
    'label'     :'u wind',
    'units'     :'$m$ $s^{-1}$',
    'dims'      :[dimy,dimt],
},
'V10M_S' :{
    'lo_name'   :'V wind at 10m at southern domain boundary',
    'label'     :'v wind',
    'units'     :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimt],
},
'V10M_N' :{
    'lo_name'   :'V wind at 10m at northern domain boundary',
    'label'     :'v wind',
    'units'     :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimt],
},
'V10M' :{
    'lo_name'   :'V wind at 10m',
    'label'     :'v wind',
    'units'      :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimt],
},
'PS' :{
    'lo_name'   :'surface pressure',
    'label'     :'pressure',
    'units'      :'$hPa$',
    'dims'      :[dimx,dimy,dimt],
},
'UV10M' :{
    'lo_name'   :'wind speed at 10m',
    'label'     :'wind',
    'units'      :'$m$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimt],
},
'SLHFLX' :{
    'lo_name'   :'surface latent heat flux',
    'label'     :'latent heat flux',
    'units'      :'$W$ $m^{-2}$',
    'dims'      :[dimx,dimy,dimt],
},
'SSHFLX' :{
    'lo_name'   :'surface sensible heat flux',
    'label'     :'sensible heat flux',
    'units'      :'$W$ $m^{-2}$',
    'dims'      :[dimx,dimy,dimt],
},

'TQC' :{
    'lo_name'   :'liquid water path',
    'label'     :'LWP',
    'units'      :'$kg$ $m^{-2}$',
    'dims'      :[dimx,dimy,dimt],
},
'CORREFL' :{
    #'lo_name'   :'corrected reflectance',
    #'label'     :'reflectance',
    'lo_name'   :'liquid water path',
    'label'     :'liquid water path',
    'units'      :'$kg$ $m^{-2}$',
    'dims'      :[dimx,dimy,dimt],
},
'TQI' :{
    'lo_name'   :'ice water path',
    'label'     :'ice water path',
    'units'      :'$kg$ $m^{-2}$',
    'dims'      :[dimx,dimy,dimt],
},
'TQV' :{
    'lo_name'   :'water vapor path',
    'label'     :'water vapor path',
    'units'      :'$kg$ $m^{-2}$',
    'dims'      :[dimx,dimy,dimt],
},
'TQVFT' :{
    'lo_name'   :'water vapor path between 3km an 6km',
    'label'     :'water vapor path (3-6km)',
    'units'      :'$kg$ $m^{-2}$',
    'dims'      :[dimx,dimy,dimt],
},
'QVFLXZI' :{
    'lo_name'   :'qv-flux accross inversion',
    'label'     :'',
    'units'      :'$kg$ $m^{-2}$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimt],
},
'QVFLXZCB' :{
    'lo_name'   :'qv-flux at cloud base',
    'label'     :'',
    'units'      :'$kg$ $m^{-2}$ $s^{-1}$',
    'dims'      :[dimx,dimy,dimt],
},

'CLCL' :{
    'lo_name'   :'low cloud fraction',
    'label'     :'low cloud fraction',
    'units'      :'',
    'dims'      :[dimx,dimy,dimt],
},
'CLCL2' :{
    'lo_name'   :'low cloud fraction',
    'label'     :'low cloud fraction',
    'units'      :'',
    'dims'      :[dimx,dimy,dimt],
},
'CLCM' :{
    'lo_name'   :'mid cloud fraction',
    'label'     :'mid cloud fraction',
    'units'      :'',
    'dims'      :[dimx,dimy,dimt],
},
'CLCH' :{
    'lo_name'   :'high cloud fraction',
    'label'     :'high cloud fraction',
    'units'      :'',
    'dims'      :[dimx,dimy,dimt],
},
'CLCT' :{
    'lo_name'   :'total cloud fraction',
    'label'     :'fraction',
    'units'      :'',
    'dims'      :[dimx,dimy,dimt],
},
'PP' :{
    'lo_name'   :'precipitation',
    'label'     :'precipitation',
    'units'      :'$mm$ $h^{-1}$',
    'dims'      :[dimx,dimy,dimt],
},
'PPGRID' :{
    'lo_name'   :'grid-scale precipitation',
    'label'     :'precipitation',
    'units'      :'$mm$ $h^{-1}$',
    'dims'      :[dimx,dimy,dimt],
},
'PPCONV' :{
    'lo_name'   :'convective precipitation',
    'label'     :'precipitation',
    'units'      :'$mm$ $h^{-1}$',
    'dims'      :[dimx,dimy,dimt],
},
#'PPANVI' :{
#    'lo_name'   :'anvil precipitation',
#    'label'     :'precipitation',
#    'units'      :'$mm$ $h^{-1}$',
#    'dims'      :[dimx,dimy,dimt],
#},
'TSURF' :{
    'lo_name'   :'surface temperature',
    'label'     :'surface T',
    'units'      :'$K$',
    'dims'      :[dimx,dimy,dimt],
},
'SST' :{
    'lo_name'   :'sea surface temperature',
    'label'     :'SST',
    'units'      :'$K$',
    'dims'      :[dimx,dimy,dimt],
},



'bulk_tend_edge_POTT_below_S' :{
    'lo_name'   :'bulk domain MBL temperature tendency due to advection from South',
    'label'     :'South flux pot. temp. tendency',
    'units'      :'$K$ $s^{-1}$',
    'dims'      :[dimt],
},
'bulk_tend_edge_POTT_below_E' :{
    'lo_name'   :'bulk domain MBL temperature tendency due to advection from East',
    'label'     :'East flux pot. temp. tendency',
    'units'      :'$K$ $s^{-1}$',
    'dims'      :[dimt],
},
'bulk_tend_edge_POTT_below_N' :{
    'lo_name'   :'bulk domain MBL temperature tendency due to advection from North',
    'label'     :'North flux pot. temp. tendency',
    'units'      :'$K$ $s^{-1}$',
    'dims'      :[dimt],
},
'bulk_tend_edge_POTT_below_W' :{
    'lo_name'   :'bulk domain MBL temperature tendency due to advection from West',
    'label'     :'West flux pot. temp. tendency',
    'units'      :'$K$ $s^{-1}$',
    'dims'      :[dimt],
},







# Master thesis stuff
'WVP_0_10' : {
    'label'         :'Water Vapor Path',
    'units'          :'[kg m-2]',
},
'WVP_0_4' : {
    'label'         :'Water Vapor Path',
    'units'          :'[kg m-2]',
},
'WVP_0_2' : {
    'label'         :'Water Vapor Path',
    'units'          :'[kg m-2]',
},
'WVP_2_4' : {
    'label'         :'Water Vapor Path',
    'units'          :'[kg m-2]',
},
'WVP_2_10' : {
    'label'         :'Water Vapor Path',
    'units'          :'[kg m-2]',
},
'WVP_4_10' : {
    'label'         :'Water Vapor Path',
    'units'          :'[kg m-2]',
},
}





def add_var_attributes(var, var_name):
    var.attrs['units'] = nlv[var_name]['units']
    var.attrs['standard_name'] = nlv[var_name]['label']
    var.attrs['long_name'] = nlv[var_name]['lo_name']
    var.name = var_name
    return(var)

