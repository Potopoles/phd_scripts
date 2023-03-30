#!/usr/bin/python
# -*- coding: utf-8 -*-
#title			:calc_EQPOTT.py
#description	:Calculate the equivalent potential temperature and store.
#author			:Christoph Heim
#created		:20190510
#modified		:20190510
#usage			:python calc_EQPOTT.py $n_jobs
#notes			:calculated according to Stull 1988, p546 (see wikipedia)
#python_version	:3.7.1
#==============================================================================
import collections, time, copy, os
from datetime import datetime
import namelist as NL
from package.Variable import Variable
from package.variable_namelist import VNL
from package.MP import TimeStepMP
from package.functions import get_dt_range, load_field
from package.plot_functions import PlotOrganizer
from namelist_plot import plt






def aggreg_vertical(ts, field_name, member_dict, var_dict):
    loader = load_field(ts, field_name, member_dict, var_dict)
    # aggregate vertical
    loader.field = loader.field.sel(altitude=slice(0,6000))
    loader.field = loader.field.differentiate(coord='altitude')
    loader.field = loader.field.mean(dim='altitude')

    new_attr = {
        'standard_name':'mean_vertical_EQPOTT_gradient',
        'long_name':'mean_vertical_gradient_of_equivalent_pot_temp_0_to_4000m',
        'units':'K m-1',
        #'grid_mapping':loader.field.attrs['grid_mapping'],
    }
    from package.variable_namelist import MODMSC
    out_loader = loader.clone_to_new_field(
                        'EQPOTT', loader.field, new_attr,
                        new_var_dict=None)

    out_loader.save_field_to_nc(alternative_base_path=
                    os.path.join(NL.out_dir,member_dict['label'],'dEQPOTTdz'))
    return(out_loader)



def plot_aggreg_vert(ts, field_name, member_dict):
    loader = load_field(ts, field_name, member_dict, var_dict)

    dataset = xr.save_field_to_nc(alternative_base_path=
                    os.path.join(NL.out_dir,member_dict['label'],'dEQPOTTdz'))
    # aggregate vertical
    loader.field = loader.field.sel(altitude=slice(0,6000))
    loader.field = loader.field.differentiate(coord='altitude')
    loader.field = loader.field.mean(dim='altitude')

    new_attr = {
        'standard_name':'mean_vertical_EQPOTT_gradient',
        'long_name':'mean_vertical_gradient_of_equivalent_pot_temp_0_to_4000m',
        'units':'K m-1',
        #'grid_mapping':loader.field.attrs['grid_mapping'],
    }
    from package.variable_namelist import MODMSC
    out_loader = loader.clone_to_new_field(
                        'EQPOTT', loader.field, new_attr,
                        new_var_dict=None)

    return(out_loader)





def prep_vertical_plot(ts, field_name, member_dict, var_dict):
    loader = load_field(ts, field_name, member_dict, var_dict)
    if loader.field['time.hour'].values[0] in NL._05['day_time']:
        # subdomain
        loader.sel_subdomain(NL._05['domain'])
        loader.field = loader.field.sel(altitude=slice(0,6000))
        # aggregate horizontal
        loader.field = loader.field.mean(dim=('rlat','rlon'))
        loader.field = loader.field.differentiate(coord='altitude')
        return(loader)


if __name__ == '__main__':

    t00 = time.time()

    ### PREPARATIONS 
    # date ranges
    dt_range = get_dt_range(NL.first_date, NL.last_date)

    # select members
    member_dicts = {}
    for member_key,member_dict in NL.member_dicts.items():
        if member_key in NL.use_members:
            member_dicts[member_key] = member_dict

    # RUN CALCULATIONS
    members = {}
    for member_key,member_dict in member_dicts.items():
        t0 = time.time()
        print(member_key)
        ## Vertical Plot
        #fargs = {
        #    'member_dict':member_dict,
        #    'var_dict':VNL['EQPOTT'],
        #    'field_name':'EQPOTT',
        #    }
        #TSMP = TimeStepMP(dt_range[member_dict['dt']])
        #TSMP.run(func=prep_vertical_plot, fargs=fargs)
        #field = TSMP.concat_timesteps()

        # Aggregate Vertical
        fargs = {
            'member_dict':member_dict,
            'var_dict':VNL['EQPOTT'],
            'field_name':'EQPOTT',
            }
        TSMP = TimeStepMP(dt_range[member_dict['dt']])
        TSMP.run(func=aggreg_vertical, fargs=fargs)
        field = TSMP.concat_timesteps()


        members[member_key] = field

        t1 = time.time()
        print(t1 - t0)

    t1 = time.time()
    print(t1 - t00)


    # PLOTTING 
    print('Plotting')
    name_dict = collections.OrderedDict()
    name_dict[''] = 'stability'
    PO = PlotOrganizer(NL.i_save_fig, path=NL.plot_dir, name_dict=name_dict)
    fig = PO.initialize_plot()
    for member_key,member_dict in member_dicts.items():
        print(member_key)
        field = members[member_key]
        field = field.mean(dim='time')
        if member_dict['smooth']:
            linestyle = '--'
        else:
            linestyle = '-'
        line, = plt.plot(field.values, field.coords['altitude'].values,
                label=member_key, color=NL.cols[member_dict['dx']],
                linestyle=linestyle)

        PO.handles.append(line)

    plt.legend(handles=PO.handles)
    
    PO.finalize_plot(fig)
    
