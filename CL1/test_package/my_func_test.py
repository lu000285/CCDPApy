import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import types
import os
from pathlib import Path
from numpy import diff

from .my_class_test import MeasuredData
from .my_class_test import Cell
from .my_class_test import Oxygen
from .my_class_test import IgG
from .my_class_test import Species
from .my_class_test import BioProcess

###########################################################################
# Check Error for Pandas
def check_key(df, key):
    try:
        return (df[key])
    except Exception as e:
        print(e)
        return pd.Series(data=np.nan)
###########################################################################
###########################################################################
# SP. Oxygen Uptake Rate
def sp_our(self):
    # our: OUR in Measured Data
    self._sp_our = (self._our / self._xv).rename('SP. OUR (mmol/109 cells/hr)')

# SP. Oxygen Consumption Rate
def sp_oxy_cons_rate(self):
    t = self._run_time_hour                 # t: run time (hrs)
    v1 = self._v_before_sampling            # v1: culture volume before sampling (mL)
    v2 = self._v_after_sampling             # v2: culture volume after sampling (mL)
    rate = self._oxygen_consumption_rate    # rate: oxygen consumption rate in Measured Data
    c = self._oxygen_consumed               # c: oxyge consumed in Measured Data

    r = pd.Series(data=[np.nan]*len(t), name='SP. OXYGEN CONSUMPTION RATE (mmol/109cell/hr)')
    for i in range(1, len(t)):
        if rate.iat[i] < 0:
            x = c.iat[i]*v1.iat[i] - c.iat[i-1]*v2.iat[i-1]
            y = (self._vcc.iat[i]*v1.iat[i] + self._vcc.iat[i-1]*v1.iat[i-1])*1000000*0.5*(t.iat[i] - t.iat[i-1])
            r.iat[i] = x / 1000 / y *1000000000
        else:
            r.iat[i] = rate.iat[i]
    self._sp_rate = r

# Call Methods
def oxy_post_process(self):
    self.sp_our()
    self.sp_oxy_cons_rate()

# getters
def get_sp_OUR(self):
    return self._sp_our

def get_sp_rate(self):
    return self._sp_rate

def get_oxy_post_data(self):
    return pd.concat([self._sp_our,
                      self._sp_rate],
                     axis=1)



###########################################################################
###########################################################################
# Calculates Specific growth rate
def sp_growth_rate(self):
    t = self._run_time_hour         # t: run time (hrs)
    cum_cell = self._cumulative     # cum_cell: Cumulative Cell Concentraion (10e6 cells/mL)
    v1 = self._v_before_sampling    # v1: culture volume before sampling (mL)
    v2 = self._v_after_sampling     # v2: culture volume after sampling (mL)
    xv = self._xv                   # xv: Viable Cell Concentration (10e6 cells/mL)

    rate = pd.Series(data=[np.nan] * len(t), name='SP. GROWTH RATE, m (hr-1) [mv-kd]') # Initialize
    
    for i in range(1, len(t)):
        x = cum_cell.iat[i] - cum_cell.iat[i-1]
        y = self._xv.iat[i]*v1.iat[i] + self._xv.iat[i-1]*v2.iat[i-1]
        rate.iat[i] = x / (y*0.5*(t.iat[i]-t.iat[i-1]))
    self._sp_g_rate = rate

# Calculates kd value
def kd(self):
    xv = self._xv                   # xv: Viable Cell Concentration (10e6 cells/mL)
    xd = self._xd                   # xd: Dead Cell Concentration (10e6 cells/mL)
    t = self._run_time_hour         # t: run time (hrs)
    v1 = self._v_before_sampling    # v1: culture volume before sampling (mL)
    v2 = self._v_after_sampling     # v2: culture volume after sampling (mL)

    rate = pd.Series(data=[np.nan] * len(t), name='kd')

    for i in range(1, len(t)):
        x = xd.iat[i]*v1.iat[i] - xd.iat[i-1]*v2.iat[i-1]
        y = self._xv.iat[i]*v1.iat[i] + self._xv.iat[i-1]*v2.iat[i-1]
        rate.iat[i] = x / (y*0.5*(t.iat[i]-t.iat[i-1]))
    self._kd_val = rate

