#!/bin/bash

n_jobs=12

grid_size_keyword=global_0.022
target_grid_nc=0.022_grid.nc

#grid_size_keyword=global_0.02
#target_grid_nc=0.02_grid.nc

#grid_size_keyword=global_0.05
#target_grid_nc=0.05_grid.nc

griddes=griddes.arpege1

weights_file=weights_ARPEGE_test

split_file=/work/ka1081/2019_06_Hackathon_Mainz/christoph_heim/newdata/ARPEGE-NH_2.5/tmp/dirtmp_201608100000/split.t119.l5400.grb.0.3.4.gp

out_file=H_test.nc

#cdo -O -P $n_jobs --cellsearchmethod spherepart genycon,$grid_size_keyword -setgrid,$griddes \
#                    -setgridtype,regular $split_file $weights_file

#cdo -O -P $n_jobs -f nc -topo,$grid_size_keyword $target_grid_nc

cdo -O -f nc4 -sellonlatbox,-95,-79,-24,-14 -remap,$target_grid_nc,$weights_file \
                     -setgrid,$griddes -setgridtype,regular $split_file $out_file
