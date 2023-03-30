#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    Class for parallel computing and loading of time step files.
author			Christoph Heim
date created    21.03.2019
date changed    04.04.2021
usage			use in another script
"""
###############################################################################
import sys, time
import multiprocessing as mp
import xarray as xr
import numpy as np
from datetime import datetime,timedelta
from package.member import Member
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



class TimeStepMP:

    def __init__(self, timesteps, njobs=None, run_async=False):
        self.timesteps = timesteps
        self.run_async = run_async

        if njobs is None:
            if len(sys.argv) > 1:
                self.njobs = int(sys.argv[1])
            else:
                self.njobs = 1
        else:
            self.njobs = njobs
        #print('TimeStepMP: njobs = '+str(self.njobs))

        self.output = None


    def run(self, func, fargs={}, step_args=None):
        outputs = []

        input = []
        for tI,ts in enumerate(self.timesteps):
            this_fargs = fargs.copy()
            this_fargs['ts'] = ts
            if step_args is not None:
                this_fargs.update(step_args[tI])

            if self.njobs > 1:
                this_fargs['func'] = func
                this_fargs = (this_fargs,)
            input.append(this_fargs)

        self.output = run_starmap(func, fargs=input,
                        njobs=self.njobs, run_async=self.run_async) 
        

    def concat_timesteps(self):
        if (self.output is not None):
            mem_keys = list(self.output[0]['members'].keys())
            var_names = list(self.output[0]['members'][mem_keys[0]].vars.keys())
            concat_members = {}
            #for mem_key in mem_keys:
            #    print(mem_key)
            #    i = 0
            #    while not hasattr(self.output[i]['members'][mem_key], 'mem_dict'):
            #        i += 1
            #    print(self.output[i]['members'][mem_key].mem_dict)
            #quit()
            for mem_key in mem_keys:
                i = 0
                while not hasattr(self.output[i]['members'][mem_key], 'mem_dict'):
                    #print(hasattr(self.output[i]['members'][mem_key], 'mem_dict'))
                    i += 1
                mem_dict = self.output[i]['members'][mem_key].mem_dict
                val_type = self.output[i]['members'][mem_key].val_type
                concat_member = Member(mem_dict, val_type=val_type)
                for var_name in var_names:
                    #print(var_name)
                    var_steps = []
                    # go through each date and append data if available
                    for time_step in self.output:
                        #print(time_step)
                        member_in = time_step['members'][mem_key]
                        # if member contains data for this date
                        if member_in.vars[var_name] is not None:
                            var_steps.append(member_in.vars[var_name])

                    # if data available concatenate
                    if len(var_steps) > 0:
                        var_all = xr.concat(var_steps, dim='time')
                    # if no data available set var to None
                    else:
                        var_all = None
                    concat_member.add_var(var_name, var_all)

                ## check if member has any data
                #member_has_data = False
                #for var_name in var_names:
                #    if concat_member.vars[var_name] is not None:
                #        member_has_data = True
                #if member_has_data:
                #    concat_members[mem_key] = concat_member

                concat_members[mem_key] = concat_member

            self.concat_output = {'members':concat_members}
        else:
            print('TimeStepWise: No values calculated')



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
        print('IterMP: njobs = '+str(self.njobs))

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
        




def test_IMP(iter_arg, fixed_arg):
    #print(str(iter_arg) + ' ' + str(fixed_arg))
    work = []
    for i in range(int(1E7)):
        work.append(1)
    return(iter_arg)

def test_TSMP(ts, task_no, test_arg):
    #print(str(ts) + ' ' + str(task_no) + ' ' + test_arg)
    return(task_no)



if __name__ == '__main__':


    if len(sys.argv) > 1:
        njobs = int(sys.argv[1])
    else:
        njobs = 1
    
    # TEST TSMP
    timesteps = np.arange(datetime(2015,1,1,1), datetime(2015,1,1,5),
                        timedelta(hours=1))
    TSMP = TimeStepMP(timesteps, njobs=njobs, run_async=False)
    fargs = {'test_arg':'test',}
    step_args = []
    for i,dt in enumerate(timesteps):
        step_args.append({'task_no':i})
    TSMP.run(test_TSMP, fargs, step_args)
    print(TSMP.output)

    # TEST BASE 
    t0 = time.time()
    IMP = IterMP(njobs=njobs, run_async=False)
    fargs = {'fixed_arg':'fixed',}
    step_args = []
    for i in range(20):
        step_args.append({'iter_arg':i})
    IMP.run(test_IMP, fargs, step_args)
    print(IMP.output)
    t1 = time.time()
    print(t1 - t0)

