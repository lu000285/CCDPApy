import pandas as pd

#############################################################################################
############################## Rolling Polynomial Regression Functions ##############################
def rolling_regression(bio_process, order=3, windows=6):

    # Cell Logistic Growth
    cell = bio_process.get_cell()
    mu_calc_df = pd.concat([cell.get_time_mid().rename('CELL RUN TIME (HOURS)'),
                            cell.midcalc_growth_rate_calc()],
                            axis=1)
    cell.set_method_flag(method='rollreg', flag=True)

    # Cell
    '''order = polyorder.loc['CELL'].iat[0]
    cell = bio_process.get_cell()
    cell.rolling_poly_regression(polyreg_order=3, windows = 4)'''

    # Oxygen
    '''order = polyorder.loc['OXYGEN'].iat[0]
    oxygen = bio_process.get_oxygen()
    oxygen.rolling_poly_regression(polyreg_order=3, windows = 4)'''

    # IgG
    '''order = polyorder.loc['IGG'].iat[0]
    igg = bio_process.get_igg()
    igg.rolling_poly_regression(polyreg_order=3, windows = 4)'''

    # AA
    spc_dict = bio_process.get_spc_dict()
    '''df_conc = pd.DataFrame() # Initialize
    df_q = pd.DataFrame() # Initialize
    df_r = pd.DataFrame() # Initialize'''

    data_list = []  # df list to append data for each species
    for spc_name, spc_obj in spc_dict.items():
        # order = polyorder.loc[aa_name].iat[0]
        data = pd.DataFrame()
        spc_obj.rolling_poly_regression(polyreg_order=order, windows=windows)
        spc_obj.set_method_flag(method='rollreg', flag=True)
        
        pre = f'Roll. Poly. Reg. Order: {order} Window: {windows}'
        title = f'{pre} q{spc_name.capitalize()} (mmol/109 cell/hr)'

        q, order, window = spc_obj.get_sp_rate(method='rollreg')
        '''df_q[title] = q
        df_conc[f'Conc. {spc_name} MID. (mM)'] = spc_obj.get_conc_mid()
        df_r[f'r{spc_name[:3].capitalize()}'] = q / 0.0016'''

        data[f'{spc_name[:3]} RUN TIME (HOURS)'] = spc_obj.get_time_mid()
        data[f'Conc. {spc_name[:3]} MID. (mM)'] = spc_obj.get_conc_mid()
        data[title] = q
        data[f'r{spc_name[:3].capitalize()}']= q / 0.0016
        data_list.append(data)

    data_list.append(mu_calc_df)
    # Add to bp
    rollreg_df = pd.concat(data_list, axis=1)
    bio_process.set_rollreg_df(rollreg_df)

    # Ratio Calc
    # ratio_calc_rollpolyreg(bio_process)

    bio_process.set_process_flag(process='rollreg', flag=True)


'''# Ratio Caluculaions
def ratio_calc_rollpolyreg(bio_process):
    aa_dict = bio_process.get_spc_dict()
    df = bio_process.get_post_rollpolyreg()
    
    # DL/DG
    dL = aa_dict['Lactate'.upper()].get_rollpolyreg_sp_rate()
    dG = aa_dict['Glucose'.upper()].get_rollpolyreg_sp_rate()
    df['DL/DG (mmol/mmol)'] = dL / dG

    # qO2/qGlc
    qO2 = aa_dict['Oxygen'.upper()].get_rollpolyreg_sp_rate()
    qGlc = dG
    df['qO2/qGlc (mmol/mmol)'] = qO2 / qGlc

    # qGln/qGlc
    qGln = aa_dict.upper()['Glutamine'].get_rollpolyreg_sp_rate()
    qGlc = dG
    df['qGln/qGlc (mmol/mmol)'] = qGln / qGlc

    # qNH3/qGln
    qNH3 = aa_dict['NH3'.upper()].get_rollpolyreg_sp_rate()
    qGln = qGln 
    df['qNH3/qGln (mmol/mmol)'] = qNH3 / qGln'''
