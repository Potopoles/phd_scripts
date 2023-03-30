#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Compute cross-sections of QC and QI
author			Christoph Heim
date created    11.10.2019
date changed    11.10.2019 
usage           args:
                1st:    number of parallel tasks
"""
###############################################################################
import os, collections
#from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
import nl_09 as nl
from nl_plot import nlp
from package.nl_models import nlm
from package.nl_variables import nlv, dimx, dimy, dimz, dimt
from package.model_pp import preproc_model, subsel_domain
from package.plot_functions import PlotOrganizer
from package.utilities import Timer
from package.member import Member
from package.variable import Variable
from package.MP import TimeStepMP
###############################################################################


###############################################################################
# compute a cross-section
###############################################################################
def compute_cross_sections(ts):
    """
    """

    timer = Timer()

    ts_string = '{:%Y-%m-%d %H:%M}'.format(ts)
    ts_code = '{:%Y%m%d_%H%M}'.format(ts)

    vars = {}
    for var_name in nl.var_names:
        print(var_name)
        dims = nlv[var_name]['dims']

        sims = {}
        for mkey,slist in nl.use_sims.items():
            if nl.i_verbosity:
                print(mkey)
            timer.start(mkey)
            for sdict in slist:
                skey = '{}_{:g}'.format(mkey,sdict['res'])  
                if nl.i_verbosity:
                    print('\t {}'.format(skey))

                sim_data_dir = os.path.join(nl.sim_base_dir, skey,
                                     sdict['sim'])
                ds = xr.open_dataset(os.path.join(sim_data_dir,
                                                  '{}.nc'.format(var_name)))
                ds = preproc_model(ds, mkey, sim_data_dir, nl,
                                   nl.domain, dims=dims)
                
                if dimt in  dims:
                    ds = ds.sel(time=ts)
                #ds = subsel_domain(ds, mkey, nl.domain)
                ds = ds.sel(lat=nl.cfg['lat_slice'])
                ds = ds.sel(lon=nl.cfg['lon_slice'])
                #ds = ds.max(dim='lon')
                if dimz in  dims:
                    ds = ds.sortby('alt')
                    ds = ds.sel(alt=slice(0,10000))
                vkey = nlm[mkey]['vkeys'][var_name]
                var = ds[vkey]

                member = Member(var, {'label':skey})
                sims[skey] = member
            timer.stop(mkey)

        var = Variable(sims)   
        var.calc_statistics()

        vars[var_name] = var


    timer.start('plot')
    nrows = nl.cfg['nrows']
    ncols = nl.cfg['ncols']

    name_dict = collections.OrderedDict()
    name_dict[''] = ts_code

    #nlp['projection']           = '3d' 

    #PO = PlotOrganizer(nl.i_save_fig,
    #                   path=os.path.join(nl.plot_base_dir,'test'),
    #                   name_dict=name_dict, nlp=nlp)
    #fig,axes = PO.initialize_plot(nrow=nrows, ncol=ncols)


    col_ind = 0
    row_ind = 0
    for mkey,slist in nl.use_sims.items():
        for sdict in slist:
            skey = '{}_{:g}'.format(mkey,sdict['res'])  
            print(skey)
            #ax = axes[row_ind, col_ind]

            HSURF   = vars['HSURF'].members[skey]
            QC  = vars['QC'].members[skey]
            #QI  = vars['QI'].members[skey]
            lon = QC.field.lon.values
            lat = QC.field.lat.values
            alt = QC.field.alt.values

            #vert_inds = [0,9,19,29,39,49,59,60,61,62,63]
            #alt = alt[vert_inds]

            hsurf = HSURF.field.values.squeeze()

            #fact_alt = 1/(1000*5)
            fact_lon = 1
            fact_lat = 1
            fact_alt = 1/(np.max(alt) - np.min(alt))

            #fact_alt /= 0.8
            #fact_alt /= 0.9
            fact_alt /= 1.2

            lon *= fact_lon
            lat *= fact_lat
            alt *= fact_alt
            hsurf *= fact_alt

            qc = np.transpose(QC.field.values, (2,1,0))
            qc[np.isnan(qc)] = 0.

            #qi = np.transpose(QI.field.values, (2,1,0))
            #qi[np.isnan(qi)] = 0.
            lon3d,lat3d,alt3d = np.mgrid[lon[0]:lon[-1]:len(lon)*1j,
                                         lat[0]:lat[-1]:len(lat)*1j,
                                         alt[0]:alt[-1]:len(alt)*1j]
            hsurf = np.transpose(hsurf, (1,0))
            lon2d,lat2d = np.mgrid[lon[0]:lon[-1]:len(lon)*1j,
                                   lat[0]:lat[-1]:len(lat)*1j,]

            #qc = qc[:,:,vert_inds]
            #qi = qi[:,:,vert_inds]

            #nz = 100
            #qc_full = np.zeros((qc.shape[0], qc.shape[1], nz))
            #qc_full[:,:,0:61] = qc[:,:,0:61]
            #qc_full[:,:,61:] = 5
            #print(qc_full.shape)
            #print(qc_full[10,10,:])
            #lon3d,lat3d,alt3d_full = np.mgrid[lon[0]:lon[-1]:len(lon)*1j,
            #                             lat[0]:lat[-1]:len(lat)*1j,
            #                             0:10000:nz*1j]

            #alt3d_full *= fact_alt
            #print(alt3d[10,10,:])
            #print(alt3d_full[10,10,:])
            ##quit()
            

            print(lon3d.shape)
            print(lat3d.shape)
            print(alt3d.shape)
            print(qc.shape)
            print('2d')
            print(lon2d.shape)
            print(lat2d.shape)
            print(hsurf.shape)

            from mayavi import mlab
            mlab.options.offscreen = True
            fig = mlab.figure(size=(1100,800))
            surf = mlab.surf(lon2d,lat2d,hsurf, colormap='pink')
            #surf = mlab.surf(lon2d,lat2d,hsurf, colormap='terrain')
            contour = mlab.contour3d(lon3d,lat3d,alt3d,qc, colormap='Blues')
            #contour = mlab.contour3d(lon3d,lat3d,alt3d_full,qc_full, colormap='Blues')
            #contour = mlab.contour3d(lon3d,lat3d,alt3d,qi, colormap='Greens')
            mlab.view(azimuth=150, elevation=60, distance=3.0)
            mlab.move(forward=-8, up=-1, right=0.5)
            #mlab.show()
            mlab.savefig('topo_alps_{}.png'.format(skey))
            #quit()
            
            col_ind += 1






if __name__ == '__main__':

    timer = Timer(mode='seconds')

    time_steps = np.arange(nl.time_sel.start,
                           nl.time_sel.stop, nl.time_dt).tolist()

    tsmp = TimeStepMP(time_steps, njobs=nl.njobs, run_async=False)
    tsmp.run(compute_cross_sections, fargs={}, step_args=None)

    # merge timings from each run with main timer and print report
    for output in tsmp.output:
        timer.merge_timings(output['timer'])

    timer.print_report()
