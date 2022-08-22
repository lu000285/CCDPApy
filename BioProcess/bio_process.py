from isort import file
from matplotlib import use
import pandas as pd

from .BioProcess import BioProcess
from ..pre_process.pre_process import pre_process
from ..in_process.in_process import cumulative_calc
from ..post_process.two_point_calc.twopt_calc import twopt_calc
from ..post_process.polynomial_regression.polynomial_regression import polyreg_calc
from ..post_process.rolling_regression.rolling_regression import rolling_regression

from ..helper_func.helper_func import input_path

###########################################################################
# **kwargs:
# aa_list:  list
# add_spc:  list
# use_feed_conc: bool
# use_conc_after_feed: bool
# allreg: bool
# polyreg:  bool
# polyorder_file: string
# rollreg: bool
# rollreg_order: int
# rollreg_window: int
###########################################################################
def bio_process(input_file,
                measurement_sheet='Measured Data',
                **kwargs):
    
    # Get File Path
    file_path = input_path(file_name=input_file)

    print(f'{input_file} Importing...')
    # Read Measured Data
    measured_data = pd.read_excel(io=file_path, 
                                  sheet_name=measurement_sheet,
                                  header=5)
    # Read Experiment Info
    exp_info = pd.read_excel(io=file_path,
                             sheet_name=measurement_sheet,
                             nrows=4,
                             usecols=[0, 1],
                             header=None,
                             index_col=0)

    print('Imported')
    
    # Bio Process Class
    bio_pro = BioProcess(experiment_info=exp_info, measured_data=measured_data)

    # Check AA List to Analyze
    if (kwargs.get('aa_list')):
        # Set AA List
        aa_list = [name.upper() for name in kwargs.get('aa_list')]
        bio_pro.set_aa_list(aa_list=aa_list)

    # Check New Species List to Add
    if (kwargs.get('add_spc')):
        # add new species to aa_list
        bio_pro.set_new_spc(new_spc_list=kwargs.get('add_spc'))
    
    bio_pro.disp_experiment()

    #****** Pre Process ******
    print('Pre Processing...')
    bio_pro = pre_process(bio_pro)
    print('Done')

    #****** In Process -Cumulative Cons/Prod ******
    print('In Processing...')
    bio_pro = cumulative_calc(bio_process=bio_pro,
                              use_feed_conc=True if (kwargs.get('use_feed_conc')) else False,
                              use_conc_after_feed=True if (kwargs.get('use_conc_after_feed')) else False)
    print('Done')

    #***** Post Process -SP. Rate Two Point Calc ******
    print('Two Point Calculations...')
    bio_pro = twopt_calc(bio_process=bio_pro)
    print('Done')

    #***** Post Process -SP. Rate Poly. Regression *****
    if (kwargs.get('polyreg') or kwargs.get('all_method')):
        print('Polynomial Regressions...')
        bio_pro = polyreg_calc(bio_process=bio_pro,
                               polyorder_file=kwargs.get('polyorder_file'))
        print('Done')

    #***** Post Process -SP. Rate Rolling Poly. Regression *****
    if (kwargs.get('rollreg') or kwargs.get('all_method')):
        print('Rolling Regressions...')
        r_lst = ['rglut1','rmct','rglnna','rasnna','raspna']
        aa_lst = ['Glucose','Lactate','Glutamine','Asparagine','Aspartate']

        order = kwargs.get('rollreg_order') if kwargs.get('rollreg_order') else 3
        window = kwargs.get('rollreg_window') if kwargs.get('rollreg_window') else 6

        bio_pro = rolling_regression(bio_process=bio_pro,
                                     order=order,
                                     windows=window,
                                     aa_lst=aa_lst,
                                     r_lst=r_lst)
        print('Done')

    return bio_pro