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
        self.measured_data = measured_data

        # Measured data: Experiment Information
        '''exp_info = measured_data.exp_info
        self._exp_id = exp_info['exp_id'] # Experiment ID
        self._experimenter_name = exp_info['name']    # Experimentor Name
        self._cell_line_name = exp_info['cell_line'] # Cell Line Name
        self._initial_volume = exp_info['initial_volume']  # Initial Culure Volume'''

        # Measured data: Parameters
        df = measured_data.param_df
        self._sample_num = df['samples'].size # Sample Numbers
        self._xv = df['viable_cell_conc_(10^6_cells/mL)'] # Viable Cell Concentration
        # self._xd = df['dead_cell_conc_(10^6_cells/mL)'] # Total Cell Concentraion
        # self._xt = df['total_cell_conc_(10^6_cells/mL)'] # Dead Cell Concentration
        self._run_time_hour = df['run_time_(hrs)']  # Run Time (hrs)
        self._v_before_sampling = df['volume_before_sampling_(mL)']   # Culture Volume Before Sampling
        self._v_after_sampling = df['volume_after_sampling_(mL)'] # Culture Volume After Sampling
        # self._our = df['our_(mmol/L/hr)']   # Oxygen Up Take Rate
        # self._oxygen_consumed = df['oxygen_consumed_(mmol/L)']   # Oxygen Consumed
        # self._oxygen_consumption_rate = df['sp_oxygen_consumption_rate_(mmol/10^9_cells/hr)']   # Oxygen Consumption Rate
        self._feed_media_added = df['feed_media_added_(mL)'] # Feed Media Added
        # self._product_conc = measured_data.c_before_feed_df['IgG_(mg/L)'] # Product(IgG) Concentraion
        self._feed_data = measured_data.feed_data   # Separate Feed Data (pd.DataFrame)
        self._feed_list = measured_data.feed_list   # Separate Feed List

        # Cumulative Consumption/Production
        # self._cumulative = pd.Series(data=[np.nan]*self._sample_num)    # Cumulative Consumption/Production
        # self._cumulative_unit = pd.Series(data=[np.nan]*self._sample_num)   # Unit of Cumulative Consumption/Production
        # self._direct_cumulative = False # True if measured data has calculated cumulative consumption/production.

        # Two-Pt. Calc.
        # self._sp_rate = pd.Series(data=[np.nan]*self._sample_num)   # Specific-Rate

        # Poly. Reg.
        '''self._polyorder = None  # Polynomial Regression Order 
        self._polyfit = None    # Polynomial Regression Fit for Cumulative Consumption/Production (numpy.polyfit)
        self._polyreg_cumulative = pd.Series(data=[np.nan]*self._sample_num)    
        self._polyreg_sp_rate = pd.Series(data=[np.nan]*self._sample_num)'''

        # Rolling Poly. Reg
        '''self._rollpolyreg_order = None
        self._rollpolyreg_window = None
        self._rollpolyreg_sp_rate = pd.Series(data=[np.nan]*self._sample_num)'''

        # Flags
        self._in_process_flag = False
        self._twopt_flag = False
        self._polyreg_flag = False
        self._rollreg_flag = False
    
    def get_profile_data(self, data_list, profile_list, kind_list, method_list):
        '''Return cumulative concentration data.
        '''
        df_lst = []
        for d, p, k, m in zip(data_list, profile_list, kind_list, method_list):
            df = self._run_time_hour.to_frame(name='runTime')
            df['value'] = d
            df['profile'] = p
            df['kind'] = k
            df['method'] = m
            df_lst.append(df)
        data = pd.concat(df_lst, axis=0)
        data = data.sort_values(by=['runTime'], kind='stable').reset_index(drop=True)
        return data