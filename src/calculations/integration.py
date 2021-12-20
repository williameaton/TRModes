# integration.py
#
# integrator factory where depending on the integration
# method specified by the user at runtime, it is chosen and
# implemented here
#
# Originally written by tschuh-at-princeton.edu, 12/15/2021

from calculations.euler import euler
from calculations.rk4 import rk4
from calculations.ab2 import ab2

# integration factory
def get_integrator(self,w,l):
    if self.data.method == 'euler':
        [W,T,count] = euler(self.data.mtype,w,self.data.dr,self.data.rr,self.data.rho,self.data.mu,l)
    elif self.data.method == 'rk4':
        [W,T,count] = rk4(self.data.mtype,w,self.data.dr,self.data.rr,self.data.rho,self.data.mu,l)
    elif self.data.method == 'ab2':
        [W,T,count] = ab2(self.data.mtype,w,self.data.dr,self.data.rr,self.data.rho,self.data.mu,l)
    else:
        raise ValueError(self.data.method)

    return W, T, count;
