from .BioProcess import BioProcess as FedBatch
from .Perfusion.BioProcess import BioProcess as Perfusion

###########################################################################
def bioprocess_pipeline(cell_culture,
                        input_file_name,
                        measurement_sheet='Measured Data',
                        feed_sheet='Separate Feed Info',
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

    measurement_sheet : str
        Sheet name of the measured data in the Excel file.

    feed_sheet : str
        Sheet name of the separate feed infomation in the Excel file.
    
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
    
    # Check spcies list
    spc_list = kwargs.get('spc_list') if kwargs.get('spc_list') else []
    new_spc_list = kwargs.get('new_spc') if kwargs.get('new_spc') else []

    # Fed-batch Cell Culture BioProcess Class
    if cell_culture=='fed-batch':
        bio_process = FedBatch(file_name=input_file_name,
                               measurement_sheet=measurement_sheet,
                               feed_sheet=feed_sheet,
                               spc_list=spc_list,
                               new_spc_list=new_spc_list)
        use_feed_conc = True if (kwargs.get('use_feed_conc')) else False
        use_conc_after_feed = True if (kwargs.get('use_conc_after_feed')) else False
        bio_process.in_process(feed_concentraion=use_feed_conc, concentration_after_feed=use_conc_after_feed)
        
    elif cell_culture=='perfusion':
        bio_process = Perfusion(file_name=input_file_name)
        a = kwargs.get('recycling_factor') if (kwargs.get('recycling_factor')) else 0.25
        c = kwargs.get('concentration_factor') if (kwargs.get('concentration_factor')) else 3
        bio_process.in_process(a=a, c=c)
    else:
        print('Inproper cell culture type. Please specify "fed-batch" or "perfuson".')
        return None

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

    return bio_process
#*** End bio_process ***#