
class ps_axis():

    def __init__(self, type, data_fname, int_required, N, L, radius, axis_loc=111):
        self.type =  self._assign_plottype(type)    # type of NM_image subclass desired
        self.figure = None                          # MPL figure the NM_image will attach itself to
        self.axis_loc = axis_loc                    # Location of NM_image axis (e.g. 111)
        self.data_fname = data_fname                # File holding relevant data for plot creation
        self.integration_required = int_required    # Does this data need to be integrated?
        self.N = N                                  # N value(s) to be plotted
        self.L = L                                  # L value(s) to be plotted
        self.radius = radius                        # Radius of model eigenfunctions are related to


    def _set_ps_axis_figure(self, f):
        # ==============================================================================================================
        # DESCRIPTION: Allows updating of the figure attribute
        # INPUTS:   f [MPL figure]    - the new MPL figure to assign to attribute
        # ==============================================================================================================
        self.figure = f

    # ------------------------------------------------------------------------------------------------------------------

    def _assign_plottype(self, plot_str):
        # ==============================================================================================================
        # DESCRIPTION: Checks inputted string is an acceptable string
        # INPUTS:   plot_str [str]    - string holding desired plot_type
        # OUTPUTS:  plot_str [str]    - string holding desired plot_type - now checked.
        # ==============================================================================================================

        # Define possible plot_types
        plottype = {
            "dispersion": True,
            "radial_2D_plot": True,
            "3D_animated": True,
        }

        # Check string matches acceptable plot type and return
        if plottype.get(plot_str, False):
            return plot_str
        else:
            raise ValueError(f"Plot type {plot_str} doesn't exist. Must be 'dispersion', 'radial_2D_plot' or '3D_animated")

    # ------------------------------------------------------------------------------------------------------------------

