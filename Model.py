# Last modified by pdabney@princeton.edu, 11/18/21

# Imports
import numpy as np

# ----------------------------------------------------------------------------------------------------
# Define Class
# ----------------------------------------------------------------------------------------------------                                 

class Model:

    def __init__(self,inputs):

        # Model parameters
        self.rho = inputs.rho
        self.mu = get_mu(inputs.Vs, inputs.rho)
        self.kappa = get_kappa(inputs.Vp, inputs.Vs, inputs.rho)
        
        self.r_min = inputs.r_min
        self.r_max = inputs.r_max
        self.dr = get_dr(inputs.Nr)

        # Mode parameters
        self.n = get_range(inputs.n)
        self.l = get_range(inputs.l)
        self.method = inputs.int_method
        self.mtype = inputs.mtype



# ----------------------------------------------------------------------------------------------------
# Define Functions
# ----------------------------------------------------------------------------------------------------

def get_mu(Vs, rho):
    
    # Computes the shear modulus (mu)  
    mu = rho * (Vs ** 2)

    return mu

# ----------------------------------------------------------------------------------------------------           
def get_kappa(Vp, Vs, rho):

    # Computes the bulk modulus (kappa) 
    kappa = rho * ((Vp ** 2) - (4/3) * (Vs ** 2))

    return kappa

# ----------------------------------------------------------------------------------------------------            
def get_dr(r_max, r_min, Nr):

    # Compute the radial step
    dr = (r_max - r_min)/Nr

    return dr

# ----------------------------------------------------------------------------------------------------           
def get_range(v_max, v_min):

    v_range = range(v_min, v_max)

    return v_range

# ----------------------------------------------------------------------------------------------------            
def eval_equation(str_input, r_max, r_min, dr):

    # Initialize array
    sol_array = []

    # Evaluate equation at each dr
    for x in np.arange(r_min, r_max, dr):
        sol_array += [eval(str_input)]

    return sol_array

# ----------------------------------------------------------------------------------------------------
def extractfromfile(fname):

    # Read in file (skips the header lines)
    f = np.loadtxt(open(fname),skiprows=0+1+2)

    # Extract Data Points                                                                    
    Vp_pts = f[:,2]                                  # Compressional (P) wave velocity 
    Vs_pts = f[:,3]                                  # Shear (S) wave velocity               
    rho_pts = f[:,1]                                 # Density

    R_pts = f[:,0]                                   # Radius
    r_max = R[-1]	      	      	     	     # Maximum radius
    r_min = R[0] 	      	      	     	     # Minimum radius
    
    return Vp_pts, Vs_pts, rho_pts, R_pts, r_max, r_min

# ----------------------------------------------------------------------------------------------------
def get_bestfit_eq(R, data):

    deg = 4                                          # Polynomial degree  

    # Determine best fit curve to the data
    coeff = np.polyfit(R, data, deg)

    # Returns the best fit equation as string
    eq = "(r ** 4) * %d + (r ** 3) * %d + (r ** 2) * %d + r * %d + %d" % (coeff[0], coeff[1], coeff[2], coeff[3], coeff[4])

    return eq

# ----------------------------------------------------------------------------------------------------


    
