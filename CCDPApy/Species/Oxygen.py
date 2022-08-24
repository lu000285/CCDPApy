from .Species import Species
from ..in_process.OxygenMixin import OxygenMixin
from ..post_process.two_point_calc.OxygenMixin import OxygenTwoPtMixin
from ..post_process.polynomial_regression.OxygenMixin import OxygenPolyRegMixin

###########################################################################
# Oxygen Class
###########################################################################
class Oxygen(Species, OxygenMixin, OxygenTwoPtMixin, OxygenPolyRegMixin):
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
        """
        Get Oxygen Uptake Rate in Measured Data (mmol/L/hr)
        
        Parameters
        ----------

        Returns
        -------
        self._our :
            Oxygen Uptake Rate in Measured Data (mmol/L/hr)
        """
        return self._our

    
    def get_sp_rate_md(self):
        """
        Get SP. Oxygen Consumption Rate in Measured Data (mmol/109cell/hr)
        
        Parameters
        ----------

        Returns
        -------
        self._oxygen_consumption_rate :
            SP. Oxygen Consumption Rate in Measured Data (mmol/109cell/hr)
        """
        return self._oxygen_consumption_rate


    def get_oxy_cons(self):
        """
        Get Oxygen Consumed (mmol/L)
        
        Parameters
        ----------

        Returns
        -------
        self._oxygen_consumed :
            Oxygen Consumed (mmol/L)
        """
        return self._oxygen_consumed

    
###########################################################################
