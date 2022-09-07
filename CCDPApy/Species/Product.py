from .Species import Species
from ..in_process.ProductMixin import ProductMixin
from ..post_process.two_point_calc.ProductMixin import ProductTwoptMixn
from ..post_process.polynomial_regression.PolyRegMixin import PolyRegMixin

###########################################################################
# Product Mixin Class
###########################################################################
class Product(Species,
              ProductMixin,
              ProductTwoptMixn,
              PolyRegMixin):
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

        # Class Members
        # Measurent Index
        self._idx = self._product_conc[self._product_conc.notnull()].index
