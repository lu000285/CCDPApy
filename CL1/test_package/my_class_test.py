import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy import diff

###########################################################################
# Check Error for Pandas
def check_key(df, key):
    try:
        return (df[key])
    except Exception as e:
        print(e)
        return pd.Series(data=np.nan)
###########################################################################
# Cell Line Class
class CellLine:
    def __init__(self):
        self._cell_line = []

    # Add Experiment
    def add_cell_line(self, exp):
        self._cell_line.append(exp)

    # Display
    def disp_cell_lines(self):
        for cl in self._cell_line:
            cl.disp_exp()
            print('\n')

    # Save Excell
    def save_excel(self, output_file_path):
        with pd.ExcelWriter(output_file_path) as writer:
            for cl in self._cell_line:
                sheet = cl.get_exp_id()
                cl.get_bioprocess_df().to_excel(writer, sheet_name=sheet, index=False)

                print(sheet + ' saved')
###########################################################################
###########################################################################
# Measured Data Class
class MeasuredData:
    # Constructor
    def __init__(self, experiment_info, raw_data):
        # Original Raw Data
        self._raw_data = raw_data

        # Experoment Infomation Members
        self._experiment_id = experiment_info.loc['Experiment ID'].get(1)
        self._experimenter_name = experiment_info.loc['Name'].get(1)
        self._cell_line_name = experiment_info.loc['Cell Line'].get(1)
        self._initial_volume = experiment_info.loc['Initial Volume (mL)'].get(1)

        # Experimental Variables
        self._sample_num = check_key(raw_data, 'SAMPLE #')
        #
        self._date = check_key(raw_data, 'DATE')
        self._time = check_key(raw_data, 'TIME')
        self._run_time_day = check_key(raw_data, 'Day')
        self._run_time_hour = check_key(raw_data, 'Hours')
        #
        self._sample_volume = check_key(raw_data, 'SAMPLE VOLUME (mL)').fillna(0)
        self._feed_media_added = check_key(raw_data, 'FEED MEDIA ADDED (mL)').fillna(0)
        #
        self._glucose_feed_added = check_key(raw_data, 'GLUCOSE ADDED (mL)').fillna(0)
        self._glutamine_feed_added = check_key(raw_data, 'GLUTAMINE FEED ADDED (mL)').fillna(0)
        #
        self._base_added = check_key(raw_data, 'BASE ADDED (mL)').fillna(0)

        self._xv = check_key(raw_data, 'VIABLE CELL CONC. XV (x106 cells/mL)').fillna(0)  # xv: Viable Cell Concentration
        self._xd = check_key(raw_data, 'DEAD CELL CONC. Xd (x106 cells/mL)').fillna(0)    # xd: Dead Cell Concentraion
        self._xt = check_key(raw_data, 'TOTAL CELL CONC. Xt (x106 cells/mL)').fillna(0)   # xt: Total Cell Concentraion
        self._viability = check_key(raw_data, 'VIABILITY (%)')
        self._pH = check_key(raw_data, 'pH')
        self._do = check_key(raw_data, 'DO (%)')
        self._our = check_key(raw_data, 'OUR (mmol/L/hr)').fillna(0)
        self._oxygen_consumption_rate = check_key(raw_data, 'SP. OXYGEN CONSUMPTION RATE (mmol/109cell/hr)').fillna(0)
        self._oxygen_consumed = check_key(raw_data, 'OXYGEN CONSUMED (mmol/L)').fillna(0)
        self._optical_density = check_key(raw_data, 'OPTICAL DENSITY')
        self._osmolaliry = check_key(raw_data, 'OSMOLALITY (mmol/kg)')
        self._igg_conc = check_key(raw_data, 'IgG CONC. (mg/L)').fillna(0)

        # Have Calculated Cumulative Consumption/Production ?
        self._direct_cumulative = False

        # Variables Used in In Process
        n = len(self._sample_num) # Number of Samples        
        self._v_before_sampling = pd.Series(data=[0.0] * n, name='VOLUME BEFORE SAMPLING (mL)')
        self._v_after_sampling = pd.Series(data=[0.0] * n, name='VOLUME AFTER SAMPLING (mL)')
        self._v_after_feeding = pd.Series(data=[0.0] * n, name='VOLUME AFTER FEEDING (mL)')
        self._feed_status = pd.Series(data=np.nan * n, name='Feed Status')

        # Call Initialize Method
        if (not self._run_time_hour.any() and not self._run_time_day.any()):
            self.run_time()

        self.culture_volume()

        self._pre_variable = pd.concat([self._run_time_day,
                                        self._run_time_hour,
                                        self._v_before_sampling,
                                        self._v_after_sampling,
                                        self._v_after_feeding,
                                        self._feed_status,
                                        ], axis=1)

    # Calculate Run Time (day, hour)
    def run_time(self):
        try: # If TIME is Timestamp('2019-08-23 13:11:00') 
            self._run_time_hour = (self._time - self._time.iat[0]).apply(lambda x: x.total_seconds() / 3600)
        except:
            # Change DATE and TIME to String
            day_str = self._date.dt.strftime('%x ')
            time_str = self._time.apply(lambda x: x.strftime('%X'))
            # Combine DATE and TIME Strings, then Change the DataType to datetime
            dt = pd.to_datetime(day_str + time_str)
            # Calculate Run Time (Hour)
            self._run_time_hour = (dt - dt.iat[0]).apply(lambda x: x.total_seconds() / 3600)
        # Calculate Run Time (Day)
        self._run_time_day = self._run_time_hour / 24
        

    # Calculate Culture Volume Before/After Sampling and After Feeding
    def culture_volume(self):
        n = len(self._sample_num) # Number of Samples
        self._v_before_sampling.iat[0] = self._initial_volume   # Initial Volume

        for i in range(n):
            # Volume After Sampling
            self._v_after_sampling.iat[i] = self._v_before_sampling.iat[i] - self._sample_volume.iat[i]
            # Added Supplements Volume
            supplements_added = self._base_added.iat[i] + self._glutamine_feed_added.iat[i] + self._feed_media_added.iat[i]
            # Volume After Feeding
            self._v_after_feeding.iat[i] = self._v_after_sampling.iat[i] + supplements_added
            if (i < n-1):
                self._v_before_sampling.iat[i+1] = self._v_after_feeding.iat[i]


    # Getters
    # Get Experiment ID
    def get_exp_id(self):
        return self._experiment_id

    # Get Cell Line Name/No.
    def get_cl_name(self):
        return self._cell_line_name

    # Get Initial Culture Volume
    def get_init_v(self):
        return self._initial_volume

    # Get the Name of Experimenter
    def get_experimenter(self):
        return self._experimenter_name

    def get_pre_data(self):
        return self._pre_variable

    def get_v_before_samp(self):
        return self._v_before_sampling

    def get_v_after_samp(self):
        return self._v_after_sampling

    def get_v_after_feed(self):
        return self._v_after_feeding
