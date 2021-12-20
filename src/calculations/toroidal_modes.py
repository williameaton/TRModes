# toroidal_modes.py
#
# driver code for the toroidal mode calculations
# for each l and n pair, use frequency bisection method
# to calculate the corresponding eigenfrequency
# also solve coupled ODE toroidal system
#
# Originally written by tschuh-at-princeton.edu, 11/15/2021
# Last modified by tschuh-at-princeton.edu, 12/20/2021

import os
import numpy as np
from calculations.integration import get_integrator
from calculations.frequency_bisection import frequency_bisection

# actual calculation
def toroidal_modes(self):
    # make an output file called lnw.txt
    lnwfile = open("lnw.txt","w")

    # if it doesnt already exist, make a directory
    # in your working directory called output_files
    # that will store Wr files
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory,r'output')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    for l in self.data.l:
        n = -1 # reset counter for radial degrees n
        f = self.fmin # we start looking for eigenfrequencies from fmin [Hz]
        wl = 2*np.pi*f # corresponding angular frequency [rad/s]

        # integrate_toroidal_system using Euler method
        [W,T,count] = get_integrator(self,wl,l)
        Twmin = T[-1]

        # now iterate to hunt radial orders and their frequencies
        while f < self.fmax:
            # increase frequency (new candidate)
            f = f + self.df
            wr = 2*np.pi*f

            # integrate for this frequency and get surface traction
            [W,T,count] = get_integrator(self,wr,l)
            Twc = T[-1]

            # check if we have changed sign (meaning we've bracketed a root)
            if (Twc*Twmin) < 0: # then we have bracketed a root
                # use bissection to get a precise estimate of the frequency
                # and eigenfunctions and the radial order n
                #[wc,_,_,n] = self.frequency_bisection(wr,wl,self.data.dr,self.data.rr,self.data.rho,self.data.mu,l,Twmin)
                [wc,_,_,n] = frequency_bisection(self,wr,wl,l,Twmin)

                # only save eigenfrequency if n >= nrange[0]
                # too slow
                if n >= self.data.n[0]:
                    # save radial order n (counted), l, and its eigenfrequency
                    self.eigf[n,l-1] = 1000*wc/(2*np.pi) # eigenfrequency [mHz]

                    # save eigenperiod
                    T0 = (2*np.pi)/wc/60 # eigenperiod [min]
                    self.Tmat[l-1,n] = T0*60 # write eigenperiod matrix [sec]

                    # save information (l,n,w) to txt file
                    # only if it was requested by user
                    if n in self.data.n:
                        lorder = repr(l)
                        norder = repr(n)
                        freq = repr(self.eigf[n,l-1])
                        lnwfile.write(lorder + " " + norder + " " + freq + "\n")

                        # write W and r to a separate file Wr_l_n.txt
                        # W and r written from inner --> outer
                        fname = "Wr_l%s_n%s.txt" % (lorder,norder)
                        Wrfile = open(os.path.join(final_directory,fname),"w")
                        Wrfile.write(lorder + " " + norder + " " + freq + "\n")
                        for r in range(len(self.data.rr)):
                            Wrfile.write(repr(W[r,0]) + " " + repr(self.data.rr[r]) + "\n")
                        Wrfile.close

                # check a new frequency estimate and get surface traction
                f = wc/(2*np.pi) + self.df # update frequency [Hz]
                [W,T,count] = get_integrator(self,f*2*np.pi,l)
                wl = wc # set current frequency as left frequency
                Twmin = T[-1] # set current surface traction as left surface traction

            else: # then we havent bracketed a frequency
                wl = wr # set current frequency as right frequency
                Twini = Twc # set current surface traction as right surface traction

            # stop search if we already have the requested number of radial orders n
            if (n+1) >= self.data.n[-1]+1:
                break

    # if we never found any eigenfrequencies bc
    # they dont fall in the range of fmin and fmax
    # then lnwfile will be empty so return error
    if np.isnan(self.eigf).all() == True:
        raise ValueError('No modes were found in the hard-coded frequency range')
        
    lnwfile.close
