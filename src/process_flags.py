# Last modified by pdabney@princeton.edu, 12/04/21

#--------------------------------------------------------------------------------------------
# Imports
#--------------------------------------------------------------------------------------------


from Model.py import *
from ps_figure.py import *
from ps_axis.py import *
import sys, getopt, argparse
from datetime import date
from os.path import exists as file_exists

#--------------------------------------------------------------------------------------------
# Define Empty Class
#--------------------------------------------------------------------------------------------

class user_inputs:
    # Empty class to store input values
    pass


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

    # Initialize classes
    model_class = Model()
    axis_class = ps_axis()
    figure_class = ps_figure()
    
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
        assert input_mtype == 'radial' or input_mtype == 'spheriodal' or input_mtype == 'toroidal', \
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
def process_input_args(cml_arguments):
    # =======================================================================================                    
    # DESCRIPTION:                                                                                                    
    #   Process the command line arguments and store values in a class
    #                                                                                                                 
    # INPUT:                                                                                                          
    #    cml_arguments         - Command line arguments (i.e. sys.argv)
    # OUTPUt:
    #    inputs                - Class containing user inputs from the command line
    # =======================================================================================
    
    # Create object that will hold information needed to parse command line
    parser = argparse.ArgumentParser()
    
    # Include all command line flags
    parser.add_argument("-gui", "--gui_launch", action="store_true", dest="gui", default=False, help="Launch GUI")

    parser.add_argument("-eqr", "--equation_rho", dest="eq_rho", nargs=1, help="Equation for density")
    parser.add_argument("-eqs", "--equation_vs", dest="eq_vs", nargs=1, help="Equation for shear velocity")
    parser.add_argument("-eqp", "--equation_vp", dest="eq_vp", nargs=1, help="Equation for compressional velocity")
    parser.add_argument("-mf", "--model_file", dest="model_file", nargs=1, help="Model file")
    parser.add_argument("-rmin", "--radius_minimum", dest="r_min", nargs=1, help="Minimum radius")
    parser.add_argument("-rmax", "--radius_maximum", dest="r_max", nargs=1, help="Maximum radius")
    parser.add_argument("-Nr", "--number_rsteps", dest="Nr", nargs=1, help="Number of radial steps")
    parser.add_argument("-n", "--n_values", dest="n", nargs=1, help="Radial order value(s)")
    parser.add_argument("-nrange", "--nrange", dest="nrange", nargs=1, help="Range of radial order values")
    parser.add_argument("-l", "--l_values", dest="l", nargs=1, help="Angular degree value(s)")
    parser.add_argument("-lrange", "--lrange", dest="lrange", nargs=1, help="Range of angular degree values")
    parser.add_argument("-int", "--integrator", dest="int_method", nargs=1, help="Integration method")
    parser.add_argument("-mtype", "--mode_type", dest="mode_type", nargs=1, help="Type of mode: toroidal, spheriodal or radial")


    # Flags related to output
    parser.add_argument("-fig", "--figure", dest="figure_output", nargs="*", help="Figure output details")
    parser.add_argument("-ofile", "--output_file", dest="output_file", nargs=1, help="File containing the computation outputs")
                        
    # Set class called inputs to store user input information
    inputs = user_inputs()
    
    # Pass in command line arguments and store values in input class
    parser.parse_args(str(cml_arguments), namespace=inputs)

    return inputs



#------------------------------------------------------------------------------------------                    
def extract_fig_info(str_in):
    # =======================================================================================                         
    # DESCRIPTION:                                                                                                    
    #   Processes the users input regarding the output figure(s).
    #                                                                                                                 
    # INPUT:                                                                                                          
    #    str_in         - String of the figure output information. (e.g. "figure1: 121 2D_radial
    #                     L4 N2; 122 dispersion L1,2,3 N[1][1,2][1,2,3]")
    # OUTPUT:
    #    fname_out      - File name of figure(s). Variable is set to None if no name is specified.
    #    ax_list        - List of figure axes. (e.g. ['121','122'])
    #    L              - Angular order value(s). (format: 'L4' or 'L1,2,3,4')
    #    N              - Radial order value(s). (format: 'N3' or 'N[1][3,4][1,2,3,4]')
    #    ptype          - Plot type: 'radial','toroidal','spheriodal'
    # =======================================================================================  

    if (str_in.find(":") != 1):
        # Separate the output file name and store
        fname_sep = str_in.split(":")
        fname_out = fname_sep[0]
        start = 1
    else:
        fname_out = None
        start = 0

    # Run through the remaining input
    ax_list=[]
    ptype=[]
    L=[]
    N=[]
    for i in range(start, len(fname_sep)):
        fig_sep = fname_sep[i].split(";")
        for k in range(0,len(fig_sep)):
            ax_sep = fig_sep[k].split(" ")
            # Removes empty strings
            newlist = [j for j in ax_sep if j]

            # Store values
            ax_list.append(ax_sep[0])
            ptype.append(ax_sep[1].lower())
            # Remove N and L identifier
            l = ax_sep[2].replace('L','')
            n = ax_sep[3].replace('N','')
            
            if len(l) > 1:
                # If there is more than one value
                l_values = str2array(l,',')
            else:
                l_values = float(l)

            if len(n) > 1:
                # If there is more than a single value
                n_rep = n.replace('[','').replace(']',' ').split(' ')
                # Removes empty strings
                new_n = [j for j in n_rep if j]
                n_values = []
                for i in range(len(new_n)):
                    # Appends an empty sublist inside the list that can be filled later
                    n_values.append([])
                    n_list = str2array(new_n[i],',')
                    for k in range(len(n_list)):
                        # Fill list with sublists
                        n_values[i].append(n_list[k])
            else:
                n_values = float(n)

            # Store n and l values
            L.append(l_values)
            N.append(n_values)
 
    return fname_out, ax_list, L, N, ptype


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
    r_max = R_pts[-1]  # Maximum radius
    r_min = R_pts[0]  # Minimum radius

    return Vp_pts, Vs_pts, rho_pts, R_pts, r_max, r_min

                                   
# ----------------------------------------------------------------------------------------------------
def get_bestfit_eq(R, data):
    # ================================================================================================               
    # DESCRIPTION:                                                                                                    
    #    Computes a fourth order polynomial best fit equation and returns it as a string.
    #
    # INPUT:                                                                                                          
    #    R               - Array of radial data
    #    data            - Array of radially dependent data
    # OUTPUT:                                                                                                         
    #    eq              - String of best fit equation
    # ================================================================================================  
    
    deg = 4  # Polynomial degree

    # Determine best fit curve to the data
    coeff = np.polyfit(R, data, deg)

    # Returns the best fit equation as string
    eq = "(r ** 4) * %d + (r ** 3) * %d + (r ** 2) * %d + r * %d + %d" % (coeff[0], coeff[1], coeff[2], \
                                                                          coeff[3], coeff[4])
    return eq


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
    for x in np.arange(start_value, end_value, dr):
        sol_array += [eval(str_input)]

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
