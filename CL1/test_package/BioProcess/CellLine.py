import pandas as pd
from ..helper_func.helper_func import output_path

###########################################################################
# Cell Line Class
###########################################################################
class CellLine:
    def __init__(self, name):
        self._cell_line_name = name
        self._cell_line = []    # List of cell lines

    # Add Experiment
    def add_cell_line(self, bio_process):
        self._cell_line.append(bio_process)

    # Display
    def disp_cell_lines(self):
        print(f'Cell Line: {self._cell_line_name}')
        print(f'Number of Lines: {len(self._cell_line)}')
        for i, cl in enumerate(self._cell_line):
            print(f'Experiment {i}:')
            cl.disp_experiment()

    # Save Excell
    def save_excel(self, file_name):
        if '.xlsx' not in file_name:
            file_name += '.xlsx'
        file_path = output_path(file_name=file_name)

        with pd.ExcelWriter(file_path) as writer:
            print(file_name + ' saving...')
            for cl in self._cell_line:
                sheet = cl.get_exp_id()
                cl.get_bioprocess_df().to_excel(writer, sheet_name=sheet, index=False)
            print(file_name + ' saved')

    # Save Excell for Rolling REgression
    def save_excel_rolling_reg(self, file_name):
        if '.xlsx' not in file_name:
            file_name += '.xlsx'
        file_path = output_path(file_name=file_name)

        with pd.ExcelWriter(file_path) as writer:
            print(file_name + ' saving...')
            for cl in self._cell_line:
                sheet = cl.get_exp_id()
                cl.get_post_rollpolyreg().to_excel(writer, sheet_name=sheet, index=False)
            print(file_name + ' saved')

###########################################################################