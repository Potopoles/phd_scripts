import numpy as np
import os
from math import log10, floor
import pickle

def round_sig(x, sig=2):
    out = []
    for val in x:
        rounded = str(round(val, sig-int(floor(log10(abs(val))))-1))
        out.append(rounded)
    return out

#### OLD UNUSED FUNCTIONS, I GUESS


def calcDiurnalCycleVertProfile(field):
	"""Calculate the diurnal cycle of the field (assuming dim 0 is time and data hourly)"""
	diurnal = np.full( ((24,) + field.shape[1:]), np.nan)
	hr0Inds = np.arange(0,9*24,24)
	hrs = np.arange(0,24)
	for hr in hrs:
		hrInds = hr0Inds + hr
		diurnal[hr,:] = np.average(field[hrInds,:],0)
	return(diurnal)
	
	
def timeseries(start, end, delta):
	from datetime import datetime, timedelta
	out = []
	curr = start
	while curr <= end:
		out.append(curr)
		curr += delta
	return(out)
	
def usedMem():
	"""Prints the currently used memory"""
	tot_m, used_m, free_m = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
	return(used_m)

def loadObj(folder, name):
    with open(folder + '/' + name + '.pkl', 'rb') as f:
        return(pickle.load(f))

def saveObj(obj, folder, name):
    with open(folder + '/' + name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

	
