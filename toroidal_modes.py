# toroidal_modes.py
#
# Originally written by tschuh-at-princeton.edu, 11/15/2021
# Last modified by tschuh-at-princeton.edu, 11/19/2021

import numpy as np
from euler import euler
from frequency_bisection import frequency_bisection

# eventually all (most) of these constants will come from Page as input

####################################################################

# Base parameters for discretization and radial integration
a = 6371000 # Earth radius [m]
b = 2891000 # CMB radius [m]
nr = 100 # number of nodes in the radial dimension
dr = (a - b) / (nr - 1) # radial step
rr = b + np.dot((np.arange(0,nr)),dr) # vector for Earth's radii [m]

# Mode parameters
# nmin = ?
nmax = 10 # max radial order n
lmin = 1 # min angular order l (l >= 1)
lmax = 2 # max angular order l
fmin = 0.00001 # starting frequency for eigenfrequency hunt [Hz]
fmax = 0.2 # max frequency for hunt [Hz]
df = 0.00001 # frequency step for hunt [Hz]
eigf = np.empty((nmax,lmax,)) # initialize nmax by lmax NaN matrix
eigf[:] = np.nan              # which will contain eigenfrequencies
Tmat = np.zeros((lmax,nmax))
twopi = 2*np.pi # constant 2pi

# Elastic parameters for a homogeneous spherical Earth model
rho0 = 4380 # mean density [kg/m^3]
vs0 = 5930 # s-wave speed [m/s]
mu0 = rho0*vs0*vs0 # shear modulus [Pa]

# create earth's density and shear profile for homogeneous model
rho = np.empty((nr,1,))
rho.fill(rho0)
mu = np.empty((nr,1,))
mu.fill(mu0)

####################################################################

# this will be a function

for l in range(lmin,lmax+1):
    n = -1 # reset counter for radial degrees n
    f = fmin # we start looking for eigenfrequencies from fmin [Hz]
    wl = twopi*f # corresponding angular frequency [rad/s]

    # integrate_toroidal_system using Euler method
    [W,T,count] = euler(wl,dr,rr,rho,mu,l)
    Twmin = T[-1]

    # now iterate to hunt radial orders and their frequencies
    while f < fmax:
        # increase frequency (new candidate)
        f = f + df
        wr = twopi*f

        # integrate for this frequency and get surface traction
        [W,T,count] = euler(wr,dr,rr,rho,mu,l)
        Twc = T[-1]

        # check if we have changed sign (meaning we've bracketed a root)
        if (Twc*Twmin) < 0: # then we have bracketed a root
            # use bissection to get a precise estimate of the frequency
            # and eigenfunctions and the radial order n
            [wc,_,_,n] = frequency_bisection(wr,wl,dr,rr,rho,mu,l,Twmin)

            # save radial order n (counted), l, and its eigenfrequency
            eigf[n,l-1] = 1000*wc/twopi # eigenfrequency [mHz]

            # save eigenperiod
            T0 = twopi/wc/60 # eigenperiod [min]
            Tmat[l-1,n] = T0*60 # write eigenperiod matrix [sec]

            # print information
            print('Found eigenfrequency w =','%.2f'%eigf[n,l-1],'mHz for n =',n,'l =',l)

            # check a new frequency estimate and get surface traction
            f = wc/twopi + df # update frequency [Hz]
            [W,T,count] = euler(f*twopi,dr,rr,rho,mu,l)
            wl = wc # set current frequency as left frequency
            Twmin = T[-1] # set current surface traction as left surface traction

        else: # then we havent bracketed a frequency
            wl = wr # set current frequency as right frequency
            Twini = Twc # set current surface traction as right surface traction

        # stop search if we already have the requested number of radial orders n
        if (n+1) >= nmax:
            break

####################################################################