# Calculate mv
def mv(self):
    self._mv_val = (self._sp_g_rate + self._kd_val).rename('mv')

# Call methods
def cell_post_process(self):
    self.calc_sp_GRate()
    self.calc_kd()
    self.calc_mv()

# getters
def get_kd(self):
    return self._kd_val

def get_sp_growth_rate(self):
    return self._sp_g_rate

def get_mv(self):
    return self._mv_val

def get_cell_post_data(self):
    return pd.concat([self._sp_g_rate,
                      self._mv_val,
                      self._kd_val],
                     axis=1)


###########################################################################
###########################################################################
# Calculate Specific Rate
def igg_sp_rate_twopt(self):
    # Get Measurement Index
    idx = self._igg_conc[self._igg_conc.notnull()].index

    s = self._cumulative[idx]           # s: substrate concentration (mM)
    t = self._run_time_hour[idx]        # t: run time (hrs)
    v = self._v_before_sampling[idx]    # v: culture volume before sampling (mL)
    xv = self._xv[idx]                  # xv: Viable Cell Concentration (10e6 cells/mL)
    
    rate = pd.Series(data=[np.nan] * len(self._sample_num), name='q'+self._name+' (mmol/109 cell/hr)')

    for i in range(1, len(idx)):
        x = (s.iat[i] - s.iat[i-1]) * 1000
        y = xv.iat[i]*v.iat[i] + xv.iat[i-1]*v.iat[i]

        rate.iat[idx[i]] = x / (y*0.5*(t.iat[i]-t.iat[i-1]))

    self._sp_rate = rate

# Getter
def get_sp_rate(self):
    return self._sp_rate


###########################################################################
###########################################################################
# Calculate Specific Rate
def sp_rate_twopt(self):
    # Get Measurement Index
    idx = self._conc_before_feed[self._conc_before_feed.notnull()].index

    s = self._cumulative[idx]           # s: substrate concentration (mM)
    t = self._run_time_hour[idx]        # t: run time (hrs)
    v = self._v_before_sampling[idx]    # v: culture volume before sampling (mL)
    xv = self._xv[idx]                  # xv: Viable Cell Concentration (10e6 cells/mL)
    
    rate = pd.Series(data=[np.nan] * len(self._sample_num),
                     name='q'+self._name+' (mmol/109 cell/hr)')
    
    # IF Have Direct Mesurement of Cumulative
    if (self._direct_cumulative):
        dsdt = diff(s)/diff(t)
        dsdt = np.insert(dsdt, 0, np.nan)
        rate = dsdt / xv

    else:
        for i in range(1, len(idx)):
            x = (s.iat[i] - s.iat[i-1]) * 1000
            y = xv.iat[i]*v.iat[i] + xv.iat[i-1]*v.iat[i]

            rate.iat[idx[i]] = x / (y*0.5*(t.iat[i]-t.iat[i-1]))

    self._sp_rate = rate

# Getter
def get_sp_rate(self):
    return self._sp_rate

###########################################################################
###########################################################################
# SP. Rate Polynomial Regression
def polyreg(self, polyorder=3):
    t = self._run_time_hour[self._idx]         # t: run time (hrs)
    s = self._cumulative[self._idx]            # s: substrate concentration (mM)
    xv = self._xv[self._idx]                  # xv: Viable Cell Concentration (10e6 cells/mL)
    v = self._v_after_sampling[self._idx]     # v: culture volume after sampling (mL)

    self._polyorder = polyorder     # Polynomial Regression Order

    # Polynomial Regression for Cumulative Consumption/Production
    print(self._name)
    print(s)
    print('/n')
    fit = np.polyfit(t, s, polyorder)  # Fitting data to polynomial Regression (Get slopes)
    p = np.poly1d(fit)  # Get polynomial curve for Cumulative Consumption/Production

    dpdt = p.deriv()      # first derivetive of polynomial fit

    y = dpdt(t)      # derivetive values corresponding to x

    # Calculate Specific Rate from Derivetive of Polynomial Regression on Cumularive Consumption/Production
    q = pd.Series(data=[np.nan] * len(self._sample_num),
                  name='q'+self._name+' (mmol/109 cell/hr)')

    # Calculate SP. rate
    for i in range(1, len(self._idx)):
        if (self._direct_cumulative):
            q.iat[self._idx[i]] = y[i] / xv.iat[i]
        else:
            q.iat[self._idx[i]] = y[i] / (xv.iat[i] * v.iat[i]) * 1000

    self._polyreg_cumulative = p(t) # Get Polynomial Fit Cumulative Consumption/Production corresponding x values
    self._polyreg_sp_rate = q       # Polynomial Fit SP. rate
    self._polyfit_cumulative = p    # For plotting

