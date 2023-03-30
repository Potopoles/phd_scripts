#!/bin/bash

inp_dir=../full
out_dir=../subdomain

#month=08
month=09
#days=(01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31)
days=(01 02 03 04 05 06 07 08 09 10 11)
hrs=(00 03 06 09 12 15 18 21)

lon0=-33.5
lon1=23.5
lat0=-30.5
lat1=20.5

start_lev=30

for day in ${days[@]}; do
for hr in ${hrs[@]}; do
    echo $day$hr
    #ncks -O -F  -d level1,$start_lev,137 -d level,$start_lev,136 \
    ncks -O -F  -d level1,$start_lev,138 -d level,$start_lev,137 \
                -d lon,$lon0,$lon1 -d lat,$lat0,$lat1 \
                $inp_dir/cas2016$month$day${hr}0000.nc $out_dir/cas2016$month${day}${hr}0000.nc
done
done



