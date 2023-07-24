import numpy as np

from CCDPApy.helper import get_measurement_indices
from CCDPApy.cell_culture_types.fed_batch.in_process import ProductMixin as Inprocess
from CCDPApy.cell_culture_types.fed_batch.post_process.polynomial import ProductMixin as Polynomial
from CCDPApy.cell_culture_types.fed_batch.post_process.rolling_window_polynomial import ProductMixin as RollingPolynomial
from .Species import Species

class Product(Species, Inprocess, Polynomial, RollingPolynomial):
    '''
    Product/IgG class.

    Attribute
    ---------
    '''
    # Constructor
    def __init__(self, name, run_time_df, volume_before_sampling, 
                 volume_after_sampling, feed_media_added,
                 viable_cell_conc, production):
        '''
        Parameters
        ---------
        '''
        super().__init__(name, run_time_df, volume_before_sampling, 
                         volume_after_sampling, feed_media_added, 
                         viable_cell_conc)
        
        # Get indices of the measurements from the concentration
        conc = production['value']
        idx = get_measurement_indices(conc)

        # Class Members
        self._idx = idx
        self._production = production

    @property
    def measurement_index(self):
        return self._idx
    
    @property
    def production(self):
        return self._production