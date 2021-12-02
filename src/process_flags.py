# Last modified by pdabney@princeton.edu, 11/30/21


from Model import *
import sys, getopt, argparse



class user_inputs:
    # Empty class to store input values
    pass



def process_flags(inputs):
    # =====================================================================================
    # DESCRIPTION:
    #   Processes the flags. If called specified by the user, will launch the GUI. Otherwise,
    #   will prepare inputs for the computations and/or animations.
    #
    # INPUT:
    #    inputs         - Class containing information about the command line arguments
    # =====================================================================================

    # Initialize classes
    model_class = Model()
    
    # Process the flags
    if bool(inputs.gui):
        # launch gui
        pass
    
    else:
        # For the input model
        if hasattr(inputs, "model_file"):
            # Evaluate the data file
            Vp_pts, Vs_pts, rho_pts, R_pts, model_class.r_max, model_class.r_min = extractfromfile(inputs.model_file)

            # Compute dr
            model_class.dr = get_dr(model_class.r_max, model_class.r_min, inputs.Nr)

            # Obtain equations for rho, Vs, Vp in order to resample
            rho_eq = get_bestfit_eq(R_pts, rho_pts)
            Vs_eq = get_bestfit_eq(R_pts, Vs_pts)
            Vp_eq = get_bestfit_eq(R_pts, Vp_pts)

            # Evaluate the equations
            model_class.rho = eval_equation(rho_eq, model_class.r_min, model_class.r_max, model_class.dr)
            model_class.Vs = eval_equation(Vs_eq, model_class.r_min, model_class.r_max, model_class.dr)
            model_class.Vp = eval_equation(Vp_eq, model_class.r_min, model_class.r_max, model_class.dr)

        else:
            # Ensure a density equation has been inputed
            assert hasattr(inputs,'eq_rho'), 'Requires density equation'
                                   
            # Compute dr                                                                                          
            model_class.dr = get_dr(inputs.r_max, inputs.r_min, inputs.Nr)
            # Obtain density
            model_class.rho = eval_equation(inputs.rho_eq, inputs.r_min, inputs.r_max, model_class.dr)            

            if inputs.mtype == "Toroidal":
                # Check the user has inputted a shear velocity equation
                assert hasattr(inputs,'eq_vs'), 'Requires shear velocity equation'                        

                # Obtain shear velocity
                model_class.Vs = eval_equation(inputs.eq_vs, inputs.r_min, inputs.r_max, model_class.dr)
                                   
            elif inputs.mtype == "Radial":
      	        # Check the user has inputted a compressional velocity equation                                                  
                assert hasattr(inputs,'eq_vp'), 'Requires compressional velocity equation'

            	# Obtain compressional velocity
                model_class.Vp = eval_equation(inputs.eq_vp, inputs.r_min, inputs.r_max, model_class.dr)

            
        # Model parameters
        if hasattr(inputs,"nrange"):
	    # Convert string to an array                                                                          
	    n_values = str2array(inputs.nrange)
            # Obtain n values
            model_class.n = get_range(n_values[1], n_values[0])
        else:
            # Convert string to an array                                                       
            model_class.n = str2array(inputs.n)

        # Check the n values
        assert all(isinstance(x, int) for x in model_class.n), 'n values must be integers'
                                   
        if hasattr(inputs,"lrange"):
            # Convert string to an array
	    l_values = str2array(inputs.lrange)
	    # Obtain l values                                                                                     
            model_class.l = get_range(l_values[1], l_values[0])            
         else:
	    # Convert string to an array                                                                          
            model_class.l = str2array(inputs.l)

        # Check l values                           
        assert all(isinstance(x, int) for x in model_class.l), 'l values must be integers'
        assert model_class.l < 0, 'l values mus zero or greater'


                                   
    return model_class
                                   
#------------------------------------------------------------------------------------------                       
# Supplementry Functions                                   
#------------------------------------------------------------------------------------------
def process_input_args(cml_arguments):
    # Process the command line arguments
                                   
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
    parser.add_argument("-l", "--l_values", dest="n", nargs=1, help="Angular degree value(s)")
    parser.add_argument("-lrange", "--lrange", dest="lrange", nargs=1, help="Range of angular degree values")
    parser.add_argument("-int", "--integrator", dest="int_method", nargs=1, help="Integration method")
    parser.add_argument("-T", "--Toroidal",action="store_const", dest="mytpe", const="Toroidal")
    parser.add_argument("-R", "--Radial", action="store_const", dest="mtype", const="Radial")
    #parser.add_argument("-S","--Spheriodal",action="store_const",dest="mtype",const="Spheriodal")

    # Flags related to output
    parser.add_argument("-fig", "--figure", dest="output_type", nargs=1, help="Figure output details")
    
    # Set class called inputs to store user input information
    inputs = user_inputs()
    
    # Pass in command line arguments and store values in input class
    parser.parse_args(str(cml_arguments), namespace=inputs)

    return inputs

#------------------------------------------------------------------------------------------
def str2array(str_in):
    # Convert n string inputs to integers                                                                 
    _list = str_in.split(",")
    array_out = [eval(x) for x in _list]

    return array_out


#------------------------------------------------------------------------------------------                       
def extractfromfile(fname):
    # Extracts compressional and shear velocity, density, and radial data points from a model text
    # file (e.g. PREM). Assumes the model file is isotropic.
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
def get_dr(r_max, r_min, Nr):
    # Computes the radial step
    dr = (r_max - r_min) / Nr
                                   
    return dr

                                   
# ----------------------------------------------------------------------------------------------------
def get_bestfit_eq(R, data):
    # Computes a fourth order polynomial best fit equation
    deg = 4  # Polynomial degree

    # Determine best fit curve to the data
    coeff = np.polyfit(R, data, deg)

    # Returns the best fit equation as string
    eq = "(r ** 4) * %d + (r ** 3) * %d + (r ** 2) * %d + r * %d + %d" % (coeff[0], coeff[1], coeff[2],
                                                                          coeff[3], coeff[4])
    return eq


# ----------------------------------------------------------------------------------------------------
def eval_equation(str_input, start_value, end_value, dr):
    # Evaluates a single variable equation at discrete points and produces an array containing the
    # solutions
    sol_array = []                                   # Initialize array

    # Evaluate equation at each dr
    for x in np.arange(start_value, end_value, dr):
        sol_array += [eval(str_input)]

    return sol_array


# ----------------------------------------------------------------------------------------------------
def get_range(v_max, v_min):
    # Obtains the consecutive range of integer values between two values  
    v_range = range(v_min, v_max)

    return v_range                                   

                                   
# ----------------------------------------------------------------------------------------------------            
def input_log(input_class):
    # Creates a file "input_log.txt" containing the input arguments
    f = open("input_log.txt", "w")

    f.close()
