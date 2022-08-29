# Python Libraries
import pandas as pd
import numpy as np

# My Libraries
from ..helper_func.helper_func import check_key
from ..pre_process.PreProcessMixin import PreProcessMixn

###########################################################################
# Measured Data Class
###########################################################################
class MeasuredData(PreProcessMixn):
    '''
    Store the measured data in a bioprocess experiment.
    
    Attributes
    ----------
    experiment_info : DataFrame
        The information of the experiment.
    raw_data : DataFrame
        The measured data of the experiment.
    sheet_name : str
    '''

    # Constructor
    def __init__(self, experiment_info, raw_data, feed_name):
        '''
        Parameters
        ----------
        experiment_info : DataFrame
            The information of the experiment.
        raw_data : str : DataFrame
            The measured data of the experiment.
        feed_name : str
        '''

        # Experoment Infomation Members
        self._experiment_id = experiment_info.loc['Experiment ID'].get(1)
        self._experimenter_name = experiment_info.loc['Name'].get(1)
        self._cell_line_name = experiment_info.loc['Cell Line'].get(1)
        self._initial_volume = float(experiment_info.loc['Initial Volume (mL)'].get(1))

        # Experimental Variables
        # Sample Number
        self._sample_num = check_key(raw_data, 'SAMPLE #')

        # Time
        self._date = check_key(raw_data, 'DATE')
        self._time = check_key(raw_data, 'TIME')
        self._run_time_day = check_key(raw_data, 'Day')
        self._run_time_hour = check_key(raw_data, 'RUN TIME (HOURS)')
        self._run_time_mid = None

        # Culture, Added Feed, and Feed Media Volume
        self._feed_name = feed_name.upper()
        self._feed_added = check_key(raw_data, f'{self._feed_name} FEED ADDED (mL)').fillna(0)
        self._base_added = check_key(raw_data, 'BASE ADDED (mL)').fillna(0)
        self._sample_volume = check_key(raw_data, 'SAMPLE VOLUME (mL)').fillna(0)
        self._feed_media_added = check_key(raw_data, 'FEED MEDIA ADDED (mL)').fillna(0)

        # Experimental Cell and Oxygen Variables
        self._xv = check_key(raw_data, 'VIABLE CELL CONC. XV (x106 cells/mL)').fillna(0)  # xv: Viable Cell Concentration
        self._xd = check_key(raw_data, 'DEAD CELL CONC. Xd (x106 cells/mL)').fillna(0)    # xd: Dead Cell Concentraion
        self._xt = check_key(raw_data, 'TOTAL CELL CONC. Xt (x106 cells/mL)').fillna(0)   # xt: Total Cell Concentraion
        self._viability = check_key(raw_data, 'VIABILITY (%)')
        self._pH = check_key(raw_data, 'pH')
        self._do = check_key(raw_data, 'DO (%)')
        self._our = check_key(raw_data, 'OUR (mmol/L/hr)').fillna(0)
        self._oxygen_consumption_rate = check_key(raw_data, 'SP. OXYGEN CONSUMPTION RATE (mmol/109cell/hr)').fillna(0)
        self._oxygen_consumed = check_key(raw_data, 'OXYGEN CONSUMED (mmol/L)').fillna(0)
        self._optical_density = check_key(raw_data, 'OPTICAL DENSITY')
        self._osmolality = check_key(raw_data, 'OSMOLALITY (mmol/kg)')
        #
        self._product_conc = check_key(raw_data, 'IgG CONC. (mg/L)').fillna(0)

        # Used to check if measured data has calculated cumulative consumption/production.
        self._direct_cumulative = False

        # Variables Used in In Process
        n = len(self._sample_num) # Number of Samples        
        self._v_before_sampling = pd.Series(data=[0.0] * n, name='VOLUME BEFORE SAMPLING (mL)')
        self._v_after_sampling = pd.Series(data=[0.0] * n, name='VOLUME AFTER SAMPLING (mL)')
        self._v_after_feeding = pd.Series(data=[0.0] * n, name='VOLUME AFTER FEEDING (mL)')
        self._feed_status = pd.Series(data=np.nan * n, name='Feed Status')

        # Call Initialize Method
        # Calculate Run Time 
        if (not self._run_time_hour.any() and not self._run_time_day.any()):
            self.run_time()

        # Calculate Culture Volume
        self.culture_volume()

        # For CL3
        ########################################################################
        if self._cell_line_name=='Merck':
            x = [1935.00, 1920.00, 1905.00, 1876.00, 1861.00, 1872.48, 1883.78, 1895.81, 1920.96, 1918.81, 1862.81, 1853.06, 1808.22, 1802.39, 1800.22]
            self._v_before_sampling = pd.Series(data=x, name='VOLUME BEFORE SAMPLING (mL)')
            self._v_after_sampling = pd.Series(data=x, name='VOLUME AFTER SAMPLING (mL)')
            self._v_after_feeding = pd.Series(data=x, name='VOLUME AFTER FEEDING (mL)')
        ########################################################################

        # Pre Process Data DF
        self._pre_data = pd.concat([self._run_time_day,
                                    self._run_time_hour,
                                    self._v_before_sampling,
                                    self._v_after_sampling,
                                    # self._v_after_feeding,
                                    # self._feed_status,
                                    ], axis=1)
    # End Constructor
    def get_xv(self):
        """
        Get Viable Cell Concentration (x106 cells/mL)
        """
        return self._xv

    def get_xd(self):
        """
        Get Dead Cell Concentration (x106 cells/mL)
        """
        return self._xd

    def get_xt(self):
        """
        Get Total Cell Concentration (x106 cells/mL)
        """
        return self._xt

    def get_viability(self):
        """
        Get Viability (%)
        """
        return self._viability
    
    def get_osmolality(self):
        '''
        Get osmolality.
        '''
        return self._osmolality

    def get_oxygen_consumed(self):
        '''
        Get oxygen consumed.
        '''
        return self._oxygen_consumed

    def get_product_conc(self):
        """
        Get Product Concentration (mg/L)
        """
        return self._product_conc

    def get_pre_data(self):
        """
        Get pre process data.
        """
        return self._pre_data

    def get_feed_added(self):
        '''
        Get species feed added.
        '''
        return self._feed_added