import pandas as pd

from .BioProcess import BioProcess
from ..pre_process.pre_process import pre_process
from ..in_process.in_process import cumulative_calc
from ..post_process.two_point_calc.twopt_calc import twopt_calc
from ..post_process.polynomial_regression.polynomial_regression import polyreg_calc
from ..post_process.rolling_regression.rolling_regression import rolling_regression
from ..helper_func.helper_func import input_path

###########################################################################

###########################################################################
def bio_process(input_file, measurement_sheet, **kwargs):
    '''
    Execute the bioprocess.

    Parameters
    ----------
    input_file : str
        The Excel file of the measured data.
        '.xlsx' must be included in the file name.

    measurement_sheet : str
        Sheet name of the measured data in the Excel file.
    
    Returns
    -------
    bio_process : python object
        Bioprocess object.

    Other Parameters
    ----------------
    **kwargs : bio_process properties, optional
        Properties:
        spc_list:  list of str. default=['Alanine', 'Arginine', 'Asparagine', 'Aspartate', 'Cystine', 'Glucose', 'Glutamine', 'Glutamate', 'Glycine', 'Histidine', 'Isoleucine', 'Lactate', 'Leucine','Lysine', 'Methonine', 'NH3', 'PHENYLALANINE', 'PROLINE', 'SERINE', 'THREONINE','TRYPTOPHAN', 'TYROSINE', 'VALINE', 'ETHANOLAMINE']
            List of species name to be analyzed.
            Upper, lower, or capitalized case can be uesd. If this is not specified,
            original species list is to be used.

        add_spc:  list of str.
            List of new species name to be analuzed, which is not listed in the original species list.

        use_feed_conc: bool, default=False
            True if the measured data has the measurements of feed concentrations. Otherwise, False.

        use_conc_after_feed: bool, default=False
            True if the measured data has the measurements of concentrations after feeding. Otherwiese, False.

        all_method: bool
            True if all regression methods are required.

        polyreg:  bool
            True if polynomial regression is needed.

        polyorder_file: string, default='polynomial_order.xlsx'.
            Name of the file, whihc includes species name and the polynomial order for each species.
            '.xlsx' must be included in the file name. The default polynomial order of 3 is to be used, if this is not specified.

        rollreg: bool
            True if rolling polynomial regression is needed.

        rollreg_order: int, default=3
            The polynomial order for the regression.

        rollreg_window: int, default=6
            The window size for the regression.
    '''

    # Get File Path
    file_path = input_path(file_name=input_file)
    # Read Measured Data
    measured_data = pd.read_excel(io=file_path, sheet_name=measurement_sheet, header=5)
    # Read Experiment Info
    exp_info = pd.read_excel(io=file_path, sheet_name=measurement_sheet, nrows=4, usecols=[0, 1], header=None, index_col=0)
    print(f'{input_file} imported.')
    
    # Bio Process Class
    bioprocess = BioProcess(experiment_info=exp_info,
                            measured_data=measured_data,
                            )

    # Check Spcies list to analze
    if (kwargs.get('spc_list')):
        spc_list = [name.upper() for name in kwargs.get('spc_list')] # Set AA List
        bioprocess.set_spc_list(spc_list=spc_list)

    # Check New Species List to Add
    if (kwargs.get('add_spc')):
        bioprocess.set_new_spc(new_spc_list=kwargs.get('add_spc')) # add new species to spc_list

    feed_name = measurement_sheet
    #****** Pre Process ******
    pre_process(bio_process=bioprocess, feed_name=feed_name)
    print('Done Pre-Process.')

    #****** In Process -Cumulative Cons/Prod ******
    cumulative_calc(bio_process=bioprocess,
                    feed_name=feed_name,
                    use_feed_conc=True if (kwargs.get('use_feed_conc')) else False,
                    use_conc_after_feed=True if (kwargs.get('use_conc_after_feed')) else False)
    print('Done In-Process.')

    #***** Post Process -SP. Rate Two Point Calc ******
    twopt_calc(bio_process=bioprocess)
    print('Done Two-Point Calculations.')

    #***** Post Process -SP. Rate Poly. Regression *****
    if (kwargs.get('polyreg') or kwargs.get('all_method')):
        polyreg_calc(bio_process=bioprocess,
                     polyorder_file=kwargs.get('polyorder_file'))
        print('Done Polynomial Regression.')

    #***** Post Process -SP. Rate Rolling Poly. Regression *****
    if (kwargs.get('rollreg') or kwargs.get('all_method')):
        order = kwargs.get('rollreg_order') if kwargs.get('rollreg_order') else 3
        window = kwargs.get('rollreg_window') if kwargs.get('rollreg_window') else 6

        rolling_regression(bio_process=bioprocess, order=order, windows=window)
        print('Done Rolling Regression.')

    return bioprocess