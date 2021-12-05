# toroidal_modes.py
#
# driver code for the Tmode calculations
#
# Originally written by tschuh-at-princeton.edu, 11/15/2021
# Last modified by tschuh-at-princeton.edu, 12/05/2021

import numpy as np
from euler import euler
from rk4 import rk4

# To do:
#
# write other ab2 integration method
# move all (most) of these constants to driver.py as inputs from Page
# connect input and output to driver.py
# speed up calculation for large n choice
# get_integrator causes a problem in frequency_bisection when using rk4 method (something with n)

# Tests:
#
# make sure cmb radius lines up with where vs = 0
# make sure euler, rk4, and ab2 outputs are right

# Notes:
#
# rk4 is much slower than euler
# rk4 solutions start to diverge from euler solutions at large n
# large n --> slower, no issues with l

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
        self.nmax = 2 # max radial order n
        self.lmin = 1 # min angular order l (l >= 1)
        self.lmax = 2 # max angular order l
        self.fmin = 0.00001 # starting frequency for eigenfrequency hunt [Hz]
        self.fmax = 0.2 # max frequency for hunt [Hz]
        self.df = 0.00001 # frequency step for hunt [Hz]
        self.eigf = np.empty((self.nmax+1,self.lmax,)) # initialize nmax by lmax NaN matrix
        self.eigf[:] = np.nan              # which will contain eigenfrequencies
        self.Tmat = np.zeros((self.lmax,self.nmax+1))

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
            [W,T,count] = rk4(w,self.dr,self.rr,self.rho,self.mu,l)
        elif self.method == 'ab2':
            pass
        else:
            raise ValueError(method)

        return W, T, count;

####################################################################

    # frequency bisection method
    def frequency_bisection(self,wmax,wmin,dr,rr,rho,mu,l,Twmin):
        # compute residuals (distance between left and right frequencies)
        res = np.absolute(wmax-wmin)

        # bisection algorithm to find roots of a function
        # where the function is T(a,w) and roots are eigenfrequencies w
        while res > np.finfo(float).eps: # loop until residual is very small (< machine epsilon)
            # try a new frequency at the center of interval [wmin,wmax]
            wc = 0.5*(wmax + wmin)

            # integrate and compute surface traction T
            #[W,T,_] = euler(wc,self.dr,self.rr,self.rho,self.mu,l)
            [W,T,_] = self.get_integrator(wc,l)
            Twc = T[-1]

            # check on which subinterval has located the root
            # basically we check if the:
            if Twc == 0: # then current surface traction is zero
                break # wc is found and we stop
            elif (Twc*Twmin) < 0: # then the root is on the left interval [wmin,wc]
                wmax = wc # wc becomes wmax
            else: # then the root is on the right interval [wc,wmax]
                wmin = wc # wc becomes wmin

            # recompute residuals
            res = np.absolute(wmax-wmin)

        # normalize eigenfunctions and recount zero crossings
        W = W / np.amax(np.absolute(W))
        T = T / np.amax(np.absolute(T))
        # must integer divide (//) by 2 at the end because np.where
        # gives twice as many outputs as MATLAB's find() function
        n = np.size(np.where(np.absolute(np.diff(np.sign(W),axis=0))>0.1))//2

        return wc, W, T, n;

####################################################################

    # actual calculation
    def Tmodes_calculation(self):
        file = open("lnw.txt","w")

        for l in range(self.lmin,self.lmax+1):
            n = -1 # reset counter for radial degrees n
            f = self.fmin # we start looking for eigenfrequencies from fmin [Hz]
            wl = 2*np.pi*f # corresponding angular frequency [rad/s]

            # integrate_toroidal_system using Euler method
            [W,T,count] = self.get_integrator(wl,l)
            Twmin = T[-1]

            # now iterate to hunt radial orders and their frequencies
            while f < self.fmax:
                # increase frequency (new candidate)
                f = f + self.df
                wr = 2*np.pi*f

                # integrate for this frequency and get surface traction
                [W,T,count] = self.get_integrator(wr,l)
                Twc = T[-1]

                # check if we have changed sign (meaning we've bracketed a root)
                if (Twc*Twmin) < 0: # then we have bracketed a root
                    # use bissection to get a precise estimate of the frequency
                    # and eigenfunctions and the radial order n
                    [wc,_,_,n] = self.frequency_bisection(wr,wl,self.dr,self.rr,self.rho,self.mu,l,Twmin)

                    # only save eigenfrequency if n >= nmin
                    # too slow
                    if n >= self.nmin:
                        # save radial order n (counted), l, and its eigenfrequency
                        self.eigf[n,l-1] = 1000*wc/(2*np.pi) # eigenfrequency [mHz]

                        # save eigenperiod
                        T0 = (2*np.pi)/wc/60 # eigenperiod [min]
                        self.Tmat[l-1,n] = T0*60 # write eigenperiod matrix [sec]

                        # print information
                        # print('Found eigenfrequency w =','%.2f'%eigf[n,l-1],'mHz for n =',n,'l =',l)

                        # save information (l,n,w) to txt file
                        lorder = repr(l)
                        norder = repr(n)
                        freq = repr(self.eigf[n,l-1])
                        file.write(lorder + " " + norder + " " + freq + "\n")

                    # check a new frequency estimate and get surface traction
                    f = wc/(2*np.pi) + self.df # update frequency [Hz]
                    [W,T,count] = self.get_integrator(f*2*np.pi,l)
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
