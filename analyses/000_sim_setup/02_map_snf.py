#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    Plot domains for SNF proposal
author			Christoph Heim
date created    23.09.2019
date changed    23.09.2019
usage			no args
"""
###############################################################################
import matplotlib
#matplotlib.use('Agg')
import collections
import matplotlib.pyplot as plt
from matplotlib.legend import Legend
import numpy as np
from package.domains import *
from package.plot_functions import (draw_map, draw_domain)
from package.plot_functions import PlotOrganizer
import nl as nl
from nl_plot import nlp
###############################################################################



name_dict = collections.OrderedDict()
name_dict[''] = 'snf_domains'
PO = PlotOrganizer(nl.i_save_fig, path=nl.plot_dir, name_dict=name_dict,
                   nlp=nlp, geo_plot=True)
PO.initialize_plot(nrow=1, ncol=1)

map_domain = {
    'label':'',
    'lon':slice(-74, 25),
    'lat':slice(-35, 31),
}
draw_map(PO.ax, map_domain, nlp, dticks=20)

handles = []
# laurelines domains
line = draw_domain(PO.ax, dom_lm_c_lh, nlp, color='k',
                        linestyle='--', linewidth=2, zorder=1) 
handles.append(line)
line = draw_domain(PO.ax, dom_lm_f_lh, nlp, color='k',
                        linestyle='-', linewidth=2, zorder=1) 
handles.append(line)

plt.legend(handles=handles, loc='upper right', title='Tropical Atlantic')
handles = []

# christophs domains
color = 'red'
line = draw_domain(PO.ax, dom_lm_12_2lev, nlp, color=color,
                        linestyle='--', linewidth=2, zorder=1) 
handles.append(line)
line = draw_domain(PO.ax, dom_lm_2, nlp, color=color,
                        linestyle='-', linewidth=2, zorder=1) 
handles.append(line)
line = draw_domain(PO.ax, dom_lm_1, nlp, color=color,
                        linestyle='-.', linewidth=2, zorder=1) 
handles.append(line)

leg = Legend(plt.gca(), handles=handles, labels=[handles[0].get_label(),
            handles[1].get_label(), handles[2].get_label()], 
             loc='lower left', title='South-East Atlantic')
plt.gca().add_artist(leg)

PO.fig.subplots_adjust(left=0.10, bottom=0.10, right=0.98, top=0.98)
factor = 1.2
PO.fig.set_size_inches(8*factor,5.5*factor)
PO.finalize_plot()

