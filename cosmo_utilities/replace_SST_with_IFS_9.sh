#/bin/bash

IFS_dir=/project/pr94/heimc/data/simulations/IFS_9/DYAMOND_2/daily/SST
ERA5_dir=/project/pr94/heimc/data/reanalyses/ERA5_ecmwf_sst

# get ERA5 grid description
cdo griddes $ERA5_dir/cas20160801000000.nc > grid_era5

# get ocean mask
cdo selname,FR_LAND $ERA5_dir/cas20160801000000.nc $ERA5_dir/mask.nc.tmp
cdo -eqc,0 -mulc,100 -nec,0 $ERA5_dir/mask.nc.tmp $ERA5_dir/mask.nc
rm $ERA5_dir/mask.nc.tmp

month_string=201608
month_string=201609

#days=(01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31)
days=(01 02 03 04 05 06 07 08 09)
#days=(10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31)
#days=(01)
hrs=(00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23)
#hrs=(00)

for day in ${days[@]}; do
for hour_string in ${hrs[@]}; do

    day_string=${month_string}${day}
    #hour_string=00
    
    
    ifs_sst_file=ifs_sst${day_string}${hour_string}0000.nc
    
    # remap ifs sst to era5 grid
    cdo remapbil,grid_era5 $IFS_dir/SST_${day_string}.nc $ERA5_dir/${ifs_sst_file}.tmp
    # compute SST difference
    #cdo -sub $ERA5_dir/${ifs_sst_file}.tmp \
    #                -selname,T_SO $ERA5_dir/cas${day_string}${hour_string}0000.nc \
    cdo -sub $ERA5_dir/${ifs_sst_file}.tmp \
                    -selname,T_SKIN $ERA5_dir/cas${day_string}${hour_string}0000.nc \
                    $ERA5_dir/sst_diff.nc.tmp
    cdo -mul $ERA5_dir/mask.nc $ERA5_dir/sst_diff.nc.tmp $ERA5_dir/sst_diff.nc.tmp2
    rm $ERA5_dir/sst_diff.nc.tmp
    cdo setmisstoc,0 $ERA5_dir/sst_diff.nc.tmp2 $ERA5_dir/sst_diff.nc
    rm $ERA5_dir/sst_diff.nc.tmp2
    
    # replace cas file with sst difference
    python replace_SST_with_IFS_9.py $day_string $hour_string
    rm $ERA5_dir/sst_diff.nc
    rm $ERA5_dir/${ifs_sst_file}.tmp 

done
done

rm $ERA5_dir/mask.nc
