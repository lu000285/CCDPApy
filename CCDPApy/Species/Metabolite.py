import pandas as pd
import numpy as np

from .Species import Species
from ..in_process.MetaboliteMixin import MetaboliteMixin
from ..post_process.polynomial.MetaboliteMixin import MetaboliteMixin as Polynomial
from ..post_process.rolling_window_polynomial.Metabolite import MetaboliteMixin as Rolling
from ..plotting.PlotMixin import PlotMixin

###########################################################################
# Metabolite Class
###########################################################################
class Metabolite(Species,
                 MetaboliteMixin,
                 Polynomial,
                 Rolling,
                 PlotMixin):
    '''
    Metabolite class.

    Attributes
    ---------
        name : str
                name of species.
        measured_data : python object
                MeasuredData object.
        production : bool, default=False, optional
            True if species is produced by bioprocess.
    '''             
    def __init__(self, name, measured_data, production=False):
        '''
        Parameters
        ---------
            name : str
                name of species.
            measured_data : python object
                MeasuredData object.
            production : bool, default=False, optional
                True if species is produced by bioprocess.
        '''
        # Constructor for MeasuredDate Class
        super().__init__(name=name, measured_data=measured_data)
        
        # Work with parameters
        key = f'{name.upper()}_(mM)'
        c_before_feed = measured_data.c_before_feed_df[key]
        c_after_feed = measured_data.c_after_feed_df[key]
        feed_c = measured_data.feed_c_df[key]
        cum_c = measured_data.cum_c_df[key]
        idx = c_before_feed[c_before_feed.notnull()].index  # Measurement indices
        t = measured_data.param_df['run_time_(hrs)'].values[idx]    # original run time (hour)
        
        # Calculate Mid Time from Original Run time
        time_mid = np.array([0.5 * (t[i] + t[i+1]) for i in range(len(t)-1)])
        
        # Class Members
        self._idx = idx
        self._c_before_feed = c_before_feed
        self._c_after_feed = c_after_feed
        self._feed_c = feed_c
        self._measured_cum_c = cum_c
        self._measured_cumulative_flag = True if cum_c.any() else False # True if there is the measurement of cumulative concentration.
        self._production = production
        #self._use_feed_c =  False
        #self._use_c_after_feed = False
        self._run_time_mid = time_mid
    
    # Getters

        

    '''def get_info_df(self, t):
        n = len(t)
        id = pd.Series(data=[self._exp_id] * n, name='Experiment ID')
        cl = pd.Series(data=[self._cell_line_name] * n, name='Cell Line')
        return pd.concat([cl, id, t], axis=1)


    def get_inpro_df(self):
        return pd.concat([self.get_info_df(self._run_time_hour),
                          self._conc_before_feed,
                          self._feed_conc,
                          self._conc_after_feed,
                          self._cumulative,
                          ], axis=1)

    def get_conc_df(self):
        t = self.get_info_df(self._run_time_hour)
        conc = self._conc_before_feed
        conc_before = pd.concat([t, conc.rename('CONC.')], axis=1)
        
        conc = self._conc_after_feed
        conc_after = pd.concat([t, conc.rename('CONC.')], axis=1)
        conc = pd.concat([conc_before, conc_after]).reset_index(drop=True)
        conc['Species'] = self._name.upper()
        conc['Species_label'] = f'{self._name.capitalize()} (mM)'

        return conc.sort_values(by=['RUN TIME (HOURS)'], kind='stable').reset_index(drop=True)
        
    def get_cumulative_df(self):
        t = self._run_time_hour
        # Two-pt calc.
        cum = self.get_info_df(t)
        cum['Cumulative'] = self.get_cumulative()
        cum['Method'] = f'Two-Pt. Calc.'
        cum['Cell_Line_Label'] = cum['Cell Line'].apply(lambda x: x+', Two-Pt. Calc.')
        cum['Experiment_ID_Label'] = cum['Experiment ID'].apply(lambda x: x+', Two-Pt. Calc.')

        # Poly. Reg.
        x = np.linspace(t.iat[0], t.iat[-1], 100)
        x = pd.Series(data=x, name=t.name)
        cum_poly = self.get_info_df(x)
        # cum[f'CUM {self._name} (mmol)'] = pd.Series(data=self._polyfit(x))
        cum_poly[f'Cumulative'] = pd.Series(data=self._polyfit(x))
        cum_poly['Method'] = f'Poly. Reg.'
        cum_poly['Order'] = self._polyorder
        cum_poly['Cell_Line_Label'] = cum_poly['Cell Line'].apply(lambda x: x+', Poly. Reg.')
        cum_poly['Experiment_ID_Label'] = cum_poly['Experiment ID'].apply(lambda x: x+', Poly. Reg.')

        # concat
        cum = pd.concat([cum, cum_poly], axis=0).reset_index(drop=True)
        if  self._production:
            name = f'{self._name.capitalize()} Production (mmol)'
        else:
            name = f'{self._name.capitalize()} Consumption (mmol)'
        cum['Species'] = self._name.upper()
        cum['Species_label'] = name
        return cum.sort_values(by=['RUN TIME (HOURS)'], kind='stable').reset_index(drop=True)

    def get_sp_rate_df(self, twopt=False, polyreg=False, rollreg=False):
        q1 = pd.DataFrame()
        q2 = pd.DataFrame()
        q3 = pd.DataFrame()

        if (twopt):
            q1 = self.get_twopt_sp_rate_df()
        if (polyreg):
            q2 = self.get_polyreg_sp_rate_df()
        if (rollreg):
            q3 = self.get_rollreg_sp_rate_df()
        df = pd.concat([q1, q2, q3], axis=0).reset_index(drop=True)
        df['Species'] = self._name.upper()
        df['Species_label'] = f'q{self._name.capitalize()} (mmol/10^9 cell/hr)'
        return df

    def get_twopt_sp_rate_df(self):
        info_df = self.get_info_df(self._run_time_hour)
        # name = f'q{self._name} (mmol/109 cell/hr)'
        name = f'Sp. rate'
        q = self._sp_rate.rename(name)
        q = pd.concat([info_df, q], axis=1)
        q['Method'] = 'Two-Pt. Calc.'
        return q
    
    def get_polyreg_sp_rate_df(self):
        info_df = self.get_info_df(self._run_time_hour)
        # name = f'q{self._name} (mmol/109 cell/hr)'
        name = f'Sp. rate'
        q = self._polyreg_sp_rate.rename(name)
        q = pd.concat([info_df, q], axis=1)
        q['Method'] = f'Poly. Reg.'
        q['Order'] = self._polyorder
        return q

    def get_rollreg_sp_rate_df(self):
        info_df = self.get_info_df(self._run_time_mid.rename('RUN TIME (HOURS)'))
        # name = f'q{self._name} (mmol/109 cell/hr)'
        name = f'Sp. rate'
        q = self._rollpolyreg_sp_rate.rename(name)
        q = pd.concat([info_df, q], axis=1)
        q['Method'] = f'Roll. Reg.'
        q['Order'] = self._rollpolyreg_order
        q['Window'] = self._rollpolyreg_window
        return q'''
        

