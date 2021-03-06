
class ps_axis():
    """
    ps_axis objects are created from the users input and pass information/specifications to the plotting scripts
    for a single matplotlib axis as part of a figure. Data these objects hold include the type of plot, the normal
    mode(s) that are to be plotted and any relevant model data, and the location of the axis on the figure.
    """
    def __init__(self, type, N, L, M, radius,  data_fname="lnw.txt", axis_loc=111):
        """
        :param type: Type of plot desired. Currently supports dispersion plots ("dispersion"), 3D volumetric animations ("3D_animated") or 2D radial plots ("radial_2D_plot").
        :type type: string

        :param L: The l values for plotting - unless for a dispersion plot there should only be one element
        :type  L: 1D array

        :param M: The m values for plotting - needed for plots of surface oscillations.
        :type  M: 1D array

        :param N: The n values for plotting - unless for a dispersion plot there should only be one element
        :type  N: 1D array

        :param radius: Radius of elastic body
        :type  radius: float

        :param axis_loc: Axis location on MPL subplots figure, defaults to 111.
        :type  axis_loc: int

        :param data_fname: File name containing l, n, omega data. Defaults to lnw.txt
        :type  data_fname: string

        """
        self.type =  self._assign_plottype(type)    # type of NM_image subclass desired
        self.figure = None                          # MPL figure the NM_image will attach itself to
        self.axis_loc = int(axis_loc)               # Location of NM_image axis (e.g. 111)
        self.integration_required = False                # Bool - is integration of data provided required
        self.data_fname = data_fname                # File holding relevant data for plot creation
        self.N = N                                  # N value(s) to be plotted
        self.L = L                                  # L value(s) to be plotted
        self.M = M                                  # M value(s) to be plotted
        self.radius = radius                        # Radius of model eigenfunctions are related to


    def _set_ps_axis_figure(self, f):
        """
        Allows updating of the figure attribute for this class.

        :param f: The matplotlib figure object
        :type f: Matplotlib Figure object
        """
        self.figure = f

    # ------------------------------------------------------------------------------------------------------------------

    def _assign_plottype(self, plot_str):
        """
        Checks inputted string is an acceptable string

        :param plot_str: String holding desired plot_type
        :type plot_str: string

        :raises ValueError: if plt_str is not "dispersion", "radial_2D_plot", "radial_2D_surface" or "3D_animated"

        """

        # Define possible plot_types
        plottype = {
            "dispersion": True,
            "2d_radial": True,
            "2d_surface": True,
            "3d_animated": True,
        }

        # Check string matches acceptable plot type and return
        if plottype.get(plot_str, False):
            return plot_str
        else:
            raise ValueError(f"Plot type {plot_str} doesn't exist. Must be 'dispersion', '2d_radial', '2d_surface' or '3d_animated")

    # ------------------------------------------------------------------------------------------------------------------

