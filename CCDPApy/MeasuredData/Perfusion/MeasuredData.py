import pandas as pd
import numpy as np

from CCDPApy.helper_func.helper_func import input_path

target_columns = ['Experiment Information',
                  'Experimental Data', 
                  'Concentration',
                  'Feed Concentration']

class MeasuredData():
    '''
    '''
    def __init__(self, file_name) -> None:
        df = pd.read_excel(input_path(file_name=file_name))
        df_list = split_df(df)
        exp_df = df_list[0]
        param_df = df_list[1]
        conc_df = df_list[2]
        feed_df = df_list[3]

        self._exp_df = exp_df
        self._param_df = param_df
        self._conc_df = conc_df
        self._feed_df = feed_df

    @property
    def get_exp_df(self):
        ''''''
        return self._exp_df
    
    @property
    def get_param_df(self):
        ''''''
        return self._param_df
    
    @property
    def get_conc_df(self):
        ''''''
        return self._conc_df
    
    @property
    def get_feed_df(self):
        ''''''
        return self._feed_df

def split_df(df):
    '''
    '''
    global target_columns
    indices = [i for i, col in enumerate(df.columns) if col in target_columns]
    indices.append(df.shape[1])
    
    df_list = []
    for i in range(1, len(indices)):
        temp = df.iloc[1:, indices[i-1]:indices[i]]
        temp.set_axis(df.iloc[0, indices[i-1]:indices[i]], axis=1, inplace=True)
        df_list.append(temp)
    return df_list