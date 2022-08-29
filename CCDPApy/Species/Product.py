from .Species import Species
from ..in_process.ProductMixin import ProductMixin
from ..post_process.two_point_calc.ProductMixin import ProductTwoptMixn
from ..post_process.polynomial_regression.PolyRegMixin import PolyRegMixin

###########################################################################
# Product Mixin Class
###########################################################################
class Product(Species, ProductMixin, ProductTwoptMixn, PolyRegMixin):
    '''
    '''
    # Constructor
    def __init__(self, experiment_info, raw_data, feed_name, name):
        # Constructor for Species
        super().__init__(experiment_info, raw_data, feed_name, name)

        # Class Members
        # Measurent Index
        self._idx = self._product_conc[self._product_conc.notnull()].index


###########################################################################