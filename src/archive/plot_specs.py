class plot_specs():
    # Class holds user-defined specifications for a plot they desire. An instance of this class is passed to
    # the plotter factory to generate the correct type of plot

    # Methods:
    def __init__(self, type, inname, outname, fig, N, L, radius, subaxis_pos=111):
        # Attributes:
        self.plot_type = self._assign_plottype(type)  # [str]          -   Holds type of plot to generate
        self.figure = fig                             # [MPL fig. obj] -   Figure  that the plot is added to
        self.subaxis_pos = subaxis_pos                # [int]          -   Position of the new axis on figure (e.g. 111)

        self.in_fname = inname                        # [str]          -   Name of file holding data for plot
        self.out_fname = outname                      # [str]          -   Name of figure that will be outputted

        self.metadata = _metadata(radius=radius, N=N, L=L)



    def _assign_plottype(self, plot_str):
        # ==============================================================================================================
        # DESCRIPTION: Checks inputted string is an acceptable string
        # INPUTS:   plot_str [str]    - string holding desired plot_type
        # OUTPUTS:  plot_str [str]    - string holding desired plot_type - now checked.
        # ==============================================================================================================

        # Define possible plot_types
        plottype = {
            "dispersion" : True,
            "2D_radial"  : True,
            "3D_animated": True,
        }

        # Check string matches acceptable plot type and return
        if plottype.get(plot_str, False):
            return plot_str
        else:
            raise ValueError(f"Plot type {plot_str} doesn't exist. Must be 'dispersion', '2D_radial' or '3D_animated")




class _metadata():
    def __init__(self, radius, N, L):
        self.radius = radius         # [float]        -   Radius for 2D plot
        self.N = N                   # [int]          -   N of eigenfunction
        self.L = L                   # [int]          -   L of eigenfunction