# toroidal_system.py
#
# 2 coupled 1st-order ODEs for W and T
# that govern toroidal oscillations
#
# Originally written by tschuh-at-princeton.edu, 12/4/2021

import numpy as np

def toroidal_system(W,T,w,r,rho,mu,k2):
    dW_dr = (W/r) + (T/mu)
    dT_dr = ((-(w**2)*rho) + ((k2-2)*mu)/(r**2))*W - (3/r)*T
    return dW_dr, dT_dr;
