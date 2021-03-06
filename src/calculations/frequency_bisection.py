# frequency_bisection.py
#
# frequency bisection method used to calculate eigenfrequencies
# roots of eigenfunctions are found by guessing a root and then checking
# its sign to see if it actually is a root. If not, the value is used
# as a boundary when refining the root search and the process is done
# again until a root is found (this is a bottleneck in the calculations)
#
# Originally written by tschuh-at-princeton.edu, 12/15/2021

import numpy as np
from calculations.euler import euler

# frequency bisection method
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
        [W,T,_] = euler(self.data.mtype,wc,self.data.dr,self.data.rr,self.data.rho,self.data.mu,l)
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
