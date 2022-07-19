import pandas as pd

from .MeasuredData import MeasuredData

###########################################################################
# Species Class
###########################################################################
class Species(MeasuredData):
    # Class Variables

    # Constructor
    def __init__(self, experiment_info, raw_data, name):
        # Constructor for MeasuredDate Class
        super().__init__(experiment_info, raw_data)

        # Class Members
        self._name = name
        self._cumulative = None
        self._cumulative_unit = None
        self._sp_rate = None

        # Poly. Reg.
        self._polyorder = None
        self._polyfit = None
        self._polyreg_cumulative = None
        self._polyreg_sp_rate = pd.Series(dtype='float')

        # Rolling Poly. Reg
        self._rollpolyreg_order = None
        self._rollpolyreg_window = None
        self._rollpolyreg_sp_rate = pd.Series(dtype='float')

    # Getters
    # Get Species Name
    def get_name(self):
        return self._name

    # Get Cumulative Consumption/Production
    def get_cumulative(self):
        return self._cumulative

    # Get Cumulative Consumption/Production unit
    def get_cumulative_unit(self):
        return self._cumulative_unit

    # Get SP. Rate
    def get_sp_rate(self):
        return self._sp_rate

    # 
