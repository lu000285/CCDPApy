import pandas as pd

from ..helper_func.helper_func import output_path
from ..plotting.PlotCellLineMixin import PlotMixin

###########################################################################
# Cell Line Class
###########################################################################
class CellLine(PlotMixin):
    def __init__(self):
        self._cell_line_list = []        # List of cell lines
        self._cell_line_dict = {}   # Dict of cell lines

    # Add Experiment
    def add_bio_process(self, bio_process):
        cl_name = bio_process.get_cell_line() # cell line name
        exp_id = bio_process.get_exp_id()     # experiment id

        # if cl_name is not in the cell line list, append it.
        if cl_name not in self._cell_line_list:
            self._cell_line_list.append(cl_name)

        exp_dict = {}
        # if cell line dict already has at least one experimnt of the cell line name
        if (cl_name in self._cell_line_dict.keys()):
            exp_dict = self._cell_line_dict[cl_name]
            
        exp_dict[exp_id] = bio_process
        self._cell_line_dict[cl_name] = exp_dict

    # Get Cell Line list
    def get_cell_line_list(self):
        return self._cell_line_list
        
    # Get Cell Line Dict
    def get_cell_line(self, cl_name):
        return self._cell_line_dict[cl_name]

    # Display
    def disp_cell_lines(self):
        for cell_line, bio_process in self._cell_line_dict.items():
            print(f'Cell Line: {cell_line}')

            for i, exp_id in enumerate(bio_process.keys()):
                print(f'Experiment {i+1}: {exp_id}')
            print('\n')


    # Save Excell
    def save_excel(self, cell_line, file_name):
        if '.xlsx' not in file_name:
            file_name += '.xlsx'
        file_path = output_path(file_name=file_name)

        with pd.ExcelWriter(file_path) as writer:
            for cl in self._cell_line_dict[cell_line].values():
                sheet = cl.get_exp_id()
                cl.get_bioprocess_df().to_excel(writer, sheet_name=sheet, index=False)
            print(file_name + ' saved')



    # Save Excell for Rolling Regression
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