from .Species import Species
from ..in_process.OxygenMixin import OxygenMixin
from ..post_process.two_point_calc.OxygenMixin import OxygenMixinTwoPt
from ..post_process.polynomial_regression.OxygenMixin import OxygenMixinPolyReg

###########################################################################
# Oxygen Class
###########################################################################
class Oxygen(Species, OxygenMixin, OxygenMixinTwoPt, OxygenMixinPolyReg):
    '''
    '''
    # Constructor
    def __init__(self, experiment_info, raw_data, name):

        # Constructor for Species Class
        super().__init__(experiment_info, raw_data, name)

        # Measurement Index
        self._idx = self._oxygen_consumption_rate[self._oxygen_consumption_rate.notnull()].index

    # Getters
    def get_our_md(self):
            return self._our
    
    def get_sp_rate_md(self):
        return self._oxygen_consumption_rate

    def get_oxy_cons(self):
        return self._oxygen_consumed

    

###########################################################################
