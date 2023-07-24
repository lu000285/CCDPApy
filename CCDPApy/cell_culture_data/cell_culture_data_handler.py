import pandas as pd

from CCDPApy.file_handle import FileHandler
from CCDPApy.cell_culture_types.fed_batch.cell_line_data import FedBatchCellLineDataHandler
from CCDPApy.cell_culture_types.fed_batch.experiment_data import FedBatchExperimentHandler

class CellCultureDataHandler:
    '''
    '''
    def __init__(self, cell_culture_type) -> None:

        # Define cell line and experiment data handler
        if cell_culture_type=='fed-batch':
            self._cell_line_handler = FedBatchCellLineDataHandler
            self._experiment_handler = FedBatchExperimentHandler
            
        elif cell_culture_type=='perfusion':
            pass

        # file handler
        self._file_handler = FileHandler

    def load_data(self, file):
        '''load an excel file and return the dictionary.'''
        file_handler = self._file_handler(file=file)
        return file_handler.read()

    def get_cell_line_names(self):
        '''get cell line names.'''
        return self._cell_line_names