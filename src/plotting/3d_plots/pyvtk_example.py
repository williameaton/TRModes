import pyvista as pv
import numpy as np


def _sphere_of_points(r, r_arr, pts_arr, pts_den=10, t=0):
    # If it takes in 100 points and makes a spherical shell of radius r:
    area = 4*np.pi*(r**2)
    # per 90 degrees:
    npts = area*pts_den
    n = int(npts**0.5)

    theta = np.linspace(-np.pi/2, np.pi/2, n)
    phi   = np.linspace(-np.pi, np.pi/2, n)
    cart_pts = np.meshgrid(theta, phi)

    theta = np.array(cart_pts[0]).flatten()
    phi = np.array(cart_pts[1]).flatten()

    x = r*np.sin(phi)*np.cos(theta) + r*np.sin(t)/3
    y = r*np.sin(phi)*np.sin(theta)+  2*r*np.cos(t)/3
    z = r*np.cos(phi)

    # This should not depend on time!!!
    r_add = np.full((len(x),), r)

    #
    r_arr = np.append(r_arr, r_add, axis=0)
    pts_arr = np.append(pts_arr, np.transpose(np.array([x, y, z])), axis=0)
    return pts_arr, r_arr

def _create_globe(time):
    p = np.array([[0, 0, 0]])
    r = np.array([0])
    for radius in np.linspace(0, 10, 30):
        p, r = _sphere_of_points(r=radius, r_arr=r, pts_arr=p, t=time)
    return p, r

'''
If we want to create a movie: 
# initial setup:
t = 0
p, r = _create_globe(t)
mesh = pv.PolyData(p)
mesh["rad"] = r

# Create a plotter:
plotter = pv.Plotter()
plotter.open_movie("test3d.mp4")
plotter.add_mesh(mesh, scalars="rad")
plotter.show(auto_close=False)
plotter.write_frame()'''

p, r = _create_globe(0)
mesh = pv.PolyData(p)
mesh["rad"] = r

for t in np.arange(0, 2*np.pi, 0.1):
    p, r = _create_globe(t)
    mesh.points = p
    mesh["rad"] = r

    mesh.plot(show_bounds=False, cpos='yz', point_size=15, render_points_as_spheres=True)
    #mesh.save(f"figs/sphere{counter}.vtk")

