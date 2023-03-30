#!/bin/bash
#description:    Extract lat-lon box of data from model FV3
#author:         Christoph Heim
#date created:   20.07.2019
#date changed:   20.07.2019
#usage:          arguments:
#                1.: cdo sellonlatbox argument
#                2.: cdo sellevidx argument
#                3.: model resolution
#                4.: out_base_dir
#                5.: out_name: name of output file (without .nc)
#                6.: inp_file: path to input file
#                7.: target_grid: description in file for target grid
###############################################################################

module load nco


domain=-16,12,-22,-8
levels=1/22
res=7.5
out_base_dir=/work/ka1081/DYAMOND/MPAS-${res}km/tmp
out_name=W_201608100000
#inp_file=


domain=$1
levels=$2
res=$3
out_base_dir=$4
out_name=$5
inp_file=$6
target_grid=$7

#echo $domain
#echo $levels
#echo $res
#echo $out_base_dir
#echo $out_name
#echo $inp_file
#echo $target_grid

out_dir=$out_base_dir/dirtmp_$out_name
grid_def=$out_base_dir/../gridspec.nc
out_file=$out_base_dir/${out_name}.nc

#echo 
#echo $out_dir
#echo $grid_def
#echo $out_file

n_jobs=4

mkdir -p $out_dir

## testing
#inp_file=$out_dir/test.tile?.nc
#echo $inp_file


cdo -P $n_jobs -O \
      -sellonlatbox,$domain \
      -setgrid,$grid_def \
      -sellevidx,$levels \
      -collgrid,gridtype=unstructured \
      $inp_file \
      $out_dir/temp.nc

cdo -P $n_jobs -gennn,$target_grid \
      $out_dir/temp.nc $out_dir/weights.nc

cdo -P $n_jobs -O \
        remap,$target_grid,$out_dir/weights.nc \
        $out_dir/temp.nc $out_file  

