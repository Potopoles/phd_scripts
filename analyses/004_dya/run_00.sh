#!/bin/bash

#arg 1: njobs
#arg 2: variable name
#arg 3: mem_key
#arg 4: run_mode

mem_keys=(COSMO_12 ICON_10 \
        NICAM_7 MPAS_7.5 IFS_9)
#mem_keys=(NICAM_7)

mem_keys=(ERA5_31 \
    COSMO_12 ICON_10 NICAM_7 MPAS_7.5 IFS_9 \
    COSMO_4.4 COSMO_2.2 \
    COSMO_4.4_calib_7 COSMO_4.4_calib_8 \
    NICAM_3.5 \
    SAM_4 \
    ICON_2.5 \
    UM_5 \
    MPAS_3.75 \
    IFS_4 \
    GEOS_3 \
    ARPEGE-NH_2.5 \
    FV3_3.25 \
    COSMO_1.1 COSMO_0.5)

#mem_keys=(COSMO_4.4_calib_7 COSMO_4.4_calib_8)

#mem_keys=(COSMO_1.1)
mem_keys=(COSMO_0.5)
##
#mem_keys=(COSMO_1.1 COSMO_0.5)


mem_keys=(ERA5_31 \
    COSMO_2.2 \
    NICAM_3.5 \
    SAM_4 \
    ICON_2.5 \
    UM_5 \
    MPAS_3.75 \
    IFS_4 \
    GEOS_3 \
    ARPEGE-NH_2.5 \
    FV3_3.25)


#mem_keys=(CM_SAF_MSG_AQUA_TERRA)
#mem_keys=(OBS)
#mem_keys=(ERA5_31)
#mem_keys=(COSMO_12)
#mem_keys=(COSMO_2.2)
#mem_keys=(COSMO_1.1)
#mem_keys=(COSMO_0.5)
#mem_keys=(NICAM_3.5)
#mem_keys=(SAM_4)
mem_keys=(ICON_2.5)
#mem_keys=(ICON_10)
#mem_keys=(ICON_10 ICON_2.5)
#mem_keys=(UM_5)
#mem_keys=(MPAS_3.75)
#mem_keys=(IFS_4)
#mem_keys=(GEOS_3)
#mem_keys=(ARPEGE-NH_2.5)
#mem_keys=(FV3_3.25)
#mem_keys=(OBS)

##mem_keys=(COSMO_4.4_long1)
##mem_keys=(COSMO_4.4_long2)
#mem_keys=(COSMO_4.4_calib_7 COSMO_4.4 COSMO_4.4_calib_13 \
#          COSMO_4.4_calib_12 COSMO_4.4_calib_18 \
#          COSMO_4.4_calib_15 COSMO_4.4_calib_16)
#mem_keys=(COSMO_4.4_calib_20 COSMO_4.4_calib_21 \
#          COSMO_4.4_calib_22 COSMO_4.4_calib_23 \
#          COSMO_4.4_calib_24 COSMO_4.4_calib_25 \
#          COSMO_4.4_calib_26 COSMO_4.4_calib_27)
#mem_keys=(OBS)
##mem_keys=(COSMO_3.3_test_1)
##mem_keys=(COSMO_3.3_test_2)
##mem_keys=(COSMO_3.3_test_6 COSMO_3.3_test_7 COSMO_3.3_SA_long)
#mem_keys=(COSMO_4.4_calib_29 COSMO_4.4_calib_30 \
#          COSMO_4.4_calib_31 COSMO_4.4_calib_32)
#
#mem_keys=(COSMO_4.4_calib_33 COSMO_4.4_calib_34 \
#          COSMO_4.4_calib_35 COSMO_4.4_calib_36)
#

mem_keys=(OBS)
#mem_keys=(COSMO_3.3_SA_3_long)


#njobs=21
njobs=18
#njobs=12
#njobs=9
#njobs=6
#njobs=3
njobs=1

run_mode=daily
#run_mode=tmean

years=(2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017 2018 2019)
years=(1983 1984 1985 1986 1987 1988 1989 1990 \
      1991 1992 1993 1994 1995 1996 1997 1998 1999 2000 \
      2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 \
      2011 2012 2013 2014 2015 2016 2017 2018 2019)
years=(1991 1992 1993 1994 1995 1996 1997 1998 1999 2000 \
      2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 \
      2011 2012 2013 2014 2015 2016 2017 2018 2019)
years=(2011 2012 2013 2014 2015 2016 2017 2018)
years=(2003)
#years=(2014 2015 2016 2017 2018)
#years=(2009 2010 2011 2012 2013)
years=(2016)
#years=(2006)


### step 1
# variables that should be DERIVED with REMAPPING!
# and then set sto DIRECT
# TODO: remap!
var_names=(LWUTOA SWUTOA SWDTOA TQI)
var_names=(LWUTOA SWUTOA SWDTOA)
var_names=(SWUTOA SWDTOA)
var_names=(LWUTOA)
## step 2
# basic variables that should DERIVED, stored,
# and then set to DIRECT
var_names=(ALBEDO INVHGT POTT RHO)
var_names=(ALBEDO INVHGT)
var_names=(ALBEDO)
#var_names=(POTT RHO)
##### step 3
#var_names=(ENTR UVFLXDIV POTTVDIV POTTHDIV \
#           TNORMI QCNORMI QVNORMI WNORMI AWNORMI \
#           TQV INVSTR INVSTRV)
#var_names=(ENTR INVSTRV TNORMI QCNORMI QVNORMI)
#var_names=(POTTVDIV)
#var_names=(WNORMI)
#### step 4
#run_mode=tmean
#var_names=(W U V POTT INVHGT)
#var_names=(W U V POTT)
#### run 07_reynolds!
#### step 5
#run_mode=daily
#var_names=(UVFLXDIVNORMI DIABHNORMI POTTDIVTURBNORMI \
#       POTTHDIVTURBNORMI POTTVDIVTURBNORMI \
#       POTTHDIVNORMI POTTVDIVNORMI)


for year in ${years[@]} 
do
    echo $year
    for var_name in ${var_names[@]} 
    do
        echo $var_name
        for mem_key in ${mem_keys[@]} 
        do
            echo $mem_key
            python 00_compute_fields.py $njobs $var_name $mem_key $run_mode $year
        done
    done
done

