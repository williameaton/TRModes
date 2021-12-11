Visualisation
=============
.. toctree::
   :maxdepth: 4
   :caption: Documentation:

   ps_figure
   ps_axis
   NM_image

We offer a number of different plotting options for visualising normal mode data, each of which are described below, which
may be in 2D or 3D, and static or animated.


2D Figures
~~~~~~~~~~
2D plots harness the functionality of ``Matplotlib`` and therefore allows any number of different 2D plots to be combined
in a single figure. By default, figures return both a static (.png) and animated (.gif) version of the figure.

Dispersion plot (static)
------------------------
    Simple dispersion plots may be produced for visualising the relationship between the azimuthal order and eigenfrequency
    of a series of normal modes. These are colour-coded such that modes of constant radial order (n) have consistent colour.

2D radial plots (animated)
--------------------------
    Radial plots show the displacement of the normal mode as a function of depth, and highlight any zero-crossing points.
    A combination of 2D radial plots and surface plots can be used to get a good understanding of 3D motions, if you don't
    want to deal with 3D plots!


3D Figures (animated)
~~~~~~~~~~~~~~~~~~~~~
Our 3D figures use a slightly different approach for visualising. We use PyVista_ to generate a series of *.vtk* files
which can then be used in conjuction with Paraview_ to produce 3D, interactive animations of normal mode oscillations.
We consider the oscillations in a lagrangian perspective by tracking the motion of initially-unperturbed particles. These
are not structured grids and so we reccommend choosing the *Point Gaussian* representation. In particular, we find the
'black-edged circle' shader preset with a radius of 0.02 to be a good representation of the particles.

.. image:: _static/Example_l4_m0_1.png
  :width: 800
  :alt: Testing alt text


.. _Paraview: https://www.paraview.org/
.. _PyVista:  https://www.pyvista.org/