# Getters
def get_polyorder(self):
    return self._polyorder

def get_polyreg_cumulative(self):
    return self._polyreg_cumulative

def get_polyreg_rate(self):
    return self._polyreg_sp_rate


###########################################################################
###########################################################################
# Plotting for ONE Species obj
def plot(self,
         concentration=True,
         cumulative=True,
         sp_rate=True,
         polyreg=True,
         fig=None,
         column=1,
         ax_idx = 1,
         figsize=(8, 6),
         data_num=100):
    
    # column: 
    # ax_idx: start ax
    
    polyreg_data_num = data_num # number of data for polynomial regression
    f1 = concentration # and self._concentration.any()
    f2 = cumulative # and self._cumulative.any()
    f3 = sp_rate # and self._sp_rate.any()
    factor = 3
    if (factor == False):
        return None

    w, h = figsize
    size = (w*factor, h)
    if (fig==None):
        fig = plt.figure(figsize=size)
    fig.tight_layout(rect=[0,0,1,0.96])

    x = self._run_time_hour[self._idx]  # x axis data
    x2 = np.linspace(x.iat[0], x.iat[-1], polyreg_data_num) # x data for polynomial regression
    
    # Concentration Profile
    ax = fig.add_subplot(column, factor, ax_idx) # add axis
    # Plot
    if (f1):
        y = self._conc_before_feed[self._idx] # y axis data
        ax.scatter(x, y, label=(self._name))    # plot

        ax.plot(x, y)
        ax.set_title('Kinetic Curve', loc='left')
        ax.set_ylabel('Concentration (mM)')
        ax.set_xlabel('Time (hrs)')
        ax.legend()
        ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

    ax_idx += 1 # add ax index

    # Cumulative Profile
    ax = fig.add_subplot(column, factor, ax_idx) # add axis
    # Plot
    if (f2):
        y = self._cumulative[self._idx]    # y axis data
        ax.scatter(x, y, label=(self._name))    # plot

        # Add Polynomial Regression Fit on the same graph
        if (self._polyreg_cumulative.any()):
            y2 = self._polyfit_cumulative(x2)
            ax.plot(x2, y2, color='orange', label=('Poly. Fit. Order:' + str(self._polyorder)))

        ax.set_title('Cumulative Curve', loc='left')
        ax.set_ylabel('Cumulative ' + self._name + ' (mmol)')
        ax.set_xlabel('Time (hrs)')
        ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
        ax.legend()

    ax_idx += 1 # add ax index
    
    # SP profile
    ax = fig.add_subplot(column, factor, ax_idx) # add axis
    # Plot
    if (f3):
        # Two-Point Calc
        y = self._sp_rate[self._idx]    # y axis data
        ax.plot(x, y, label=(self._name + '\nTwo-Point Calc.'))    # plot

        ax.set_title('SP. Rate', loc='left')
        ax.set_ylabel('SP. rate (mmol/109 cell/hr)')
        ax.set_xlabel('Time (hrs)')
        ax.legend()
        ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

        # Polynomial Regression
        if (polyreg):
            y2 = self._polyreg_sp_rate[self._idx]

            ax.plot(x, y2, ls=':',
                    label=('Poly. Reg. Fit.\nOrder: ' + str(self._polyorder)))   # plot

            ax.set_ylabel('SP. rate (mmol/109 cell/hr)')
            ax.set_xlabel('Time (hrs)')
            ax.legend()
            ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
            
    ax_idx += 1 # add ax index

    fig.suptitle(self._name + ' Profile', fontsize='xx-large')

    return fig


