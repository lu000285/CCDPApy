import pandas as pd


###########################################################################
def cumulative_calc(bio_process,
                    use_feed_conc,
                    use_conc_after_feed):
    '''
    Calculate cumulative consumptions/productions for species.

    Parameters
    ----------
        bio_process : BioProcess object
        use_feed_conc : bool
        use_conc_after_feed : bool
    '''

    # Cell
    cell = bio_process.get_cell()   # Get Cell object.
    cell.in_process()   # Calc. cumulative
    cell.set_method_flag(method='cumulative', flag=True)    # Set cumulative flag true
    # bio_process.set_cell(cell)  # set Cell to bio_process

    # Oxygen
    oxygen = bio_process.get_oxygen()   # Get Oxygen object.
    oxygen.in_process() # Calc. cumulative
    oxygen.set_method_flag(method='cumulative', flag=True)  # Set cumulative flag true
    # bio_process.set_oxygen(oxygen)  # set Cell to bio_process

    # Product/IgG
    igg = bio_process.get_product()
    igg.in_process()    # Calc. cumulative
    igg.set_method_flag(method='cumulative', flag=True) # Set cumulative flag true
    # bio_process.set_igg(igg)    # set Cell to bio_process

    # Metabolite Cumulative
    spc_list = bio_process.get_spc_list()  # Get AA List to Analyze
    spc_dict = bio_process.get_spc_dict()                        # Initialize
    spc_cumulative_df = pd.DataFrame()   # Initialize
    spc_conc_df = pd.DataFrame()
    spc_conc_after_feed_df = pd.DataFrame()

    for s in spc_list:
        s = s.upper()   # Name
        spc = spc_dict[s]
        
        # Calculate Cumulative Consumption/Production
        spc.in_process(use_feed_conc=use_feed_conc, use_conc_after_feed=use_conc_after_feed)
        spc.set_method_flag(method='cumulative', flag=True)
        unit = spc.get_cumulative_unit()    # Unit
        
        spc_cumulative_df['CUM '+s+' '+unit] = spc.get_cumulative()  # Add to DF
        spc_conc_df[s+' (mM) (before Feed)'] = spc.get_conc_before_feed()
        spc_conc_after_feed_df[s+' (mM) (After Feed)'] = spc.get_conc_after_feed()
        spc_dict[s] = spc    # Add to Dictionary
    
    # Add to bp obj
    bio_process.set_spc_df(spc_cumulative_df)
    # bio_process.set_spc_dict(spc_dict=spc_dict)
    bio_process.set_spc_conc(spc_conc_df)
    bio_process.set_spc_conc_after_feed(conc_after_feed=spc_conc_after_feed_df)

    # Cumulative for Nitrogen, and AA Carbon
    bio_process.cumulative_others()

    # Set in process flag True
    bio_process.set_process_flag(process='inpro', flag=True)

# End cumulative_calc