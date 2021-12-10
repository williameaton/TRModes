
class ps_axis():
    """ps_axis objects are created from the users input and pass information/specifications to the plotting scripts
       for a single matplotlib axis as part of a figure. Data these objects hold include the type of plot, the normal
       mode(s) that are to be plotted and any relevant model data, and the location of the axis on the figure."""
    def __init__(self, type, data_fname, int_required, N, L, radius, axis_loc=111):
        """
        :param type: Type of plot desired. Currently supports dispersion plots ("dispersion"), 3D volumetric animations
        ("3D_animated") or 2D radial plots ("radial_2D_plot").
        :type type: string
        """
        self.type =  self._assign_plottype(type)    # type of NM_image subclass desired
        self.figure = None                          # MPL figure the NM_image will attach itself to
        self.axis_loc = int(axis_loc)               # Location of NM_image axis (e.g. 111)
        self.data_fname = data_fname                # File holding relevant data for plot creation
        self.integration_required = int_required    # Does this data need to be integrated?
        self.N = N                                  # N value(s) to be plotted
        self.L = L                                  # L value(s) to be plotted
        self.radius = radius                        # Radius of model eigenfunctions are related to


    def _set_ps_axis_figure(self, f):
        """Allows updating of the figure attribute for this class.
            :param f: The matplotlib figure object
            :type f: Matplotlib Figure object
        """
        self.figure = f

    # ------------------------------------------------------------------------------------------------------------------

    def _assign_plottype(self, plot_str):
        """Checks inputted string is an acceptable string
           :param plot_str: String holding desired plot_type
           :type plot_str: string
           :raises ValueError: if plt_str is not "dispersion", "radial_2D_plot" or "3D_animated"
        """

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

