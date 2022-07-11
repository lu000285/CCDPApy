import sys
import pandas as pd
import numpy as np
from pyrsistent import v
import scipy as sc
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import math
import types
import os
from pathlib import Path
from RollingRegression import *
from LogisticGrowth import *
import argparse
# Main Function
def main():
    # input arguments for the .py file
    parser = argparse.ArgumentParser(description='Data Processing for CL1')
    optional = parser._action_groups.pop()  # creates group of optional arguments
    required = parser.add_argument_group('required arguments')  # creates group of required arguments

    # required input, the followinf is an example
    # required.add_argument('-nig', '--num_ig', help='number of IG run in training', required=True, type=int, default=1)
    optional.add_argument('-m', '--mid_cal', help='Mid-cal. is on (1) or off (0)',type=int, default=0)
    args = parser.parse_args()  # get the arguments from the program input, set them to args
    mid_cal = args.mid_cal
    # Base directry where this file exits
    BASE_DIR = Path(__file__).resolve().parent

    # CL1 Input
    INPUT_SHEET = 'Measured Data'
    input_CL1_1 = 'VS_NIIMBL VS-001.xlsx'
    input_CL1_2 = 'VS_NIIMBL VS-002.xlsx'
    input_CL1_3 = 'VS_NIIMBL VS-003.xlsx'
    input_CL1 = [input_CL1_1, input_CL1_2, input_CL1_3]
    input_path = [os.path.join(BASE_DIR, file_name) for file_name in input_CL1]

    # CL2 Output
    output_file = 'In_Process_Calc_CL1.xlsx'
    OUTPUT_BASE = os.path.join(BASE_DIR, 'output_files')
    # Make output files directry
    try:
        os.makedirs(OUTPUT_BASE)    
        print("Directory " , OUTPUT_BASE ,  " Created ")
    except FileExistsError:
        print("Directory " , OUTPUT_BASE ,  " already exists")

    OUTPUT_CL1 = os.path.join(OUTPUT_BASE, output_file)

    midcalc_output_file = 'Mid_Calc_CL1.xlsx'
    OUTPUT_CL1_midcalc = os.path.join(OUTPUT_BASE, midcalc_output_file)
    
    exp = {} # For String each experiment
    exp_mid = {} # empty dict to store mid-calc. results
    for i, input in enumerate(input_path):
        # Pre Process
        bio_process, exp_no, aa_lst = preProcess(input_file_path=input, sheet_name=INPUT_SHEET)
        
        # Polynomial Regression
        poly_reg_df = polynomialRegressionCalc(bio_process.get_measured_data(), bio_process.get_species_dict())
        bio_process.set_post_process(poly_reg_df)

        # Savitzky-Golay Filter
        polyorder=3
        windos_size = 5
        savgol_df = savgolFilterCalc(bio_process.get_measured_data(),
                                    bio_process.get_species_dict(),
                                    polyorder=polyorder,
                                    window_size=windos_size)
        bio_process.set_post_process(savgol_df)

        # Mid-Calcaulation
        if mid_cal == 1:
            mid_calc_df = RollPolynomialRegressionCalc(bio_process.get_species_dict(),aa_lst, windows=4)
            mu_calc_df = midcalc_growth_rate_calc(bio_process.get_species_dict())
            exp_mid[exp_no] = pd.concat([mid_calc_df, mu_calc_df], axis=1)#mid_calc_df
        exp[exp_no] = bio_process

    # Saving Excel Files
    saveExcell(data=exp, output_file_path=OUTPUT_CL1)

    # Saving Excel Files
    if mid_cal == 1:
        saveExcell_midcalc(data=exp_mid, output_file_path=OUTPUT_CL1_midcalc)

    # Plotting via BioProcess class
    species = ['Lactate', 'Glucose', 'Glutamine', 'Asparagine', 'Aspartate']
    img_1 = 'CL1_1_WS_5.png'
    img_2 = 'CL1_2_WS_5.png'
    img_3 = 'CL1_3_WS_5.png'
    img_lst = [img_1, img_2, img_3]
    output_img_path = [os.path.join(OUTPUT_BASE, img_name) for img_name in img_lst]

    for i, x in enumerate(exp.values()):
        fig = x.plot_profile(species, polyreg=True, savgol=True)
        fig.savefig(output_img_path[i])
        print(img_lst[i] + ' saved')

    # Savgol Filter Window Size = 7
    exp_2 = {}
    for key, value in exp.items():
        # Savitzky-Golay Filter
        windos_size = 7
        savgol_df = savgolFilterCalc(value.get_measured_data(), value.get_species_dict(), window_size=windos_size)
        value.set_post_process(savgol_df)

        exp_2[key] = value

    # Plotting via BioProcess class
    img_1 = 'CL1_1_WS_7.png'
    img_2 = 'CL1_2_WS_7.png'
    img_3 = 'CL1_3_WS_7.png'
    img_lst = [img_1, img_2, img_3]
    output_img_path = [os.path.join(OUTPUT_BASE, img_name) for img_name in img_lst]

    for i, x in enumerate(exp_2.values()):
        fig = x.plot_profile(species, polyreg=True, savgol=True)
        fig.savefig(output_img_path[i])
        print(img_lst[i] + ' saved')

    # Savgol Filter Window Size = 9
    exp_3 = {}
    for key, value in exp.items():
        # Savitzky-Golay Filter
        windos_size = 9
        savgol_df = savgolFilterCalc(value.get_measured_data(), value.get_species_dict(), window_size=windos_size)
        value.set_post_process(savgol_df)

        exp_3[key] = value

    # Plotting via BioProcess class
    img_1 = 'CL1_1_WS_9.png'
    img_2 = 'CL1_2_WS_9.png'
    img_3 = 'CL1_3_WS_9.png'
    img_lst = [img_1, img_2, img_3]
    output_img_path = [os.path.join(OUTPUT_BASE, img_name) for img_name in img_lst]

    for i, x in enumerate(exp_3.values()):
        fig = x.plot_profile(species, polyreg=True, savgol=True)
        fig.savefig(output_img_path[i])
        print(img_lst[i] + ' saved')

    # Savgol Filter Window Size = 13
    exp_4 = {}
    for key, value in exp.items():
        # Savitzky-Golay Filter
        windos_size = 13
        savgol_df = savgolFilterCalc(value.get_measured_data(), value.get_species_dict(), window_size=windos_size)
        value.set_post_process(savgol_df)

        exp_4[key] = value

    # Plotting via BioProcess class
    img_1 = 'CL1_1_WS_13.png'
    img_2 = 'CL1_2_WS_13.png'
    img_3 = 'CL1_3_WS_13.png'
    img_lst = [img_1, img_2, img_3]
    output_img_path = [os.path.join(OUTPUT_BASE, img_name) for img_name in img_lst]

    for i, x in enumerate(exp_4.values()):
        fig = x.plot_profile(species, polyreg=True, savgol=True)
        fig.savefig(output_img_path[i])
        print(img_lst[i] + ' saved')


    
    return 0





# Cell Bioprocess Class
class BioProcess:
    def __init__(self, cell_line, measured_data, in_process, species_list, species_dict):
        self._cell_line = cell_line
        self._measured_data = measured_data
        self._in_process = in_process
        self._species_list = species_list
        self._species_dict = species_dict
        self._post_process = None

    # Getters
    def get_cell_line(self):
        return self._cell_line
    def get_measured_data(self):
        return self._measured_data
    def get_in_process(self):
        return self._in_process
    def get_species_list(self):
        return self._species_list
    def get_species_dict(self):
        return self._species_dict

    def get_post_process(self):
        return self._post_process

    def get_bioprocess_df(self):
        return pd.concat([self._measured_data,
                          self._in_process,
                          self._post_process],
                         axis = 1)

    # Setters
    def set_post_process(self, post_process):
        self._post_process = pd.concat([self._post_process, post_process], axis=1)


    # Plotting Method
    def plot_profile(self, species_list, polyreg=False, savgol=False):
        n = len(species_list)

        fig = plt.figure(figsize=(8*3, 6*n))

        for i, x in enumerate(species_list):
            fig = self._species_dict[x].plot(polyreg=polyreg, savgol=savgol,
                                             fig=fig, column=n, ax_idx=1+i*3,)

        title = ''
        for name in species_list:
            title += name + ' '
        fig.suptitle(title + 'Profils', fontsize='xx-large')

        return fig


