import pandas as pd

#############################################################################################
def rolling_regression(bio_process, order=3, windows=6):
    '''
    Calculate SP. rate for species using rolling polynomial regression.

    Parameters
    ----------
        bio_process : BioProcess object
        order : int, defalut=3, optional
            polynomial order for rolling polynomial regression.
        windows : int, default=6, optional
            data point size used for rolling polynomial regression.
    '''
    method = 'rollreg'

    # Cell Logistic Growth
    cell = bio_process.get_cell()
    mu_calc_df = pd.concat([cell.get_time_mid().rename('CELL RUN TIME (HOURS)'),
                            cell.midcalc_growth_rate_calc()],
                            axis=1)
    cell.set_method_flag(method=method, flag=True)

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

    # Metabolite
    spc_dict = bio_process.get_spc_dict()
    spc_list = bio_process.get_spc_list()
    data_list = []  # df list to append data for each species

    for spc_name in spc_list:
        data = pd.DataFrame()
        spc = spc_dict[spc_name.upper()]    # species object
        # calculate sp. rate
        spc.rolling_poly_regression(polyreg_order=order, windows=windows)
        # Set flag true
        spc.set_method_flag(method=method, flag=True)
        
        q = spc.get_sp_rate(method=method)
        pre = f'Roll. Poly. Reg. Order: {order} Window: {windows}'
        title = f'{pre} q{spc_name.capitalize()} (mmol/109 cell/hr)'
        data[f'{spc_name[:3]} RUN TIME (HOURS)'] = spc.get_time_mid() # run time 
        data[f'Conc. {spc_name[:3]} MID. (mM)'] = spc.get_conc_mid() # concentraion
        data[title] = q # SP. rate
        data[f'r{spc_name[:3].capitalize()}']= q / 0.0016 # Residual

        # add data to data list
        data_list.append(data)

    # Add data for cell to data_list
    data_list.append(mu_calc_df)
    # Concat data_list
    rollreg_df = pd.concat(data_list, axis=1)
    # Add to bp
    bio_process.set_process_data(process=method, data=rollreg_df)

######################################################
    # SP. rate for Nitrogen and AA Carbon
    # bio_process.sp_rate_others(method=method)

    # Ratio Calc
    # bio_process.ratio_calc(method=method)
######################################################

    # Ratio Calc
    bio_process.ratio_calc(method=method)

    # Set flag true
    bio_process.set_process_flag(process=method, flag=True)

<<<<<<< HEAD
# End rolling_regression
=======
    # qNH3/qGln
    qNH3 = aa_dict['NH3'.upper()].get_rollpolyreg_sp_rate()
    qGln = qGln 
    df['qNH3/qGln (mmol/mmol)'] = qNH3 / qGln'''
>>>>>>> a9dab1f50394347fd12051a460a78bafdba045d3
