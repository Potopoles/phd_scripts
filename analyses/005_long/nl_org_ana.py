#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 005_99_anaorg:
author			Christoph Heim
date created    25.08.2021
date changed    22.11.2021
usage			import in another script
"""
###############################################################################
import os
from base.nl_global import (plot_glob_base_dir, inp_glob_base_dir,
                               ana_glob_base_dir)
from base.nl_domains import *
from nl_mem_src import *
###############################################################################

## paths
ana_name        = '005_long'
plot_base_dir   = os.path.join(plot_glob_base_dir, ana_name, 'org_ana')
inp_base_dir    = inp_glob_base_dir
ana_base_dir    = os.path.join(ana_glob_base_dir, ana_name)

### run settings
i_debug = 2
i_skip_missing = 1
i_plot = 1

ANA_NATIVE_domain = dom_SA_3km_large3
#ANA_NATIVE_domain = dom_SA_ana
