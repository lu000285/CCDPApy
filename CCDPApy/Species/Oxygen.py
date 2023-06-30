import numpy as np

from .Species import Species
from ..in_process.OxygenMixin import OxygenMixin
from ..post_process.polynomial.OxygenMixin import OxygenMixin as Polynomial

###########################################################################
# Oxygen Class
###########################################################################
class Oxygen(Species, 
             OxygenMixin,
             Polynomial):
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

        # Work with parameters
        df = measured_data.param_df
        rate = df['sp_oxygen_consumption_rate_(mmol/10^9_cells/hr)']
        our = df['our_(mmol/L/hr)']
        consumption = df['oxygen_consumed_(mmol/L)']
        idx = consumption[consumption.notnull()].index

        # Members
        self._idx = idx
        self._measured_consumption_rate = rate   # Measured oxygen consumption rate
        self._measured_our = our                 # Measured oxygen Up Take Rate
        self._measured_consumption = consumption # Measured oxygen consumption

    # Getters
    def get_measured_our(self):
        """Get Oxygen Uptake Rate in Measured Data (mmol/L/hr)
        """
        return self._measured_our

    def get_measured_sp_rate(self):
        """Get SP. Oxygen Consumption Rate in Measured Data (mmol/109cell/hr)
        """
        return self._measured_consumption_rate

    def get_measured_consumption(self):
        """Get Oxygen Consumed (mmol/L)
        """
        return self._measured_consumption

# End Oxygen class
