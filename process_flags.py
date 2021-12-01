# Last modified by pdabney@princeton.edu, 11/28/21


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
    
    if bool(inputs.gui):
        # launch gui
        pass
    
    else:
        # For the input model
        if hasattr(inputs, "model_file"):
            # evaluate the data file
            # -extractfromfile()
            # -get_bestfit_eq()
            # -get_dr()
            # -eval_equation()
            pass
        elif hasattr(inputs,"eq_rho") and hasattr(inputs, "eq_vs"):
            # -get_dr()
            # -eval_equation
            pass
        elif hasattr(inputs,"eq_rho") and hasattr(inputs, "eq_vp"):
            # -get_dr()                                                                                           
            # -eval_equation
            pass
        else:
            # Error
            pass

        # Model parameters
        if hasattr(inputs,"nrange"):
            # -get_range()
            pass
        if hasattr(inputs,"lrange"):
            # -get_range
            pass


#------------------------------------------------------------------------------------------
# Process the command line arguments

def process_input_args(cml_arguments):

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
    parser.add_argument("-otype", "--output_type", dest="output_type", nargs=1, help="Output type")
    parser.add_argument("-oname", "--output_name", dest="output_name", help="Output filename")
    
    
    # Set class called inputs to store user input information
    inputs = user_inputs()
    
    # Pass in command line arguments and store values in input class
    parser.parse_args(str(cml_argumentcs), namespace=inputs)

    return inputs

#------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
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
def input_log(input_class):
    # Creates a file "input_args.txt" containing the input arguments

    f = open("input_log.txt", "w")

    f.close()
