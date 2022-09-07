# Python Libraries
import pandas as pd
import numpy as np

# My Libraries
from ..MeasuredData.MeasuredData import MeasuredData
from .GetterMixin import GetterMixin
from .SetterMixin import SetterMixin

###########################################################################
# Species Class
###########################################################################
class Species(GetterMixin, SetterMixin):
    '''
    Species class.

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
        # Class Members
        self._name = name

        # Measured data
        self._exp_id = measured_data.exp_id
        self._experimenter_name = measured_data.exp_name
        self._cell_line_name = measured_data.cell_line_name
        self._initial_volume = measured_data.initial_v
        self._sample_num = measured_data.sample_num
        self._xv = measured_data.xv
        self._xd = measured_data.xd
        self._xt = measured_data.xt
        self._run_time_hour = measured_data.run_time_hour
        self._v_before_sampling = measured_data.v_before_sampling
        self._v_after_sampling = measured_data.v_after_sampling
        self._our = measured_data.our
        self._oxygen_consumed = measured_data.oxygen_consumed
        self._oxygen_consumption_rate = measured_data.oxygen_consumption_rate
        self._product_conc = measured_data.product_conc
        self._feed_media_added = measured_data.feed_media_added
        self._feed_data = measured_data.feed_data
        self._feed_list = measured_data.feed_list

        # Cumulative Consumption/Production
        self._cumulative = pd.Series(data=[np.nan]*self._sample_num)
        self._cumulative_unit = pd.Series(data=[np.nan]*self._sample_num)
        self._direct_cumulative = False # Used to check if measured data has calculated cumulative consumption/production.

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
        