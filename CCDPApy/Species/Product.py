import numpy as np

from .Species import Species
from ..in_process.ProductMixin import ProductMixin
from ..post_process.polynomial.ProductMixin import ProductMixin as Polynomial
from ..post_process.rolling_window_polynomial.ProductMixin import ProductMixin as Rolling

###########################################################################
# Product Mixin Class
###########################################################################
class Product(Species,
              ProductMixin,
              Polynomial,
              Rolling):
    '''
    Product/IgG class.

    Attribute
    ---------
        name : str
            name of species.
        measured_data : python object
                MeasuredData object.
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
        # Constructor for Species
        super().__init__(name=name, measured_data=measured_data)

        # Work with parameters
        df = measured_data.param_df
        conc = df['IgG_(mg/L)']
        idx = conc[conc.notnull()].index  # Measurent Index
        t = df['run_time_(hrs)'].values[idx]    # original run time (hour)

        # Calculate Mid Time from Original Run time
        time_mid = np.array([0.5 * (t[i] + t[i+1]) for i in range(len(t)-1)])

        # Class Members
        self._idx = idx
        self._run_time_mid = time_mid
        self._conc = conc
        

