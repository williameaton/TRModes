# Last modified by pdabney@princeton.edu, 12/13/21

class Model:
    # Attributes
    def __init__(self,rho, mu, r_min, r_max, rr, dr, n, l,method, mtype):

        # Model parameters
        self.rho = rho
        self.mu = mu
        
        self.r_min = r_min
        self.r_max = r_max
        self.dr = dr
        self.rr = rr
        
        # Mode parameters
        self.n = n
        self.l = l
        self.mtype = mtype

        # Integration Method
        self.method = method
