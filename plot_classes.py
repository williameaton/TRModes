import numpy as np
from abc import ABC, abstractmethod

class plot_specs():
    # Class holds user-defined specifications for a plot they desire. An instance of this class is passed to
    # the plotter factory to generate the correct type of plot

    # Methods:
    def __init__(self, inname):
        self.plot_type = None
        self.in_fname = inname
        self.out_fname = None
        self.radius = None
        self.test = None


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




class gen_plot(ABC):
    # Abstract base class. Sub-classes of this are classes to generate different types of plots
    # E.g. a class called gen_dispersion

    # Attributes
    def __init__(self, plot_specs):
        self.out_fname = plot_specs.out_fname
        self.data = None        # [p x 3] matrix where p is up to the user. Each row has n, l, omega loaded from .txt file
        self.mpl_figure= None
        self.mpl_axis= None
        self.integration_required= None   # Bool - true or false depending on if integration needed



    # Methods:
    def plot(self):
        # Function is the driver for plotting - accessed by main codes. Will first prepare the plot. This incorporates
        # any loading of the data and processing (e.g. integration). Then runs the make_plot function to actually make
        # the plot
        self.__prepare_plot()
        self.__make_plot()
        self.__output_plot()


    def make_plot(self):
        # The actual plotting step - should return fig and axis to the plot function.
        pass



    def prepare_plot(self, plot_specs):
        # Should include all loading/re-arrangement of data/any integration etc
        self.load_data(plot_specs)
        if self.integration_required:
            self.integrate_mode()

    def integrate_mode(self, n, l, omega):
        # I think this may be the same for each class type that requires the ability for integration. If not, then it
        # will need to be an abstract method.
        pass

    def output_plot(self):
        # Some kind of generic function to save to a file
        pass

    @abstractmethod
    def load_data(self):
        # Should include all loading/re-arrangement of data/any integration etc
        print("Hello")
        pass