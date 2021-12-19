import os
from os.path import exists as file_exists
from datetime import date


def input_log(inputs):

    """
    Initalizes a log file to store the user inputs and other parameters used for calculations or
    plotting.

    :param inputs: Users command line inputs.
    :type inputs: object

    """

    # remove lnw.txt if the file exists                                                                                                  
    if file_exists('input_log.txt'):
        os.remove('input_log.txt')
        
    # Get the current date
    today = date.today()
    d = today.strftime("%m-%d-%Y")

    # Get string for command line inputs                                                                                                     
    attrs = vars(inputs)
    attrs_str = ', '.join("%s: %s " % item for item in attrs.items())
    
    # Creates a file "input_log.txt" containing the input arguments
    f = open("input_log.txt", "a")

    # Write command line arguments 
    f.write("----------------------------------------------------------------------------------------")
    f.write("\n" + "Date: " + d + "\n")
    f.write("\n" + "Command Line Input Arguments: \n")
    f.write("\n" + str(attrs_str) + "\n" + "\n")
    f.write("----------------------------------------------------------------------------------------")
    
    if inputs.output_file is not None:
        f.write("\n" + "\n" + "Output File:   " + inputs.output_file[0] + "\n" + "\n")
        f.write("----------------------------------------------------------------------------------------")

    # Close file
    f.close()

    
# ----------------------------------------------------------------------------------------------------
def add2log(string, variable, lines):

    """
    Adds variables to log.

    
    :param string: Variable name.
    :type string: string

    :param variable: Value of the variable.
    :type variable: float, string or 1D array

    :param lines: Number of lines to write the log. Current options are in one line (1) or two lines (2).
    :type lines: int

    """
    
    # Add colon to string
    added_c = string + ':'
    # Ensure even spacing
    _string = f"{added_c: <15}"

    # Open log
    f = open("input_log.txt", "a")
    # Append to log
    if lines ==	2:
        f.write("\n" + _string + "\n" + str(variable))
    elif lines == 1:
        f.write("\n" + _string + " " + str(variable))

    # Close file
    f.close()

# ----------------------------------------------------------------------------------------------------  
def add2log_break(btype):

    """
    Adds a break line or space to the input log.


    :param btype: Break type. Currently takes a line break ("l") or space break ("s").
    :type btype: string

    """
    
    # Adds a break line to log
    f = open("input_log.txt", "a")
    # Append to log
    if btype == "s":
        f.write("\n")
    elif btype == "l":
        f.write("\n")
        f.write("----------------------------------------------------------------------------------------")

    # Close file
    f.close()
