import numpy as np
from abc import ABC, abstractmethod

class plot_specs():
    # Class holds user-defined specifications for a plot they desire. An instance of this class is passed to
    # the plotter factory to generate the correct type of plot

    # Methods:
    def __init__(self, type, inname, outname, radius, fig, subaxis_pos=111):
        self.plot_type = self._assign_plottype(type)
        self.in_fname = inname
        self.out_fname = outname
        self.radius = radius
        self.figure = fig
        self.subaxis_pos = subaxis_pos


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


    # Methods:
    def plot(self):
        # Function is the driver for plotting - accessed by main codes. Will first prepare the plot. This incorporates
        # any loading of the data and processing (e.g. integration). Then runs the make_plot function to actually make
        # the plot
        self.__prepare_plot()
        self.__make_plot()
        self.__output_plot()


    def _make_plot(self):
        # The actual plotting step - should return fig and axis to the plot function.
        pass



    def _prepare_plot(self, plot_specs):
        # Should include all loading/re-arrangement of data/any integration etc
        self._load_radial_data(plot_specs)
        if self.integration_required:
            self.integrate_mode()

    def _integrate_mode(self, n, l, omega):
        # I think this may be the same for each class type that requires the ability for integration. If not, then it
        # will need to be an abstract method.
        pass

    def _output_plot(self):
        # Some kind of generic function to save to a file
        pass

    @abstractmethod
    def _load_radial_data(self):
        # Should include all loading/re-arrangement of data/any integration etc
        print("Hello")
        pass

