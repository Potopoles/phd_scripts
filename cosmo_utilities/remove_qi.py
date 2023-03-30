from netCDF4 import Dataset
import os, sys, glob


folder='/scratch/snx3000/heimc/lmp/wd/16080100_SA_4_2/lm_coarse'
tar_var = 'QI'
value = 0.

for file in glob.glob(os.path.join(folder, 'lffd*')):
    #path = os.path.join(folder,file)

    print(file)

    tar_nc = Dataset(file, 'a')
    print(tar_nc[tar_var][:].shape)

    tar_nc[tar_var][:] = value

    tar_nc.close()

    #quit()
