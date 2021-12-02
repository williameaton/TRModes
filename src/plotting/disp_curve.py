from NM_image import NM_image
import numpy as np

class disp_curve(NM_image):
    # ATTRIBUTES
    def __init__(self, ps_axis):
        self.specs = ps_axis                                # Data from ps_axis (N, L, and the figure are included)
        self.omega = None                                   # Eigenfrequency, loaded from a file
        self.n = None                                       # These will hold the entire n & l values
        self.l = None                                       # listed in the file
        self.ax = None                                      # The axis of the figure
        self.anim_line = None
        
    # ------------------------------------------------------------------------------------------------------------------

    # METHODS
    def _load_data(self):
        # Data file is expected to be nx3 where the columns represent l, n, omega respectively
        # Load the data and assign the columns to the proper variables
        file_data = np.loadtxt(self.specs.data_fname)
        self.specs.L = file_data[:,0]
        self.specs.N = file_data[:,1]
        self.omega = file_data[:,2]

    # ------------------------------------------------------------------------------------------------------------------

    def _produce_plot(self):

        # Set the axis and prepare the plot
        self.ax = self.specs.figure.add_subplot(self.specs.axis_loc)
        plot = self.ax.scatter(self.specs.L, self.omega, s=200/len(self.omega), c=self.specs.N, cmap='rainbow', edgecolors='none')
        self.anim_line = plot

        # Add plot details
        self._add_labels()

    # ------------------------------------------------------------------------------------------------------------------

    def _add_labels(self):
        self.ax.set_title("Dispersion Curve")
        self.ax.set_xlim(np.min(self.specs.L)-1, np.max(self.specs.L)+1)
        self.ax.set_xlabel("Angular degree (l)")
        self.ax.set_ylabel("Frequency [mHz]")

    # ------------------------------------------------------------------------------------------------------------------

    # Have to include these two
    def init_anim_data(self):
        pass

    # ------------------------------------------------------------------------------------------------------------------

    def update_anim_data(self, iteration):
        pass

    # ------------------------------------------------------------------------------------------------------------------