###########################################################################
# Metabolite Class for Nitrogen, and AA Carbon
###########################################################################
class Metabolite2(Species, Polynomial, Rolling):
    '''
    Store information for Nitrogen and AA carbon.

    Attributes
    ---------
        name : str
            name of species.
        measured_data : python object
                MeasuredData object.
        cumulative : pandas.DataFrame
            calculated cumulative consumption/production.
    '''
    def __init__(self, name, measured_data, cumulative):
        '''
        Parameters
        ----------
            name : str
                name of species.
            measured_data : python object
                MeasuredData object.
            cumulative : pandas.DataFrame
                calculated cumulative consumption/production.
        '''
        # Constructor for MeasuredDate Class
        super().__init__(name=name, measured_data=measured_data)

        self._cumulative = cumulative
        self._sp_rate = pd.DataFrame()
        self._idx = self._cumulative[self._cumulative.notnull()].index
        self._run_time_mid = self.__mid_calc_runtime()


    #*** Praivete Methods ***#
    def __mid_calc_runtime(self):
        idx = self._idx                 # Measurement index
        t = self._run_time_hour[idx]         # run time hour

        t_mid = pd.Series(data=[np.nan] * (len(idx)-1),
                            name='RUN TIME MID (HOURS)', dtype='float')

        for i in range(len(idx)-1):
            t_mid.iat[i] = (t.iat[i]+t.iat[i+1])/2

        return t_mid
        