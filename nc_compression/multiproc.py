#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    Class for parallel computing and loading of time step files.
author			Christoph Heim
date created    21.03.2019
date changed    09.04.2020
usage			use in another script
"""
###############################################################################
import sys, time
import multiprocessing as mp
import xarray as xr
import numpy as np
from datetime import datetime,timedelta
###############################################################################

def starmap_helper(tup):
    func = tup['func']
    del tup['func']
    return(func(**tup))


def run_starmap(func, fargs={}, njobs=1, run_async=False):
    outputs = []
    if njobs > 1:
        pool = mp.Pool(processes=njobs)
        if run_async:
            outputs = pool.starmap_async(starmap_helper, fargs).get()
        else:
            outputs = pool.starmap(starmap_helper, fargs)
        pool.close()
        pool.join()
    else:
        for i in range(len(fargs)):
            out = func(**fargs[i])
            outputs.append(out)
    return(outputs)



class IterMP:

    def __init__(self, njobs=None, run_async=False):
        self.run_async = run_async

        if njobs is None:
            if len(sys.argv) > 1:
                self.njobs = int(sys.argv[1])
            else:
                self.njobs = 1
        else:
            self.njobs = njobs
        #print('IterMP: njobs = '+str(self.njobs))

        self.output = None


    def run(self, func, fargs={}, step_args=None):
        outputs = []

        input = []
        for tI in range(len(step_args)):
            this_fargs = fargs.copy()
            if step_args is not None:
                this_fargs.update(step_args[tI])

            if self.njobs > 1:
                this_fargs['func'] = func
                this_fargs = (this_fargs,)
            input.append(this_fargs)

        self.output = run_starmap(func, fargs=input,
                        njobs=self.njobs, run_async=self.run_async) 



def test_IterMP(iter_arg, const_arg):
    print(str(iter_arg) + ' ' + str(const_arg))
    return(iter_arg/10)



if __name__ == '__main__':


    # first argument: number of jobs
    if len(sys.argv) > 1:
        njobs = int(sys.argv[1])
    else:
        njobs = 1
    
    IMP = IterMP(njobs=njobs, run_async=False)
    fargs = {'const_arg':'constant argument for all tasks',}
    step_args = []
    for i in range(20):
        step_args.append({'iter_arg':i})
    IMP.run(test_IterMP, fargs, step_args)
    print(IMP.output)

