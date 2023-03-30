#!/bin/bash

#arg 1: njobs
#arg 2: img save mode
#arg 3: variable
#arg 4: panel label

njobs=12
var_name=W
#var_name=QC
#var_name=QV
i_save_fig=3
i_recompute=0


python 04_cross_sects.py $njobs $i_save_fig $i_recompute $var_name  3
#python 04_cross_sects.py $njobs 3 $var_name  6
#python 04_cross_sects.py $njobs 3 $var_name  9
#python 04_cross_sects.py $njobs 3 $var_name 12
#python 04_cross_sects.py $njobs 3 $var_name 15
#python 04_cross_sects.py $njobs 3 $var_name 18
#python 04_cross_sects.py $njobs 3 $var_name 21
#python 04_cross_sects.py $njobs 3 $var_name 23
