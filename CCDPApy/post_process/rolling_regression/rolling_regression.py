import pandas as pd

#############################################################################################
############################## Rolling Polynomial Regression Functions ##############################
def rolling_regression(bio_process,
                       polyorder_file='polynomial_order.xlsx',
                       aa_lst=None, r_lst=None,
                       order=3, windows=6):

    # Read Poly. Order file
    # polyorder = pd.read_excel(io=polyorder_file, index_col=0)

    # polyorder = bio_process.get_polyorder_df()
    # polyorder.index = [name.upper() for name in polyorder.index]

    cell = bio_process.get_cell()
    mid_time = cell.get_time_mid()
    # Logistic Growth
    mu_calc_df = cell.midcalc_growth_rate_calc()

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
    if (aa_lst==None and r_lst==None):
        r_lst = ['rglut1','rmct','rglnna','rasnna','raspna']
        aa_lst = ['Glucose','Lactate','Glutamine','Asparagine','Aspartate']

    aa_dict = bio_process.get_aa_dict()
    df_conc = pd.DataFrame() # Initialize
    df_q = pd.DataFrame() # Initialize
    df_r = pd.DataFrame() # Initialize
    df_conc['RUN TIME (HOURS)'] = mid_time

    for i, aa_name in enumerate(aa_lst):
        # order = polyorder.loc[aa_name].iat[0]
        aa_obj = aa_dict[aa_name.upper()]
        aa_obj.rolling_poly_regression(polyreg_order=order, windows=windows)
        pre = f'Roll. Poly. Reg. Order: {order} Window: {windows}'
        title = f'{pre} q{aa_name.capitalize()} (mmol/109 cell/hr)'

        q = aa_obj.get_rollpolyreg_sp_rate()
        df_q[title] = q
        df_conc[f'Conc. {aa_name} MID. (mM)'] = aa_obj.get_conc_mid()
        df_r[r_lst[i]] = q / 0.0016

    # Add to bp
    bio_process.set_post_rollpolyreg(df_q)

    # Ratio Calc
    # ratio_calc_rollpolyreg(bio_process)

    # Add to bp
    bio_process.set_post_rollpolyreg(pd.concat([df_conc,
                                                df_q,
                                                df_r,
                                                mu_calc_df], axis=1))

    return bio_process
        

# Ratio Caluculaions
def ratio_calc_rollpolyreg(bio_process):
    aa_dict = bio_process.get_aa_dict()
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
    df['qNH3/qGln (mmol/mmol)'] = qNH3 / qGln