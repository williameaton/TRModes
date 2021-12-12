# Last modified by pdabney@princeton.edu, 12/12/21

class Model:
    # Attributes
    def __init__(self,inputs):

        # Model parameters
        self.rho = inputs.rho
        self.mu = inputs.mu
        
        self.r_min = inputs.r_min
        self.r_max = inputs.r_max
        self.dr = inputs.dr
        self.rr = inputs.rr
        
        # Mode parameters
        self.n = inputs.n
        self.l = inputs.l
        self.mtype = inputs.mtype

        # Integration Method
        self.method = inputs.int_method
