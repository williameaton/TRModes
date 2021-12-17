from inputs.Model import Model
import os
from os.path import exists as file_exists
from datetime import date
import numpy as np


def process_inputs(inputs):

    """
    Takes oject storing the user inputs and returns an model object with specifications for
    mode calculations.


    :param inputs: Users command line inputs
    :type inputs: object

    """

    # -------------------------------------------------------------------------------------- 
    # INPUT LOG:

    # remove lnw.txt if the file exists
    if file_exists('input_log.txt'):
        os.remove('input_log.txt')

    # Get string for command line inputs
    attrs = vars(inputs)
    attrs_str = ', '.join("%s: %s " % item for item in attrs.items())
    # Begin log
    input_log(attrs_str)

    
    # --------------------------------------------------------------------------------------
    # MODEL INPUT:
    
    # For the input model
    if inputs.model_file is not None:

        # Make sure file exists
        assert file_exists(inputs.model_file[0]), 'Model file does not exist. \n'
        
        # Evaluate the data file
        Vpf, Vsf, rhof, rrf, r_maxf, r_minf = extractfromfile(inputs.model_file[0])

        # Finds the closes value to the user specified maximum and minimum radius
        r_min, min_idx = nearest(rrf,float(inputs.r_min[0]))
        r_max, max_idx = nearest(rrf,float(inputs.r_max[0]))

        # Remove values outside of min and max radius range
        rr = rrf[min_idx:max_idx]
        Vs = Vsf[min_idx:max_idx]
        Vp = Vpf[min_idx:max_idx]
        rho = rhof[min_idx:max_idx]

        # Check for any zero values
        if not np.all(Vs):
            res = np.max(np.where(Vs == 0)[0])
            rr = rr[res+1:len(rr)]
            Vs = Vs[res+1:len(Vs)]
            Vp = Vp[res+1:len(Vp)]
            rho = rho[res+1:len(rho)]
            r_min = rr[0]
            print('**Minimum radius changed: ', r_min)
            
        # Compute a dr array (not evenly spaced)
        dr = rr[1:len(rr)] - rr[0:len(rr)-1]
        
        # Obtain Number of radial steps
        Nr = len(dr)
        
        # Compute the bulk and shear modulus
        mu = rho * (Vs ** 2);

            
    else:
        # Ensure a density and shear velocity equations have been inputed
        # (both are required regardless of mode type)
        assert (inputs.eq_rho is not None), 'Requires density equation. \n'
        assert (inputs.eq_vs is not None), 'Requires shear velocity equation. \n'

        # Convert string to number value
        r_min = [eval(x) for x in inputs.r_min][0]
        r_max =	[eval(x) for x in inputs.r_max][0]
        Nr = [eval(x) for x in inputs.Nr][0]
        
        # Compute ds
        ds = (r_max - r_min) / Nr
        
        # Compute vector for radius
        rr = r_min + np.dot((np.arange(0,Nr)),ds)

        # Store as an array                                                             
        dr = [ds] * (len(rr)-1)
        
        # Obtain density and shear velocity (both are used for all computations
        rho = eval_equation(inputs.eq_rho[0], r_min, r_max, ds)
        Vs = eval_equation(inputs.eq_vs[0], r_min, r_max, ds)

        # Compute the shear modulus
        mu=[]
        for i in range(len(rho)):
            mu.append(rho[i] * (Vs[i] ** 2))
        
    #----------------------------------------------------------------------------------------   
    # MODE INPUTS:
    
    if inputs.nrange is not None:
        # Convert string to an array
        n_values = str2array(inputs.nrange[0], ",")

        # Obtain n values
        n = [*range(n_values[1], n_values[0])]
    else:
        # Convert string to an array
        n = str2array(inputs.n[0],",")


    if inputs.lrange is not None:
        # Convert string to an array
        l_values = str2array(inputs.lrange[0],",")
            
	# Obtain l values                                                                                  
        l = [*range(l_values[1], l_values[0])]
    else:
	# Convert string to an array                                                                       
        l = str2array(inputs.l[0],",")

        
    #-------------------------------------------------------------------------------------------
    # Set the model class
    model_class = Model(rho,mu,r_min,r_max,rr,dr,n,l,inputs.int_method[0],inputs.mode_type[0])

    
    #-------------------------------------------------------------------------------------------
    # CHECK INPUTS:
    
    # Check that r_min is less than r_max
    assert model_class.r_min < model_class.r_max, \
    'The minimum radius must be smaller than the maximum radius'
    
    # Check the n values                                                                                 
    assert all(isinstance(x, int) for x in model_class.n), 'n values must be integers. \n'
    assert all(x >= 0 for x in model_class.n), 'n values must be zero or greater. \n'

    # Check l values
    assert all(isinstance(x, int) for x in model_class.l), 'l values must be integers. \n'
    assert all(x >= 0 for x in model_class.l) >= 0, 'l values must zero or greater. \n'

    # Check mode type input values
    input_mtype = model_class.mtype
    assert input_mtype.lower() == 'toroidal', \
        'Mode type does not exist. See Readme for details. \n'

    # Check intergration method
    input_int = model_class.method
    assert input_int.lower() == 'rk4' or input_int.lower() == 'ab2' or input_int.lower() == 'euler', \
        'Integration method does not exist. See Readme for details. \n'
            

    #--------------------------------------------------------------------------------------------
    # Add input information to log
    add2log("Model Parameters","\n",1)
    add2log("r_max", model_class.r_max,1)
    add2log("r_min", model_class.r_min,1)
    add2log("Nr", Nr,1)
    add2log_break("s")
    add2log("dr", model_class.dr,2)
    add2log_break("s")
    add2log("rr", model_class.rr,2)
    add2log_break("s")
    add2log("rho", model_class.rho,2)
    add2log_break("s")
    add2log("mu", model_class.mu,2)
    add2log_break("s")
    add2log_break("l")
    add2log("Mode Parameters", "\n",1)
    add2log("mtype", model_class.mtype,1)
    add2log("l", model_class.l,1)
    add2log("n", model_class.n,1)
    add2log("\nIntegration Method", "\n", 1)
    add2log("method", model_class.method,1)
    add2log_break("s")
    add2log_break("l")
    

    return model_class



