# driver.py
#
# this will be the main driver code that ties
# input, calculation, and output together
#
# EXAMPLE:
#
# python driver.py -eqr '-2.8471e-7*(r**3)+3.84976e-3*(r**2)-17.6479*r+32447.9' -eqs sqrt(mu/rho) rmin 2891000 -rmax 6371000 -Nr 100 -n 0,5 -l 1,3,5 -int euler -mtype toroidal
#
# python driver.py -eqr 4380 -eqs 5930 -rmin 2891000 -rmax 6371000 -Nr 100 -n 0,5 -l 1,3,5 -int euler -mtype toroidal
#
# python driver.py -mf '/home/pdabney/APC524/Final_Project/TRModes/database/prem.200' -rmin 2891000 -rmax 6371000 -n 0,5 -l 1,3,5 -int euler -mtype toroidal
# Note: change path as needed
#
#
# Originally written by tschuh-at-princeton.edu, 12/03/2021
# Last modified by tschuh-at-princeton.edu, 12/13/2021
# Last modified by pdabney@princeton.edu, 12/14/2021

import numpy as np
import sys, argparse
import os
from calculations.toroidal_modes import toroidal_modes
from inputs.Model import Model
from inputs.process_inputs import process_inputs
from inputs.process_input_fig import process_input_fig
from inputs.process_input_args import process_input_args
from plotting.ps_figure import ps_figure
from plotting.ps_axis import ps_axis
'''
class dummy_inputs():
     def __init__(self):
          # physical planet values
          self.r_max = 6371000  # Earth radius [m]
          self.r_min = 2891000 # CMB radius [m]
          self.nr = 100 # number of nodes in the radial dimension
          self.dr = np.empty((self.nr))
          self.dr.fill((self.r_max - self.r_min)/(self.nr - 1))
          for i in range(1,self.nr):
              self.rr = self.r_min + np.dot((np.arange(0,self.nr)),self.dr[i]) # vector for Earth's radii [m]

          # mode parameters
          # cant compute n=0, l=1 mode
          self.nrange = [0, 5] # n >= 0
          self.lrange = [1, 3, 5] # l >= 1

          # integration method
          self.method = 'euler'

          # create earth's density and shear profile for homogeneous spherical Earth model
          self.rho = np.empty((self.nr))
          self.rho.fill(4380) # mean density [kg/m^3]
          self.mu = np.empty((self.nr))
          self.mu.fill(4380*(5930**2)) # shear modulus [Pa] = rho0*(vs0)^2
          self.kappa = np.empty((self.nr))
          self.kappa.fill(4380*(6000**2) - ((4/3)*(4380*(5930**2)))) # bulk modulus [Pa] = rho*(vp)^2 - (4/3)*mu
'''
 #inputs = dummy_inputs()

# do calculations
# calculate = mode_driver(inputs)
# calculate.get_modes()
# inputs = process_input_args()                                                                            


def driver():

    # Store command line arguments in a class called inputs
    inputs = process_input_args()

    #--------------------------------------------------------------------------------------------
    # CALCULATIONS:

    # If this attribute exists (which is require for calculations), modes will be computed
    if inputs.mode_type is not None:

        # Process the user inputs
        model_class = process_inputs(inputs);

        # Compute modes
        calculate = mode_driver(model_class)
        calculate.get_modes()

        # Returns output file name
        inputs.output_filename = "lnw.txt"

        #--------------------------------------------------------------------------------------------
        # PLOTTING:
        # To set up classes for plottting
        if hasattr(inputs, 'figure_output'):
            # Check that an output file exists
            assert os.path.exists(inputs.output_filename), \
                'Output file does not exist. Must compute modes. \n'

            #"test1we: 121 2D_radial_plot L[[ N2; 122 dispersion L1,2,3 N[1][1,2][1,2,3]"


            # SOME DUMMY EXAMPLE CASES:
            FNAME_OUT = ["test1we", "test2we"]
            AX_LOCS   = [[121, 122], [111]]
            PTYPES    = [["radial_2D_plot", "radial_2D_plot"], ["3D_animated"]]
            # In these cases I avoided a dispersion plot as wasnt sure how the n, l, m are put in, I assume they would go in
            # The first sublist so it was like this:
            #   n = [[[1,2,5], [5]], [[5]]]
            #   l = [[[1,2,3], [5]], [[5]]]
            #   m = [[[0,0,0], [0]], [[0]]]
            # Or something but I tried something like that and got an error so hoppefully Huda can fix it!

            n         = [[[5], [5]], [[5]]]
            l         = [[[3], [5]], [[5]]]
            m         = [[[0], [0]], [[3]]]

            fig_list = []
            # If there are multiple figures to produce
            #for x in range(0,len(inputs.output_filename)):
            for j in range(2):

                # Convert input string
                #fname_out, ax_locs, L, N, ptype = process_input_fig(inputs.output_filename[x])

                fname_out = FNAME_OUT[j]
                ax_locs = AX_LOCS[j]
                ptype = PTYPES[j]
                N = n[j]
                L = l[j]
                M = m[j]

                temp_axis_list = []
                # Create axis class
                for i in range(len(ax_locs)):

                    temp_axis_list.append(ps_axis(type=ptype[i], data_fname=inputs.output_filename, axis_loc=ax_locs[i],
                                                  N=N[i], L=L[i], M=M[i], radius=inputs.r_max))

                # Create figure class
                fig_list.append(ps_figure(temp_axis_list, fname_out))


            # Run plotting commands for each figure:
            for fig in fig_list:
                fig.plot()


#----------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Okay this now works for some cases of the cmd line input. It works for a simple case like the one that Terry put in e.g.:
    # python driver.py -eqr 4380 -eqs 5930 -rmin 2891000 -rmax 6371000 -Nr 100 -n 0,5 -l 1,3,5 -int euler -mtype toroidal
    # Importantly it DOES NOT work for Page's example. The reason for this is that it isnt happy reading in the equation page uses for -eqr...not sure what
    # Page has been doing before to run this from the command line but page can you make sure this works?


    # For wills debugging need to manually assign sys.argv instead of parsing through cmd line (uncomment this):
    #sys.argv = ['driver.py', '-eqr', '4380', '-eqs', '5930', '-rmin', '2891000', '-rmax', '6371000', '-Nr', '100', '-n', '0,5', '-l', '1,3,5', '-int', 'euler', '-mtype', 'toroidal']

    driver()
#----------------------------------------------------------------------------------------------------------------------------------------------------
