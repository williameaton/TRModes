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

     -mtype		Mode type to compute. Options include 'spheriodal','toroidal', or 'radial'.

     -n	<integer(s)>	Radial order value(s). For more than one value, must be comma separated.		
     -l <integer(s)>	Angular	order value(s), must be positive. For more than one value, must be comma
     			separated.
     -nrange <integers> Range of radial order values, comma separated.
     -lrange <integers> Range of angular order values, comma separated and positive.

     -int <string> 	Integration method type. Current options are 4th-order Runge-Kutta ("rk4"),
     	  		2nd-order Adams-Bashforth ("ab2"), and Forward Euler method ("euler").

     -fig <string>	Plotting information for output figures. Must include axis, figure type, angular order
     	  		(l) and radial order (n), and optional name for figure file. Figure type options are "2D",
			"3D", or "Disperion". n,l must be integers and l must be positive.

     -ofile <string>    File name of preexisting output data. If no file exists, must compute mode frequencies.