# Species Class
class Species:
    def __init__(self,
                 name,
                 run_time,
                 conc=pd.Series(data=np.nan, name='CONC.'),
                 viable_cell=pd.Series(data=np.nan, name='VIABLE CELL CONC.'),
                 v_before=pd.Series(data=np.nan, name='VOLUME BEFORE SAMPLING.'),
                 v_after=pd.Series(data=np.nan, name='VOLUME AFTER SAMPLING.'),
                 v_after_feed=pd.Series(data=np.nan, name='VOLUME AFTER SAMPLING.'),
                 viability=pd.Series(data=np.nan, name='VIABILITY'),
                 total_cell=pd.Series(data=np.nan, name='TOTAL CELL CONC.'),
                 ):
        
        # Members
        self._name = name
        self._run_time = run_time
        self._concentration = conc
        self._vcc = viable_cell
        self._v_before = v_before
        self._v_after = v_after
        self._v_after_feed = v_after_feed
        self._viability=viability
        self._tcc=total_cell

        self._cumulative = pd.Series(data=np.nan, name='CUM CONS.')
        self._sp_rate = pd.Series(data=np.nan, name='SP.')
        self._conc_after_feed = pd.Series(data=np.nan, name='CONC. AFTER FEEDING')

        # New for mid-point calculation
        self._run_time_mid = pd.Series(data=np.nan, name='Middle run time')
        self._conc_mid = pd.Series(data=np.nan, name='Mid-point CONC.') # average of before and after feeding

        # For polynomial regression
        self._polyreg_order = np.nan
        self._polyreg_cumulative = pd.Series(data=np.nan, name='Poly. Fit CUM CONS.')
        self._polyreg_sp_rate = pd.Series(data=np.nan, name='Poly. Fit SP.')
        self._polyfit_cumulative = np.nan

        # For rolling polynomial regression
        self._rollpolyreg_order = np.nan
        self._rollpolyreg_cumulative = pd.Series(data=np.nan, name='Poly. Fit CUM CONS.')
        self._rollpolyreg_sp_rate = pd.Series(data=np.nan, name='Poly. Fit SP.')
        self._rollpolyfit_cumulative = np.nan

        # For svitzky golay filter
        self._window_size = np.nan
        self._savgol_order = np.nan
        self._savgol_cumulative = pd.Series(data=np.nan, name='Savgol Filter CUM CONS.')
        self._savgol_sp_rate = pd.Series(data=np.nan, name='Savogol Filter SP.')

    # Setters
    def set_cumlative(self, cumulative):
        self._cumulative = cumulative

    def set_sp_rate(self, rate):
        self._sp_rate = rate

    # Getters
    def get_name(self):
        return self._name

    def get_conc(self):
        return self._concentration

    def get_time(self):
        return self._run_time
    
    def get_vcc(self):
        return self._vcc

    def get_tcc(self):
        return self._tcc

    def get_viability(self):
        return self._viability

    def get_v_before(self):
        return self._v_before

    def get_cumulative(self):
        return self._cumulative

    def get_sp_rate(self):
        return self._sp_rate
    
    def get_conc_after_feed(self):
        return self._conc_after_feed
    
    def get_run_time_mid(self):
        return self._run_time_mid
    
    def get_conc_mid(self):
        return self._conc_mid
            
class Metabolites(Species):
    def __init__(self,
                 name,
                 run_time,
                 conc,
                 feed_conc,
                 feed_flowrate,
                 viable_cell=pd.Series(data=np.nan, name='VIABLE CELL CONC.'),
                 v_before=pd.Series(data=np.nan, name='VOLUME BEFORE SAMPLING.'),
                 v_after=pd.Series(data=np.nan, name='VOLUME AFTER SAMPLING.'),
                 v_after_feed=pd.Series(data=np.nan, name='VOLUME AFTER SAMPLING.')
                 ):
        
        super().__init__(name, run_time, conc, viable_cell, v_before, v_after, v_after_feed)

        self._feed_concentration = feed_conc
        self._feed_flowrate = feed_flowrate

    # getters
    def get_feed_conc(self):
        return self._feed_concentration

    def get_feed_flowrate(self):
        return self._feed_flowrate

# Plotting for ONE Species obj
def plot(self, concentration=True, cumulative=True, sp_rate=True,
         polyreg=False, savgol=False,
         fig=None, column=1, ax_idx = 1,
         figsize=(8, 6), grid=True, data_num=100):
    # column: 
    # ax_idx: start ax
    
    polyreg_data_num = data_num # number of data for polynomial regression
    f1 = concentration # and self._concentration.any()
    f2 = cumulative # and self._cumulative.any()
    f3 = sp_rate # and self._sp_rate.any()
    factor = f1 + f2 + f3
    if (factor == False):
        return None

    factor = concentration + cumulative + sp_rate
    w, h = figsize
    size = (w*factor, h)
    if (fig==None):
        fig = plt.figure(figsize=size)
    fig.tight_layout(rect=[0,0,1,0.96])

    x = self._run_time  # x axis data
    x2 = np.linspace(x.iat[0], x.iat[-1], polyreg_data_num) # x data for polynomial regression
    

    # Concentration Profile
    if (f1):
        ax = fig.add_subplot(column, factor, ax_idx) # add axis
        y = self._concentration # y axis data

        ax.scatter(x, y, label=(self._name))    # plot
        ax.plot(x, y)

        ax.set_title('Kinetic Curve', loc='left')
        ax.set_ylabel('Concentration (mM)')
        ax.set_xlabel('Time (hrs)')
        ax.legend()
        ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
        ax_idx += 1 # add ax index

    # Cumulative Profile
    if (f2):
        ax = fig.add_subplot(column, factor, ax_idx) # add axis
        y = self._cumulative    # y axis data

        ax.scatter(x, y, label=(self._name))    # plot

        # Add Polynomial Regression Fit on the same graph
        if (self._polyreg_cumulative.any()):
            y2 = self._polyfit_cumulative(x2)

            ax.plot(x2, y2, label=('Poly. Fit. Order:' + str(self._polyreg_order)))

        ax.set_title('Cumulative Curve', loc='left')
        ax.set_ylabel('Cumulative ' + self._name + ' (mmol)')
        ax.set_xlabel('Time (hrs)')
        ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
        ax.legend()
        ax_idx += 1 # add ax index
    
    # SP profile
    if (f3):
        # Two-Point Calc
        ax = fig.add_subplot(column, factor, ax_idx) # add axis
        y = self._sp_rate    # y axis data

        ax.plot(x, y, label=(self._name + '\nTwo-Point Calc.'))    # plot

        ax.set_title('SP. Rate', loc='left')
        ax.set_ylabel('SP. rate (mmol/109 cell/hr)')
        ax.set_xlabel('Time (hrs)')
        ax.legend()
        ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

        # Polynomial Regression
        if (polyreg):
            # ax = fig.add_subplot(column, factor, ax_idx) # add axis
            y2 = self._polyreg_sp_rate

            ax.plot(x, y2, ls=':', label=('Poly. Reg. Fit.\nOrder: ' + str(self._polyreg_order)))   # plot

            # ax.set_title('SP. Rate\nPolynomial Fit Estimate', loc='left')
            ax.set_ylabel('SP. rate (mmol/109 cell/hr)')
            ax.set_xlabel('Time (hrs)')
            ax.legend()
            ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

        # Savgol Filter
        if (savgol):
            # ax = fig.add_subplot(column, factor, ax_idx) # add axis
            y2 = self._savgol_sp_rate

            ax.plot(x, y2, ls='-.', label=('Savgol. Fil.\nOrder: ' + str(self._savgol_order) +\
                                '\nWindow Size: ' + str(self._window_size)))   # plot

            # ax.set_title('SP. Rate\nSavitzky Golay Filter', loc='left')
            ax.set_ylabel('SP. rate (mmol/109 cell/hr)')
            ax.set_xlabel('Time (hrs)')
            ax.legend()
            ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
            
        ax_idx += 1 # add ax index

    fig.suptitle(self._name + ' Profile', fontsize='xx-large')

    return fig

