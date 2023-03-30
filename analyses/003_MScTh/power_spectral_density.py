"""
Calculate 1D power spectral density of 2D field.

Christian Zeman, 2019
"""

import numpy as np

def calculate_PSD(var, dist, dir):
    """Calculate averaged 1D PSD along x- or y-axis.

       This method calculates the 1D power spectral density of a 2D field
       by calculating the 1D PSD of all rows/columns and then averaging it.
       The Welch window function is used in order to deal with the non-
       periodicity. 

       (based on https://ch.mathworks.com/matlabcentral/fileexchange/
                 54315-1-dimensional-surface-roughness-power-spectrum-of
                 -a-profile-or-topography)

       Arguments:
       var -- variable of interest
       dist -- grid point distance [m]
       dir -- direction for 1D spectrum (0=x, 1=y)

       Returns:
       C -- 1D PSD averaged over rows/columns
       k -- wavevector (2*pi/wavelength)

       Comments Christoph Heim, 2019:
       For highlighting spectral peak multiply k*spectral energy (C)
       and plot either lin vs log or log vs log.
       Also, potentially run it over both dimensions and average
       spectra (like Davide Panosetti did).
    """

    # Get direction and dimension
    if dir == 1:
        var = var.transpose()
    n, m = var.shape

    # Window function just in one direction (Welch)
    win = np.ones((n,1)) * (1. - ((np.arange(0,m)-((m-1)/2.))/((m+1)/2.))**2)
    varWin = var * win
   
    # Normalization factor (due to window function)
    U = np.sum(win[0,:]**2) / (m-1)

    # Calculate 1D PSD
    Hm = np.fft.fft(varWin)
    Cq = (1./U) * (dist/m)*(1./(2.*np.pi)) * np.abs(np.fft.fftshift(Hm, 1))**2

    # Corresponding wave vector
    k_1 = (2.*np.pi/m) * np.arange(0,m)
    k_2 = np.fft.fftshift(k_1)
    k_3 = np.unwrap(k_2 - 2.*np.pi)
    k = k_3 / dist 

    # Average lines
    C = np.mean(Cq, 0)

    return k, C

