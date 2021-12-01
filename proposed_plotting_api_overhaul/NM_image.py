from abc import ABC, abstractmethod

class NM_image(ABC):
    # Abstract base class. Sub-classes of this are classes to generate different types of plots
    # E.g. a class called gen_dispersion

    # METHODS:
    def make(self):
        # Function is the driver for plotting - accessed by main codes. Will first prepare the plot. This incorporates
        # any loading of the data and processing (e.g. integration). Then runs the make_plot function to actually make
        # the plot
        self._prepare_plot()
        self._produce_plot()

    # ------------------------------------------------------------------------------------------------------------------

    def _prepare_plot(self):
        # Should include all loading/re-arrangement of data/any integration etc
        self._load_data()
        if self.specs.integration_required:
            self._integrate_mode()
    # ------------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def _produce_plot(self):
        # The actual plotting step for static images - should return fig and axis to the plot function.
        pass
    # ------------------------------------------------------------------------------------------------------------------

    def _integrate_mode(self, n, l, omega):
        # Some method for integration if it is required - probably hijack this from Terrys code
        pass
    # ------------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def _load_data(self):
        # Should include all loading/re-arrangement of data/any integration etc
        pass
    # ------------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def init_anim_data(self):
        # Function is used to initialise MPL artists (e.g. a 2DLine object) as part of animations
        # see _gen_animations() in ps_figure.py
        pass
    # ------------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def update_anim_data(self, iteration):
        # Function is used to update MPL artists (e.g. a 2DLine object) as part of animations for given iteration value
        # see _gen_animations() in ps_figure.py
        pass
    # ------------------------------------------------------------------------------------------------------------------
