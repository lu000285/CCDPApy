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

    # Oxygen
    try: 
        order = polyorder.loc['OXYGEN'].iat[0]
    except:
        order = 3
    oxygen = bio_process.get_oxygen()
    oxygen.polyreg(polyorder=order)

    # IgG
    try:
        order = polyorder.loc['IGG'].iat[0]
    except:
        order = 3
    igg = bio_process.get_igg()
    igg.polyreg(polyorder=order)

    
    # AA
    aa_dict = bio_process.get_aa_dict()
    polyreg_df = pd.DataFrame()     # Initialize

    for aa_name, aa_obj in aa_dict.items():
        try:
            order = polyorder.loc[aa_name].iat[0]
        except:
            order = 3
        aa_obj.polyreg(polyorder=order)

        title = f'Poly. Reg. Order: {order} q{aa_name.capitalize()} (mmol/109 cell/hr)'

        polyreg_df[title] = aa_obj.get_polyreg_sp_rate()

    # Add
    bio_process.set_post_polyreg(polyreg_df)

    # Ratio Calc
    polyreg_ratio_calc(bio_process)

    return bio_process
###########################################################################

###########################################################################
# Ratio Caluculaions
def polyreg_ratio_calc(bio_process):
    aa_dict = bio_process.get_aa_dict()
    df = bio_process.get_post_polyreg()

    if ('Glucose'.upper() in aa_dict.keys()):
        dG = aa_dict['Glucose'.upper()].get_polyreg_sp_rate()
        # DL/DG
        if ('Lactate'.upper() in aa_dict.keys()):
            dL = aa_dict['Lactate'.upper()].get_polyreg_sp_rate()
            df['Poly. Reg. DL/DG (mmol/mmol)'] = dL / dG

        # qO2/qGlc
        oxygen = bio_process.get_oxygen()
        qO2 = oxygen.get_sp_rate_md()
        qGlc = dG
        df['Poly. Reg. qO2/qGlc (mmol/mmol)'] = qO2 / qGlc

        if ('Glutamine'.upper() in aa_dict.keys()):
            # qGln/qGlc
            qGln = aa_dict['Glutamine'.upper()].get_polyreg_sp_rate()
            df['Poly. Reg. qGln/qGlc (mmol/mmol)'] = qGln / qGlc

    # qNH3/qGln
    if ('NH3'.upper() in aa_dict.keys() and 'Glutamine'.upper() in aa_dict.keys()):
        qGln = aa_dict['Glutamine'.upper()].get_polyreg_sp_rate()
        qNH3 = aa_dict['NH3'].get_polyreg_sp_rate()
        df['Poly. Reg. qNH3/qGln (mmol/mmol)'] = qNH3 / qGln
###########################################################################