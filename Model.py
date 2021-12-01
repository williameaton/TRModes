# Last modified by pdabney@princeton.edu, 11/18/21

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
        self.dr = self.get_dr(inputs.Nr)

        # Mode parameters
        self.n = self.get_range(inputs.n)
        self.l = self.get_range(inputs.l)
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

    
    def get_dr(r_max, r_min, Nr):
        # Computes the radial step
        dr = (r_max - r_min) / Nr
        return dr

    
    def get_range(v_max, v_min):
        # Obtains the consecutive range of integer values between two values
        v_range = range(v_min, v_max)
        return v_range

    
    def eval_equation(str_input, start_value, end_value, dr):
        # Evaluates a single variable equation at discrete points and produces an array containing the
        # solutions
        sol_array = []                                   # Initialize array

        # Evaluate equation at each dr
        for x in np.arange(start_value, end_value, dr):
            sol_array += [eval(str_input)]
        return sol_array




