# Python Libraries
import pandas as pd
import matplotlib.pyplot as plt

# My Libraries
from ..helper_func.helper_func import output_path
from ..helper_func.helper_func import input_path
from .GetterMixin import GetterMixin
from .SetterMixin import SetterMixin
from .DispMixin import DispMixin
from .BioProcessMixin import BioProcessMixin
from ..plotting.PlotMixin import PlotMixin

###########################################################################
# Cell Bioprocess Class
###########################################################################
class BioProcess(BioProcessMixin, GetterMixin, SetterMixin, DispMixin, PlotMixin):
    '''
    Store bioprocess information.

    Attributes
    ----------
    experiment_info : pd.DataFrame
        Information of the experiment.
        Experiment ID, experimentor name, cell line name, and initial culture volume.
    measured_data : pd.DataFrame
        Measured data of the experiment.
    '''
    def __init__(self, experiment_info, measured_data):
        '''
        Parameters
        ----------
        experiment_info : pd.DataFrame
            Information of the experiment.
            Experiment ID, experimentor name, cell line name, and initial culture volume.
        measured_data : pd.DataFrame
            Measured data of the experiment.
        '''
        # Experiment DF
        self._exp_info = experiment_info        # experiment info
        self._measured_data = measured_data     # measured data
        self._feed_added = None                 # spc feed added                      
        self._polyorder_df = None               # Poly. Reg. Order

        # Experoment Infomation Members
        self._experiment_id = experiment_info.loc['Experiment ID'].get(1)
        self._experimenter_name = experiment_info.loc['Name'].get(1)
        self._cell_line_name = experiment_info.loc['Cell Line'].get(1)
        self._initial_volume = experiment_info.loc['Initial Volume (mL)'].get(1)

        # Cell Line Name and Exp ID Column
        self._expID_col = pd.Series(data=[self._experiment_id] * len(measured_data), name='Experiment ID')
        self._cl_col = pd.Series(data=[self._cell_line_name] * len(measured_data), name='Cell Line')

        # Species Object
        self._cell = None       # Cell
        self._oxygen = None     # Oxygen
        self._procut = None     # Product/IgG

        self._original_spc_list = ['Alanine', 'Arginine', 'Asparagine',
                                   'Aspartate', 'Cystine', 'Glucose',
                                   'Glutamine', 'Glutamate', 'Glycine',
                                   'Histidine', 'Isoleucine', 'Lactate',
                                   'Leucine','Lysine', 'Methionine',
                                   'NH3', 'Phenylalanine', 'Proline',
                                   'Serine', 'Threonine', 'Tryptophan',
                                   'Tyrosine', 'Valine', 'Ethanolamine']
                                  
        self._spc_list = None            # Species List
        self._spc_dict = {}              # Species Dictionary = {'name': Metabolite obj}
        self._special_spc_dict = {}      # Special Species Dictionary; Nitrogen, AA carbon
        self._spc_df = None              # Species Cumulative DF
        self._spc_conc_df = None         # Species Conc DF
        self._conc_after_feed_df = None  # Species Conc After Feed DF
        
        self._pre_process = None        # Pre Process DF
        self._in_process = None         # In Process DF
        self._post_twopt = None         # Post Process-Two Point Calc. DF
        self._post_polyreg = None       # Post Process-Polynomial Regression DF
        self._post_rollpolyreg = None   # Post Process-Rolling Polynomial Regression DF

        # Flags
        self._pre_process_flag = False
        self._in_process_flag = False
        self._twopt_flag = False
        self._polyreg_flag = False
        self._rollreg_flag = False


    # Class Methods
    def get_input_dir(self, file_name):
        '''
        Return the file path from the file name.

        Parameters
        ---------
        file_name : str
            file name.

        Returns
        -------
        path : str
            The file path.
        '''
        path = input_path(file_name=file_name)
        return path


    def save_excel(self, file_name):
        '''
        Save the file as an Excel.

        Parameters
        ----------
        file_name : str
            File name.
        '''
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
        '''

        '''
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
                     spc_list,
                     method,
                     combined=False,
                     save_file_name=None):

        print('Making a plot......')

        twopt = False
        polyreg = False
        rollreg = False

        # Check Regression Method to Plot
        if ('all' in method):
            twopt = True
            polyreg = True
            rollreg = True
        if ('twopt' in method):
            twopt = True
        if ('polyreg' in method):
            polyreg = True
        if ('rollreg' in method):
            rollreg = True
        
        n = len(spc_list)
        fig = plt.figure(figsize=(8*3, 6*n))

        for i, name in enumerate(spc_list):
            fig = self._spc_dict[name.upper()].plot(twopt=twopt,
                                                    polyreg=polyreg,
                                                    rollreg=rollreg,
                                                    fig=fig,
                                                    column=n,
                                                    ax_idx=1+i*3)

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
