Calculations
============
.. toctree::
   :maxdepth: 4
   :caption: Documentation:

   toroidal_modes

Currently we offer 2 types of mode calculations: Toroidal and Radial

Toroidal Modes
--------------

Overview
~~~~~~~~

The displacement vector **s** corresponding to toroidal modes can be written as

.. math::

   s^T(r,\theta,\phi,t) = \sum_{n} \sum_{l} \sum_{m} {}_{n}A_{l}^{m}\ {}_{n}W_{l}(r)\ C_{l}^{m}(\theta,\phi)\ e^{i {}_{n}\omega_{l}^{m} t}

where **n** is the radial oder, **l** is the angular order, and **m** is the azimuthal order. This equation stipulates that toroidal oscillations are completely described horizontally by vector spherical harmonics :math:`C_{l}^{m}(\theta,\phi)` which are known analytically. Their depth variations, on the other hand, are characterized by a radial differential equation satisfied by a set of toroidal eigenfunctions :math:`{}_{n}W_{l}(r)` and eigenfrequencies :math:`{}_{n}\omega_{l}` that are both dependent on the seismic properties of the Earth model under consideration.


Toroidal eigenfunctions :math:`W(r)` are completely decoupled from their spheroidal counterparts and they satisfy the following second-order ordinary differential equation (ODE):

.. math::

   \frac{1}{r^2} \frac{d}{dr} \left[\mu r^2 \left(\frac{dW}{dr} - \frac{W}{r}\right)\right] + \frac{\mu}{r}\left(\frac{dW}{dr} - \frac{W}{r}\right) + \left[\omega^2 \rho - \frac{\mu \left(k^2 - 2\right)}{r^3}\right] W = 0 

where :math:`k^2 = l(l + 1)` and to which we can associate the radial toroidal traction defined as

.. math::

   T = \mu \left(\frac{dW}{dr} - \frac{W}{r}\right)

These two equations can be rearranged into a coupled system of first-order ODEs more suited for numerical computations

.. math::

   \frac{d}{dr} \begin{bmatrix} W(r)\\T(r) \end{bmatrix} = \begin{bmatrix} \frac{1}{r} & \frac{1}{\mu(r)} \\ -\omega^2 \rho(r) + \frac{(k^2 - 2) \mu(r)}{r^2} & -\frac{3}{r} \end{bmatrix} \begin{bmatrix} W(r)\\T(r) \end{bmatrix}

This is essentially an eigenvalue problem. Our goal therefore is to solve this system subject to some boundary conditions at the lower and upper ends of the region of interest to deduce its non-trivial solutions :math:`{}_{n}\omega_{l}` and :math:`{}_{n}W_{l}`.

Numerical Integration
~~~~~~~~~~~~~~~~~~~~~

For low frequencies **w** and low angular degrees **l**, the system of ODEs above can be integrated numerically. With our TRModes software this can be performed using a simple forward Euler method, a fourth-order Runge-Kutta method, or a second-order Adams-Bashforth method. Regardless of user choice, we integrate the solution from known boundary condtions at the minimum r value up to the maximum r value. In an Earth model this would correspond to the Core-Mantle boundary (CMB) up to the surface.

Searching for Eigenfrequencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In general, for each value of **l**, there are an infinite number **n** of frequencies :math:`{}_{n}\omega_{l}` that satisfy the above ODE system and the boundary conditions. Therefore, a systematic seearch must be performed to identify all the eigenfrequencies in a given frequency range and for a particular value of **l**. This then becomes a root finding problem that can be solved by first identifying regions containing the roots (bracketing an eigenfrequency), and then refining the value of the eigenfrequency once an interval is known. This is done repeatedly until we are confident about landing on an eigenfrequency.

Radial Modes
------------
