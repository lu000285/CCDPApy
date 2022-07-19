import pandas as pd

from .BioProcess import BioProcess
from ..helper_func.helper_func import input_path

###########################################################################

###########################################################################
def bio_process(input_file_name,
                measured_data_sheet_name='Measured Data',
                aa_list=None):

    if '.xlsx' not in input_file_name:
        input_file_name += '.xlsx'
        
    input = input_path(input_file_name)

    print(f'{input_file_name} Importing...')
    # Read Excel Files
    measured_data = pd.read_excel(io=input, 
                                  sheet_name=measured_data_sheet_name,
                                  header=5)

    exp_info = pd.read_excel(io=input,
                             sheet_name=measured_data_sheet_name,
                             nrows=4,
                             usecols=[0, 1],
                             header=None,
                             index_col=0)

    print(f'{input_file_name} Imported\n')
    
    # Bio Process
    bio_pro = BioProcess(experiment_info=exp_info, measured_data=measured_data)
    # Check AA List to Analyze
    if (aa_list):
        # Set AA List
        aa_list = [name.upper() for name in aa_list]
        bio_pro.set_aa_list(aa_list=aa_list)

    return bio_pro