###########################################################################
###########################################################################
# Cell Bioprocess Class
class BioProcess:
    def __init__(self, experiment_info, measured_data):
        #
        self._exp_info = experiment_info
        self._measured_data = measured_data

        # Experoment Infomation Members
        self._experiment_id = experiment_info.loc['Experiment ID'].get(1)
        self._experimenter_name = experiment_info.loc['Name'].get(1)
        self._cell_line_name = experiment_info.loc['Cell Line'].get(1)
        self._initial_volume = experiment_info.loc['Initial Volume (mL)'].get(1)

        self._cl_col = pd.Series(data=[self._cell_line_name] * len(measured_data), name='Cell Line')

        #
        self._cell = None
        self._oxygen = None
        self._igg = None
        self._aa_list = None
        self._aa_dict = None
        self._aa_df = None
        self._pre_process = None
        self._in_process = None
        self._post_process_list = []
        self._post_process = None

        # Polynomial Regression
        self._polyorder_df = None

    # Getters
    def get_cell(self):
        return self._cell
    
    def get_oxygen(self):
        return self._oxygen

    def get_igg(self):
        return self._igg

    def get_cell_line(self):
        return self._cell_line_name

    def get_exp_id(self):
        return self._experiment_id

    def get_exp_info(self):
        return self._exp_info

    def get_measured_data(self):
        return self._measured_data

    def get_pre_process(self):
        return self._pre_process

    def get_in_process(self):
        blank = pd.Series(data=np.nan, name='/')
        self._in_process = pd.concat([self._pre_process,
                                      blank,
                                      self._aa_df],
                                     axis=1)
        return self._in_process

    def get_aa_list(self):
        return self._aa_list

    def get_aa_dict(self):
        return self._aa_dict

    def get_post_process(self):
        return self._post_process

    def get_bioprocess_df(self):
        in_pro = self.get_in_process()

        blank = pd.Series(data=np.nan, name='/')
        return pd.concat([self._cl_col,
                          self._measured_data,
                          blank,
                          in_pro,
                          blank,
                          self._post_process],
                         axis = 1)
    
    def get_polyorder_df(self):
        return self._polyorder_df

    # Setters
    def set_cell(self, cell):
        self._cell = cell
        self._pre_process = cell.get_pre_data()

    def set_oxygen(self, oxygen):
        self._oxygen = oxygen
        self._pre_process = oxygen.get_pre_data()

    def set_igg(self, igg):
        self._igg = igg
        self._pre_process = igg.get_pre_data()

    def set_aa_df(self, aa_df):
        self._aa_df = aa_df

    def set_aa_dict(self, aa_dict):
        self._aa_dict = aa_dict

    def set_aa_list(self, aa_list):
        self._aa_list = aa_list

    def set_pre_process(self, pre_process):
        self._pre_process = pre_process

    def set_in_process(self, in_process):
        self._in_process = in_process

    def set_polyorder_df(self, polyorder):
        self._polyorder_df = polyorder

    # Add Post Process Data
    def add_post_process(self, post_process):
        blank = pd.Series(data=np.nan, name='/')
        self._post_process_list.append(post_process)
        self._post_process_list.append(blank)
        self._post_process = pd.concat(self._post_process_list, axis=1)

    # Display Methods
    def disp_exp(self):
        print(f'Cell Line:              {self._cell_line_name}')
        print(f'Experiment ID:          {self._experiment_id}')
        print(f'Experimenter Name:      {self._experimenter_name}')
        print(f'Initial Culture Volume: {self._initial_volume}')
        print('Metabolite List:')
        print(self.get_aa_list)

    # Plotting Method
    def plot_profile(self,
                     aa_list=None,
                     polyreg=True,
                     save_file_path=None):
        if (not aa_list):
            aa_list = self._aa_list
        n = len(aa_list)

        fig = plt.figure(figsize=(8*3, 6*n))

        for i, x in enumerate(aa_list):
            x = x.upper()
            fig = self._aa_dict[x].plot(polyreg=polyreg,
                                             fig=fig,
                                             column=n,
                                             ax_idx=1+i*3,)

        title = ''
        for name in aa_list :
            title += name + ' '
        fig.suptitle(title + 'Profils', fontsize='xx-large')

        # Save
        if (save_file_path != None):
            fig.savefig(save_file_path)

        return fig
