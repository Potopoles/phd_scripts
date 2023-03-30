def setSSI(i_subdomain, ssI):
    if i_subdomain == 0:
        domainName = 'Whole_Domain'
        lon0 = 0
        #lon1 = 261 
        lon1 = 262 
        lat0 = 0
        #lat1 = 245
        lat1 = 246
    elif i_subdomain == 1:
        domainName = 'Alpine_Region'
        lon0 = 50
        lon1 = 237
        lat0 = 41
        lat1 = 155
    elif i_subdomain == 2:
        domainName = 'Northern_Italy'
        lon0 = 95 
        lon1 = 160 
        lat0 = 60 
        lat1 = 100 
    elif i_subdomain == 3:
        domainName = 'South_Western_Alps'
        lon0 = 50 
        lon1 = 115 
        lat0 = 35 
        lat1 = 90 
    elif i_subdomain == 4:
        domainName = 'Close_Up_Crossect'
        lon0 = 110 
        lon1 = 110
        lat0 = 85  
        lat1 = 135 
    elif i_subdomain == 9:
        domainName = 'Test_Domain'
        lon0 = 130 
        lon1 = 135 
        lat0 = 120  
        lat1 = 123 
         
    ssI['4.4']['rlon'] = list(range(lon0,lon1))
    ssI['4.4']['rlat'] = list(range(lat0,lat1)) 
    ssI['4.4']['srlon'] = list(range(lon0,lon1)) 
    ssI['4.4']['srlat'] = list(range(lat0,lat1)) 
    ssI['2.2']['rlon'] = list(range(lon0*2,lon1*2+1))
    ssI['2.2']['rlat'] = list(range(lat0*2,lat1*2+1)) 
    ssI['2.2']['srlon'] = list(range(lon0*2,lon1*2+1)) 
    ssI['2.2']['srlat'] = list(range(lat0*2,lat1*2+1)) 
    ssI['1.1']['rlon'] = list(range(lon0*4,lon1*4+3))
    ssI['1.1']['rlat'] = list(range(lat0*4,lat1*4+3)) 
    ssI['1.1']['srlon'] = list(range(lon0*4,lon1*4+3)) 
    ssI['1.1']['srlat'] = list(range(lat0*4,lat1*4+3)) 

    #ssI['rlon'] = [lon0,lon1]
    #ssI['rlat'] = [lat0,lat1]

    return(ssI, domainName)