###########################################################################
###########################################################################
def cumulative_in_pro(bio_process):
    exp_info = bio_process.get_exp_info()
    measured_data = bio_process.get_measured_data()

    # Cell
    cell = Cell(experiment_info=exp_info, raw_data=measured_data, name='Cell')
    bio_process.set_cell(cell)

    # Oxygen
    oxygen = Oxygen(experiment_info=exp_info, raw_data=measured_data, name='Oxygen')
    bio_process.set_oxygen(oxygen)

    # IgG
    igg = IgG(experiment_info=exp_info, raw_data=measured_data, name='IgG',)
    bio_process.set_igg(igg)

    # AA Cumulative
    aa_lst = bio_process.get_aa_list()
    aa_dict = {}                        # Initialize
    aa_cumulative_df = pd.DataFrame()   # Initialize
    for s in aa_lst:
        s = s.upper()   # Name
        conc_before = check_key(measured_data, f'{s} CONC. (mM)')           # Concentration Before Feeding
        conc_after = check_key(measured_data, f'{s} CONC. (mM).1')          # Concentration After Feeding
        feed = check_key(measured_data, f'FEED {s} CONC. (mM)')             # Feed Concentration

        # Check Calculated Cumulative Concentration
        cumulative = check_key(measured_data, f'CUM {s} CONS. (mM)')
        if (not cumulative.any()):
            cumulative = check_key(measured_data, f'CUM {s} PROD. (mM)')

        # Object
        spc = Species(experiment_info=exp_info,
                    raw_data=measured_data,
                    name=s,
                    conc_before_feed=conc_before,
                    conc_after_feed=conc_after,
                    feed_conc=feed,
                    cumulative=cumulative,
                    production=True if (s=='LACTATE' or s=='NH3') else False)
        unit = spc.get_cumulative_unit()    # Unit
        
        aa_cumulative_df['CUM ' + s + unit] = spc.get_cumulative()  # Add to DF
        aa_dict[s] = spc    # Add to Dictionary

        # Other Spc Cumulative

        # Add to bp obj
        bio_process.set_aa_df(aa_cumulative_df)
        bio_process.set_aa_dict(aa_dict=aa_dict)
        bio_process.set_pre_process(pre_process=cell.get_pre_data())
        bio_process.set_in_process(in_process=aa_cumulative_df)

    return bio_process
###########################################################################
###########################################################################
def twopt_post_pro(bio_process):
    # Cell
    cell = bio_process.get_cell()
    cell.post_process()

    # Oxygen
    oxygen = bio_process.get_oxygen()
    oxygen.post_process()

    # IgG
    igg = bio_process.get_igg()
    igg.sp_rate_twopt()

    # AA
    aa_dict = bio_process.get_aa_dict()
    aa_rate_twopt_df = pd.DataFrame()   # Initialize

    for aa_name, aa_obj in aa_dict.items():
        aa_obj.sp_rate_twopt()
        title = f'Two-Pt. Calc. q{aa_name.capitalize()} (mmol/109 cell/hr)'

        aa_rate_twopt_df[title] = aa_obj.get_sp_rate()

    # Add to bp
    bio_process.add_post_process(aa_rate_twopt_df)
    
    return bio_process
###########################################################################
###########################################################################
def polyreg_post_pro(bio_process):
    polyorder = bio_process.get_polyorder_df()
    polyorder.index = [name.upper() for name in polyorder.index]

    # Cell
    order = polyorder.loc['CELL'].iat[0]
    cell = bio_process.get_cell()
    cell.polyreg(polyorder=order)

    # Oxygen
    '''order = polyorder.loc['OXYGEN'].iat[0]
    oxygen = bio_process.get_oxygen()
    oxygen.polyreg(polyorder=order)'''

    # IgG
    order = polyorder.loc['IGG'].iat[0]
    igg = bio_process.get_igg()
    igg.polyreg(polyorder=order)

    
    # AA
    aa_dict = bio_process.get_aa_dict()
    polyreg_df = pd.DataFrame()     # Initialize

    for aa_name, aa_obj in aa_dict.items():
        order = polyorder.loc[aa_name].iat[0]
        aa_obj.polyreg(polyorder=order)

        title = f'Poly. Reg. Order: {order} q{aa_name} (mmol/109 cell/hr)'

        polyreg_df[title] = aa_obj.get_polyreg_rate()

    # Add
    bio_process.add_post_process(polyreg_df)

    return bio_process
