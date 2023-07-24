import pandas as pd
import numpy as np

from CCDPApy.helper import get_measurement_indices
from CCDPApy.cell_culture_types.fed_batch.in_process import CellMixin as Inprocess
from CCDPApy.cell_culture_types.fed_batch.post_process.polynomial import CellMixin as Polynomial
from CCDPApy.cell_culture_types.fed_batch.post_process.rolling_window_polynomial import LogisticGrowthMixin as LogisticGrowoth
from .Species import Species

class Cell(Species, Inprocess, Polynomial, LogisticGrowoth):
    '''Cell class.
    Attributes
    ---------
    '''
    # Constructor
    def __init__(self, name, run_time_df, volume_before_sampling, 
                 volume_after_sampling, feed_media_added,
                 viable_cell_conc, dead_cell_conc, total_cell_conc):
        '''
        Parameters
        ---------
        '''
        # Constructor for Spcies Class
        super().__init__(name, run_time_df, volume_before_sampling, volume_after_sampling, 
                         feed_media_added, viable_cell_conc)
        
        # Calculate viability
        value = viable_cell_conc['value'].values / total_cell_conc['value'].values * 100
        viab = viable_cell_conc.copy()
        viab.index.name = 'Viability'
        viab['value'] = value
        viab['unit'] = '%'

        # Get indices of the measurement from the viable cell concentration
        xv = self._viable_cell_conc['value']
        idx = get_measurement_indices(xv)

        # Class Members
        self._idx = idx
        self._dead_cell_conc = dead_cell_conc
        self._total_cell_conc = total_cell_conc
        self._viability = viab

    @property
    def measurement_index(self):
        return self._idx
    @property
    def dead_cell_conc(self):
        return self._dead_cell_conc
    @property
    def total_cell_conc(self):
        return self._total_cell_conc
    @property
    def viability(self):
        return self._viability