import pandas as pd

###########################################################################
def polyreg_calc(bio_process, polyorder_file):
    if (polyorder_file):
        input_path = bio_process.get_input_dir(file_name=polyorder_file)
        polyorder = pd.read_excel(io=input_path, index_col=0)
        # polyorder = bio_process.get_polyorder_df()
        polyorder.index = [name.upper() for name in polyorder.index]

    # Cell
    try:
        order = polyorder.loc['CELL'].iat[0]
    except:
        order = 3
    cell = bio_process.get_cell()
    cell.polyreg(polyorder=order)
    cell.set_method_flag(method='polyreg', flag=True)

    # Oxygen
    try: 
        order = polyorder.loc['OXYGEN'].iat[0]
    except:
        order = 3
    oxygen = bio_process.get_oxygen()
    oxygen.polyreg(polyorder=order)
    oxygen.set_method_flag(method='polyreg', flag=True)

    # IgG
    try:
        order = polyorder.loc['IGG'].iat[0]
    except:
        order = 3
    igg = bio_process.get_igg()
    igg.polyreg(polyorder=order)
    igg.set_method_flag(method='polyreg', flag=True)
    
    # AA
    spc_dict = bio_process.get_spc_dict()
    polyreg_df = pd.DataFrame()     # Initialize

    for spc_name, aa_obj in spc_dict.items():
        try:
            order = polyorder.loc[spc_name].iat[0]
        except:
            order = 3
        aa_obj.polyreg(polyorder=order)
        aa_obj.set_method_flag(method='polyreg', flag=True)

        title = f'Poly. Reg. Order: {order} q{spc_name.capitalize()} (mmol/109 cell/hr)'
        polyreg_df[title] = aa_obj.get_sp_rate(method='polyreg')

    # Add
    bio_process.set_polyreg_df(polyreg_df)

    # Ratio Calc
    polyreg_ratio_calc(bio_process)

    # Set polyreg flag True
    bio_process.set_process_flag(process='polyreg', flag=True)

###########################################################################

###########################################################################
# Ratio Caluculaions
def polyreg_ratio_calc(bio_process):
    aa_dict = bio_process.get_spc_dict()
    df = bio_process.get_polyreg_df()

    if ('Glucose'.upper() in aa_dict.keys()):
        dG = aa_dict['Glucose'.upper()].get_sp_rate(method='polyreg')
        # DL/DG
        if ('Lactate'.upper() in aa_dict.keys()):
            dL = aa_dict['Lactate'.upper()].get_sp_rate(method='polyreg')
            df['Poly. Reg. DL/DG (mmol/mmol)'] = dL / dG

        # qO2/qGlc
        oxygen = bio_process.get_oxygen()
        qO2 = oxygen.get_sp_rate_md()
        qGlc = dG
        df['Poly. Reg. qO2/qGlc (mmol/mmol)'] = qO2 / qGlc

        if ('Glutamine'.upper() in aa_dict.keys()):
            # qGln/qGlc
            qGln = aa_dict['Glutamine'.upper()].get_sp_rate(method='polyreg')
            df['Poly. Reg. qGln/qGlc (mmol/mmol)'] = qGln / qGlc

    # qNH3/qGln
    if ('NH3'.upper() in aa_dict.keys() and 'Glutamine'.upper() in aa_dict.keys()):
        qGln = aa_dict['Glutamine'.upper()].get_sp_rate(method='polyreg')
        qNH3 = aa_dict['NH3'].get_sp_rate(method='polyreg')
        df['Poly. Reg. qNH3/qGln (mmol/mmol)'] = qNH3 / qGln
###########################################################################