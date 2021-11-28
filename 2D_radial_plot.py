import matplotlib.pyplot as plt
import numpy as np
from plot_classes import gen_plot, plot_specs
import matplotlib.animation as animation


class radial_plot_2D(gen_plot):
    # Attributes
    def __init__(self, plot_specs):
        self.out_fname = plot_specs.out_fname
        self.data_fname = plot_specs.in_fname
        self.data = None
        self.z = None
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
        W = self.data*0.5
        self.z = np.linspace(0, 1, len(W))

        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        dispersion, = ax.plot(W, self.z, linewidth=2)

        # Plot zero axis:
        ax.plot([0, 0], [0, np.amax(self.z)], 'k-', linewidth=1, alpha=0.7)

        def init():  # only required for blitting to give a clean slate.
            i = 0
            dispersion.set_xdata(W * np.cos(i * 2 * np.pi / 100))
            return dispersion,

        def animate(i):
            dispersion.set_xdata(W * np.cos(i * 2 * np.pi / 100))  # update the data.
            return dispersion,

        ani = animation.FuncAnimation(
            fig, animate, init_func=init, interval=20, blit=False, save_count=50)

        # Format the figure:
        ax.set_theta_zero_location("N")
        W_max = np.amax(np.abs(W))
        ax.set_xlim([-W_max, W_max])
        ax.set_ylabel("Relative Radius")
        ax.set_xticklabels([])
        ax.set_ylim(0, np.amax(self.z))
        ax.grid(False)

        # Detect and add zero-crossings:
        zero_crossings = np.where(np.diff(np.sign(W)))[
            0]  ## BY THE WAY THIS SHOULD BE EQUAL TO N - write a test - how will this work for crossing at 0 or R?

        # Get z of zerocrossing:
        rad_0x = self.z[zero_crossings]

        theta = np.linspace(-W_max, W_max, 200)  # 200 is arbitrary
        for i in range(len(rad_0x)):
            line_rad = theta * 0 + rad_0x[i]
            ax.plot(theta, line_rad, ":", color='r', linewidth=1)

        ax.set_title(r"Toroidal mode ${}_{8}T_{50}$")
        plt.show()

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
