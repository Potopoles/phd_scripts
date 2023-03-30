from netCDF4 import Dataset
import sys, glob
import numpy as np

src_file = 'laf20160801000000.nc'
tar_files = glob.glob('{}*'.format(sys.argv[1]))
print(tar_files)

try:
    print('exit. Add 2nd argument = yes if you want to proceed.')
    proceed = sys.argv[2]
    if proceed == "yes":
        print('proceed')

    for tar_file in tar_files:
        print(tar_file)


        src_nc = Dataset(src_file, 'r')
        tar_nc = Dataset(tar_file, 'a')
        #print(tar_nc['T_S'][:].shape)
        #print(src_nc['FR_LAND'][:].shape)
        land_mask = np.argwhere(src_nc['FR_LAND'][:] == 0)

        for j in range(src_nc['FR_LAND'][:].shape[1]):
            for i in range(src_nc['FR_LAND'][:].shape[2]):
                if src_nc['FR_LAND'][0,j,i] == 0.:
                    tar_nc['T_S'][0,j,i] = 290.
        #tar_nc['T_S'][:][land_mask] = 280.

        tar_nc.close()
        src_nc.close()
except IndexError:
    pass

