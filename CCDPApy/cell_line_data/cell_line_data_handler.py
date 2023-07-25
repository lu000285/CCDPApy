from CCDPApy.Constants import CELL_LINE_COLUMN, ID_COLUMN
from CCDPApy.cell_culture_types.fed_batch.experiment_data import FedBatchExperimentHandler
from CCDPApy.cell_culture_types.perfusion.experiment_data.experiment_handler import PerfusionExperimentHandler
class CellLineDataHandler:
    '''
    '''
    def __init__(self, cell_line_name, data, cell_culture_type=None) -> None:
        '''
        '''
        # Define cell line and experiment data handler
        if cell_culture_type=='fed-batch':
            self._experiment_handler = FedBatchExperimentHandler
            
        elif cell_culture_type=='perfusion':
            self._experiment_handler = PerfusionExperimentHandler

        data = data['measured_data'].copy()
        mask = data[CELL_LINE_COLUMN]==cell_line_name
        data_masked = data[mask].copy()

        self._cell_line_name = cell_line_name
        self._mask = mask
        self._measured_data = data_masked
        self._experiment_names = list(data_masked[ID_COLUMN].unique())
    
    def get_experiment_names(self):
        '''get experiment names in the cell culture.'''
        return self._experiment_names
    
    def get_measured_data(self):
        '''get measured data.'''
        return self._measured_data
    
    @property
    def cell_line_name(self):
        return self._cell_line_name