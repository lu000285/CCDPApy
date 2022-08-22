# Python Libraries
import pandas as pd

# My Libraries
from .MeasuredData import MeasuredData

###########################################################################
# Species Class
###########################################################################
class Species(MeasuredData):
    '''
    '''
    # Constructor
    def __init__(self, experiment_info, raw_data, name):
        # Constructor for MeasuredDate Class
        super().__init__(experiment_info, raw_data)

        # Class Members
        self._name = name
        self._cumulative = pd.Series(data=[pd.NA]*self._sample_num)
        self._cumulative_unit = pd.Series(data=[pd.NA]*self._sample_num)
        self._sp_rate = pd.Series(data=[pd.NA]*self._sample_num)

        # Poly. Reg.
        self._polyorder = None
        self._polyfit = None
        self._polyreg_cumulative = pd.Series(data=[pd.NA]*self._sample_num)
        self._polyreg_sp_rate = pd.Series(data=[pd.NA]*self._sample_num)

        # Rolling Poly. Reg
        self._rollpolyreg_order = None
        self._rollpolyreg_window = None
        self._rollpolyreg_sp_rate = pd.Series(data=[pd.NA]*self._sample_num)


    # Getters
    def get_name(self):
        """
        Get Species Name
        
        Parameters
        ----------

        Returns
        -------
        self._name :
            Species Name
        """
        return self._name


    def get_cumulative(self):
        """
        Get Cumulative Consumption/Production
        
        Parameters
        ----------

        Returns
        -------
        self._cumulative :
            Cumulative Consumption/Production
        """
        return self._cumulative


    def get_cumulative_unit(self):
        """
        Get Cumulative Consumption/Production unit
        
        Parameters
        ----------

        Returns
        -------
        self._cumulative_unit :
            Cumulative Consumption/Production unit
        """
        return self._cumulative_unit


    def get_sp_rate(self):
        """
        Get Get SP. Rate
        
        Parameters
        ----------

        Returns
        -------
        self._sp_rate :
            SP. Rate
        """
        return self._sp_rate

