#!/bin/bash
# 29.11.2019
# Christoph Heim
# download data from daint project to O3

src_base_dir=heimc@ela.cscs.ch:/project/pr04/heimc/data/simulations
dest_base_dir=/net/o3/hymet_nobackup/heimc/data/simulations

models=(NICAM_7 NICAM_3.5\
        SAM_4 \
        ICON_10 ICON_2.5 \
        UM_5 \
        MPAS_7.5 MPAS_3.75 \
        IFS_9 IFS_4 \
        GEOS_3 \
        ARPEGE-NH_2.5 \
        FV3_3.25)
#models=(COSMO_12 COSMO_4.4 COSMO_2.2 COSMO_1.1)
models=(MPAS_7.5)


#simulations=(SA_3D)
#simulations=(alps_MT_RAW1_10 alps_MT_RAW1_09 alps_MT_SM1_10 alps_MT_SM1_09)
simulations=(SA)
#simulations=(SA_2lev)

vars=(W H SWUTOA SWNDTOA SWDTOA TQC U10M V10M SLHFLX SSHFLX LWUTOA \
      QV QC T T2M SWDSFC PP PPCONV PPGRID SWNDSFC SWDIFFUSFC PPANVI)
vars=(SWUTOA SWNDTOA SWDTOA)
#vars=(W H)
#vars=(TQC U10M V10M SLHFLX SSHFLX)
#vars=(QV QC T T2M SWDSFC PP PPCONV PPGRID SWNDSFC SWDIFFUSFC PPANVI)

echo $vars

for model in ${models[@]}; do
    echo $model
    for sim in ${simulations[@]}; do
        echo '   '$sim
        for var in ${vars[@]}; do
            dest_dir=$dest_base_dir/$model/$sim/daily/$var
            mkdir -p $dest_dir
            rsync -u $src_base_dir/$model/$sim/daily/$var/${var}_*.nc $dest_dir
        done
    done
done
