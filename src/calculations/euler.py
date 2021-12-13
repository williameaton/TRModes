# euler.py
#
# Originally written by tschuh-at-princeton.edu, 11/15/2021
# Last modified by tschuh-at-princeton.edu, 12/04/2021

import numpy as np
from calculations.toroidal_system import toroidal_system

def euler(w,dr,rr,rho,mu,l):

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
    
    # integrate towards the surface using forward Euler method
    for i in range(1,nr):
        # toroidal_system computes dW/dr and dT/dr
        W[i] = W[i-1] + dr[i-1]*toroidal_system(W[i-1],T[i-1],w,rr[i-1],rho[i-1],mu[i-1],k2)[0]
        T[i] = T[i-1] + dr[i-1]*toroidal_system(W[i-1],T[i-1],w,rr[i-1],rho[i-1],mu[i-1],k2)[1]
        
    # count zero crossings
    # must integer divide (//) by 2 at the end because np.where
    # gives twice as many outputs as MATLAB's find() function
    count = np.size(np.where(np.absolute(np.diff(np.sign(W),axis=0))>0.1))//2
    
    return W, T, count;
