def plotVertProf(var_vP, varNCO, ax, meta):
    zvals = varNCO.dims['altitude'].vals
    zvals = np.expand_dims(zvals, 0)
    zvals = np.repeat(zvals,len(subSpaceInds['diurnal']),axis=0)

    PLOT = ax.plot(np.transpose(var_vP), np.transpose(zvals))
    ax.axvline(x=0, color=(0.5,0.5,0.5), linestyle='-', linewidth=1)
    ax.legend(PLOT, subSpaceInds['diurnal'])
    ax.set_xlim([meta['min'], meta['max']])
    ax.grid()
    


import os
os.chdir('00_scripts/')

i_resolutions = 3 # 1 = 4.4, 2 = 4.4 + 2.2, 3 = ...
i_plot = 2 # 0 = no plot, 1 = show plot, 2 = save plot
import matplotlib
if i_plot == 2:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt


inpPath = '../02_fields/subDomDiur'
plotOutDir = '../00_plots/06_bulk'
plotName = 'potTT_TOT.png'

import numpy as np
import ncClasses.ncObject as ncObject

profiles = {}

modes = ['', 'f']
if i_resolutions == 1:
    ress = ['4.4']
elif i_resolutions == 2:
    ress = ['4.4', '2.2']
elif i_resolutions == 3:
    ress = ['4.4','2.2','1.1']
elif i_resolutions == 4:
    ress = ['2.2']
elif i_resolutions == 5:
    ress = ['1.1']

for res in ress:
    print(res)
    for mode in modes:
        #mode = ''
        print(mode)

        subSpaceInds = {}
        subSpaceInds['rlon'] = (50,100)
        subSpaceInds['rlat'] = (20,57)
        #subSpaceInds['rlon'] = (50,60)
        #subSpaceInds['rlat'] = (30,40)
        subSpaceInds['altitude'] = list(range(1,41))

        subSpaceInds['diurnal'] = [0,3,6,9,12,15,18,21]
        #subSpaceInds['diurnal'] = [3,9,15,21]
        #subSpaceInds['diurnal'] = [21]

        fact = 1
        if res == '2.2':
            fact = 2
        elif res == '1.1':
            fact = 4
        if 'rlon' in subSpaceInds:
            subSpaceInds['rlon'] = [x * fact for x in subSpaceInds['rlon']]
            subSpaceInds['rlon'] = list(range(subSpaceInds['rlon'][0], subSpaceInds['rlon'][1]+1))
        if 'rlat' in subSpaceInds:
            subSpaceInds['rlat'] = [x * fact for x in subSpaceInds['rlat']]
            subSpaceInds['rlat'] = list(range(subSpaceInds['rlat'][0], subSpaceInds['rlat'][1]+1))


        from functions_06 import LoadField
        LF = LoadField(inpPath, res, mode, subSpaceInds)
        (RHO,rho) = LF.loadField('zRHO.nc', 'RHO')
        #(W,w) = LF.loadField('zW.nc', 'W')
        (T,t) = LF.loadField('zT.nc', 'T')
        (TT_TOT,tt_tot) = LF.loadField('zATT_TOT.nc', 'ATT_TOT')
        (P,p) = LF.loadField('zP.nc', 'P')

        from functions_06 import vertProf


        # CALCULATE POTENTIAL TEMPERATURE
        Rd = 287.1
        cp = 1005
        kappa = Rd/cp 
        pott = t*np.power((100000/p), kappa)

        # CALCULATE POTENTIAL TEMPERATURE TENDENCY (TODO)
        pottt_tot = pott/t*tt_tot

        # CALCULATE VERTICAL PROFILE
        pottt_tot_vP = vertProf(pottt_tot*3600, rho)

        profiles[str(res+mode)] = pottt_tot_vP

pltMeta = {}
pltMeta['max'] = -np.Inf
pltMeta['min'] = np.Inf
for key,vals in profiles.items():
    if np.nanmax(vals) > pltMeta['max']:
        pltMeta['max'] = np.nanmax(vals)
    if np.nanmin(vals) < pltMeta['min']:
        pltMeta['min'] = np.nanmin(vals)
    

fig, axes = plt.subplots(ncols=3, nrows=2, figsize=(16,8))
plotVertProf(profiles['4.4f'], P, axes[0,0], pltMeta)
plotVertProf(profiles['4.4'], P, axes[1,0], pltMeta)
if '2.2' in ress:
    plotVertProf(profiles['2.2f'], P, axes[0,1], pltMeta)
    plotVertProf(profiles['2.2'], P, axes[1,1], pltMeta)
if '1.1' in ress:
    plotVertProf(profiles['1.1f'], P, axes[0,2], pltMeta)
    plotVertProf(profiles['1.1'], P, axes[1,2], pltMeta)
    
if i_plot == 1:
    plt.show()
elif i_plot == 2:
    plotPath = plotOutDir + '/' + plotName
    plt.savefig(plotPath, format='png', bbox_inches='tight')
