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

cosmo_change = {
    'mem_oper':     'diff',
    'mem_keys':     ['COSMO_3.3_pgw', 'COSMO_3.3_ctrl'],
}
cosmo_rel_change = {
    'mem_oper':     'rel0.001',
    'mem_keys':     ['COSMO_3.3_pgw', 'COSMO_3.3_ctrl'],
}


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
name_dict = {'fig_01':'trades_lon_normi'}

default_ana_cfgs = {
    'time_periods':     time_periods_ana,
    'name_dict_append': {},
    'time_periods':time_periods_ana_SON,
    'name_dict_append': {'month':'SON'},
    'time_periods':time_periods_ana_DJF,
    'name_dict_append': {'month':'DJF'},
    'time_periods':time_periods_ana_MAM,
    'name_dict_append': {'month':'MAM'},
    'time_periods':time_periods_ana_JJA,
    'name_dict_append': {'month':'JJA'},

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


cfg_show_xlabel = ['5,0','5,1']
cfg_show_yticks = ['0,0','0,3','1,0','1,3','2,0','2,3','3,0','3,1','4,0','4,1','5,0','5,1']
cfg_show_ylabel = ['0,0','0,3','1,0','1,3','2,0','2,3','3,0','3,1','4,0','4,1','5,0','5,1']


## this is not really used but just created to make sure all analyses work.
PO = PlotOrganizer(
    i_save_fig=nl_glob.i_save_fig,
    path=os.path.join(nl_glob.plot_base_dir),
    name_dict=name_dict,
    nlp=nlp, 
    geo_plot=False
)
PO.fig = plt.figure(constrained_layout=False, figsize=(14,13))
gs = GridSpec(
    6,9, PO.fig, 
    width_ratios=[1,2,0.4,1,0.5,1,2,0.4,1], 
    #height_ratios=[1,1,1,1]
)
gs.update(
    left=0.05,
    right=0.99,
    bottom=0.07,
    top=0.96,
    wspace=0.10,
    hspace=0.50,
)


pan_cfgs = {
    '0,0': {
        'rowi':0,'coli':0,
        'ana_cfg': {
            'ana_number':       2,
            'mem_cfgs':         ['COSMO_3.3_ctrl'],
            'var_names':        ['CLDFNORMI'], 
            'plot_domain':      dom_trades_west,
        },
        'gen_cfg': {
        },
    },
    '0,1': {
        'rowi':0,'coli':1,
        #'width':2,
        'ana_cfg': {
            'ana_number':       4,
            'mem_cfgs':         ['COSMO_3.3_ctrl'],
            'var_type':         'CLDF_CLDF', 
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'CTRL {} [{}]'.format(nlv['CLDF']['label'], get_plt_units('CLDF')),
            'axvline':          {'x':-15,'color':'k','linestyle':'--','linewidth':0.5},
        },
    },
    '0,2': {
        'rowi':0,'coli':3,
        'ana_cfg': {
            'ana_number':       2,
            'mem_cfgs':         ['COSMO_3.3_ctrl'],
            'var_names':        ['CLDFNORMI'], 
            'plot_domain':      dom_trades_east,
        },
        'gen_cfg': {
        },
    },

    '0,3': {

        'rowi':0,'coli':5,
        'ana_cfg': {
            'ana_number':       2,
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLDFNORMI'], 
            'plot_domain':      dom_trades_west,
        },
        'gen_cfg': {
        },
    },
    '0,4': {
        'rowi':0,'coli':6,
        'ana_cfg': {
            'ana_number':       4,
            'mem_cfgs':         [cosmo_change],
            'var_type':         'CLDF_CLDF', 
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'PGW$-$CTRL {} [{}]'.format(nlv['CLDF']['label'], get_plt_units('CLDF')),
            'axvline':          {'x':-15,'color':'k','linestyle':'--','linewidth':0.5},
        },
    },
    '0,5': {
        'rowi':0,'coli':8,
        'ana_cfg': {
            'ana_number':       2,
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['CLDFNORMI'], 
            'plot_domain':      dom_trades_east,
        },
        'gen_cfg': {
        },
    },



    '1,0': {
        'rowi':1,'coli':0,
        'ana_cfg': {
            'ana_number':       2,
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['POTTNORMI'], 
            'plot_domain':      dom_trades_west,
        },
        'gen_cfg': {
        },
    },
    '1,1': {
        'rowi':1,'coli':1,
        #'width':2,
        'ana_cfg': {
            'ana_number':       4,
            'mem_cfgs':         [cosmo_change],
            'var_type':         'POTT_CLDF', 
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'CTRL {} [{}]'.format(nlv['POTT']['label'], get_plt_units('POTT')),
            'axvline':          {'x':-15,'color':'k','linestyle':'--','linewidth':0.5},
        },
    },
    '1,2': {
        'rowi':1,'coli':3,
        'ana_cfg': {
            'ana_number':       2,
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['POTTNORMI'], 
            'plot_domain':      dom_trades_east,
        },
        'gen_cfg': {
        },
    },

    '1,3': {

        'rowi':1,'coli':5,
        'ana_cfg': {
            'ana_number':       2,
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['RHNORMI'], 
            'plot_domain':      dom_trades_west,
        },
        'gen_cfg': {
        },
    },
    '1,4': {
        'rowi':1,'coli':6,
        'ana_cfg': {
            'ana_number':       4,
            'mem_cfgs':         [cosmo_change],
            'var_type':         'RH_CLDF', 
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'PGW$-$CTRL {} [{}]'.format(nlv['RH']['label'], get_plt_units('RH')),
            'axvline':          {'x':-15,'color':'k','linestyle':'--','linewidth':0.5},
        },
    },
    '1,5': {
        'rowi':1,'coli':8,
        'ana_cfg': {
            'ana_number':       2,
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['RHNORMI'], 
            'plot_domain':      dom_trades_east,
        },
        'gen_cfg': {
        },
    },



    '2,0': {
        'rowi':2,'coli':0,
        'ana_cfg': {
            'ana_number':       2,
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['BVFNORMI'], 
            'plot_domain':      dom_trades_west,
        },
        'gen_cfg': {
        },
    },
    '2,1': {
        'rowi':2,'coli':1,
        'ana_cfg': {
            'ana_number':       4,
            'mem_cfgs':         [cosmo_change],
            'var_type':         'BVF_CLDF', 
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'PGW$-$CTRL {} [{}]'.format(nlv['BVF']['label'], get_plt_units('BVF')),
            'axvline':          {'x':-15,'color':'k','linestyle':'--','linewidth':0.5},
        },
    },
    '2,2': {
        'rowi':2,'coli':3,
        'ana_cfg': {
            'ana_number':       2,
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['BVFNORMI'], 
            'plot_domain':      dom_trades_east,
        },
        'gen_cfg': {
        },
    },



    '2,3': {
        'rowi':2,'coli':5,
        'ana_cfg': {
            'ana_number':       2,
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['QVNORMI'], 
            'plot_domain':      dom_trades_west,
        },
        'gen_cfg': {
        },
    },
    '2,4': {
        'rowi':2,'coli':6,
        'ana_cfg': {
            'ana_number':       4,
            'mem_cfgs':         [cosmo_change],
            'var_type':         'QV_CLDF', 
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'PGW$-$CTRL {} [{}]'.format(nlv['QV']['label'], get_plt_units('QV')),
            'axvline':          {'x':-15,'color':'k','linestyle':'--','linewidth':0.5},
        },
    },
    '2,5': {
        'rowi':2,'coli':8,
        'ana_cfg': {
            'ana_number':       2,
            'mem_cfgs':         [cosmo_change],
            'var_names':        ['QVNORMI'], 
            'plot_domain':      dom_trades_east,
        },
        'gen_cfg': {
        },
    },



    '3,0': {
        'rowi':3,'coli':1,
        #'width':2,
        'ana_cfg': {
            'ana_number':       15,
            'mem_cfgs':         [cosmo_change],
            'plot_dict':        {'l1':['LTS','INVSTRV','EIS'],'r1':['TSURF'],'r2':['T@alt=3000']}, 
            'i_plot_legend':    1,
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'PGW$-$CTRL',
            'axvline':          {'x':-15,'color':'k','linestyle':'--','linewidth':0.5},
        },
    },
    '3,1': {
        'rowi':3,'coli':6,
        #'width':2,
        'ana_cfg': {
            'ana_number':       15,
            'mem_cfgs':         [cosmo_change],
            'plot_dict':        {'l1':['DQVINV'],'r1':['RH@alt=3000'],'r2':['POTTHDIV@alt=300']}, 
            'i_plot_legend':    1,
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'PGW$-$CTRL',
            'axvline':          {'x':-15,'color':'k','linestyle':'--','linewidth':0.5},
        },
    },



    '4,0': {
        'rowi':4,'coli':1,
        #'width':2,
        'ana_cfg': {
            'ana_number':       15,
            'mem_cfgs':         [cosmo_rel_change],
            'plot_dict':        {'l1':['W@alt=3000'],'r1':['ENTR'],'r2':['UV10M']}, 
            'i_plot_legend':    1,
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'PGW/CTRL$-$1',
            'axvline':          {'x':-15,'color':'k','linestyle':'--','linewidth':0.5},
        },
    },
    '4,1': {
        'rowi':4,'coli':6,
        #'width':2,
        'ana_cfg': {
            'ana_number':       15,
            'mem_cfgs':         [cosmo_rel_change],
            #'plot_dict':        {'l1':['SLHFLX'],'r1':['SSHFLX'],'r2':['PP']}, 
            'plot_dict':        {'l1':['SLHFLX'],'r1':['SSHFLX'],'r2':['SBUOYIFLX']}, 
            'i_plot_legend':    1,
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'PGW/CTRL$-$1',
            'axvline':          {'x':-15,'color':'k','linestyle':'--','linewidth':0.5},
        },
    },



    '5,0': {
        'rowi':5,'coli':1,
        'ana_cfg': {
            'ana_number':       15,
            'mem_cfgs':         [cosmo_change],
            #'plot_dict':        {'l1':['INVHGT'],'r1':['LCL','LOWCLDBASE'],'r2':['DINVHGTLCL','DINVHGTLOWCLDBASE']}, 
            'plot_dict':        {'l1':['INVHGT'],'r1':['LCL',],'r2':['LOWCLDBASE']}, 
            'i_plot_legend':    1,
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            'title':            'PGW$-$CTRL',
            'axvline':          {'x':-15,'color':'k','linestyle':'--','linewidth':0.5},
        },
    },
    '5,1': {
        'rowi':5,'coli':6,
        #'width':2,
        'ana_cfg': {
            'ana_number':       15,
            #'mem_cfgs':         [cosmo_rel_change],
            'mem_cfgs':         [cosmo_change],
            'plot_dict':        {'l1':['CLCL'],'r1':['CRESWNDTOA']}, 
            'i_plot_legend':    1,
            'plot_domain':      dom_trades_full,
        },
        'gen_cfg': {
            #'title':            'PGW/CTRL$-$1',
            'title':            'PGW$-$CTRL',
            'axvline':          {'x':-15,'color':'k','linestyle':'--','linewidth':0.5},
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
