#!/bin/bash
#description:    Extract lat-lon box of data from model MPAS.
#author:         Christoph Heim
#date created:   19.07.2019
#date changed:   22.07.2019
#usage:          arguments:
#                1.: cdo sellonlatbox argument
#                2.: cdo sellevidx argument
#                3.: model resolution
#                4.: out_base_dir
#                5.: out_name: name of output file (without .nc)
#                6.: var_name: NC key of variable in file
#                7.: inp_file: path to input file
#                8.: target_grid: description in file for target grid
#                9.: time_cdo_fmt: time string for cdo settimeaxis
#               10.: vdim: name of vertical dimension in nc file
###############################################################################

module load nco


domain=-16,12,-22,-8
levels=1/22
res=7.5
out_base_dir=/work/ka1081/DYAMOND/MPAS-${res}km/tmp
out_name=W_201608100000
var_name=w
#inp_file=


domain=$1
levels=$2
res=$3
out_base_dir=$4
out_name=$5
var_name=$6
inp_file=$7
target_grid=$8
time_cdo_fmt=$9
vdim=${10}

#echo $domain
#echo $levels
#echo $res
#echo $out_base_dir
#echo $out_name
#echo $var_name
#echo $inp_file
#echo $target_grid
#echo $time_cdo_fmt
#echo $vdim
#exit

out_dir=$out_base_dir/dirtmp_$out_name
grid_def=$out_base_dir/../MPAS_${res}km_grid.nc
out_file=$out_base_dir/${out_name}.nc

n_jobs=4

mkdir -p $out_dir

cdo setattribute,*@axis="txz" -selname,$var_name \
        $inp_file $out_dir/temp1.nc

cdo -P $n_jobs -O -f nc4 \
        -sellonlatbox,$domain \
        -setgrid,mpas:$grid_def, -selgrid,1 \
        $out_dir/temp1.nc $out_dir/temp2.nc

cdo -P $n_jobs -gennn,$target_grid \
        $out_dir/temp2.nc $out_dir/weights.nc

cdo -P $n_jobs -f nc4 -O \
        -setreftime,2016-08-01,00:00:00,minutes \
        -settaxis,$time_cdo_fmt \
        -remap,$target_grid,$out_dir/weights.nc \
        -sellevidx,$levels \
        $out_dir/temp2.nc $out_dir/temp3.nc #$out_file 

ncpdq -O --rdr=time,$vdim,lat,lon \
        $out_dir/temp3.nc $out_file

