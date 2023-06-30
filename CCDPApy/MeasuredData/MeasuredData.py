# Python Libraries
import pandas as pd
import numpy as np

# My Libraries
from ..helper_func.helper_func import check_key
from ..helper_func.helper_func import input_path, get_unit
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
        # Read and get DataFrame for measured data, and experimtent and separate feed information.
        data_df, exp_info, feed_info = read_excel(file_name=file_name,
                                                        measurement_sheet=measurement_sheet,
                                                        feed_sheet=feed_sheet)
        self.exp_info = exp_info
        
        # Experiment information
        self._initial_volume = exp_info['initial_volume'].to_numpy()[0]
        self._unit = exp_info['unit'].to_string(index=False)

        # Measurement information
        c_before_feed_df, c_after_feed_df, feed_c_df, cum_c_df, param_df = data_df
        self.c_before_feed_df = c_before_feed_df
        self.c_after_feed_df = c_after_feed_df
        self.feed_c_df = feed_c_df
        self.cum_c_df = cum_c_df
        self.param_df = param_df

        # Separate feed
        self.feed_list, self.feed_data = separate_feed(feed_data=feed_info)

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
    if 'date' in feed_data and 'time' in feed_data:
        feed_data = feed_data.drop(['samples', 'date', 'time'], axis=1)

    if 'day' in feed_data and 'run_time_(hrs)' in feed_data:
        feed_data = feed_data.drop(['samples', 'day', 'run_time_(hrs)'], axis=1)
    feed_list = [f.upper().replace('_ADDED_(ML)', '') for f in feed_data.columns]

    return (feed_list, feed_data.fillna(0))

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
            Pandas DataFrame of the measured data, experiment information, and separeate feed informaiton.
    '''
    # Get File Path to input_files directory.
    file_path = input_path(file_name=file_name)
    # Read Measured Data
    measured_data = pd.read_excel(io=file_path, sheet_name=measurement_sheet, header=5)
    # Split parameters into concentrations and others
    for i, col in enumerate(measured_data.columns):
        if "IgG CONC. (mg/L)" in col:
            split_idx = i
            break
        else:
            split_idx = 18
    param_index = measured_data.columns[:split_idx+1]
    conc_index = measured_data.columns[split_idx+1:]
    # Separate measured data into concetnration data and other parameter data
    # Concentrations before feed
    c_before_feed_indices = [idx for idx, col in enumerate(conc_index) if 'CONC' in col and not '.1' in col and not 'FEED' in col]
    c_before_feed_df = measured_data[conc_index[c_before_feed_indices]].copy()
    c_before_feed_df.columns = [col.replace(' CONC. ', '_') for col in c_before_feed_df.columns]
    # Concentrations after feed
    c_after_feed_indices = [idx for idx, col in enumerate(conc_index) if 'CONC' in col and '.1' in col]
    c_after_feed_df = measured_data[conc_index[c_after_feed_indices]].copy()
    c_after_feed_df.columns = [col.replace(' CONC. ', '_').replace('.1', '') for col in c_after_feed_df.columns]
    # Feed concentrations
    feed_c_indices = [idx for idx, col in enumerate(conc_index) if 'FEED' in col and 'CONC' in col]
    feed_c_df = measured_data[conc_index[feed_c_indices]].copy()
    feed_c_df.columns = [col.replace(' CONC. ', '_').replace('FEED ', '') for col in feed_c_df.columns]
    # Cumulative concentrations
    cum_c_indices = [idx for idx, col in enumerate(conc_index) if 'CUM' in col]
    cum_c_df = measured_data[conc_index[cum_c_indices]].copy()
    cum_c_df.columns = [col.replace('CUM ', '').replace(' ', '_') for col in cum_c_df.columns]
    # Other parameter data
    param_df = measured_data[param_index].copy()
    param_df = param_df.rename(columns={'SAMPLE #': 'samples',
                                        'SAMPLE VOLUME (mL)': 'sample_volume_(mL)',
                                        'VOLUME AFTER SAMPLING (mL)': 'volume_after_sampling_(mL)',
                                        'FEED MEDIA ADDED (mL)': 'feed_media_added_(mL)', 
                                        'BASE ADDED (mL)': 'base_added_(mL)',
                                        'VIABLE CELL CONC. XV (x106 cells/mL)': 'viable_cell_conc_(10^6_cells/mL)',
                                        'DEAD CELL CONC. Xd (x106 cells/mL)': 'dead_cell_conc_(10^6_cells/mL)',
                                        'TOTAL CELL CONC. Xt (x106 cells/mL)': 'total_cell_conc_(10^6_cells/mL)',
                                        'VIABILITY (%)': 'viability_(%)',
                                        'pH': 'ph',
                                        'DO (%)': 'do_(%)',
                                        'OUR (mmol/L/hr)': 'our_(mmol/L/hr)', 
                                        'SP. OXYGEN CONSUMPTION RATE (mmol/109cell/hr)': 'sp_oxygen_consumption_rate_(mmol/10^9_cells/hr)',
                                        'OXYGEN CONSUMED (mmol/L)': 'oxygen_consumed_(mmol/L)',
                                        'OPTICAL DENSITY': 'optical_density',
                                        'OSMOLALITY (mmol/kg)': 'osmolality_(mmol/kg)',
                                        'IgG CONC. (mg/L)': 'IgG_(mg/L)'})
    if 'DATE' in param_df:
        param_df = param_df.rename(columns={'DATE': 'date'})
    if 'TIME' in param_df:
        param_df = param_df.rename(columns={'TIME': 'time'})
    if 'Day' in param_df:
        param_df = param_df.rename(columns={'Day': 'run_time_(days)'})
    if 'RUN TIME (HOURS)' in param_df:
        param_df = param_df.rename(columns={'RUN TIME (HOURS)': 'run_time_(hrs)'})
    
    # Read Experiment Info
    exp_info = pd.read_excel(io=file_path, sheet_name=measurement_sheet, nrows=4, usecols=[0, 1], header=None, index_col=0).T
    for col in exp_info.columns:
        if "Volume" in col:
            init_vol_org = col
            unit = get_unit(col)
    exp_info = exp_info.rename(columns={'Cell Line': 'cell_line', 
                                        'Experiment ID': 'exp_id', 
                                        'Name': 'name',
                                        init_vol_org: 'initial_volume'})
    exp_info['unit'] = unit
    exp_info['initial_volume'] = exp_info['initial_volume'].astype('float64')

    # Read Separate Feed Info
    feed_info = pd.read_excel(io=file_path, sheet_name=feed_sheet).rename(columns={'SAMPLE #': 'samples'})
    if 'DATE' in feed_info:
        feed_info = feed_info.rename(columns={'DATE': 'date'})
    if 'TIME' in feed_info:
        feed_info = feed_info.rename(columns={'TIME': 'time'})
    if 'Day' in feed_info:
        feed_info = feed_info.rename(columns={'Day': 'run_time_(days)'})
    if 'RUN TIME (HOURS)' in feed_info:
        feed_info = feed_info.rename(columns={'RUN TIME (HOURS)': 'run_time_(hrs)'})
    feed_info.columns = [col.replace(" ", "_") for col in feed_info.columns]

    # print(f'{file_name} imported.')

    return (c_before_feed_df, c_after_feed_df, feed_c_df, cum_c_df, param_df), exp_info, feed_info
