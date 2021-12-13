# rk4.py
#
# Originally written by tschuh-at-princeton.edu, 12/04/2021

import numpy as np
from calculations.toroidal_system import toroidal_system

def rk4(w,dr,rr,rho,mu,l):

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

    # integrate towards the surface using Runge-Kutta 4th order method
    for i in range(1,nr):
        Wk1 = dr[i-1]*toroidal_system(W[i-1],T[i-1],w,rr[i-1],rho[i-1],mu[i-1],k2)[0]
        Wk2 = dr[i-1]*toroidal_system(W[i-1] + 0.5*dr[i-1],T[i-1] + 0.5*float(Wk1),w,rr[i-1],rho[i-1],mu[i-1],k2)[0]
        Wk3 = dr[i-1]*toroidal_system(W[i-1] + 0.5*dr[i-1],T[i-1] + 0.5*float(Wk2),w,rr[i-1],rho[i-1],mu[i-1],k2)[0]
        Wk4 = dr[i-1]*toroidal_system(W[i-1] + dr[i-1],T[i-1] + float(Wk3),w,rr[i-1],rho[i-1],mu[i-1],k2)[0]

        Tk1 = dr[i-1]*toroidal_system(W[i-1],T[i-1],w,rr[i-1],rho[i-1],mu[i-1],k2)[1]
        Tk2 = dr[i-1]*toroidal_system(W[i-1] + 0.5*dr[i-1],T[i-1] + 0.5*float(Tk1),w,rr[i-1],rho[i-1],mu[i-1],k2)[1]
        Tk3 = dr[i-1]*toroidal_system(W[i-1] + 0.5*dr[i-1],T[i-1] + 0.5*float(Tk2),w,rr[i-1],rho[i-1],mu[i-1],k2)[1]
        Tk4 = dr[i-1]*toroidal_system(W[i-1] + dr[i-1],T[i-1] + float(Tk3),w,rr[i-1],rho[i-1],mu[i-1],k2)[1]

        W[i] = W[i-1] + (1/6)*(float(Wk1) + 2*float(Wk2) + 2*float(Wk3) + float(Wk4))
        T[i] = T[i-1] + (1/6)*(float(Tk1) + 2*float(Tk2) + 2*float(Tk3) + float(Tk4))

    # count zero crossings
    # must integer divide (//) by 2 at the end because np.where
    # gives twice as many outputs as MATLAB's find() function
    count = np.size(np.where(np.absolute(np.diff(np.sign(W),axis=0))>0.1))//2
    
    return W, T, count;