###########################################################################
# Cell
class Cell(MeasuredData):
    '''
    '''
    # Constructor
    def __init__(self, experiment_info, raw_data, name):

        # Constructor for MeasuredDate Class
        super().__init__(experiment_info, raw_data)

        # Members
        self._name = name
        self._idx = self._xv[self._xv.notnull()].index
        self._cumulative = None
        self._ixv = None

        # Call Calculation Methods
        self.integral_viable_cell()
        self.cumulative_cells_prod()

    # Methods
    # Integral of Viable Cell
    def integral_viable_cell(self, initial_conc=0):
        xv = self._xv
        t = self._run_time_hour
        s = pd.Series(data=[initial_conc] * len(t),
                      name='INTEGRAL OF VIABLE CELL CONC. IVCC (x106 cells hr/mL)')

        for i in range(1, len(t)):
            s.iat[i] = s.iat[i-1] + (xv.iat[i] + xv.iat[i-1]) / 2 * (t.iat[i] - t.iat[i-1])

        self._ixv = s

    # Cumulative Cell Produced
    def cumulative_cells_prod(self, initial_conc=0):
        # xv: vialbe cell concentration (10e6 cells/ml) or IgG
        # v1: culture volume before sampling (ml)
        # v2: culture volume after feeding (ml)
        # Cells produced = xv(i) * v(i) - xv(i-1) * v(i-1)
        xv = self._xv
        v1 = self._v_before_sampling
        v2 = self._v_after_sampling

        s = pd.Series(data=[initial_conc] * len(xv),
                      name='CUM CELLS PROD. (x106 cells)')

        for i in range(1, len(xv)):
            s.iat[i] = s.iat[i-1] + xv.iat[i] * v1.iat[i] - xv.iat[i-1] * v2.iat[i-1]
        
        self._cumulative = s

    # Getters
    def get_ivcc(self):
        return self._ixv

    def get_cumulative(self):
        return self._cumulative
