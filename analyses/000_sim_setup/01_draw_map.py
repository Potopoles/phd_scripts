#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    Plot map with domains
author			Christoph Heim
date created    20.04.2019
date changed    06.01.2021
usage			1st: i_save_fig (0: show, 1: png, 2: pdf, 3: jpg)
"""
###############################################################################
import matplotlib
import collections
import matplotlib.pyplot as plt
import numpy as np
from base.nl_domains import *
from package.plot_functions import (draw_map, draw_domain)
from package.plot_functions import PlotOrganizer
import nl as nl
from nl_plot import nlp
###############################################################################



name_dict = collections.OrderedDict()
#name_dict['test'] = 'ERAI_12_2'
#name_dict['test'] = 'ERA5_4_2'
#name_dict['test'] = 'ERA5_12_4_2'
#name_dict['test'] = 'ERA5_4_2_itcz'
#name_dict[''] = 'domain_soil_spinup'
#name_dict[''] = '3D_animation'
name_dict['ana'] = nl.i_plot_ana_domains
name_dict['mod'] = nl.i_plot_model_domains
name_dict['dya'] = nl.i_plot_dya_domains
name_dict['trnsp'] = nlp['transparent_bg'] 
PO = PlotOrganizer(nl.i_save_fig, path=nl.plot_base_dir,
                   name_dict=name_dict,
                   nlp=nlp, geo_plot=True)
PO.initialize_plot(nrows=1, ncols=1)
ax = PO.axes[0,0]
ax.set_visible(True)
#ax = plt.axes(projection=nlP['projection'])
draw_map(ax, nl.map_domain, nlp, dticks=nl.dticks)

handles = []
### model domains
if nl.i_plot_model_domains:

    if nl.i_plot_dom_12km:
        col = plt.rcParams['axes.prop_cycle'].by_key()['color'][0]
        col = 'k'
        line = draw_domain(ax, dom_DYA_12km, nlp, color=col, linestyle='--',
                        linewidth=nlp['lw'], zorder=1) 
        handles.append(line)
    if nl.i_plot_dom_4km:
        #col = plt.rcParams['axes.prop_cycle'].by_key()['color'][1]
        #col = 'k'
        #line = draw_domain(ax, dom_SA_4km, nlp, color=col, linestyle='--',
        #                linewidth=nlp['lw'], zorder=1) 
        #handles.append(line)
        col = 'k'
        line = draw_domain(ax, dom_DYA_4km, nlp, color=col, linestyle='-',
                        linewidth=nlp['lw'], zorder=1) 
        handles.append(line)
        #line = draw_domain(ax, dom_SSA_4km, nlp, color=col, linestyle='-',
        #                linewidth=nlp['lw'], zorder=1) 
        #handles.append(line)
    if nl.i_plot_dom_3km:
        col = 'k'
        line = draw_domain(ax, dom_SA_3km_large3, nlp, color=col, linestyle='-',
                        linewidth=nlp['lw'], zorder=1) 
        handles.append(line)
        #col = 'red'
        #line = draw_domain(ax, dom_SA_3km, nlp, color=col, linestyle='-',
        #                linewidth=nlp['lw'], zorder=1) 
        #handles.append(line)
        #col = 'k'
        #line = draw_domain(ax, dom_SA_3km_OLD, nlp, color=col, linestyle='--',
        #                linewidth=nlp['lw'], zorder=1) 
        #handles.append(line)
        #col = 'orange'
        #line = draw_domain(ax, dom_SA_3km_large, nlp, color=col, linestyle='-',
        #                linewidth=nlp['lw'], zorder=1) 
        #handles.append(line)
        #col = 'purple'
        #line = draw_domain(ax, dom_SA_3km_large2, nlp, color=col, linestyle='-',
        #                linewidth=nlp['lw'], zorder=1) 
        #handles.append(line)
        #col = 'k'
        #line = draw_domain(ax, dom_SA_3km_interim2, nlp, color=col, linestyle='-',
        #                linewidth=nlp['lw'], zorder=1) 
        #handles.append(line)
        #col = 'red'
        #line = draw_domain(ax, dom_SA_3km_interim, nlp, color=col, linestyle='-',
        #                linewidth=nlp['lw'], zorder=1) 
        #handles.append(line)
        #col = 'orange'
        #line = draw_domain(ax, dom_DYA_3km, nlp, color=col, linestyle='-',
        #                linewidth=nlp['lw'], zorder=1) 
        #handles.append(line)
        #col = 'green'
        #line = draw_domain(ax, dom_SSA_3km, nlp, color=col, linestyle='-',
        #                linewidth=nlp['lw'], zorder=1) 
        #handles.append(line)
    if nl.i_plot_dom_2km:
        col = plt.rcParams['axes.prop_cycle'].by_key()['color'][2]
        col = 'purple'
        line = draw_domain(ax, dom_DYA_2km, nlp, color=col, linestyle='-',
                        linewidth=nlp['lw'], zorder=1) 
        handles.append(line)
    if nl.i_plot_dom_1km:
        col = plt.rcParams['axes.prop_cycle'].by_key()['color'][3]
        col = 'blue'
        line = draw_domain(ax, dom_DYA_1km, nlp, color=col, linestyle='-',
                        linewidth=nlp['lw'], zorder=1) 
        handles.append(line)
    if nl.i_plot_dom_05km:
        col = plt.rcParams['axes.prop_cycle'].by_key()['color'][4]
        col = 'green'
        line = draw_domain(ax, dom_DYA_05km, nlp, color=col, linestyle='-',
                        linewidth=nlp['lw'], zorder=1) 
        handles.append(line)



    # 3-level nesting
    #line = draw_domain(ax, dom_lm_12_3lev, nlp, color='k', linestyle='--',
    #                linewidth=2, zorder=1) 
    #handles.append(line)
    #line = draw_domain(ax, dom_lm_4_3lev, nlp, color='k', linestyle='-',
    #                linewidth=2, zorder=1) 
    #handles.append(line)

    # 2-level nesting
    #line = draw_domain(ax, dom_lm_12_2lev, nlp, color='k',
    #                linestyle='--', linewidth=2, zorder=1) 
    #handles.append(line)

    #line = draw_domain(ax, dom_lm_4_2lev, nlp, color='k',
    #                linestyle='-', linewidth=2, zorder=1) 
    #handles.append(line)

    #line = draw_domain(ax, dom_lm_4_itcz, nlp, color='k', linestyle='-',
    #                linewidth=2, zorder=1) 
    #handles.append(line)



    ## soil spinup
    #line = draw_domain(ax, dom_lm_24_soil_spinup,
    #                nlp, color='black', linestyle='-', linewidth=2, zorder=1) 
    #handles.append(line)
    
    ### 3D animation
    #line = draw_domain(ax, dom_lm_2_3D_anim, nlp, color='orange', linestyle='-',
    #                linewidth=2, zorder=1) 
    #handles.append(line)

    if nl.i_plot_dom_gulf:
        col = 'k'
        line = draw_domain(ax, dom_gulf_12, nlp, color=col, linestyle='--',
                        linewidth=nlp['lw'], zorder=1) 
        line = draw_domain(ax, dom_gulf_2, nlp, color=col, linestyle='-',
                        linewidth=nlp['lw'], zorder=1) 
        handles.append(line)


### analysis domains
if nl.i_plot_ana_domains:


    ### DYAMOND paper domains
    if nl.i_plot_dom_SEA_Sc:
        line = draw_domain(ax, dom_SEA_Sc, nlp, color='red',
                                linestyle='--', linewidth=nlp['lw'], zorder=1) 
        handles.append(line)

    if nl.i_plot_dom_Sc_zoom:
        line = draw_domain(ax, dom_Sc_zoom, nlp, color='blue',
                                linestyle='--', linewidth=nlp['lw'], zorder=1) 
        handles.append(line)

    if nl.i_plot_dom_SEA_Sc_sub_Sc:
        line = draw_domain(ax, dom_SEA_Sc_sub_Sc, nlp, color='gold',
                                linestyle='-', linewidth=nlp['lw'], zorder=1) 
        handles.append(line)
    if nl.i_plot_dom_SEA_Sc_sub_Cu:
        line = draw_domain(ax, dom_SEA_Sc_sub_Cu, nlp, color='darkorange',
                                linestyle='-', linewidth=nlp['lw'], zorder=1) 
        handles.append(line)
    if nl.i_plot_dom_SEA_Sc_sub_St:
        line = draw_domain(ax, dom_SEA_Sc_sub_St, nlp, color='red',
                                linestyle='--', linewidth=nlp['lw'], zorder=1) 
        handles.append(line)
    ### DYAMOND paper domains


    ### trade wind / low cloud region
    if nl.i_plot_dom_SA_ana:
        line = draw_domain(ax, dom_SA_ana, nlp, color='red',
                                linestyle='-', linewidth=nlp['lw'], zorder=1) 
        handles.append(line)
    if nl.i_plot_dom_SA_ana_land:
        line = draw_domain(ax, dom_SA_ana_land, nlp, color='blue',
                                linestyle='-', linewidth=nlp['lw'], zorder=1) 
        handles.append(line)
    if nl.i_plot_dom_SA_ana_sea:
        line = draw_domain(ax, dom_SA_ana_sea, nlp, color='red',
                                linestyle='-', linewidth=nlp['lw'], zorder=1) 
        handles.append(line)
    if nl.i_plot_dom_ITCZ:
        line = draw_domain(ax, dom_ITCZ, nlp, color='blue',
                                linestyle='-', linewidth=nlp['lw'], zorder=1) 
        handles.append(line)
    if nl.i_plot_dom_trades:
        line = draw_domain(ax, dom_trades, nlp, color='red',
                                linestyle='-', linewidth=nlp['lw'], zorder=1) 
        handles.append(line)
    if nl.i_plot_dom_trades_shallow:
        line = draw_domain(ax, dom_trades_shallow, nlp, color='orange',
                                linestyle='-', linewidth=nlp['lw'], zorder=1) 
        handles.append(line)
    if nl.i_plot_dom_trades_deep:
        line = draw_domain(ax, dom_trades_deep, nlp, color='green',
                                linestyle='-', linewidth=nlp['lw'], zorder=1) 
        handles.append(line)
    if nl.i_plot_dom_SA_ana_merid_cs:
        line = draw_domain(ax, dom_SA_ana_merid_cs, nlp, color='purple',
                                linestyle='-', linewidth=nlp['lw'], zorder=1) 
        handles.append(line)
    ### trade wind / low cloud region



    if nl.i_plot_dom_test:
        line = draw_domain(ax, dom_test, nlp, color='orange',
                                linestyle='--', linewidth=nlp['lw'], zorder=1) 
        handles.append(line)


    #line = draw_domain(ax, dom_cross_sect, nlp, color='green',
    #                        linestyle='--', linewidth=2, zorder=1) 
    #handles.append(line)

    
    #line = draw_domain(ax, dom_northern_italy, nlp, color='blue',
    #                        linestyle='-', linewidth=2, zorder=1) 
    #handles.append(line)
    #print(ax.get_xlim())
    #print(dom_alps_vert_prof)
    #line = draw_domain(ax, dom_alps_vert_prof, nlp, color='blue',
    #                        linestyle='-', linewidth=2, zorder=1) 
    #handles.append(line)






    #line = draw_domain(ax, dom_SEA_Sc_zoom, nlp, color='orange',
    #                        linestyle='-', linewidth=2, zorder=1) 
    #handles.append(line)

    #line = draw_domain(ax, dom_SA_zoom, nlp, color='k',
    #                        linestyle='-', linewidth=2, zorder=1) 
    #handles.append(line)





### dyamond domains
if nl.i_plot_dya_domains:
    #line_dya_1 = draw_domain(ax, dom_dya_1, nlp, color='purple', linestyle='-',
    #                linewidth=2, zorder=1) 
    line = draw_domain(ax, dom_dya_2, nlp, color='violet', linestyle='-',
                    linewidth=nlp['lw'], zorder=1) 
    handles.append(line)


### 4km test domain 
if nl.i_plot_4km_test:
    ## full
    #line = draw_domain(ax, dom_lm_12_test_full, nlp,
    #                color='k', linestyle='--',
    #                linewidth=2, zorder=1) 
    #handles.append(line)
    #line = draw_domain(ax, dom_lm_4_test_full, nlp,
    #                color='k', linestyle='-',
    #                linewidth=2, zorder=1) 
    #handles.append(line)

    ## nona
    #line = draw_domain(ax, dom_lm_12_test_nona, nlp, color='k', linestyle='--',
    #                linewidth=2, zorder=1) 
    #handles.append(line)
    #line = draw_domain(ax, dom_lm_4_test_nona, nlp, color='k', linestyle='-',
    #                linewidth=2, zorder=1) 
    #handles.append(line)

    ## noitcz
    #line = draw_domain(ax, dom_lm_12_test_noitcz, nlp, color='k',
    #                linestyle='--', linewidth=2, zorder=1) 
    #handles.append(line)
    #line = draw_domain(ax, dom_lm_4_test_noitcz,
    #                nlp, color='k', linestyle='-',
    #                linewidth=2, zorder=1) 
    #handles.append(line)

    ## small itcz
    line = draw_domain(ax, dom_lm_12_test_smallitcz, nlp, color='k',
                    linestyle='--', linewidth=nlp['lw'], zorder=1) 
    handles.append(line)
    line = draw_domain(ax, dom_lm_4_test_smallitcz,
                    nlp, color='k', linestyle='-',
                    linewidth=nlp['lw'], zorder=1) 
    handles.append(line)

    ## small
    #line = draw_domain(ax, dom_lm_12_test_small, nlp, color='k',
    #                linestyle='--', linewidth=2, zorder=1) 
    #handles.append(line)
    #line = draw_domain(ax, dom_lm_4_test_small,
    #                nlp, color='k', linestyle='-',
    #                linewidth=2, zorder=1) 
    #handles.append(line)

    ### more land
    #line = draw_domain(ax, dom_lm_12_test_land, nlp, color='k',
    #                linestyle='--', linewidth=2, zorder=1) 
    #handles.append(line)
    #line = draw_domain(ax, dom_lm_4_test_land,
    #                nlp, color='k', linestyle='-',
    #                linewidth=2, zorder=1) 
    #handles.append(line)




### alps 50km cs
if nl.i_plot_alps_50km:
    line = draw_domain(ax, dom_lm_alps_50km, nlp,
                    color='k', linestyle='-',
                    linewidth=nlp['lw'], zorder=1) 
    handles.append(line)


plt.legend(handles=handles, loc='upper left')
PO.fig.subplots_adjust(**nlp['arg_subplots_adjust'])
PO.fig.set_size_inches(nlp['figsize_inches'])
PO.finalize_plot()

