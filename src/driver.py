# driver.py
#
# main driver code that ties input,
# calculation, and output together
#
# EXAMPLES:
#
# python driver.py -eqr 4380 -eqs 5930 -rmin 2891000 -rmax 6371000 -Nr 100 -n 0,5 -l 1,3,5 -int euler -mtype toroidal
# example1: -fig 'test1: 121 2d_radial L4 N2 M4; 122 dispersion L[1,2,3] N[1][1,2][1,2,3]' 'test2: 111 3d_animated L2 N2 M4'
# example2: -fig 'test3: 111 dispersion L[1,4,6] N_all[2-8]' 
# python driver.py -eqr '4380' -eqs '5930' -rmin 2891000 -rmax 6371000 -Nr 100 -n 0,5 -l 1,3,5 -int euler -mtype toroidal
#
# python driver.py -eqr '4380*r' -eqs '5930*r' -rmin 2891000 -rmax 6371000 -Nr 100 -n 0,5 -l 1,3,5 -int euler -mtype toroidal
#
# python driver.py -mf '/path/to/TRModes/database/prem.200' -rmin 2891000 -rmax 6371000 -n 0,5 -l 1,3,5 -int euler -mtype toroidal
# Note: change path as needed, tilde (~) doesnt work
#
# Originally written by tschuh-at-princeton.edu, 12/03/2021
# Last modified by tschuh-at-princeton.edu, 12/16/2021

import numpy as np
import sys, argparse
import os
from calculations.mode_driver import mode_driver
from inputs.Model import Model
from inputs.process_inputs import process_inputs
from inputs.process_input_fig import process_input_fig
from inputs.process_input_args import process_input_args
from plotting.ps_figure import ps_figure
from plotting.ps_axis import ps_axis

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
        print("Calculations phase...")

        calculate = mode_driver(model_class)
        calculate.get_modes()


    #--------------------------------------------------------------------------------------------
    # PLOTTING:
    # To set up classes for plottting
    if inputs.figure_output is not None:
        print("Entering plotting phase...")

        fig_list = []

        for j in range(len(inputs.figure_output)):
            fname_out, ax_locs, L, N, M, ptype = process_input_fig(inputs.figure_output[j])


            temp_axis_list = []
            # Create axis class
            for i in range(len(ax_locs)):
                if ptype[i] == 'dispersion':
                    inputs.output_filename = 'lnw.txt'
                else:
                    files = os.listdir('output/')
                    substr_l = ''.join(['l',str(L[i][0])])
                    substr_n = ''.join(['n',str(N[i][0])])
                    file_substr_l = [string for string in files if substr_l in string]
                    File = [string for string in file_substr_l if substr_n in string]
                    inputs.output_filename = ''.join(['output/',File[0]])

                # Check that an output file exists                                                           
                assert os.path.exists(inputs.output_filename), \
                    'Output file does not exist. Must compute modes. \n'
            
                temp_axis_list.append(ps_axis(type=ptype[i], data_fname=inputs.output_filename, axis_loc=ax_locs[i],
                                              N=N[i], L=L[i], M=M[i], radius=inputs.r_max))



            # Create figure class
            fig_list.append(ps_figure(temp_axis_list, fname_out))


        # Run plotting commands for each figure:
        for fig in fig_list:
            fig.plot()


#----------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    # For wills debugging need to manually assign sys.argv instead of parsing through cmd line (uncomment this):
    #sys.argv = ['driver.py', '-eqr', '4380', '-eqs', '5930', '-rmin', '2891000', '-rmax', '6371000', '-Nr', '100', '-n', '0,5', '-l', '1,3,5', '-int', 'euler', '-mtype', 'toroidal']

    driver()
#----------------------------------------------------------------------------------------------------------------------------------------------------
