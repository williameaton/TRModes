from plotting.NM_image import NM_image
import numpy as np

class disp_curve(NM_image):
    """
    A concrete subclass of NM_image that produces dispersion plots for multiple n, l, omega combinations.
    """
    def __init__(self, ps_axis):
        """
        :param ps_axis: ps_axis object that holds specifications for the details of the plot
        :type ps_axis: ps_axis object
        """
        self.specs = ps_axis                        # Data from ps_axis (the figure and N & L values that the user wants to plot are included)
        self.omega = None                           # Eigenfrequency, loaded from a file
        self.n = None                               # N values, loaded from a file
        self.l = None                               # l values, loaded from a file
        self.ax = None                              # The axis of the figure
        self.anim_line = None                       # See if we still need to keep this...
        self.index = np.array([])
        
    # ------------------------------------------------------------------------------------------------------------------

    # METHODS
    def _load_data(self):
        """
        Data file is expected to be nx3 where the columns represent l, n, omega respectively
        Load the data and assign the columns to the proper variables
        """
        file_data = np.loadtxt(self.specs.data_fname)
        self.l = file_data[:,0]
        self.n = file_data[:,1]
        self.omega = file_data[:,2]

        # Know what values to plot based on the user-defined values of N & L
        self._data_to_plot()

    # ------------------------------------------------------------------------------------------------------------------

    def _produce_plot(self):
        """
        First-order function that produces the plot on the relevant Matplotlib axis.
        """

        # Set the axis and prepare the plot
        self.ax = self.specs.figure.add_subplot(self.specs.axis_loc)
        plot = self.ax.scatter(self.l[self.index], self.omega[self.index], s=20, c=self.n[self.index], cmap='rainbow', edgecolors='none')
        self.anim_line = plot

        # Add plot details
        self._add_labels()

    # ------------------------------------------------------------------------------------------------------------------

    def _data_to_plot(self):
        """
        Find the data that the user wants to plot
        Remember: self.specs.L is a list, and self.specs.N is a list of sublists
        (each sublist is corresponding to one value of l)
        """

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
                # Check if the requested points are in the file
                # For some reason, ind==0 is considered as an empty variable. Have to check for that 
                if ind or ind==0:
                    # Append the final index to self.index
                    self.index = np.append(self.index, ind)
                else:
                    raise ValueError(f"Cannot find l =  {i}, n = {j} in the provided file")

            # Increase the count to move to the next set of N
            count = count+1
        
        # Make sure the indices are integers 
        self.index = self.index.astype(int)

    # ------------------------------------------------------------------------------------------------------------------
    
    def _add_labels(self):
        """
        Adds axis and plot title labels.
        """
        self.ax.set_title("Dispersion Curve")
        self.ax.set_xlim(np.min(self.specs.L)-1, np.max(self.specs.L)+1)
        self.ax.set_xlabel("Angular degree (l)")
        self.ax.set_ylabel("Frequency [mHz]")

    # ------------------------------------------------------------------------------------------------------------------

    # Have to include these two
    def init_anim_data(self):
        """
        Function defined in ABC but not used for this type of plot.
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------

    def update_anim_data(self, iteration):
        """
        Function defined in ABC but not used for this type of plot.

        :param iteration: iteration for animation frame
        :type iteration: integer
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
