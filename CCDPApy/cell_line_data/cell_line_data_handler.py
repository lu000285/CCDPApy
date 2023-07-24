from CCDPApy.Constants import CELL_LINE_COLUMN, ID_COLUMN

class CellLineDataHandler:
    '''
    '''
    def __init__(self, cell_line_name, data, cell_culture_type=None) -> None:
        '''
        '''
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