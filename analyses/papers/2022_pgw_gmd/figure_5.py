import os
import xarray as xr
import matplotlib.pyplot as plt
import datetime
import cartopy.crs as ccrs
from package.plot_functions import draw_map
from base.nl_domains import *

data_base_dir = '/net/o3/hymet_nobackup/heimc/data/cosmo_out/paper_pgw_geopot'

#sim_names = ['Amon_None','Emon_None']
sim_names = ['Amon_500hPa','Emon_500hPa']

ana_date = datetime.datetime(2006,8,1,0)
plevs = [100000,70000,10000]
plt.rcParams['savefig.dpi'] = 600

nsims = len(sim_names)

fig,axes = plt.subplots(1, 3, figsize=(14,3), subplot_kw={'projection': ccrs.PlateCarree()})

for plev_ind,plev in enumerate(plevs):
    print(plev_ind)
    ax = axes[plev_ind]
    nlp = {
        'projection':ccrs.PlateCarree(),
        'map_margin':[0,0,0,0],
    }
    draw_map(ax, dom_SA_3km_large3, nlp, add_xlabel=True, add_ylabel=True, dticks=20)
    
    data_path = os.path.join(data_base_dir, 'lm_coarse_{}'.format(sim_names[0]), 'plev')
    file_name = 'lffd{:%Y%m%d%H%M%S}p.nc'.format(ana_date)
    file_path = os.path.join(data_path, file_name)

    var_1 = xr.open_dataset(file_path)['FI'].sel(pressure=plev).squeeze()

    data_path = os.path.join(data_base_dir, 'lm_coarse_{}'.format(sim_names[1]), 'plev')
    file_name = 'lffd{:%Y%m%d%H%M%S}p.nc'.format(ana_date)
    file_path = os.path.join(data_path, file_name)

    var_2 = xr.open_dataset(file_path)['FI'].sel(pressure=plev).squeeze()

    diff = (var_1 - var_2) / 9.81

    diff.plot.contourf(
        ax=ax,
        levels = 10,
        cmap='RdBu_r',
        vmin = -5,
        vmax = 5,
        extend = 'both',
        cbar_kwargs={'label':'$\phi$ [m]'},
    )
    ax.set_title('{}hPa'.format(int(plev/100)))
    ax.set_xlabel('longitude')
    if plev_ind == 0:
        ax.set_ylabel('latitude')
    else:
        ax.set_ylabel('')

        #plt.show()

#fig.suptitle('Geopotential differences Emon-Amon')
#fig.tight_layout()
fig.subplots_adjust(
    left=0.06,
    right=0.97,
    top=0.90,
    bottom=0.15,
    wspace=0.25,
)
#plt.show()
plt.savefig('Figure_5_diff_phi.jpg')





#data_base_dir = '/net/o3/hymet_nobackup/heimc/data/cosmo_out/paper_pgw_geopot'
#
#sim_names = ['Amon_None','Amon_500hPa','Emon_None','Emon_500hPa']
#sim_names = ['ctrl','Amon_None','Amon_500hPa','Emon_None','Emon_500hPa']
#
#ana_date = datetime.datetime(2006,8,1,0)
#plev = 50000
#
#nsims = len(sim_names)
#
#fig,axes = plt.subplots(nsims-1, nsims-1, figsize=(14,10))
#
#for sim_ind_1,sim_name_1 in enumerate(sim_names):
#    print(sim_ind_1)
#    
#    data_path = os.path.join(data_base_dir, 'lm_coarse_{}'.format(sim_name_1), 'plev')
#    file_name = 'lffd{:%Y%m%d%H%M%S}p.nc'.format(ana_date)
#    file_path = os.path.join(data_path, file_name)
#
#    var_1 = xr.open_dataset(file_path)['FI'].sel(pressure=plev).squeeze()
#
#    for sim_ind_2,sim_name_2 in enumerate(sim_names):
#
#        if sim_ind_2 >= sim_ind_1:
#            if (sim_ind_1 >= 1) & (sim_ind_2 < nsims-1):
#                ax = axes[sim_ind_1-1, sim_ind_2]
#                ax.set_visible(False)
#            continue
#
#        ax = axes[sim_ind_1-1, sim_ind_2]
#        
#        data_path = os.path.join(data_base_dir, 'lm_coarse_{}'.format(sim_name_2), 'plev')
#        file_name = 'lffd{:%Y%m%d%H%M%S}p.nc'.format(ana_date)
#        file_path = os.path.join(data_path, file_name)
#
#        var_2 = xr.open_dataset(file_path)['FI'].sel(pressure=plev).squeeze()
#
#        diff = (var_1 - var_2) / 9.81
#
#        if 'ctrl' in sim_name_2:
#            diff.plot.contourf(
#                ax=ax,
#                levels = 10,
#                cmap='viridis',
#                extend = 'both',
#                cbar_kwargs={'label':'$\phi$ [m]'},
#            )
#        else:
#            diff.plot.contourf(
#                ax=ax,
#                levels = 10,
#                cmap='RdBu_r',
#                vmin = -5,
#                vmax = 5,
#                extend = 'both',
#                cbar_kwargs={'label':'$\phi$ [m]'},
#            )
#        ax.set_title('{} - {}'.format(sim_name_1, sim_name_2))
#        ax.set_xlabel('longitude')
#        ax.set_ylabel('latitude')
#
#        #plt.show()
#
#fig.suptitle('Geopotential differences at {} hPa'.format(int(plev/100)))
#fig.tight_layout()
##plt.show()
#plt.savefig('diff_phi_at_{}hPa.jpg'.format(int(plev/100)))
