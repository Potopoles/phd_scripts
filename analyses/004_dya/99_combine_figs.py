#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
description     Merge Figures together.
author			Christoph Heim
date created    15.06.2021
date changed    15.06.2021
usage           args:
                1st:    TODO
"""
###############################################################################
import os
import numpy as np
#import xarray as xr
#import matplotlib.pyplot as plt
#from pathlib import Path
#from datetime import datetime, timedelta
from PIL import Image
import nl_99 as nl
#from package.nl_variables import nlv
#from package.var_pp import var_mapping, compute_variable
#from package.utilities import Timer, dt64_to_dt, subsel_domain
#from package.plot_functions import PlotOrganizer, draw_map
#from package.functions import load_member_var, time_periods_to_dates
#from package.mp import TimeStepMP, IterMP
#from package.member import Member
#from package.comparison import Comparison
###############################################################################




def concat_img_array(img_paths, resample=Image.BICUBIC, color_space='RGB'):
    #min_height = min(im.height for im in im_list)
    #im_list_resize = [im.resize((int(im.width * min_height / im.height), 
    #                    min_height),resample=resample)
    #                    for im in im_list]
    #total_width = sum(im.width for im in im_list_resize)

    ### load images
    imgs = [] 
    for row_ind in range(len(img_paths)): 
        imgs.append([])
        for col_ind in range(len(img_paths[0])): 
            imgs[row_ind].append(Image.open(img_paths[row_ind][col_ind]))

    #### resize images
    #imgs = [] 
    #for row_ind in range(len(img_paths)): 
    #    imgs.append([])
    #    for col_ind in range(len(img_paths[0])): 
    #        imgs[row_ind].append(Image.open(img_paths[row_ind][col_ind]))

    ### determine total width/height
    tot_height = 0
    for row_ind in range(len(img_paths)): 
        tot_height += imgs[row_ind][0].height
    tot_width = 0
    for col_ind in range(len(img_paths[0])): 
        tot_width += imgs[0][col_ind].width

    if nl.merged_name == 'fig_08':
        crop = 320
        tot_height -= crop * 4
    if nl.merged_name in ['fig_04', 'fig_05', 'fig_07', 'fig_12']:
        crop = 370
        tot_width -= crop

    ### merge images
    merged = Image.new(color_space, (tot_width, tot_height), 'WHITE')
    pos_y = 0
    pos_x = 0
    for row_ind in range(len(img_paths)): 
        for col_ind in range(len(img_paths[0])): 
            img = imgs[row_ind][col_ind]
            # crop for Fig. 8
            if nl.merged_name == 'fig_08':
                if row_ind < len(img_paths)-1:
                    left = 0
                    top = 0
                    right = img.width
                    bottom = img.height - crop
                    img = img.crop((left, top, right, bottom))
            elif nl.merged_name in ['fig_04', 'fig_05', 'fig_07', 'fig_12']:
                if col_ind == len(img_paths[0])-1:
                    left = 0
                    top = 0
                    right = img.width - crop
                    bottom = img.height
                    img = img.crop((left, top, right, bottom))
            merged.paste(img, (pos_x, pos_y))
            pos_x += img.width
        pos_x = 0
        pos_y += img.height

    return(merged)


if __name__ == '__main__':

    ###########################################################################
    # PREPARATION STEPS

    # combine img names and image path to array giving absolute paths
    # in geometric order to merge.
    img_paths = [] 
    for row_ind in range(len(nl.img_names)): 
        img_paths.append([])
        for col_ind in range(len(nl.img_names[0])): 
            img_paths[row_ind].append(os.path.join(nl.inp_path,
                                            nl.img_names[row_ind][col_ind]))


    ##print(nl.img_names)
    ##img_path = os.path.join(nl.plot_base_dir, nl.img_names[0][0])
    ##img = Image.open(img_path)
    ##print(img.mode)
    ##img = img.convert('CMYK')
    ##print(img.mode)
    ##img.save(img_path)

    ###########################################################################
    # MERGE
    merged = concat_img_array(img_paths)
    merged.save(os.path.join(nl.inp_path,
                        '{}.{}'.format(nl.merged_name, nl.fig_type)),
                        dpi=(600,600))
    merged_cmyk = concat_img_array(img_paths, color_space='CMYK')
    merged_cmyk.save(os.path.join(nl.inp_path,
                        '{}_cmyk.{}'.format(nl.merged_name, nl.fig_type)))
