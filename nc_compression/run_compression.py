#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description:    Compress COSMO model output using the tool nczip by Urs Beyerle
author:         Christoph Heim
date created:   09.04.2020
date changed:   23.11.2021
Usage:
1) Set base directory variable (work_dir in namelist.py).
2) prepare batch job in submit.sbatch by adjusting the input arguments.
    1st:    number of workers for parallel execution
    2nd:    first subdirectory (e.g. name of simulation) 
    3rd:    second subdirectory (for COSMO output group)
3) submit batch job.
"""
###############################################################################
import os, subprocess, glob
from pathlib import Path
from datetime import datetime
from multiproc import IterMP 
from timer import Timer
import namelist as nl
###############################################################################

def compress_file(file,
                 run_compression=True, run_coarse_grain=False,
                 lossy=False, verbous=False, weights_file_path=None):
    """
    Compress NC files using the tool nczip by Urs Beyerle (IAC).
    Compress files either in a conserving way or in a lossy way.
    Conserving means that files can be uncompressed back without information
    loss.
    Lossy means that in addition to the compression, the data type of the
    fields stored in the NC files are converted to "short" datatype. 
    (this only applies to the fields, not to the dimensions).
    Compared to the COSMO output datatype float, this
    saves additional 50% of disk space. However, the values of the
    field are mapped to the short datatype value range (64K representations)
    based on the maximum and minimum value of the field. This is done for
    each file separately. Thus, if the max/min of the time series changes
    from file to file, this introduces a substantial error. Due to this,
    I would not recommend applying lossy compression to the raw COSMO model
    output.
    #########################################################################
    args:
        file    (string)    file to compress (file is overwritten)
        lossy   (boolean)   False: apply conserving compression
                            True: apply lossy compression
        verbous (boolean)   True: print nczip debug output
    """
    print(file)

    ### coarse grain if grid file is given
    if weights_file_path is not None:
        print('coarse grain')

        # rename file to temporary file
        bash_command = 'mv {} {}.tmp'.format(file, file)
        process = subprocess.Popen(bash_command.split(),
                                    stdout=subprocess.PIPE)
        output, error = process.communicate()

        # coarse grain
        #bash_command = 'cdo remap,{},{} {}.tmp {}'.format(
        # TODO test for various cases if -delvar,vcoord works in general
        bash_command = 'cdo -L remap,{},{} -delvar,vcoord {}.tmp {}'.format(
            nl.cg_trg_grid, weights_file_path, file, file)
        process = subprocess.Popen(bash_command.split(),
                                    stdout=subprocess.PIPE)
        output, error = process.communicate()

        # delete temporary file
        bash_command = 'rm {}.tmp'.format(file)
        process = subprocess.Popen(bash_command.split(),
                                    stdout=subprocess.PIPE)


    ### apply compression
    if run_compression:
        if verbous:
            vflag = '-v'
        else:
            vflag = '-q'
        if lossy:
            subprocess.call(['nczip', vflag, '-p', file],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.STDOUT)
        else:
            subprocess.call(['nczip', vflag, '-1', file],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.STDOUT)




if __name__ == '__main__':

    # initialize Timer instance
    timer = Timer(mode='seconds') 

    # initialize instance of multiprocessing helper class 
    itermp = IterMP(njobs=nl.n_par, run_async=nl.run_async)

    # loop over cosmo output groups of simulation
    for output_group in nl.output_groups:
        print('##### COSMO output group {} \t #####'.format(output_group))
        timer.start(output_group)

        # construct directory path
        data_dir = os.path.join(nl.work_dir, nl.sim_name, 
                                output_group, str(nl.first_date.year))

        # check if path exists
        if not os.path.exists(data_dir):
            raise ValueError('Path does not exist: {}'.format(data_dir))

        # find all files in directory
        #files = glob.glob(os.path.join(data_dir,'lffd{:%Y%m}*.nc'.format(
        #                    nl.first_date)))
        files = glob.glob(os.path.join(data_dir,'lffd*.nc'))

        files.sort()

        # only select files within time period
        sel_files = []
        for file in files:
            if len(Path(file).name.split('z')) == 1:
                file_date = datetime.strptime(Path(file).name, 'lffd%Y%m%d%H%M%S.nc')
            elif len(Path(file).name.split('z')) == 2:
                file_date = datetime.strptime(Path(file).name, 'lffd%Y%m%d%H%M%Sz.nc')
            #print(file_date)
            if (file_date >= nl.first_date) and (file_date <= nl.last_date):
                sel_files.append(file)

        sel_files.sort()
        print(sel_files)
        #quit()

        # function arguments that are constant accross subtasks
        const_args = {
            'run_compression':  nl.args.run_compression,
            'lossy':            nl.run_lossy,
            'verbous':          nl.run_verbous,
        }
        if nl.args.run_coarse_grain and (output_group in nl.coarse_grain_groups):
            if nl.coarse_grain_groups[output_group]:

                # weights file
                weights_file_path = os.path.join(nl.work_dir, nl.sim_name, 
                                                output_group, 'weights.nc')
                # exemplary input file to compute weights
                inp_file_path = sel_files[0]

                ### compute weights
                if not os.path.exists(weights_file_path):
                    print('compute weights')
                    #bash_command = 'cdo gencon,{} -setgrid,{} {} {}'.format(
                    # TODO test for various cases if -delvar,vcoord works in general
                    bash_command = 'cdo -L gencon,{} -setgrid,{} -delvar,vcoord {} {}'.format(
                                    nl.cg_trg_grid, nl.cg_src_grid, 
                                    inp_file_path, weights_file_path)
                    process = subprocess.Popen(bash_command.split(),
                                                stdout=subprocess.PIPE)
                    output, error = process.communicate()
                    #quit()
                    print('compute weights completed')

                const_args['weights_file_path'] = weights_file_path 

        #quit()

        # function arguments specific to each subtask
        step_args = []
        for file in sel_files:
            step_args.append({'file':file})

        # run job in parallel
        itermp.run(compress_file, const_args, step_args)

        timer.stop(output_group)

    timer.print_report()

