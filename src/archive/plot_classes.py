from abc import ABC, abstractmethod

class gen_plot(ABC):
    # Abstract base class. Sub-classes of this are classes to generate different types of plots
    # E.g. a class called gen_dispersion


    # Methods:
    def plot(self, plot_specs):
        # Function is the driver for plotting - accessed by main codes. Will first prepare the plot. This incorporates
        # any loading of the data and processing (e.g. integration). Then runs the make_plot function to actually make
        # the plot
        self._prepare_plot(plot_specs)
        self._make_plot()


    @abstractmethod
    def _make_plot(self):
        # The actual plotting step - should return fig and axis to the plot function.
        pass

    def _prepare_plot(self, plot_specs):
        # Should include all loading/re-arrangement of data/any integration etc
        self._load_radial_data(plot_specs)
        if self.integration_required:
            self._integrate_mode()

    def _integrate_mode(self, n, l, omega):
        # I think this may be the same for each class type that requires the ability for integration. If not, then it
        # will need to be an abstract method.
        pass

    @abstractmethod
    def _output_plot(self):
        # Some kind of generic function to save to a file
        pass

    @abstractmethod
    def _load_radial_data(self):
        # Should include all loading/re-arrangement of data/any integration etc
        print("Hello")
        pass

