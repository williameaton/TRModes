# ab2.py
#
# Originally written by tschuh-at-princeton.edu,12/05/2021

import numpy as np
from calculations.toroidal_system import toroidal_system

def ab2(w,dr,rr,rho,mu,l):

    #############################################################
    
    # some initialization
    nr = len(rr)
    k2 = l*(l+1)
    W = np.zeros((nr,1))
    T = np.zeros((nr,1))

    # prescribe boundary conditions at CMB
    W[0] = 1
    T[0] = 0

    #############################################################

    # integrate towards the surface using Adams-Bashforth 2nd order method
    counter = 0
    for i in range(1,nr):

        if counter == 0:
            # use Euler method for 1st step
            W[i] = W[i-1] + dr[i-1]*toroidal_system(W[i-1],T[i-1],w,rr[i-1],rho[i-1],mu[i-1],k2)[0]
            T[i] = T[i-1] + dr[i-1]*toroidal_system(W[i-1],T[i-1],w,rr[i-1],rho[i-1],mu[i-1],k2)[1]
            counter = 1
        else:
            W[i] = W[i-1] + (3/2)*dr[i-1]*toroidal_system(W[i-1],T[i-1],w,rr[i-1],rho[i-1],mu[i-1],k2)[0] - (1/2)*dr[i-2]*toroidal_system(W[i-2],T[i-2],w,rr[i-2],rho[i-2],mu[i-2],k2)[0]
            T[i] = T[i-1] + (3/2)*dr[i-1]*toroidal_system(W[i-1],T[i-1],w,rr[i-1],rho[i-1],mu[i-1],k2)[1] - (1/2)*dr[i-2]*toroidal_system(W[i-2],T[i-2],w,rr[i-2],rho[i-2],mu[i-2],k2)[1]
            
    # count zero crossings
    # must integer divide (//) by 2 at the end because np.where
    # gives twice as many outputs as MATLAB's find() function
    count = np.size(np.where(np.absolute(np.diff(np.sign(W),axis=0))>0.1))//2
    
    return W, T, count;
