#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    plotting namelist for 005_org_ana:
author			Christoph Heim
date created    06.09.2021
date changed    25.04.2022
usage			import in another script
"""
###############################################################################
###############################################################################
nlp = {}


#### PLOT RESOLUTION
nlp['dpi'] = 600

nlp['figsize_spatial'] =  {
    '1x1': (5,4),
    '1x2': (8,4),
    # last updated with sp_02
    '1x3': (11,2.5),
    '2x2': (8,6),
    # last updated with sp_02
    '2x3': (11,5),
    # last updated with sp_02
    '2x5': (18,5),
    # last updated with sp_05
    '3x2': (6,8),
    # last updated with sp_06 cfg: change_3
    '3x3': (10,6.5),
    # last updated with sp_01
    '3x4': (14,7),
    # last updated with sp_02
    '3x5': (16,7),
    # last updated with sp_05
    '3x6': (20,7),
    # last updated with sp_06
    '4x3': (12,8),
    # last updated with sp_05
    '4x4': (12,8),
    '4x5': (16,11),
    # last updated with sp_05
    '4x6': (20,12),
    # last updated with sp_05
    '4x7': (24,12),
    # last updated with sp_05
    '4x8': (28,12),
    '5x5': (16,13),
    '5x6': (20,13),
    # last updated with sp_06
    '6x3': (13,14),
    # last updated with sp_02
    '6x4': (16,20),
    '6x6': (20,15),
}
nlp['figsize_lineplot'] =  {
    # last updated with pr_01
    '1x3': (8,3),
    # last updated with tl_01
    '2x2': (9,6),
    # last updated with pr_01
    '2x3': (8,6),
    # last updated with tl_01
    '3x2': (9,9),
    # last updated with pr_01
    '3x3': (8,8),
    # last updated with pr_01
    '3x4': (12,8),
    # last updated with pr_01
    '4x4': (12,10),
    # last updated with pr_01
    '5x4': (12,13),
    # last updated with tl_03
    '5x2': (8,11),
}

nlp['args_subplots_adjust_dict_spatial'] =  {
    '1x1': {
        'left':0.08,
        'bottom':0.10,
        'right':0.98,
        'top':0.95,
        'wspace':0.40,
        'hspace':0.20,
    },
    '1x2': {
        'left':0.08,
        'bottom':0.10,
        'right':0.98,
        'top':0.95,
        'wspace':0.40,
        'hspace':0.20,
    },
    # last updated with pr_01
    '1x3': {
        'left':0.08,
        'bottom':0.18,
        'right':0.99,
        'top':0.90,
        'wspace':0.10,
        'hspace':0.10,
    },
    # last updated with tl_01
    '2x2': {
        'left':0.09,
        'bottom':0.09,
        'right':0.98,
        'top':0.95,
        'wspace':0.18,
        'hspace':0.25,
    },
    # last updated with sp_02
    '2x3': {
        'left':0.08,
        'bottom':0.08,
        'right':0.99,
        'top':0.97,
        'wspace':0.20,
        'hspace':0.15,
    },
    # last updated with sp_02
    '2x5': {
        'left':0.05,
        'bottom':0.06,
        'right':0.98,
        'top':0.97,
        'wspace':0.30,
        'hspace':0.15,
    },
    # last updated with sp_05
    '3x2': {
        'left':0.07,
        'bottom':0.05,
        'right':0.99,
        'top':0.97,
        'wspace':0.40,
        'hspace':0.40,
    },
    # last updated with sp_06 cfg: change_3
    '3x3': {
        'left':0.08,
        'bottom':0.07,
        'right':0.98,
        'top':0.97,
        'wspace':0.10,
        'hspace':0.25,
    },
    # last updated with sp_06 cfg: change_3
    '3x4': {
        'left':0.06,
        'bottom':0.06,
        'right':0.98,
        'top':0.98,
        'wspace':0.10,
        'hspace':0.20,
    },
    # last updated with sp_02
    '3x5': {
        'left':0.03,
        'bottom':0.05,
        'right':0.99,
        'top':0.98,
        'wspace':0.20,
        'hspace':0.10,
    },
    # last updated with sp_05
    '3x6': {
        'left':0.05,
        'bottom':0.05,
        'right':0.99,
        'top':0.98,
        'wspace':0.20,
        'hspace':0.10,
    },
    # last updated with sp_06
    '4x3': {
        'left':0.07,
        'bottom':0.05,
        'right':0.97,
        'top':0.97,
        'wspace':0.20,
        'hspace':0.20,
    },
    # last updated with sp_05
    '4x4': {
        'left':0.07,
        'bottom':0.05,
        'right':0.97,
        'top':0.97,
        'wspace':0.20,
        'hspace':0.20,
    },
    '4x5': {
        'left':0.04,
        'bottom':0.03,
        'right':0.99,
        'top':0.98,
        'wspace':0.10,
        'hspace':0.06,
    },
    # last updated with sp_05
    '4x6': {
        'left':0.04,
        'bottom':0.03,
        'right':0.99,
        'top':0.98,
        'wspace':0.10,
        'hspace':0.06,
    },
    # last updated with sp_05
    '4x7': {
        'left':0.04,
        'bottom':0.03,
        'right':0.99,
        'top':0.98,
        'wspace':0.10,
        'hspace':0.06,
    },
    # last updated with sp_05
    '4x8': {
        'left':0.04,
        'bottom':0.03,
        'right':0.99,
        'top':0.98,
        'wspace':0.10,
        'hspace':0.06,
    },
    '5x5': {
        'left':0.04,
        'bottom':0.03,
        'right':0.99,
        'top':0.98,
        'wspace':0.10,
        'hspace':0.06,
    },
    '5x6': {
        'left':0.04,
        'bottom':0.03,
        'right':0.99,
        'top':0.98,
        'wspace':0.10,
        'hspace':0.06,
    },
    # last updated with sp_06
    '6x3': {
        'left':0.05,
        'bottom':0.04,
        'right':0.99,
        'top':0.98,
        'wspace':0.08,
        'hspace':0.20,
    },
    # last updated with sp_02
    '6x4': {
        'left':0.04,
        'bottom':0.03,
        'right':0.99,
        'top':0.98,
        'wspace':0.10,
        'hspace':0.06,
    },
    '6x6': {
        'left':0.04,
        'bottom':0.03,
        'right':0.99,
        'top':0.98,
        'wspace':0.10,
        'hspace':0.06,
    },
}



nlp['args_subplots_adjust_dict_lineplot'] =  {
    '1x1': {
        'left':0.08,
        'bottom':0.10,
        'right':0.98,
        'top':0.95,
        'wspace':0.40,
        'hspace':0.20,
    },
    '1x2': {
        'left':0.08,
        'bottom':0.10,
        'right':0.98,
        'top':0.95,
        'wspace':0.40,
        'hspace':0.20,
    },
    # last updated with pr_01
    '1x3': {
        'left':0.08,
        'bottom':0.18,
        'right':0.99,
        'top':0.90,
        'wspace':0.10,
        'hspace':0.10,
    },
    # last updated with tl_01
    '2x2': {
        'left':0.09,
        'bottom':0.09,
        'right':0.98,
        'top':0.95,
        'wspace':0.18,
        'hspace':0.25,
    },
    # last updated with pr_01
    '2x3': {
        'left':0.08,
        'bottom':0.10,
        'right':0.98,
        'top':0.95,
        'wspace':0.25,
        'hspace':0.35,
    },
    # last updated with tl_02
    '3x2': {
        'left':0.11,
        'bottom':0.06,
        'right':0.98,
        'top':0.96,
        'wspace':0.18,
        'hspace':0.30,
    },
    '3x3': {
        'left':0.07,
        'bottom':0.05,
        'right':0.99,
        'top':0.97,
        'wspace':0.40,
        'hspace':0.40,
    },
    # last updated with pr_01
    '3x4': {
        'left':0.06,
        'bottom':0.07,
        'right':0.97,
        'top':0.96,
        'wspace':0.25,
        'hspace':0.30,
    },
    '3x5': {
        'left':0.03,
        'bottom':0.05,
        'right':0.99,
        'top':0.98,
        'wspace':0.20,
        'hspace':0.10,
    },
    '4x4': {
        'left':0.07,
        'bottom':0.05,
        'right':0.99,
        'top':0.97,
        'wspace':0.40,
        'hspace':0.40,
    },
    '4x5': {
        'left':0.04,
        'bottom':0.03,
        'right':0.99,
        'top':0.98,
        'wspace':0.10,
        'hspace':0.06,
    },
    # last updated with sp_05
    '4x6': {
        'left':0.04,
        'bottom':0.03,
        'right':0.99,
        'top':0.98,
        'wspace':0.10,
        'hspace':0.06,
    },
    # last updated with tl_03
    '5x2': {
        'left':0.10,
        'bottom':0.05,
        'right':0.98,
        'top':0.97,
        'wspace':0.25,
        'hspace':0.30,
    },
    # last updated with pr_01
    '5x4': {
        'left':0.06,
        'bottom':0.05,
        'right':0.98,
        'top':0.97,
        'wspace':0.15,
        'hspace':0.30,
    },
    '5x5': {
        'left':0.04,
        'bottom':0.03,
        'right':0.99,
        'top':0.98,
        'wspace':0.10,
        'hspace':0.06,
    },
    '5x6': {
        'left':0.04,
        'bottom':0.03,
        'right':0.99,
        'top':0.98,
        'wspace':0.10,
        'hspace':0.06,
    },
    '6x6': {
        'left':0.04,
        'bottom':0.03,
        'right':0.99,
        'top':0.98,
        'wspace':0.10,
        'hspace':0.06,
    },
}


####### PANEL LABELS
nlp['i_add_panel_labels'] = 1
nlp['kwargs_panel_labels'] = {
    'start_ind': 0,
    'shift_right': 0.00,
    'shift_up': 0.04,
    'fontsize': 14,
}
