import pandas as pd

from CCDPApy.Constants import CELL_LINE_COLUMN, ID_COLUMN, DATE_COLUMN, RUN_TIME_DAY_COLUMN, RUN_TIME_HOUR_COLUMN

class ExperimentDataHandler:
    '''
    '''
    def __init__(self, cell_line_name, cell_line_id, data, cell_culture_type=None) -> None:
        '''
        '''
        data = data['measured_data'].copy()
        mask = (data[CELL_LINE_COLUMN]==cell_line_name) & (data[ID_COLUMN]==cell_line_id)
        data_masked = data[mask].copy()

        self._cell_culture_name = cell_line_name
        self._cell_line_id = cell_line_id
        self._mask = mask
        self._measured_data = data_masked.reset_index(drop=True)

    def _preprocess(self):
        '''data pre-processing.'''
        self._calculate_run_time()
    
    def _calculate_run_time(self):
        '''calcularate run time (day) and (hr).'''
        date = self._measured_data[DATE_COLUMN]
        date_time = pd.to_datetime(date)
        time_diff = date_time - date_time.iat[0]
        
        run_time_hour = time_diff.dt.total_seconds() / 3600.0
        run_time_day = time_diff.dt.days
        run_time = pd.DataFrame(data={RUN_TIME_DAY_COLUMN: run_time_day,
                                      RUN_TIME_HOUR_COLUMN: run_time_hour})
        self._run_time = run_time
    
    def get_measured_data(self):
        '''get measured data.'''
        return self._measured_data
    
    def get_species(self, species='all'):
        '''Return species object.
        '''
        spc = self._spc_dict
        key = species.lower()
        if key=='all':
            return spc
        elif key in spc.keys() or key=='igg':
            return spc[key]
        else:
            print("Wrong species name. Please check below.")
            print(spc.keys())
    
    @property
    def cell_line_name(self):
        return self._cell_culture_name
    
    @property
    def cell_line_id(self):
        return self._cell_line_id
    
    @property
    def run_time(self):
        return self._run_time