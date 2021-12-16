# radial_system.py
#
# 6 coupled 1st-order ODEs for U, V, P, R, S, and B
# that govern radial oscillations
#
# Originally written by tschuh-at-princeton.edu, 12/15/2021

import numpy as np

def radial_system(U,V,P,R,S,B,w,r,rho,mu,kappa,k2,l):

    # define gravitational constant [N*m^2/kg^2]
    G = 6.67e-11
    # define g for specific planet
    # need to define mass and radius of planet
    g = G*M/(r**2)
    
    dU_dr = -2*((kappa+(4/3)*mu)**-1)*(kappa-(2/3)*mu)*(U/r) + k2*((kappa+(4/3)*mu)**-1)*(kappa-(2/3)*mu)*(V/r) + ((kappa+(4/3)*mu)**-1)*R
    dV_dr = -k2*(U/r) + (V/r) + (S/mu)
    dP_dr = -4*np.pi*G*rho*U - (l+1)*(P/r) + B
    dR_dr = (-(w**2)*rho - (4*rho*g)/r + ((12*kappa*mu)/(r**2))*((kappa+(4/3)*mu)**-1))*U + (((k2*rho*g)/r) - ((6*k2*kappa*mu)/(r**2))*((kappa+(4/3)*mu)**-1))*V - ((4*mu)/r)*((kappa+(4/3)*mu)**-1)*R + ((k2*S)/r) - (((l+1)*rho*P)/r) + rho*B
    dS_dr = (((k2*rho*g)/r) - ((6*k2*kappa*mu)/(r**2))*((kappa+(4/3)*mu)**-1))*U - ((w**2)*rho + ((2*mu)/(r**2)) - ((4*(k2**2)*mu*(kappa+(1/3)*mu)*((kappa+(4/3)*mu)**-1))/(r**2)))*V - ((k2*(kappa-(2/3)*mu)*((kappa+(4/3)*mu)**-1))/r)*R - ((3*S)/r) + ((k2*rho*P)/r)
    dB_dr = ((-4*np.pi*G*(l+1)*rho*U)/r) + ((4*np.pi*G*k2*rho*V)/r) + (((l-1)*B)/r)
    return dU_dr, dV_dr, dP_dr, dR_dr, dS_dr, dB_dr;
