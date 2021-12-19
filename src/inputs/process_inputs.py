from inputs.Model import Model
from inputs.input_log import add2log, add2log_break
from os.path import exists as file_exists
import numpy as np
import pytest
import os

def process_inputs(inputs):

    """
    Takes oject storing the user inputs and returns an model object with specifications for
    mode calculations.


    :param inputs: Users command line inputs
    :type inputs: object

    """

    
    # --------------------------------------------------------------------------------------
    # MODEL INPUT:
    
    # For the input model
    if inputs.model_file is not None:

        # Make sure file exists
        assert file_exists(inputs.model_file[0]), 'Model file does not exist. \n'
        
        # Evaluate the data file
        Vpf, Vsf, rhof, rrf, r_maxf, r_minf = extractfromfile(inputs.model_file[0])

        # Finds the closes value to the user specified maximum and minimum radius
        rmin, min_idx = nearest(rrf,float(inputs.r_min[0]))
        rmax, max_idx = nearest(rrf,float(inputs.r_max[0]))

        idx = [min_idx, max_idx]
        # Ensure the order of the indexes are increasing
        idx.sort()
        
        # Remove values outside of min and max radius range
        rr = rrf[idx[0]:idx[1]]
        Vs = Vsf[idx[0]:idx[1]]
        Vp = Vpf[idx[0]:idx[1]]
        rho = rhof[idx[0]:idx[1]]
        
        
        # Check for any zero values and update array
        if not np.all(Vs):
            res = Vs != 0
            id_min, id_max = res.argmax()-1, res.size - res[::-1].argmax()
            rr = rr[id_min+1:id_max]
            Vs = Vs[id_min+1:id_max]
            Vp = Vp[id_min+1:id_max]
            rho = rho[id_min+1:id_max]
            
            # Let the user know that the radius has changed
            if float(inputs.r_max[0]) != rr[-1]:
                print('** Maximum radius changed: ', rr[-1])
            if float(inputs.r_min[0]) != rr[0]:
                print('** Minimum radius changed: ', rr[0])

        # Get minimum and maximum radii
        r_max = rr[-1]
        r_min = rr[0]
        
        # Compute a dr array (not evenly spaced)
        dr = rr[1:len(rr)+1] - rr[0:len(rr)-1]
        
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
        rrv = r_min + np.dot((np.arange(0,Nr+1)),ds)
        rr = rrv.tolist()
        
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
        n = [*range(n_values[0], n_values[1]+1)]
    else:
        # Convert string to an array
        n = str2array(inputs.n[0],",")


    if inputs.lrange is not None:
        # Convert string to an array
        l_values = str2array(inputs.lrange[0],",")
            
	# Obtain l values                                                                                  
        l = [*range(l_values[0], l_values[1]+1)]
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
    vp = f[:, 2]    # Compressional wave velocity
    vs = f[:, 3]    # Shear wave velocity
    rho = f[:, 1]   # Density
    rr = f[:, 0]    # radius
    r_min = rr[-1]  # Maximum radius
    r_max = rr[0]   # Minimum radius

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


