Installation
============

TRModes is a selection of python scripts which can be execute from the command line using the ``driver.py`` module.

Installation is therefore pretty simple. All code is available from our Github_ and can be cloned using the usual commands.

.. _Github: https://github.com/willeaton101/TRModes

A number of python packages are required for running TRModes:

* NumPy
* SciPy
* Matplotlib
* PyVista
* Imageio-ffmpeg


For this (lovely) documentation, we also use a theme that requires installing sphinx-rtd-theme-1.0.0:

    ``$ pip3 install sphinx-rtd-theme-1.0.0``
will do the trick! Alternatively, you can edit the ``html_theme`` in ``docs/conf.py`` and change to ``default``

Once all the files and dependencies are downloaded, you can start running the program from your command line. In the
absence of a GUI (under development) the syntax for command line arguments are quite specific and details can be found
on the "Running TRModes" page.
