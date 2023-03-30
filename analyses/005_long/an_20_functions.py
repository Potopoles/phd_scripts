#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     functions for Cloud 3D structure
dependencies    
author			Christoph Heim
date changed    14.06.2022
date changed    14.06.2022
usage           args:
"""
###############################################################################
import os, sys
max_rec = 100000
sys.setrecursionlimit(max_rec)
print(sys.getrecursionlimit())
import numpy as np
import xarray as xr
from pathlib import Path
from numba.core import types
from numba import jit, njit
from numba.typed import Dict
from package.utilities import pickle_save, pickle_load

import matplotlib.pyplot as plt
###############################################################################

MAX_CLUSTER_SIZE = 10000
CORE_CANDS_SIZE = 10000


def load_clusters(self, member, date):
    ### SAVE DATA
    for var_name in ['CORES', 'STRATS']:
        out_base_dir = os.path.join(self.nl.ana_base_dir, 'native_grid')
        out_dir = os.path.join(out_base_dir, member.mem_dict['sim'],   
                                member.mem_dict['case'], 
                                self.nl.plot_domain['key'], 
                                member.mem_dict['freq'], var_name)
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        clinds = pickle_load(out_dir, '{}_{:%Y%m%d}'.format(var_name, date))
        member.add_var(var_name, clinds)


def compute_and_save_clusters(self, member, date):
    vars = member.vars

    W = vars['W']
    QC = vars['QC']
    W = W.interp(alt=QC.alt)
    QC_cloud = QC.where(QC >= 1E-5, np.nan)

    # find cloudy regions within cumulus updraft cores (so called cores)
    print('compute clusters cores')
    #QC_core = QC_cloud.where(W >= self.nl.W_thresh_core, np.nan).copy()
    QC_core = QC_cloud.where(W/vars['INVHGT'] >= self.nl.W_thresh_core, np.nan).copy()
    # find remaining (stratiform) cloudy regions
    QC_strat = QC_cloud.where(np.isnan(QC_core), np.nan).copy()
    #QC_core.to_netcdf('core.nc')
    #QC_strat.to_netcdf('strat.nc')
    #quit()

    ### find convective cores
    indices_cores = np.full_like(QC_core.values, -1)
    cores,indices_cores,i_got_error = find_convective_cores(
        QC_core.values, 
        indices_cores
    )
    cores.pop(0)
    # store as xarray dataarray
    INDS_3D = {}
    INDS_3D['CORES'] = xr.zeros_like(QC_core)
    INDS_3D['CORES'].data = indices_cores
    #INDS_3D['CORES'].isel(time=0).to_netcdf('core_inds.nc')
    #INDS_3D['CORES'].to_netcdf('core_inds.nc')

    if i_got_error:
        QC_core.to_netcdf('errors/QC_{}_{:%Y%m%d}.nc'.format(member.mem_dict['case'], date))
        INDS_3D['CORES'].to_netcdf('errors/INDS_{}_{:%Y%m%d}.nc'.format(member.mem_dict['case'], date))
        raise ValueError('Increase MAX_CLUSTER_SIZE please.')
    # first cluster was artificial to set numba data type of list

    ### find stratiform clouds
    print('compute clusters strats')
    indices_strat = np.full_like(QC_strat.values, np.nan)
    indices_rest = np.full_like(QC_strat.values, 0)
    strats,indices_strat,indices_rest = find_stratiform_clouds(
        QC_strat.values, 
        indices_strat,
        indices_rest,
        indices_cores,
        self.nl.model_dx,
        self.nl.max_dist_core_strat,
        QC_strat.alt.values,
    )
    # store as xarray dataarray
    INDS_3D['STRATS'] = xr.zeros_like(QC_strat)
    INDS_3D['STRATS'].data = indices_strat
    #INDS_3D['STRATS'].isel(time=0).to_netcdf('strat_inds.nc')
    #INDS_3D['STRATS'].to_netcdf('strat_inds.nc')

    #print(np.unique(STRAT_INDS_3D.values[~np.isnan(STRAT_INDS_3D.values)]))
    INDS_3D['REST'] = xr.zeros_like(QC_strat)
    INDS_3D['REST'].data = indices_rest
    #INDS_3D['REST'].to_netcdf('rest_inds.nc')
    print('{:%Y%m%d}: Could not find core for {} ({:5.3f} %) stratiform grid cells.'.format(
        date,
        INDS_3D['REST'].sum().values,
        (INDS_3D['REST'].sum() / np.sum(~np.isnan(INDS_3D['STRATS']))*100).values))

    ## store indices of cores and strats in form of xarray indices
    core_inds = [0] * len(cores)
    strat_inds = [0] * len(cores)
    for ci in range(len(cores)):
        ### core
        inds = {}
        for dim in ['timi','alti','lati','loni']:
            inds[dim] = xr.DataArray(cores[ci][dim], dims='gp')
        core_inds[ci] = inds
        ### strats
        inds = {}
        for dim in ['timi','alti','lati','loni']:
            inds[dim] = xr.DataArray(strats[ci][dim], dims='gp')
        strat_inds[ci] = inds
    member.add_var('CORES', core_inds)
    member.add_var('STRATS', strat_inds)

    ### SAVE DATA
    for var_name in ['CORES', 'STRATS']:
        if var_name == 'CORES':
            clinds = core_inds
        elif var_name == 'STRATS':
            clinds = strat_inds
        else:
            raise NotImplementedError()
        out_base_dir = os.path.join(self.nl.ana_base_dir, 'native_grid')
        out_dir = os.path.join(out_base_dir, member.mem_dict['sim'],   
                                member.mem_dict['case'], 
                                self.nl.plot_domain['key'], 
                                member.mem_dict['freq'], var_name)
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        nc_out_path = os.path.join(out_dir,
                        '{}_{:%Y%m%d}.nc'.format(var_name, date))
        INDS_3D[var_name].to_netcdf(nc_out_path)
        pickle_save(clinds, out_dir, '{}_{:%Y%m%d}'.format(var_name, date))



@njit
def new_core_cands_dict(size=100):
    core_cands = dict()
    core_cands['ind' ] = np.full(size, -1, np.int32)
    core_cands['alti'] = np.full(size, -1, np.int32)
    core_cands['lati'] = np.full(size, -1, np.int32)
    core_cands['loni'] = np.full(size, -1, np.int32)
    return(core_cands)

@njit
def get_dist(
    alti, lati, loni, 
    ref_alti, ref_lati, ref_loni, 
    alt_coord, model_dx
):
    dist = np.sqrt(
        np.power(alt_coord[alti]/1000. - alt_coord[ref_alti]/1000., 2.) +
        np.power((lati - ref_lati)*model_dx, 2.) +
        np.power((loni - ref_loni)*model_dx, 2.)
    )
    return(dist)

@njit
def find_stratiform_clouds(
        qc, 
        indices_strat, 
        indices_rest, 
        indices_cores,
        model_dx,
        max_dist_core_strat, 
        alt_coord,
    ):
    checked = np.zeros_like(qc, dtype=np.int32)
    # for each core store a cluster of stratiform clouds around it
    strats = [new_cluster_dict() for i in range(int(np.nanmax(indices_cores))+1)]
    size_strats = [0 for i in range(int(np.nanmax(indices_cores))+1)]
    for timi in range(qc.shape[0]):
        #timi = 4
        print('#############',timi)
        for alti in range(qc.shape[1]):
            #alti = 2
            #print('#####',alti)
            for lati in range(qc.shape[2]):
                #lati = 36
                #print('##',lati)
                for loni in range(qc.shape[3]):
                    #loni = 22
                    #print(loni)
                    pos_ind = loni + qc.shape[3] * lati + qc.shape[3]*qc.shape[2] * alti
                    #print(timi,alti,lati,loni)
                    #alti = 8
                    #lati = 31
                    #loni = 29
                    ### if this is already a core cell position do not do anything
                    if ~np.isnan(indices_cores[timi,alti,lati,loni]):
                        continue
                    core_cands = new_core_cands_dict(size=CORE_CANDS_SIZE)
                    indices_strat,core_cands,ncands = find_core_for_strat(
                            qc, indices_cores, indices_strat, checked, core_cands,
                            timi, alti, lati, loni,
                            max_dist_core_strat, alti, lati, loni,
                            alt_coord, model_dx,
                            pos_ind, ncands = 0
                    )
                    if ncands > 0:
                        #print(core_cands)
                        if ncands == 1:
                            core_ind = core_cands['ind'][ncands-1]
                        else:
                            dists = np.zeros(ncands, dtype=np.float32)
                            min_dist = 100000
                            min_dist_ci = -1
                            for ci in range(ncands):
                                dist = get_dist(
                                    core_cands['alti'][ci],
                                    core_cands['lati'][ci], 
                                    core_cands['loni'][ci], 
                                    alti, lati, loni,
                                    alt_coord, 
                                    model_dx
                                )
                                if dist <= min_dist:
                                    min_dist = dist
                                    min_dist_ci = ci
                                dists[ci] = dist
                            core_ind = core_cands['ind'][min_dist_ci]

                        ## insert cluster index into 4D array
                        indices_strat[timi,alti,lati,loni] = core_ind

                        ## insert cluster into stratiform cluster dictionary
                        if size_strats[core_ind] >= MAX_CLUSTER_SIZE-1:
                            raise ValueError('STRAT: increase MAX_CLUSTER_SIZE')
                        if core_ind >= len(strats)-1:
                            raise ValueError('hmmm.....')
                        strats[core_ind]['timi'][size_strats[core_ind]] = timi
                        strats[core_ind]['alti'][size_strats[core_ind]] = alti
                        strats[core_ind]['lati'][size_strats[core_ind]] = lati
                        strats[core_ind]['loni'][size_strats[core_ind]] = loni
                        size_strats[core_ind] += 1

                    ## no core found
                    else:
                        ### is it a stratiform cloudy grid cell without any core?
                        if ~np.isnan(qc[timi,alti,lati,loni]):
                            indices_rest[timi,alti,lati,loni] = 1
                    #quit()
        #return(strats,indices_strat,indices_rest)

    ## remove unused array positions for strats
    for core_ind in range(len(strats)):
        ngp = np.sum(strats[core_ind]['timi'] >= 0)
        #print(ngp)
        for dim in ['timi','alti','lati','loni']:
            strats[core_ind][dim] = strats[core_ind][dim][:ngp]
    return(strats,indices_strat,indices_rest)

#@njit
@njit(boundscheck=True)
def find_core_for_strat(
        qc, indices_cores, indices_strat, checked, core_cands,
        timi, alti, lati, loni,
        max_dist, ref_alti, ref_lati, ref_loni,
        alt_coord, model_dx,
        pos_ind, ncands = 0
    ):
    #print(alti,lati,loni)
    ### was this gp not checked before by another neighbor?
    if checked[timi,alti,lati,loni] != pos_ind:
        checked[timi,alti,lati,loni] = pos_ind
        dist = get_dist(
            alti, lati, loni, 
            ref_alti, ref_lati, ref_loni, 
            alt_coord, model_dx
        )
        #print('dist {}'.format(dist))
        #quit()
        ### is this gp close enough to reference point?
        if dist <= max_dist:
            ### is this a core?
            if ~np.isnan(indices_cores[timi,alti,lati,loni]):
                if ncands >= core_cands['ind'].size-1:
                    raise ValueError('Increase size of core_cands')
                #print('Found core!')
                #print(indices_cores[timi,alti,lati,loni])
                core_cands['ind' ][ncands] = indices_cores[timi,alti,lati,loni]
                core_cands['alti'][ncands] = alti
                core_cands['lati'][ncands] = lati
                core_cands['loni'][ncands] = loni
                ncands += 1
            else:
                ### is it a stratiform cloudy grid cell?
                if ~np.isnan(qc[timi,alti,lati,loni]):
                    #print('lookup')
                    ### look for neighbors in vertical direction
                    for alti2 in [alti-1,alti+1]:
                        # consider boundaries
                        if (alti2 >= 0) and (alti2 < qc.shape[1]):
                            #print('dive alt from {},{},{} to {},{},{}'.format(alti,lati,loni,alti2,lati,loni))
                            indices_strat,core_cands,ncands = find_core_for_strat(
                                qc, indices_cores, indices_strat, checked, core_cands,
                                timi, alti2, lati, loni,
                                max_dist, ref_alti, ref_lati, ref_loni,
                                alt_coord, model_dx,
                                pos_ind, ncands,
                            )
                    ### look for neighbors in meridional direction
                    for lati2 in [lati-1,lati+1]:
                        # consider boundaries
                        if (lati2 >= 0) and (lati2 < qc.shape[2]):
                            #print('dive lat from {},{},{} to {},{},{}'.format(alti,lati,loni,alti,lati2,loni))
                            indices_strat,core_cands,ncands = find_core_for_strat(
                                qc, indices_cores, indices_strat, checked, core_cands,
                                timi, alti, lati2, loni,
                                max_dist, ref_alti, ref_lati, ref_loni,
                                alt_coord, model_dx,
                                pos_ind, ncands,
                            )
                    ### look for neighbors in zonal direction
                    for loni2 in [loni-1,loni+1]:
                        # consider boundaries
                        if (loni2 >= 0) and (loni2 < qc.shape[3]):
                            #print('dive lon from {},{},{} to {},{},{}'.format(alti,lati,loni,alti,lati,loni2))
                            indices_strat,core_cands,ncands = find_core_for_strat(
                                qc, indices_cores, indices_strat, checked, core_cands,
                                timi, alti, lati, loni2,
                                max_dist, ref_alti, ref_lati, ref_loni,
                                alt_coord, model_dx,
                                pos_ind, ncands,
                            )
                    #print(ncands)
                    #quit()
                else:
                    #indices_strat[timi,alti,lati,loni] = np.nan
                    pass
        else:
            pass
    else:
        pass
    return(indices_strat,core_cands,ncands)


@njit
def new_cluster_dict():
    #cluster = Dict.empty(
    #    key_type=types.unicode_type,
    #    value_type=types.int32[:],
    #)
    cluster = dict()
    cluster['timi'] = np.full(MAX_CLUSTER_SIZE, -1, np.int32)
    cluster['alti'] = np.full(MAX_CLUSTER_SIZE, -1, np.int32)
    cluster['lati'] = np.full(MAX_CLUSTER_SIZE, -1, np.int32)
    cluster['loni'] = np.full(MAX_CLUSTER_SIZE, -1, np.int32)
    return(cluster)

@njit
def find_convective_cores(qc, indices):
    cluster_ind = 0
    cluster = new_cluster_dict()
    clusters = [cluster]
    for timi in range(qc.shape[0]):
        #print(timi)
        for alti in range(qc.shape[1]):
            for lati in range(qc.shape[2]):
                for loni in range(qc.shape[3]):
                    cluster,found_new_cluster,size,i_got_error = add_new_cluster_3D(
                            qc, indices, timi, alti, lati, loni, 
                            new_cluster_dict(), cluster_ind, size=0)
                    if i_got_error:
                        return(clusters,indices,i_got_error)
                    if found_new_cluster:
                        # shorten arrays to necessary size
                        ngp = np.sum(cluster['alti'] >= 0)
                        for dim in ['timi','alti','lati','loni']:
                            cluster[dim] = cluster[dim][:ngp]
                        clusters.append(cluster)
                        cluster_ind += 1
                        #print(cluster)
                        #quit()
                        #return(clusters,indices)
    return(clusters,indices,i_got_error)


@njit
def add_new_cluster_3D(
        qc, indices, timi, alti, lati, loni, 
        cluster, cluster_ind, size=0,
    ):
    found_new_cluster = False
    i_got_error = False
    if ~np.isnan(qc[timi,alti,lati,loni]):
        if indices[timi,alti,lati,loni] == -1:
            found_new_cluster = True
            indices[timi,alti,lati,loni] = cluster_ind
            if size >= MAX_CLUSTER_SIZE-1:
                i_got_error = True
                return(cluster,found_new_cluster,size,i_got_error)
            cluster['timi'][size] = timi
            cluster['alti'][size] = alti
            cluster['lati'][size] = lati
            cluster['loni'][size] = loni
            #print('{} {} {}'.format(timi,alti,lati,loni))
            size += 1
            ### look for neighbors in vertical direction
            for alti2 in [alti-1,alti+1]:
                # consider boundaries
                if (alti2 >= 0) and (alti2 < qc.shape[1]):
                    #print('dive alt from {},{},{} to {},{},{}'.format(alti,lati,loni,alti2,lati,loni))
                    cluster,_,size,i_got_error = add_new_cluster_3D(
                            qc, indices, timi,alti2, lati, loni, 
                            cluster, cluster_ind, size=size)
            ### look for neighbors in meridional direction
            for lati2 in [lati-1,lati+1]:
                # consider boundaries
                if (lati2 >= 0) and (lati2 < qc.shape[2]):
                    #print('dive lat from {},{},{} to {},{},{}'.format(alti,lati,loni,alti,lati2,loni))
                    cluster,_,size,i_got_error = add_new_cluster_3D(
                            qc, indices, timi,alti, lati2, loni, 
                            cluster, cluster_ind, size=size)
            ### look for neighbors in zonal direction
            for loni2 in [loni-1,loni+1]:
                # consider boundaries
                if (loni2 >= 0) and (loni2 < qc.shape[3]):
                    #print('dive lon from {},{},{} to {},{},{}'.format(alti,lati,loni,alti,lati,loni2))
                    cluster,_,size,i_got_error = add_new_cluster_3D(
                            qc, indices, timi,alti, lati, loni2, 
                            cluster, cluster_ind, size=size)
        return(cluster,found_new_cluster,size,i_got_error)
    else:
        indices[timi,alti,lati,loni] = np.nan
        return(cluster,found_new_cluster,size,i_got_error)


@njit
def find_core_coli_center(
        timi, alti, lati, loni, latloni, 
        W, 
        ngp, ncol,
    ):
    """
    Determine index of center column of core
    """
    coli_center = -1
    nvert_col = np.zeros(ncol, dtype=np.int32)
    wmean_col = np.zeros(ncol, dtype=np.float32)
    nvert_max = 0
    ncol_nvert_max = 0
    # loop over columns 
    for coli in range(ncol):
        # loop over grid points
        for gpi in range(ngp):
            # if this gp is part of col
            if (lati[gpi], loni[gpi]) == latloni[coli]:
                nvert_col[coli] += 1
                wmean_col[coli] += W[timi[gpi],alti[gpi],lati[gpi],loni[gpi]]

        # compute wmean from wsum
        wmean_col[coli] /= nvert_col[coli]

        # update maximum vertical column
        if nvert_col[coli] > nvert_max:
            nvert_max = nvert_col[coli]
            ncol_nvert_max = 1
        elif nvert_col[coli] == nvert_max:
            ncol_nvert_max += 1

    # only one column with largest vertical extent
    if ncol_nvert_max == 1:
        # loop over columns 
        for coli in range(ncol):
            if nvert_col[coli] == nvert_max:
                coli_center = coli
    # more than one column with largest vertical extent
    else:
        wmean_col_max = 0
        coli_wmean_max = -1
        # loop over columns 
        for coli in range(ncol):
            if nvert_col[coli] == nvert_max:
                if wmean_col[coli] >= wmean_col_max:
                    coli_wmean_max = coli

        coli_center = coli_wmean_max
    return(coli_center)


@njit
def find_center_dists(
        c_coli_center, c_latloni, 
        latloni, 
        ncol,
        model_dx,
    ):
    """
    Determine distance of column centers and borders from core center
    """
    col_center_dist = np.zeros(ncol)

    # loop over columns 
    for coli in range(ncol):
        ### distance of column border from core center
        dist = np.sqrt(
            np.power(latloni[coli][0] - c_latloni[c_coli_center][0], 2.) + 
            np.power(latloni[coli][1] - c_latloni[c_coli_center][1], 2.) 
        ) * model_dx
        col_center_dist[coli] = dist
    return(col_center_dist)


@njit
def compute_tangmean_stats(
        timi, alti, lati, loni, latloni, 
        norm_inv, alt_coord, rel_alt_coord, rad_coord,
        QC, INVHGT,
        col_center_dist,
        model_dx,
        ncol, ngp, nrad,
    ):
    """
    Compute the horizontal mean distance of the cloud border from the core center.
    Also compute the tangential mean qv.
    """
    #if norm_inv == 0:
    #    vert_coord_use = alt_coord
    #else:
    #    vert_coord_use = rel_alt_coord
    vert_coord_use = rel_alt_coord

    ## horizontal mean distance of cloud border from the core center
    #tangmean_border_dist = np.zeros(len(vert_coord_use), dtype=np.float32)
    #tangmean_border_dist_count = np.zeros(len(vert_coord_use), dtype=np.int32)

    # cloud area f(vert_coord)
    cloud_area = np.zeros(len(vert_coord_use), dtype=np.float32)

    # tangential mean QC
    tangmean_qc = np.zeros((len(vert_coord_use),nrad), dtype=np.float32)
    tangmean_qc_count = np.zeros((len(vert_coord_use),nrad), dtype=np.int32)

    # radial bin width (is constant)
    drad = rad_coord[1] - rad_coord[0]

    #if norm_inv == 0:
        #raise NotImplementedError()
        ## loop over all altitude indices
        #for glob_alti in range(len(alt_coord)):
        #    # loop over columns 
        #    for coli in range(ncol):
        #        # loop over grid points
        #        for gpi in range(ngp):
        #            # if this gp is part of col and altitude level
        #            if (((lati[gpi], loni[gpi]) == latloni[coli]) &
        #                (alti[gpi] == glob_alti)):

        #                tangmean_border_dist[glob_alti] += col_center_dist[coli] + 0.5*model_dx
        #                tangmean_border_dist_count[glob_alti] += 1

        #                radi = int(col_center_dist[coli] / drad)
        #                if radi < nrad:
        #                    tangmean_qc[glob_alti,radi] += QC[timi[gpi],alti[gpi],lati[gpi],loni[gpi]]
        #                    tangmean_qc_count[glob_alti,radi] += 1

        #    ### compute mean values from cumulative sums and set Nan
        #    if tangmean_border_dist_count[glob_alti] > 0:
        #        tangmean_border_dist[glob_alti] /= tangmean_border_dist_count[glob_alti]
        #    else:
        #        tangmean_border_dist[glob_alti] = np.nan

        #    for radi in range(nrad):
        #        if tangmean_qc_count[glob_alti,radi] > 0:
        #            tangmean_qc[glob_alti,radi] /= tangmean_qc_count[glob_alti,radi]
        #        else:
        #            tangmean_qc[glob_alti,radi] = np.nan
    #else:
    # loop over columns 
    for coli in range(ncol):
        ngp_col = 0
        radi = int(col_center_dist[coli] / drad)
        #print(col_center_dist[coli])
        #print(radi)
        if radi < nrad:
            ## count number of grid points in this column 
            for gpi in range(ngp):
                # if this gp is part of col
                if (lati[gpi], loni[gpi]) == latloni[coli]:
                    ngp_col += 1
            #print(ngp_col)
            col_vals = np.full(ngp_col, np.nan)
            col_alts = np.full(ngp_col, np.nan)
            ## collect the grid points in this column
            vi = 0
            for gpi in range(ngp):
                # if this gp is part of col
                if (lati[gpi], loni[gpi]) == latloni[coli]:
                    col_vals[vi] = QC[timi[gpi],alti[gpi],lati[gpi],loni[gpi]]
                    col_alts[vi] = alt_coord[alti[gpi]]
                    vi += 1
            ## sort after increasing altitude
            order = col_alts.argsort()
            col_vals = col_vals[order]
            col_alts = col_alts[order]

            #print(col_alts[:])
            #print(col_vals[:])
            
            if norm_inv:
                invhgt = INVHGT[timi[gpi],latloni[coli][0],latloni[coli][1]]
                targ_alts = rel_alt_coord * invhgt
                #print(timi[gpi],latloni[coli][0],latloni[coli][1])
                #print(INVHGT[timi[gpi],latloni[coli][0],latloni[coli][1]])
                if len(col_vals) > 1:
                    interp_vals = np.interp(targ_alts, col_alts, col_vals)
                    ## set extrapolation values to NaN (except closest one)
                    for i in range(0,len(interp_vals)):
                        # using i+1/i-1 (if possible) makes sure
                        # that constant extrapolation is done for
                        # one target alt just beyond the source data alt
                        # This is done to not cut the clouds at their vertical
                        # boundaries during the interpolation alt --> rel_alt
                        ip1 = min(i+1, len(interp_vals)-1)
                        im1 = max(i-1, 0)
                        # prevent constant extrapolation across the inversion
                        if targ_alts[i] > invhgt:
                            im1 += 1
                        if targ_alts[ip1] < np.min(col_alts):
                            interp_vals[i] = np.nan
                        elif targ_alts[im1] > np.max(col_alts):
                            interp_vals[i] = np.nan
                elif len(col_vals) == 1:
                    interp_vals = np.full(len(targ_alts), np.nan)
                    ai_closest = np.argmin(np.abs(col_alts - targ_alts))
                    interp_vals[ai_closest] = col_vals[0]
                else:
                    raise ValueError()
                #print(targ_alts[5:10])
                #print(interp_vals[5:10])
                tangmean_qc[~np.isnan(interp_vals),radi] += interp_vals[~np.isnan(interp_vals)]
                tangmean_qc_count[~np.isnan(interp_vals),radi] += 1 
            else:
                raise NotImplementedError()
    ### compute mean values from cumulative sums and set Nan
    ### at the same time compute cloud area
    for ai in range(tangmean_qc.shape[0]):
        for radi in range(nrad):
            if tangmean_qc_count[ai,radi] > 0:
                tangmean_qc[ai,radi] /= tangmean_qc_count[ai,radi]
                # compute cloud area
                cloud_area[ai] += tangmean_qc_count[ai,radi] * model_dx**2
            else:
                tangmean_qc[ai,radi] = np.nan
            ## compute cloud area
            #cloud_area[ai] += tangmean_qc_count[ai,radi] * model_dx**2
        ## since area == 0 means no cloud, set to NaN
        if cloud_area[ai] == 0:
            cloud_area[ai] = np.nan
    #print(tangmean_qc_count[5:10,:])
    #print(cloud_area[5:10])
    #print(tangmean_qc[5:,:4])
    #print(tangmean_qc_count[5:,:4])
    #plt.contourf(tangmean_qc[5:,:4])
    #plt.colorbar()
    #plt.show()
    #print('FINISHED')
    return(cloud_area, tangmean_qc)



@njit
def cloud_statistics(
        c_timi, 
        c_alti, 
        c_lati, 
        c_loni, 
        c_latloni, 

        s_timi, 
        s_alti, 
        s_lati, 
        s_loni, 
        s_latloni, 

        b_timi, 
        b_alti, 
        b_lati, 
        b_loni, 
        b_latloni, 

        norm_inv,
        alt_coord, 
        rel_alt_coord, 
        rad_coord,
        model_dx,

        QC, W, INVHGT,
    ):
    c_ngp = len(c_alti)
    c_ncol = len(c_latloni)
    s_ngp = len(s_alti)
    s_ncol = len(s_latloni)
    b_ngp = len(b_alti)
    b_ncol = len(b_latloni)
    nrad = len(rad_coord)

    ### column index of central core column
    c_coli_center = find_core_coli_center(
        c_timi, c_alti, c_lati, c_loni, c_latloni,
        W,
        c_ngp, c_ncol,
    )

    ### distance of individual core columns from central core column
    c_col_center_dist = find_center_dists(
        c_coli_center, c_latloni, 
        c_latloni, 
        c_ncol,
        model_dx,
    )
    ### distance of individual strat columns from central core column
    s_col_center_dist = find_center_dists(
        c_coli_center, c_latloni, 
        s_latloni, 
        s_ncol,
        model_dx,
    )
    ### distance of individual core&strat columns from central core column
    b_col_center_dist = find_center_dists(
        c_coli_center, c_latloni, 
        b_latloni, 
        b_ncol,
        model_dx,
    )
    #print(c_col_center_dist)
    #print(s_col_center_dist)
    #print(b_col_center_dist)

    ### tangential statistics for cores
    (
        c_cloud_area,
        c_tangmean_qc,
    ) = compute_tangmean_stats(
        c_timi, c_alti, c_lati, c_loni, c_latloni, 
        norm_inv, alt_coord, rel_alt_coord, rad_coord,
        QC, INVHGT,
        c_col_center_dist,
        model_dx,
        c_ncol, c_ngp, nrad,
    )

    ### tangential statistics for strats
    (
        s_cloud_area,
        s_tangmean_qc,
    ) = compute_tangmean_stats(
        s_timi, s_alti, s_lati, s_loni, s_latloni, 
        norm_inv, alt_coord, rel_alt_coord, rad_coord,
        QC, INVHGT,
        s_col_center_dist,
        model_dx,
        s_ncol, s_ngp, nrad,
    )

    ### tangential statistics for cores&strats
    ( 
        b_cloud_area,
        b_tangmean_qc,
    ) = compute_tangmean_stats(
        b_timi, b_alti, b_lati, b_loni, b_latloni, 
        norm_inv, alt_coord, rel_alt_coord, rad_coord,
        QC, INVHGT,
        b_col_center_dist,
        model_dx,
        b_ncol, b_ngp, nrad,
    )
    #print(c_cloud_area)
    #print(s_tangmean_border_dist)
    #print(b_tangmean_border_dist)

    return(
        c_cloud_area,
        s_cloud_area,
        b_cloud_area,
        c_tangmean_qc,
        s_tangmean_qc,
        b_tangmean_qc,
    )
