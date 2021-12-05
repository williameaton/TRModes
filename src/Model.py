# Last modified by pdabney@princeton.edu, 11/30/21

# Imports
import numpy as np


class Model:
    # Attributes
    def __init__(self,inputs):

        # Model parameters
        self.rho = inputs.rho
        self.mu = inputs.mu
        self.kappa = inputs.kappa
        
        self.r_min = inputs.r_min
        self.r_max = inputs.r_max
        self.dr = inputs.dr

        # Mode parameters
        self.n = inputs.n
        self.l = inputs.l
        self.method = inputs.int_method
        self.mtype = inputs.mtype

