#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description:    Functions to preprocess models on daint.
author:         Christoph Heim
date created:   11.03.2020
date changed:   07.04.2022
usage:          import in pp scripts
"""
###############################################################################
import os, subprocess, glob
import xarray as xr
from datetime import datetime, timedelta
from package.utilities import dt64_to_dt, Timer
#from cdo import Cdo
###############################################################################

#cdo = Cdo()

def ARPEGE_fix_timeaxis(ts, inp_native_dir, var_name):
    #######################
    # special fix of broken time axis for ARPEGE-NH
    time_deltas = {
        180:['QV', 'QC', 'T', 'W', 'U', 'V', 'H', 'P'],
        30:['U10M', 'V10M', 'T2M', 'PS', 'MSLP', 
             'LWUTOA', 'SWNDTOA', 'SWDTOA', 'SWUTOA',
             'SST', 'SLHFLX', 'SSHFLX',
             'TQC', 'TQI', 'TQV',
             'CLCL', 'CLCT', 'PP', 'PPCONV', 'PPGRID'],
    }
    time_delta_min = -999999
    for time_delta,var_names in time_deltas.items():
        if var_name in var_names:
            time_delta_min = time_delta
    if time_delta_min == -999999:
        raise NotImplementedError()

    src_files = glob.glob(os.path.join(inp_native_dir,
                            '{}_{:%Y%m%d}*.nc'.format(var_name, ts)))
    for file in src_files:
        tmp_file = '{}.tmp'.format(file)
        dt = datetime.strptime(os.path.split(file)[-1].split('_')[-1][:-3],
                                '%Y%m%d%H%M')
        #print(dt)
        command = ['cdo', 'settaxis,{:%Y-%m-%d},{:%H:%M:%S},{}min'.format(
                    dt, dt, time_delta_min), file, tmp_file]
        subprocess.call(command,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT)
        command = ['mv', tmp_file, file]
        subprocess.call(command,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT)
    #######################



#def NICAM_fix_timeaxis(ts, inp_native_dir, var_name):
#    #######################
#    # special fix of broken time axis for ARPEGE-NH
#    time_deltas = {
#        15:['TQI'],
#    }
#    time_delta_min = -999999
#    for time_delta,var_names in time_deltas.items():
#        if var_name in var_names:
#            time_delta_min = time_delta
#    if time_delta_min == -999999:
#        raise NotImplementedError()
#
#    src_files = glob.glob(os.path.join(inp_native_dir,
#                            '{}_{:%Y%m%d}*.nc'.format(var_name, ts)))
#    for file in src_files:
#        tmp_file = '{}.tmp'.format(file)
#        dt = datetime.strptime(os.path.split(file)[-1].split('_')[-1][:-3],
#                                '%Y%m%d')
#        command = ['cdo', 'settaxis,{:%Y-%m-%d},{:%H:%M:%S},{}min'.format(
#                    dt, dt, time_delta_min), file, tmp_file]
#        subprocess.call(command,
#                        stdout=subprocess.DEVNULL,
#                        stderr=subprocess.STDOUT)
#        command = ['mv', tmp_file, file]
#        subprocess.call(command,
#                        stdout=subprocess.DEVNULL,
#                        stderr=subprocess.STDOUT)
#    #######################



def run_merge_day(ts, inp_native_dir, out_daily_dir, var_name, i_overwrite_daily=True):
    timer = Timer()
    timer.start('merge')
    #print(ts)
    src_files = glob.glob(os.path.join(inp_native_dir,
                            '{}_{:%Y%m%d}*.nc'.format(var_name, ts)))
    # add preceeding day (just to be sure..)
    src_files.extend(glob.glob(os.path.join(inp_native_dir,
                            '{}_{:%Y%m%d}*.nc'.format(var_name,
                                                        ts+timedelta(days=1)))))
    # add next day (to ensure 00:30 - next day 00:00 is possible)
    src_files.extend(glob.glob(os.path.join(inp_native_dir,
                            '{}_{:%Y%m%d}*.nc'.format(var_name,
                                                        ts-timedelta(days=1)))))
    tmp_out_file = os.path.join(out_daily_dir,
                            '{}_{:%Y%m%d}.nc.cdo'.format(var_name, ts))
    out_file = os.path.join(out_daily_dir,
                            '{}_{:%Y%m%d}.nc'.format(var_name, ts))

    # quit here if output file already exists and should not be overwritten
    if (not i_overwrite_daily) and os.path.exists(out_file):
        print('file {}_{:%Y%m%d}.nc exists already. skip.'.format(var_name, ts))
        timer.stop('merge')
        output = {'timer':timer}
        return(output)

    if len(src_files) > 0:
        #cdo.mergetime(input=src_files, output=tmp_out_file)
        cmd = ['cdo', '-O', 'mergetime']
        cmd.extend(src_files)
        cmd.append(tmp_out_file)
        subprocess.call(cmd)

        # check if there are time steps for this date
        with xr.open_dataset(tmp_out_file) as f:
            dts = f.time
        nts = 0
        for ti,dt64 in enumerate(dts):
            dt = dt64_to_dt(dt64.values)
            if (dt >= ts+timedelta(minutes=15)) and (dt <= ts+timedelta(days=1)):
                nts += 1
        #print('done')
        #quit()
        # if there are time steps, select only these
        if nts > 0:
            command_str = ["ncrcat", "-O", "-d",
                           r"time,{:%Y-%m-%d %H:%M:%S},{:%Y-%m-%d}".format(
                           ts+timedelta(minutes=15), ts+timedelta(days=1))]
            command_str.append(tmp_out_file)
            command_str.append(out_file)
            subprocess.call(command_str)
            os.remove(tmp_out_file)
        else:
            os.remove(tmp_out_file)
            print('\t\t\tWARN: merge: no sub-daily files for date {:%Y%m%d}.'.format(ts))
        # else delete this date
    else:
        pass
        print('\t\t\tWARN: merge: no sub-daily files for date {:%Y%m%d}.'.format(ts))
    timer.stop('merge')
    output = {'timer':timer}
    return(output)


def ncrcat_date_together(directory, date, var_name):
    timer = Timer()
    timer.start('orderts')
    # see if files of dates surrounding the desired date exist
    file_name = '{}_{:%Y%m%d}.nc'.format(var_name, date)
    file_path = os.path.join(directory, file_name)
    check_dates = [date - timedelta(days=1), date, date + timedelta(days=1)]
    check_files = []
    for check_date in check_dates:
        check_file = os.path.join(directory, 
                    '{}_{:%Y%m%d}.nc'.format(var_name, check_date))
        if os.path.exists(check_file):
            check_files.append(check_file)
    command_str = ["ncrcat", "-O", "-d",
                   r"time,{:%Y-%m-%d %H:%M:%S},{:%Y-%m-%d}".format(
                   date+timedelta(minutes=15), date+timedelta(days=1))]
    command_str.extend(check_files)
    command_str.append(file_path)
    subprocess.call(command_str)
    timer.stop('orderts')
    output = {'timer':timer}
    return(output)


def delete_15min_time_steps(ts, directory, var_name):
    timer = Timer()
    timer.start('del15')
    file_name = '{}_{:%Y%m%d}.nc'.format(var_name, ts)
    file_path = os.path.join(directory, file_name)
    if os.path.exists(file_path):
        # find indices with not 15/45 minute time values
        with xr.open_dataset(file_path) as f:
            dts = f.time
        delete_inds = []
        for ti,dt in enumerate(dts):
            min = dt64_to_dt(dt.values).minute
            if min in [15, 45]:
                delete_inds.append(ti+1)

        if len(delete_inds) > 0:
            # remove others
            tmp_file = '{}.tmp'.format(file_path)
            delete_inds_str = str(delete_inds)[1:-1].replace(' ', '')
            command_str = ["cdo", "delete,timestep={}".format(delete_inds_str),
                           file_path, tmp_file]
            subprocess.call(command_str, stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL)
            command_str = ["mv", tmp_file, file_path]
            subprocess.call(command_str)
    else:
        pass
        #print('\t\t\tWARN: 15min: no file for date {:%Y%m%d}.'.format(ts))
    timer.stop('del15')
    output = {'timer':timer}
    return(output)



def run_sellonlat(ts, inp_daily_dir, out_daily_dir, var_name,
                 out_domain):
    timer = Timer()
    timer.start('selbox')
    inp_file = os.path.join(inp_daily_dir,
                            '{}_{:%Y%m%d}.nc'.format(var_name, ts))
    out_file = os.path.join(out_daily_dir,
                            '{}_{:%Y%m%d}.nc'.format(var_name, ts))
    if os.path.exists(inp_file):
        cdo.sellonlatbox(out_domain['lon'].start,
                         out_domain['lon'].stop,
                         out_domain['lat'].start,
                         out_domain['lat'].stop, 
                         input=inp_file, output=out_file)
    else:
        pass
        #print('\t\t\tWARN: box: no file for date {:%Y%m%d}.'.format(ts))
    timer.stop('selbox')
    output = {'timer':timer}
    return(output)


