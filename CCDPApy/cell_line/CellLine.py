import pandas as pd

from CCDPApy.helper import output_path
from ..plotting.PlotCellLineMixin import PlotMixin
from ..plotting.InteractivePlot import InteractivePlotMixin

class CellLine(PlotMixin, InteractivePlotMixin):
    def __init__(self):
        self._cell_line_list = []   # List of cell lines
        self._cell_line_dict = {}   # Dict of cell lines

    def add_bio_process(self, bio_process):
        '''
        Add BioProcess object to CellLine object.

        Parameters
        ----------
            bio_process : python object
                BioProcess object
        '''
        cl_name = bio_process.cell_line # cell line name
        exp_id = bio_process.id     # experiment id

        # if cl_name is not in the cell line list, append it.
        if cl_name not in self._cell_line_list:
            self._cell_line_list.append(cl_name)

        exp_dict = {}
        # if cell line dict already has at least one experimnt of the cell line name
        if (cl_name in self._cell_line_dict.keys()):
            exp_dict = self._cell_line_dict[cl_name]
            
        exp_dict[exp_id] = bio_process
        self._cell_line_dict[cl_name] = exp_dict

    def add_cell_line(self, cell_line):
        '''Add another cell line.'''
        cl_dict = cell_line.get_cell_line()
        self._cell_line_dict.update(cl_dict)
        self._cell_line_list.append(list(cl_dict.keys())[0])

    def get_cell_line_list(self):
        '''Retuern list of cell line names stored in CellLine class.
        '''
        return self._cell_line_list
        
    def get_cell_line(self, cell_line_name=None):
        '''
        Return dictionary of BioProcess object stored in CellLine class.

        Returns
        -------
            python dictionary
                {'cell line name': BioProcess object}
        '''
        if cell_line_name is None:
            return self._cell_line_dict
        else:
            return self._cell_line_dict[cell_line_name]

    def disp_cell_lines(self):
        '''Display Cell Line Name and Experiment ID stored in CellLine Class.
        '''
        for cell_line, bio_process in self._cell_line_dict.items():
            print(f'Cell Line: {cell_line}')
            for exp_id in bio_process.keys():
                print(f'    ID: {exp_id}')


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

    def get_plot_data(self) -> tuple:
        '''Return In-Process and Post-Process data for a plot.'''
        cell_line_lst = self._cell_line_list
        cell_line = self._cell_line_dict

        conc_df_list = []
        cumulative_conc_df_list = []
        sp_rate_df_list = []
        for cl_name in cell_line_lst:
            cl = cell_line[cl_name]
            for bio_process in cl.values():
                conc_df_list.append(bio_process.get_conc_df())
                cumulative_conc_df_list.append(bio_process.get_cumulative_conc_df())
                sp_rate_df_list.append(bio_process.get_sp_rate_df())

        conc_df = pd.concat(conc_df_list, axis=0).reset_index(drop=True)
        cumulative_conc_df = pd.concat(cumulative_conc_df_list, axis=0).reset_index(drop=True)
        sp_rate_df = pd.concat(sp_rate_df_list, axis=0).reset_index(drop=True)
        return conc_df, cumulative_conc_df, sp_rate_df
    
    def get_cell_plot_data(self) -> tuple:
        ''''''
        cell_line_lst = self._cell_line_list
        cell_line = self._cell_line_dict

        conc_df_list = []
        ivcc_df_list = []
        cumulative_conc_df_list = []
        sp_rate_df_list = []
        for cl_name in cell_line_lst:
            cl = cell_line[cl_name]
            for bio_process in cl.values():
                conc, ivcc, cumulative, rate = bio_process.get_cell_data_df()
                conc_df_list.append(conc)
                ivcc_df_list.append(ivcc)
                cumulative_conc_df_list.append(cumulative)
                sp_rate_df_list.append(rate)

        conc_df = pd.concat(conc_df_list, axis=0).reset_index(drop=True)
        ivcc_df = pd.concat(ivcc_df_list, axis=0).reset_index(drop=True)
        cumulative_conc_df = pd.concat(cumulative_conc_df_list, axis=0).reset_index(drop=True)
        sp_rate_df = pd.concat(sp_rate_df_list, axis=0).reset_index(drop=True)
        return conc_df, ivcc_df, cumulative_conc_df, sp_rate_df


    '''def get_plot_data(self):
        Return In-Process and Post-Process data for a plot.
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
        return pd.concat(df_list, axis=0).reset_index(drop=True)'''