# Add plot method to Species Class
Species.plot = plot


##############################################################################################
################################## Initialization Functions ##################################
##############################################################################################

##############################################################################################
# Returns run time with a unit of day
##############################################################################################
def runTIme_d(dt):
    s = pd.Series([0] * len(dt))
    
    for i in range(len(dt)):
        s.iat[i] = (dt.iat[i] - dt.iat[0]).total_seconds() / 3600 / 24

    return s

##############################################################################################
# returns run time with a unit of hour
##############################################################################################
def runTime_h(dt):
    s = pd.Series([0] * len(dt))
    
    for i in range(len(dt)):
        s.iat[i] = (dt.iat[i] - dt.iat[0]).total_seconds() / 3600

    return s

##############################################################################################
# Returns culture volume befour and after sampling
##############################################################################################
def volumeCalc(df, init_vol):
    v_after_sampling = pd.Series([0] * len(df))
    v_before_sampling = pd.Series([0] * len(df))
    v_after_feeding = pd.Series([0] * len(df))
    v0 = init_vol

    v_before_sampling[0] = v0

    for i in range(len(df)-1):
        v_after_sampling.iat[i] = v_before_sampling.iat[i] - df['SAMPLE VOLUME (mL)'].iat[i]
        v_before_sampling.iat[i+1] = df['FEED MEDIA ADDED (mL)'].iat[i] + df['GLUTAMINE FEED ADDED (mL)'].iat[i] + df['BASE ADDED (mL)'].iat[i] + v_after_sampling.iat[i]
        v_after_feeding.iat[i] = df['FEED MEDIA ADDED (mL)'].iat[i] + df['GLUTAMINE FEED ADDED (mL)'].iat[i] + df['BASE ADDED (mL)'].iat[i] + v_after_sampling.iat[i]

    v_after_sampling.iat[-1] = v_before_sampling.iat[-1] - df['SAMPLE VOLUME (mL)'].iat[-1]
    v_after_feeding.iat[-1] = df['FEED MEDIA ADDED (mL)'].iat[-1] + df['GLUTAMINE FEED ADDED (mL)'].iat[-1] + df['BASE ADDED (mL)'].iat[-1] + v_after_sampling.iat[-1]

    return (v_before_sampling, v_after_sampling, v_after_feeding)


##############################################################################################
# Initialize Data Frame
##############################################################################################
def inializeDF(df_data ,initial_culture_volume=0, feed_status = [0]):
    df = pd.DataFrame()
    df['RUN TIME (DAYS)'] = runTIme_d(df_data["TIME"])
    df['RUN TIME (HOURS)'] = runTime_h(df_data["TIME"])
    df['VOLUEME BEFORE SAMPLING (mL)'], df['VOLUME AFTER SAMPLING (mL)'], df['VOLUME AFTER FEEDING (mL)'] = volumeCalc(df_data, initial_culture_volume)
    df['FEED MEDIA ADDED (mL)'] = df_data['FEED MEDIA ADDED (mL)']
    df['GLUTAMINE ADDED (mL)'] = df_data['GLUTAMINE FEED ADDED (mL)']
    df['BASE ADDED (mL)'] = df_data['BASE ADDED (mL)']
    if len(feed_status) != len(df):
        df['Feed status'] = feed_status * len(df)
    else:
        df['Feed status'] = feed_status

    return df

##############################################################################################
# Initialize Data List
##############################################################################################
def initializeList(df_data, first_column=19, num=23):
    # Extract concentration data frame of amino acids and others
    last_column = first_column + num + 1
    df_conc = df_data.iloc[:, first_column: last_column]

    # Create name list
    aa_lst = [name.replace('*', '').replace(' CONC. (mM)', "").replace(' ', '').upper() for name in df_conc.columns]

    # Create feed name list
    feed_aa_lst = ["FEED %s CONC. (mM)" %i for i in aa_lst]

    return (aa_lst, feed_aa_lst, df_conc)


#####################################################################################################################
################################## Cumulative Concentration Calculatoion Functions ##################################
#####################################################################################################################

#####################################################################################################################
# Integral of Viable Cell Concentration
#####################################################################################################################
def integralViableCell(self, initial_conc=0):
    vcc = self._vcc
    t = self._run_time
    s = pd.Series([initial_conc] * len(t))

    for i in range(1, len(t)):
        s.iat[i] = s.iat[i-1] + (vcc.iat[i] + vcc.iat[i-1]) / 2 * (t.iat[i] - t.iat[i-1])

    self._i_vcc = s

# getter
def get_integral_vcc(self):
    return self._i_vcc


#####################################################################################################################
# Calculate production of cells, and returns the cumulative production.
#
# can be used to calculate IgG production.
#####################################################################################################################
def cumuCellProd(self, initial_conc=0):
    # xv: vialbe cell concentration (10e6 cells/ml) or IgG
    # v1: culture volume before sampling (ml)
    # v2: culture volume after sampling (ml)
    # Cells produced = xv(i) * v(i) - xv(i-1) * v(i-1)
    xv = self._concentration
    v1 = self._v_before
    v2 = self._v_after

    s = pd.Series([initial_conc] * len(xv))

    for i in range(1, len(xv)):
        s.iat[i] = s.iat[i-1] + xv[i] * v1[i] - xv[i-1] * v2[i-1]
    
    self._cumulative = s


#####################################################################################################################
# Calculate Cumulative Oxygen Concentration
#####################################################################################################################
def cumuOxyConc(self, initial_conc=0):
    # oxy: concentration of oxygen
    # v1: culture volume before sampling
    # v2: culture volume after sampling
    oxy = self._concentration
    v1 = self._v_before
    v2 = self._v_after

    s = pd.Series([initial_conc] * len(oxy))

    for i in range(1, len(oxy)):
        s.iat[i] = s.iat[i-1] + (oxy.iat[i] * v1.iat[i] - oxy.iat[i-1] * v2.iat[i-1]) / 1000

    self._cumulative = s


#####################################################################################################################
# Calculate consumption/Production of a substrate, and returns the cumulative consumption/production
#
# to calculate production, function argument must be True -> production=True 
#####################################################################################################################
def cumulativeCons(self, production=False):
    # sf: substrate feed concentration (mM)
    # s: substrate concentration (mM)
    # f: feed flowrate (ml/hr)
    # v1: culture volume before sampling (ml)
    # v2: culture volume after sampling (ml)
    # Consumed substrate = sf*f + s[i-1]*v[i-1] - s[i]*v[i]
    s = self._concentration
    sf = self._feed_concentration
    f = self._feed_flowrate
    v1 = self._v_before
    v2 = self._v_after

    conc0 = 0 # initial concentration
    se = pd.Series([conc0] * len(sf))

    for i in range(1, len(sf)):
        se.iat[i] = se.iat[i-1] + (sf.iat[i] * f.iat[i-1] - s.iat[i] * v1[i] + s.iat[i-1] * v2[i-1]) / 1000

    if (production == True):
        se *= -1

    self._cumulative = se

