from NM_image import NM_image
import numpy as np

class disp_curve(NM_image):
    # ATTRIBUTES
    def __init__(self, ps_axis):
        self.specs = ps_axis                                # Data from ps_axis (N, L, and the figure are included)
        self.index = np.array([])
        self.omega = None                           # Eigenfrequency, loaded from a file
        self.n = None                              # These will hold the entire n & l values
        self.l = None                              # listed in the file
        self.ax = None                                      # The axis of the figure
        self.anim_line = None
        
    # ------------------------------------------------------------------------------------------------------------------

    # METHODS
    def _load_data(self):
        # Data file is expected to be nx3 where the columns represent l, n, omega respectively
        # Load the data and assign the columns to the proper variables
        file_data = np.loadtxt(self.specs.data_fname)
        self.l = file_data[:,0]
        self.n = file_data[:,1]
        self.omega = file_data[:,2]

        # Know what values to plot based on the user-defined values of N & L
        self._data_to_plot()

    # ------------------------------------------------------------------------------------------------------------------

    def _produce_plot(self):

        # Set the axis and prepare the plot
        self.ax = self.specs.figure.add_subplot(self.specs.axis_loc)
        plot = self.ax.scatter(self.l[self.index], self.omega[self.index], s=20, c=self.n[self.index], cmap='rainbow', edgecolors='none')
        self.anim_line = plot

        # Add plot details
        self._add_labels()

    # ------------------------------------------------------------------------------------------------------------------

    def _data_to_plot(self):
        # Find the data that the user wants to plot
        # Remember: self.specs.L is a list, and self.specs.N is a list of sublists 
        # (each sublist is corresponding to one value of l)
        
        count = 0

        for i in self.specs.L:
            for j in self.specs.N[count]:
                # Find the indices of the current value of l
                indl = np.where(self.l==i)
                indl = indl[0]
                # Find the indices of the current value of n
                indn = np.where(self.n==j)
                indn = indn[0]
                # The common index
                ind = np.intersect1d(indl, indn)
                # Append the final index to self.index
                self.index = np.append(self.index, ind)
            count = count+1
        
        # Make sure they are integers
        self.index = self.index.astype(int)


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
