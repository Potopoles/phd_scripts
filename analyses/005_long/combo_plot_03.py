import os
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from types import SimpleNamespace

from base.nl_plot_global import nlp
from base.nl_time_periods import *
from base.nl_domains import *
from package.nl_variables import nlv,get_plt_units
from package.plot_functions import PlotOrganizer
from functions_combo_plot import org_plot_var

mem_dicts = dict(ctrl=[],pgw=[],diff=[],rel=[])
tp_dict = {
    'SON':  time_periods_ana_SON,
    'DJF':  time_periods_ana_DJF,
    'MAM':  time_periods_ana_MAM,
    'JJA':  time_periods_ana_JJA,
    'full': time_periods_ana, 
}
colors = ['red','orange','green','blue','k']
linestyles = ['-','-','-','-','-']
linewidths = [1,1,1,1,2]
i = 0
for tp_key,tp in tp_dict.items():
    mem_dicts['ctrl'].append({
        'mem_key':      'COSMO_3.3_ctrl', 
        'time_periods': tp,
        'color':        colors[i], 
        #'linestyle':    linestyles[i], 
        #'linestyle':    '-', 
        'linewidth':    linewidths[i], 
        'label':        tp_key, 
    })
    mem_dicts['pgw'].append({
        'mem_key':      'COSMO_3.3_pgw', 
        'time_periods': tp,
        'color':        colors[i], 
        'linestyle':    '--', 
        'linewidth':    linewidths[i], 
        'label':        tp_key, 
    })
    mem_dicts['diff'].append({
        'mem_oper':     'diff',
        'mem_keys':     ['COSMO_3.3_pgw', 'COSMO_3.3_ctrl'],
        'time_periods': tp,
        'color':        colors[i], 
        #'linestyle':    linestyles[i], 
        'linewidth':    linewidths[i], 
        'label':        tp_key, 
    })
    mem_dicts['rel'].append({
        'mem_oper':     'rel0.001',
        'mem_keys':     ['COSMO_3.3_pgw', 'COSMO_3.3_ctrl'],
        'time_periods': tp,
        'color':        colors[i], 
        #'linestyle':    linestyles[i], 
        'linewidth':    linewidths[i], 
        'label':        tp_key, 
    })
    i += 1

mem_dicts['abs'] = []
mem_dicts['abs'].extend(mem_dicts['ctrl'])
mem_dicts['abs'].extend(mem_dicts['pgw'])


def perform_generic_steps(ax, gen_cfg):
    if not gen_cfg['show_xlabel']:
        ax.set_xlabel('') 
    if not gen_cfg['show_ylabel']:
        ax.set_ylabel('') 
    if not gen_cfg['show_yticks']:
        ax.yaxis.set_ticklabels([])

    if 'title' in gen_cfg:
        ax.set_title(gen_cfg['title'])

    if 'axvline' in gen_cfg:
        ax.axvline(**gen_cfg['axvline'])

nl_glob = SimpleNamespace()
nl_glob.i_debug = 4
nl_glob.i_save_fig = 3
nl_glob.plot_base_dir = '/net/o3/hymet_nobackup/heimc/plots/005_long/combo_plots'
name_dict = {'fig_03':'trades_lon_normi'}

default_ana_cfgs = {
    'i_plot_legend':    0,
    'title':            '',
    ## an_02
    ## an_04
    'i_add_cbar_label': 0,
    'line_along':       'lon',
    'norm_inv':         1,
}
if 'name_dict_append' in default_ana_cfgs:
    name_dict.update(default_ana_cfgs['name_dict_append'])


cfg_show_xlabel = ['3,0','3,1','3,2','3,3']
cfg_show_yticks = ['0,0','0,1','0,2','0,3','1,0','1,1','1,2','1,3','2,0','2,1','2,2','2,3','3,0','3,1','3,2','3,3','4,0','4,1']
cfg_show_ylabel = ['0,0','0,2','1,0','1,2','2,0','2,2','3,0','3,2','4,0']


## this is not really used but just created to make sure all analyses work.
PO = PlotOrganizer(
    i_save_fig=nl_glob.i_save_fig,
    path=os.path.join(nl_glob.plot_base_dir),
    name_dict=name_dict,
    nlp=nlp, 
    geo_plot=False
)
PO.fig = plt.figure(constrained_layout=False, figsize=(16,16))
gs = GridSpec(
    5,7, PO.fig, 
    width_ratios=[1,0.2,1,0.5,1,0.2,1], 
    #height_ratios=[1,1,1,1]
)
gs.update(
    left=0.05,
    right=0.95,
    bottom=0.07,
    top=0.96,
    wspace=0.10,
    hspace=0.50,
)


