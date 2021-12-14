from plotting.NM_image import NM_image
import numpy as np

class radial_2D_plot(NM_image):
    """A concrete subclass of NM_image that produces displacement vs depth 2D plots for an individual mode. """

    # Attributes
    def __init__(self, ps_axis):
        """
        :param ps_axis: ps_axis object that holds specifications for the details of the plot
        :type ps_axis: ps_axis object
        """

        self.specs = ps_axis                                # All the data from the ps_axis including the figure
        self.mpl_axis = self._make_polar_axis(ps_axis)      # The MPL axes for this NM_image
        self.omega = None                                   # Eigenfrequency - loaded from data
        self.anim_line = None                               # Holds some MPL artist (e.g. 2DLine) for animation
        self.r_data = None                                  # Data for plotting loaded from some file
        self.displacement = None                            # Data for plotting loaded from some file

    # ------------------------------------------------------------------------------------------------------------------

    # METHODS:
    def _produce_plot(self):
        """First-order function that produces the plot on the relevant Matplotlib axis."""
        W_max = np.amax(np.abs(self.displacement))              # Max displacement

        plot, = self.mpl_axis.plot(self.displacement, self.r_data, linewidth=2)      # Plot the displacement vs depth
        self.anim_line = plot # Storing the 2D line object for animation

        self._add_figure_details(self.displacement, W_max)                      # Adding decoration to figure:
    # ------------------------------------------------------------------------------------------------------------------


    def init_anim_data(self):
        """Initialises data values for first frame of an animation. """
        new_xdata = self.displacement * 0                               # Initially for animation, displacement = 0
        new_ydata = self.r_data                                      # Depth array unaffected

        return new_xdata, new_ydata
    # ------------------------------------------------------------------------------------------------------------------


    def update_anim_data(self, iteration):
        """Function is used to update MPL artists (e.g. a 2DLine object) as part of animations for given iteration value
           see _gen_animations() in ps_figure.py

           :type iteration: int
           :param iteration: Iteration step for animations
        """
        new_xdata = (self.displacement * np.cos(iteration * 2 * np.pi / 100))  # Rotation of displacement curve around 0 line
        new_ydata = self.r_data                                             # Depth array unaffected

        return new_xdata, new_ydata
    # ------------------------------------------------------------------------------------------------------------------

    def _load_data(self):
        """
        Module called in _prepare_plot(). Expected file format is single column of data with first 1 line with L, N,
        Omega. Next lines are displacement/sensitivity at (increasing/decreasing) depth
        """

        file_data = np.loadtxt(f"./output/Wr_l{self.specs.L[0]}_n{self.specs.N[0]}.txt", skiprows=1)
        self.displacement = file_data[:,0]*0.5 # Multiplied by 0.5 just so magnitude stays inside polar axis
        self.r_data = file_data[:,1]

    # ------------------------------------------------------------------------------------------------------------------

    def _integrate_mode(self, n, l, omega):
        """Not sure if we will use this function. TBC."""
        pass

    # ------------------------------------------------------------------------------------------------------------------

    def _make_polar_axis(self, specs):
        """Generates and adds a matplotlib polar axes to the figure.

        :type specs: ps_axis object
        :param specs: Specifications for the plot type to know which location to generate the axis on matplotlib figure
        """
        return self.specs.figure.add_subplot(specs.axis_loc, projection='polar')

    # ------------------------------------------------------------------------------------------------------------------


    def _add_figure_details(self, W, W_max):
        """
        Adds all the bells and whistles to the figure like zerocrossing lines etc

        :param W: Displacement values as a function of radius
        :type W: 1D Numpy array

        :param W_max: Maximum magnitude of displacement in array (must be positive).
        :type W_max: float
        """
        self._format_figure_metadata(W_max)

        # Adding grid lines at zero crossings:
        self.mpl_axis.plot([0, 0], [0, np.amax(self.r_data)], 'k-', linewidth=1, alpha=0.7)

        # Detect and add zero-crossings:
        zero_crossings = np.where(np.diff(np.sign(W)))[0]
        # Get z of zerocrossing:
        rad_0x = self.r_data[zero_crossings]

        theta = np.linspace(-W_max, W_max, 200)  # 200 is arbitrary
        for i in range(len(rad_0x)):
            line_rad = theta * 0 + rad_0x[i]
            self.mpl_axis.plot(theta, line_rad, ":", color='r', linewidth=1)





    def _format_figure_metadata(self, W_max):
        """
        Updates axes artists like the title/axes limits etc

        :param W_max: Maximum magnitude of displacement in array (must be positive).
        :type  W_max: float
        """

        # Format the figure metadata e.g. titles etc:
        self.mpl_axis.set_theta_zero_location("N")
        self.mpl_axis.set_xlim([-W_max, W_max])
        self.mpl_axis.set_ylabel("Radius")
        self.mpl_axis.set_xticklabels([])
        self.mpl_axis.set_ylim(0, np.amax(self.r_data))
        self.mpl_axis.grid(False)
        self.mpl_axis.set_title(rf"Toroidal mode $ _{str(int(self.specs.N[0]))}T_{str(int(self.specs.L[0]))}$")


    # ------------------------------------------------------------------------------------------------------------------
