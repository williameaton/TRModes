# driver.py
#
# this will be the main driver code that ties
# input, calculation, and output together
#
# Originally written by tschuh-at-princeton.edu, 12/03/2021
# Last modified by tschuh-at-princeton.edu, 12/07/2021

import numpy as np
from toroidal_modes import toroidal_modes
#from Model import Model

class dummy_inputs():
    def __init__(self):
        self.a = 6371000  # Earth radius [m]
        self.b = 2891000 # CMB radius [m]
        self.nr = 100 # number of nodes in the radial dimension
        self.dr = (self.a - self.b) / (self.nr - 1) # radial step
        self.rr = self.b + np.dot((np.arange(0,self.nr)),self.dr) # vector for Earth's radii [m]

        # Mode parameters
        # cant compute n=0, l=1 mode
        self.nmin = 0 # min radial order n (n >=0)
        self.nmax = 5 # max radial order n
        self.lrange = [1, 3, 5] # l >= 1
        self.fmin = 0.00001 # starting frequency for eigenfrequency hunt [Hz]
        self.fmax = 0.2 # max frequency for hunt [Hz]
        self.df = 0.00001 # frequency step for hunt [Hz]
        self.eigf = np.empty((self.nmax+1,self.lrange[-1],)) # initialize nmax by lmax NaN matrix
        self.eigf[:] = np.nan              # which will contain eigenfrequencies
        self.Tmat = np.zeros((self.lrange[-1],self.nmax+1))

        # Elastic parameters for a homogeneous spherical Earth model
        self.rho0 = 4380 # mean density [kg/m^3]
        self.vs0 = 5930 # s-wave speed [m/s]
        self.mu0 = self.rho0*self.vs0*self.vs0 # shear modulus [Pa]
        self.kappa = 0
        
        # create earth's density and shear profile for homogeneous model
        self.rho = np.empty((self.nr,1,))
        self.rho.fill(self.rho0)
        self.mu = np.empty((self.nr,1,))
        self.mu.fill(self.mu0)
        
        # integration method
        self.method = 'euler'

# once Page and I sort out variables that I have and she doesnt
# and vice versa, uncomment this line
inputs = dummy_inputs()
#m = Model(inputs)

# do calculations
calculate = toroidal_modes(inputs)
calculate.Tmodes_calculation()