pan_cfgs = {
    '0,0': {
        'rowi':0,'coli':0,
        #'width':2,
        'ana_cfg': {
            'ana_number':       15,
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['CRESWNDTOA']}, 
            'i_plot_legend':    1,
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'CTRL',
        },
    },
    '0,1': {
        'rowi':0,'coli':2,
        'ana_cfg': {
            'ana_number':       15,
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['CRESWNDTOA']}, 
            'i_plot_legend':    0,
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'PGW$-$CTRL',
        },
    },

    '0,2': {
        'rowi':0,'coli':4,
        'ana_cfg': {
            'ana_number':       15,
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['TSURF']}, 
            'i_plot_legend':    0,
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'CTRL',
        },
    },
    '0,3': {
        'rowi':0,'coli':6,
        'ana_cfg': {
            'ana_number':       15,
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['TSURF']}, 
            'i_plot_legend':    0,
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'PGW$-$CTRL',
        },
    },



    '1,0': {
        'rowi':1,'coli':0,
        'ana_cfg': {
            'ana_number':       15,
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['DQVINV']}, 
            'i_plot_legend':    0,
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'CTRL',
        },
    },
    '1,1': {
        'rowi':1,'coli':2,
        'ana_cfg': {
            'ana_number':       15,
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['DQVINV']}, 
            'i_plot_legend':    0,
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'PGW$-$CTRL',
        },
    },

    '1,2': {
        'rowi':1,'coli':4,
        'ana_cfg': {
            'ana_number':       15,
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['T@alt=3000']}, 
            'i_plot_legend':    0,
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'CTRL',
        },
    },
    '1,3': {
        'rowi':1,'coli':6,
        'ana_cfg': {
            'ana_number':       15,
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['T@alt=3000']}, 
            'i_plot_legend':    0,
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'PGW$-$CTRL',
        },
    },



    '2,0': {
        'rowi':2,'coli':0,
        'ana_cfg': {
            'ana_number':       15,
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['RH@alt=3000']}, 
            'i_plot_legend':    0,
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'CTRL',
        },
    },
    '2,1': {
        'rowi':2,'coli':2,
        'ana_cfg': {
            'ana_number':       15,
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['RH@alt=3000']}, 
            'i_plot_legend':    0,
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'PGW$-$CTRL',
        },
    },

    '2,2': {
        'rowi':2,'coli':4,
        'ana_cfg': {
            'ana_number':       15,
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['LTS']}, 
            'i_plot_legend':    0,
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'CTRL',
        },
    },
    '2,3': {
        'rowi':2,'coli':6,
        'ana_cfg': {
            'ana_number':       15,
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['LTS']}, 
            'i_plot_legend':    0,
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'PGW$-$CTRL',
        },
    },



    '3,0': {
        'rowi':3,'coli':0,
        'ana_cfg': {
            'ana_number':       15,
            'mem_cfgs':         mem_dicts['ctrl'],
            #'plot_dict':        {'l1':['POTTHDIV@alt=300']}, 
            'plot_dict':        {'l1':['UV10M']}, 
            'i_plot_legend':    0,
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'CTRL',
        },
    },
    '3,1': {
        'rowi':3,'coli':2,
        'ana_cfg': {
            'ana_number':       15,
            'mem_cfgs':         mem_dicts['diff'],
            #'plot_dict':        {'l1':['POTTHDIV@alt=300']}, 
            'plot_dict':        {'l1':['UV10M']}, 
            'i_plot_legend':    0,
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'PGW$-$CTRL',
        },
    },

    '3,2': {
        'rowi':3,'coli':4,
        'ana_cfg': {
            'ana_number':       15,
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['ENTR']}, 
            'i_plot_legend':    0,
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'CTRL',
        },
    },
    '3,3': {
        'rowi':3,'coli':6,
        'ana_cfg': {
            'ana_number':       15,
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['ENTR']}, 
            'i_plot_legend':    0,
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'PGW$-$CTRL',
        },
    },




    '4,0': {
        'rowi':4,'coli':0,
        'ana_cfg': {
            'ana_number':       15,
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['INVHGT']}, 
            'i_plot_legend':    0,
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'CTRL',
        },
    },
    '4,1': {
        'rowi':4,'coli':2,
        'ana_cfg': {
            'ana_number':       15,
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['INVHGT']}, 
            'i_plot_legend':    0,
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'PGW$-$CTRL',
        },
    },

    '4,2': {
        'rowi':4,'coli':4,
        'ana_cfg': {
            'ana_number':       15,
            'mem_cfgs':         mem_dicts['ctrl'],
            'plot_dict':        {'l1':['W@alt=3000']}, 
            'i_plot_legend':    0,
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'CTRL',
        },
    },
    '4,3': {
        'rowi':4,'coli':6,
        'ana_cfg': {
            'ana_number':       15,
            'mem_cfgs':         mem_dicts['diff'],
            'plot_dict':        {'l1':['W@alt=3000']}, 
            'i_plot_legend':    0,
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'PGW$-$CTRL',
        },
    },
}
# set default values
for pan_key,pan_cfg in pan_cfgs.items():
    if 'ana_cfg' in pan_cfg:
        for key,val in default_ana_cfgs.items():
            if key not in pan_cfg['ana_cfg']:
                pan_cfgs[pan_key]['ana_cfg'][key] = val

## generic settings
for pan_key,pan_cfg in pan_cfgs.items():
    # xlabels
    if pan_key in cfg_show_xlabel:
        pan_cfgs[pan_key]['gen_cfg']['show_xlabel'] = True
    else:
        pan_cfgs[pan_key]['gen_cfg']['show_xlabel'] = False

    # ylabels
    if pan_key in cfg_show_ylabel:
        pan_cfgs[pan_key]['gen_cfg']['show_ylabel'] = True
    else:
        pan_cfgs[pan_key]['gen_cfg']['show_ylabel'] = False

    # yaxis ticks
    if pan_key in cfg_show_yticks:
        pan_cfgs[pan_key]['gen_cfg']['show_yticks'] = True
    else:
        pan_cfgs[pan_key]['gen_cfg']['show_yticks'] = False





coli = 0
rowi = 0
for pan_key,pan_cfg in pan_cfgs.items():
    org_plot_var(gs, pan_cfg, nl_glob, PO, perform_generic_steps)
PO.finalize_plot()
