What is our class structure?
===========================

We use three main classes to produce plots and animation. The ``ps_figure`` class defines objects that control an entire
matplotlib figure. Each ``ps_figure`` contains a list of ps_axis objects. Each ``ps_axis`` object is responsible for producing a
graphic (plot/animation) on a single axis of the matplotlib figure. This can be visualised in the figure below:

.. image:: _static/plot_2D_classes.png
  :width: 800
  :alt: Testing alt text

Each ``ps_axis`` class produces its plot by enacting the creation of a ``NM_image``. In fact, ``NM_image`` is an abstract base
class and objects of concrete sub-classes are created. Each of these subclasses represents a different type of plot (e.g.
a dispersion plot or a 2D_radial plot).

