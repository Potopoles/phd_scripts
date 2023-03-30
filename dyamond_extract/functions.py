#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description:    Functions used in DYAMOND data extraction.
author:         Christoph Heim
date created:   15.07.2019
date changed:   15.07.2019
usage:          use in main scripts
python:         3.5.2
"""
###############################################################################
import os
###############################################################################

def paste_dir_names(out_base_dir, model_name, res, domain):
    out_dir = os.path.join(out_base_dir,
                           '{}_{}'.format(model_name, res),
                           domain['code'])
    out_tmp_dir = os.path.join(out_base_dir,
                               '{}_{}'.format(model_name, res),
                               'tmp')

    return(out_dir, out_tmp_dir)
