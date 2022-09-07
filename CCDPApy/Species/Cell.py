import pandas as pd

from .Species import Species
from ..in_process.CellMixin import CellMixin
from ..post_process.two_point_calc.CellMixin import CellMixnTwoPt
from ..post_process.polynomial_regression.CellMixin import CellMixinPolyReg
from ..post_process.rolling_regression.LogisticGrowthMixin import LogisticGrowthMixin

###########################################################################
# Cell
###########################################################################
class Cell(Species,
           CellMixin,
           CellMixnTwoPt,
           CellMixinPolyReg, 
           LogisticGrowthMixin):
    '''
    Cell class.

    Attributes
    ---------
        name : str
            name of species.
        measured_data : python object
            MeasuredData object.

    Methods
    -------
        runtime_mid_calc
    '''
    # Constructor
    def __init__(self, name, measured_data):
        '''
        Parameters
        ---------
            name : str
                name of species.
            measured_data : python object
                MeasuredData object.
        '''
        # Constructor for Spcies Class
        super().__init__(name=name, measured_data=measured_data)

        # Members
        self._idx = self._xv[self._xv.notnull()].index

        # Calculate run time middle
        self._runtime_mid_calc()

    
    # Private method
    def _runtime_mid_calc(self):
        '''
        Mid-point calculation of conc. and run time

        Parameters
        ----------
            idx : 
                measurements index.
            t : 
                run time (hrs).
            t_mid :
                midpoints run time (hrs).
        '''
        idx = self._idx # Measurement index
        t = self._run_time_hour[idx] # original run time (hour)
        t_mid = pd.Series(data=[pd.NA] * (len(t)-1),
                            name='RUN TIME MID (HOURS)')
        # Calculate Mid Time from Original Run time
        for i in range(len(t_mid)):
            t_mid.iat[i] = (t.iat[i] + t.iat[i+1])/2

        self._run_time_mid = t_mid
