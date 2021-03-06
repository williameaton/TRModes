from plotting.NM_image import NM_image
import numpy as np
import pyvista as pv
import scipy.special as ss
import math

class anim_plot_3D(NM_image):
    """
    A concrete subclass of NM_image that produces 3D animations for an individual mode's oscillations.
    """

    # Attributes
    def __init__(self, ps_axis):
        """
        :param ps_axis: ps_axis object that holds specifications for the details of the plot
        :type ps_axis: ps_axis object
        """

        self.specs = ps_axis        # All the data from the ps_axis including the figure
        self.radial_data = None     # Data for plotting loaded from some file
        self.mesh = None
        self.p = None
        self.r = None
        self.dt = 0.1
    # ------------------------------------------------------------------------------------------------------------------

    # METHODS:
    def _produce_plot(self):
        pass

    # ------------------------------------------------------------------------------------------------------------------


    def init_anim_data(self):
        """
        Initialises data values for first frame of an animation.
        """

        print("Initialising 3d model globe...")
        self.p, self.r = _create_globe(l=self.specs.L[0], m=self.specs.M[0], time=0, radial_data=self.radial_data)
        self.mesh = pv.PolyData(self.p)
        self.mesh["rad"] = self.r
    # ------------------------------------------------------------------------------------------------------------------


    def update_anim_data(self, path):
        """
        Creates the next animation frame. Outputs a file to iteration

        :param path: The file directory for saving to. This, by default, is the name of the figure.
        :type  path: string

        """

        # loop through time values
        print(f"Updating frames with timestep dt = {self.dt}...")
        print("Completed:")
        counter = 0
        for t in np.arange(self.dt, 2 * np.pi, self.dt):
            # Save current state of mesh - here iteration is being used as a file directory (sorry gabe!)
            out_dir = path +"/" + f"l{self.specs.L[0]}_m{self.specs.M[0]}_n{self.specs.N[0]}_" + str(counter) + ".vtk"
            self.mesh.save(out_dir)

            # Update frame
            self.p, self.r = _create_globe(l=self.specs.L[0], m=self.specs.M[0], time=t, radial_data=self.radial_data)
            self.mesh.points = self.p
            self.mesh["rad"] = self.r

            # Occassionally print progress
            if counter%4==0:
                print(f"Time = {np.round(t, decimals=2)}")
            counter += 1

        print(f"VTK files saved to {path}/")

    # ------------------------------------------------------------------------------------------------------------------

    def _load_data(self):
        """
        Loads the displacement vs depth data using the data_fname provided. First 1 row of file is skipped.
        """

        print("Loading radial displacement vs depth data...")
        file_data = np.loadtxt(f"./output/Wr_l{self.specs.L[0]}_n{self.specs.N[0]}.txt", skiprows=1)
        file_data = file_data[:, ::-1]

        # Need to normalise displacement data such that unit sphere globe is created for animations
        # Also radial data is normalised so that the displacements in animations arent crazy!:
        for i in range(2):
            max = np.amax(np.abs(file_data[:,i]))
            file_data[:,i] = file_data[:,i]/max


        self.radial_data = file_data

    # ----------------------------------------------------------------------------------------------------------------------


def _calc_ylm(l, m, theta, phi):
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
    prefactor = np.sqrt( ((2*l + 1)*math.factorial(l-m))/(4*np.pi*math.factorial(l+m)))

    # Create filled arrays of correct length for m, l:
    M = np.zeros((len(theta),)) + m
    L = np.zeros((len(theta),)) + l

    # Get associated legrendre polynomial plm:
    plm = ss.lpmv(M, L, np.cos(theta))
    ylm_im = prefactor * plm * (np.cos(m*phi))    # Imaginary part
    ylm_real  = prefactor * plm * (np.sin(m*phi)) # Real part
    return ylm_im, ylm_real

# ----------------------------------------------------------------------------------------------------------------------