###########################################################################
###########################################################################
def bio_process(input_file_name,
                measured_data_sheet_name='Measured Data',
                aa_list=None,
                polyorder_file_name=None):
    
    # About Input Data for Measured Data
    BASE_DIR = 'drive/MyDrive/Yudai Fukae/Data analysis tool/Biomanufacturing Data/CL3'
    input = os.path.join(BASE_DIR, input_file_name)

    # Read Excel Files
    measured_data = pd.read_excel(io=input, 
                                    sheet_name=measured_data_sheet_name,
                                    header=5)
    exp_info = pd.read_excel(io=input,
                                    sheet_name=measured_data_sheet_name,
                                    nrows=4,
                                    usecols=[0, 1],
                                    header=None,
                                    index_col=0)

    # Check AA List to Analyze
    if (not aa_list):
        # Original
        aa_list = ['ALANINE', 'ARGININE', 'ASPARAGINE', 'ASPARTATE', 'CYSTINE',
                   'GLUCOSE', 'GLUTAMINE', 'GLUTAMATE', 'GLYCINE', 'HISTIDINE',
                   'ISOLEUCINE', 'LACTATE', 'LEUCINE','LYSINE', 'METHIONINE',
                   'NH3', 'PHENYLALANINE', 'PROLINE', 'SERINE',
                   'THREONINE','TRYPTOPHAN', 'TYROSINE', 'VALINE']
    
    # Bio Process
    bio_pro = BioProcess(experiment_info=exp_info, measured_data=measured_data)
    bio_pro.set_aa_list(aa_list=aa_list)     # Set AA List

    # Cumulative
    bio_pro = cumulative_in_pro(bio_pro)

    # SP. Rate. Two-Point Calc.
    bio_pro = twopt_post_pro(bio_pro)

    if (polyorder_file_name):
        # Read Poly. Order file
        polyorder_df = pd.read_excel(io=polyorder_file_name, index_col=0)

        bio_pro.set_polyorder_df(polyorder_df)       # Set Poly. Order
        bio_pro = polyreg_post_pro(bio_pro)

    # Other Process

    return bio_pro
###########################################################################

def init():
    # Add Methods to Cell Class
    Cell.calc_sp_GRate = sp_growth_rate
    Cell.calc_kd = kd
    Cell.calc_mv = mv
    Cell.post_process = cell_post_process
    Cell.get_sp_growth_rate = get_sp_growth_rate
    Cell.get_kd = get_kd
    Cell.get_mv = get_mv
    Cell.get_post_data = get_cell_post_data

    # Add Methods to Oxygen Class
    Oxygen.sp_our = sp_our
    Oxygen.sp_oxy_cons_rate = sp_oxy_cons_rate
    Oxygen.post_process = oxy_post_process
    Oxygen.get_sp_OUR = get_sp_OUR
    Oxygen.get_sp_rate = get_sp_rate
    Oxygen.get_post_data = get_oxy_post_data

    IgG.sp_rate_twopt = igg_sp_rate_twopt
    IgG.get_sp_rate = get_sp_rate

    Species.sp_rate_twopt = sp_rate_twopt
    Species.get_sp_rate = get_sp_rate

    # Add Methods to Classes
    Cell.polyreg = polyreg
    Cell.get_polyorder = get_polyorder
    Cell.get_polyreg_cumulative = get_polyreg_cumulative
    Cell.get_polyreg_rate = get_polyreg_rate

    Oxygen.polyreg = polyreg
    Oxygen.get_polyorder = get_polyorder
    Oxygen.get_polyreg_cumulative = get_polyreg_cumulative
    Oxygen.get_polyreg_rate = get_polyreg_rate

    IgG.polyreg = polyreg
    IgG.get_polyorder = get_polyorder
    IgG.get_polyreg_cumulative = get_polyreg_cumulative
    IgG.get_polyreg_rate = get_polyreg_rate

    Species.polyreg = polyreg
    Species.get_polyorder = get_polyorder
    Species.get_polyreg_cumulative = get_polyreg_cumulative
    Species.get_polyreg_rate = get_polyreg_rate

    # Add plot method to Species Class
    Cell.plot = plot
    Oxygen.plot = plot
    IgG.plot = plot
    Species.plot = plot