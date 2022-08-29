# Python Libraries
import pandas as pd
import numpy as np

# My Libraries
from .MeasuredData import MeasuredData
from .GetterMixin import GetterMixin
from .SetterMixin import SetterMixin

###########################################################################
# Species Class
###########################################################################
class Species(MeasuredData, GetterMixin, SetterMixin):
    '''
    '''
    # Constructor
    def __init__(self, experiment_info, raw_data, feed_name, name):
        # Constructor for MeasuredDate Class
        super().__init__(experiment_info, raw_data, feed_name)

        # Class Members
        self._name = name

        # Cumulative Consumption/Production
        self._cumulative = pd.Series(data=[np.nan]*self._sample_num)
        self._cumulative_unit = pd.Series(data=[np.nan]*self._sample_num)

        # Two-Pt. Calc.
        self._sp_rate = pd.Series(data=[np.nan]*self._sample_num)

        # Poly. Reg.
        self._polyorder = None
        self._polyfit = None
        self._polyreg_cumulative = pd.Series(data=[np.nan]*self._sample_num)
        self._polyreg_sp_rate = pd.Series(data=[np.nan]*self._sample_num)

        # Rolling Poly. Reg
        self._rollpolyreg_order = None
        self._rollpolyreg_window = None
        self._rollpolyreg_sp_rate = pd.Series(data=[np.nan]*self._sample_num)

        # Flags
        self._in_process_flag = False
        self._twopt_flag = False
        self._polyreg_flag = False
        self._rollreg_flag = False
        