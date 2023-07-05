import pandas as pd
import numpy as np

from CCDPApy.MeasuredData.Perfusion.MeasuredData import MeasuredData
from CCDPApy.helper_func.helper_func import split_name_unit
from CCDPApy.Species.Perfusion.Cell import Cell
from CCDPApy.Species.Perfusion.Metabolite import Metabolite
from CCDPApy.Species.Perfusion.Variables import metabolite_dict
from .GetterMixin import GetterMixin
from CCDPApy.in_process.Perfusion.InProcessMixin import InProcessMixin as InProcess
from CCDPApy.post_process.Perfusion.polynomial.PolynomialMixin import PolynomialMixin as Polynomial

param_columns = ['time', 
                 'culture_volume', 
                 'flowrate',
                 'viable_cell_concentration', 
                 'dead_cell_concentration', 
                 'total_cell_concentration']

class BioProcess(GetterMixin, InProcess, Polynomial):
    '''
    '''
    def __init__(self, file_name, **kwargs) -> None:
        '''
        '''
        md = MeasuredData(file_name=file_name)
        exp_df = md.get_exp_df
        param_df = md.get_param_df
        conc_df = md.get_conc_df
        feed_df = md.get_feed_df

        # Global variables
        global param_columns

        # Create column indces
        col_indices = create_col_indices(param_df)
        conc_col_indices = create_col_indices(conc_df)
        feed_col_indices = create_col_indices(feed_df)

        # Work with the parameters        
        param_df_dict = create_df_dict(param_df, param_columns, col_indices)
        run_time = param_df_dict['time']
        culture_volume = param_df_dict['culture_volume']
        flow_rate = param_df_dict['flowrate']
        viable_cell = param_df_dict['viable_cell_concentration']
        dead_cell = param_df_dict['dead_cell_concentration']
        total_cell = param_df_dict['total_cell_concentration']

        # Species object dictionary
        spc_dict = {}
        feed_list = []

        # Create cell object
        cell = Cell(run_time, culture_volume, flow_rate, viable_cell, dead_cell, total_cell)
        spc_dict['cell'] = cell

        # Create metabolite object
        for name, val in conc_col_indices.items():
            conc = conc_df.iloc[:, val['index']].copy().to_frame(name='value')
            conc['unit'] = val['unit']
            conc.index.name = 'conentration'

            # Check feed concentration
            if feed_col_indices.get(name):
                val = feed_col_indices[name]
                feed = feed_df.iloc[:, val['index']]
                if feed.any():
                    feed = feed.copy().to_frame(name='value')
                    feed_list.append(metabolite_dict.get(name.capitalize()))
                else:
                    feed = feed.copy().to_frame(name='value').fillna(0)
                feed['unit'] = val['unit']
            else:
                feed = run_time.copy()
                feed['value'] = 0.0
                feed['unit'] = np.nan
            feed.index.name = 'feed_concentration'

            spc_dict[name] = Metabolite(name, run_time, culture_volume, flow_rate, conc, feed, viable_cell)

        # Store variables
        self._cell_line = exp_df['Cell Line'].iat[0]
        self._run_id = exp_df['Experimental ID'].iat[0]
        self._experimenter = exp_df['Name'].iat[0]
        self._exp_df = exp_df
        self._species = spc_dict
        self._feed_list = feed_list

    def __repr__(self) -> str:
        species = [s.get_abbr for s in self._species.values()]
        return "\n".join([
            f'Cell Line:     {self._cell_line}',
            f'Run ID:        {self._run_id}',
            f'Experimenter   {self._experimenter}',
            f'Species List   {species}',
            f'Feed List      {self._feed_list}',
        ])


def create_col_indices(df):
    '''Create the dictionary of column indices and units.
    '''
    column_indices = {}
    for i, col in enumerate(df.columns):
        name, unit = split_name_unit(col)
        key = name.lower().replace(' ', '_')
        column_indices[key] = {'index': i, 'unit': unit}
    return column_indices

def create_df_dict(df, columns, col_indices):
    '''
    '''
    df_dict = {}
    for col_name in columns:
        index = col_indices[col_name]['index']
        unit = col_indices[col_name]['unit']
        temp = df.iloc[:, index].copy().to_frame(name='value').astype('float')
        temp['unit'] = unit
        temp.index.name = col_name
        df_dict[col_name] = temp
    return df_dict
