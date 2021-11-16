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
    for i in range(2,nr+1):
        # call function toroidal_system
        [dW_dr,dT_dr] = toroidal_system(W[i-2],T[i-2],w,rr[i-2],rho[i-2],mu[i-2],k2)
        W[i-1] = W[i-2] + dr*dW_dr
        T[i-1] = T[i-2] + dr*dT_dr

    # count zero crossings
    # I think this works, we'll test more later
    count = np.size(np.argwhere(np.absolute(np.diff(np.sign(W),axis=0))>0.1))
    
    return W, T, count;

def toroidal_system(W,T,w,r,rho,mu,k2):
    dW_dr = (W/r) + (T/mu)
    dT_dr = ((-(w**2)*rho) + ((k2-2)*mu)/(r**2))*W - (3/r)*T
    return dW_dr, dT_dr;
