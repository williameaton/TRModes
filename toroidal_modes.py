import numpy as np
from euler import euler

# eventually all (most) of these constants will come from Page as input

####################################################################

# Base parameters for discretization and radial integration
a = 6371000 # Earth radius [m]
b = 2891000 # CMB radius [m]
nr = 100 # number of nodes in the radial dimension
dr = (a - b) / (nr - 1) # radial step
rr = b + np.dot((np.arange(0,nr)),dr) # vector for Earth's radii [m]

# Mode parameters
nmax = 9 # max radial order n
lmax = 10 # max angular order l
fmin = 0.00001 # starting frequency for eigenfrequency hunt [Hz]
fmax = 0.2 # max frequency for hunt [Hz]
df = 0.00001 # frequency step for hunt [Hz]
eigf = np.empty((nmax,lmax,)) # initialize nmax by lmax NaN matrix
eigf[:] = np.nan              # which will contain eigenfrequencies
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

for l in range(1,lmax+1):
    n = -1 # reset counter for radial degrees n
    f = fmin # we start looking for eigenfrequencies from fmin [Hz]
    wl = twopi*f # corresponding angular frequency [rad/s]

    # integrate_toroidal_system using Euler method
    [W,T,count] = euler(wl,dr,rr,rho,mu,l)
    Twmin = T[-1]

    # keep going...
