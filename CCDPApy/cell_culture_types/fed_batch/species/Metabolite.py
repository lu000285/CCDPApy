import pandas as pd
import numpy as np

from CCDPApy.helper import get_measurement_indices
from CCDPApy.cell_culture_types.fed_batch.in_process import MetaboliteMixin as Inprocess
from CCDPApy.cell_culture_types.fed_batch.post_process.polynomial import MetaboliteMixin as Polynomial
from CCDPApy.cell_culture_types.fed_batch.post_process.rolling_window_polynomial import MetaboliteMixin as RollingPolynomial
from .Species import Species

# from CCDPApy.in_process.Fed_batch.MetaboliteMixin import MetaboliteMixin as Inprocess

class Metabolite(Species, Inprocess, Polynomial, RollingPolynomial):
    '''
    Metabolite class.
    Attributes
    ---------
    '''             
    def __init__(self, name, run_time_df, volume_before_sampling, 
                 volume_after_sampling, feed_media_added,
                 viable_cell_conc, separate_feed, separate_feed_sum,
                 conc_before_feed, conc_after_feed, feed_conc, measured_cumulative_conc):
        '''
        Parameters
        ---------
        '''
        super().__init__(name, run_time_df, volume_before_sampling, 
                         volume_after_sampling, feed_media_added, 
                         viable_cell_conc)
        
        # Get indices of the measurements from the concentration
        conc = conc_before_feed['value']
        idx = get_measurement_indices(conc)
        
        # Class Members
        self._idx = idx
        self._separate_feed = separate_feed
        self._separate_feed_sum = separate_feed_sum
        self._conc_before_feed = conc_before_feed
        self._conc_after_feed = conc_after_feed
        self._feed_conc = feed_conc
        self._measured_cumulative_conc = measured_cumulative_conc
        value = measured_cumulative_conc['value']
        self._measured_cumulative_flag = True if value.notnull().any() else False # True if there is the measurement of cumulative concentration.
    
    @property
    def measurement_index(self):
        return self._idx
    @property
    def conc_before_feed(self):
        return self._conc_before_feed
    @property
    def conc_after_feed(self):
        return self._conc_after_feed
    @property
    def feed_conc(self):
        return self._feed_conc
    @property
    def measured_cumulative_conc(self):
        return self._measured_cumulative_conc
    @property
    def measured_cumulative_flag(self):
        return self._measured_cumulative_flag
    @property
    def separate_feed(self):
        return self._separate_feed
    @property
    def separate_feed_sum(self):
        return self._separate_feed_sum