#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    geographic domains to use in other scripts
author			Christoph Heim
date created    20.04.2019
date changed    28.02.2022
usage			import in another script
"""
###############################################################################
import numpy as np



###############################################################################
# MODEL DOMAINS
###############################################################################
###### 12km
dom_native = {
    'key':'dom_native',
    'label':'Native model domain',
    'lon':slice(None, None),
    'lat':slice(None, None),
    'nlon':None,
    'nlat':None,}


###### 12km
lon0 = -33.04
lat0 = -30.07
nlon = 510
nlat = 456
dom_DYA_12km = {
    'key':'dom_DYA_12km',
    'label':'COSMO 12',
    'lon':slice(lon0, lon0 + 0.11*(nlon-1)),
    'lat':slice(lat0, lat0 + 0.11*(nlat-1)),
    'nlon':nlon,
    'nlat':nlat,}

###### 4km
lon0 = -32
lat0 = -29
nlon = 1350
nlat = 1200
dom_DYA_4km = {
    'key':'dom_DYA_4km',
    #'label':'COSMO 4.4 (DYA)',
    'label':'COSMO 4.4',
    'lon':slice(lon0, lon0 + 0.04*(nlon-1)),
    'lat':slice(lat0, lat0 + 0.04*(nlat-1)),
    'nlon':nlon,
    'nlat':nlat,
    'dticks':20,}
#print(dom_DYA_4km)
#quit()


lon0 = -40
lat0 = -29
nlon = 1600
nlat = 1440
dom_SA_4km = {
    'key':'dom_SA_4km',
    'label':'COSMO 4.4 SA',
    'lon':slice(lon0, lon0 + 0.04*(nlon-1)),
    'lat':slice(lat0, lat0 + 0.04*(nlat-1)),
    'nlon':nlon,
    'nlat':nlat,
    'dticks':20,}
#print(dom_SA_4km)
#quit()

lon0 = -27
lat0 = -29
nlon = 1200
nlat = 700
dom_SSA_4km = {
    'key':'dom_SSA_4km',
    'label':'COSMO 4.4 SSA',
    'lon':slice(lon0, lon0 + 0.04*(nlon-1)),
    'lat':slice(lat0, lat0 + 0.04*(nlat-1)),
    'nlon':nlon,
    'nlat':nlat,
    'dticks':20,}


###### 3km
lon0 = -25.02
lat0 = -25.00
nlon = 1450
nlat = 850
dom_SSA_3km = {
    'key':'dom_SSA_3km',
    'label':'COSMO 3.3',
    'lon':slice(lon0, lon0 + 0.03*(nlon-1)),
    'lat':slice(lat0, lat0 + 0.03*(nlat-1)),
    'nlon':nlon,
    'nlat':nlat,
    'dticks':20,}
#print(dom_SSA_3km)
#quit()

lon0 = -32.01
lat0 = -29.02
nlon = 1800
nlat = 1600
dom_DYA_3km = {
    'key':'dom_DYA_3km',
    'label':'COSMO 3.3',
    'lon':slice(lon0, lon0 + 0.03*(nlon-1)),
    'lat':slice(lat0, lat0 + 0.03*(nlat-1)),
    'nlon':nlon,
    'nlat':nlat,
    'dticks':20,}
#print(dom_SA_3km_test)
#quit()

#lon0 = -52.02
#lat0 = -34.00
#nlon = 2614
#nlat = 1900
lon0 = -50.04
lat0 = -36.10
nlon = 2550
nlat = 1950
dom_SA_3km = {
    'key':'dom_SA_3km',
    'label':'extended',
    'lon':slice(lon0, lon0 + 0.03*(nlon-1)),
    'lat':slice(lat0, lat0 + 0.03*(nlat-1)),
    'nlon':nlon,
    'nlat':nlat,
    'dticks':20,}
#print(dom_SA_3km)
#quit()

lon0 = -54.54
lat0 = -36.10
nlon = 2750
nlat = 2000
dom_SA_3km_large2 = {
    'key':'dom_SA_3km_large2',
    'label':'large 2',
    'lon':slice(lon0, lon0 + 0.03*(nlon-1)),
    'lat':slice(lat0, lat0 + 0.03*(nlat-1)),
    'nlon':nlon,
    'nlat':nlat,
    'dticks':20,}


lon0 = -54.54
lat0 = -37.45
nlon = 2750
nlat = 2065
dom_SA_3km_large3 = {
    'key':'dom_SA_3km_large3',
    #'label':'large 3',
    'label':'COSMO 3.3',
    'lon':slice(lon0, lon0 + 0.03*(nlon-1)),
    'lat':slice(lat0, lat0 + 0.03*(nlat-1)),
    'nlon':nlon,
    'nlat':nlat,
    'dticks':20,}


lon0 = -58.02
lat0 = -36.40
nlon = 3000
nlat = 2100
dom_SA_3km_large = {
    'key':'dom_SA_3km_large',
    'label':'large',
    'lon':slice(lon0, lon0 + 0.03*(nlon-1)),
    'lat':slice(lat0, lat0 + 0.03*(nlat-1)),
    'nlon':nlon,
    'nlat':nlat,
    'dticks':20,}

lon0 = -53.52
lat0 = -36.10
nlon = 2800
nlat = 1970
dom_SA_3km_interim = {
    'key':'dom_SA_3km_interim',
    'label':'large',
    'lon':slice(lon0, lon0 + 0.03*(nlon-1)),
    'lat':slice(lat0, lat0 + 0.03*(nlat-1)),
    'nlon':nlon,
    'nlat':nlat,
    'dticks':20,}

#lon0 = -50.52
#lat0 = -36.10
#nlon = 2570
#nlat = 1930
lon0 = -50.04
lat0 = -36.10
nlon = 2550
nlat = 1950
dom_SA_3km_interim2 = {
    'key':'dom_SA_3km_interim2',
    'label':'extended',
    'lon':slice(lon0, lon0 + 0.03*(nlon-1)),
    'lat':slice(lat0, lat0 + 0.03*(nlat-1)),
    'nlon':nlon,
    'nlat':nlat,
    'dticks':20,}


lon0 = -34.02
lat0 = -31.00
nlon = 2014
nlat = 1800
dom_SA_3km_OLD = {
    'key':'dom_SA_3km_OLD',
    #'label':'COSMO 3.3 OLD',
    'label':'original',
    'lon':slice(lon0, lon0 + 0.03*(nlon-1)),
    'lat':slice(lat0, lat0 + 0.03*(nlat-1)),
    'nlon':nlon,
    'nlat':nlat,
    'dticks':20,}
#print(dom_SA_3km_OLD)
#quit()



###### 2km
lon0 = -24
lat0 = -24
nlon = 2100
nlat = 1180
dom_DYA_2km = {
    'key':'dom_DYA_2km',
    'label':'COSMO 2.2',
    'lon':slice(lon0, lon0 + 0.02*(nlon-1)),
    'lat':slice(lat0, lat0 + 0.02*(nlat-1)),
    'nlon':nlon,
    'nlat':nlat,}
#print(dom_2km)
#quit()


###### 1km
lon0 = -16.8
lat0 = -21
nlon = 3200
nlat = 1830
dom_DYA_1km = {
    'key':'dom_DYA_1km',
    'label':'COSMO 1.1',
    'lon':slice(lon0, lon0 + 0.01*(nlon-1)),
    'lat':slice(lat0, lat0 + 0.01*(nlat-1)),
    'nlon':nlon,
    'nlat':nlat,}

###### 0.5km
lon0 = -15.25
lat0 = -19.75
nlon = 5300
nlat = 3100
dom_DYA_05km = {
    'key':'dom_DYA_0.5km',
    'label':'COSMO 0.5',
    'lon':slice(lon0, lon0 + 0.005*(nlon-1)),
    'lat':slice(lat0, lat0 + 0.005*(nlat-1)),
    'nlon':nlon,
    'nlat':nlat,}






###### 24km soil spin up
#lon0 = -75
#lat0 = -37
#nlon = 490
#nlat = 330
lon0 = -68.4
lat0 = -38.54
nlon = 464
nlat = 308
dom_lm_24_soil_spinup = {
    'key':'dom_24km',
    'label':'24km',
    'lon':slice(lon0, lon0 + 0.22*(nlon-1)),
    'lat':slice(lat0, lat0 + 0.22*(nlat-1)),
    'nlon':nlon,
    'nlat':nlat,
    'dticks':20,}

#print(dom_lm_24_soil_spinup)
#quit()




###############################################################################
# OBSERVATION AND REANALYSIS DATA SETS
###############################################################################

###### ERA5 download
lon0 = -55
lat0 = -38
nlon = 280
nlat = 210
dom_ERA5 = {
    'key':'dom_ERA5_download',
    'label':'ERA5_download',
    'lon':slice(lon0, lon0 + 0.30*(nlon-1)),
    'lat':slice(lat0, lat0 + 0.30*(nlat-1)),
    'nlon':nlon,
    'nlat':nlat,
    'dticks':20,}

#print(dom_ERA5)
#quit()

###### ERA5 COSMO nesting
lon0 = -70.875
lat0 = -31.89694
nlon = 349
nlat = 228
dom_ERA5_COSMO_nesting = {
    'key':'dom_COSMO_nesting',
    'label':'COSMO_nesting',
    'lon':slice(lon0, lon0 + 0.28331*(nlon-1)),
    'lat':slice(lat0, lat0 + 0.28105*(nlat-1)),
    'nlon':nlon,
    'nlat':nlat,
    'dticks':20,}

#print(dom_ERA5_COSMO_nesting)
#quit()

lon0 = 31
lat0 = 6
lon1 = 74
lat1 = 48
dom_ERA5_gulf = {
    'key':'dom_ERA5_gulf',
    'label':'ERA5_gulf',
    'lon':slice(lon0, lon1),
    'lat':slice(lat0, lat1),
    'nlon':nlon,
    'nlat':nlat,
    'dticks':20,}


###### METEOSAT DISK AREA
lon0 = -60
lat0 = -60
lon1 = 60
lat1 = 60
nlon = np.nan
nlat = np.nan
dom_meteosat_disk = {
    'key':'dom_meteosat_disk',
    'label':'Meteosat Disk',
    'lon':slice(lon0, lon1),
    'lat':slice(lat0, lat1),
    'nlon':nlon,
    'nlat':nlat,
    'dticks':20,}


###############################################################################
# ANALYSIS DOMAINS
###############################################################################

######### FULL 3km domain over ocean with margin
dom_global = {
    #'mask':{'field':'FRLAND','transform':None,'thresh':0.0},
    'key':'dom_global',
    'label':'Global',
    'lon':slice(-180,180),
    'lat':slice(-90,90),
    'nlon':360,
    'nlat':180,
    'dticks':90,}



###############################################################################
######### FULL 3km domain over ocean
lon0 = -54.54
lat0 = -37.45
nlon = 2750
nlat = 2065
dom_SA_3km_large3_sea = {
    'mask':{'field':'FRLAND','transform':None,'thresh':0.0},
    'key':'dom_SA_3km_large3_sea',
    'label':'COSMO 3.3',
    'lon':slice(lon0, lon0 + 0.03*(nlon-1)),
    'lat':slice(lat0, lat0 + 0.03*(nlat-1)),
    'nlon':nlon,
    'nlat':nlat,
    'dticks':20,}
######### FULL 3km domain over land
dom_SA_3km_large3_land = {
    'mask':{'field':'FRLAND','transform':'1-x','thresh':1.0},
    'key':'dom_SA_3km_large3_land',
    'label':'COSMO 3.3',
    'lon':slice(lon0, lon0 + 0.03*(nlon-1)),
    'lat':slice(lat0, lat0 + 0.03*(nlat-1)),
    'nlon':nlon,
    'nlat':nlat,
    'dticks':20,}
#print(dom_SA_3km_large3)
#quit()
###############################################################################


###############################################################################
######### FULL 3km domain with margin
dx = 0.03
margin = 2.00
lon0 = dom_SA_3km_large3['lon'].start + margin
lat0 = dom_SA_3km_large3['lat'].start + margin
nlon = dom_SA_3km_large3['nlon'] - margin/dx * 2
nlat = dom_SA_3km_large3['nlat'] - margin/dx * 2
dom_SA_anim = {
    'key':'dom_SA_anim',
    'label':'Animation',
    'lon':slice(lon0, lon0 + 0.03*(nlon-1)),
    'lat':slice(lat0, lat0 + 0.03*(nlat-1)),
    'nlon':nlon,
    'nlat':nlat,
    'dticks':20,}
dx = 0.03
margin_left = 3.50
margin_right = 2.00
margin_top = 3.50
margin_bottom = 2.00
lon0 = dom_SA_3km_large3['lon'].start + margin_left
lat0 = dom_SA_3km_large3['lat'].start + margin_bottom
nlon = dom_SA_3km_large3['nlon'] - (margin_left + margin_right)/dx
nlat = dom_SA_3km_large3['nlat'] - (margin_bottom + margin_top)/dx
dom_SA_anim2 = {
    'key':'dom_SA_anim2',
    'label':'Animation',
    'lon':slice(lon0, lon0 + 0.03*(nlon-1)),
    'lat':slice(lat0, lat0 + 0.03*(nlat-1)),
    'nlon':nlon,
    'nlat':nlat,
    'dticks':20,}
#dom_anim3 = {
#    'label' :'anim3',
#    'key'  :'dom_SA_anim3',
#    'lon'   :slice(-32.0, 15.0),
#    'lat'   :slice(-25.0,- 3.0),
#    'dticks':10,
#}
#dom_anim3['nlat'] = (dom_anim3['lat'].stop - dom_anim3['lat'].start) / 0.03 + 1
#dom_anim3['nlon'] = (dom_anim3['lon'].stop - dom_anim3['lon'].start) / 0.03 + 1
###############################################################################
######### FULL 3km domain with margin
dx = 0.03
margin = 1.5
lon0 = dom_SA_3km_large3['lon'].start + margin
lon1 = dom_SA_3km_large3['lon'].stop - 4
lat0 = -30
lat1 = dom_SA_3km_large3['lat'].stop - margin
#nlon = int(dom_SA_3km_large3['nlon'] - margin/dx * 2)
nlon = int((lon1 - lon0) / dx + 1)
nlat = int((lat1 - lat0) / dx + 1)
dom_SA_ana = {
    'key':'dom_SA_ana',
    'label':'Tropics',
    'lon':slice(lon0, lon1),
    'lat':slice(lat0, lat1),
    'nlon':nlon,
    'nlat':nlat,
    'dticks':20,}
#print(dom_SA_ana)
#quit()
######### FULL 3km domain over ocean with margin
dom_SA_ana_sea = {
    'mask':{'field':'FRLAND','transform':None,'thresh':0.5},
    'key':'dom_SA_ana_sea',
    'label':'ATL',
    'lon':dom_SA_ana['lon'],
    'lat':dom_SA_ana['lat'],
    'nlon':dom_SA_ana['nlon'],
    'nlat':dom_SA_ana['nlat'],
    'dticks':20,
}
#print(dom_SA_ana_sea)
#quit()
dom_SA_ana_sea_2 = {
    'mask':{'field':'FRLAND','transform':None,'thresh':0.5},
    'key':'dom_SA_ana_sea_2',
    'label':'ATL',
    'lon':slice(dom_SA_ana['lon'].start, 17),
    'lat':dom_SA_ana['lat'],
    'dticks':20,
}
######### FULL 3km domain over land with margin
dom_SA_ana_land = {
    'mask':{'field':'FRLAND','transform':'1-x','thresh':1.0},
    'key':'dom_SA_ana_land',
    #'label':'Tropics (land)',
    'label':'Continents',
    'lon':dom_SA_ana['lon'],
    'lat':dom_SA_ana['lat'],
    'nlon':dom_SA_ana['nlon'],
    'nlat':dom_SA_ana['nlat'],
    'dticks':20,
}

########## meridional Atlantic cross-section domain
dom_SA_ana_merid_cs = {
    'key':      'dom_NS_cs',
    #'label':    'OCEAN-CS',
    'label':    'HC-W',
    'lon':      slice(-34.0,-18.0),
    'lat':      dom_SA_ana['lat'],
    'dticks':   10,
}
dom_SA_ana_merid_cs_2 = {
    'key':      'dom_NS_cs_2',
    'label':    'HC-E',
    'lon':      slice(-34.0+23,-18.0+23),
    'lat':      dom_SA_ana['lat'],
    'dticks':   10,
}

########## meridional Africa cross-section domain
dom_SA_ana_merid_cs_afr = {
    'key':      'dom_NS_cs_afr',
    'label':    'LAND-CS',
    #'lon':      slice(15.0,dom_SA_ana['lon'].stop),
    'lon':      slice(12.0,dom_SA_ana['lon'].stop),
    'lat':      dom_SA_ana['lat'],
    'dticks':   10,
}

# trade wind / low cloud region
nlon = int(dom_SA_3km_large3['nlon'] - margin/dx * 2)
nlat = int((lat1 - lat0) / dx + 1)
dom_trades = {
    'mask':{'field':'FRLAND','transform':None,'thresh':0.0},
    'label' :'Trades',
    'key'  :'dom_trades',
    'lon'   :slice(-32.0, 15.0),
    'lat'   :slice(-25.0,- 3.0),
    'dticks':10,
}
dom_trades['nlat'] = (dom_trades['lat'].stop - dom_trades['lat'].start) / 0.03 + 1
dom_trades['nlon'] = (dom_trades['lon'].stop - dom_trades['lon'].start) / 0.03 + 1
# ITCZ
dom_ITCZ = {
    'mask':{'field':'FRLAND','transform':None,'thresh':0.0},
    'label' :'ITCZ',
    'key'  :'dom_ITCZ',
    #'lon'   :slice(-53.0, 12.0),
    'lon'   :slice(-50.0,-10.0),
    'lat'   :slice(- 5.0, 13.0),
    'dticks':10,
}
# deep MBL subdomain
dom_trades_deep = {
    'mask':{'field':'FRLAND','transform':None,'thresh':0.0},
    #'label' :'Trades deep',
    'label' :'TRD-S',
    'key'  :'dom_trades_deep',
    #'lon'   :slice(-32.0,- 5.0),
    #'lat'   :slice(-20.0,- 5.0),
    'lon'   :slice(-32.0,- 1.0),
    'lat'   :slice(-20.0,- 3.0),
    'dticks':10,
}
# shallow MBL subdomain
dom_trades_shallow = {
    'mask':{'field':'FRLAND','transform':None,'thresh':0.0},
    #'label' :'Trades shallow',
    'label' :'STC',
    'key'  :'dom_trades_shallow',
    #'lon'   :slice(- 5.0, 15.0),
    #'lat'   :slice(-32.0,- 5.0),
    'lon'   :slice(- 3.0, 15.0),
    'lat'   :slice(-30.0,- 7.0),
    'dticks':10,
}
# Gulf of Guinea and beyond
dom_guinea_gulf = {
    'mask':{'field':'FRLAND','transform':None,'thresh':0.0},
    'label' :'Gulf of Guinea',
    'key'  :'dom_guinea_gulf',
    'lon'   :slice(-10.0, 13.0),
    'lat'   :slice(- 8.0,  7.0),
    'dticks':10,
}

###### domains for PGW feedback paper
############################################################
dom_ITCZ_feedback = {
    'mask':{'field':'FRLAND','transform':None,'thresh':0.0},
    'label' :'ITCZ',
    'key'  :'dom_ITCZ_feedback',
    'lon'   :slice(-42.0,-15.0),
    'lat'   :slice(- 5.0, 13.0),
    'dticks':10,
}

dom_trades_west = {
    'mask':{'field':'FRLAND','transform':None,'thresh':0.0},
    'label' :'TRD-W',
    'key'  :'dom_trades_west',
    'lon'   :slice(-34.0,-15.0),
    'lat'   :slice(-25.0,- 5.0),
    'dticks':10,
}
dom_trades_west['nlat'] = (dom_trades_west['lat'].stop - dom_trades_west['lat'].start) / 0.03 + 1
dom_trades_west['nlon'] = (dom_trades_west['lon'].stop - dom_trades_west['lon'].start) / 0.03 + 1

dom_trades_east = {
    'mask':{'field':'FRLAND','transform':None,'thresh':0.0},
    'label' :'TRD-E',
    'key'  :'dom_trades_east',
    'lon'   :slice(-15.0, 11.0),
    'lat'   :slice(-25.0,- 5.0),
    'dticks':10,
}
dom_trades_east['nlat'] = (dom_trades_east['lat'].stop - dom_trades_east['lat'].start) / 0.03 + 1
dom_trades_east['nlon'] = (dom_trades_east['lon'].stop - dom_trades_east['lon'].start) / 0.03 + 1

dom_trades_easternmost = {
    'mask':{'field':'FRLAND','transform':None,'thresh':0.0},
    'label' :'TRD-EE',
    'key'  :'dom_trades_easternmost',
    'lon'   :slice(  0.0, 15.0),
    'lat'   :slice(-25.0,- 5.0),
    'dticks':10,
}
dom_trades_easternmost['nlat'] = (
    dom_trades_easternmost['lat'].stop - dom_trades_easternmost['lat'].start) / 0.03 + 1
dom_trades_easternmost['nlon'] = (
    dom_trades_easternmost['lon'].stop - dom_trades_easternmost['lon'].start) / 0.03 + 1

dom_trades_full = {
    'mask':{'field':'FRLAND','transform':None,'thresh':0.0},
    'label' :'TRD-S',
    'key'  :'dom_trades_full',
    'lon'   :slice(-34.0, 11.0),
    'lat'   :slice(-25.0,- 5.0),
    'dticks':10,
}
dom_trades_full['nlat'] = (dom_trades_full['lat'].stop - dom_trades_full['lat'].start) / 0.03 + 1
dom_trades_full['nlon'] = (dom_trades_full['lon'].stop - dom_trades_full['lon'].start) / 0.03 + 1

dom_trades_NA = {
    'mask':{'field':'FRLAND','transform':None,'thresh':0.0},
    'label' :'TRD-N',
    'key'  :'dom_trades_NA',
    'lon'   :slice(dom_SA_ana['lon'].start,-18.0),
    'lat'   :slice(  8.0,dom_SA_ana['lat'].stop),
    'dticks':10,
}
dom_trades_NA['nlat'] = (dom_trades_NA['lat'].stop - dom_trades_NA['lat'].start) / 0.03 + 1
dom_trades_NA['nlon'] = (dom_trades_NA['lon'].stop - dom_trades_NA['lon'].start) / 0.03 + 1

dom_trades_merid = {
    'mask':{'field':'FRLAND','transform':None,'thresh':0.0},
    'label' :'TRD merid',
    'key'  :'dom_trades_merid',
    'lon'   :slice(- 3.0, 11.0),
    'lat'   :slice(-25.0,- 3.0),
    'dticks':10,
}
dom_trades_merid['nlat'] = (dom_trades_merid['lat'].stop - dom_trades_merid['lat'].start) / 0.03 + 1
dom_trades_merid['nlon'] = (dom_trades_merid['lon'].stop - dom_trades_merid['lon'].start) / 0.03 + 1


dom_trades_extended = {
    'label' :'TRDEXT',
    'key'  :'dom_trades_extended',
    'lon'   :slice(dom_SA_ana['lon'].start,dom_SA_ana['lon'].stop+10),
    'lat'   :slice(-25.0,- 5.0),
    'dticks':10,
}
dom_trades_extended['nlat'] = (dom_trades_extended['lat'].stop - dom_trades_extended['lat'].start) / 0.03 + 1
dom_trades_extended['nlon'] = (dom_trades_extended['lon'].stop - dom_trades_extended['lon'].start) / 0.03 + 1
############################################################







# ITCZ
dom_ITCZ_cs = {
    'label' :'ITCZ cs',
    'key'  :'dom_ITCZ_cs',
    'lon'   :slice(-27.0,-20.0),
    'lat'   :9.2,
    'dticks':10,
    'hide_legend':1,
}
# deep MBL subdomain
dom_trades_deep_cs = {
    'label' :'Trades deep cs',
    'key'  :'dom_trades_deep_cs',
    'lon'   :slice(-19.0,-12.0),
    'lat'   :-8,
    'dticks':10,
    'hide_legend':1,
}
# shallow MBL subdomain
dom_trades_shallow_cs = {
    'label' :'Trades shallow cs',
    'key'  :'dom_trades_shallow_cs',
    'lon'   :slice( -2.0,  5.0),
    'lat'   :-15,
    'dticks':10,
    'hide_legend':1,
}
###############################################################################

######### DYAMOND paper domains START
# South-East Atlantic Stratocumulus
dom_SEA_Sc = {
    'label' :'full analysis',
    'key'  :'dom_SEA_Sc',
    #'lon'   :slice(-15,11),
    #'lat'   :slice(-19.5,-4.5),
    'lon'   :slice(-14.7,10.3),
    'lat'   :slice(-18.4,-4.8),
    'dticks':6,
}
# Snapshot for COSMO LWP
dom_Sc_zoom = {
    'label' :'snapshot',
    'key'  :'dom_snapshot',
    'lon'   :slice(-4,2),
    'lat'   :slice(-15,-9),
    #'lon'   :slice(  6.0, 10.3),
    #'lat'   :slice(-18.4,-14.0),
    'dticks':3,
}
# South-East Atlantic Stratocumulus subdomain for trade wind Cumulus
dom_SEA_Sc_sub_Cu = {
    #'label' :'trade-wind cumulus',
    'label' :'cross-section 2',
    'key'  :'dom_SEA_Sc_sub_Cu',
    'lon'   :slice(-14.7,-10.7),
    #'lat'   :slice(- 8.8,- 4.8),
    'lat'   :slice(- 9.0,- 9.0),
    'dticks':3,
}
# South-East Atlantic Stratocumulus only low-lying part
dom_SEA_Sc_sub_Sc = {
    #'label' :'stratocumulus',
    'label' :'cross-section 1',
    'key'  :'dom_SEA_Sc_sub_Sc',
    #'lon'   :slice(- 0.0,  3.9), # used for spatial plot subticks
    'lon'   :slice(- 0.0,  4.0),
    #'lat'   :slice(-15.0,-11.0),
    'lat'   :slice(-15.0,-15.0),
    'dticks':3,
}
dom_SEA_Sc_sub_St = {
    'label' :'Stratus',
    'key'  :'dom_SEA_Sc_sub_St',
    'lon'   :slice(  6.3, 10.3),
    'lat'   :slice(-18.4,-14.4),
    'dticks':3,
}
######### DYAMOND paper domains END




# South Atlantic Stratocumulus
dom_test = {
    'label' :'test',
    'key'  :'dom_test',
    'lon'   :slice(-52, 20),
    'lat'   :slice(5.5,5.5),
    'dticks':3,
}
# subdomain DYAMOND simulations
dom_SA = {
    'label' :'South Atlantic',
    'key'  :'dom_SA',
    'lon'   :slice(-35,15),
    'lat'   :slice(-26,5),
}
# domain used for 2D cross-sections
dom_cross_sect = {
    'label' :'cross-section',
    'key'  :'dom_crosss',
    'lon'   :slice(-19, 11),
    'lat'   :slice(-17,-14),
}
# domain used for 2D cross-sections
dom_cs_close = {
    'label' :'close cross-section',
    'key'  :'dom_crosss',
    'lon'   :slice(- 8.0, 10.0),
    'lat'   :slice(-15.1,-14.9),
    #'lat'   :slice(-16.0),
}
# South-East Atlantic Stratocumulus TQC animation
dom_SEA_Sc_anim = {
    'label' :'South-East Atlantic Sc Animation',
    'key'  :'dom_SEA_anim',
    'lon'   :slice(-8,11),
    'lat'   :slice(-18,-6),
    'dticks':6,
    #'lon'   :slice(-4,5.5),
    #'lat'   :slice(-15,-9),
    #'dticks':3,
}

#dom_SEA = {
#    'label' :'South-East Atlantic',
#    'key'  :'dom_SEA',
#    'lon'   :slice(-25,14),
#    'lat'   :slice(-21,0),
#    #'lon'   :slice(0,18),
#    #'lat'   :slice(-16,0),
#}
## South-East Atlantic Stratocumulus
#dom_SEA_Sc_less = {
#    'label' :'Analysis',
#    'key'  :'dom_SEA_Sc',
#    'lon'   :slice(-15,11),
#    'lat'   :slice(-20,-4),
#    'dticks':10,
#}
#


lon0 = -40
lon1 = 0
lat0 = 0
lat1 = 40
dx = 1
nlon = int((lon1 - lon0) / dx + 1)
nlat = int((lat1 - lat0) / dx + 1)
dom_macronesia = {
    'key':'dom_macronesia',
    'label':'Macronesia',
    'lon':slice(lon0, lon1),
    'lat':slice(lat0, lat1),
    'nlon':nlon,
    'nlat':nlat,
    'dticks':20,}


###############################################################################
# DISS APPENDIX PLOTS
###############################################################################
dom_tuning = {
    'mask':{'field':'FRLAND','transform':None,'thresh':0.0},
    'label' :'tuning',
    'key'  :'dom_tuning',
    'lon'   :slice(-26.0, 15.0),
    'lat'   :slice(-28.0,- 2.0),
    'dticks':10,
}
dom_sim_tuning = {
    'mask':{'field':'FRLAND','transform':None,'thresh':0.0},
    'label' :'simulation',
    'key'  :'dom_sim_tuning',
    'lon'   :slice(-27.0, 21.0),
    'lat'   :slice(-29.0,- 1.0),
    'dticks':10,
}


###############################################################################
# ANALYSIS POINTS
###############################################################################
# point St. Helena island
point_st_helena = {
    'label' :'St. Helena grid point',
    'key'  :'point_StHelena',
    'lon'   :-5.6672,
    'lat'   :-15.9419,
}


###############################################################################
# MASTER THESIS ANALYSIS DOMAINS
###############################################################################
dom_alpine_region = {
    'label':'Alpine Region',
    ## normal
    #'lon':slice(-3.76+10,3.68+10),
    #'lat':slice(-3.44+47,1.079+47),
    # rotated
    'lon':slice(-3.76,3.68),
    'lat':slice(-3.44,1.079),
}
dom_northern_italy = {
    'label':'Northern Italy',
    'lat':slice(-2.68+10,-1.12+10),
    'lon':slice(-1.96+47,0.60+47),
    ## rotated
    #'lat':slice(-2.68,-1.12),
    #'lon':slice(-1.96,0.60),
}
dom_alpine_ridge = {
    'label':'Alpine Ridge',
    # rotated
    'lon':slice(-1.375, 0.225),
    'lat':slice(-0.695,-0.295),
}
dom_alps_vert_prof = {
    'label':'Vertical Profile',
    #'lon':slice(-1.78+10, 0.62+10),
    #'lat':slice(-1.09+47,-0.09+47),
    # rotated
    'lon':slice(-1.78, 0.62),
    'lat':slice(-1.09,-0.09),
}


###############################################################################
# DYAMOND DOMAINS
###############################################################################
# first DYAMOND extraction domain (small)
dom_dya_1 = {
    'label':'DYAMOND 1',
    'key':'DYAMOND_1',
    'lat':slice(-25,-5),
    'lon':slice(-19,15)
}

# main DYAMOND extraction domain (large)
dom_dya_2 = {
    'label':'DYAMOND 2',
    'key':'DYAMOND_2',
    'lat':slice(-30,18),
    'lon':slice(-45,18)
}





###############################################################################
# OLD ANALYSIS DOMAINS
###############################################################################
## South-East Atlantic 3D cross-sect
#dom_3D = {
#    'label' :'South-East Atlantic',
#    'key'  :'SEA',
#    'lon'   :slice(-17,16),
#    'lat'   :slice(-23,1.6),
#    #'lon'   :slice(0,18),
#    #'lat'   :slice(-16,0),
#}




###############################################################################
# OLD MODEL DOMAINS
###############################################################################
##############################
###### 3 LEVEL NESTING
##############################
####### 12km
#lon0 = -31.06
#lat0 = -31.06
#nlon = 509
#nlat = 342
#dom_lm_12_3lev = {
#    'key':'12km',
#    'label':'12km',
#    'lon':slice(lon0, lon0 + 0.11*nlon),
#    'lat':slice(lat0, lat0 + 0.11*nlat),
#    'nlon':nlon,
#    'nlat':nlat,}
####### 4km
#lon0 = -35
#lat0 = -29
#nlon = 1400
#nlat = 1200
#dom_lm_4_3lev = {
#    'key':'4km',
#    'label':'4km',
#    'lon':slice(lon0, lon0 + 0.04*nlon),
#    'lat':slice(lat0, lat0 + 0.04*nlat),
#    'nlon':nlon,
#    'nlat':nlat,}
#
##############################
###### 2 LEVEL NESTING
##############################
####### 12km_2lev
#lon0 = -28.09
#lat0 = -28.09
#nlon = 460
#nlat = 288
#dom_lm_12_2lev = {
#    'key':'12km_2lev',
#    'label':'12km_2lev',
#    'lon':slice(lon0, lon0 + 0.11*nlon),
#    'lat':slice(lat0, lat0 + 0.11*nlat),
#    'nlon':nlon,
#    'nlat':nlat,}
#
####### 4km_2lev
#lon0 = -27.00
#lat0 = -27.00
#nlon = 1200
#nlat = 740
#dom_lm_4_2lev = {
#    'key':'4km_2lev',
#    'label':'4km_2lev',
#    'lon':slice(lon0, lon0 + 0.04*nlon),
#    'lat':slice(lat0, lat0 + 0.04*nlat),
#    'nlon':nlon,
#    'nlat':nlat,}
#
####### 4km_itcz
#lon0 = -32
#lat0 = -29
#nlon = 1350
#nlat = 1200
#dom_lm_4_itcz = {
#    'key':'4km',
#    'label':'4.4km',
#    'lon':slice(lon0, lon0 + 0.04*nlon),
#    'lat':slice(lat0, lat0 + 0.04*nlat),
#    'nlon':nlon,
#    'nlat':nlat,}


####### 50km alps for CS
#lon0 = -10
#lat0 = 25
#nlon = 90
#nlat = 80
#dom_lm_alps_50km = {
#    'key':'50km',
#    'label':'50km',
#    'lon':slice(lon0, lon0 + 0.45*nlon),
#    'lat':slice(lat0, lat0 + 0.45*nlat),
#    'nlon':nlon,
#    'nlat':nlat,}



###### 2.2km
lon0 =  39.00
lat0 =  14.00
dlon = 00.02
dlat = 00.02
nlon = 1351
nlat = 1101
dom_gulf_2 = {
    'key':'dom_gulf_2',
    'label':'COSMO 2.2',
    'lon':slice(lon0, lon0 + dlon*(nlon-1)),
    'lat':slice(lat0, lat0 + dlat*(nlat-1)),
    'nlon':nlon,
    'nlat':nlat,
    'dticks':10,
    }

###### 12km
lon0 =  31.50
lat0 =   6.50
dlon = 00.11
dlat = 00.11
nlon = 383
nlat = 374
dom_gulf_12 = {
    'key':'dom_gulf_12',
    'label':'COSMO 12',
    'lon':slice(lon0, lon0 + dlon*(nlon-1)),
    'lat':slice(lat0, lat0 + dlat*(nlat-1)),
    'nlon':nlon,
    'nlat':nlat,
    'dticks':10,
    }
    
###### dom gulf
lon0 =  20.00
lon1 =  80.00
lat0 =   0.00
lat1 =  60.00
dom_map_gulf = {
    'key':'dom_map_gulf',
    'label':'',
    'lon':slice(lon0, lon1),
    'lat':slice(lat0, lat1),
    'nlon':nlon,
    'nlat':nlat,
    'dticks':10,
    }

###### dom gulf
lon0 =  31.50
lat0 =   6.50
dlon = 00.11
dlat = 00.11
nlon = 383
nlat = 374
dom_gulf_anim = {
    'key':'dom_gulf_anim',
    'label':'',
    'lon':slice(lon0, lon0 + dlon/6*(nlon*6-1)),
    'lat':slice(lat0, lat0 + dlat/6*(nlat*6-1)),
    'nlon':nlon*6,
    'nlat':nlat*6,
    'dticks':10,
    }


