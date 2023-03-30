#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    Class that handles the member of an analysis. A member could
                for instance be a certain simulation at
                specific resolution or an observational data set.
                A member can contain multiple variables and manage
                additional information about them.
author			Christoph Heim
date created    21.03.2019
date changed    16.11.2021
usage			use in another script
"""
###############################################################################
import time, cartopy, copy
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from package.utilities import subsel_domain, area_weighted_mean_lat_lon
###############################################################################

class Member:

    def __init__(self, mem_dict, val_type='abs'):
        """
        -----------------------------------------------------------------------
        INPUT:
        mem_dict:       dict - Dictionary with metadata for this member.
        val_type:       Absolute value of one member (abs) or difference 
                        between two members (diff)?
        -----------------------------------------------------------------------
        COMMENTS:
        """
        self.mem_dict = copy.deepcopy(mem_dict)
        self.val_type = val_type
        self.vars = {}
        # statistical values that can be used for labels etc.
        self.stat = {}
        # plot min and max (to compute and store globally among several 
        # members)
        self.plot_min_max = {}

        if 'label' not in self.mem_dict:
            raise ValueError('Member dict does not contain label')
        
        # handle objects for legends/global colorbars (for each variable)
        self.handles = {}
    ###########################################################################



    def add_var(self, var_name, var):
        """
        Add variable to members vars dict.
        -----------------------------------------------------------------------
        INPUT:
        var:            xr Dataarray - xarray Dataarray of variable
        var_name:       str - Name of variable.
        -----------------------------------------------------------------------
        """
        if var_name in self.vars:
            raise ValueError('Variable already part of this member')
        else:
            #if self.agg_level is not None:
            #    if var.attrs['agg_level'] != self.agg_level:
            #        raise ValueError('Variable has not the same agg level 
            #                        as member')
            #self.agg_level = var.agg_level
            #self.agg_operator = var.agg_operator
            self.vars[var_name] = var



    def compute_statistics(self, domain):
        """
        Computes field mean statistics for given domain. These values can
        later be used for plot labels etc.
        -----------------------------------------------------------------------
        INPUT:
        domain:         dict - containing information of domain
        -----------------------------------------------------------------------
        """
        for var_name,var in self.vars.items():
            if var is not None:
                self.stat[var_name] = {}
                dom_var = subsel_domain(var, domain)
                self.stat[var_name]['mean'] = area_weighted_mean_lat_lon(dom_var).values
                self.stat[var_name]['max'] = dom_var.squeeze().max().values
                self.stat[var_name]['min'] = dom_var.min().values
                self.stat[var_name]['rms'] = np.sqrt((dom_var**2).mean()).values
