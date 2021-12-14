class Model:

    """
    Model objects are created from the users inputs to store and pass specifications for the
    computation of mode frequencies. These objects hold model parameters, mode parameters, and
    the integration method.
    """
    
    def __init__(self, rho, mu, r_min, r_max, rr, dr, n, l, method, mtype):

        """
        :param rho: Density values from input model.
        :type rho: 1D array

        :param mu: Shear modulus values computed from model data.
        :type mu: 1D array

        :param r_min: Minimum radius of elastic body.
        :type r_min: float
        
        :param r_max: Maximum radius of elastic body.
        :type r_max: float

        :param dr: Radial step between data points. May be an array of constants or a varying array.
        :type dr: 1D array

        :param rr: Radial data values from input model.
        :type rr: 1D array

        :param n: Radial order values to compute mode frequencies for.
        :type n: int or 1D array

        :param l: Angular order values to compute mode frequencies for.
        :type l: int or 1D array

        :param mtype: Type of mode to compute. Currently computes "toroidal".
        :type mtype: string

        :param method: Integration method for compuation. Currently supports Euler ("euler"), 2nd-order Adams-Bashforth ("ab2") or 4th-order Runge-Kutta ("rk4").
        :type method: string

        """
        
        # Model parameters
        self.rho = rho                     # Density
        self.mu = mu                       # Shear modulus         
        
        self.r_min = r_min                 # Minimum radius 
        self.r_max = r_max                 # Maximum radius
        self.dr = dr                       # Radial step
        self.rr = rr                       # Radial points
        
        # Mode parameters
        self.n = n                         # Radial order
        self.l = l                         # Angular order
        self.mtype = mtype                 # Mode Type

        self.method = method               # Integration method
