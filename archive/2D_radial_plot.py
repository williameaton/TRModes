import matplotlib.pyplot as plt
import numpy as np
from plot_classes import gen_plot
from plot_specs import plot_specs
import matplotlib.animation as animation


class radial_plot_2D(gen_plot):
    # Attributes
    def __init__(self, ps):
        self.out_fname            = ps.out_fname
        self.data_fname           = ps.in_fname
        self.data                 = None
        self.z                    = None
        self.N                    = None
        self.L                    = None
        self.radius               = ps.metadata.radius
        self.omega                = None
        self.mpl_figure           = ps.figure
        self.mpl_axis             = self._make_polar_axis(ps)
        self.animation            = None
        self.integration_required = False  # Bool - true or false depending on if integration needed



    # METHODS:
    def _make_plot(self):
        W = self.data*0.5
        W_max = np.amax(np.abs(W))

        self.z = np.linspace(0, 1, len(W))*self.radius

        plot, = self.mpl_axis.plot(W, self.z, linewidth=2)

        # Plot zero axis:
        self.mpl_axis.plot([0, 0], [0, np.amax(self.z)], 'k-', linewidth=1, alpha=0.7)

        def init():  # only required for blitting to give a clean slate.
            i = 0
            plot.set_xdata(W * np.cos(i * 2 * np.pi / 100))
            return plot,

        def animate(i):
            plot.set_xdata(W * np.cos(i * 2 * np.pi / 100))  # update the data.
            return plot,

        self.animation = animation.FuncAnimation(self.mpl_figure, animate, init_func=init, interval=20, blit=False, save_count=200)

        self._format_figure_metadata(W_max)

        # Detect and add zero-crossings:
        zero_crossings = np.where(np.diff(np.sign(W)))[
            0]  ## BY THE WAY THIS SHOULD BE EQUAL TO N - write a test - how will this work for crossing at 0 or R?

        # Get z of zerocrossing:
        rad_0x = self.z[zero_crossings]

        theta = np.linspace(-W_max, W_max, 200)  # 200 is arbitrary
        for i in range(len(rad_0x)):
            line_rad = theta * 0 + rad_0x[i]
            self.mpl_axis.plot(theta, line_rad, ":", color='r', linewidth=1)

        self.mpl_axis.set_title(rf"Toroidal mode $ _{str(int(self.N))}T_{ str(int(self.L))}$")

    # ------------------------------------------------------------------------------------------------------------------

    def _load_radial_data(self, ps):
        # Expected file format is single column of data - first 3 lines are N, L, Omega. Next lines are displacement/
        # sensitivity at (increasing/decreasing) depth
        file_data = np.loadtxt(self.data_fname)
        self.N = file_data[0]
        self.L = file_data[1]
        self.omega = file_data[2]
        self.data = file_data[3:]

    # ------------------------------------------------------------------------------------------------------------------

    def _integrate_mode(self, n, l, omega):
        # I think this may be the same for each class type that requires the ability for integration. If not, then it
        # will need to be an abstract method.
        pass

    # ------------------------------------------------------------------------------------------------------------------

    def _output_plot(self):
        # Write output to mp4 and gif
        writer = animation.FFMpegWriter(fps=60)
        suffix = [".mp4", ".gif"]

        for i in range(len(suffix)):
            out_str = self.out_fname+suffix[i]
            print(f"Writing to {out_str}...")
            self.animation.save(out_str, writer=writer)

    # ------------------------------------------------------------------------------------------------------------------

    def _make_polar_axis(self, specs):
        return self.mpl_figure.add_subplot(specs.subaxis_pos, projection='polar')

    # ------------------------------------------------------------------------------------------------------------------

    def _format_figure_metadata(self, W_max):
        # ==============================================================================================================
        # DESCRIPTION:
        # INPUTS:
        # OUTPUTS:
        # ==============================================================================================================

        # Format the figure metadata e.g. titles etc:
        self.mpl_axis.set_theta_zero_location("N")
        self.mpl_axis.set_xlim([-W_max, W_max])
        self.mpl_axis.set_ylabel("Radius")
        self.mpl_axis.set_xticklabels([])
        self.mpl_axis.set_ylim(0, np.amax(self.z))
        self.mpl_axis.grid(False)

    # ------------------------------------------------------------------------------------------------------------------









if __name__ == "__main__":
    # create dummy plot_specs object
    fig = plt.figure()
    specs = plot_specs(type        = "2D_radial",
                       inname      = "example_2D_data.txt",
                       outname     = "test",
                       radius      = 6371,
                       fig         = fig,
                       subaxis_pos = 111,
                       N           = 50,
                       L           = 5)

    # Create gen_plot object
    r2D = radial_plot_2D(specs)
    r2D.plot(specs)