#-------------------------------------------------------------------------------------------------                 
# Supplementry Functions                                   
#-------------------------------------------------------------------------------------------------
def str2array(str_in, delim):

    """
    Converts a list of strings to 1D array.
    
    :params str_in: String list (e.g. '1,2,3,4')
    :type str_in: string

    :params delim: Delimiter separating the values
    :type delim: string

    """
    
    # Separate each value in the string
    list = str_in.split(delim)
    
    # Convert each string to a number value
    array_out = [eval(x) for x in list]

    return array_out


#------------------------------------------------------------------------------------------  
def nearest(lst,k):

    """
    Finds the nearest value in an array and its index.


    :param lst: Array of numbers
    :type lst: 1D array

    :param k: Value to find
    :type k: float

    """

    lst = np.asarray(lst)
    ind = (np.abs(lst - k)).argmin()
        
    return lst[ind], ind


#------------------------------------------------------------------------------------------                       
def extractfromfile(fname):

    """
    Extracts compressional and shear velocity, density, maximum and minimum raduis and radial
    data points from a model text file (e.g. PREM). Assumes the model file is isotropic. 


    :param fname: File name containing the input model.
    :type fname: string

    """

    # Read in file (skips the header lines) 
    f = np.loadtxt(open(fname), skiprows=0 + 1 + 2)

    # Extract Data Points
    vp_pts = f[:, 2]  # Compressional wave velocity
    vp = vp_pts[::-1]
    vs_pts = f[:, 3]  # Shear wave velocity
    vs = vs_pts[::-1]
    rho_pts = f[:, 1]  # Density
    rho = rho_pts[::-1]
    d_pts = f[:, 0]   # Depth
    r_max = d_pts[-1]  # Maximum radius
    r_min = d_pts[0]  # Minimum radius
    R_pts = r_max - d_pts
    rr = R_pts[::-1]  

    return vp, vs, rho, rr, r_max, r_min

                                   
# ----------------------------------------------------------------------------------------------------
def eval_equation(str_input, start_value, end_value, ds):

    """
    Evaluates a single variable equation at discrete points and produces an array containing the                                                                         
    solutions at each point. 
    

    :param str_input: Single variable equation - variable must be r.
    :type str_input: string

    :param start_value: Starting value
    :type start_value: float

    :param end_value: Ending value
    :type end_value: float

    :param ds: Step between each point
    :type ds: float

    """

    sol_array = []                                   # Initialize array

    # Evaluate equation at each dr
    for r in np.arange(start_value, end_value, ds):
        sol_array.append(eval(str_input))
    return sol_array


# ----------------------------------------------------------------------------------------------------            
def input_log(inputs):

    """
    Initalizes a log file to store the user inputs and other parameters used for calculations or
    plotting.

    :param inputs: Users command line inputs.
    :type inputs: object

    """

    # Get the current date
    today = date.today()
    d = today.strftime("%m-%d-%Y")

    # Creates a file "input_log.txt" containing the input arguments
    f = open("input_log.txt", "a")

    # Write command line arguments 
    f.write("----------------------------------------------------------------------------------------")
    f.write("\n" + "Date: " + d + "\n")
    f.write("\n" + "Command Line Input Arguments: \n")
    f.write("\n" + str(inputs) + "\n" + "\n")
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
