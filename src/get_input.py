# Last modified by pdabney@princeton.edu, 12/04/21


from Model.py import *
from process_flags import *
import sys, getopt, argparse



def get_input(argv):
    # =====================================================================================
    # DESCRIPTION:
    #    Processes the user input and produces classes that will be used for computations
    #    and/or animations and plots
    #
    # INPUT:
    #    inputs         - Class containing information about the command line arguments
    # =====================================================================================
    
    # Run through command line arguments and store inputs in the class Inputs                                
    Inputs = process_input_args(sys.argv)

    # Process flags and store in proper classes
    model_class = process_flags(Inputs)

    # Include figure_class or axis_class here or in the driver?
    
    return model_class


