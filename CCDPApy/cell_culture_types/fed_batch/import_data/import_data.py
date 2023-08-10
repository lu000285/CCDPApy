import pandas as pd

from CCDPApy.helper import input_path

SHEET_NAME_1 = 'Cell Concentration'
SHEET_NAME_2 = 'Cumulative Cell Production'
SHEET_NAME_3 = 'Integral of Viable Cell'
SHEET_NAME_4 = 'Cell Growth Rate'
SHEET_NAME_5 = 'Concentration'
SHEET_NAME_6 = 'Cumulative Concentration'
SHEET_NAME_7 = 'SP Rate'
 
class ImportMixin:
    '''import processed data file.'''

    def import_data(self, file_name, sheet_name='Processed Data'):
        ''''''
        if not '.xlsx' in file_name:
            print('Invalid extension. Use .xlsx')
            return
        path = input_path(file_name=file_name)
        imported_data = pd.read_excel(io=path, sheet_name=sheet_name)

        # Rename columns
        new_columns = [col if 'Unnamed' not in col else '' for col in imported_data.columns]
        imported_data.columns = new_columns

        if self._processed_data.size==0:
            self._processed_data = imported_data
        else:
            self._processed_data = pd.concat([self._processed_data, imported_data], axis=0)