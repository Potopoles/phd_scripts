from importlib import import_module, reload
from types import SimpleNamespace

from package.functions import (import_namelist)

def org_plot_var(gs, pan_cfg, nl_glob, PO, 
    perform_generic_steps
):
    if 'height' in pan_cfg:
        row_sel = slice(pan_cfg['rowi'],pan_cfg['rowi']+pan_cfg['height']+1)
    else:
        row_sel = pan_cfg['rowi']
    if 'width' in pan_cfg:
        col_sel = slice(pan_cfg['coli'],pan_cfg['coli']+pan_cfg['width']+1)
    else:
        col_sel = pan_cfg['coli']
    ax = PO.fig.add_subplot(gs[row_sel,col_sel])
    #if 'ana_cfg' not in pan_cfg:
    #    ax.set_visible(False)
    #    return()
    ana_cfg = pan_cfg['ana_cfg']
    gen_cfg = pan_cfg['gen_cfg']

    #if ana_cfg['ana_number'] in [4]:
    #    if isinstance(col_sel, slice):
    #        PO.cax = PO.fig.add_subplot(gs[row_sel,col_sel.stop])
    #    else:
    #        PO.cax = PO.fig.add_subplot(gs[row_sel,col_sel+1])

    # INITIALIZE ANALYSIS OBJECT
    ##########################################################################
    Analysis = getattr(import_module(
                        'an_{:02d}'.format(ana_cfg['ana_number'])),
                        'Analysis_{:02d}'.format(ana_cfg['ana_number']))
    ana = Analysis(nl=SimpleNamespace())
    # PREPARE NAMELIST
    ##########################################################################
    nl_ana_raw = import_module('nl_{:02d}'.format(ana_cfg['ana_number']))
    # make sure namelist is reloaded from scratch without modifications
    # from last panel
    reload(nl_ana_raw)
    # import attributes from default analysis namelist
    import_namelist(ana.nl, nl_ana_raw)
    # copy serial selector
    ana.nl.time_plt_sel = None
    # copy attributes from analysis plotting namelist 
    nl_ana_plot_raw = import_module('nl_plot_{:02d}'.format(ana_cfg['ana_number']))
    setattr(ana.nl, 'nlp', getattr(nl_ana_plot_raw, 'nlp'))
    # some additional settings
    ana.nl.i_debug = nl_glob.i_debug
    #ana.nl.ANA_NATIVE_domain = nl_glob.ANA_NATIVE_domain
    ana.nl.computation_mode = 'load'
    #ana.nl.n_par = nl_glob.n_par
    # copy attributes from panel dict (ana_cfg) to analysis namelist (ana_nl)
    for attr_key,attr in ana_cfg.items():
        #print(attr_key)
        setattr(ana.nl, attr_key, attr)

    # prepare actual analysis namelist
    ana.prepare_namelist()

    # RUN ANALYSIS FOR PLOTTING
    ##########################################################################
    # load data
    ana.indiv_targ_members = ana.load_data()

    # configure target members
    targ_members = ana.prepare_for_plotting(ana.indiv_targ_members)

    # plot
    ana.draw_axis(PO, targ_members, ax)

    # GENERIC CONFIGURATION STEPS
    ##########################################################################
    perform_generic_steps(ax, gen_cfg)


