Command Line Input Arguments
============================
.. toctree::
   :maxdepth: 4
   :caption: Documentation:

   process_input_args
   process_inputs
   process_input_fig


Currently the program is run using command line arguments. The inputs are specified using
flags, therefore the order of arguments does not matter. The inputs and flags are described
below. In the future, the user will be able to run the code using a Graphical User Interface
(GUI).


List of Flags
~~~~~~~~~~~~~

+----------------+-----------+------------------------------------------------+
|      Flags     |   Type    |                   Description                  |
+================+===========+================================================+
| -gui           |           | Launches the GUI (any other flags implemented  |
|                |           | will be ignored)                               |
+----------------+-----------+------------------------------------------------+
| -mf            | string    | File name of input model, full path included.  |   
+----------------+-----------+------------------------------------------------+
| -eqr           | string    | Density equation           	      	      |
+----------------+-----------+------------------------------------------------+
| -eqp           | string    | Compressional velocity equation                |
+----------------+-----------+------------------------------------------------+
| -eqs           | string    | Shear velocity equation                        |
+----------------+-----------+------------------------------------------------+
| -rmin          | float     | Minimum Radius             	      	      |
+----------------+-----------+------------------------------------------------+
| -rmax          | float     | Maximum Radius                                 |
+----------------+-----------+------------------------------------------------+
| -nr            | float     | Number of radial steps                         |
+----------------+-----------+------------------------------------------------+
| -mtype         | string    | Type of mode to compute. Available options are |
|                |           | "toroidal" or "radial"                         |
+----------------+-----------+------------------------------------------------+
| -n             | integer(s)| Radial order value(s). For more than one value,|
|                |           | must be comma separated.                       |
+----------------+-----------+------------------------------------------------+
| -l             | integer(s)| Angular order value(s). For more than one      |
|                |           | value, must be comma separated.                |
+----------------+-----------+------------------------------------------------+
| -nrange        | integer(s)| Range of radial order values, comma separated. |
+----------------+-----------+------------------------------------------------+
| -lrange        | integer(s)| Range of angular order values, comma separated.|
+----------------+-----------+------------------------------------------------+
| -int           | string    | Type of integration method. Available options  |
|                |           | are 4th-order Runge-Kutta ("rk4"), 2nd-order   |
|                |           | Adams-Bashforth ("ab2") or Forward Euler method|
|                |           | ("euler").                                     |
+----------------+-----------+------------------------------------------------+
| -fig           | string    | Specifications for output figures. Must include|
|                |    	     | axis, figure type, angular order (L), radial   |
|                |    	     | order (N), and azimuthal order (M). Optional   |
|                |    	     | figure name for output. Available options for  |
|                |           | figure type include "dispersion", "3D_anim",   |
|                |           | "radial_2D_plot" or "radial_2D_surface".       |
+----------------+-----------+------------------------------------------------+
| -ofile         | string    | File name of preexisting output data. If no    |
|                |           | file exists, must compute mode frequencies.    |
+----------------+-----------+------------------------------------------------+


If the user wants to use a model file:

- Model equations (density, shear and compressional velocity) are not require and will be ignored if inputted.

If the user wants to use model equations:

- Torodial: Requires density and shear velocity equations.
- Radial: Required density and compressional velocity equations.


Example Inputs
--------------