#####################################################################################################################
# Calculate Cumulative for Nitrogen and AA Carbon
#####################################################################################################################
def cumOthers(spc_dict):
    ala = spc_dict['Alanine'].get_cumulative()
    arg = spc_dict['Arginine'].get_cumulative()
    asn = spc_dict['Asparagine'].get_cumulative()
    asp = spc_dict['Aspartate'].get_cumulative()
    cyt = spc_dict['Cystine'].get_cumulative()
    gln = spc_dict['Glutamine'].get_cumulative()
    glu = spc_dict['Glutamate'].get_cumulative()
    gly = spc_dict['Glycine'].get_cumulative()
    his = spc_dict['Histidine'].get_cumulative()
    iso = spc_dict['Isoleucine'].get_cumulative()
    leu = spc_dict['Leucine'].get_cumulative()
    lys = spc_dict['Lysine'].get_cumulative()
    met = spc_dict['Methionine'].get_cumulative()
    nh3 = spc_dict['NH3'].get_cumulative()
    phe = spc_dict['Phenylalanine'].get_cumulative()
    pro = spc_dict['Proline'].get_cumulative()
    ser = spc_dict['Serine'].get_cumulative()
    thr = spc_dict['Threonine'].get_cumulative()
    tryp = spc_dict['Tryptophan'].get_cumulative()
    tyr = spc_dict['Tyrosine'].get_cumulative()
    val = spc_dict['Valine'].get_cumulative()

    # Calculate cumulative consumption
    # NITROGEN
    nitrogen_cum = (ala*1 + arg*4 + asn*2 + asp*1 + cyt*2 + gln*2 + glu*1 + gly*1 +\
                    his*3 + iso*1 + leu*1 + lys*2 + met*1 - nh3*1 + phe*1 + pro*1 +\
                    ser*1 + thr*1 + tryp*2 + tyr*1 + val*1)
    # NITROGEN (w/o NH3, Ala)
    nitrogen_w_o_NH3_Ala_cum = (ala*1 + nh3*1 + nitrogen_cum)
    # AA CARBON
    aa_carbon_cum = (-ala*3 + arg*6 + asn*4 + asp*4 + cyt*6 + gln*5 + glu*5 + gly*2 +\
                 his*6 + iso*6 + leu*6 + lys*6 + met*5 + phe*9 + pro*5 + ser*3 +\
                 thr*4 + tryp*11 + tyr*9 + val*5)

    # return df
    return (nitrogen_cum, nitrogen_w_o_NH3_Ala_cum, aa_carbon_cum)


#####################################################################################################################
# Cumulative Calculations
#####################################################################################################################
def cumulativeCalc(df_data, init_df, AA_lst):
    # name and feed name list, and concentration df for amino acids
    aa_lst, feed_aa_lst, df_aa_conc = AA_lst

    # dictionary for species
    spc_dict = {}

    # Necessary variables
    v1 = init_df['VOLUEME BEFORE SAMPLING (mL)']    # culture volume before sampling (mM)
    v2 = init_df['VOLUME AFTER SAMPLING (mL)']      # culture volume after sampling (mM)
    v3 = init_df['VOLUME AFTER FEEDING (mL)']      # culture volume after sampling (mM)
    f = init_df['FEED MEDIA ADDED (mL)']            # feed flowrate (ml/hr)
    t = init_df['RUN TIME (HOURS)']                 # run time (hrs)
    # Initialize DF
    df = pd.DataFrame()
    df_feed = pd.DataFrame() # Concentration After Feeding

######################################## Calculations about Cells ########################################
    vcc = df_data['VIABLE CELL CONC. XV (x106 cells/mL)']
    viability=df_data['VIABILITY (%)']
    tcc=vcc/df_data['VIABILITY (%)']
    cell = Species('Cell', run_time=t, conc=vcc, viable_cell=vcc, v_before=v1, v_after=v2, v_after_feed=v3, viability=viability, total_cell=tcc)
    vcc_0 = 0 # initial cell concentration

    # Add methods to cell obj
    cell.calc_ivcc = types.MethodType(integralViableCell, cell)
    cell.get_ivcc = types.MethodType(get_integral_vcc, cell)
    cell.calc_cumulative = types.MethodType(cumuCellProd, cell)

    # Calculate integral of vialble cell concentraion
    cell.calc_ivcc(initial_conc=vcc_0)
    # Calculate cumulative cells Produced
    cell.calc_cumulative(initial_conc=vcc_0)

    # Add IVCC to df
    df['INTEGRAL OF VIABLE CELL CONC. IVCC (x106 cells hr/mL)'] = cell.get_ivcc()
    # Add Cumulative Cells Produced to df
    df['CUM CELLS PROD. (x106 cells)'] = cell.get_cumulative()
    # Add cell obj to sp_dict
    spc_dict['Cell'] = cell

######################################## Calculations about Oxygen ########################################
    # Oxygen consumed
    oxy_c = df_data['OXYGEN CONSUMED (mmol/L)'] # oxygen concentraion
    oxy = Species('Oxygen', run_time=t, conc=oxy_c, viable_cell=vcc, v_before=v1, v_after=v2, v_after_feed=v3)
    oxy_0 = 0     # initial concentration
    
    # Add method to oxy obj
    oxy.calc_cumulative_oxy = types.MethodType(cumuOxyConc, oxy)

    # Calculate cumulative oxygen consumed
    oxy.calc_cumulative_oxy(oxy_0)

    # Add cumulative oxygen to df
    df['CUM OXYGEN CONS. (mmol)'] = oxy.get_cumulative()

    # Add oxygen obj to dictionary
    spc_dict['Oxygen'] = oxy

######################################## Calculations about Oxygen ########################################
    # IgG Produced
    xv = df_data['IgG CONC. (mg/L)']    # IgG concentraion
    igg = Species('IgG', run_time=t, conc=xv, viable_cell=vcc, v_before=v1, v_after=v2, v_after_feed=v3)
    igg_0 = 0     # initial concentration

    # Add method to igg obj
    igg.calc_cumulative_igg = types.MethodType(cumuCellProd, igg)

    # Calculate cumulative IgG production
    igg.calc_cumulative_igg(igg_0)

    # Adjust unit to mg
    igg.set_cumlative(igg.get_cumulative() / 1000)

    # Add cumulative IgG to df
    df['CUM IgG PROD. (mg)'] = igg.get_cumulative()

    # Add igg obj to dictionary
    spc_dict['IgG'] = igg

######################################## Calculations about Amino Acids ########################################
    # Add method to Metabolites class
    Metabolites.calc_cumulative = cumulativeCons
    Metabolites.calc_conc_after_feed = conc_after_feeding_calc
    Metabolites.mid_calc = mid_calc_conc_runtime

    for i, name in enumerate(aa_lst):
        s = df_aa_conc.iloc[:, i].squeeze()     # species concentration
        sf = df_data[feed_aa_lst[i]]   # feed concentraion

        # Create metabolite object 
        if name.capitalize() == 'Glutamine':
            glucose = init_df['GLUTAMINE ADDED (mL)']
            meta = Metabolites(name.upper(),
                               run_time=t,
                               conc=s,
                               feed_conc=sf,
                               feed_flowrate=glucose,
                               viable_cell=vcc,
                               v_before=v1,
                               v_after=v2,
                               v_after_feed=v3)
        else:
            meta = Metabolites(name.upper(),
                               run_time=t,
                               conc=s,
                               feed_conc=sf,
                               feed_flowrate=f,
                               viable_cell=vcc,
                               v_before=v1,
                               v_after=v2,
                               v_after_feed=v3)
           
        # Calculate cumulative consumption/production
        if name.capitalize() == 'Lactate':
            meta.calc_cumulative(production=True)
        else:
            meta.calc_cumulative()

        # Add metabolite obj to dictionary
        spc_dict[name.capitalize().replace('Nh3', 'NH3')] = meta

        # Add cumulative consumption to DF
        df['CUM. ' + name.upper() +' (mmol)'] = meta.get_cumulative()
        
        # Calculate conc. after feeding and add it to DF
        meta.calc_conc_after_feed()
        df_feed['CONC. ' + name.upper() +' (mM), after feeding'] = meta.get_conc_after_feed()
        
        # mid-clac
        meta.mid_calc()
        # df['CONC. ' + name.upper() +' (mM), mid'] = meta.get_conc_mid()
        
        # ##### Concentration After Feeding
        # # concentration = (concentration * volume after feed + feed concentration * feed added) / (volume after feed + feed added + glutamine added)
        # # after feed
        # g = init_df['GLUTAMINE ADDED (mL)']
        # df_feed[name.upper() +' (mmol)\nafter feeding'] = (s*v2  + sf*f) / (v2 + f + g)

