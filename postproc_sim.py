#!/usr/bin/env python

import argparse#, os, shutil, stat, subprocess, getpass, json

if __name__ == '__main__':

    #---------------------------------------------------------------------------
    # Parse arguments
    #
    parser = argparse.ArgumentParser(description = "Extract, compress, and" +
                                                    " store cosmo output.")
    parser.add_argument('-j', '--jobs', type=str, default='ect',
        help="List of jobs. Default all.")
    #parser.add_argument('-s', '--src', type=str, required=True,
    #    help="Source directory.")
    #parser.add_argument('-d', '--dst', type=str, default=None,
    #    help="Destination directory.")
    parser.add_argument('-w', '--wait', type=str, default=None,
        help="Job dependency.")
    #parser.add_argument('-a', '--account', type=str, default='pr94',
    #    help="Allocation account.")
    #parser.add_argument('-n', '--jobName', type=str, default='storeData',
    #    help="Job name.")
    #parser.add_argument('-o', '--overwrite', type=bool, default=False,
    #    help="Overwrite existing files.")
    args = parser.parse_args()


    if 't' in args.jobs:
        print('Submitting data transfer job...')
        elif (args.wait is not None):
            # wait until the simulation is over
            dependencies = '--dependency=afterok'
            dependencies += ':' + str(args.wait)
        else:
            dependencies = '--comment="comment"'
        sbatch = [
            'sbatch',
            '--account=' + account,
            '--job-name=T' + args.jobName,
            dependencies,
            'transfer.job',
            '-s ' + source,
            '-d ' + destin
            ]
        print('\t' + ' '.join(sbatch))
        job3 = subprocess.run(sbatch, stdout=subprocess.PIPE)
        job3ID = int(job3.stdout.split()[-1])
        print('\tsubmitted with ID: {0:d}'.format(job3ID))
