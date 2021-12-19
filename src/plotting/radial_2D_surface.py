from plotting.NM_image import NM_image
import numpy as np
import math
import scipy.special as ss

class radial_2D_surface(NM_image):
    """A concrete subclass of NM_image that produces surface motion 2D plots for an individual mode. """
    
    # Attributes
    def __init__(self, ps_axis):
        """
        :param ps_axis: ps_axis object that holds specifications for the details of the plot
        :type ps_axis: ps_axis object
        """

        self.specs = ps_axis                                # All the data from the ps_axis including the figure
        self.anim_line = None                               # Storing the 2D line object for animation
        self.ax = None                                      # The axis of the figure

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
        
        # Define a coordinate system
        theta = np.linspace(0, np.pi, 1000)
        phi = np.linspace(0, np.pi*2, 1000)

        # Define the 2D grid of theta and phi
        theta, phi = np.meshgrid(theta, phi)
        # Now convert from spherical to Cartesian coordinates
        x, z = self._sph2cart(theta, phi)

        # Calculate Ylm to generate the corresponding surface pattern
        ylm_phi, ylm_th = self._calc_ylm(theta, phi)

        # Toroidal modes equation

        

    # ------------------------------------------------------------------------------------------------------------------

    def _sph2cart(self, theta, phi):
        """Converts spherical coordinates to Cartesian."""

        # Convert to cartesian coordinates for plotting in plane perpendicular to y axis
        x = self.specs.radius*np.cos(phi)*np.sin(theta)
        z = self.specs.radius*np.cos(theta)

        return x, z

    # ------------------------------------------------------------------------------------------------------------------

    def _calc_ylm(self, theta, phi):
        """
        Calculates the spherical harmonic Y_lm as a function of theta and phi.
        :param l: Angular degree of spherical harmonic
        :type l: int
        :param m: Azimuthal order of spherical harmonic
        :type m: int
        :param theta: Array of theta coordinates
        :type theta: 1D array
        :param phi: Array of phi coordinates
        :type phi: 1D array
        :return ylm_im: Imaginary component of Ylm
        :return ylm_real: Real component of Ylm
        """

        # Using equation: Ylm(theta, phi) = ((2l + 1)(l-m)/(4pi(l+m)!))**0.5 * Plm(cos(theta)) where Plm is the associated
        # legendre polynomial.
        prefactor = np.sqrt( ((2*self.specs.L[0] + 1)*math.factorial(self.specs.L[0]-self.specs.M[0]))/(4*np.pi*math.factorial(self.specs.L[0]+self.specs.M[0])))

        # Create filled arrays of correct length for m, l:
        M = np.zeros((len(theta),)) + self.specs.M[0]
        L = np.zeros((len(theta),)) + self.specs.L[0]

        # Get associated legrendre polynomial plm:
        plm = ss.lpmv(M, L, np.cos(theta))
        ylm_im = prefactor * plm * (np.cos(self.specs.M[0]*phi))    # Imaginary part
        ylm_real  = prefactor * plm * (np.sin(self.specs.M[0]*phi)) # Real part
        return ylm_im, ylm_real

    # ------------------------------------------------------------------------------------------------------------------

    def init_anim_data(self):
        """Initialises data values for first frame of an animation. """
        
    # ------------------------------------------------------------------------------------------------------------------

    def update_anim_data(self, iteration):
        """Function is used to update MPL artists (e.g. a 2DLine object) as part of animations for given iteration value
        see _gen_animations() in ps_figure.py

        :type iteration: int
        :param iteration: Iteration step for animations
        """