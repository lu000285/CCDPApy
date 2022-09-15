# Python Libraries
import pandas as pd
import numpy as np

# My Libraries
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
        self._exp_id = measured_data.exp_id # Experiment ID
        self._experimenter_name = measured_data.exp_name    # Experimentor Name
        self._cell_line_name = measured_data.cell_line_name # Cell Line Name
        self._initial_volume = measured_data.initial_v  # Initial Culure Volume
        self._sample_num = measured_data.sample_num # Sample Numbers
        self._xv = measured_data.xv # Viable Cell Concentration
        self._xd = measured_data.xd # Total Cell Concentraion
        self._xt = measured_data.xt # Dead Cell Concentration
        self._run_time_hour = measured_data.run_time_hour   # Run Time (hrs)
        self._v_before_sampling = measured_data.v_before_sampling   # Culure Volume Before Sampling
        self._v_after_sampling = measured_data.v_after_sampling # Culture Volume After Sampling
        self._our = measured_data.our   # Oxygen Up Take Rate
        self._oxygen_consumed = measured_data.oxygen_consumed   # Oxygen Consumed
        self._oxygen_consumption_rate = measured_data.oxygen_consumption_rate   # Oxygen Consumption Rate
        self._product_conc = measured_data.product_conc # Product(IgG) Concentraion
        self._feed_media_added = measured_data.feed_media_added # Feed Media Added
        self._feed_data = measured_data.feed_data   # Separate Feed Data (pd.DataFrame)
        self._feed_list = measured_data.feed_list   # Separate Feed List

        # Cumulative Consumption/Production
        self._cumulative = pd.Series(data=[np.nan]*self._sample_num)    # Cumulative Consumption/Production
        self._cumulative_unit = pd.Series(data=[np.nan]*self._sample_num)   # Unit of Cumulative Consumption/Production
        self._direct_cumulative = False # True if measured data has calculated cumulative consumption/production.

        # Two-Pt. Calc.
        self._sp_rate = pd.Series(data=[np.nan]*self._sample_num)   # Specific-Rate

        # Poly. Reg.
        self._polyorder = None  # Polynomial Regression Order 
        self._polyfit = None    # Polynomial Regression Fit for Cumulative Consumption/Production (numpy.polyfit)
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
        