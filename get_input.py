# Main code to process the user inputs and convert to a class that can be passed to the computations
#
# Last modified by pdabney@princeton.edu, 11/18/21

#---------------------------------------------------------------------------------------------------                                    
# Imports
from Model.py import *


#---------------------------------------------------------------------------------------------------
def get_input():

    # Process the command line inputs
    process_flags()

    # Set the classes
    set_class()



    return model_class, ouput_class, control_class

#---------------------------------------------------------------------------------------------------                                    
