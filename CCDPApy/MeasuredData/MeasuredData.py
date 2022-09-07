# Python Libraries
import pandas as pd
import numpy as np

# My Libraries
from ..helper_func.helper_func import check_key
from ..helper_func.helper_func import input_path
from .GetterMixin import GetterMixin
from ..pre_process.PreProcessMixin import PreProcessMixn

###########################################################################
# Measured Data Class
###########################################################################
class MeasuredData(GetterMixin, PreProcessMixn):
    '''
    Store measured data in a bioprocess experiment.
    
    Attributes
    ----------
    experiment_info : pandas.DataFrame
        The information of the experiment.
    measured_data : pandas.DataFrame
        The measured data of the experiment.
    feed_data : pandas.DataFrame
        Separate feed information.
    '''

    # Constructor
    def __init__(self, file_name, measurement_sheet, feed_sheet):
        '''
        Parameters
        ----------
        experiment_info : pandas.DataFrame
            Experimental information.
        measured_data : pandas.DataFrame
            Measured data of the experiment.
        feed_data : pandas.DataFrame
            Separate feed information.
        '''
        # Read adn get DataFrame for measured data, and experimtent and separate feed information.
        measured_data, exp_info, feed_info = read_excel(file_name=file_name,
                                                        measurement_sheet=measurement_sheet,
                                                        feed_sheet=feed_sheet)
        self.data_df = measured_data # measured data DataFrame

        # Experoment Infomation Members
        self.exp_id = exp_info.loc['Experiment ID'].get(1)
        self.exp_name = exp_info.loc['Name'].get(1)
        self.cell_line_name = exp_info.loc['Cell Line'].get(1)
        self.initial_v = float(exp_info.loc['Initial Volume (mL)'].get(1))

        # Experimental Data
        self.sample_num = check_key(measured_data, 'SAMPLE #')  # Sample Number

        # Time
        self.date = check_key(measured_data, 'DATE')
        self.time = check_key(measured_data, 'TIME')
        self.run_time_day = check_key(measured_data, 'Day')
        self.run_time_hour = check_key(measured_data, 'RUN TIME (HOURS)')

        # Culture and Feed Media Volume
        self.base_added = check_key(measured_data, 'BASE ADDED (mL)').fillna(0)
        self.sample_volume = check_key(measured_data, 'SAMPLE VOLUME (mL)').fillna(0)
        self.feed_media_added = check_key(measured_data, 'FEED MEDIA ADDED (mL)').fillna(0)

        # Experimental Cell, Oxygen, and IgG/Product Data
        self.xv = check_key(measured_data, 'VIABLE CELL CONC. XV (x106 cells/mL)').fillna(0)  # xv: Viable Cell Concentration
        self.xd = check_key(measured_data, 'DEAD CELL CONC. Xd (x106 cells/mL)').fillna(0)    # xd: Dead Cell Concentraion
        self.xt = check_key(measured_data, 'TOTAL CELL CONC. Xt (x106 cells/mL)').fillna(0)   # xt: Total Cell Concentraion
        self.viability = check_key(measured_data, 'VIABILITY (%)')
        self.pH = check_key(measured_data, 'pH')
        self.do = check_key(measured_data, 'DO (%)')
        self.our = check_key(measured_data, 'OUR (mmol/L/hr)').fillna(0)
        self.oxygen_consumption_rate = check_key(measured_data, 'SP. OXYGEN CONSUMPTION RATE (mmol/109cell/hr)').fillna(0)
        self.oxygen_consumed = check_key(measured_data, 'OXYGEN CONSUMED (mmol/L)').fillna(0)
        self.optical_density = check_key(measured_data, 'OPTICAL DENSITY')
        self.osmolality = check_key(measured_data, 'OSMOLALITY (mmol/kg)')
        self.product_conc = check_key(measured_data, 'IgG CONC. (mg/L)').fillna(0)

        # Separate feed
        self.feed_list, self.feed_data = separate_feed(feed_data=feed_info)

        # Variables Used in In Process
        n = len(self.sample_num) # Number of Samples        
        self.v_before_sampling = pd.Series(data=[0.0] * n, name='VOLUME BEFORE SAMPLING (mL)')
        self.v_after_sampling = pd.Series(data=[0.0] * n, name='VOLUME AFTER SAMPLING (mL)')
        self.v_after_feeding = pd.Series(data=[0.0] * n, name='VOLUME AFTER FEEDING (mL)')
        #self.feed_status = pd.Series(data=np.nan * n, name='Feed Status')

        # For CL3
        ########################################################################
        if self.cell_line_name=='Merck':
            x = [1935.00, 1920.00, 1905.00, 1876.00, 1861.00, 1872.48, 1883.78, 1895.81, 1920.96, 1918.81, 1862.81, 1853.06, 1808.22, 1802.39, 1800.22]
            self.v_before_sampling = pd.Series(data=x, name='VOLUME BEFORE SAMPLING (mL)')
            self.v_after_sampling = pd.Series(data=x, name='VOLUME AFTER SAMPLING (mL)')
            self.v_after_feeding = pd.Series(data=x, name='VOLUME AFTER FEEDING (mL)')
        ########################################################################

        # Pre Process Data DF
        self.pre_data = pd.DataFrame()
 
    # End Constructor


def separate_feed(feed_data):
    '''
    Check separate feed information.

    Parameters
    ----------
        feed_data : pandas.DataFrame
            separate feed information.
        feed_list : list of str
            list of separate feed name.

    Returns
    -------
        feed_data : pandas.DataFrame
        feed_list : list of str
    '''
    try:
        feed_data = feed_data.drop(['SAMPLE #', 'DATE', 'TIME'], axis=1)
    except:
        feed_data = feed_data.drop(['SAMPLE #', 'Day', 'RUN TIME (HOURS)'], axis=1)
    feed_list = [f.upper().replace(' ADDED (ML)', '') for f in feed_data.columns]
    return (feed_list, feed_data)

def read_excel(file_name, measurement_sheet, feed_sheet):
    '''
    Read Excel file and get measured data DataFrame,
    experiment information DataFrame, and feed information DataFrame.

    Parameters
    ----------
        file_name : str
            file name.
    Returns
    -------
        (measured_data, exp_info, feed_info) : python tupple
            DataFrame for measured data, experiment information, and separeate feed informaiton.
    '''
    # Get File Path to input_files directory.
    file_path = input_path(file_name=file_name)
    # Read Measured Data
    measured_data = pd.read_excel(io=file_path, sheet_name=measurement_sheet, header=5)
    # Read Experiment Info
    exp_info = pd.read_excel(io=file_path, sheet_name=measurement_sheet, nrows=4, usecols=[0, 1], header=None, index_col=0)
    # Read Separate Feed Info
    feed_info = pd.read_excel(io=file_path, sheet_name=feed_sheet)
    print(f'{file_name} imported.')

    return (measured_data, exp_info, feed_info)
