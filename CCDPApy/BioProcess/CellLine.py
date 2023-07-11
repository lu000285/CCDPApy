import pandas as pd

from ..helper_func.helper_func import output_path
from ..plotting.PlotCellLineMixin import PlotMixin
from ..plotting.InteractivePlot import InteractivePlotMixin

###########################################################################
# Cell Line Class
###########################################################################
class CellLine(PlotMixin, InteractivePlotMixin):
    def __init__(self):
        self._cell_line_list = []   # List of cell lines
        self._cell_line_dict = {}   # Dict of cell lines

    # Add Experiment
    def add_bio_process(self, bio_process):
        '''
        Add BioProcess object to CellLine object.

        Parameters
        ----------
            bio_process : python object
                BioProcess object
        '''
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

    def get_cell_line_list(self):
        '''Retuern list of cell line names stored in CellLine class.
        '''
        return self._cell_line_list
        
    def get_cell_line(self, cl_name):
        '''
        Return dictionary of BioProcess object stored in CellLine class.

        Returns
        -------
            python dictionary
                {'cell line name': BioProcess object}
        '''
        return self._cell_line_dict[cl_name]

    def disp_cell_lines(self):
        '''Display Cell Line Name and Experiment ID stored in CellLine Class.
        '''
        for cell_line, bio_process in self._cell_line_dict.items():
            print(f'Cell Line: {cell_line}')

            for i, exp_id in enumerate(bio_process.keys()):
                print(f'Experiment {i+1}: {exp_id}')


    def save_excel(self, cell_line, file_name):
        '''
        Save each bioprocess data in the same cell line as an Excel file.
        Please include '.xlsx'.
        Do not include rolling regression data. To save the rolling regression data,
        use save_excel_rollreg method. 

        Parameters
        ----------
        cell_line : str
            Cell Line name.
        file_name : str
            File name.
            Please include '.xlsx'.
        '''
        if '.xlsx' not in file_name:
            file_name += '.xlsx'
        file_path = output_path(file_name=file_name)

        with pd.ExcelWriter(file_path) as writer:
            for bio_process in self._cell_line_dict[cell_line].values():
                sheet = bio_process.get_exp_id()
                bio_process.get_bioprocess_df().to_excel(writer, sheet_name=sheet, index=False)
            print(file_name + ' saved')


    # Save Excell for Rolling Regression
    def save_excel_rollreg(self, cell_line, file_name):
        '''
        Save each rolling regression data in the same cell line as an Excel file.
        Please include '.xlsx'.
        Do not include other bioprocess data. To save other data,
        use save_excel method.

        Parameters
        ----------
        cell_line : str
            Cell Line name.
        file_name : str
            File name.
            Please include '.xlsx'.
        '''
        if '.xlsx' not in file_name:
            file_name += '.xlsx'
        file_path = output_path(file_name=file_name)

        with pd.ExcelWriter(file_path) as writer:
            for cl in self._cell_line_dict[cell_line].values():
                sheet = cl.get_exp_id()
                cl.get_process_data('rollreg').to_excel(writer, sheet_name=sheet, index=False)
            print(file_name + ' saved')

    def get_plot_data(self):
        '''Return In-Process and Post-Process data for a plot.'''
        df_list = []
        cell_line_lst = self._cell_line_list
        cell_line = self._cell_line_dict

        for cl_name in cell_line_lst:
            cl = cell_line[cl_name]
            for bio_process in cl.values():
                df1 = bio_process.get_in_process_data()
                df2 = bio_process.get_post_process_data()
                df_list.append(df1)
                df_list.append(df2)
        return pd.concat(df_list, axis=0).reset_index(drop=True)