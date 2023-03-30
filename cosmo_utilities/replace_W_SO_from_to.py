from netCDF4 import Dataset
import sys


src_file = sys.argv[1]
tar_file = sys.argv[2]
print(src_file)
print(tar_file)

print('exit. Add 3rd argument = yes if you want to proceed.')
try:
    proceed = sys.argv[3]
    if proceed == "yes":
        print('proceed')

        tar_nc = Dataset(tar_file, 'a')
        src_nc = Dataset(src_file, 'r')
        print(tar_nc['W_SO'][:].shape)
        print(src_nc['W_SO'][:].shape)

        tar_nc['W_SO'][:] = src_nc['W_SO'][:]

        tar_nc.close()
        src_nc.close()
except IndexError:
    pass

