# mode_driver.py
#
# driver code for calculations
# depending on mode type specified by user (mtype) at runtime,
# this class calls the appropriate mode functions to calculate
# eigenfunctions W and eigenfrequencies omega
#
# Originally written by tschuh-at-princeton.edu, 12/15/2021
# Last modified by tschuh-at-princeton.edu, 12/20/2021

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
