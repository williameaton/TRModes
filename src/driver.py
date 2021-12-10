# driver.py
#
# this will be the main driver code that ties
# input, calculation, and output together
#
# Originally written by tschuh-at-princeton.edu, 12/03/2021
# Last modified by tschuh-at-princeton.edu, 12/09/2021
# Last modified by pdabney@princeton.edu, 12/09/21

import numpy as np
import sys
from calculations.toroidal_modes import toroidal_modes
from inputs.Model import Model
from inputs.process_inputs import process_inputs
from inputs.process_input_fig import process_input_fig
from inputs.process_input_args import process_input_args

# class dummy_inputs():
#     def __init__(self):
#         # physical planet values
#         self.a = 6371000  # Earth radius [m]
#         self.b = 2891000 # CMB radius [m]
#         self.nr = 100 # number of nodes in the radial dimension
#         self.dr = (self.a - self.b) / (self.nr - 1) # radial step
#         self.rr = self.b + np.dot((np.arange(0,self.nr)),self.dr) # vector for Earth's radii [m]

#         # mode parameters
#         # cant compute n=0, l=1 mode
#         self.nrange = [0, 5] # n >= 0
#         self.lrange = [1, 3, 5] # l >= 1

#         # integration method
#         self.method = 'euler'
        
#         # elastic parameters for a homogeneous spherical Earth model
#         self.rho0 = 4380 # mean density [kg/m^3]
#         self.vs0 = 5930 # s-wave speed [m/s]
#         self.mu0 = self.rho0*self.vs0*self.vs0 # shear modulus [Pa]
        
#         # create earth's density and shear profile for homogeneous model
#         self.rho = np.empty((self.nr,1,))
#         self.rho.fill(self.rho0)
#         self.mu = np.empty((self.nr,1,))
#         self.mu.fill(self.mu0)

# # once Page and I sort out variables that I have and she doesnt
# # and vice versa, uncomment this line
# inputs = dummy_inputs()
# #m = Model(inputs)

# # do calculations
# calculate = toroidal_modes(inputs)
# calculate.Tmodes_calculation()


def driver(sys.argv):
    
    # Store command line arguments in a class called inputs
    inputs = process_input_args(sys.argv)

    #--------------------------------------------------------------------------------------------
    # CALCULATIONS:
    
    # If this attribute exists (which is require for calculations), modes will be computed
    if hasattr(inputs, 'mode_type'):
        # Process the user inputs 
        model_class = process_inputs(inputs);

        # Compute modes
        calculate = toroidal_modes(model_class)
        calculate.Tmodes_calculation()

        # Returns output file name
        inputs.output_filename = output_filename


    #--------------------------------------------------------------------------------------------
    # PLOTTING:
    
    # To set up classes for plottting
    if hasattr(inputs, 'figure_output'):
        # Check that an output file exists
        assert file_exists(inputs.output_filename), \
            'Output file does not exist. Must compute modes. \n'

        # If there are multiple figures to produce
        for x in range(0,len(inputs.output_filename):
                # Convert input string 
                fname_out, ax_list, L, N, ptype = process_input_fig(inputs.output_filename[x])

                # Create figure class
                figure_class = ps_figure(ax_list, fname_out)

                # Create axis class
                for k in ax_list:
                       axis_class = ps_axis(inputs.mode_type, inputs.output_filename, int_required, N, L, radius, ax_list)
            
