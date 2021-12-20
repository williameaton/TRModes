from plotting.ps_figure import *
from plotting.ps_axis import ps_axis
import pytest
import numpy as np

# Note because of import errors I have had to put the tests into this directory, rather than tests. I guess we could turn
# the scripts into a package to avoid this?


def test_assign_plottype():
    # Check that error is raised if plot 'type' isnt correct
    with pytest.raises(ValueError):
        # Test 3 different cases
        for type in [0, "diispersion", None]:
            ps_axis(type=type,
                    N=0,
                    L=0,
                    M=0,
                    radius=0)



def test_axis_factory_dispersion():
    # Create a dummy PS_figure object:
    dummy_fig = ps_figure(axes_list=[], fname_out="test.txt")
    # Create dummy axis object:
    dummy_axis = ps_axis(type="dispersion", N=0, L=0, M=0, radius=0)

    # Following command should return an disp_curve object
    image_object = dummy_fig._axis_factory(axis_obj=dummy_axis, _listlen=2)
    assert type(image_object).__name__ == 'disp_curve'



def test_axis_factory_pyvista():
    # Create a dummy PS_figure object:
    dummy_fig = ps_figure(axes_list=[], fname_out="test.txt")

    # (1) Check that if listlen > 1 then an error is thrown
    dummy_axis = ps_axis(type="3d_animated", N=0, L=0, M=0, radius=0)
    with pytest.raises(ValueError):
        dummy_fig._axis_factory(axis_obj=dummy_axis, _listlen=2)

    # (2) Check that if listlen = 1 then it creates correct object:
    image_object = dummy_fig._axis_factory(axis_obj=dummy_axis, _listlen=1)
    assert type(image_object).__name__ == 'anim_plot_3D'


def test_calc_ylm():
    # Test random values work for YLM
    from plotting.anim_plot_3D import _calc_ylm
    imag, real = _calc_ylm(l=5, m=3, theta=np.array([0, np.pi/6, np.pi*1.67]), phi=np.array([0, np.pi*0.53, np.pi*0.88]))
    assert (np.round(imag, 5) == np.array([0., -0.06937,  0.12513])).all()
    assert (np.round(real, 5) == np.array([0., 0.23877, -0.26591])).all()


def test_sphere_points():
    # Checking that sphere of points gives the correct values:
    from plotting.anim_plot_3D import _sphere_of_points
    colours = np.array([0,], dtype='float64')
    coords = np.array([[0,0,0]])
    coords, colours = _sphere_of_points(l=3, m=2, radius=10, colours=colours, pts_arr=coords, radial_disp=0, pts_den=0.01, t=0)

    # Define true solutions:
    real_coords = np.array([[ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
                            [ 0.00000000e+00,  0.00000000e+00,  1.00000000e+01],
                            [ 1.00000000e+01,  0.00000000e+00,  6.12323400e-16],
                            [ 1.22464680e-15,  0.00000000e+00, -1.00000000e+01],
                            [-0.00000000e+00,  0.00000000e+00,  1.00000000e+01],
                            [-7.07106781e+00,  7.07106781e+00,  6.12323400e-16],
                            [-8.65956056e-16,  8.65956056e-16, -1.00000000e+01],
                            [-0.00000000e+00, -0.00000000e+00,  1.00000000e+01],
                            [-1.83697020e-15, -1.00000000e+01,  6.12323400e-16],
                            [-2.24963967e-31, -1.22464680e-15, -1.00000000e+01]])

    real_colours = np.array([ 0., 10., 10., 10.,  9.,  9.,  9., 10., 10., 10.])

    # Assert equality of both
    assert (np.round(coords, 8)==np.round(real_coords, 8) ).all()
    assert (np.round(colours, 2)== np.round(real_colours, 2)).all()


def test_get_colours():
    from plotting.anim_plot_3D import _get_colours
    # Create dummy variables:
    npts = 10
    theta = np.linspace(-1, 1, npts)
    phi = np.linspace(0, 3, npts)

    new_colours = _get_colours(r=5, theta=theta, phi=phi, npts=npts, l=3, m=1)
    true_colours = np.array([5.7509872, 3.7299771, 5.0074482, 4.5284283, 3.1851242,
                             4.9212658,  3.7288056, 3.5394573, 5.2223527, 3.6902237 ])

    assert (np.round(true_colours, 7) == np.round(new_colours,7) ).all()