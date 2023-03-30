from netCDF4 import Dataset
import sys


tar_file = sys.argv[1]
tar_var = sys.argv[2]
value = float(sys.argv[3])
print(tar_file)
print(tar_var)
print(value)

print('exit. Add 4th argument = yes if you want to proceed.')
try:
    proceed = sys.argv[4]
    if proceed == "yes":
        print('proceed')

        tar_nc = Dataset(tar_file, 'a')
        print(tar_nc[tar_var][:].shape)

        tar_nc[tar_var][:] = value

        tar_nc.close()
except IndexError:
    pass

