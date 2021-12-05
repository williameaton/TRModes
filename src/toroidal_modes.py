# toroidal_modes.py
#
# Originally written by tschuh-at-princeton.edu, 11/15/2021
# Last modified by tschuh-at-princeton.edu, 12/02/2021

import numpy as np
from euler import euler
from frequency_bisection import frequency_bisection

# To do:
#
# write other integration methods (rk4 and ab2) 
# eventually all (most) of these constants will come from Page as input
# make driver code

# Tests:
#
# make sure cmb radius lines up with where vs = 0

####################################################################

class toroidal_modes():

    def __init__(self):
        # Base parameters for discretization and radial integration
        self.a = 6371000 # Earth radius [m]
        self.b = 2891000 # CMB radius [m]
        self.nr = 100 # number of nodes in the radial dimension
        self.dr = (self.a - self.b) / (self.nr - 1) # radial step
        self.rr = self.b + np.dot((np.arange(0,self.nr)),self.dr) # vector for Earth's radii [m]

        # Mode parameters
        # cant compute n=0, l=1 mode
        self.nmin = 0 # min radial order n (n >=0)
        self.nmax = 1 # max radial order n
        self.lmin = 1 # min angular order l (l >= 1)
        self.lmax = 2 # max angular order l
        self.fmin = 0.00001 # starting frequency for eigenfrequency hunt [Hz]
        self.fmax = 0.2 # max frequency for hunt [Hz]
        self.df = 0.00001 # frequency step for hunt [Hz]
        self.eigf = np.empty((self.nmax+1,self.lmax,)) # initialize nmax by lmax NaN matrix
        self.eigf[:] = np.nan              # which will contain eigenfrequencies
        self.Tmat = np.zeros((self.lmax,self.nmax+1))
        self.twopi = 2*np.pi # constant 2pi

        # Elastic parameters for a homogeneous spherical Earth model
        self.rho0 = 4380 # mean density [kg/m^3]
        self.vs0 = 5930 # s-wave speed [m/s]
        self.mu0 = self.rho0*self.vs0*self.vs0 # shear modulus [Pa]
        
        # create earth's density and shear profile for homogeneous model
        self.rho = np.empty((self.nr,1,))
        self.rho.fill(self.rho0)
        self.mu = np.empty((self.nr,1,))
        self.mu.fill(self.mu0)
        
        # integration method
        self.method = 'euler'

####################################################################

    # integration factory
    def get_integrator(self,w,l):
        if self.method == 'euler':
            [W,T,count] = euler(w,self.dr,self.rr,self.rho,self.mu,l)
        elif self.method == 'rk4':
            pass
        elif self.method == 'ab2':
            pass
        else:
            raise ValueError(method)

        return W, T, count;

####################################################################

    def Tmodes_calculation(self):
        file = open("lnw.txt","w")

        for l in range(self.lmin,self.lmax+1):
            n = -1 # reset counter for radial degrees n
            f = self.fmin # we start looking for eigenfrequencies from fmin [Hz]
            wl = self.twopi*f # corresponding angular frequency [rad/s]

            # integrate_toroidal_system using Euler method
            [W,T,count] = self.get_integrator(wl,l)
            Twmin = T[-1]

            # now iterate to hunt radial orders and their frequencies
            while f < self.fmax:
                # increase frequency (new candidate)
                f = f + self.df
                wr = self.twopi*f

                # integrate for this frequency and get surface traction
                [W,T,count] = self.get_integrator(wr,l)
                Twc = T[-1]

                # check if we have changed sign (meaning we've bracketed a root)
                if (Twc*Twmin) < 0: # then we have bracketed a root
                    # use bissection to get a precise estimate of the frequency
                    # and eigenfunctions and the radial order n
                    [wc,_,_,n] = frequency_bisection(wr,wl,self.dr,self.rr,self.rho,self.mu,l,Twmin)

                    # only save eigenfrequency if n >= nmin
                    # too slow
                    if n >= self.nmin:
                        # save radial order n (counted), l, and its eigenfrequency
                        self.eigf[n,l-1] = 1000*wc/self.twopi # eigenfrequency [mHz]

                        # save eigenperiod
                        T0 = self.twopi/wc/60 # eigenperiod [min]
                        self.Tmat[l-1,n] = T0*60 # write eigenperiod matrix [sec]

                        # print information
                        # print('Found eigenfrequency w =','%.2f'%eigf[n,l-1],'mHz for n =',n,'l =',l)

                        # save information (l,n,w) to txt file
                        lorder = repr(l)
                        norder = repr(n)
                        freq = repr(self.eigf[n,l-1])
                        file.write(lorder + " " + norder + " " + freq + "\n")

                    # check a new frequency estimate and get surface traction
                    f = wc/self.twopi + self.df # update frequency [Hz]
                    [W,T,count] = self.get_integrator(f*self.twopi,l)
                    wl = wc # set current frequency as left frequency
                    Twmin = T[-1] # set current surface traction as left surface traction

                else: # then we havent bracketed a frequency
                    wl = wr # set current frequency as right frequency
                    Twini = Twc # set current surface traction as right surface traction

                # stop search if we already have the requested number of radial orders n
                if (n+1) >= self.nmax+1:
                    break

        file.close
        
####################################################################
