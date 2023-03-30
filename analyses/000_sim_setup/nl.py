#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 000
author			Christoph Heim
date created    20.04.2019
date changed    10.09.2020
usage			import in another script
"""
###############################################################################
import os, subprocess, sys
from base.nl_domains import *
from base.nl_global import (plot_glob_base_dir, inp_glob_base_dir,
                               ana_glob_base_dir)
###############################################################################
# PATHS
ana_name        = '000_sim_setup'
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name)

i_save_fig = int(sys.argv[1])

lon0 = -83
#lon1 = 30
lon1 = 35
#lat0 = -37
lat0 = -39
lat1 = 30
dom_plot_map = {
    'lon':slice(lon0, lon1),
    'lat':slice(lat0, lat1)}

map_domain = dom_SA_3km
dticks  = 15
map_domain = dom_plot_map 
dticks  = 20
#map_domain = dom_map_gulf
#dticks  = 20

###############################################################################
i_plot_model_domains = 1

i_plot_dom_12km = 0
i_plot_dom_4km = 0
i_plot_dom_3km = 1
i_plot_dom_2km = 0
i_plot_dom_1km = 0
i_plot_dom_05km = 0

i_plot_dom_gulf = 0


###############################################################################
i_plot_ana_domains = 1

###### two paper domains
i_plot_dom_SEA_Sc = 0
i_plot_dom_Sc_zoom = 0
i_plot_dom_SEA_Sc_sub_Cu = 0
i_plot_dom_SEA_Sc_sub_Sc = 0
i_plot_dom_SEA_Sc_sub_St = 0
######
###### long sim domains
i_plot_dom_SA_ana = 1
i_plot_dom_SA_ana_sea = 0
i_plot_dom_SA_ana_land = 0
i_plot_dom_ITCZ = 1
i_plot_dom_trades_shallow = 1
i_plot_dom_trades_deep = 1
i_plot_dom_trades = 1
i_plot_dom_SA_ana_merid_cs = 1
######
i_plot_dom_test = 0

###############################################################################
i_plot_dya_domains = 0

i_plot_4km_test = 0
i_plot_alps_50km = 0


