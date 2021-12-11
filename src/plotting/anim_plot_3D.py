from NM_image import NM_image
import numpy as np
import pyvista as pv
import scipy.special as ss
import math

class anim_plot_3D(NM_image):
    """A concrete subclass of NM_image that produces 3D animations for an individual mode's oscillations. """

    # Attributes
    def __init__(self, ps_axis):
        """
        :param ps_axis: ps_axis object that holds specifications for the details of the plot
        :type ps_axis: ps_axis object
        """

        self.specs = ps_axis                                # All the data from the ps_axis including the figure
        self.radial_data = None                             # Data for plotting loaded from some file
        self.mesh = None
        self.p = None
        self.r = None
    # ------------------------------------------------------------------------------------------------------------------

    # METHODS:
    def _produce_plot(self):
        """This will create a static plot of the surface toroidal pattern in Matplotlib - to be added later, kinda worthless"""
        pass


    # ------------------------------------------------------------------------------------------------------------------


    def init_anim_data(self):
        """Initialises data values for first frame of an animation. """
        print("Initialising 3d model globe...")
        self.p, self.r = _create_globe(time=0, radial_data=self.radial_data)
        self.mesh = pv.PolyData(self.p)
        self.mesh["rad"] = self.r
    # ------------------------------------------------------------------------------------------------------------------


    def update_anim_data(self, iteration):
        # loop through time values
        print("Updating frames with timestep dt = 0.1...")
        print("Completed:")
        counter = 0
        for t in  np.arange(0.1, 2 * np.pi, 0.1):
            # Save current state of mesh - here iteration is being used as a file directory (sorry gabe!)
            out_dir = iteration +"/" + self.specs.data_fname + str(counter) + ".vtk"
            self.mesh.save(out_dir)
            #self.mesh.plot(show_bounds=False, cpos='yz', point_size=15, render_points_as_spheres=True)

            # Update frame
            self.p, self.r = _create_globe(t, self.radial_data)
            self.mesh.points = self.p
            self.mesh["rad"] = self.r

            print(f"Time = {t}")
            counter += 1


    # ------------------------------------------------------------------------------------------------------------------

    def _load_data(self):
        """ Module called in _prepare_plot(). Expected file format is single column of data with first 3 lines are N, L,
        Omega. Next lines are displacement/sensitivity at (increasing/decreasing) depth"""

        print("Loading radial displacement vs depth data...")
        displacement = np.loadtxt(self.specs.data_fname, skiprows=6)

        # Instead of using a real radial value we normalise to a value of 1
        # This is because otherwise large, real radii require a number of points that scales with r^2 so the data gets
        # too large.
        # Hence we use a unit sphere
        r = np.linspace(0, 1, len(displacement))

        self.radial_data = np.transpose(np.array([r, displacement]))

    # ------------------------------------------------------------------------------------------------------------------


def _calc_ylm(l, m, theta, phi):
    # Real part only?
    prefactor = np.sqrt( ((2*l + 1)*math.factorial(l-m))/(4*np.pi*math.factorial(l+m)))
    # Degree l, order m:
    M = np.zeros((len(theta),)) + m
    L = np.zeros((len(theta),)) + l

    plm = ss.lpmv(M, L, np.cos(theta))
    ylm_phi = prefactor * plm * (np.cos(m*phi))
    ylm_th = prefactor * plm * (np.sin(m*phi))
    return ylm_phi, ylm_th

def _sphere_of_points(r, r_arr, pts_arr, radial_amp, pts_den=1000, t=0):
    # If it takes in 100 points and makes a spherical shell of radius r:
    area = 4*np.pi*(r**2)
    npts = area*pts_den
    npts = int(npts**0.5)

    theta = np.linspace(0, np.pi, npts)
    phi   = np.linspace(0, 1.5*np.pi , npts)
    THETA, PHI = np.meshgrid(theta, phi)

    theta = np.array(THETA).flatten()
    phi = np.array(PHI).flatten()

    l = 4
    m = 0

    if npts!=0:
        ylm_phi, ylm_th = _calc_ylm(l=l, m=m, theta=theta, phi=phi)
        r_add = np.full((len(theta),), r) + np.sin(10*phi)
        ylm_phi = ylm_phi*np.sin(t)*radial_amp*0.4
        ylm_th = ylm_th*np.sin(t)*radial_amp*0.4
    else:
        ylm_th = 0
        ylm_phi =0
        r_add = np.full((len(theta),), r)




    phi += ((l-m)/l)*ylm_phi
    theta += (m/l)*ylm_th

    x = r*np.cos(phi)*np.sin(theta)
    y = r*np.sin(phi)*np.sin(theta)
    z = r*np.cos(theta)

    # This should not depend on time!!!

    #
    r_arr = np.append(r_arr, r_add, axis=0)
    pts_arr = np.append(pts_arr, np.transpose(np.array([x, y, z])), axis=0)
    return pts_arr, r_arr



def _create_globe(time, radial_data):
    p = np.array([[0, 0, 0]])
    r = np.array([0])
    for i in range(len(radial_data[:,0])):
        p, r = _sphere_of_points(r=radial_data[i,0], r_arr=r, pts_arr=p, radial_amp=radial_data[i,1], t=time)
    return p, r