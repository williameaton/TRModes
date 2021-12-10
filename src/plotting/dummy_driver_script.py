import matplotlib.pyplot as plt

from ps_figure import ps_figure
from ps_axis import ps_axis

## DUMMY SCRIPT FOR DEMONSTRATING FUNCTIONALITY. In reality all of the
# objects should have been passed to use by Page's code.

# Create 2 dummy axes:
ax1 = ps_axis(type="3D_animated",
              data_fname="./example_2D_data.txt",
              int_required=False,
              N=5,
              L=5,
              radius=6371,
              axis_loc=121)
'''
ax2 = ps_axis(type="dispersion",
              data_fname="./lnw.txt",
              int_required=False,
              N=[[1,33], [1,35,60,90], [1,50]],
              L=[55,56,60],
              radius=6371,
              axis_loc=122)'''

# Create 1 dummy figure:
f = ps_figure(axes_list=[ax1],
              fname_out="test2")

f.plot()