def _sphere_of_points(l, m, radius, colours, pts_arr, radial_disp, pts_den=1000, t=0):
    """
    Generates coordinates for a quasi-spherical shell of points and appends them to a current array of points. Coordinates
    have a corresponding 'colour' value so the changes of those coordinates in time can be visualised. Coordinates may be
    changed through time (as sphere oscillates) but the colours do not.

    :param l: Angular degree of spherical harmonic
    :type l: int

    :param m: Azimuthal order of spherical harmonic
    :type m: int

    :param radius: Radius of the shell to be generated
    :type  radius: float

    :param colours: Current array of colours associated with the coordinates
    :type  colours: 1D array

    :param pts_arr: Array of current cartesian coordinates to be updated
    :type pts_arr:  3D array

    :param radial_disp: Array of the strength of the oscillation with depth.
    :type radial_disp: 1D array

    :param pts_den: Density of points per unit area. Defaults to 1000. We reccomend not changing this.
    :type radial_amp: float

    :param t: Time at which these coordinates exist. Time is used to oscillate the coordinates. Defaults to 0.
    :type t: float
    """

    if radius==0:
        x, y, z = 0
        colours = np.array([0])

    else:
        # Get number of coordinate points in each dimension:
        npts = int((4*np.pi*(radius**2)*pts_den)**0.5)

        # Create theta and phi arrays. Currently hard coded to produce sphere with 2 octets missing for visualisation inside.
        theta = np.linspace(0, np.pi, npts)
        phi   = np.linspace(0, 1.5*np.pi , npts)
        THETA, PHI = np.meshgrid(theta, phi)

        theta = np.array(THETA).flatten()
        phi = np.array(PHI).flatten()

        new_colours = _get_colours(radius, theta, phi, npts, l, m)
        theta, phi = deform_coords(theta, phi, npts, l, m, radial_disp, t)

        # Convert to cartesian coordinates for VTK file.
        x = radius*np.cos(phi)*np.sin(theta)
        y = radius*np.sin(phi)*np.sin(theta)
        z = radius*np.cos(theta)


    # Append new colours and coordinates to present coordinates array.
    colours = np.append(colours, new_colours, axis=0)
    pts_arr = np.append(pts_arr, np.transpose(np.array([x, y, z])), axis=0)

    return pts_arr, colours



def _create_globe(l, m, time, radial_data):
    """
    Creates a (deformed) 3D spheroid of points based on radial steps given by user and time.
    :param l: Angular degree of spherical harmonic
    :type l: int

    :param m: Azimuthal order of spherical harmonic
    :type m: int

    :param time: Time value for frame. Should be between 0 and 2pi but will operate with any value.
    :type time: float

    :param radial_data: Array of radial points and displacement at those points.
    :type radial_data: 2D array

    :return points: Updated array of points/coordinates
    :return colours: Updated array of colour values corresponding to each coordinate.
    """
    colours = np.array([])
    points = np.empty(shape=(0,3))

    # Loop through each radial data point to produce a shell of spheres.
    for i in range(len(radial_data[:,0])):
        points, colours = _sphere_of_points(l= l,
                                            m= m,
                                            radius=radial_data[i,0],
                                            colours=colours,
                                            pts_arr=points,
                                            radial_disp=radial_data[i, 1],
                                            t=time)
    return points, colours


def deform_coords(theta, phi, npts, l, m, radial_disp, t):
    """
    Deforms the original coordinates based on an oscillation of a Ylm pattern over 2*pi

    :param theta: Array of theta coordinates
    :type theta: 1D array

    :param phi: Array of phi coordinates
    :type phi: 1D array

    :param npts: Number of coordinate points
    :type npts: int

    :param l: Angular degree of spherical harmonic
    :type l: int

    :param m: Azimuthal order of spherical harmonic
    :type m: int

    :param radial_disp: Array of the strength of the oscillation with depth.
    :type radial_disp: 1D array

    :param t: Time at which these coordinates exist. Time is used to oscillate the coordinates. Defaults to 0.
    :type t: float

    :return theta: Updated, deformed array of theta coordinates

    :return phi: Updated, deformed array of phi coordinates
    """

    if npts != 0:
        # Any point outside the centre of sphere.
        ylm_phi, ylm_th = _calc_ylm(l=l, m=m, theta=theta, phi=phi)  # Get ylm values.
        ylm_phi = ylm_phi * np.sin(t) * radial_disp * 0.4  # Update YLMs as a function of radius and time
        ylm_th = ylm_th * np.sin(t) * radial_disp * 0.4  # - time is what produces oscillation animations
    else:
        # If at centre of sphere.
        ylm_th = 0
        ylm_phi = 0

        # Deform the theta, phi coordinates according to the YLM patterns
    phi += ((l - m) / l) * ylm_phi
    theta += (m / l) * ylm_th

    return theta, phi



def _get_colours(r, theta, phi, npts, l, m):
    """
    Creates array of colour values for the shell with patterns designed for different l,m oscillations
        :param r: Radius of shell
        :type r: float

        :param theta: Array of theta coordinates
        :type theta: 1D array

        :param phi: Array of phi coordinates
        :type phi: 1D array

        :param npts: Number of coordinate points
        :type npts: int

        :param l: Angular degree of spherical harmonic
        :type l: int

        :param m: Azimuthal order of spherical harmonic
        :type m: int

        :return clr_add: Colour array to be added

        """


    # Set initial homogenous colour based on shell radius
    clr_add = np.full((len(theta),), r)

    # If not at centre of planet
    if npts!=0:
        if l-m!=0:
            clr_add += np.sin(18 * phi)
        if m!=0:
            clr_add += np.sin(18 * theta)

    return clr_add
