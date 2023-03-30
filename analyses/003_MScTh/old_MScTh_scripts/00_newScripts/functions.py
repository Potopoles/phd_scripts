import numpy as np
import pickle
def unstaggerZ_4D(var):
    nt,nzs,ny,nx = var.shape
    unst = np.full((nt,nzs-1,ny,nx), np.nan)
    for k in range(0,nzs-1):
        unst[:,k,:,:] = 0.5*(var[:,k+1,:,:] + var[:,k,:,:])
    return(unst)

def unstaggerZ_1D(var):
    nzs, = var.shape
    unst = np.full((nzs-1), np.nan)
    for k in range(0,nzs-1):
        unst[k] = 0.5*(var[k+1] + var[k])
    return(unst)

def loadObj(folder, name):
    with open(folder + '/' + name + '.pkl', 'rb') as f:
        return(pickle.load(f))

def saveObj(obj, folder, name):
    with open(folder + '/' + name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