######################################## Calculations about Others ########################################
    # Create Species obj for Nitrogen, Nitrogen (w/o NH3, Ala), and AA Carbon
    nitrogen = Species('Nitrogen', run_time=t, viable_cell=vcc, v_before=v1, v_after=v2, v_after_feed=v3)    # NITROGEN
    nitrogen_w_o_NH3_Ala = Species('Nitrogen (w/o NH3, Ala)', run_time=t, viable_cell=vcc, v_before=v1, v_after=v2, v_after_feed=v3) # NITROGEN (w/o NH3, Ala)
    aa_carbon = Species('AA Carbon', run_time=t, viable_cell=vcc, v_before=v1, v_after=v2, v_after_feed=v3)    # AA CARBON

    # Calculate cumulative consumption for Nitrogen, Nitrogen (w/o NH3, Ala), and AA Carbon
    nitrogen_cum, nitrogen_w_o_NH3_Ala_cum, aa_carbon_cum = cumOthers(spc_dict)

    # Add cumulative consumption
    nitrogen.set_cumlative(nitrogen_cum)                            # NITROGEN
    nitrogen_w_o_NH3_Ala.set_cumlative(nitrogen_w_o_NH3_Ala_cum)    # NITROGEN (w/o NH3, Ala)
    aa_carbon.set_cumlative(aa_carbon_cum)                          # AA CARBON

    # Add objs to dictionary
    spc_dict['Nitrogen'] = nitrogen
    spc_dict['Nitrogen (w/o NH3, Ala)'] = nitrogen_w_o_NH3_Ala
    spc_dict['AA Carbon'] = aa_carbon

    # Add cumulative consumption to DF
    df['CUM. Nitrogen (mmol)'] = nitrogen.get_cumulative()
    df['CUM. Nitrogen (w/o NH3, Ala) (mmol)'] = nitrogen_w_o_NH3_Ala.get_cumulative()
    df['CUM. AA Carbon'] = aa_carbon.get_cumulative()

    return (spc_dict, pd.concat([df, df_feed], axis=1))


##########################################################################################################
################################## Specific Rate Calculatoion Functions ##################################
##########################################################################################################

##########################################################################################################
# Calculate SP Rate for Oxygen
##########################################################################################################

# SP. Oxygen Uptake Rate
def sp_OUR(self, our):
    self._sp_our = our / self._vcc
    self._sp_our.iat[0] = np.nan

# getter
def get_sp_OUR(self):
    return self._sp_our

# SP. Oxygen Consumption Rate
def spOxyConsRate(self, rate, oxy_cons):
    # t: run time (hrs)
    # v1: culture volume before sampling (mL)
    # v2: culture volume after sampling (mL)
    t = self._run_time
    v1 = self._v_before
    v2 = self._v_after

    for i in range(1, len(t)):
        if rate.iat[i] < 0:
            x = oxy_cons.iat[i]*v1.iat[i] - oxy_cons.iat[i-1]*v2.iat[i-1]
            y = (self._vcc.iat[i]*v1.iat[i] + self._vcc.iat[i-1]*v1.iat[i-1])*1000000*0.5*(t.iat[i] - t.iat[i-1])
            rate.iat[i] = x / 1000 / y *1000000000

    rate.iat[0] = np.nan
    self._sp_rate = rate

##########################################################################################################
# Calculates Specific growth rate
##########################################################################################################
def spGrowthRate(self):
    # vcc: Viable Cell Concentration (10e6 cells/mL)
    # cum_cell: Cumulative Cell Concentraion (10e6 cells/mL)
    # t: run time (hrs)
    # v1: culture volume before sampling (mL)
    # v2: culture volume after sampling (mL)
    t = self._run_time
    cum_cell = self._cumulative
    v1 = self._v_before
    v2 = self._v_after

    rate = pd.Series([np.nan] * len(t)) # Initialize
    
    for i in range(1, len(t)):
        x = cum_cell.iat[i] - cum_cell.iat[i-1]
        y = self._vcc.iat[i]*v1.iat[i] + self._vcc.iat[i-1]*v2.iat[i-1]
        rate.iat[i] = x / (y*0.5*(t.iat[i]-t.iat[i-1]))
    self._sp_g_rate = rate

# getter 
def get_sp_growth_rate(self):
    return self._sp_g_rate

##########################################################################################################
# Calculates kd value
##########################################################################################################
def kd(self, dead_cell):
    # vcc: Viable Cell Concentration (10e6 cells/mL)
    # dcc: Dead Cell Concentration (10e6 cells/mL)
    # t: run time (hrs)
    # v1: culture volume before sampling (mL)
    # v2: culture volume after sampling (mL)
    dcc = dead_cell
    t = self._run_time
    v1 = self._v_before
    v2 = self._v_after

    rate = pd.Series([np.nan] * len(t))

    for i in range(1, len(t)):
        x = dcc.iat[i]*v1.iat[i] - dcc.iat[i-1]*v2.iat[i-1]
        y = self._vcc.iat[i]*v1.iat[i] + self._vcc.iat[i-1]*v2.iat[i-1]
        rate.iat[i] = x / (y*0.5*(t.iat[i]-t.iat[i-1]))
        
    self._kd_val = rate

# getter
def get_kd(self):
    return self._kd_val

##########################################################################################################
# Calculate mv
##########################################################################################################
def mv(self):
    self._mv_val = self._sp_g_rate + self._kd_val

# getter
def get_mv(self):
    return self._mv_val
    
##########################################################################################################
# Calculate Specific Rate
##########################################################################################################
def rateCalc(self):
    # s: substrate concentration (mM)
    # vcc: Viable Cell Concentration (10e6 cells/mL)
    # t: run time (hrs)
    # v1: culture volume before sampling (mL)
    # v2: culture volume after sampling (mL)
    s = self._cumulative
    t = self._run_time
    v1 = self._v_before
    v2 = self._v_after
    vcc = self._vcc
    
    rate = pd.Series([np.nan] * len(t))

    for i in range(1, len(t)):
        x = (s.iat[i] - s.iat[i-1]) * 1000
        y = vcc.iat[i]*v1.iat[i] + vcc.iat[i-1]*v2.iat[i-1]
        rate.iat[i] = x / (y*0.5*(t.iat[i]-t.iat[i-1]))

    self._sp_rate = rate

