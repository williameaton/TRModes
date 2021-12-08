# driver.py
#
# this will be the main driver code that ties
# input, calculation, and output together
#
# Originally written by tschuh-at-princeton.edu, 12/03/2021
# Last modified by tschuh-at-princeton.edu, 12/07/2021
# Last modified by pdabney@princeton.edu, 12/07/2021

import numpy as np
import sys, argparse
from datetime import data
from os.path import exists as file_exists
from toroidal_modes import toroidal_modes
from Model import Model
from process_flags import *



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
                       
                       
