#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description:    Namelist for run_compression.py 
author:         Christoph Heim
date created:   09.04.2020
date changed:   23.01.2022
usage:          import from run_compression.py
"""
###############################################################################
import os, argparse
from datetime import datetime
###############################################################################

# base directory containing a subdirectory for each simulation to compress
work_dir = os.path.join('/scratch', 'snx3000', 'heimc', 'data', 'compr_cosmo')
#work_dir = os.path.join('/scratch', 'snx3000', 'heimc', 'pgw')
## TODO
#work_dir = os.path.join('/scratch', 'snx3000', 'heimc', 'data', 'coarse_grain')

## input arguments
parser = argparse.ArgumentParser(description = 'Compress files.')
# case key
parser.add_argument('sim_name', type=str)
# number of parallel processes
parser.add_argument('-p', '--n_par', type=int, default=1)
# year
parser.add_argument('-f', '--first_date', type=str, default='200608010000')
# month
parser.add_argument('-l', '--last_date', type=str, default='200608312300')
# month
parser.add_argument('-o', '--output_groups', type=str, default=None)
# run compression
parser.add_argument('-c', '--run_compression', type=int, default=1)
# run coarse grain
parser.add_argument('-g', '--run_coarse_grain', type=int, default=0)
args = parser.parse_args()
print(args)

# process input arguments
n_par = args.n_par
first_date = datetime.strptime(args.first_date, '%Y%m%d%H%M')
last_date = datetime.strptime(args.last_date, '%Y%m%d%H%M')
output_groups = args.output_groups.split(',')
sim_name = args.sim_name
print(first_date)
print(last_date)
print(output_groups)
print(sim_name)
#quit()


# Apply conserving (False) or lossy (True) compression
# For raw COSMO output, lossy is not recommended
# (see header of run_compresison.py for more information)
run_lossy = False

# if True, nczip will output debug information
run_verbous = False

# if True, run parallel tasks asynchroneous
run_async = True

# if True, grid will be coarse grained
coarse_grain_groups = {
    '3h_3D':        True,
    '1h_2D_cg':     True,
    #'3h_3D_zlev':   True,
    '3h_3D_cloud':  True,
}
if sim_name in ['SA_3_pgw/lm_c','SA_3_pgw2/lm_c','SA_3_pgw3/lm_c']:
    cg_src_grid = os.path.join('grids', 'grid_SA_3')
    cg_trg_grid = os.path.join('grids', 'grid_SA_3_to_0.060')
elif sim_name in ['SA_3_itcz_pgw/lm_c','SA_3_itcz_pgw2/lm_c']:
    cg_src_grid = os.path.join('grids', 'grid_SA_3_itcz')
    cg_trg_grid = os.path.join('grids', 'grid_SA_3_itcz_to_0.060')
else:
    raise NotImplementedError()

print('###################### Start compression job #####################')
print(('Run with {} parallel task(s) for simulation {} '+
       'and COSMO output group(s) {} from {} until {}').format(
       n_par, sim_name, output_groups, first_date, last_date))