##########################################################################################################
# Calculate Specific Rate for Nitrogne and AA carbon
##########################################################################################################
def qOthersCalc(df):
    qAla = df['qAlanine']
    qArg = df['qArginine']
    qAsn = df['qAsparagine']
    qAsp = df['qAspartate']
    qCys = df['qCystine']
    qGln = df['qGlutamine']
    qGlu = df['qGlutamate']
    qGly = df['qGlycine']
    qHis = df['qHistidine']
    qIso = df['qIsoleucine']
    qLeu = df['qLeucine']
    qLys = df['qLysine']
    qMet = df['qMethionine']
    qNh3 = df['qNh3']
    qPhe = df['qPhenylalanine']
    qPro = df['qProline']
    qSer = df['qSerine']
    qThr = df['qThreonine']
    qTry = df['qTryptophan']
    qTyr = df['qTyrosine']
    qVal = df['qValine']

    # Nitrogen
    x = qAla*1 + qArg*4 + qAsn*2 + qAsp*1 + qCys*1
    y = qGln*2 + qGlu*1 + qGly*1 + qHis*3 + qIso*1
    z = qLeu*1 + qLys*2 + qMet*1 - qNh3 + qPhe*1 + qPro*1
    w = qSer*1 + qThr*1 + qTry*1 + qTyr*1 + qVal*1

    qNitrogen = x + y + z + w

    # Nitrogen (w/o NH3, Ala)
    qNitrogen_w_o_NH3_Ala = -qAla*1 + qNh3*1 + qNitrogen

    # aaC (mmol/109 cells/hr)
    x = qAla*3 + qArg*6 + qAsn*4 + qAsp*4 + qCys*6
    y = qGln*5 + qGlu*5 + qGly*2 + qHis*6 + qIso*6
    z = qLeu*6 + qLys*6 + qMet*5 + qPhe*9 + qPro*5 + qSer*3 + qThr*4 + qTry*4 + qTyr*9 + qVal*5
    qaac = x + y + z

    # aaC (consumption only)
    x = qAla.abs()*3 + qArg.abs()*6 + qAsn.abs()*4 + qAsp.abs()*4 + qCys.abs()*6
    y = qGln.abs()*5 + qGlu.abs()*5 + qGly.abs()*2 + qHis.abs()*6 + qIso.abs()*6
    z = qLeu.abs()*6 + qLys.abs()*6 + qMet.abs()*5 + qPhe.abs()*9 + qPro.abs()*5 + qSer.abs()*3 + qThr.abs()*4 + qTry.abs()*4 + qTyr.abs()*9 + qVal.abs()*5

    qaac_cons = (x + y + z + qaac) / 2

    return (qNitrogen, qNitrogen_w_o_NH3_Ala, qaac, qaac_cons)

##########################################################################################################
# Additional method and member for AA carbon
##########################################################################################################
def set_sp_rate_cons_only(self, sp_rate):
    self._sp_rate_cons_only = sp_rate

def get_sp_rate_cons_only(self):
    return self._sp_rate_cons_only

##########################################################################################################
#
##########################################################################################################
def specificRate(df_data, df_init, spc_dict, AA_lst):
    # Initialize data frame
    df = pd.DataFrame()

    # name list for amino acids and others
    aa_lst = AA_lst[0]

    # Necessary variables
    v1 = df_init['VOLUEME BEFORE SAMPLING (mL)']    # culture volume before sampling (mM)
    v2 = df_init['VOLUME AFTER SAMPLING (mL)']      # culture volume after sampling (mM)
    f = df_init['FEED MEDIA ADDED (mL)']            # feed flowrate (ml/hr)
    t = df_init['RUN TIME (HOURS)']                 # run time (hrs)
    vcc = df_data['VIABLE CELL CONC. XV (x106 cells/mL)']   # viable cell concentraion
    dcc = df_data['DEAD CELL CONC. Xd (x106 cells/mL)']     # dead cell concentraion
    our = df_data['OUR (mmol/L/hr)']
    oxy_cons_rate = df_data['SP. OXYGEN CONSUMPTION RATE (mmol/109cell/hr)']
    oxy_consmed = df_data['OXYGEN CONSUMED (mmol/L)']

######################################## Calculations about Oxygen ########################################
    # Oxygen obj
    oxy = spc_dict['Oxygen']

    # Add method to Oxygen obj
    oxy.calc_sp_OUR = types.MethodType(sp_OUR, oxy)
    oxy.get_sp_OUR = types.MethodType(get_sp_OUR, oxy)
    oxy.calc_sp_rate = types.MethodType(spOxyConsRate, oxy)

    # Calculate SP. OUR
    oxy.calc_sp_OUR(our)
    # Calculate SP. Rate
    oxy.calc_sp_rate(rate=oxy_cons_rate, oxy_cons=oxy_consmed)

    # Add calculations to df
    df['SP. OUR (mmol/109 cells/hr)'] = oxy.get_sp_OUR()
    df['SP. OXYGEN CONSUMPTION RATE (mmol/109cell/hr)'] = oxy.get_sp_rate()

######################################## Calculations about Cells ########################################
    # Cell obj
    cell = spc_dict['Cell']

    # Add method to Cell obj
    cell.calc_sp_GRate = types.MethodType(spGrowthRate, cell)
    cell.calc_kd = types.MethodType(kd, cell)
    cell.calc_mv = types.MethodType(mv, cell)
    cell.get_sp_growth_rate = types.MethodType(get_sp_growth_rate, cell)
    cell.get_kd = types.MethodType(get_kd, cell)
    cell.get_mv = types.MethodType(get_mv, cell)

    # Calculations
    cell.calc_sp_GRate()
    cell.calc_kd(dead_cell=dcc)
    cell.calc_mv()

    # Add calculations to df
    df['SP. GROWTH RATE, m (hr-1) [mv-kd]'] = cell.get_sp_growth_rate()
    df['kd'] = cell.get_kd()
    df['mv'] = cell.get_mv()

######################################## Calculations about Iger_feedG ########################################
    # IgG obj
    igg = spc_dict['IgG']

    # Add method to Cell obj
    igg.calc_sp_rate = types.MethodType(rateCalc, igg)

    # Calculation
    igg.calc_sp_rate()

    # Add calculation to df
    df['qIgG (mg/109 cell/hr)'] = igg.get_sp_rate()

######################################## Calculations about Metabolites ########################################
    # Add method to Metabolite class
    Metabolites.calc_sp_rate = rateCalc

    for name in aa_lst:
        # Rename: 'ALANINE' -> 'Alanine'
        name = name.capitalize().replace('Nh3', 'NH3')
        
        # Metabolite obj
        meta = spc_dict[name]

        # Calculate sp rate
        meta.calc_sp_rate()

        # Add calculation to df
        df['q' + name.capitalize()] = meta.get_sp_rate()
        
    # obj for others
    nitrogen = spc_dict['Nitrogen']
    nitrogen_w_o_NH3_ala = spc_dict['Nitrogen (w/o NH3, Ala)']
    aa_carbon = spc_dict['AA Carbon']

    # Add member to aa_corbon obj for sp rate (consumprion only)
    aa_carbon.set_sp_rate_cons_only = types.MethodType(set_sp_rate_cons_only, aa_carbon)
    aa_carbon.get_sp_rate_cons_only = types.MethodType(get_sp_rate_cons_only, aa_carbon)

    # Calculate sp rate for Others
    qNit, qNit_aln, qaac, qaac_cons = qOthersCalc(df)

    # Add calculations to dictionary
    nitrogen.set_sp_rate(qNit)
    nitrogen_w_o_NH3_ala.set_sp_rate(qNit_aln)
    aa_carbon.set_sp_rate(qaac)
    aa_carbon.set_sp_rate_cons_only(qaac_cons)

    # Add calculations to df
    df['qNitrogen'] = qNit
    df['qNitrogen (w/o NH3, Ala)'] = qNit_aln
    df['qaaC'] = qaac
    df['qaaC (consumption only)'] = qaac_cons

    # Rename
    df.columns = ['Two-Point Calc.\n' + name.replace('Nh3', 'NH3') + ' (mmol/109 cell/hr)' for name in df.columns]

    # Ratio Caluculaions
    # DL/DG
    dL = spc_dict['Lactate'].get_sp_rate()
    dG = spc_dict['Glucose'].get_sp_rate()
    df['DL/DG (mmol/mmol)'] = dL / dG

    # qO2/qGlc
    qO2 = oxy_cons_rate
    qGlc = dG
    df['qO2/qGlc (mmol/mmol)'] = qO2 / qGlc

    # qGln/qGlc
    qGln = spc_dict['Glutamine'].get_sp_rate()
    df['qGln/qGlc (mmol/mmol)'] = qGln / qGlc

    # qNH3/qGln
    qNH3 = spc_dict['NH3'].get_sp_rate()
    df['qNH3/qGln (mmol/mmol)'] = qNH3 / qGln

    return (spc_dict, df)

