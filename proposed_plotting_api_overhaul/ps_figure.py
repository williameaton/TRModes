from radial_2D_plot import radial_2D_plot
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class ps_figure():

    def __init__(self, axes_list, fname_out):
        self.axes_list = axes_list              # List of PS_axis objects to be used
        self.fname_out = fname_out              # Figure output filename
        self.figure = plt.Figure()              # Matplotlib figure to be used
        self.animation = None                   # Funcanimate.animation object will end up here if animations used
        self.NM_img_objs = []                   # List of NM_image objects generated from PS_axis inputs by
                                                #  function _gen_NM_img_objects()
    # ------------------------------------------------------------------------------------------------------------------


    def plot(self):
        # Create the different NM_image subclass objects (e.g. dispersion, 2D_radial) from the inputted PS_axis objs
        # This also adds the plots from each of these subclasses to the overall figure
        self._gen_NM_img_objects()

        # Generate any animations
        self._gen_animations()

        # Output everything!
        self._output_plots()

    # ------------------------------------------------------------------------------------------------------------------

    def _axis_factory(self, axis_obj):
        # Factory function that takes in a PS_axis object and returns an object of the relevant subclass of NM_image
        # e.g. a 2D radial plot or a dispersion plot

        # Let axis_obj know what figure it is related to
        axis_obj._set_ps_axis_figure(self.figure)

        # Determine correct type of NM_image subclass to generate and generate it
        if axis_obj.type == "radial_2D_plot":
            obj = radial_2D_plot(axis_obj)
        elif axis_obj.type == "dispersion":
            #obj = dispersion(axis_obj)
            pass

        return obj

    # ------------------------------------------------------------------------------------------------------------------

    def _gen_NM_img_objects(self):
        # Iteratively generating a NM_image object and running obj.make(); this updates obj to its finall form
        # i.e. actually creating the plot
        # Note that these objects are stored in self.NM_img_objs for use in producing animations
        for axis_i in self.axes_list:
            # Create NM_image object
            obj = self._axis_factory(axis_i)
            # Axis object makes plot and adds to fig
            obj.make()
            # Append this NM_image object to the list
            self.NM_img_objs.append(obj)

    # ------------------------------------------------------------------------------------------------------------------

    def _output_plots(self):
        # Output a static version of the figure:
        out_str = "./" + self.fname_out + ".png"
        print(f"Saving static figure {out_str}")
        self.figure.savefig(out_str)

        # Now save an animated version:
        out_str = "./" + self.fname_out + ".mp4"
        print(f"Saving animated figure {out_str}")
        self.animation.save(out_str)

    # ------------------------------------------------------------------------------------------------------------------

    def _gen_animations(self):
        # This is a function which basically takes all of the axis objects stored in NM_img_objs and animates them if
        # that is feasible:

        # Get all of the line objects that will be animated from all the NM_img_objs:
        lines = []
        for a in self.NM_img_objs:
            lines.append(a.anim_line)

        # Define an initialisation function for the animation that updates the data for each line type
        # The way in which the data is updated is defined for each NM_image subclass separately in two functions:
        # init_anim_data() and update_anim_data()

        def init():
            # Loop through all the line objects
            for i in range(len(self.NM_img_objs)):
                # self.axes_objs[i].init_anim_data will return x_data, y_data to be updated
                lines[i].set_data(self.NM_img_objs[i].init_anim_data())
            return lines

        def animate(iteration):
            for i in range(len(self.NM_img_objs)):
                # self.axes_objs[i].update_anim_data will return x_data, y_data to be updated
                lines[i].set_data(self.NM_img_objs[i].update_anim_data(iteration))
            return lines

        # Create animation and save it to as an attribute of the figure class
        self.animation = animation.FuncAnimation(self.figure, animate, init_func=init,
                                                 interval=20, blit=True, save_count=200)
    # ------------------------------------------------------------------------------------------------------------------
