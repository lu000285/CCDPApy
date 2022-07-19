import pandas as pd

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
        


###########################################################################
# Metabolite Class for Nitrogen, and AA Carbon
###########################################################################
class Metabolite2(Species, PolyRegMixin):
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