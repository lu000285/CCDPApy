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
    '''

    # Constructor
    def __init__(self, experiment_info, raw_data):
        '''
        Parameters
        ----------
        experiment_info : DataFrame
            The information of the experiment.
        raw_data : str : DataFrame
            The measured data of the experiment.
        '''

        # Experoment Infomation Members
        self._experiment_id = experiment_info.loc['Experiment ID'].get(1)
        self._experimenter_name = experiment_info.loc['Name'].get(1)
        self._cell_line_name = experiment_info.loc['Cell Line'].get(1)
        self._initial_volume = float(experiment_info.loc['Initial Volume (mL)'].get(1))

        # Experimental Variables
        self._sample_num = check_key(raw_data, 'SAMPLE #')
        #
        self._date = check_key(raw_data, 'DATE')
        self._time = check_key(raw_data, 'TIME')
        self._run_time_day = check_key(raw_data, 'Day')
        self._run_time_hour = check_key(raw_data, 'RUN TIME (HOURS)')
        #
        self._sample_volume = check_key(raw_data, 'SAMPLE VOLUME (mL)').fillna(0)
        self._feed_media_added = check_key(raw_data, 'FEED MEDIA ADDED (mL)').fillna(0)
        #
        self._glucose_feed_added = check_key(raw_data, 'GLUCOSE ADDED (mL)').fillna(0)
        self._glutamine_feed_added = check_key(raw_data, 'GLUTAMINE FEED ADDED (mL)').fillna(0)
        #
        self._base_added = check_key(raw_data, 'BASE ADDED (mL)').fillna(0)

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
        self._osmolaliry = check_key(raw_data, 'OSMOLALITY (mmol/kg)')
        self._product_conc = check_key(raw_data, 'IgG CONC. (mg/L)').fillna(0)

        # Have Calculated Cumulative Consumption/Production ?
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

        # Calc Run Time Mid
        self.mid_calc_runtime()

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


        self._pre_data = pd.concat([self._run_time_day,
                                    self._run_time_hour,
                                    self._v_before_sampling,
                                    self._v_after_sampling,
                                    # self._v_after_feeding,
                                    # self._feed_status,
                                    ], axis=1)
    # End Constructor


    def get_exp_id(self):
        """
        Get Experimant ID
        
        Parameters
        ----------

        Returns
        -------
        self._experiment_id : str
            Expeirment ID
        """
        return self._experiment_id

    def get_cl_name(self):
        """
        Get Cell Line Name
        
        Parameters
        ----------

        Returns
        -------
        self._cell_line_name : str
            Cell Line Name
        """
        return self._cell_line_name

    def get_init_v(self):
        """
        Get Initial Culture Volume
        
        Parameters
        ----------

        Returns
        -------
        self._initial_volume : float
            Initial Culture Volume
        """
        return self._initial_volume


    def get_experimenter(self):
        """
        Get the Name of Experimenter
        
        Parameters
        ----------

        Returns
        -------
        self._experimenter_name : str
            Name of Experimenter
        """
        return self._experimenter_name


    def get_pre_data(self):
        """
        Get Pre Process Data
        
        Parameters
        ----------

        Returns
        -------
        self._pre_data :
            Pre Process Data
        """
        return self._pre_data


    def get_v_before_samp(self):
        """
        Get Culture Volume Before Sampling
        
        Parameters
        ----------

        Returns
        -------
        self._v_before_sampling :
            Culture Volume Before Sampling
        """
        return self._v_before_sampling


    def get_v_after_samp(self):
        """
        Get Culture Volume After Sampling
        
        Parameters
        ----------

        Returns
        -------
        self._v_after_sampling :
            Culture Volume After Sampling
        """
        return self._v_after_sampling


    def get_v_after_feed(self):
        """
        Get Culture Volume After Feeding.
        
        Parameters
        ----------

        Returns
        -------
        self._v_after_feeding :
            Culture Volume After Feeding
        """
        return self._v_after_feeding

###########################################################################
