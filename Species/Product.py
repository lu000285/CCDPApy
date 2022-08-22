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
    def __init__(self, experiment_info, raw_data, name):
        # Constructor for Species
        super().__init__(experiment_info, raw_data, name)

        # Class Members
        # Measurent Index
        self._idx = self._product_conc[self._product_conc.notnull()].index

    # Getter
    def get_product_conc(self):
        """
        Get Product Concentration (mg/L)
        
        Parameters
        ----------

        Returns
        -------
        self._product_conc :
            Product Concentration (mg/L)
        """
        return self._product_conc

###########################################################################