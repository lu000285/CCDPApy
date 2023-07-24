import pandas as pd

from .Fed_batch import BioProcess as FedBatch
from .Perfusion import BioProcess as Perfusion

from CCDPApy.helper import input_path
from .CellLine import CellLine

def bioprocess_pipeline(cell_culture_type,
                        input_file_name,
                        **kwargs):
    '''
    Execute the bioprocess; 
    in-process, two-point calculations, polynomial regression, rolling polynomial regression.

    Parameters
    ----------
    cell_culture : str
        Meethod of cell culture. 'fed-bacth', 'perfusion'.
    input_file : str
        The Excel file of the measured data.
        '.xlsx' must be included in the file name.
    
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

        new_spc:  list of str.
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
    cell_line = CellLine()
    # Check spcies list
    spc_list = kwargs.get('spc_list') if kwargs.get('spc_list') else []
    new_spc_list = kwargs.get('new_spc') if kwargs.get('new_spc') else []

    # Read all sheets into a dictionary
    file_path = input_path(input_file_name)
    sheets_dict = pd.read_excel(file_path, sheet_name=None)

    # Access each sheet's DataFrame
    for sheet_name, df in sheets_dict.items():
        if cell_culture_type=='fed-batch':
            use_feed_conc = True if (kwargs.get('use_feed_conc')) else False
            use_conc_after_feed = True if (kwargs.get('use_conc_after_feed')) else False
            bio_process = FedBatch(data=df, use_feed_conc=use_feed_conc, use_conc_after_feed=use_conc_after_feed)
        
        elif cell_culture_type=='perfusion':
            bio_process = Perfusion(file_name=input_file_name)
            a = kwargs.get('recycling_factor') if (kwargs.get('recycling_factor')) else 0.25
            c = kwargs.get('concentration_factor') if (kwargs.get('concentration_factor')) else 3
        
        else:
            print('Inproper cell culture type. Please choose "fed-batch" or "perfuson".')
            return
        
        bio_process.in_process()

        #***** Post Process Polynomial Regression *****
        if (kwargs.get('polyreg') or kwargs.get('all_method')):
            bio_process.polynomial(polyorder_file=kwargs.get('polyorder_file'))
            #print('Polynomial Regression. Done')

        #***** Post Process Rolling Window Polynomial Regression *****
        if (kwargs.get('rollreg') or kwargs.get('all_method')):
            order = kwargs.get('rollreg_order') if kwargs.get('rollreg_order') else 3
            window = kwargs.get('rollreg_window') if kwargs.get('rollreg_window') else 6
            bio_process.roll_regression(degree=order, windows=window)
            #print('Rolling Regression. Done.')

        cell_line.add_bio_process(bio_process=bio_process)

    return cell_line
#*** End bio_process ***#