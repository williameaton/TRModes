# Euler.py

import numpy as np

def euler(w,dr,rr,rho,mu,l):
    
    # some initialization
    nr = len(rr)
    k2 = l*(l+1)
    W = np.zeros((nr,1))
    T = np.zeros((nr,1))

    # prescribe boundary conditions at CMB
    W[0] = 1
    T[0] = 0

    #integrate towards the surface using forward Euler method
    for i in range(1,nr):
        # call function toroidal_system
        [dW_dr,dT_dr] = toroidal_system(W[i-1],T[i-1],w,rr[i-1],rho[i-1],mu[i-1],k2)
        W[i] = W[i-1] + dr*dW_dr
        T[i] = T[i-1] + dr*dT_dr

    # count zero crossings
    # must integer divide (//) by 2 at the end because np.where
    # gives twice as many outputs as MATLAB's find() function
    count = np.size(np.where(np.absolute(np.diff(np.sign(W),axis=0))>0.1))//2
    
    return W, T, count;

def toroidal_system(W,T,w,r,rho,mu,k2):
    dW_dr = (W/r) + (T/mu)
    dT_dr = ((-(w**2)*rho) + ((k2-2)*mu)/(r**2))*W - (3/r)*T
    return dW_dr, dT_dr;
