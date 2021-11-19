List of flags:

     -gui		Launches the GUI (any other flags implemented will be ignored).

     -mf <string>	File name of input model. If no model is provided by
     			the user, the default file is a homogeneous model.

     -eqr <string>	Density equation.
     -eqp <string>	Compressional velocity equation.
     -eqs <string>	Shear velocity equation.

     -rmin <float>	Minimum radius.
     -rmax <float>	Maximum radius.
     -Nr <float>	Number of radial steps.

     -T			Computes Toroidal modes.
     -R			Computes Radial modes.
     -S			Computes Spheriodal modes.


     -n	<integer(s)>	Radial order value(s). For more than one value, must be comma separated.		
     -l <integer(s)>	Angular	order value(s).	For more than one value must be comma separated.
     -nrange <integers> Range of radial order values, comma separated.
     -lrange <integers> Range of angular order values, comma separated.

     -int <string> 	Integration method type. Current options are 4th-order Runge-Kutta ("rk4"),
     	  		2nd-order Adams-Bashforth ("ab2"), and Forward Euler method ("euler").

     -otype <string>	Output type. Options are 2-Dimensional visuals ("2D"), 3-Dimensional visuals
     	    		("3D"), and a dispersion curve ("disp").

     -oname <string>	Optional output file prefix name.