###########################################################################
###########################################################################
# Oxygen Class
class Oxygen(MeasuredData):
    '''
    '''
    # Constructor
    def __init__(self, experiment_info, raw_data, name):

        # Constructor for MeasuredDate Class
        super().__init__(experiment_info, raw_data)

        # Members
        self._name = name
        # self._idx = self._xv[self.xv.notnull()].index
        self._cumulative = None

        # Call Calculation Methods
        self.cumulative_oxy_cons()

    # Methods
    def cumulative_oxy_cons(self, initial_conc=0):
        # oxy: concentration of oxygen
        # v1: culture volume before sampling
        # v2: culture volume after sampling
        oxy = self._oxygen_consumed
        v1 = self._v_before_sampling
        v2 = self._v_after_sampling

        s = pd.Series([initial_conc] * len(oxy),
                      name = 'CUM OXYGEN CONS. (mmol)')

        for i in range(1, len(oxy)):
            s.iat[i] = s.iat[i-1] + (oxy.iat[i] * v1.iat[i] - oxy.iat[i-1] * v2.iat[i-1]) / 1000

        self._cumulative = s

    # Getters
    def get_cumulative(self):
        return self._cumulative
###########################################################################
###########################################################################
# IgG Class
class IgG(MeasuredData):
    '''
    '''
    # Constructor
    def __init__(self, experiment_info, raw_data, name):
        # Constructor for MeasuredDate Class
        super().__init__(experiment_info, raw_data)

        # Members
        self._name = name
        self._idx = self._igg_conc[self._igg_conc.notnull()].index
        self._cumulative = None

        # Call Calculation Methods
        self.cumulative_igg_prod()

    # Cumulative Cell Produced
    def cumulative_igg_prod(self, initial_conc=0):
        # Cells produced = xv(i) * v(i) - xv(i-1) * v(i-1)
        igg = self._igg_conc            # igg: IgG concentration (10e6 cells/ml)
        v1 = self._v_before_sampling    # v1: culture volume before sampling (ml)
        v2 = self._v_after_sampling     # v2: culture volume after feeding (ml)

        s = pd.Series(data=[initial_conc] * len(igg),
                      name='CUM IgG PROD. (mg)')

        for i in range(1, len(igg)):
            s.iat[i] = s.iat[i-1] + igg.iat[i] * v1.iat[i] - igg.iat[i-1] * v2.iat[i-1]
        
        self._cumulative = s / 1000 # Adjust unit

    # Getters
    def get_cumulative(self):
        return self._cumulative
