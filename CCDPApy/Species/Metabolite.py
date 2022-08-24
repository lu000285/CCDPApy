import pandas as pd
import numpy as np

from .Species import Species
from ..in_process.MetaboliteMixin import MetaboliteMixin
from ..post_process.two_point_calc.MetaboliteMixin import MetaboliteMixinTwoPt
from ..post_process.polynomial_regression.PolyRegMixin import PolyRegMixin
from ..post_process.rolling_regression.RollPolyRegMixin import RollPolyregMixin
from ..plot.PlotMixin import PlotMixin

###########################################################################
# Metabolite Class
###########################################################################
class Metabolite(Species, MetaboliteMixin, MetaboliteMixinTwoPt, PolyRegMixin,
                 RollPolyregMixin, PlotMixin):
    '''
    '''             
    def __init__(self,
                 experiment_info,
                 raw_data,
                 name,
                 conc_before_feed,
                 conc_after_feed,
                 feed_conc,
                 cumulative,
                 production=False):
        
        # Constructor for MeasuredDate Class
        super().__init__(experiment_info, raw_data, name)
        
        # Members
        self._conc_before_feed = conc_before_feed
        self._conc_after_feed = conc_after_feed
        self._feed_conc = feed_conc
        self._production = production
        self._idx = self._conc_before_feed[self._conc_before_feed.notnull()].index
        self._cumulative = cumulative

        self._use_feed_conc =  None
        self._use_conc_after_feed = None
    
    # Getters
    def get_info_df(self, t):
        n = len(t)
        id = pd.Series(data=[self._experiment_id]*n,
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

    def get_cumulative_df(self):
        t = self._run_time_hour       
        x = np.linspace(t.iat[0], t.iat[-1], 100)
        x = pd.Series(data=x, name=t.name)
        cum = self.get_info_df(x)
        cum[f'CUM {self._name} (mmol)'] = pd.Series(data=self._polyfit(x))
        cum['Method'] = f'Poly. Reg. Order: {self._polyorder}'
        return cum

    def get_sp_rate_df(self, twopt=True, polyreg=False, rollreg=False):
        info_df = self.get_info_df(self._run_time_hour)

        name = f'q{self._name} (mmol/109 cell/hr)'
        q = self._sp_rate.rename(name)
        q = pd.concat([info_df, q], axis=1)
        q['Method'] = 'Two-Pt. Calc.'

        q2 = pd.DataFrame()
        q3 = pd.DataFrame()

        if (polyreg):
            q2 = self.get_polyreg_sp_rate_df()
        if (rollreg):
            q3 = self.get_rollreg_sp_rate_df()
        
        return pd.concat([q, q2, q3], axis=0)
    
    def get_polyreg_sp_rate_df(self):
        info_df = self.get_info_df(self._run_time_hour)
        name = f'q{self._name} (mmol/109 cell/hr)'
        q = self._polyreg_sp_rate.rename(name)
        q = pd.concat([info_df, q], axis=1)
        q['Method'] = f'Poly. Reg. Order: {self._polyorder}'
        return q

    def get_rollreg_sp_rate_df(self):
        info_df = self.get_info_df(self._run_time_mid.rename('RUN TIME (HOURS)'))
        name = f'q{self._name} (mmol/109 cell/hr)'
        q = self._rollpolyreg_sp_rate.rename(name)
        q = pd.concat([info_df, q], axis=1)
        q['Method'] = f'Roll. Reg. Order: {self._rollpolyreg_order} Window: {self._rollpolyreg_window}'
        return q
        

###########################################################################
# Metabolite Class for Nitrogen, and AA Carbon
###########################################################################
class Metabolite2(Species, PolyRegMixin):
    '''
    '''
    def __init__(self,
                 experiment_info,
                 raw_data,
                 name, 
                 cumulative):

        # Constructor for MeasuredDate Class
        super().__init__(experiment_info, raw_data, name)

        self._cumulative = cumulative
        self._sp_rate = None
        self._idx = self._cumulative[self._cumulative.notnull()].index


    # Setters
    def set_sp_rate(self, sp_rate):
        self._sp_rate = sp_rate