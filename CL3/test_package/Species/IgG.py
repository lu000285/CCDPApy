import imp
from .Species import Species
from ..in_process.IgGMixin import IgGMixin
from ..post_process.two_point_calc.IgGMixin import IgGMixnTwoPt
from ..post_process.polynomial_regression.PolyRegMixin import PolyRegMixin

###########################################################################
# IgG Mixin Class
###########################################################################
class IgG(Species, IgGMixin, IgGMixnTwoPt, PolyRegMixin):
    '''
    '''
    # Constructor
    def __init__(self, experiment_info, raw_data, name):
        # Constructor for Species
        super().__init__(experiment_info, raw_data, name)

        # Members
        # Measurent Index
        self._idx = self._igg_conc[self._igg_conc.notnull()].index

    # Getter
    def get_igg_conc(self):
        return self._igg_conc

###########################################################################