###########################################################################
###########################################################################
# Species Class
class Species(MeasuredData):
    def __init__(self, experiment_info, raw_data, name,
                 conc_before_feed, conc_after_feed, feed_conc, cumulative,
                 production=False):
        
        # Constructor for MeasuredDate Class
        super().__init__(experiment_info, raw_data,)
        
        # Members
        self._name = name
        self._conc_before_feed = conc_before_feed
        self._conc_after_feed = conc_after_feed
        self._feed_conc = feed_conc
        self._production = production

        self._idx = self._conc_before_feed[self._conc_before_feed.notnull()].index
        self._cumulative = cumulative
        
        # Call Initialize Method
        # IF Measured Data has Cumulative Consumption/Production
        if (self._cumulative.any()):
            self._direct_cumulative = True
            self._cumulative_unit = '(mM)'
        else:
            self._cumulative_unit = '(mmol)'
            # IF Experiments Measure the Feed Concentration
            if (self._feed_conc.any()):
                self.conc_after_feeding()           # Calculate Concentration After Feeding
                self.cumulative_cons_from_feed()    # Calculate Cumulative Consumption/Production with Feed Concentraion

            # IF Experiments Measure the Concentraion After Feeding
            elif (self._conc_after_feed.any()):
                self.cumulative_cons_from_conc_after_feed()  # Calculate Cumulative Consumption/Production with Concentraion after Feeding

            else:
                self.cumulative_cons_without_feed()


    # Calculate Concentration After Feeding
    def conc_after_feeding(self):
        s = self._conc_before_feed         # s: Substrate Concentration (mM)
        sf = self._feed_conc   # sf: Substrate Feed Concentration (mM)
        f = self._feed_media_added      # f: Feed Flowrate (ml/hr)
        v2 = self._v_after_sampling     # v2: Culture Volume After Sampling (ml)
        g = self._glutamine_feed_added  # g: Glutamine Feed Added
        # g = self._glucose_feed_added

        self._conc_after_feed = (s*v2 + sf*f) / (v2 + f + g)


    # Calculate Cumulative Consumption/Production
    def cumulative_cons_from_feed(self):
        # Count Measurement
        idx = self._idx

        s = self._conc_before_feed[idx]      # s: Substrate Concentration (mM)
        sf = self._feed_conc[idx]             # sf: Substrate Feed Concentration (mM)
        f = self._feed_media_added[idx]       # f: Feed Flowrate (ml/hr)
        v1 = self._v_before_sampling[idx]     # v1: Culture Volume Before Sampling (ml)
        v2 = self._v_after_sampling[idx]      # v2: Culture Volume After Sampling (ml)

        conc0 = 0 # Initial Concentration
        se = pd.Series(data=[conc0] * len(self._sample_num),
                       name=f'CUM {self._name} {self._cumulative_unit}')   # Initialize

        # For Glutamine
        if self._name == 'GLUTAMINE':
            f = self._glutamine_feed_added

        # Consumed Substrate = sf*f + s[i-1]*v[i-1] - s[i]*v[i]
        for i in range(1, len(idx)):
            se.iat[idx[i]] = se.iat[i-1] + (sf.iat[i] * f.iat[i-1] - s.iat[i] * v1[i] + s.iat[i-1] * v2[i-1]) / 1000

        # The Case that Species is Produced but Not Consumed.
        if (self._production == True):
            se *= -1

        self._cumulative = se


    # Calculate Cumulative Consumption/Production with concentration after feeding
    def cumulative_cons_from_conc_after_feed(self):
        # Count Measurement
        idx = self._idx

        s1 = self._conc_before_feed[idx]     # s: Substrate Concentration Before Feeding (mM)
        s2 = self._conc_after_feed[idx]      # s: Substrate Concentration After Feeding (mM)
        v = self._v_before_sampling[idx]     # v: Culture Volume After Feeding (ml)

        conc0 = 0 # Initial Concentration
        s = pd.Series([np.nan] * len(self._sample_num),
                      name=f'CUM {self._name} {self._cumulative_unit}')   # Initialize
        s.iat[0] = conc0

        # Consumed Substrate = 
        for i in range(1, len(idx)):
            si = (s2.iat[i-1] * v.iat[i] - s1.iat[i] * v.iat[i]) / 1000
            s.iat[idx[i]] = s.iat[idx[i-1]] + si

        # The Case that Species is Produced but Not Consumed.
        if (self._production == True):
            s *= -1

        self._cumulative = s

    def cumulative_cons_without_feed(self):
        # Count Measurement
        idx = self._idx

        s = self._conc_before_feed[idx]      # s: Substrate Concentration (mM)
        v1 = self._v_before_sampling[idx]     # v1: Culture Volume Before Sampling (ml)
        v2 = self._v_after_sampling[idx]      # v2: Culture Volume After Sampling (ml)

        conc0 = 0 # Initial Concentration
        se = pd.Series(data=[conc0] * len(self._sample_num),
                        name=f'CUM {self._name} {self._cumulative_unit}')   # Initialize

        # Consumed Substrate = sf*f + s[i-1]*v[i-1] - s[i]*v[i]
        for i in range(1, len(idx)):
            se.iat[idx[i]] = se.iat[i-1] + (- s.iat[i] * v1[i] + s.iat[i-1] * v2[i-1]) / 1000

        # The Case that Species is Produced but Not Consumed.
        if (self._production == True):
            se *= -1

        self._cumulative = se

    # Getters
    # Get Species Name
    def get_name(self):
        return self._name

    # Get Concentration
    def get_conc_before_feed(self):
        return self._conc_before_feed

    # Get Concentration After Feeding
    def get_conc_after_feed(self):
        return self._conc_after_feed

    # Get Concentration After Feeding
    def get_feed_conc(self):
        return self._feed_conc

    # Get Cumulative Consumption/Production
    def get_cumulative(self):
        return self._cumulative

    def get_cumulative_unit(self):
        return self._cumulative_unit
###########################################################################
###########################################################################

###########################################################################