##############################################################################################
# Calc. of concentration after feeding
##############################################################################################
def conc_after_feeding_calc(self):
    # sf: substrate feed concentration (mM)
    # s: substrate concentration (mM)
    # vf: feed volume (ml)
    # v2: culture volume after sampling (ml)
    # v3: culture volume after feeding (ml)
    # conc_after_feed[i] = (v2[i] * s[i] + vf[i] * sf[i])/v3[i]
    s = self._concentration
    sf = self._feed_concentration
    f = self._feed_flowrate
    v2 = self._v_after
    v3 = self._v_after_feed
    v_af  = (s* v2 + sf*f)/v3
    self._conc_after_feed = v_af

##############################################################################################
# Mid-point calculation of conc. and run time
##############################################################################################
def mid_calc_conc_runtime(self):
    # c1: conc after feeding at t
    # c2: measured conc at t + 1
    c1 = self._conc_after_feed
    c2 = self._concentration   
    t = self._run_time
    
    t_mid = pd.Series([np.nan] * (len(t)-1))
    c_mid = pd.Series([np.nan] * (len(t)-1))
    for i in range(len(t_mid)):
        t_mid.iat[i] = (t.iat[i] + t.iat[i+1])/2
        c_mid.iat[i] = (c1.iat[i]+c2.iat[i+1])/2

    self._run_time_mid = t_mid
    self._conc_mid = c_mid

############################################################################################
################################### In Process Function ###################################
############################################################################################

def inProcessCalc(df_measured_data, feed_status, initial_volume, first_column, num_aa):

    # Initailize Output Data Frame
    init_df = inializeDF(df_measured_data, initial_culture_volume=initial_volume, feed_status=feed_status)

    # Initialize Species dictionary {'Species name': 'Species object'}
    ############################################################################################
    # Some useful methods
    # spc_dict['ALANINE'].get_concentration      :returns mesured concentration (pd.Series)
    # spc_dict['ALANINE'].get_feed_concentration :returns mesured feed concentration (pd.Series)
    # spc_dict['ALANINE'].get_cum_concentration  :returns cumulative concentraion (pd.Series)
    # spc_dict['ALANINE'].get_sp_rate            :returns specific rate(pd.Series)
    ############################################################################################

    # AA_tuple = (aa_lst, aa_feed_lst, df_conc): aino acids name list, feed name list, concentration df
    AA_tuple = initializeList(df_data=df_measured_data, first_column=first_column, num=num_aa)

    # Cumulative Consumption/Production Data Frame
    spc_dict, df_cumulative = cumulativeCalc(df_measured_data, init_df, AA_tuple)

    # Specific Rate Data Frame
    spc_dict, df_sp_rate = specificRate(df_measured_data, init_df, spc_dict, AA_tuple)

    # In Process Calc Data Frame
    in_process_calc_df = pd.concat([init_df, df_cumulative, df_sp_rate], axis=1)

    # Split
    aa_lst, aa_feed_lst, df_conc = AA_tuple

    return (aa_lst, spc_dict, pd.concat([init_df, in_process_calc_df], axis=1))

    # Save
    # output_df.to_excel(output_file_path, sheet_name=output_sheet_name, index=False)

#############################################################################################
############################## Polynomial Regression Functions ##############################
#############################################################################################

#############################################################################################
# Polynomial Regression
#############################################################################################
def poly_regression(self, polyreg_order=3):
    x = self._run_time
    y = self._cumulative
    vcc = self._vcc
    v = self._v_before

    self._polyreg_order = polyreg_order # Polynomial Regression Order

    # Polynomial Regression for Cumulative Consumption/Production
    fit = np.polyfit(x, y, polyreg_order)  # Fitting data to polynomial Regression (Get slopes)
    p = np.poly1d(fit)  # Get polynomial curve for Cumulative Consumption/Production

    dp1 = p.deriv()      # first derivetive of polynomial fit

    dy = dp1(x)      # derivetive values corresponding to x

    # Calculate Specific Rate from Derivetive of Polynomial Regression on Cumularive Consumption/Production
    q = pd.Series([np.nan] * len(x))

    # Calculate SP. rate
    for i in range(1, len(x)):
        q.iat[i] = dy[i] / (vcc.iat[i] * v.iat[i]) * 1000

    self._polyreg_cumulative = p(x) # Get Polynomial Fit Cumulative Consumption/Production corresponding x values
    self._polyreg_sp_rate = q   # Polynomial Fit SP. rate
    self._polyfit_cumulative = p # For plotting

# Setter for SP. Oxygen Consumption Rate
def set_polyreg_sp_OUR(self, poly_sp_our):
    self._polyreg_sp_rate = poly_sp_our

# Getters
def get_polyreg_cumulative(self):
    return self._polyreg_cumulative

def get_polyreg_sp_rate(self):
    return self._polyreg_sp_rate

def get_polyreg_order(self):
    return self._polyreg_order

# Add method to Species Class
Species.poly_regression = poly_regression
Species.get_polyreg_cumulative = get_polyreg_cumulative
Species.get_polyreg_sp_rate = get_polyreg_sp_rate
Species.get_polyreg_order = get_polyreg_order

# Ratio Caluculaions
def ratioCalcPolyReg(spc_dict):
    df = pd.DataFrame()
    
    # DL/DG
    dL = spc_dict['Lactate'].get_polyreg_sp_rate()
    dG = spc_dict['Glucose'].get_polyreg_sp_rate()
    df['DL/DG (mmol/mmol)'] = dL / dG

    # qO2/qGlc
    qO2 = spc_dict['Oxygen'].get_polyreg_sp_rate()
    qGlc = dG
    df['qO2/qGlc (mmol/mmol)'] = qO2 / qGlc

    # qGln/qGlc
    qGln = spc_dict['Glutamine'].get_polyreg_sp_rate()
    qGlc = dG
    df['qGln/qGlc (mmol/mmol)'] = qGln / qGlc

    # qNH3/qGln
    qNH3 = spc_dict['NH3'].get_polyreg_sp_rate()
    qGln = qGln 
    df['qNH3/qGln (mmol/mmol)'] = qNH3 / qGln

    return df

# 
def polynomialRegressionCalc(df_measured_data, spc_dict):
    df = pd.DataFrame() # Initialize

    # About Polynomial Regression
    poly_reg_order_dict = {'AA Carbon': 3, 'Alanine': 3, 'IgG': 3, 'Arginine': 3, 'Asparagine': 4,
                           'Aspartate': 4, 'Cell': 3, 'Cystine': 3, 'Ethanolamine': 3, 'Glucose': 4,
                           'Glutamine': 3, 'Glutamate': 4,'Glycine': 3, 'Histidine': 3, 'Isoleucine': 3,
                           'Lactate': 5, 'Leucine': 3, 'Lysine': 3, 'Methionine': 3, 'NH3': 3, 'Nitrogen': 3,
                           'Nitrogen (w/o NH3, Ala)': 3, 'Oxygen': 3, 'Phenylalanine': 3, 'Proline': 3,
                           'Serine': 3, 'Threonine': 3, 'Tryptophan': 3, 'Tyrosine': 3, 'Valine': 3}

    # SP. OXYGEN CONSUMPTION RATE
    ocr = df_measured_data['SP. OXYGEN CONSUMPTION RATE (mmol/109cell/hr)']

    # Calculate Polynomial Regression
    for name, order in poly_reg_order_dict.items():
        # order = 3
        spc = spc_dict[name]
        spc.poly_regression(polyreg_order=order)
        unit = ' (mmol/10e9 cells/hr)'

        # Sp. Oxygen Consumption Rate
        if name == 'Oxygen':
            spc.set_polyreg_sp_OUR = types.MethodType(set_polyreg_sp_OUR, spc)
            ocr.mask(ocr <= 0, spc.get_polyreg_sp_rate())
            spc.set_polyreg_sp_OUR(ocr)
            df['SP. OUR (mmol/10e9 cells/hr)'] = spc.get_polyreg_sp_rate()

        # Change unit for IgG    
        elif name == 'IgG':
            unit = ' (mg/10e9 cells/hr)'
            df['q' + name + unit] = spc.get_polyreg_sp_rate()

        else:
            df['q' + name +unit] = spc.get_polyreg_sp_rate()
    # Rename
    df.columns = ['Poly. Regression\n' + name for name in df.columns]

    # Ratio Calculation
    df_ratio = ratioCalcPolyReg(spc_dict)

    return pd.concat([df, df_ratio], axis=1)



