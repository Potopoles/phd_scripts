#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description:    Timer Class
author:         Christoph Heim
date created:   27.06.2019
date changed:   09.04.2020
usage:          import in other scripts
"""
###############################################################################
import time
import numpy as np
from datetime import datetime, timedelta
###############################################################################

class Timer:
    
    TOTAL_CPU_TIME  = 'tot_cpu'
    REAL_TIME       = 'total'
    
    def __init__(self, mode='minutes', parallel=False):
        self.mode = mode
        self.parallel = parallel

        self.timings = {self.TOTAL_CPU_TIME:0.}
        self.flags = {self.TOTAL_CPU_TIME:None}

        # start real total computation time timer.
        self.start(self.REAL_TIME)


    def start(self, timer_key):
        """
        Start timer with key timer_key.
        Also start TOTAL_CPU_TIME timer if not already running.
        """
        # start TOTAL_CPU_TIME timer
        if self.flags[self.TOTAL_CPU_TIME] is None:
            self.flags [self.TOTAL_CPU_TIME] = time.time()
        # start timer_key timer
        if timer_key not in self.timings.keys():
            self.timings[timer_key] = 0.
        else:
            if self.flags[timer_key] is not None:
                print('Caution: Timer', timer_key, 'already running')
        self.flags[timer_key] = time.time()

    def stop(self, timer_key):
        """
        Stop timer with key timer_key.
        Also stop TOTAL_CPU_TIME timer if timer_key is the only running task
        """
        if (timer_key not in self.flags.keys()
            or self.flags[timer_key] is None):
            raise ValueError('No time measurement in progress for timer ' +
                            str(timer_key) + '.')

        self.timings[timer_key] += time.time() - self.flags[timer_key]
        self.flags[timer_key] = None

        # Check if any other timer is running. If not, stop TOTAL_CPU_TIME timer
        other_timers_running = False
        for key,flag in self.flags.items():
            if key not in [self.TOTAL_CPU_TIME, self.REAL_TIME]:
                if flag is not None:
                    other_timers_running = True
        if not other_timers_running:
            self.timings[self.TOTAL_CPU_TIME] += (time.time() - 
                                            self.flags[self.TOTAL_CPU_TIME])
            self.flags[self.TOTAL_CPU_TIME] = None

    def merge_timings(self, Timer):
        """
        Merge timings from parallel execution Timer instances into this timer.
        """
        for timer_key in Timer.flags.keys():
            if ( (timer_key in self.timings.keys()) and 
                 (timer_key != self.REAL_TIME) ):
                self.timings[timer_key] += Timer.timings[timer_key]
            else:
                self.timings[timer_key] = Timer.timings[timer_key]

    def print_report(self, short=False):

        timer_key = self.REAL_TIME
        self.timings[timer_key] += time.time() - self.flags[timer_key]
        self.flags[timer_key] = None

        n_decimal_perc = 0
        n_decimal_sec = 1
        n_decimal_min = 2
        cpu_time = max(0.00001,self.timings[self.TOTAL_CPU_TIME])
        real_time = max(0.00001,self.timings[self.REAL_TIME])

        # shorten labels of different timings for nice printing
        max_len = 7
        new_timings = {}
        for key,value in self.timings.items():
            if len(key) > max_len:
                key = key[(len(key)-max_len):]
                new_timings[key] = value
            else:
                new_timings[key] = value
        self.timings = new_timings

        if not short:
            if self.mode == 'minutes':
                print('##########################################################')
                print('Took ' + str(np.round(real_time/60,n_decimal_min))
                      + ' min.')
                print('Detailed process times (cpu time, not real time):')
                for key,value in self.timings.items():
                    if key != self.REAL_TIME:
                        print(key + '\t' + 
                            str(np.round(100*value/cpu_time,n_decimal_perc)) +
                        '\t%\t' + str(np.round(value/60,n_decimal_min)) + ' \tmin')
            elif self.mode == 'seconds':
                print('##########################################################')
                print('Took ' + str(np.round(real_time,n_decimal_sec)) + ' sec.')
                print('Detailed process times (cpu time, not real time):')
                for key,value in self.timings.items():
                    if key != self.REAL_TIME:
                        print(key + '\t' + 
                            str(np.round(100*value/cpu_time,n_decimal_perc)) +
                        '\t%\t' + str(np.round(value,n_decimal_sec)) + ' \tsec')
            else:
                raise ValueError()
        else:
            print('##########################################################')
            print('Took ' + str(np.round(real_time/60,n_decimal_min))
                  + ' min.')


