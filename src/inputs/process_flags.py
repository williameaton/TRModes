# Last modified by pdabney@princeton.edu, 12/09/21

#--------------------------------------------------------------------------------------------
# Imports
#--------------------------------------------------------------------------------------------


from Model.py import *
import sys, getopt, argparse
from datetime import date
from os.path import exists as file_exists

#--------------------------------------------------------------------------------------------
# MAIN FUNCTION
#--------------------------------------------------------------------------------------------

def process_flags(inputs):
    # =======================================================================================
    # DESCRIPTION:
    #   Processes the flags. If called specified by the user, will launch the GUI. Otherwise,
    #   will prepare inputs for the computations and/or animations.
    #
    # INPUT:
    #    inputs         - Class containing information about the command line arguments
    # =======================================================================================

    # Initialize class
    model_class = Model()
    
    # Process the flags
    if bool(inputs.gui):
        # launch gui
        pass

    
    # --------------------------------------------------------------------------------------- 
    # USE EXISTING OUTPUT FILE TO OBTAIN VISUALS
    elif hasattr(inputs, "output_filename"):
        data_fname = inputs.output_filename
    
    # ---------------------------------------------------------------------------------------
    # SET UP INPUTS TO COMPUTE MODES
    else:
        # For the input model
        if hasattr(inputs, "model_file"):
            # Make sure file exists
            assert file_exists(inputs.model_file), 'Model file does not exist. \n'
            
            # Evaluate the data file
            Vp_pts, Vs_pts, rho_pts, R_pts, model_class.r_max, model_class.r_min = extractfromfile(inputs.model_file)

            # Compute dr
            model_class.dr = (model_class.r_max - model_class.r_min) / inputs.Nr

            # Obtain equations for rho, Vs, Vp in order to resample
            rho_eq = get_bestfit_eq(R_pts, rho_pts)
            Vs_eq = get_bestfit_eq(R_pts, Vs_pts)
            Vp_eq = get_bestfit_eq(R_pts, Vp_pts)

            # Evaluate the equations
            rho = eval_equation(rho_eq, model_class.r_min, model_class.r_max, model_class.dr)
            Vs = eval_equation(Vs_eq, model_class.r_min, model_class.r_max, model_class.dr)
            Vp = eval_equation(Vp_eq, model_class.r_min, model_class.r_max, model_class.dr)

            # Compute the bulk and shear modulus
            model_class.kappa = rho * ((Vp ** 2) - (4 / 3) * (Vs ** 2));
            model_class.mu = rho * (Vs ** 2);
            
        else:
            # Ensure a density and shear velocity equations have been inputed
            # (both are required regardless of mode type)
            assert hasattr(inputs,'eq_rho'), 'Requires density equation. \n'
            assert hasattr(inputs,'eq_vs'), 'Requires shear velocity equation. \n'
                
            # Compute dr                                                                                          
            model_class.dr = (inputs.r_max - inputs.r_min) / inputs.Nr
            
            # Obtain density and shear velocity (both are used for all computations
            rho = eval_equation(inputs.rho_eq, inputs.r_min, inputs.r_max, model_class.dr)            
            Vs = eval_equation(inputs.eq_vs, inputs.r_min, inputs.r_max, model_class.dr)

            # Compute the shear modulus
            model_class.mu = rho * (Vs ** 2);

            
            if inputs.mtype == "Radial":
      	        # Check the user has inputted a compressional velocity equation
                assert hasattr(inputs,'eq_vp'), 'Requires compressional velocity equation. \n'

            	# Obtain compressional velocity
                Vp = eval_equation(inputs.eq_vp, inputs.r_min, inputs.r_max, model_class.dr)

                # Compute the bulk modulus
                model_class.kappa = rho * ((Vp ** 2) - (4 / 3) * (Vs ** 2));

                
        #----------------------------------------------------------------------------------------   
        # Model parameters
        
        if hasattr(inputs,"nrange"):
	    # Convert string to an array                                                                          
	    n_values = str2array(inputs.nrange)
            
            # Obtain n values
            model_class.n = range(n_values[1], n_values[0])
            
        else:
            # Convert string to an array                                                       
            model_class.n = str2array(inputs.n)

        # Check the n values
        assert all(isinstance(x, int) for x in model_class.n), 'n values must be integers. \n'
        assert model_class.n >= 0, 'n values must be zero or greater. \n'
                                   
        if hasattr(inputs,"lrange"):
            # Convert string to an array
	    l_values = str2array(inputs.lrange,",")
            
	    # Obtain l values                                                                                     
            model_class.l = range(l_values[1], l_values[0]) 

        else:
	    # Convert string to an array                                                                          
            model_class.l = str2array(inputs.l,",")

        # Check l values                           
        assert all(isinstance(x, int) for x in model_class.l), 'l values must be integers. \n'
        assert model_class.l >= 0, 'l values must zero or greater. \n'

        # Check mode type input values
        input_mtype = inputs.mode_type.lower()
        assert input_mtype == 'radial' or input_mtype == 'toroidal', \
            'Mode type does not exist. See Readme for details. \n'

        # Check intergration method
        input_int = inputs.int_method.lower()
        assert input_int == 'rk4' or input_int == 'ab2', input_int == 'euler', \
            'Integration method does not exist. See Readme for details. \n'
            

    #------------------------------------------------------------------------------------
    # OUTPUT PARAMETERS
    if hasattr(inputs,"figure_outputs"):
        for i in range(inputs.figure_outputs):
            fname_out, ax_list, L, N, ptype = extract_fig_info(inputs.figure_outputs[i])
            # Check for corresponding number n and l values                                                       
            assert len(L) == len(N), \
                'Error: Must have corresponding number of n and l values. See Readme for details. \n'
            # Check all N and L values are zero or greater and integers   
            assert all(isinstance(x, int) for x in N), 'N values must be integers. \n'
            assert N >= 0, 'N values must be zero or greater. \n'
            assert all(isinstance(x, int) for x in L), 'L values must be integers. \n'
            assert L >= 0, 'L values must be zero or greater. \n'
            # Check is plot type exists
            assert ptype == 'dispersion' or ptype == 'radial_2d_plot', \
                'Plot type does not exist. See Readme for details. \n'

                        
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
    #    Vp_pts           - Compressional velocity data point array 
    #    Vs_pts           - Shear velocity data point array
    #    rho_pts          - Density data point array
    #    R_pts            - Radial data point array
    #    r_max            - Maximum radius
    #    r_min            - Minimum radius
    # ======================================================================================= 

    f = np.loadtxt(open(fname), skiprows=0 + 1 + 2)  # Read in file (skips the header lines)

    # Extract Data Points
    Vp_pts = f[:, 2]  # Compressional wave velocity
    Vs_pts = f[:, 3]  # Shear wave velocity
    rho_pts = f[:, 1]  # Density
    R_pts = f[:, 0]  # Radius
    r_min = R_pts[-1]  # Minimum radius
    r_max = R_pts[0]  # Maximum radius

    return Vp_pts, Vs_pts, rho_pts, R_pts, r_max, r_min

                                   
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
    for r in np.arange(start_value, end_value, dr):
        sol_array.append(eval(str_input))

    return sol_array


# ----------------------------------------------------------------------------------------------------            
def input_log(cml_arguments):
    # ================================================================================================                
    # DESCRIPTION:                                                                                                    
    #    Creates or adds to a log of the command line arguments used.
    #
    # INPUT:                                                                                                          
    #    cml_arguments     - Command line arguments (i.e. sys.argv)
    # ================================================================================================

    # Get the current date
    d = today.strftime("%m-%d-%Y")

    # Creates a file "input_log.txt" containing the input arguments
    f = open("input_log.txt", "a")

    # Write command line arguments 
    f.write("Date: " + d + "\n")
    f.write("\n" + str(cml_arguments) + "\n" + "\n")

    # Close file
    f.close()

    
# ----------------------------------------------------------------------------------------------------
