# Last modified by pdabney@princeton.edu, 11/30/21

# Imports
import numpy as np


class Model:
    # Attributes
    def __init__(self,inputs):

        # Model parameters
        self.rho = inputs.rho
        self.mu = self.get_mu(inputs.Vs, inputs.rho)
        self.kappa = self.get_kappa(inputs.Vp, inputs.Vs, inputs.rho)
        
        self.r_min = inputs.r_min
        self.r_max = inputs.r_max
        self.dr = inputs.Nr

        # Mode parameters
        self.n = inputs.n
        self.l = inputs.l
        self.method = inputs.int_method
        self.mtype = inputs.mtype


    # Functions
    def get_mu(Vs, rho):
        # Computes the shear modulus
        mu = rho * (Vs ** 2)
        return mu

    def get_kappa(Vp, Vs, rho):
        # Computes the bulk modulus
        kappa = rho * ((Vp ** 2) - (4 / 3) * (Vs ** 2))
        return kappa

    
