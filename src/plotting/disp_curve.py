from NM_image import NM_image
import numpy as np

class disp_curve(NM_image):
    # ATTRIBUTES
    def __init__(self, ps_axis):
        self.specs = ps_axis                                # Data from ps_axis (N, L, and the figure are included)
        self.omega = None                                   # Eigenfrequency, loaded from a file
        self.ax = None
        self.anim_line = None
        
    # ------------------------------------------------------------------------------------------------------------------

    # METHODS
    def _load_data(self):
        # Data file is expected to be nx3 where the columns represent n, l, omega respectively
        # Load the data and assign the columns to the proper variables
        # file_data = np.loadtxt(self.specs.data_fname)
        #self.specs.N = file_data[:,0]
        #self.specs.L = file_data[:,1]
        #self.omega = file_data[:,2]
        self.specs.N = np.array(
            [0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5,
             0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5])

        self.specs.L = np.array(
            [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6,
             7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10])
        self.omega = np.array(
            [float("NaN"), 0.99, 1.77, 2.60, 3.44, 4.30, 0.36, 1.10, 1.83, 2.64, 3.47, 4.32, 0.57, 1.25, 1.92, 2.70,
             3.51, 4.35,
             0.75, 1.42, 2.03, 2.77, 3.57, 4.40, 0.93, 1.60, 2.17, 2.87, 3.64, 4.46, 1.10, 1.78, 2.32, 2.98, 3.73, 4.52,
             1.26, 1.97, 2.49, 3.10, 3.82, 4.60,
             1.43, 2.15, 2.67, 3.24, 3.93, 4.69, 1.60, 2.33, 2.86, 3.40, 4.05, 4.79, 1.75, 2.50, 3.05, 3.57, 4.18,
             4.89])

    # ------------------------------------------------------------------------------------------------------------------

    def _produce_plot(self):

        # Set the axis and prepare the plot
        self.ax = self.specs.figure.add_subplot(self.specs.axis_loc)
        plot = self.ax.scatter(self.specs.L, self.omega, s=100, c=self.specs.N, cmap='rainbow', edgecolors='none')
        self.anim_line = plot

        # Add plot details
        self._add_labels()


    def _add_labels(self):
        self.ax.set_title("Dispersion Curve")
        self.ax.set_xlim(np.min(self.specs.L)-1, np.max(self.specs.L)+1)
        self.ax.set_xlabel("Angular degree (l)")
        self.ax.set_ylabel("Frequency [mHz]")



    # Have to include these two
    def init_anim_data(self):
        pass

    # ------------------------------------------------------------------------------------------------------------------

    def update_anim_data(self, iteration):

        pass
    # ------------------------------------------------------------------------------------------------------------------
