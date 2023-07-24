import pandas as pd

from CCDPApy.cell_culture_data import CellCultureDataHandler
from CCDPApy.plotting.InteractivePlot import InteractivePlotMixin

from .GeterMixin import GetterMixin
from .constants import DATA_SHEET, FEED_SHEET, SEPARATE_FEED_SHEET, POLYNOMIAL_SHEET
from .constants import EXPERIMENT_DATA_COLUMN, CONC_BEFOROE_FEED_COLUMN, CONC_AFTER_FEED_COLUMN, MEASURED_CUMULATIVE_COLUMN
from .constants import CELL_LINE_COLUMN, ID_COLUMN, DATE_COLUMN

from CCDPApy.helper import split_df

class FedBatchCellCultureDataHandler(CellCultureDataHandler, GetterMixin, InteractivePlotMixin):
    ''''''
    def __init__(self, parameters) -> None:
        super().__init__(cell_culture_type='fed-batch')
        
        # Cell culture parameters
        param_dict = {}
        if isinstance(parameters, list):
            for param in parameters:
                param_dict[param.cell_line_name] = param
        else:
            param_dict[parameters.cell_line_name] = parameters
        self._param = param_dict

        # calss members to store processed data
        self._cell_data = {'conc': None,
                           'cumulative': None,
                           'integral': None,
                           'growth_rate': None}
        
        self._metabolite_data = {'conc': None,
                                 'cumulative': None,
                                 'sp_rate': None}


    def load_data(self, file, sheet_name=[DATA_SHEET, FEED_SHEET, SEPARATE_FEED_SHEET, POLYNOMIAL_SHEET]):
        '''load an excel file.'''
        sheets_dict = super().load_data(file=file)

        measured_data = sheets_dict[sheet_name[0]]
        feed_data = sheets_dict[sheet_name[1]]
        separate_feed_data = sheets_dict[sheet_name[2]]
        polynomial_degree = sheets_dict[sheet_name[3]]
        
        # change dtype at Cell Line and ID columns
        cols = [CELL_LINE_COLUMN, ID_COLUMN]
        feed_data[cols] = feed_data[cols].astype('string')
        separate_feed_data[cols] = separate_feed_data[cols].astype('string')
        polynomial_degree[cols] = polynomial_degree[cols].astype('string')
        
        # save
        # measured_data.iloc[1:, :] = measured_data.iloc[1:, :].sort_values(by=EXPERIMENT_DATA_COLUMN, kind='stable')
        self._data = measured_data#.reset_index(drop=True)
        self._feed_data = feed_data#.sort_values(by=DATE_COLUMN, kind='stable', ignore_index=True)
        self._separate_feed_data = separate_feed_data#.sort_values(by=DATE_COLUMN, kind='stable', ignore_index=True)
        self._polynomial_degree_data = polynomial_degree
        
        # pre-process
        self.preprocess_data()

    def preprocess_data(self, taerget_columns=[EXPERIMENT_DATA_COLUMN, CONC_BEFOROE_FEED_COLUMN, CONC_AFTER_FEED_COLUMN, CONC_AFTER_FEED_COLUMN, MEASURED_CUMULATIVE_COLUMN]):
        '''loaded data formatting.'''
        data_list = split_df(self._data, taerget_columns)
        data = data_list[0]
        data[[CELL_LINE_COLUMN, ID_COLUMN]] = data[[CELL_LINE_COLUMN, ID_COLUMN]].astype('string')
        self._data = data
        self._conc_before_feed_data = data_list[1]
        self._conc_after_feed_data = data_list[2]
        self._measured_cumulative_data = data_list[3].astype('float64')
        self._cell_line_names = list(self._data[CELL_LINE_COLUMN].unique())

        # Store all data in dict
        data = {'measured_data': self._data,
                'conc_before_feed': self._conc_before_feed_data,
                'conc_after_feed': self._conc_after_feed_data,
                'measured_cumulative_conc': self._measured_cumulative_data,
                'feed_conc': self._feed_data,
                'separate_feed_conc': self._separate_feed_data,
                'polynomial_degree_data': self._polynomial_degree_data}
        self._data_set = data

    def perform_data_process(self):
        '''in-prcessing data for all cell lines.'''
        cell_line_names = self.get_cell_line_names()
        data_set = self.get_all_data()

        cell_lines = [name for name in cell_line_names if name in self._param.keys()]

        cell_line_handles = {}
        for cell_line in cell_lines:
            param = self._param[cell_line]
            # call cell line data handler
            cell_line_data_handler = self._cell_line_handler(
                cell_line_name=cell_line,
                data=data_set,
                use_feed_conc=param.use_feed_conc,
                use_conc_after_feed=param.use_conc_after_feed
            )
            # in-processing
            cell_line_data_handler.in_process()

            # post-porcessing-polynomial regression
            if param.polynomial:
                cell_line_data_handler.polynomial()

            # post-processing-rolling window polynomial regression
            if param.rolling_window_polynomial:
                deg = param.rolling_polynomial_degree
                window = param.rolling_polynomial_window
                cell_line_data_handler.rolling_window_polynomial(deg=deg, window=window)

            # store handlers
            cell_line_handles[cell_line] = cell_line_data_handler
        self._cell_line_handles = cell_line_handles

        # store data
        self.store_data()

    def store_data(self):
        '''store data for the cell and metabolite from cell line data handlers.'''
        cell_line_handles = self._cell_line_handles

        cell_conc, cell_cumulative, cell_integral, cell_growth_rate = [], [], [], []
        conc, cumulative, sp_rate = [], [], []
        for cell_line_handler in cell_line_handles.values():
            # cell data
            cell_data = cell_line_handler.get_cell_data()
            cell_conc.append(cell_data['conc'])
            cell_cumulative.append(cell_data['cumulative'])
            cell_integral.append(cell_data['integral'])
            cell_growth_rate.append(cell_data['growth_rate'])

            # metabolite data
            metabolite_data = cell_line_handler.get_metabolite_data()
            conc.append(metabolite_data['conc'])
            cumulative.append(metabolite_data['cumulative'])
            sp_rate.append(metabolite_data['sp_rate'])

        # concat
        cell_conc =  pd.concat(cell_conc, axis=0)
        cell_cumulative = pd.concat(cell_cumulative, axis=0)
        cell_integral = pd.concat(cell_integral, axis=0)
        cell_growth_rate = pd.concat(cell_growth_rate, axis=0)
        conc = pd.concat(conc, axis=0)
        cumulative = pd.concat(cumulative, axis=0)
        sp_rate = pd.concat(sp_rate, axis=0)

        # store data
        self._cell_data['conc'] =  cell_conc
        self._cell_data['cumulative'] = cell_cumulative
        self._cell_data['integral'] = cell_integral
        self._cell_data['growth_rate'] = cell_growth_rate
        self._metabolite_data['conc'] = conc
        self._metabolite_data['cumulative'] = cumulative
        self._metabolite_data['sp_rate'] = sp_rate

    def get_cell_line_handles(self, cell_line_name=None):
        ''''''
        if cell_line_name:
            return self._cell_line_handles[cell_line_name]
        else :
            return self._cell_line_handles
    
    def get_experiment_ids(self):
        ''''''
        id_list = []
        for cell_line_handler in self._cell_line_handles.values():
            id_list += list(cell_line_handler.get_experiment_handle())
        return id_list
    