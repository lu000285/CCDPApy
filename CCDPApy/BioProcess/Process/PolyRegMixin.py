import pandas as pd

from .RatioCalcMixin import RatioCalcMixin
from ...helper_func.helper_func import input_path

class PolyRegMixin(RatioCalcMixin):
    '''
    Mixin class for BioProcess class to calculate specific rates for species using polynomial regression.
    '''
    def poly_regression(self, polyorder_file):
        '''
        Calculate SP. rates for species using polynomial regression.

        Parameters
        ----------
            polyorder_file : str
                name of a Excel file for polynomial regression order.
        '''
        method = 'polyreg'
        species = self._spc_dict

        # Check polynomial file
        if (polyorder_file):
            path = input_path(file_name=polyorder_file)
            # polyorder df
            polyorder = pd.read_excel(io=path, index_col=0)
            polyorder.index = [name.upper() for name in polyorder.index]

        # 
        for spc_name, spc in species.items():
            # Get a polynomial degree in the file, or use 3 as default
            try:
                degree = polyorder.loc[spc_name.upper()].iat[0]
            except:
                degree = 3
            # Fitting the polynomial
            spc.polynomial(deg=degree)

        # Set polyreg flag True
        self.set_process_flag(process=method, flag=True)
