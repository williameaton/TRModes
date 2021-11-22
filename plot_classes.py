import numpy as np

class plot_spec():
    # Class holds user-defined specifications for a plot they desire. An instance of this class is passed to
    # the plotter factory to generate the correct type of plot

    # FUNCTIONS:
    def __init__(self, specs):
        self.plot_type
        self.in_fname
        self.out_fname
        self.radius
        self.test


    def _assign_plottype(self, plot_str):
        # ==============================================================================================================
        # DESCRIPTION: Checks inputted string is an acceptable string
        # INPUTS:   plot_str [str]    - string holding desired plot_type
        # OUTPUTS:  plot_str [str]    - string holding desired plot_type - now checked.
        # ==============================================================================================================

        # Define possible plot_types
        plottype = {
            "dispersion" : True,
            "2D_radial"  : True,
            "3D_animated": True,
        }

        # Check string matches acceptable plot type and return
        if plottype.get(plot_str, False):
            return plot_str
        else:
            raise ValueError(f"Plot type {plot_str} doesn't exist. Must be 'dispersion', '2D_radial' or '3D_animated")


