#!/bin/bash
# do not run with ./ but with source

module load daint-gpu
module load ncview
#module load CDO # raises error now
module load NCO
#module unload xalt

export PATH="/project/pr133/heimc/anaconda3/bin:$PATH"
source /project/pr133/heimc/anaconda3/etc/profile.d/conda.sh

# make sure xarray does not explode with number of threads
export OMP_NUM_THREADS=1
