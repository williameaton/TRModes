import matplotlib.pyplot as plt
import numpy as np
from plot_classes import gen_plot, plot_specs


class radial_plot_2D(gen_plot):
    # Attributes
    def __init__(self, plot_specs):
        self.out_fname = plot_specs.out_fname
        self.data_fname = plot_specs.in_fname
        self.data = None
        self.N= None
        self.L= None
        self.omega= None
        self.mpl_figure= None
        self.mpl_axis= None
        self.integration_required = False  # Bool - true or false depending on if integration needed



    # Methods:
    def plot(self, plot_specs):
        # Function is the driver for plotting - accessed by main codes. Will first prepare the plot. This incorporates
        # any loading of the data and processing (e.g. integration). Then runs the make_plot function to actually make
        # the plot
        super().prepare_plot(plot_specs)
        self.make_plot()
        self.output_plot()

    def make_plot(self):
        # The actual plotting step - should return fig and axis to the plot function.
        pass

    def load_data(self, plot_specs):
        # Expected file format is single column of data - first 3 lines are N, L, Omega. Next lines are displacement/
        # sensitivity at (increasing/decreasing) depth
        file_data = np.loadtxt(self.data_fname)
        self.N = file_data[0]
        self.L = file_data[1]
        self.omega = file_data[2]
        self.data = file_data[3:]


    def integrate_mode(self, n, l, omega):
        # I think this may be the same for each class type that requires the ability for integration. If not, then it
        # will need to be an abstract method.
        pass

    def output_plot(self):
        # Some kind of generic function to save to a file
        pass


if __name__ == "__main__":
    # create dummy plot_specs object
    specs = plot_specs(inname="example_2D_data.txt")
    # Create gen_plot object
    r2D = radial_plot_2D(specs)
    r2D.plot(specs)
