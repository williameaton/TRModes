# Last modified by pdabney@princeton.edu, 12/13/21

#--------------------------------------------------------------------------------------------
# Imports
#--------------------------------------------------------------------------------------------

from inputs.Model import Model
from os.path import exists as file_exists
from datetime import date
import numpy as np

#--------------------------------------------------------------------------------------------
# MAIN FUNCTION
#--------------------------------------------------------------------------------------------

def process_inputs(inputs):
    # =======================================================================================
    # DESCRIPTION:
    #   Processes the flags. If called specified by the user, will launch the GUI. Otherwise,
    #   will prepare inputs for the computations and/or animations.
    #
    # INPUT:
    #    inputs         - Class containing information about the command line arguments
    # =======================================================================================

    # INPUT LOG
    attrs = vars(inputs)
    attrs_str = ', '.join("%s: %s " % item for item in attrs.items())
    # Begin log
    input_log(attrs_str)

    # --------------------------------------------------------------------------------------
    # MODEL INPUT
    
    # For the input model
    if inputs.model_file is not None:
        # Make sure file exists
        assert file_exists(inputs.model_file), 'Model file does not exist. \n'
        
        # Evaluate the data file
        Vp, Vs, rho, rr, r_max, r_min = extractfromfile(inputs.model_file)
        
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

        r_min = [eval(x) for x in inputs.r_min][0]
        r_max =	[eval(x) for x in inputs.r_max][0]
        Nr = [eval(x) for x in inputs.Nr][0]
        
        # Compute ds
        ds = (r_max - r_min) / Nr
        
        # Compute vector for radius
        rr = r_min + np.dot((np.arange(0,Nr)),ds)

        # Store as an array                                                             
        dr = [ds] * len(rr)
        
        # Obtain density and shear velocity (both are used for all computations
        rho = eval_equation(inputs.eq_rho[0], r_min, r_max, ds)
        Vs = eval_equation(inputs.eq_vs[0], r_min, r_max, ds)

        # Compute the shear modulus
        mu=[]
        for i in range(len(rho)):
            mu.append(rho[i] * (Vs[i] ** 2))

        # Maximum and minimum radius
        r_max = inputs.r_max
        r_min = inputs.r_min
                
    #----------------------------------------------------------------------------------------   
    # Calculation parameters
    if inputs.nrange is not None:
        # Convert string to an array
        n_values = str2array(inputs.nrange[0], ",")

        # Obtain n values
        n = range(n_values[1], n_values[0])
    else:
        # Convert string to an array
        n = str2array(inputs.n[0],",")


    if inputs.lrange is not None:
        # Convert string to an array
        l_values = str2array(inputs.lrange[0],",")
            
	# Obtain l values                                                                                  
        l = range(l_values[1], l_values[0])
    else:
	# Convert string to an array                                                                       
        l = str2array(inputs.l[0],",")


    # Set the model class
    model_class = Model(rho,mu,r_min,r_max,rr,dr,n,l,inputs.int_method[0],inputs.mode_type[0])
        
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
            

    #------------------------------------------------------------------------------------
    # Add input information to log
    add2log("Model Parameters","\n","1l")
    add2log("r_max", model_class.r_max[0],"1l")
    add2log("r_min", model_class.r_min[0],"1l")
    add2log("Nr", Nr,"1l")
    add2log_space()
    add2log("dr", model_class.dr,"2l")
    add2log_space()
    add2log("rr", model_class.rr,"2l")
    add2log_space()
    add2log("rho", model_class.rho,"2l")
    add2log_space()
    add2log("mu", model_class.mu,"2l")
    add2log_space()
    add2log_line()
    add2log("Mode Parameters", "\n","1l")
    add2log("mtype", model_class.mtype,"1l")
    add2log("l", model_class.l,"1l")
    add2log("n", model_class.n,"1l")
    add2log("\nIntegration Method", "\n", "1l")
    add2log("method", model_class.method,"1l")
    add2log_space()
    add2log_line()
    
    return model_class



#--------------------------------------------------------------------------------------------                     
# Supplementry Functions                                   
#--------------------------------------------------------------------------------------------
def str2array(str_in, delim):
    # =======================================================================================                         
    # DESCRIPTION:                                                                                                    
    #   Converts a string of a list of numbers to an array.
    #                                                                                                                 
    # INPUT:                                                                                                          
    #    str_in           - Input string
    #    delim            - Delimiter separating the values
    # OUTPUT:                                                                                                         
    #    array_out        - Output array 
    # ======================================================================================= 

    # Separate each value in the string
    list = str_in.split(delim)
    
    # Convert each string to a number value
    array_out = [eval(x) for x in list]

    return array_out


#------------------------------------------------------------------------------------------                       
def extractfromfile(fname):
    # =======================================================================================                         
    # DESCRIPTION:                                                                                                    
    #    Extracts compressional and shear velocity, density, and radial data points from a model text                 
    #    file (e.g. PREM). Assumes the model file is isotropic. 
    #                                                                                                                 
    # INPUT:                                                                                                          
    #    fname            - File name containing the input model.
    # OUTPUT:                                                                                                         
    #    vp               - Compressional velocity data point array 
    #    vs               - Shear velocity data point array
    #    rho              - Density data point array
    #    rr               - Radial data point array
    #    r_max            - Maximum radius
    #    r_min            - Minimum radius
    # ======================================================================================= 

    f = np.loadtxt(open(fname), skiprows=0 + 1 + 2)  # Read in file (skips the header lines)

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
    # ================================================================================================                
    # DESCRIPTION:                                                                                         
    #    Evaluates a single variable equation at discrete points and produces an array containing the
    #    solutions at each point.
    #                                                                                                                 
    # INPUT:                                                                                                          
    #    str_input        - String of a single variable equation
    #    start_value      - Start value to evaluate
    #    end_value        - End value to evaluate
    #    ds               - Step between each point
    # OUTPUT:                                                                                                         
    #    sol_array        - Array containing the solutions to the equation
    # ================================================================================================     
    sol_array = []                                   # Initialize array
    # Evaluate equation at each dr
    for r in np.arange(start_value, end_value, ds):
        sol_array.append(eval(str_input))
    return sol_array


# ----------------------------------------------------------------------------------------------------            
def input_log(inputs):
    # ================================================================================================                
    # DESCRIPTION:                                                                                                    
    #    Creates or adds to a log of the command line arguments used.
    #
    # INPUT:                                                                                                          
    #    cml_arguments     - Command line arguments (i.e. sys.argv)
    # ================================================================================================

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
    # ================================================================================================  
    # DESCRIPTION:                                                                                      
    #    Add to input log 
    #                                                                                                   
    # INPUT:                                                                                            
    #    string
    #    variable
    #    lines
    # ================================================================================================
    # Add colon to string
    added_c = string + ':'
    # Ensure even spacing
    _string = f"{added_c: <15}"
    # Open log
    f = open("input_log.txt", "a")
    if lines ==	"2l":
        f.write("\n" + _string + "\n" + str(variable))
    else:
        # Append to log
        f.write("\n" + _string + " " + str(variable))
    # Close file
    f.close()

# ----------------------------------------------------------------------------------------------------  
def add2log_line():
    # Adds a break line to log
    f = open("input_log.txt", "a")
    f.write("\n")
    f.write("----------------------------------------------------------------------------------------")
    f.close()

# ----------------------------------------------------------------------------------------------------                                              
def add2log_space():
    # Adds a break line to log                                                                                              
    f = open("input_log.txt", "a")
    f.write("\n")
    f.close()
