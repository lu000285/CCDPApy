from .Species import Species
from ..in_process.OxygenMixin import OxygenMixin
from ..post_process.two_point_calc.OxygenMixin import OxygenTwoPtMixin
from ..post_process.polynomial_regression.OxygenMixin import OxygenPolyRegMixin

###########################################################################
# Oxygen Class
###########################################################################
class Oxygen(Species, OxygenMixin, OxygenTwoPtMixin, OxygenPolyRegMixin):
    '''
    Oxygen class.

    Attribute
    ---------
        name : str
            name of species.
        measured_data : python object
            MeasuredData object.
    '''
    # Constructor
    def __init__(self, name, measured_data):
        '''
        Parameters
        ---------
            name : str
                name of species.
            measured_data : python object
                MeasuredData object.
        '''
        # Constructor for Species Class
        super().__init__(name=name, measured_data=measured_data)

        # Measurement Index
        self._idx = self._oxygen_consumption_rate[self._oxygen_consumption_rate.notnull()].index


    # Getters
    def get_our_md(self):
        """Get Oxygen Uptake Rate in Measured Data (mmol/L/hr)
        """
        return self._our

    
    def get_sp_rate_md(self):
        """Get SP. Oxygen Consumption Rate in Measured Data (mmol/109cell/hr)
        """
        return self._oxygen_consumption_rate

    def get_oxy_cons(self):
        """Get Oxygen Consumed (mmol/L)
        """
        return self._oxygen_consumed

# End Oxygen class
