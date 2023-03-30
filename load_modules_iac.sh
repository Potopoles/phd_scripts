#!/bin/bash

# my own conda
#export PATH="/net/mie/lhome/heimc/miniconda3/bin:$PATH"

# iac conda
#module load conda/2019
#source activate iacpy3_2019

eval "$(/home/heimc/miniconda3/bin/conda shell.bash hook)"
# make sure xarray does not explode with number of threads
export OMP_NUM_THREADS=1
conda activate schlange39

source /home/heimc/phd_scripts/package/o3.env
