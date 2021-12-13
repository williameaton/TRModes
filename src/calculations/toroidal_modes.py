# toroidal_modes.py
#
# driver code for the Tmode calculations
#
# Originally written by tschuh-at-princeton.edu, 11/15/2021
# Last modified by tschuh-at-princeton.edu, 12/05/2021

import os
import numpy as np
from calculations.euler import euler
from calculations.rk4 import rk4
from calculations.ab2 import ab2

# To do:
#
# speed up calculation for large n choice
# get_integrator causes a problem in frequency_bisection when using rk4 method (something with n)

# Tests:
#
# make sure cmb radius lines up with where vs = 0
# make sure euler, rk4, and ab2 outputs are right

# Notes:
#
# speed from fastest to slowest: euler, ab2, rk4
# solutions from different methods diverge as n increases
# larger n --> slower, no issues with l

####################################################################

class toroidal_modes():

    def __init__(self, data):
        # save data from Page's inputs to self.data
        self.data = data

        # define variables that are not user input
        # frequency-related variables
        self.fmin = 0.00001 # starting frequency for eigenfrequency hunt [Hz]
        self.fmax = 0.2 # max frequency for hunt [Hz]
        self.df = 0.00001 # frequency step for hunt [Hz]
        self.eigf = np.empty((self.data.nrange[-1]+1,self.data.lrange[-1],)) # initialize nmax by lmax NaN matrix
        self.eigf[:] = np.nan              # which will contain eigenfrequencies
        self.Tmat = np.zeros((self.data.lrange[-1],self.data.nrange[-1]+1))
        
####################################################################

    # integration factory
    def get_integrator(self,w,l):
        if self.data.method == 'euler':
            [W,T,count] = euler(w,self.data.dr,self.data.rr,self.data.rho,self.data.mu,l)
        elif self.data.method == 'rk4':
            [W,T,count] = rk4(w,self.data.dr,self.data.rr,self.data.rho,self.data.mu,l)
        elif self.data.method == 'ab2':
            [W,T,count] = ab2(w,self.data.dr,self.data.rr,self.data.rho,self.data.mu,l)
        else:
            raise ValueError(method)

        return W, T, count;

####################################################################

    # frequency bisection method
    #def frequency_bisection(self,wmax,wmin,dr,rr,rho,mu,l,Twmin):
    def frequency_bisection(self,wmax,wmin,l,Twmin):    
        # compute residuals (distance between left and right frequencies)
        res = np.absolute(wmax-wmin)

        # bisection algorithm to find roots of a function
        # where the function is T(a,w) and roots are eigenfrequencies w
        while res > np.finfo(float).eps: # loop until residual is very small (< machine epsilon)
            # try a new frequency at the center of interval [wmin,wmax]
            wc = 0.5*(wmax + wmin)

            # integrate and compute surface traction T
            # use Euler method for now b/c integrator factory isnt working here
            [W,T,_] = euler(wc,self.data.dr,self.data.rr,self.data.rho,self.data.mu,l)
            #[W,T,_] = self.get_integrator(wc,l)
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
        # make an output file called lnw.txt
        lnwfile = open("lnw.txt","w")

        # if it doesnt already exist, make a directory
        # in your working directory called output_files
        # that will store Wr files
        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory,r'output_files')
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)
        
        for l in self.data.lrange:
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
                    #[wc,_,_,n] = self.frequency_bisection(wr,wl,self.data.dr,self.data.rr,self.data.rho,self.data.mu,l,Twmin)
                    [wc,_,_,n] = self.frequency_bisection(wr,wl,l,Twmin)

                    # only save eigenfrequency if n >= nrange[0]
                    # too slow
                    if n >= self.data.nrange[0]:
                        # save radial order n (counted), l, and its eigenfrequency
                        self.eigf[n,l-1] = 1000*wc/(2*np.pi) # eigenfrequency [mHz]

                        # save eigenperiod
                        T0 = (2*np.pi)/wc/60 # eigenperiod [min]
                        self.Tmat[l-1,n] = T0*60 # write eigenperiod matrix [sec]

                        # print information
                        # print('Found eigenfrequency w =','%.2f'%eigf[n,l-1],'mHz for n =',n,'l =',l)

                        # save information (l,n,w) to txt file
                        # only if it was requested by user
                        if n in self.data.nrange:
                            lorder = repr(l)
                            norder = repr(n)
                            freq = repr(self.eigf[n,l-1])
                            lnwfile.write(lorder + " " + norder + " " + freq + "\n")

                            # write W and r to a separate file Wr_l_n.txt
                            # W and r written from inner --> outer
                            fname = "Wr_l=%s_n=%s.txt" % (lorder,norder)
                            Wrfile = open(os.path.join(final_directory,fname),"w")
                            #Wrfile = open(fname,"w")
                            Wrfile.write(lorder + " " + norder + " " + freq + "\n")
                            for r in range(len(self.data.rr)):
                                Wrfile.write(repr(W[r,0]) + " " + repr(self.data.rr[r]) + "\n")
                            Wrfile.close

                    # check a new frequency estimate and get surface traction
                    f = wc/(2*np.pi) + self.df # update frequency [Hz]
                    [W,T,count] = self.get_integrator(f*2*np.pi,l)
                    wl = wc # set current frequency as left frequency
                    Twmin = T[-1] # set current surface traction as left surface traction
                    
                else: # then we havent bracketed a frequency
                    wl = wr # set current frequency as right frequency
                    Twini = Twc # set current surface traction as right surface traction

                # stop search if we already have the requested number of radial orders n
                if (n+1) >= self.data.nrange[-1]+1:
                    break

        lnwfile.close
        
####################################################################
