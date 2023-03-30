#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description:    Class to process time
author:         Christoph Heim
date created:   01.07.2021
date changed:   13.04.2022
usage:          import in other scripts
"""
###############################################################################
import pandas as pd
from package.utilities import dt64_to_dt
###############################################################################

class Time_Processing:
    DIURNAL_CYCLE   = 'DIURNALCYCLE'
    ANNUAL_CYCLE    = 'ANNUALCYCLE'
    SEASONAL_CYCLE  = 'SEASONALCYCLE'
    HOURLY_SERIES   = 'HOURLY'
    DAILY_SERIES    = 'DAILY'
    MONTHLY_SERIES  = 'MONTHLY'
    YEARLY_SERIES   = 'YEARLY'
    ALL_TIME        = 'ALLTIME'
    # nl dict groups
    ACTION      = 'ACTION'
    FREQUENCY   = 'FREQUENCY'
    OPERATOR    = 'OPERATOR'
    # ACTIONS
    RESAMPLE    = 'RESAMPLE'
    GROUPBY     = 'GROUPBY'
    NONE        = 'NONE'
    # OPERATORS
    MEAN = 'MEAN'
    MIN = 'MIN'
    MAX = 'MAX'
    P25 = 'P25'
    P75 = 'P75'
    quantiles = {
        MIN:0.00,
        P25:0.25,
        P75:0.75,
        MAX:1.00,
    }

    def format_time_label(time_plt_sel):
        if time_plt_sel is not None:
            # format member label
            time_key = list(time_plt_sel.keys())[0]
            if time_key == 'month':
                months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                label = '{}'.format(months[time_plt_sel[time_key]-1])
            elif time_key == 'season':
                label = '{}'.format(time_plt_sel[time_key])
            elif time_key == 'hour':
                hours = ['{:02d}:00'.format(hr) for hr in range(23)]
                label = '{}'.format(hours[time_plt_sel[time_key]])
            elif time_key == 'time':
                label = '{:%d.%m.%Y %H:%M}'.format(dt64_to_dt(time_plt_sel[time_key]))
            else:
                raise NotImplementedError()
        else:
            label = ''
        return(label)

    def format_time_code(time_plt_sel):
        if time_plt_sel is not None:
            # format member label
            time_key = list(time_plt_sel.keys())[0]
            if time_key == 'month':
                label = '{:02d}'.format(time_plt_sel[time_key])
            elif time_key == 'season':
                numbers = {'DJF':0,'MAM':1,'JJA':2,'SON':3}
                label = '{}{}'.format(numbers[time_plt_sel[time_key]],
                                      time_plt_sel[time_key])
            elif time_key == 'hour':
                hours = ['{:02d}00'.format(hr) for hr in range(23)]
                label = '{}'.format(hours[time_plt_sel[time_key]])
            else:
                raise NotImplementedError()
        else:
            label = ''
        return(label)

    def get_agg_var_name(var_name, agg_level, agg_operator=MEAN):
        return('{}--{}--{}'.format(var_name, agg_level, agg_operator))

    def get_var_name(agg_var_name):
        return(agg_var_name.split('--')[0])

    def get_agg_level(agg_var_name):
        return(agg_var_name.split('--')[1])

    def get_agg_operator(agg_var_name):
        #try:
        #    return(int(agg_var_name.split('(')[1].split(')')[0]))
        #except ValueError:
        #    return(agg_var_name.split('(')[1].split(')')[0])
        return(agg_var_name.split('--')[2])

    def aggregate(var, agg_level, agg_operator=MEAN):
        ### DO NOT AGGREGATE TIME SERIES
        if agg_level == Time_Processing.NONE:
            out_var = var
            out_var.attrs['time_key'] = 'time'
            out_var.attrs['agg_level'] = Time_Processing.NONE

        ### COMPUTE DIURNAL CYCLE
        if agg_level == Time_Processing.DIURNAL_CYCLE:
            out_var = Time_Processing.run_aggregation_step(var, 
                  { Time_Processing.ACTION:Time_Processing.GROUPBY, 
                    Time_Processing.FREQUENCY:'H',
                    Time_Processing.OPERATOR:agg_operator })
            out_var.attrs['time_key'] = 'hour'
            out_var.attrs['agg_level'] = Time_Processing.DIURNAL_CYCLE
            out_var.attrs['agg_operator'] = agg_operator

        ### COMPUTE ANNUAL CYCLE
        if agg_level == Time_Processing.ANNUAL_CYCLE:
            # first compute monthly mean values
            out_var = Time_Processing.run_aggregation_step(var, 
                  { Time_Processing.ACTION:Time_Processing.RESAMPLE, 
                    Time_Processing.FREQUENCY:'M', 
                    Time_Processing.OPERATOR:Time_Processing.MEAN })
            #print(out_var.values)
            #print(out_var.time)
            # then group by years
            out_var = Time_Processing.run_aggregation_step(out_var, 
                  { Time_Processing.ACTION:Time_Processing.GROUPBY, 
                    Time_Processing.FREQUENCY:'M',
                    Time_Processing.OPERATOR:agg_operator })
            #print(out_var)
            #quit()
            out_var.attrs['time_key'] = 'month'
            out_var.attrs['agg_level'] = Time_Processing.ANNUAL_CYCLE
            out_var.attrs['agg_operator'] = agg_operator
            #print(out_var)
            #quit()

        ### COMPUTE SEASONAL CYCLE
        if agg_level == Time_Processing.SEASONAL_CYCLE:
            # first compute seasonal mean values
            out_var = Time_Processing.run_aggregation_step(var, 
                  { Time_Processing.ACTION:Time_Processing.RESAMPLE, 
                    Time_Processing.FREQUENCY:'QS-DEC', 
                    Time_Processing.OPERATOR:Time_Processing.MEAN })
            # then group by years
            out_var = Time_Processing.run_aggregation_step(out_var, 
                  { Time_Processing.ACTION:Time_Processing.GROUPBY, 
                    Time_Processing.FREQUENCY:'QS-DEC',
                    Time_Processing.OPERATOR:agg_operator })
            out_var.attrs['time_key'] = 'season'
            out_var.attrs['agg_level'] = Time_Processing.SEASONAL_CYCLE
            out_var.attrs['agg_operator'] = agg_operator

        ### RESAMPLE HOURLY
        if agg_level == Time_Processing.HOURLY_SERIES:
            # this is already done on basis of daily routines
            out_var = Time_Processing.run_aggregation_step(var, 
                  { Time_Processing.ACTION:Time_Processing.RESAMPLE, 
                    Time_Processing.FREQUENCY:'H', 
                    Time_Processing.OPERATOR:agg_operator }) 
            out_var.attrs['time_key'] = 'time'
            out_var.attrs['agg_level'] = Time_Processing.HOURLY_SERIES
            out_var.attrs['agg_operator'] = agg_operator


        ### RESAMPLE DAILY
        if agg_level == Time_Processing.DAILY_SERIES:
            # this is already done on basis of daily routines
            out_var = var
            out_var.attrs['time_key'] = 'time'
            out_var.attrs['agg_level'] = Time_Processing.DAILY_SERIES
            out_var.attrs['agg_operator'] = agg_operator

        ### RESAMPLE MONTHLY
        if agg_level == Time_Processing.MONTHLY_SERIES:
            #print(var.values)
            #print(var.time)
            out_var = Time_Processing.run_aggregation_step(var, 
                  { Time_Processing.ACTION:Time_Processing.RESAMPLE, 
                    Time_Processing.FREQUENCY:'M', 
                    Time_Processing.OPERATOR:agg_operator })
            #print(out_var.values)
            #print(out_var.time)
            #quit()
            out_var.attrs['time_key'] = 'time'
            out_var.attrs['agg_level'] = Time_Processing.MONTHLY_SERIES
            out_var.attrs['agg_operator'] = agg_operator

        ### RESAMPLE YEARLY
        if agg_level == Time_Processing.YEARLY_SERIES:
            out_var = Time_Processing.run_aggregation_step(var, 
                  { Time_Processing.ACTION:Time_Processing.RESAMPLE, 
                    Time_Processing.FREQUENCY:'Y', 
                    Time_Processing.OPERATOR:agg_operator })
            out_var.attrs['time_key'] = 'time'
            out_var.attrs['agg_level'] = Time_Processing.YEARLY_SERIES
            out_var.attrs['agg_operator'] = agg_operator

        ### AGGREGATE FULL TIME SERIES
        if agg_level == Time_Processing.ALL_TIME:
            out_var = Time_Processing.run_aggregation_step(var, 
                  { Time_Processing.ACTION:Time_Processing.RESAMPLE, 
                    Time_Processing.FREQUENCY:None, 
                    Time_Processing.OPERATOR:agg_operator })
            out_var.attrs['time_key'] = 'None'
            out_var.attrs['agg_level'] = Time_Processing.ALL_TIME
            out_var.attrs['agg_operator'] = agg_operator

        return(out_var)



    def run_aggregation_step(var, command):
        """
        Organize temporal resampling and grouping of var.
        """
        attrs = var.attrs
        if command[Time_Processing.ACTION] == Time_Processing.RESAMPLE:
            var = Time_Processing.resample(var, 
                                command[Time_Processing.FREQUENCY],
                                command[Time_Processing.OPERATOR])
        elif command[Time_Processing.ACTION] == Time_Processing.GROUPBY:
            var = Time_Processing.groupby(var, 
                                command[Time_Processing.FREQUENCY],
                                command[Time_Processing.OPERATOR])
        elif command[Time_Processing.ACTION] == Time_Processing.NONE:
            pass
        else:
            raise NotImplementedError()
        if isinstance(var, dict):
            for key,value in var.items():
                var[key].attrs = attrs
        else:
            var.attrs = attrs
        return(var)
            
    def resample(var, frequency, operator):
        """
        Temporal resampling of var.
        - frequency == None: Average entire time series
        """
        # make sure that files starting at e.g. 01:00 and ending at
        # 00:00 of the next day (which makes sense for daily files
        # containing mean values as the time stamp is valid backwards)
        # do not end up in two dates (this and the next one) after
        # resampling to daily mean values.
        #print(var.time)
        nts = len(var.time)
        if frequency is not None:
            if ( ('D' in frequency) and
                 (dt64_to_dt(var.time.values[0]).hour*60 + 
                  dt64_to_dt(var.time.values[0]).minute > 0 and 
                  dt64_to_dt(var.time.values[-1]).hour == 0) ):
                var = var.assign_coords(time=var.time-pd.Timedelta(10,'min'))
        if operator == Time_Processing.MEAN:
            #var = var.resample({'time':'24H'}, base=1).mean(dim='time')
            # resample and drop all fully nan-entries which may have been
            # generated by resampler if there are gaps in the time series
            # that are larger than the resampling frequency.
            if frequency is not None:
                var = var.resample({'time':frequency}).mean(
                                dim='time').dropna(dim='time', how='all')
            # if frequency is None, just average entire time series
            else:
                var = var.mean(dim='time')
        else:
            raise NotImplementedError()
        #print(var.time)
        #quit()
        ## make sure we do not end up with more time steps than before
        ## (sanity check for exceptional cases like the one above)
        #if len(var.time) > nts:
        #    print('old was {} and new is {}'.format(nts, len(var.time)))
        #    raise ValueError()
        return(var)

    def groupby(var, frequency, operator, add_empty=True):
        """
        Temporal grouping and then perform an operation across groups.
        """
        # get correct command for pandas
        # (could probably be done easier..)
        if frequency == 'Y':
            grp_cmnd = 'time.year'
        elif frequency == 'QS-DEC':
            grp_cmnd = 'time.season'
        elif frequency == 'M':
            grp_cmnd = 'time.month'
        elif frequency == 'YD':
            grp_cmnd = 'time.dayofyear'
        elif frequency == 'D':
            grp_cmnd = 'time.day'
        elif frequency == 'H':
            grp_cmnd = 'time.hour'
        else:
            raise NotImplementedError()

        if operator == Time_Processing.MEAN:
            var = var.groupby(grp_cmnd).mean(dim='time')
        # compute percentiles
        elif operator in [Time_Processing.MIN,Time_Processing.MAX,
                          Time_Processing.P25,Time_Processing.P75]:
            var = var.groupby(grp_cmnd).quantile(
                        Time_Processing.quantiles[operator], dim='time')
        elif operator == None:
            var_grps = var.groupby(grp_cmnd)
            # separate each group individually in var dict.
            var = {}
            for key,val in var_grps:
                var[key] = val
        else:
            print('Error: Operator {} not implemented.'.format(operator))
            raise NotImplementedError()
        return(var)

# convert to static method
Time_Processing.aggregate = staticmethod(Time_Processing.aggregate)






if __name__ == '__main__':
    pass
