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

        # Check polynomial file
        if (polyorder_file):
            path = input_path(file_name=polyorder_file)
            # polyorder df
            polyorder = pd.read_excel(io=path, index_col=0)
            polyorder.index = [name.upper() for name in polyorder.index]

        # Cell
        try:
            order = polyorder.loc['CELL'].iat[0]
        except:
            order = 3
        cell = self._cell
        cell.polyreg(polyorder=order)
        cell.set_method_flag(method=method, flag=True)

        # Oxygen
        try: 
            order = polyorder.loc['OXYGEN'].iat[0]
        except:
            order = 3
        oxygen = self._oxygen
        oxygen.polyreg(polyorder=order)
        oxygen.set_method_flag(method=method, flag=True)

        # IgG
        try:
            order = polyorder.loc['IGG'].iat[0]
        except:
            order = 3
        product = self._product
        product.polyreg(polyorder=order)
        product.set_method_flag(method=method, flag=True)
        
        # Metabolites
        data = self.get_process_data(method=method)

        for s in (self._spc_list + self._spc_list_2):
            s = s.upper() # Name
            spc = self._spc_dict[s]    # species object
            try:
                order = polyorder.loc[s].iat[0]
            except:
                order = 3
            spc.polyreg(polyorder=order)    # Calculate sp. rate
            spc.set_method_flag(method=method, flag=True)   # Set Flag True

            title = f'Poly. Reg. Order: {order} q{s.capitalize()} (mmol/109 cell/hr)'
            data[title] = spc.get_sp_rate(method=method)

        # Ratio Calc
        self.ratio_calc(method=method)

        # Set polyreg flag True
        self.set_process_flag(process=method, flag=True)
