# Python Libraries
import pandas as pd
import matplotlib.pyplot as plt

# My Libraries
from ..helper_func.helper_func import output_path
from ..helper_func.helper_func import input_path
from .GetterMixin import GetterMixin
from .SetterMixin import SetterMixin
from .DispMixin import DispMixin

###########################################################################
# Cell Bioprocess Class
###########################################################################
class BioProcess(GetterMixin, SetterMixin, DispMixin):
    def __init__(self, experiment_info, measured_data):
        # Measured Data DF
        self._exp_info = experiment_info
        self._measured_data = measured_data

        # Poly. Reg. Order DF
        self._polyorder_df = None

        # Experoment Infomation Members
        self._experiment_id = experiment_info.loc['Experiment ID'].get(1)
        self._experimenter_name = experiment_info.loc['Name'].get(1)
        self._cell_line_name = experiment_info.loc['Cell Line'].get(1)
        self._initial_volume = experiment_info.loc['Initial Volume (mL)'].get(1)

        # Cell Line Name and Exp ID Column
        self._expID_col = pd.Series(data=[self._experiment_id] * len(measured_data), name='Experiment ID')
        self._cl_col = pd.Series(data=[self._cell_line_name] * len(measured_data), name='Cell Line')

        # Class Members
        self._cell = None               # Cell Object
        self._oxygen = None             # Oxygen Object
        self._igg = None                # IgG Object

        self._original_aa_list = ['ALANINE', 'ARGININE', 'ASPARAGINE', 'ASPARTATE', 'CYSTINE',
                                  'GLUCOSE', 'GLUTAMINE', 'GLUTAMATE', 'GLYCINE', 'HISTIDINE',
                                  'ISOLEUCINE', 'LACTATE', 'LEUCINE','LYSINE', 'METHIONINE',
                                  'NH3', 'PHENYLALANINE', 'PROLINE', 'SERINE',
                                  'THREONINE','TRYPTOPHAN', 'TYROSINE', 'VALINE', 'ETHANOLAMINE']
                                  
        self._aa_list = None            # Metsbolite List
        self._aa_dict = None            # Metsbolite Dictionary = {'name': Metabolite obj}
        self._aa_df = None              # Metsbolite Cumulative DF
        self._aa_conc_df = None         # Metabolite Conc DF
        self._conc_after_feed_df = None # Metabolite Conc After Feed DF
        
        self._pre_process = None        # Pre Process DF
        self._in_process = None         # In Process DF
        self._post_twopt = None         # Post Process-Two Point Calc. DF
        self._post_polyreg = None       # Post Process-Polynomial Regression DF

        # Other Post Process DF
        self._post_rollpolyreg = None   # Rolling Polynomial Regression


    # Class Methods

    # Get Directry
    def get_input_dir(self, file_name):
        return input_path(file_name=file_name)



    # Saveing Method
    def save_excel(self, file_name):
        if '.xlsx' not in file_name:
            file_name += '.xlsx'
        file_path = output_path(file_name=file_name)
        out_df = self.get_bioprocess_df()
        # Save
        print(f'{file_name} Saving......')
        out_df.to_excel(file_path, sheet_name=self._experiment_id, index=False)
        print(f'{file_name} Saved.\n')



    # Saveing Rolling PolyReg Method
    def save_excel_rollpolyreg(self, file_name):
        if '.xlsx' not in file_name:
            file_name += '.xlsx'
        file_path = output_path(file_name=file_name)
        out_df = self.get_post_rollpolyreg()
        # Save
        print(f'{file_name} Saving......')
        out_df.to_excel(file_path, sheet_name=self._experiment_id, index=False)
        print(f'{file_name} Saved.\n')

    

    # Plotting Method
    def plot_profile(self,
                     aa_list=None,
                     polyreg=True,
                     rolling=False,
                     save_file_name=None):

        print('Making a plot......')
        if (not aa_list):
            aa_list = self._aa_list
        n = len(aa_list)

        fig = plt.figure(figsize=(8*3, 6*n))

        for i, x in enumerate(aa_list):
            x = x.upper()
            fig = self._aa_dict[x].plot(polyreg=polyreg,
                                        rolling=rolling,
                                        fig=fig,
                                        column=n,
                                        ax_idx=1+i*3,)

        fig.suptitle(f'Profils for {self._experiment_id}', fontsize='xx-large')
        print('Done')



        # Save
        if (save_file_name != None):
            file_path = output_path(save_file_name)
            print(f'{save_file_name} Saving...')
            fig.savefig(file_path)
            print(f'{save_file_name} Saved\n')

        return fig

###########################################################################
