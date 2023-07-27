import pandas as pd

SHEET_NAME_1 = 'Cell Concentration'
SHEET_NAME_2 = 'Cumulative Cell Production'
SHEET_NAME_3 = 'Integral of Viable Cell'
SHEET_NAME_4 = 'Cell Growth Rate'
SHEET_NAME_5 = 'Concentration'
SHEET_NAME_6 = 'Cumulative Concentration'
SHEET_NAME_7 = 'SP Rate'
 
class ImportMixin:
    '''import processed data file.'''

    def import_data(self, file):
        ''''''
        
        data_sheets = pd.read_excel(io=file, sheet_name=None)

        cell_data = {}
        metabolite_data = {}

        cell_data['conc'] = data_sheets[SHEET_NAME_1]
        cell_data['cumulative'] = data_sheets[SHEET_NAME_2]
        cell_data['integral'] = data_sheets[SHEET_NAME_3]
        cell_data['growth_rate'] = data_sheets[SHEET_NAME_4]

        metabolite_data['conc'] = data_sheets[SHEET_NAME_5]
        metabolite_data['cumulative'] = data_sheets[SHEET_NAME_6]
        metabolite_data['sp_rate'] = data_sheets[SHEET_NAME_7]