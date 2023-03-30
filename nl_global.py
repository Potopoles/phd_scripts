#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Global namelist that contains paths used in every analysis.
author			Christoph Heim
date created    13.02.2020
date changed    19.02.2020
usage           no args
"""
###############################################################################
import os
###############################################################################
plot_glob_base_dir      = os.path.join('/net','o3','hymet_nobackup','heimc',
                                       'plots')
inp_glob_base_dir       = os.path.join('/net','o3','hymet_nobackup','heimc',
                                       'data', 'input')
ana_glob_base_dir       = os.path.join('/net','o3','hymet_nobackup','heimc',
                                       'analyses')

model_specifics_path = os.path.join('package','model_specific')


