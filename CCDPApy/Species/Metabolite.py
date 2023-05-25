import pandas as pd
import numpy as np

from .Species import Species
from ..in_process.MetaboliteMixin import MetaboliteMixin
from ..post_process.two_point_calc.MetaboliteMixin import MetaboliteMixinTwoPt
from ..post_process.polynomial_regression.PolyRegMixin import PolyRegMixin
from ..post_process.rolling_regression.RollPolyRegMixin import RollPolyregMixin
from ..plotting.PlotMixin import PlotMixin

###########################################################################
# Metabolite Class
###########################################################################
class Metabolite(Species,
                 MetaboliteMixin,
                 MetaboliteMixinTwoPt,
                 PolyRegMixin,
                 RollPolyregMixin,
                 PlotMixin):
    '''
    Metabolite class.

    Attributes
    ---------
        name : str
                name of species.
        measured_data : python object
                MeasuredData object.
        conc_before_feed : pandas.DataFrame
            species concentration before feeding.
        conc_after_feed : pandas.DataFrame
            species concentration after feeding.
        feed_conc : pandas.DataFrame
            feed concentration.
        cumulative : pandas.DataFrame
            calculated cumulative consumption/production for species.
        production : bool, default=False, optional
            True if species is produced by bioprocess.
    '''             
    def __init__(self,
                 name,
                 measured_data,
                 conc_before_feed,
                 conc_after_feed,
                 feed_conc,
                 cumulative,
                 production=False):
        '''
        Parameters
        ---------
            name : str
                name of species.
            measured_data : python object
                MeasuredData object.
            conc_before_feed : pandas.DataFrame
                species concentration before feeding.
            conc_after_feed : pandas.DataFrame
                species concentration after feeding.
            feed_conc : pandas.DataFrame
                feed concentration.
            cumulative : pandas.DataFrame
                calculated cumulative consumption/production for species.
            production : bool, default=False, optional
                True if species is produced by bioprocess.
        '''
        # Constructor for MeasuredDate Class
        super().__init__(name=name, measured_data=measured_data)
        
        # Members
        self._conc_before_feed = conc_before_feed
        self._conc_after_feed = conc_after_feed
        self._feed_conc = feed_conc
        self._production = production
        self._idx = self._conc_before_feed[self._conc_before_feed.notnull()].index
        self._cumulative = cumulative

        self._use_feed_conc =  False
        self._use_conc_after_feed = False
    
    # Getters
    def get_info_df(self, t):
        n = len(t)
        id = pd.Series(data=[self._exp_id]*n,
                        name='Experiment ID')
        cl = pd.Series(data=[self._cell_line_name]*n,
                        name='Cell Line')
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
        conc['Species'] = self._name.capitalize()

        return conc.sort_values(by=['RUN TIME (HOURS)'], kind='stable').reset_index(drop=True)
        

    def get_cumulative_df(self):
        t = self._run_time_hour       
        x = np.linspace(t.iat[0], t.iat[-1], 100)
        x = pd.Series(data=x, name=t.name)
        cum = self.get_info_df(x)
        # cum[f'CUM {self._name} (mmol)'] = pd.Series(data=self._polyfit(x))
        cum[f'Cumulative Prod./Cons.'] = pd.Series(data=self._polyfit(x))
        cum['Method'] = f'Poly. Reg. Order: {self._polyorder}'
        cum['Species'] = self._name.capitalize()
        return cum

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
        
        return pd.concat([q1, q2, q3], axis=0).reset_index(drop=True)

    def get_twopt_sp_rate_df(self):
        info_df = self.get_info_df(self._run_time_hour)
        # name = f'q{self._name} (mmol/109 cell/hr)'
        name = f'Sp. rate'
        q = self._sp_rate.rename(name)
        q = pd.concat([info_df, q], axis=1)
        q['Species'] = self._name
        q['Method'] = 'Two-Pt. Calc.'
        return q
    
    def get_polyreg_sp_rate_df(self):
        info_df = self.get_info_df(self._run_time_hour)
        # name = f'q{self._name} (mmol/109 cell/hr)'
        name = f'Sp. rate'
        q = self._polyreg_sp_rate.rename(name)
        q = pd.concat([info_df, q], axis=1)
        q['Species'] = self._name
        q['Method'] = f'Poly. Reg.'
        q['Order'] = self._polyorder
        return q

    def get_rollreg_sp_rate_df(self):
        info_df = self.get_info_df(self._run_time_mid.rename('RUN TIME (HOURS)'))
        # name = f'q{self._name} (mmol/109 cell/hr)'
        name = f'Sp. rate'
        q = self._rollpolyreg_sp_rate.rename(name)
        q = pd.concat([info_df, q], axis=1)
        q['Species'] = self._name
        q['Method'] = f'Roll. Reg.'
        q['Order'] = self._rollpolyreg_order
        q['Window'] = self._rollpolyreg_window
        return q
        

###########################################################################
# Metabolite Class for Nitrogen, and AA Carbon
###########################################################################
class Metabolite2(Species, PolyRegMixin, RollPolyregMixin):
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
        