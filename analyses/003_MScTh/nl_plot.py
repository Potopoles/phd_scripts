from package.nl_plot_global import nlp
#import cartopy
import numpy as np

# COLORMAP SIMPLE
nlp['cmap'] = 'RdBu_r'

# COLORMAP VERSION 1
import matplotlib.pyplot as plt
cmap = plt.get_cmap('RdBu_r')
colors = cmap(np.linspace(0.0, 0.5, + cmap.N // 2))
from matplotlib.colors import LinearSegmentedColormap
nlp['cmap'] = LinearSegmentedColormap.from_list('test', colors)

## COLORMAP VERSION 2
#from matplotlib.colors import LinearSegmentedColormap
#nlp['cmap'] = LinearSegmentedColormap.from_list('name', ['blue', 'white', 'brown'])


#nlp['projection']   = cartopy.crs.PlateCarree(),
nlp['map_margin']   = (0,0,0,0) # lon0, lon1, lat0, lat1



