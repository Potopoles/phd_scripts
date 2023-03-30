"""
author: Christoph Heim
This script takes the SST from DYAMOND IFS9 and replaces the SST in the 
lbfd files in int2lm_out with the one from IFS9.
"""
import sys, os
from netCDF4 import Dataset

era5_dir=os.path.join('/project','pr94','heimc','data','reanalyses',
                      'ERA5_ecmwf_sst')

#day_string = '20200801'
#hour_string = '00'
day_string = sys.argv[1]
hour_string = sys.argv[2]

tar_file = os.path.join(era5_dir, 'cas{}{}0000.nc'.format(
                        day_string, hour_string))
src_file = os.path.join(era5_dir, 'sst_diff.nc')
print(tar_file)
print(src_file)
#quit()

#with Dataset(tar_file, 'r') as tar_nc:
#    print(tar_nc['T_SKIN'][:].shape)
#quit()

var_name_tar='T_SKIN'
var_name_src='var34'

#tar_nc = Dataset(tar_file, 'a')
with Dataset(src_file, 'r') as src_nc:
    #print(tar_nc['W_SO'][:].shape)
    #print(src_nc['T_SO'][:].shape)
    #print(src_nc['T_SO'][0,0,:,:])
    #src_nc['T_SO'][0,1,:,:] = src_nc['T_SO'][0,0,:,:]

    with Dataset(tar_file, 'a') as tar_nc:
        #print(tar_nc['T_SKIN'][:].shape)

        #for k in range(4):
        #    tar_nc['T_SO'][0,k,:,:] = (
        #                    tar_nc['T_SO'][0,k,:,:] + 
        #                    src_nc['T_SO'][0,0,:,:])

        tar_nc[var_name_tar][0,:,:] = (
                        tar_nc[var_name_tar][0,:,:] + 
                        src_nc[var_name_src][0,:,:] )
