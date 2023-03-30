#!/bin/bash


#vars=(PP)

#directories=(daily debug raw_output restart)
directories=(daily)

models=(COSMO_1.1 COSMO_2.2 COSMO_4.4 COSMO_12)
#models=(COSMO_4.4)
models=($2)

source_base_dir=/scratch/snx3000/heimc/data
dest_base_dir=/project/pr133/heimc/data

#case_names=(test_ERAI_12_2 test_ERA5_12_2 test_ERA5_4_2_3hr test_ERA5_4_2_1hr \
#            test_ERA5_12_4_2 test_ERA5_4_2_itcz test_ERA5_4_2_itcz_soil \
#            test_ERAI_4_2_itcz test_ERA5_4_2_itcz_80lev \
#            test_ERA5_4_1)
#case_names=(SA_12_EXPL SA_12_SHAL)
#case_names=(SA_4_2)
case_names=($1)

echo copy from $source_base_dir to $dest_base_dir

for model in  ${models[@]}; do
    echo $model

    for case_name in ${case_names[@]}; do
        echo '   '$case_name

        for dir in ${directories[@]}; do
            echo "         " $dir
            dest_dir=$dest_base_dir/simulations/$model/$case_name/$dir
            src_dir=$source_base_dir/simulations/$model/$case_name/$dir

            mkdir -p $dest_dir
            cp -ru $src_dir/* $dest_dir/
            #cp -r $src_dir/* $dest_dir/
        done

        #for var in ${vars[@]}; do 
        #    echo '       '$var

        #    dest_dir=$dest_base_dir/simulations/$model/$case_name/daily/$var
        #    src_dir=$source_base_dir/simulations/$model/$case_name/daily/$var

        #    mkdir -p $dest_dir
        #    cp -u $src_dir/${var}_*.nc $dest_dir
        #    #cp $src_dir/${var}_20160801.nc $dest_dir
        #done

        #for var in ${vars[@]}; do 
        #    echo '       '$var

        #    dest_dir=$dest_base_dir/simulations/$model/$case_name/daily/$var
        #    src_dir=$source_base_dir/simulations/$model/$case_name/daily/$var

        #    mkdir -p $dest_dir
        #    #cp -u $src_dir/${var}_*.nc $dest_dir
        #    cp $src_dir/${var}_*.nc $dest_dir
        #done
    done
done

