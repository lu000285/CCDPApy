import pandas as pd
import numpy as np

from .Species import Species
from ..in_process.CellMixin import CellMixin
from ..post_process.polynomial.CellMixin import CellMixin as Polynomial
from ..post_process.rolling_window_polynomial.LogisticGrowthMixin import LogisticGrowthMixin

###########################################################################
# Cell
###########################################################################
class Cell(Species,
           CellMixin,
           Polynomial, 
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

        # Work with parameters
        df = measured_data.param_df
        xd = df['dead_cell_conc_(10^6_cells/mL)']
        xt = df['total_cell_conc_(10^6_cells/mL)']
        viab = df['viability_(%)']
        
        xv = self._xv
        idx = xv[xv.notnull()].index  # Indices of measurements
        t = df['run_time_(hrs)'].values[idx]    # original run time (hour)

        # Calculate Mid Time from Original Run time
        time_mid = np.array([0.5 * (t[i] + t[i+1]) for i in range(len(t)-1)])

        # Class Members
        self._idx = idx
        self._run_time_mid = time_mid
        self._xd = xd
        self._xt = xt
        self._viability = viab