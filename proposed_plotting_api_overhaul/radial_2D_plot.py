from NM_image import NM_image
import numpy as np

class radial_2D_plot(NM_image):
    # Example of a concrete subclass of NM_image

    # Attributes
    def __init__(self, ps_axis):
        self.specs = ps_axis                                # All the data from the ps_axis including the figure
        self.mpl_axis = self._make_polar_axis(ps_axis)      # The MPL axes for this NM_image
        self.omega = None                                   # Eigenfrequency - loaded from data
        self.anim_line = None                               # Holds some MPL artist (e.g. 2DLine) for animation
        self.data = None                                    # Data for plotting loaded from some file

    # ------------------------------------------------------------------------------------------------------------------

    # METHODS:
    def _produce_plot(self):
        W = self.data                                           # Displacement/sensitivity
        W_max = np.amax(np.abs(W))                              # Max W

        self.z = np.linspace(0, 1, len(W)) * self.specs.radius  # Create Z data for plotting against

        plot, = self.mpl_axis.plot(W, self.z, linewidth=2)      # Plot the displacement vs depth
        self.anim_line = plot                                   # Storing the 2D line object for animation

        self._add_figure_details(W, W_max)                      # Adding decoration to figure:
    # ------------------------------------------------------------------------------------------------------------------


    def init_anim_data(self):
        new_xdata = self.data * 0                               # Initially for animation, displacement = 0
        new_ydata = self.z                                      # Depth array unaffected

        return new_xdata, new_ydata
    # ------------------------------------------------------------------------------------------------------------------


    def update_anim_data(self, iteration):
        new_xdata = (self.data * np.cos(iteration * 2 * np.pi / 100))  # Rotation of displacement curve around 0 line
        new_ydata = self.z                                             # Depth array unaffected

        return new_xdata, new_ydata
    # ------------------------------------------------------------------------------------------------------------------

    def _load_data(self):
        # Expected file format is single column of data - first 3 lines are N, L, Omega. Next lines are displacement/
        # sensitivity at (increasing/decreasing) depth
        file_data = np.loadtxt(self.specs.data_fname)
        self.specs.N = file_data[0]
        self.specs.L = file_data[1]
        self.omega = file_data[2]
        self.data = file_data[3:]*0.5 # Multiplied by 0.5 just so magnitude stays inside polar axis

    # ------------------------------------------------------------------------------------------------------------------

    def _integrate_mode(self, n, l, omega):
        # Unsure whether this will just be defined in NM_image or whether it needs to be abstact in NM_image...TBC
        pass

    # ------------------------------------------------------------------------------------------------------------------

    def _make_polar_axis(self, specs):
        # Generate and add an MPL axes to the figure - type required is polar
        return self.specs.figure.add_subplot(specs.axis_loc, projection='polar')

    # ------------------------------------------------------------------------------------------------------------------


    def _add_figure_details(self, W, W_max):
        # Adds all the bells and whistles to the figure like zerocrossing lines etc
        self._format_figure_metadata(W_max)

        # Adding grid lines at zero crossings:
        self.mpl_axis.plot([0, 0], [0, np.amax(self.z)], 'k-', linewidth=1, alpha=0.7)

        # Detect and add zero-crossings:
        zero_crossings = np.where(np.diff(np.sign(W)))[0]
        # Get z of zerocrossing:
        rad_0x = self.z[zero_crossings]

        theta = np.linspace(-W_max, W_max, 200)  # 200 is arbitrary
        for i in range(len(rad_0x)):
            line_rad = theta * 0 + rad_0x[i]
            self.mpl_axis.plot(theta, line_rad, ":", color='r', linewidth=1)





    def _format_figure_metadata(self, W_max):
        # ==============================================================================================================
        # DESCRIPTION: Updates axes artists like the title/axes limits etc
        # INPUTS: W_max [float] - max. displacement data value for determining x_lims of plot
        # OUTPUTS: N/A
        # ==============================================================================================================

        # Format the figure metadata e.g. titles etc:
        self.mpl_axis.set_theta_zero_location("N")
        self.mpl_axis.set_xlim([-W_max, W_max])
        self.mpl_axis.set_ylabel("Radius")
        self.mpl_axis.set_xticklabels([])
        self.mpl_axis.set_ylim(0, np.amax(self.z))
        self.mpl_axis.grid(False)
        self.mpl_axis.set_title(rf"Toroidal mode $ _{str(int(self.specs.N))}T_{str(int(self.specs.L))}$")


    # ------------------------------------------------------------------------------------------------------------------