#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    time periods definitions:
author			Christoph Heim
date created    20.05.2022
date changed    20.05.2022
usage			import in another script
"""
###############################################################################
from datetime import datetime, timedelta
from dateutil.relativedelta import *
import numpy as np
###############################################################################

start_year = 2006
end_year = 2010
start_month = 8
end_month = 12
start_day = 1
end_day = 31
time_periods_full = [{
    'first_date':datetime(start_year,start_month,start_day),
    'last_date':datetime(end_year,end_month,end_day)
}]


start_year = 2007
end_year = 2010
#end_year = 2007
start_month = 1
end_month = 12
start_day = 1
end_day = 31

time_periods_ana = [{
    'first_date':datetime(start_year,start_month,start_day),
    'last_date':datetime(end_year,end_month,end_day)
}]

time_periods_ana_JFM = []
time_periods_ana_FMA = []
time_periods_ana_MAM = []
time_periods_ana_AMJ = []
time_periods_ana_MJJ = []
time_periods_ana_JJA = []
time_periods_ana_JAS = []
time_periods_ana_ASO = []
time_periods_ana_SON = []
time_periods_ana_OND = []
time_periods_ana_ONDJ = []
time_periods_ana_NDJ = []
time_periods_ana_DJF = []
time_periods_ana_MJ = []
years = np.arange(start_year,end_year+0.1).astype(np.int)
#years = np.arange(2004,2020.1).astype(np.int)
for year in years:
    time_periods_ana_JFM.append(
        {
            'first_date':datetime(year,1,1),
            'last_date':datetime(year,3,31)
        }
    )
    time_periods_ana_FMA.append(
        {
            'first_date':datetime(year,2,1),
            'last_date':datetime(year,4,30)
        }
    )
    time_periods_ana_MAM.append(
        {
            'first_date':datetime(year,3,1),
            'last_date':datetime(year,5,31)
        }
    )
    time_periods_ana_AMJ.append(
        {
            'first_date':datetime(year,4,1),
            'last_date':datetime(year,6,30)
        }
    )
    time_periods_ana_MJJ.append(
        {
            'first_date':datetime(year,5,1),
            'last_date':datetime(year,7,31)
        }
    )
    time_periods_ana_JJA.append(
        {
            'first_date':datetime(year,6,1),
            'last_date':datetime(year,8,31)
        }
    )
    time_periods_ana_JAS.append(
        {
            'first_date':datetime(year,7,1),
            'last_date':datetime(year,9,30)
        }
    )
    time_periods_ana_ASO.append(
        {
            'first_date':datetime(year,8,1),
            'last_date':datetime(year,10,31)
        }
    )
    time_periods_ana_SON.append(
        {
            'first_date':datetime(year,9,1),
            'last_date':datetime(year,11,30)
        }
    )
    time_periods_ana_SON.append(
        {
            'first_date':datetime(year,10,1),
            'last_date':datetime(year,12,31)
        }
    )
    time_periods_ana_OND.append(
        {
            'first_date':datetime(year,10,1),
            'last_date':datetime(year,12,31)
        }
    )
    time_periods_ana_ONDJ.append(
        {
            'first_date':datetime(year,1,1),
            'last_date':datetime(year,1,31)
        }
    )
    time_periods_ana_ONDJ.append(
        {
            'first_date':datetime(year,10,1),
            'last_date':datetime(year,12,31)
        }
    )
    time_periods_ana_NDJ.append(
        {
            'first_date':datetime(year,1,1),
            'last_date':datetime(year,1,31)
        }
    )
    time_periods_ana_NDJ.append(
        {
            'first_date':datetime(year,11,1),
            'last_date':datetime(year,12,31)
        }
    )
    time_periods_ana_DJF.append(
        {
            'first_date':datetime(year,1,1),
            'last_date':datetime(year,3,1)-timedelta(days=1)
        }
    )
    time_periods_ana_DJF.append(
        {
            'first_date':datetime(year,12,1),
            'last_date':datetime(year,12,31)
        }
    )
    time_periods_ana_MJ.append(
        {
            'first_date':datetime(year,5,1),
            'last_date':datetime(year,6,30)
        }
    )

start_year = 2006
end_year = 2006
start_month = 8
end_month = 12
start_day = 1
end_day = 31
time_periods_2006 = [{
    'first_date':datetime(start_year,start_month,start_day),
    'last_date':datetime(end_year,end_month,end_day)
}]

start_year = 2007
end_year = 2007
start_month = 1
end_month = 12
start_day = 1
end_day = 31
time_periods_2007 = [{
    'first_date':datetime(start_year,start_month,start_day),
    'last_date':datetime(end_year,end_month,end_day)
}]

start_year = 2008
end_year = 2008
start_month = 1
end_month = 12
start_day = 1
end_day = 31
time_periods_2008 = [{
    'first_date':datetime(start_year,start_month,start_day),
    'last_date':datetime(end_year,end_month,end_day)
}]

start_year = 2007
end_year = 2008
start_month = 1
end_month = 12
start_day = 1
end_day = 31
time_periods_2007_2008 = [{
    'first_date':datetime(start_year,start_month,start_day),
    'last_date':datetime(end_year,end_month,end_day)
}]

start_year = 2009
end_year = 2010
start_month = 1
end_month = 12
start_day = 1
end_day = 31
time_periods_2009_2010 = [{
    'first_date':datetime(start_year,start_month,start_day),
    'last_date':datetime(end_year,end_month,end_day)
}]

start_year = 2009
end_year = 2009
start_month = 1
end_month = 12
start_day = 1
end_day = 31
time_periods_2009 = [{
    'first_date':datetime(start_year,start_month,start_day),
    'last_date':datetime(end_year,end_month,end_day)
}]


start_year = 2010
end_year = 2010
start_month = 1
end_month = 12
start_day = 1
end_day = 31
time_periods_2010 = [{
    'first_date':datetime(start_year,start_month,start_day),
    'last_date':datetime(end_year,end_month,end_day)
}]


start_year = 1985
end_year = 2014
#end_year = 1985
start_month = 1
end_month = 12
start_day = 1
end_day = 31
time_periods_cmip6_hist = [{
    'first_date':datetime(start_year,start_month,start_day),
    'last_date':datetime(end_year,end_month,end_day)
}]
time_periods_cmip6_hist_JFM = []
time_periods_cmip6_hist_FMA = []
time_periods_cmip6_hist_MAM = []
time_periods_cmip6_hist_AMJ = []
time_periods_cmip6_hist_MJJ = []
time_periods_cmip6_hist_JJA = []
time_periods_cmip6_hist_JAS = []
time_periods_cmip6_hist_ASO = []
time_periods_cmip6_hist_SON = []
time_periods_cmip6_hist_NDJ = []
time_periods_cmip6_hist_DJF = []
time_periods_cmip6_hist_MJ = []
time_periods_cmip6_hist_OND = []
time_periods_cmip6_hist_ONDJ = []
years = np.arange(start_year,end_year+0.1).astype(np.int)
for year in years:
    time_periods_cmip6_hist_JFM.append(
        {
            'first_date':datetime(year,1,1),
            'last_date':datetime(year,3,31)
        }
    )
    time_periods_cmip6_hist_FMA.append(
        {
            'first_date':datetime(year,2,1),
            'last_date':datetime(year,4,30)
        }
    )
    time_periods_cmip6_hist_MAM.append(
        {
            'first_date':datetime(year,3,1),
            'last_date':datetime(year,5,31)
        }
    )
    time_periods_cmip6_hist_AMJ.append(
        {
            'first_date':datetime(year,4,1),
            'last_date':datetime(year,6,30)
        }
    )
    time_periods_cmip6_hist_MJJ.append(
        {
            'first_date':datetime(year,5,1),
            'last_date':datetime(year,7,31)
        }
    )
    time_periods_cmip6_hist_JJA.append(
        {
            'first_date':datetime(year,6,1),
            'last_date':datetime(year,8,31)
        }
    )
    time_periods_cmip6_hist_JAS.append(
        {
            'first_date':datetime(year,7,1),
            'last_date':datetime(year,9,30)
        }
    )
    time_periods_cmip6_hist_ASO.append(
        {
            'first_date':datetime(year,8,1),
            'last_date':datetime(year,10,31)
        }
    )
    time_periods_cmip6_hist_SON.append(
        {
            'first_date':datetime(year,9,1),
            'last_date':datetime(year,11,30)
        }
    )
    time_periods_cmip6_hist_NDJ.append(
        {
            'first_date':datetime(year,1,1),
            'last_date':datetime(year,1,31)
        }
    )
    time_periods_cmip6_hist_NDJ.append(
        {
            'first_date':datetime(year,11,1),
            'last_date':datetime(year,12,31)
        }
    )
    time_periods_cmip6_hist_DJF.append(
        {
            'first_date':datetime(year,1,1),
            'last_date':datetime(year,3,1)-timedelta(days=1)
        }
    )
    time_periods_cmip6_hist_DJF.append(
        {
            'first_date':datetime(year,12,1),
            'last_date':datetime(year,12,31)
        }
    )
    time_periods_cmip6_hist_MJ.append(
        {
            'first_date':datetime(year,5,1),
            'last_date':datetime(year,6,30)
        }
    )
    time_periods_cmip6_hist_OND.append(
        {
            'first_date':datetime(year,10,1),
            'last_date':datetime(year,12,31)
        }
    )
    time_periods_cmip6_hist_ONDJ.append(
        {
            'first_date':datetime(year,1,1),
            'last_date':datetime(year,1,31)
        }
    )
    time_periods_cmip6_hist_ONDJ.append(
        {
            'first_date':datetime(year,10,1),
            'last_date':datetime(year,12,31)
        }
    )


start_year = 2070
end_year = 2099
#end_year = 2070
start_month = 1
end_month = 12
start_day = 1
end_day = 31
time_periods_cmip6_scen = [{
    'first_date':datetime(start_year,start_month,start_day),
    'last_date':datetime(end_year,end_month,end_day)
}]
time_periods_cmip6_scen_JFM = []
time_periods_cmip6_scen_FMA = []
time_periods_cmip6_scen_MAM = []
time_periods_cmip6_scen_AMJ = []
time_periods_cmip6_scen_MJJ = []
time_periods_cmip6_scen_JJA = []
time_periods_cmip6_scen_JAS = []
time_periods_cmip6_scen_ASO = []
time_periods_cmip6_scen_SON = []
time_periods_cmip6_scen_NDJ = []
time_periods_cmip6_scen_DJF = []
time_periods_cmip6_scen_MJ = []
time_periods_cmip6_scen_OND = []
time_periods_cmip6_scen_ONDJ = []
years = np.arange(start_year,end_year+0.1).astype(np.int)
for year in years:
    time_periods_cmip6_scen_JFM.append(
        {
            'first_date':datetime(year,1,1),
            'last_date':datetime(year,3,31)
        }
    )
    time_periods_cmip6_scen_FMA.append(
        {
            'first_date':datetime(year,2,1),
            'last_date':datetime(year,4,30)
        }
    )
    time_periods_cmip6_scen_MAM.append(
        {
            'first_date':datetime(year,3,1),
            'last_date':datetime(year,5,31)
        }
    )
    time_periods_cmip6_scen_AMJ.append(
        {
            'first_date':datetime(year,4,1),
            'last_date':datetime(year,6,30)
        }
    )
    time_periods_cmip6_scen_MJJ.append(
        {
            'first_date':datetime(year,5,1),
            'last_date':datetime(year,7,31)
        }
    )
    time_periods_cmip6_scen_JJA.append(
        {
            'first_date':datetime(year,6,1),
            'last_date':datetime(year,8,31)
        }
    )
    time_periods_cmip6_scen_JAS.append(
        {
            'first_date':datetime(year,7,1),
            'last_date':datetime(year,9,30)
        }
    )
    time_periods_cmip6_scen_ASO.append(
        {
            'first_date':datetime(year,8,1),
            'last_date':datetime(year,10,31)
        }
    )
    time_periods_cmip6_scen_SON.append(
        {
            'first_date':datetime(year,9,1),
            'last_date':datetime(year,11,30)
        }
    )
    time_periods_cmip6_scen_NDJ.append(
        {
            'first_date':datetime(year,1,1),
            'last_date':datetime(year,1,31)
        }
    )
    time_periods_cmip6_scen_NDJ.append(
        {
            'first_date':datetime(year,11,1),
            'last_date':datetime(year,12,31)
        }
    )
    time_periods_cmip6_scen_DJF.append(
        {
            'first_date':datetime(year,1,1),
            'last_date':datetime(year,3,1)-timedelta(days=1)
        }
    )
    time_periods_cmip6_scen_DJF.append(
        {
            'first_date':datetime(year,12,1),
            'last_date':datetime(year,12,31)
        }
    )
    time_periods_cmip6_scen_MJ.append(
        {
            'first_date':datetime(year,5,1),
            'last_date':datetime(year,6,30)
        }
    )
    time_periods_cmip6_scen_OND.append(
        {
            'first_date':datetime(year,10,1),
            'last_date':datetime(year,12,31)
        }
    )
    time_periods_cmip6_scen_ONDJ.append(
        {
            'first_date':datetime(year,1,1),
            'last_date':datetime(year,1,31)
        }
    )
    time_periods_cmip6_scen_ONDJ.append(
        {
            'first_date':datetime(year,10,1),
            'last_date':datetime(year,12,31)
        }
    )


start_year = 2016
end_year = 2016
start_month = 8
end_month = 8
start_day = 1
end_day = 20
time_periods_tuning = [{
    'first_date':datetime(start_year,start_month,start_day),
    'last_date':datetime(end_year,end_month,end_day)
}]









#start_year = 2005
#end_year = 2014
start_year = 2004
end_year = 2010
start_month = 1
end_month = 12
start_day = 1
end_day = 31
time_periods_cm_saf_msg_aqua_terra = [{
    'first_date':datetime(start_year,start_month,start_day),
    'last_date':datetime(end_year,end_month,end_day)
}]


#start_year = 2004
#end_year = 2020
#start_month = 1
#end_month = 12
start_year = 2004
end_year = 2014
start_month = 1
end_month = 12
start_day = 1
end_day = 31
time_periods_ceres_ebaf = [{
    'first_date':datetime(start_year,start_month,start_day),
    'last_date':datetime(end_year,end_month,end_day)
}]


#start_year = 2000
#end_year = 2019
#start_month = 6
#end_month = 5
start_year = 2001
end_year = 2014
start_month = 1
end_month = 12
start_day = 1
end_day = 31
time_periods_gpm_imerg = [{
    'first_date':datetime(start_year,start_month,start_day),
    'last_date':datetime(end_year,end_month,end_day)
}]








def get_time_periods_for_month(year, month):
    if year is not None:
        start_date = datetime(year,month,1)
        end_date = start_date + relativedelta(months=1) - timedelta(days=1)
        time_periods = [{
            'first_date':start_date,
            'last_date':end_date
        }]
    else:
        time_periods = []
        for year in [2007,2008,2009,2010]:
            start_date = datetime(year,month,1)
            end_date = start_date + relativedelta(months=1) - timedelta(days=1)
            time_periods.append({
                'first_date':start_date,
                'last_date':end_date
            })
    return(time_periods)

