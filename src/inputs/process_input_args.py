import argparse

def process_input_args():

    """
    Takes the users' inputs and returns an object that stores all the command line arguments.
    
    """
    
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
    parser.add_argument("-mtype", "--mode_type", dest="mode_type", nargs=1, help="Type of mode: toroidal or radial")


    # Flags related to output
    parser.add_argument("-fig", "--figure", dest="figure_output", nargs="*", help="Figure output details")
    parser.add_argument("-ofile", "--output_file", dest="output_file", nargs=1, help="File containing the computation outputs")
    
    return(parser.parse_args())

