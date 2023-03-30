#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description	    :Calculate the spectral densities for 2D fields and store
author			:Christoph Heim
date created    :07.05.2019
date changed    :25.10.2019
usage			:no args
==============================================================================
"""
from namelist_plot import plt
import collections, time, os
import xarray as xr
from scipy import signal
from datetime import datetime
import numpy as np
import namelist as NL
from package.plot_functions import PlotOrganizer
from package.variable import Variable
from package.nl_variables import nlv
from package.MP import TimeStepMP
from package.field_io import FieldLoader
from package.functions import get_dt_range
from power_spectral_density import calculate_PSD


def k2lamb(k):
    lamb = 1/k
    return(lamb)

def lamb2k(lamb):
    ## unit wave number
    #k = 1/lamb
    # angular wave number
    k = 2*np.pi/lamb
    return(k)

def calc_spectra(ts, task_no, member_dict, var_dicts, altitudes, domain):
    #print(ts)

    for var_name,dict in var_dicts.items():
        loader = FieldLoader(var_name, member_dict,
                    var_dicts[var_name], chunks=NL.chunks)
        loader.load_timesteps(ts)
        whole_field = loader.field


        # subselect domain and altitudes
        whole_field = \
            whole_field.sel(rlat=slice(domain['rlat'][0], domain['rlat'][1]),
                            rlon=slice(domain['rlon'][0], domain['rlon'][1]),
                            altitude=altitudes)

        C_alts = []
        for alt in altitudes:
            # subselect vertical segment
            field = whole_field.sel(altitude=slice(alt,alt))

            # calculate deviations (W' = W - W_mean)
            mean_val = field.mean(dim=('rlon', 'rlat'))
            field.values = field - mean_val

            # set nan values to 0
            field = field.where(~np.isnan(field), 0.0)

            # remove linear trends in lon and lat direction
            detrended = signal.detrend(field.values, axis=2, type='linear')
            detrended = signal.detrend(detrended, axis=3, type='linear')
            field.values = detrended

            # calculate power spectral density in both dimensions
            # only take positive wave number part and convert
            # units to km^-1.
            # lat dim
            k_lat,C_lat = calculate_PSD(field.values.squeeze(),
                                member_dict['dx'], 0)
            C_lat = C_lat[k_lat > 0]
            k_lat = k_lat[k_lat > 0]*1000/(2*np.pi)

            # lon dim
            k_lon,C_lon = calculate_PSD(field.values.squeeze(),
                                member_dict['dx'], 1)
            C_lon = C_lon[k_lon > 0]
            k_lon = k_lon[k_lon > 0]*1000/(2*np.pi)

            # interpolate both onto same wave number vector
            k_interp = np.linspace(max(np.min(k_lon),np.min(k_lat)),
                                   min(np.max(k_lon),np.max(k_lat)),
                                   min(len(k_lon),len(k_lat)))
            C_lon_interp = np.interp(k_interp, k_lon, C_lon)
            C_lat_interp = np.interp(k_interp, k_lat, C_lat)

            # average both dimensions in interpolated space
            C_mean = 0.5 * (C_lon_interp + C_lat_interp)

            #plt.semilogx(k_lon, C_lon*k_lon)
            #plt.semilogx(k_lat, C_lat*k_lat)
            #plt.semilogx(k_interp, C_mean*k_interp)
            #plt.show()
            #quit()

            C_alts.append(C_mean)

        lamb = k2lamb(k_interp)

        C = np.zeros((1, len(altitudes), len(C_alts[0])))
        for i in range(len(C_alts)):
            C[0,i,:] = C_alts[i]


        spec = xr.DataArray(C, coords={'time':whole_field.coords['time'],
                            'altitude':whole_field.coords['altitude'],
                            'k':k_interp},
                            dims=('time','altitude','k'))

        spec.name = var_name+'_spec'
        if var_name == 'W':
            spec.attrs = {
                'standard_name':'vertical_velocity_spectra',
                'long_name':'horizontal_2d_spectra_of_vertical_velocity',
                'units':'m s-1',
                'subdomain':domain['label'],
            }
        elif var_name == 'QC':
            spec.attrs = {
                'standard_name':'cloud_water_spectra',
                'long_name':'horizontal_2d_spectra_of_specific_cloud_water_content',
                'units':'kg kg-1',
                'subdomain':domain['label'],
            }

        lamb = xr.DataArray(lamb, coords={'k':k_interp},
                                dims=('k'))
        lamb.name = 'lambda'
        lamb.attrs = {
            'standard_name':'wavelength',
            'long_name':'wavelength',
            'units':'km',
            'details':'1/k',
            'subdomain':domain['label'],
        }

        k_attrs = {
            'standard_name':'wave_number',
            'long_name':'wave_number',
            'units':'km-1',
        }
        spec.coords['k'].attrs = k_attrs

        # dataset
        dataset = xr.Dataset({'time':[ts],
                            'altitude':np.asarray(altitudes, np.float64),
                            'k':k_interp,
                            var_name+'_spec':spec,
                            'lambda':lamb})

        out_path = os.path.join(member_dict['out_dir'],'spectra',var_name)
        if not os.path.exists(out_path):
            os.mkdir(out_path)
        out_path = os.path.join(out_path, 'lffd{:%Y%m%d%H}z.nc'.format(ts))
        dataset.to_netcdf(out_path)




if __name__ == '__main__':
    t00 = time.time()

    ### PREPARATIONS 
    # date ranges (select only hours in NL.diurn_hrs)
    dt_range_hourly = get_dt_range(NL.first_date, NL.last_date)['hourly']
    dt_range_hourly = [dt for dt in dt_range_hourly if dt.hour in NL.diurn_hrs]

    # select members
    member_dicts = {}
    for member_key,member_dict in NL.member_dicts.items():
        if member_key in NL.use_members:
            member_dicts[member_key] = member_dict

    # RUN CALCULATIONS
    if NL.i_recompute:
        members = {}
        for member_key,member_dict in member_dicts.items():
            t0 = time.time()
            print(member_key)
            fargs = {
                'member_dict':member_dict,
                'var_dicts':{},
                'altitudes':NL.altitudes,
                'domain':NL.domain_03,
                }
            for var_name in NL.var_names:
                fargs['var_dicts'][var_name] = nlv[var_name]

            step_args = []
            for i,dt in enumerate(dt_range_hourly):
                step_args.append({'task_no':i})
                
            TSMP = TimeStepMP(dt_range_hourly)
            TSMP.run(func=calc_spectra, fargs=fargs, step_args=step_args)

            t1 = time.time()
            print(t1 - t0)

        t1 = time.time()
        print(t1 - t00)


    # PLOT
    if NL.i_plot: 
        for altitude in NL.altitudes:
            print('plot ' + str(altitude) + ' km')
            name_dict = collections.OrderedDict()
            name_dict[''] = NL.plot_var+'_spectrum' 
            #name_dict['nonorm'] = NL.plot_var+'_spectrum' 
            name_dict['time'] = NL.title_time
            name_dict['altitude'] = int(altitude/1000)
            PO = PlotOrganizer(NL.i_save_fig, path=NL.plot_dir, name_dict=name_dict)
            fig,axes = PO.initialize_plot(1,3)
            #fig.set_size_inches((5,4))
            fig.set_size_inches((12,4))

            plot_panels = [['SM4', 'RAW4'], ['SM2', 'RAW2'], ['SM1', 'RAW1']]
            #plot_panels = [['RAW4'], ['SM2'], []]
            panel_labels = ['a)','b)', 'c)', 'd)', 'e)', 'f)']
            lind = 0
            for axI in range(3):
                handles = []
                ax1 = axes[0,axI]
                ax2 = ax1.twiny()
                for member in plot_panels[axI]:
                    print(member)
                    member_dict = member_dicts[member]

                    # select files of selected time steps
                    path = os.path.join(member_dict['out_dir'],'spectra',NL.plot_var)
                    files = []
                    for dt in dt_range_hourly:
                        file = 'lffd{:%Y%m%d%H}z.nc'.format(dt)
                        if file in os.listdir(path):
                            files.append(os.path.join(path,file))
                        else:
                            raise IOError('file ' + file + ' not found.')
                    # load an process spectra
                    data = xr.open_mfdataset(files)
                    spec = data[NL.plot_var+'_spec']
                    spec = spec.sel(altitude=[altitude])
                    spec = spec.mean(dim='time')

                    if member_dict['smooth']:
                        #ax = axes[0]
                        #linestyle = '--'
                        color = 'black'
                    else:
                        #ax = axes[1]
                        #linestyle = '-'
                        color = 'red'

                    # not angular wave number but unit wave number
                    # n waves per km
                    x_k = spec['k']
                    x_lamb = 1/spec['k']
                    # go back to angular wave number
                    x_k = x_k * 2*np.pi
                    y = spec*x_k
                    # normalize to unit area
                    #y = y/y.integrate(dim='k')
            
                    #line, = ax1.semilogx(x_k, y.values.squeeze(),
                    #        label=member_dict['label'], linestyle=linestyle,
                    #        color=NL.cols[member_dict['dx']])
                    line, = ax1.semilogx(x_k, y.values.squeeze(),
                            label=member_dict['label'], linestyle='-',
                            color=color)
                    handles.append(line)

                ax2.semilogx(x_lamb, y.values.squeeze(), linestyle='None')

                # style figure
                ax1.set_xlim((lamb2k(500),lamb2k(1)))
                ax1.set_xlabel('Wave Number [$2\pi$ $km^{-1}$]')
                ax2.set_xlim(500,1)
                ax2.set_xlabel(r'Wave Length [$km$]')
                if axI == 0:
                    ax1.set_ylabel(r'$kS(k)/s^2$')
                ax1.xaxis.grid()

                #title = os.path.split(PO.path)[1].replace('_',' ').\
                #            replace('.png','').replace('.pdf','') + ' km'
                #plt.title(title)

                #fig.subplots_adjust(top=0.93, left=0.12, bottom=0.11)

                ax1.legend(handles=handles, loc='upper left')

                # make panel label
                pan_lab_x = ax1.get_xlim()[0]
                pan_lab_y = ax1.get_ylim()[1] + (ax1.get_ylim()[1] - ax1.get_ylim()[0]) * 0.05
                ax1.text(pan_lab_x,pan_lab_y,panel_labels[lind], fontsize=15, weight='bold')
                lind += 1


            fig.subplots_adjust(top=0.85, left=0.09, bottom=0.16, right=0.98,
                                wspace=0.15)   
            PO.finalize_plot(fig)


