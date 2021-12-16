from NM_image import NM_image
import numpy as np

class radial_2D_surface(NM_image):
    """A concrete subclass of NM_image that produces surface motion 2D plots for an individual mode. """
    
    # Attributes
    def __init__(self, ps_axis):
        """
        :param ps_axis: ps_axis object that holds specifications for the details of the plot
        :type ps_axis: ps_axis object
        """

        self.specs = ps_axis                                # All the data from the ps_axis including the figure
        self.r_circle = None                                # Circle's radius
        self.anim_line = None                               # Storing the 2D line object for animation
        self.ax = None                                      # The axis of the figure
        self.x = None                                       # Related to the circle
        self.y = None                                       # Related to the circle
        self.l_len = None                                   # Length vertical segments at x=0
        self.y_pos = np.zeros(self.specs.N-1)               # To hold the y position of horizontal lines

    # ------------------------------------------------------------------------------------------------------------------

    # METHODS
    def _load_data(self):
        """Function defined in ABC but not used for this type of plot."""
        pass

    # ------------------------------------------------------------------------------------------------------------------

    def _produce_plot(self):
        """First-order function that produces the plot on the relevant Matplotlib axis."""
        
        # The axis
        self.ax = self.specs.figure.add_subplot(self.specs.axis_loc)
        # Plot the circle
        self._plot_circle()
        # Plot the horizontal lines
        self._plot_hlines()

        x_data = np.zeros(self.specs.N)
        y_min = np.zeros(self.specs.N)
        y_max = np.zeros(self.specs.N)

        plot, = self.ax.vlines(x=x_data, ymin=y_min, ymax=y_max, color='red', linewidth=2.5)
        self.anim_line = plot 

    # ------------------------------------------------------------------------------------------------------------------

    def _plot_circle(self):
        self.r_circle = 30
        # 360 degrees to plot full circle
        theta = 360
        # t is angle here changing the value of 360
        t = np.linspace(0, theta, 360)

        # Circumference-defining points
        self.x = self.r_circle*np.sin(np.radians(t))
        self.y = self.r_circle*np.cos(np.radians(t)) + self.r_circle    # Radius added to make the minimum point = 0
        # Plot the circle now
        self.ax.plot(self.x, self.y, color='black', linewidth=3)

    # ------------------------------------------------------------------------------------------------------------------

    def _plot_hlines(self):
        # Know at which positions we should put the horizontal lines
        self.l_len = 2*self.r_circle/self.specs.N
        y_start = 0
        # Know their extension and plot them
        for i in range(self.specs.N-1):
            self.y_pos[i] = y_start + self.l_len
            y_start = self.y_pos[i]
            ind = np.where(self.y<=self.y_pos[i])
            ind = ind[0][0]
            if self.x[ind]<0:
                self.ax.hlines(y=self.y_pos[i], xmin=self.x[ind], xmax=-self.x[ind], color='black', linewidth=2.5)
            else:
                self.ax.hlines(y=self.y_pos[i], xmin=-self.x[ind], xmax=self.x[ind], color='black', linewidth=2.5)

        self.y_pos = np.append(self.y_pos, 2*self.r_circle)

    # ------------------------------------------------------------------------------------------------------------------

    def init_anim_data(self):
        """Initialises data values for first frame of an animation. """
        y_start = 0
        new_x = np.zeros(self.specs.N)
        new_min = np.zeros(self.specs.N)
        new_max = np.zeros(self.specs.N)

        for i in range(self.specs.N):
            new_min[i] = y_start+0.5
            new_max[i] = self.y_pos[i]-0.5
            y_start = self.y_pos[i]
        
        return new_x, new_min, new_max

    # ------------------------------------------------------------------------------------------------------------------

    def update_anim_data(self, iteration):
        """Function is used to update MPL artists (e.g. a 2DLine object) as part of animations for given iteration value
        see _gen_animations() in ps_figure.py

        :type iteration: int
        :param iteration: Iteration step for animations
        """