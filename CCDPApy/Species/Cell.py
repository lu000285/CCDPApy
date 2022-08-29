import pandas as pd

from .Species import Species
from ..in_process.CellMixin import CellMixin
from ..post_process.two_point_calc.CellMixin import CellMixnTwoPt
from ..post_process.polynomial_regression.CellMixin import CellMixinPolyReg
from ..post_process.rolling_regression.LogisticGrowthMixin import LogisticGrowthMixin

###########################################################################
# Cell
###########################################################################
class Cell(Species, CellMixin, CellMixnTwoPt, CellMixinPolyReg, LogisticGrowthMixin):
    '''
    '''
    # Constructor
    def __init__(self, experiment_info, raw_data, feed_name, name):

        # Constructor for Spcies Class
        super().__init__(experiment_info, raw_data, feed_name, name)

        # Members
        self._idx = self._xv[self._xv.notnull()].index

        # Calculate run time middle
        self.runtime_mid_calc()

    # Mid-point calculation of conc. and run time
    def runtime_mid_calc(self):
        idx = self._idx # Measurement index
        t = self._run_time_hour[idx] # original run time (hour)
        t_mid = pd.Series(data=[pd.NA] * (len(t)-1),
                            name='RUN TIME MID (HOURS)')
        # Calculate Mid Time from Original Run time
        for i in range(len(t_mid)):
            t_mid.iat[i] = (t.iat[i] + t.iat[i+1])/2

        self._run_time_mid = t_mid

###########################################################################