# mode_driver.py
#
# driver code for calculations
#
# Originally written by tschuh-at-princeton.edu, 12/15/2021

# To do:
#
# add radial mode calculations (all set up to do this)
# speed up calculation for large n choice
# get_integrator causes a problem in frequency_bisection when using rk4 method (something with n)

# Tests:
#
# make sure cmb radius lines up with where vs = 0
# make sure euler, rk4, and ab2 outputs are right

# Notes:
#
# tell Page to take user Nr and add 1?
# speed from fastest to slowest: euler, ab2, rk4
# solutions from different methods diverge as n increases
# larger n --> slower, no issues with l

import numpy as np
from calculations.toroidal_modes import toroidal_modes

class mode_driver():
    def __init__(self,data):
        # save data from Page's inputs to self.data
        self.data = data

        # define variables that are not user input
        # frequency-related variables
        self.fmin = 0.00001 # starting frequency for eigenfrequency hunt [Hz]
        self.fmax = 0.2 # max frequency for hunt [Hz]
        self.df = 0.00001 # frequency step for hunt [Hz]
        self.eigf = np.empty((self.data.n[-1]+1,self.data.l[-1],)) # initialize nmax by lmax NaN matrix
        self.eigf[:] = np.nan              # which will contain eigenfrequencies
        self.Tmat = np.zeros((self.data.l[-1],self.data.n[-1]+1))

    def get_modes(self):
        if self.data.mtype == 'toroidal':
            toroidal_modes(self)
        else:
            raise ValueError(self.data.mtype)
