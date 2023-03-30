#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    namelist for 004_05_daily_variab:
author			Christoph Heim
date created    17.01.2020
date changed    17.01.2020
usage			import in another script
"""
###############################################################################
import os, subprocess, sys
from datetime import datetime, timedelta
from package.utilities import set_up_directories
from base.nl_domains import *
from nl_plot_03 import nlp
###############################################################################
## paths
ana_name        = '004_dyamond'
plot_base_dir   = os.path.join('/net','o3','hymet_nobackup','heimc',
                               'plots', ana_name)
sim_base_dir    = os.path.join('/net','o3','hymet_nobackup','heimc','data',
                               'simulations')
obs_base_dir    = os.path.join('/net','o3','hymet_nobackup','heimc','data',
                               'obs')
ana_base_dir    = os.path.join('/net','o3','hymet_nobackup','heimc',
                               'analyses', ana_name)
grid_des_file   = os.path.join(ana_base_dir, 'grid_45km')

## computation
njobs = 1
if len(sys.argv) > 1:
    njobs = int(sys.argv[1])

## observations
use_obs = {
    'SWUTOA': {'name':'SEVIRI_CERES',
               'path':os.path.join(obs_base_dir,
                                    'seviri_ceres','trs'),
               'sel_str':'TRSdm{:%Y%m%d}*.nc',
    },
    'LWUTOA': {'name':'SEVIRI_CERES',
               'path':os.path.join(obs_base_dir,
                                    'seviri_ceres','tet'),
               'sel_str':'TETdm{:%Y%m%d}*.nc',
    },
}



## simulations
dya_dom = 'SA'
dya_sims = {
    ## use sims
    'COSMO_2.2'     :{'mkey':'COSMO',       'res':2.2,  'sim':'SA_2lev',
                      'label':'COSMO 2.2'                               },
    'COSMO_4.4'     :{'mkey':'COSMO',       'res':4.4,  'sim':'SA_3lev',
                      'label':'COSMO 4.4'                               },
    'NICAM_3.5'     :{'mkey':'NICAM',       'res':3.5,  'sim':dya_dom,
                      'label':'NICAM 3.5'                               },
    'SAM_4'         :{'mkey':'SAM',         'res':4,    'sim':dya_dom,
                      'label':'SAM 4'                                   },
    'ICON_2.5'      :{'mkey':'ICON',        'res':2.5,  'sim':dya_dom,
                      'label':'ICON 2.5'                                },
    'UM_5'          :{'mkey':'UM',          'res':5,    'sim':dya_dom,
                      'label':'UM 5'                                    },
    'MPAS_3.75'     :{'mkey':'MPAS',        'res':3.75, 'sim':dya_dom,
                      'label':'MPAS 3.75'                               },
    'IFS_4'         :{'mkey':'IFS',         'res':4,    'sim':dya_dom,
                      'label':'IFS 4'                                   },
    'GEOS_3'        :{'mkey':'GEOS',        'res':3,    'sim':dya_dom,
                      'label':'GEOS 3'                                  },
    'ARPEGE-NH_2.5' :{'mkey':'ARPEGE-NH',   'res':2.5,  'sim':dya_dom,
                      'label':'ARPEGE-NH 2.5'                           },
    'FV3_3.25'      :{'mkey':'FV3',         'res':3.25, 'sim':dya_dom,
                      'label':'FV3 3.25'                                },

    ## all others
    #'COSMO_12'      :{'mkey':'COSMO',       'res':12,   'sim':'SA_3lev'},
    #'NICAM_7'       :{'mkey':'NICAM',       'res':7,    'sim':dya_dom},
    #'ICON_10'       :{'mkey':'ICON',        'res':10,   'sim':dya_dom},
    #'MPAS_7.5'      :{'mkey':'MPAS',        'res':7.5,  'sim':dya_dom},
    #'IFS_9'         :{'mkey':'IFS',         'res':9,    'sim':dya_dom},
}
test_ERA5_sims = {
    'ERAI_12_2_2.2'     :{'mkey':'COSMO',   'res':2.2,  'sim':'test_ERAI_12_2',
                            'label':'ERAI-12-02 2km'},
    'ERA5_12_2_2.2'     :{'mkey':'COSMO',   'res':2.2,  'sim':'test_ERA5_12_2',
                            'label':'ERA5@6hr-12-02 2km'},
    'ERA5_4_2_3hr_2.2'  :{'mkey':'COSMO',   'res':2.2,  'sim':'test_ERA5_4_2_3hr',
                            'label':'ERA5@3hr-04-02 2km'},
    'ERA5_4_2_1hr_2.2'  :{'mkey':'COSMO',   'res':2.2,  'sim':'test_ERA5_4_2_1hr',
                            'label':'ERA5@1hr-04-02 2km'},
    'ERA5_12_4_2_2.2'   :{'mkey':'COSMO',   'res':2.2,  'sim':'test_ERA5_12_4_2_inner',
                            'label':'ERA5@6hr-12-04-02 2km'},

    'ERA5_4_2_3hr_4.4'  :{'mkey':'COSMO',   'res':4.4,  'sim':'test_ERA5_4_2_3hr',
                            'label':'ERA5@3hr-04-02 4km'},
    'ERA5_4_2_1hr_4.4'  :{'mkey':'COSMO',   'res':4.4,  'sim':'test_ERA5_4_2_1hr',
                            'label':'ERA5@1hr-04-02 4km'},
    'ERA5_12_4_2_4.4'   :{'mkey':'COSMO',   'res':4.4,  'sim':'test_ERA5_12_4_2_outer',
                            'label':'ERA5@6hr-12-04-02 4km'},

    #'ERAI_12_2_12'      :{'mkey':'COSMO',   'res':12,  'sim':'test_ERAI_12_2',
    #                        'label':'ERAI-12-2 12km'},
    #'ERA5_12_2_12'      :{'mkey':'COSMO',   'res':12,  'sim':'test_ERA5_12_2',
    #                        'label':'ERA5@6hr-12-2 12km'},
    #'ERA5_12_4_2_12'    :{'mkey':'COSMO',   'res':12,  'sim':'test_ERA5_12_4_2_outer',
    #                        'label':'ERA5@6hr-12-04-02 12km'},
}


## run settings
i_save_fig = 0
i_remap = 0
i_debug = 0

var_name = 'SWUTOA'

# plotting settings
i_plot_obs = True

### time
### time
if i_remap:
    first_date = datetime(2016,8,1)
    last_date = datetime(2016,8,31)
else:
    first_date = datetime(2016,8,3)
    #last_date = datetime(2016,8,31)
    #last_date = datetime(2016,9,9)
    last_date = datetime(2016,8,5)
frequency = timedelta(hours=3)

# remapping
remap_padding = 1.0



stretch = 1.3
plot_var = 'osw'
#plot_var = 'olw'
#plot_var = 'tqc'
#plot_var = 'uv10m'
#plot_var = 'inv_hgt'
#plot_var = 'cld_hgt'
#plot_var = 'inv_str'
#plot_var = 'slhflx'
#plot_var = 'precip'
#plot_var = 'qv500m'

#run_mode = 'dya'
run_mode = 'test_ERA5'

## script specific run configs

run_configs = {
    'dya':  {
        'subplts':  {'left':0.08,  'bottom':0.21,
                       'right':0.98, 'top':0.95,
                       'wspace':0.03,'hspace':0.19},
        'use_sims': dya_sims,
        'domain':   dom_SEA_Sc,
        'figsize':  (13.9*stretch,8.0*stretch),
        'nrows':    3,
        'ncols':    4,
    },

    'test_ERA5':  {
        'subplts':  {'left':0.08,  'bottom':0.21,
                       'right':0.98, 'top':0.95,
                       'wspace':0.03,'hspace':0.19},
        'use_sims': test_ERA5_sims,
        'domain':   dom_SEA_Sc,
        'figsize':  (13.9*stretch,8.0*stretch),
        'nrows':    3,
        'ncols':    3,
    },
}


var_configs = {
    'osw':{
        'var_name'  :'SWUTOA',
        'remapped'  :True,
        #'min_max'   :(0,'obs'),
        'min_max'   :(0,None),
        'var_plot_name' :'osw',
        'cmap'      :'cubehelix',
    },
    'olw':{
        'var_name'  :'LWUTOA',
        'remapped'  :True,
        'min_max'   :(None,None),
        'var_plot_name' :'olw',
        'cmap'      :'rainbow',
    },
    'tqc':{
        'var_name'  :'TQC',
        'remapped'  :True,
        'min_max'   :(0,0.08),
        'var_plot_name' :'tqc',
        'cmap'      :'clouds',
    },
    'uv10m':{
        'var_name'  :'UV10M',
        'remapped'  :True,
        'min_max'   :(2.5,None),
        'var_plot_name' :'uv10m',
        'cmap'      :'blue_red',
    },
    'inv_hgt':{
        'compute_exact':False,
        'var_name'  :'INVHGT',
        'remapped'  :True,
        'min_max'   :(None,None),
        'var_plot_name' :'invhgt',
        'cmap'      :'cubehelix',
    },
    'cld_hgt':{
        'compute_exact':False,
        'var_name'  :'CLDHGT',
        'remapped'  :True,
        'min_max'   :(None,2000),
        'var_plot_name' :'cldhgt',
        'cmap'      :'cubehelix',
    },
    'inv_str':{
        'compute_exact':False,
        'var_name'  :'INVSTR',
        'remapped'  :True,
        'min_max'   :(0.,0.04),
        'var_plot_name' :'invstr',
        'cmap'      :'cubehelix',
    },
    'slhflx':{
        'var_name'  :'SLHFLX',
        'remapped'  :True,
        'min_max'   :(None,None),
        'var_plot_name' :'slhflx',
        'cmap'      :'colorful',
    },
    'precip':{
        'var_name'  :'PP',
        'remapped'  :True,
        'min_max'   :(0,0.10),
        'var_plot_name' :'precip',
        'cmap'      :'rain',
    },
    'qv500m':{
        'var_name'  :'QV',
        'interp_sel':{'alt':1500},
        'remapped'  :True,
        'min_max'   :(None,None),
        'var_plot_name' :'qv500m',
        'cmap'      :'cubehelix',
    },


}
cfg = run_configs[run_mode]
cfg.update(var_configs[plot_var])

