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
    def __init__(self, experiment_info, raw_data, name):

        # Constructor for Spcies Class
        super().__init__(experiment_info, raw_data, name)

        # Members
        self._idx = self._xv[self._xv.notnull()].index

    # Getters
    def get_xv(self):
        """
        Get Viable Cell Concentration (x106 cells/mL)
        
        Parameters
        ----------

        Returns
        -------
        self._xv :
            Viable Cell Concentration (x106 cells/mL)
        """
        return self._xv

    def get_xd(self):
        """
        Get Dead Cell Concentration (x106 cells/mL)
        
        Parameters
        ----------

        Returns
        -------
        self._xd :
            Dead Cell Concentration (x106 cells/mL)
        """
        return self._xd

    def get_xt(self):
        """
        Get Total Cell Concentration (x106 cells/mL)
        
        Parameters
        ----------

        Returns
        -------
        self._xt :
            Total Cell Concentration (x106 cells/mL)
        """
        return self._xt

    def get_viability(self):
        """
        Get Viability (%)
        
        Parameters
        ----------

        Returns
        -------
        self._viability :
            Viability (%)
        """
        return self._viability
###########################################################################