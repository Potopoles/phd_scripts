#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Store some constant values
author			Christoph Heim
date created    02.12.2019
date changed    25.01.2021
usage           import in another scripts
"""
###############################################################################
import numpy as np

CON_G = 9.81 # [m/s2]
CON_RD = 287.06 # [J kg-1 K-1]
CON_RV = 462.00 # [J kg-1 K-1]

CON_LH_EVAP = 2.501E6 # [J kg-1] latent heat of evaporation at 0°C
CON_LH_FUSE = 3.337E5 # [J kg-1] latent heat of fusion at 0°C
CON_LH_SUBL = CON_LH_EVAP + CON_LH_FUSE # [J kg-1] latent heat of sublimation at 0°C
CON_CP_AIR = 1.012E3 # [J kg-1 K-1] heat capacity of air

CON_RAD_EARTH = 6371000 # [m]

CON_M_PER_DEG = CON_RAD_EARTH * np.pi / 180 # [m/deg]
