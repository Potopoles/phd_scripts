#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Super class for analysis
author			Christoph Heim
date created    09.09.2021
date changed    11.07.2022
"""
###############################################################################
import os,dask,copy,time
import numpy as np
import pandas as pd
from pathlib import Path
import datetime
from datetime import timedelta
from package.time_processing import Time_Processing as TP
from package.functions import (
    load_member_var, 
    save_member_to_pickle,
    save_member_var_to_netcdf,
    load_member_from_pickle,
    load_member_var_from_netcdf,
    time_periods_to_dates,
    get_comb_mem_key,
    loc_to_var_name,
    create_dates_code,
    create_combined_member,
)
from package.utilities import dt64_to_dt
from package.member import Member
from nl_var_src import set_up_var_src_dict, set_up_mean_var_src_dict
###############################################################################

class Analysis:
    
    def __init__(self, nl):
        super(Analysis, self).__init__()
        self.nl = nl
        self.ana_number = None


    def create_combined_target_members(self, targ_mem_cfg, indiv_targ_members):
        #print(targ_mem_cfg)
        #quit()
        if 'mem_keys' in targ_mem_cfg:
            # iteratively compute and collect sub-members of this member
            sub_targ_members = []
            for sub_mem_cfg in targ_mem_cfg['mem_keys']:
                #print(sub_mem_cfg)
                sub_targ_mem_key,sub_targ_member = self.create_combined_target_members(
                                                        sub_mem_cfg, indiv_targ_members)
                sub_targ_members.append(sub_targ_member)
                #print(sub_targ_member.val_type)
                #print(sub_targ_member.vars.keys())
            #quit()
            #print(targ_mem_cfg)
            targ_mem_date_key,targ_member = create_combined_member(
                                            sub_targ_members, targ_mem_cfg)
            #quit()
            #dates_code = create_dates_code(time_periods_to_dates(targ_mem_cfg['time_periods']))
            #targ_mem_date_key = '{}#time#{}'.format(targ_mem_key, dates_code)
        else:
            dates_code = create_dates_code(time_periods_to_dates(targ_mem_cfg['time_periods']))
            targ_mem_date_key = '{}#time#{}'.format(targ_mem_cfg['mem_key'], dates_code)
            targ_member = indiv_targ_members[targ_mem_date_key]

        #print(targ_member.val_type)

        for attr in ['label','spread','mem_oper','color','linestyle','linewidth','zorder']:
            if attr in targ_mem_cfg:
                targ_member.mem_dict[attr] = targ_mem_cfg[attr]

        return(targ_mem_date_key, targ_member)


    def prepare_for_plotting_DEFAULT(self, indiv_targ_members):
        targ_members = {}
        #print(self.targ_mem_list)
        ## combine members
        for targ_mem_cfg in self.targ_mem_list:
            #print('#####################################')
            #print(targ_mem_cfg)
            targ_mem_key, targ_member = self.create_combined_target_members(
                                        targ_mem_cfg, indiv_targ_members)
            targ_members[targ_mem_key] = targ_member
            #print(targ_member.val_type)
        #quit()
        return(targ_members)


    def prepare_for_plotting(self, members):
        members = self.prepare_for_plotting_DEFAULT(members)
        return(members)


    def draw_axis_DEFAULT(self, ax):
        # show hidden axis again
        ax.set_visible(True)


    def draw_axis(self, PO, members, ax):
        self.draw_axis_DEFAULT(ax)


    def compute_src_members_for_date(self, ts):
        """
        Organize full analysis for a given date (ts).
        ts has to be called ts because compute_for_date is called from TimeStepMP.
        """
        #print(ts)

        if (self.nl.i_debug >= 1) and (ts.day == 1):
            print('Start processing month {:%Y%m}.'.format(ts))
        #if (self.nl.i_debug >= 1) and (ts.day == 1):
        #    print('Start processing month {:%Y%m}. Memory: {} MB'.format(ts, 
        #        psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2))

        ######## LOAD MEMBERS
        ##########################################################################
        members = {}
        for mem_key,mem_dict in self.src_mem_dict.items():
            #print(mem_key)
            # create member instance
            members[mem_key] = Member(mem_dict, val_type='abs')
            # set time key
            members[mem_key].time_key = 'time'

            for loc_var_name in self.nl.var_names:

                # skip any date != first date of the month for
                # members with frequency monthly.
                if (mem_dict['freq'] == 'monthly') and (ts.day != 1):
                    var = None
                # also skip any date for daily member that is not
                # part of its date selection
                elif (mem_dict['freq'] == 'monthly') and (ts not in mem_dict['dates']):
                    var = None
                elif (mem_dict['freq'] == 'daily') and (ts not in mem_dict['dates']):
                    #print('not in date selection')
                    var = None
                else:
                    if self.nl.i_debug >= 2:
                        print('{}: {} for {:%Y%m%d}'.format(mem_key, 
                                                    loc_var_name, ts))

                    # in case of alt specification format accordingly
                    loc_dim = None
                    if '@' in loc_var_name:
                        loc_dim = loc_var_name.split('@')[1].split('=')[0]
                        loc_value = loc_var_name.split('@')[1].split('=')[1]
                        var_name = loc_var_name.split('@{}='.format(loc_dim))[0]
                    else:
                        var_name = loc_var_name

                    # load variable
                    var = load_member_var(var_name, mem_dict['freq'],
                                        ts, ts, mem_dict,
                                        self.nl.var_src_dict,
                                        self.nl.mean_var_src_dict,
                                        self.nl.var_src_dict[var_name]['load'],
                                        domain=self.nl.var_dom_map[loc_var_name],
                                        i_debug=self.nl.i_debug,
                                        dask_chunks=self.nl.dask_chunks)
                if var is not None:
                    # make sure all monthly data has first date of month
                    # as time stamp (this is assumed later on)
                    if mem_dict['freq'] == 'monthly':
                        new_time = [dt64_to_dt(var.time.values[0]).replace(day=1)]
                        var = var.assign_coords(time=new_time)
                    # optionally subselect specified altitude
                    if loc_dim is not None:
                        if len(loc_value.split('-')) == 1:
                            if float(loc_value) in var[loc_dim].values:
                                var = var.sel({loc_dim:float(loc_value)})
                            else:
                                var = var.interp({loc_dim:float(loc_value)})
                        elif len(loc_value.split('-')) == 2:
                            var = var.sel({loc_dim:slice(
                                float(loc_value.split('-')[0]),
                                float(loc_value.split('-')[1])
                                )
                            })
                            if len(var.alt) == 0:
                                raise ValueError('No altitude values in selected range for member {}.'.format(mem_key))
                        else:
                            raise ValueError()

                    # compute variable
                    var = self.compute_var(var)
                    # optionally load variable
                    if self.nl.computation_mode == 'load':
                        var.load()
                    members[mem_key].add_var(loc_var_name, var)

                    ## print used memory
                    #if self.nl.i_debug >= 3:
                    #    print('{} {}'.format(ts, 
                    #        psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2))
                else:
                    # free up memory
                    try:
                        del members[mem_key].mem_dict 
                    except AttributeError:
                        pass

                    members[mem_key].add_var(loc_var_name, None)

        output = {'members':members}
        return(output)


    def compute_var(self, var, freq):
        var = var.mean(dim=['lon', 'lat', 'alt'])

        if self.nl.agg_level not in [TP.HOURLY_SERIES, TP.DIURNAL_CYCLE]:
            var = TP.run_aggregation_step(var, 
                      { TP.ACTION:TP.RESAMPLE, 
                        TP.FREQUENCY:'D', 
                        TP.OPERATOR:TP.MEAN  })
            var.attrs['time_key'] = 'time'
            if freq == 'daily':
                var.attrs['agg_level'] = TP.DAILY_SERIES
            elif freq == 'monthly':
                var.attrs['agg_level'] = TP.MONTHLY_SERIES
            else:
                raise NotImplementedError()
            var.attrs['agg_operator'] = TP.MEAN

        return(var)


    def _src_mem_to_indiv_targ_mem(self, targ_mem_cfg, src_members, targ_members):
        if 'mem_keys' in targ_mem_cfg:
            raise ValueError()
            # iteratively compute and collect sub-members of this member
            for sub_mem_cfg in targ_mem_cfg['mem_keys']:
                #print(sub_mem_cfg)
                self._src_mem_to_indiv_targ_mem(sub_mem_cfg, src_members, targ_members)
        else:
            targ_mem_key = targ_mem_cfg['mem_key']
            src_member = src_members[targ_mem_key]
            dates = time_periods_to_dates(targ_mem_cfg['time_periods'])
            #print(dates)

            # create target member key with dates
            dates_code = create_dates_code(dates)
            #print(dates_code)
            #quit()
            targ_mem_date_key = '{}#time#{}'.format(targ_mem_key, dates_code)
            #print(targ_mem_date_key)
            #quit()

            # output member
            targ_member = Member(src_member.mem_dict, val_type='abs')
            del targ_member.mem_dict['dates']
            for var_name in list(src_member.vars.keys()):
                src_var = src_member.vars[var_name]
                # select dates
                if targ_member.mem_dict['freq'] == 'daily':
                    pass
                elif targ_member.mem_dict['freq'] == 'monthly':
                    dates = [date for date in dates if date.day == 1]
                else:
                    raise NotImplementedError()

                # check for missing dates
                use_dates = np.empty((0,), dtype='datetime64[us]')  
                for date in dates:

                    #print(src_var.time)
                    #print(np.median(np.diff(src_var.time)/1E9/3600))
                    
                    #if len(src_var.time) > 1:

                    # sub-daily resolution
                    if np.median(np.diff(src_var.time)/1E9/3600) < 24:
                        #print(src_var.time.sel(
                        #    time=slice('{:%Y-%m-%d}'.format(date), 
                        #              '{:%Y-%m-%d %H:%M}'.format(date + timedelta(days=1)))))
                        use_dates = np.append(use_dates, src_var.time.sel(
                            time=slice('{:%Y-%m-%d}'.format(date), 
                                      '{:%Y-%m-%d %H:%M}'.format(date + timedelta(days=1)))))
                    # daily resolution
                    else:
                        if not np.datetime64(date) in src_var.time:
                            print('Attention: {:%Y%m%d} missing for {}'.format(date, 
                                    targ_member.mem_dict['mod']))
                        else:
                            #use_dates.append(date)
                            use_dates = np.append(use_dates, date)


                    #if not any([date == datetime.datetime.combine(
                    #                dt64_to_dt(dt).date(), 
                    #                datetime.time()) for dt in src_var.time]):
                    ##if not np.datetime64(date) in src_var.time:
                    #    print('Attention: {:%Y%m%d} missing for {}'.format(date, 
                    #            targ_member.mem_dict['mod']))
                    #else:
                    #    use_dates.append(date)
                use_dates = np.unique(use_dates)
                #print(use_dates)
                #print(src_var.time.shape)
                #print(np.unique(src_var.time).shape)
                #print(src_var.time)
                #quit()
                # in case of multiple daily values all with the same time average
                # field, simply take the first one
                if (len(src_var.time) > 1) and  (len(np.unique(src_var.time)) == 1):
                    src_var = src_var.isel(time=range(0,1))
                targ_var = src_var.sel(time=use_dates)
                #time_label = create_dates_code(use_dates)

                targ_member.vars[var_name] = targ_var

            #print(targ_member.vars[var_name].time)
            #quit()
            # aggregate in time for all variables
            self.aggregate_time(targ_member)
            #print(targ_member.vars[TP.get_agg_var_name(var_name,    
            #                                self.nl.agg_level, 
            #                                agg_operator=TP.MEAN)])
            #quit()

            # save in output dictionary
            targ_member.dates_code = dates_code
            targ_members[targ_mem_date_key] = targ_member



    def aggregate_time(self, member):
        for var_name in list(member.vars.keys()):
            var = member.vars[var_name]
            for agg_operator in self.nl.agg_operators:
                #print(agg_operator)
                agg_var_name = TP.get_agg_var_name(var_name,
                                    self.nl.agg_level, agg_operator)

                if var is not None:
                    agg_var = TP.aggregate(var, self.nl.agg_level,
                                            agg_operator)
                else:
                    agg_var = None
                member.vars[agg_var_name] = agg_var
            # delete unaggregated variable
            del member.vars[var_name]
        #quit()


    def aggreg_src_members_to_indiv_targ_members(self, src_members):
        indiv_targ_members = {}
        for targ_mem_key,targ_mem_cfg in self.indiv_targ_mem_cfg.items():
            #print(targ_mem_key)
            self._src_mem_to_indiv_targ_mem(
                targ_mem_cfg, src_members, indiv_targ_members)
        #for key,mem in indiv_targ_members.items():
        #    print(key)
        #quit()

        print('aggreg src members to indiv targ members done.')
        #print('memory used: {} MB'.format(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2))
        #time.sleep(2)
        return(indiv_targ_members)


    def _add_mem_to_src_mem_dict(self, src_mem_dict, mem_cfg):
        #print('add {}'.format(mem_cfg))
        # recursively add sub-members of this member
        if 'mem_keys' in mem_cfg:
            for sub_mem_cfg in mem_cfg['mem_keys']:
                self._add_mem_to_src_mem_dict(src_mem_dict, sub_mem_cfg)
        # add this member
        else:
            mem_key = mem_cfg['mem_key']
            mem_dates = time_periods_to_dates(mem_cfg['time_periods'])
            # if member not yet in mem_src_dict, add a new entry
            if mem_key not in src_mem_dict:
                src_mem_dict[mem_key] = self.nl.mem_src[mem_key]
                #src_mem_dict[mem_key]['dates'] = mem_dates
                # for performance reasons use np.datetime64
                src_mem_dict[mem_key]['dates'] = np.array(mem_dates, dtype='datetime64')
                #src_mem_dict[mem_key]['dates'] = np.array(mem_dates, dtype='datetime64[us]')
            # if mem_key alredy in mem_src_dict, then merely combine the dates
            else:
                #src_mem_dict[mem_key]['dates'].extend(
                #    [dt for dt in mem_dates \
                #        if dt not in src_mem_dict[mem_key]['dates']])
                src_mem_dict[mem_key]['dates'] = np.unique(
                    np.append(src_mem_dict[mem_key]['dates'], mem_dates))
                #print(len(src_mem_dict[mem_key]['dates']))
                #print(src_mem_dict[mem_key]['dates'][0])
                #quit()


    def _add_mem_to_targ_mem_list(self,
        inp_mem_cfg,
        parent_mem_cfg = None):
        """
        Convert mem_cfg entries from namelist into targ_mem_dict format.
        """
        mem_cfg = copy.deepcopy(inp_mem_cfg)

        # if member is not given as dictionary but by mem_src_dict key
        # set up a dictionary
        if not isinstance(mem_cfg, dict):
            mem_cfg = {
                'mem_key':      mem_cfg, 
            }

        #print(mem_cfg)
        #quit()
        #  set default values
        for key in ['agg_level', 'time_periods']:
            if key not in mem_cfg:
                if (parent_mem_cfg is not None) and (key in parent_mem_cfg):
                    mem_cfg[key] =  parent_mem_cfg[key]
                else:
                    mem_cfg[key] = getattr(self.nl, key)


        if 'mem_keys' in mem_cfg:
            # check for wrong configurations
            #print(mem_cfg)
            if 'mem_oper' not in mem_cfg:
                raise ValueError('mem_cfg: if mem_keyS is provided, mem_oper has to be provided, as well.')
            if not isinstance(mem_cfg['mem_keys'], list):
                raise ValueError('mem_cfg: if mem_keyS is provided, has to be a list.')
            else:
                if len(mem_cfg['mem_keys']) == 1:
                    raise ValueError('mem_cfg: if mem_keyS is provided, should be more than one element.')
            #if 'time_periods' in mem_cfg:
            #    for sub_mem_cfg in mem_cfg['mem_keys']:
            #        if 'time_periods' in sub_mem_cfg:
            # recursively create mem_cfgs for the sub-members that constitute this member
            mem_cfgs = []
            for sub_mem_cfg in mem_cfg['mem_keys']:
                sub_mem_cfg = self._add_mem_to_targ_mem_list(
                    sub_mem_cfg,
                    parent_mem_cfg = mem_cfg
                )
                mem_cfgs.append(sub_mem_cfg)
            mem_cfg['mem_keys'] = mem_cfgs
        else:
            # check for wrong configurations
            if 'mem_oper' in mem_cfg:
                raise ValueError('mem_cfg: if mem_key is provided, mem_oper must not be provided.')
        return(mem_cfg)


    def _add_mem_to_indiv_targ_mem_cfg(self, targ_mem_cfg, indiv_targ_mem_cfg):
        if 'mem_keys' in targ_mem_cfg:
            # iteratively compute and collect sub-members of this member
            for sub_mem_cfg in targ_mem_cfg['mem_keys']:
                #print(sub_mem_cfg)
                self._add_mem_to_indiv_targ_mem_cfg(sub_mem_cfg, indiv_targ_mem_cfg)
        else:
            targ_mem_key = targ_mem_cfg['mem_key']
            #print(targ_mem_cfg['time_periods'])
            dates = time_periods_to_dates(targ_mem_cfg['time_periods'])
            # create target member key with dates
            dates_code = create_dates_code(dates)
            #print(dates_code)
            #quit()
            targ_mem_date_key = '{}#time#{}'.format(targ_mem_key, dates_code)

            # save in output dictionary
            if targ_mem_date_key not in indiv_targ_mem_cfg:
                indiv_targ_mem_cfg[targ_mem_date_key] = targ_mem_cfg


    def prepare_namelist_DEFAULT(self):
        # set up paths
        Path(self.nl.ana_base_dir).mkdir(parents=True, exist_ok=True)
        self.nl.pickle_dir = os.path.join(self.nl.ana_base_dir,
                            '{:02d}'.format(self.ana_number))

        # set up var_src_dict
        self.nl.var_src_dict = set_up_var_src_dict(self.nl.inp_base_dir,
                                            self.nl.ana_base_dir,
                                            self.nl.ANA_NATIVE_domain)

        # set up mean_var_src_dict
        self.nl.mean_var_src_dict = set_up_mean_var_src_dict(self.nl.inp_base_dir,
                                            self.nl.ana_base_dir,
                                            self.nl.ANA_NATIVE_domain)

        # aggregated var names for loading
        self.nl.load_agg_var_names = []
        for var_name in self.nl.var_names:
            for agg_operator in self.nl.agg_operators:
                agg_var_name = TP.get_agg_var_name(var_name,
                                self.nl.agg_level, agg_operator)
                self.nl.load_agg_var_names.append(agg_var_name)

        # set variable domains
        self.nl.var_dom_map = {}
        for var_name in self.nl.var_names:
            self.nl.var_dom_map[var_name] = self.nl.plot_domain

        # set up target member list
        targ_mem_list = []
        for mem_cfg in self.nl.mem_cfgs:
            mem_cfg = self._add_mem_to_targ_mem_list(
                mem_cfg,
                targ_mem_list,
            )
            targ_mem_list.append(mem_cfg)
        self.targ_mem_list = targ_mem_list
        #for cfg in targ_mem_list:
        #    print(cfg)
        #quit()

        # set up individual target member configurations
        indiv_targ_mem_cfg = {}
        for mem_cfg in targ_mem_list:
            self._add_mem_to_indiv_targ_mem_cfg(mem_cfg, indiv_targ_mem_cfg)
        self.indiv_targ_mem_cfg = indiv_targ_mem_cfg
        #for key,val in indiv_targ_mem_cfg.items():
        #    print(key)
        #    print(val)
        #quit()


        # find all dates and months that need to be computed among the src members
        # TODO: this takes very long for e.g. 30 year period members like cmip
        print('Perform slow namelist steps...')
        # determine source members based on target member list
        # fill in src_mem_dict
        src_mem_dict = {}
        for mem_cfg in targ_mem_list:
            #print(mem_cfg)
            self._add_mem_to_src_mem_dict(src_mem_dict, mem_cfg)
        self.src_mem_dict = src_mem_dict
        # convert datetime64 back to datetime
        # TODO: this is new and will have to be tested
        # TODO: why do some members have dates as dt64 while others have datetime?
        for key,mem_dict in src_mem_dict.items():
            if not isinstance(mem_dict['dates'][0], datetime.datetime):
                dates = [dt64_to_dt(dt) for dt in mem_dict['dates']]
            else:
                dates = mem_dict['dates']
            src_mem_dict[key]['dates'] = dates
        #for key,mem_dict in src_mem_dict.items():
        #    print(key)
        #    print(mem_dict)
        #quit()

        #self.iter_dates = []
        self.iter_dates = np.empty(0,dtype='datetime64[us]')
        for mem_key,mem_dict in self.src_mem_dict.items():
            #print(mem_key)
            #self.iter_dates.extend([dt for dt in mem_dict['dates'] \
            #                        if dt not in self.iter_dates])
            self.iter_dates = np.unique(np.append(self.iter_dates, mem_dict['dates']))
        # convert back to datetime list. this is cumbersome but the only way
        # I found to work.
        self.iter_dates = pd.to_datetime(self.iter_dates).tz_localize(None)
        self.iter_dates = [dt64_to_dt(dt) for dt in self.iter_dates]
        self.iter_months = [date for date in self.iter_dates if date.day == 1]
        #print(len(self.iter_dates))
        #print(len(np.unique(self.iter_dates)))
        #quit()
        print('Done!')

        # computation settings
        if self.nl.computation_mode not in ['normal', 'load', 'dask']:
            raise ValueError('Invalid input argument for computation_mode')
        if self.nl.computation_mode == 'dask':
            dask.config.set(num_workers=self.nl.n_par)#, num_threads=4)
        else:
            self.nl.dask_chunks = None



    def prepare_namelist(self):
        self.prepare_namelist_DEFAULT()


    def save_data(self, members, netcdf=True):
        if len(members) == 0:
            #if self.nl.i_debug > 0:
            print('Warning in save_to_pickle. No members available.')
        Path(self.nl.pickle_dir).mkdir(exist_ok=True, parents=True)
        for mem_key,member in members.items():

            # save variables
            for loc_agg_var_name in list(member.vars.keys()):
                loc_var_name = TP.get_var_name(loc_agg_var_name)

                save_member_var_to_netcdf(self.nl.pickle_dir, member,
                                self.nl.var_dom_map[loc_var_name],
                                loc_agg_var_name,
                                #self.nl.time_periods,
                                #self.iter_dates,
                                self.nl.pickle_append,
                                netcdf)

            ## delete variables and save member
            #member.vars = {}
            #save_member_to_pickle(self.nl.pickle_dir, member,
            #                #self.nl.time_periods,
            #                #self.iter_dates,
            #                self.nl.pickle_append)


    def load_data(self, netcdf=True):
        members = {}
        for mem_key,mem_cfg in self.indiv_targ_mem_cfg.items():
            mem_dict = self.src_mem_dict[mem_cfg['mem_key']] 
            #quit()
            #member = load_member_from_pickle(
            #                self.nl.pickle_dir,
            #                mem_dict,
            #                #self.nl.time_periods,
            #                self.iter_dates,
            #                self.nl.i_skip_missing,
            #                self.nl.pickle_append)
            member = Member(mem_dict, val_type='abs')
            member.dates_code = mem_key.split('#time#')[1]
            #print(member.dates_code)
            #quit()
            for loc_agg_var_name in self.nl.load_agg_var_names:
                #print(loc_agg_var_name)
                agg_var_name = loc_to_var_name(loc_agg_var_name)
                var_name = TP.get_var_name(agg_var_name)
                loc_var_name = TP.get_var_name(loc_agg_var_name)
                ds_var = load_member_var_from_netcdf(
                                self.nl.pickle_dir,
                                mem_dict,
                                self.nl.var_dom_map[loc_var_name],
                                loc_agg_var_name,
                                #self.nl.time_periods,
                                #self.iter_dates,
                                member.dates_code,
                                self.nl.i_skip_missing,
                                self.nl.pickle_append,
                                netcdf
                            )
                if ds_var is not None:
                    if netcdf:
                        var = ds_var[TP.get_var_name(var_name)]
                    else:
                        var = ds_var
                else:
                    var = None
                member.vars[loc_agg_var_name] = var
            members[mem_key] = member
        return(members)