#############################################################################################
############################## Savitzky Golay Filter Functions ##############################
#############################################################################################

# Calcultate Cumulative Consumption/Production
# and SP. Rate with Savitzky Golay filter
def savgolFilter(self, polyorder, window):
    t = self._run_time
    vcc = self._vcc
    v = self._v_before
    y = self._cumulative
    # order = self._polyreg_order
    self._window_size = window
    self._savgol_order = polyorder
    

    dt = t[1] - t[0]

    # Calcultate cumulative consumption/production
    p = savgol_filter(y, window_length=window, polyorder=polyorder) # cumulative numpy list
    self._savgol_cumulative = pd.Series(p)  # cumulative df

    # initialize df
    q = pd.Series([np.nan] * len(t)) 

    # 1st derivetive of cumulatie curve numpy list
    dpdt = savgol_filter(y, window_length=window, polyorder=polyorder, deriv=1, delta=dt)   
    
    # Calculate SP. rate
    for i in range(1, len(t)):
        q.iat[i] = dpdt[i] / (vcc.iat[i] * v.iat[i]) * 1000

    self._savgol_sp_rate = q

# Setter for SP. Oxygen Consumption Rate
def set_savgol_sp_OUR(self, poly_sp_our):
    self._polyreg_sp_rate = poly_sp_our

# Getters
def get_savgol_cumulative(self):
    return self._savgol_cumulative

def get_savgol_sp_rate(self):
    return self._savgol_sp_rate

# Add method to Species Class
Species.savgolFilter = savgolFilter
Species.get_savgol_cumulative = get_savgol_cumulative
Species.get_savgol_sp_rate = get_savgol_sp_rate

# Ratio Caluculaions
def ratioCalcSavgol(spc_dict):
    df = pd.DataFrame()
    
    # DL/DG
    dL = spc_dict['Lactate'].get_savgol_sp_rate()
    dG = spc_dict['Glucose'].get_savgol_sp_rate()
    df['DL/DG (mmol/mmol)'] = dL / dG

    # qO2/qGlc
    qO2 = spc_dict['Oxygen'].get_savgol_sp_rate()
    qGlc = dG
    df['qO2/qGlc (mmol/mmol)'] = qO2 / qGlc

    # qGln/qGlc
    qGln = spc_dict['Glutamine'].get_savgol_sp_rate()
    qGlc = dG
    df['qGln/qGlc (mmol/mmol)'] = qGln / qGlc

    # qNH3/qGln
    qNH3 = spc_dict['NH3'].get_savgol_sp_rate()
    qGln = qGln 
    df['qNH3/qGln (mmol/mmol)'] = qNH3 / qGln

    return df


#
def savgolFilterCalc(df_measured_data, spc_dict, polyorder=3, window_size=5):
    df = pd.DataFrame() # Initialize

    # SP. OXYGEN CONSUMPTION RATE
    ocr = df_measured_data['SP. OXYGEN CONSUMPTION RATE (mmol/109cell/hr)']

    # Calculate Polynomial Regression
    for name, spc in spc_dict.items():

        spc.savgolFilter(polyorder=polyorder, window=window_size)
        unit = ' (mmol/10e9 cells/hr)'

        # Sp. Oxygen Consumption Rate
        if name == 'Oxygen':
            spc.set_savgol_sp_OUR = types.MethodType(set_savgol_sp_OUR, spc)
            ocr.mask(ocr <= 0, spc.get_savgol_sp_rate())
            spc.set_savgol_sp_OUR(ocr)
            df['SP. OUR (mmol/10e9 cells/hr)'] = spc.get_savgol_sp_rate()

        # Change unit for IgG    
        elif name == 'IgG':
            unit = ' (mg/10e9 cells/hr)'
            df['q' + name + unit] = spc.get_savgol_sp_rate()

        else:
            df['q' + name +unit] = spc.get_savgol_sp_rate()

    # Rename
    df.columns = ['Savgol Filter\nPoly. Order: ' + str(polyorder) + '\nWindow Size: ' + str(window_size) + '\n' + name for name in df.columns]

    # Ratio Calculation
    df_ratio = ratioCalcSavgol(spc_dict)

    return pd.concat([df, df_ratio], axis=1)


############################################################################################
# Read a value in a specific cell from Excel 
############################################################################################
def read_value_from_excel(filename, sheet_name=None, column="A", row=1):
    """Read a single cell value from an Excel file"""
    if sheet_name == None:
        out = pd.read_excel(filename, skiprows=row - 1, usecols=column, nrows=1, header=None, names=["Value"]).iloc[0]["Value"]
    else:
        out = pd.read_excel(filename, sheet_name=sheet_name, skiprows=row - 1, usecols=column, nrows=1, header=None, names=["Value"]).iloc[0]["Value"]

    return out


def preProcess(input_file_path, sheet_name=None, cell_line=1, input_header_num=5, first_column=19, num_aa=23,
                feed_status=[0]):
    if (sheet_name):
        # Experiment NO.
        exp_no = read_value_from_excel(input_file_path, sheet_name=sheet_name, column='B', row=1)
        # Initial Culture Volume
        initial_volume = read_value_from_excel(input_file_path, sheet_name=sheet_name, column='B', row=4)
        # Read an Excel file as a Data Frame
        df_measured_data = pd.read_excel(io=input_file_path, sheet_name=sheet_name, header=input_header_num)

    else:
        # Experiment NO.
        exp_no = read_value_from_excel(input_file_path, column='B', row=1)
        # Initial Culture Volume
        initial_volume = read_value_from_excel(input_file_path, column='B', row=4)
        # Read an Excel file as a Data Frame
        df_measured_data = pd.read_excel(io=input_file_path, header=input_header_num)

    # Filling missing data with values of 0
    df_measured_data = df_measured_data.fillna(value=0)

    # In Process Calculations
    aa_lst, spc_dict, in_process_calc_df = inProcessCalc(df_measured_data,
                                                         feed_status,
                                                         initial_volume,
                                                         first_column,
                                                         num_aa)

    # Column of Cell Line number to Measured Data
    cl = pd.Series(data=['CL'+str(cell_line)] * len(in_process_calc_df), name='Cell Line')

    # Add data to Cell Line
    bioP = BioProcess(cell_line=cell_line,
                     measured_data=pd.concat([cl, df_measured_data], axis=1),   # Add cell line number column
                     in_process=in_process_calc_df,
                     species_list=aa_lst,
                     species_dict=spc_dict)
    
    print(exp_no + ' completed')
    
    return (bioP, exp_no, aa_lst)


# Save in process DF in Excell with Sheet name of 'In Process Calc.'
def saveExcell(data, output_file_path):
    
    with pd.ExcelWriter(output_file_path) as writer:
        for key, value in data.items():
            value.get_bioprocess_df().to_excel(writer, sheet_name=key, index=False)

            print(key + ' saved')

# Save in process DF in Excell with Sheet name of 'In Process Calc.'
def saveExcell_midcalc(data, output_file_path):
    
    with pd.ExcelWriter(output_file_path) as writer:
        for key, value in data.items():
            value.to_excel(writer, sheet_name=key, index=False)

            print(key + ' saved')

# Add rolling_regression method to Species Class
Species.rolling_poly_regression = rolling_poly_regression
Species.get_rollpolyreg_sp_rate = get_rollpolyreg_sp_rate


# Add LogisticGrowthFit method to Species Class
Species.LogisticGrowthFit = LogisticGrowthFit


if __name__ == '__main__':
    sys.exit(main())