from .SPRateMixin import SPRateMixin
from .RatioCalcMixin import RatioCalcMixin


class TwoPtMixin(SPRateMixin, RatioCalcMixin):
    '''
    Mixin class for BioProcess to calculate specific rates for species using two-point calculations.

    Methods
    -------
        two_pt_calc
    '''

    def two_pt_calc(self):
        '''Calculate SP. rates for species using two-point calculations.
        '''
        method = 'twopt'

        # Cell
        self._cell.post_process_twopt() # Calculate sp. rate with two-point calc.
        self._cell.set_method_flag(method=method, flag=True)  # Set flag True

        # Oxygen
        self._oxygen.post_process_twopt() # Calculate sp. rate with two-point calc.
        self._oxygen.set_method_flag(method=method, flag=True)  # Set flag True

        # IgG/Product
        self._product.post_process_twopt()    # Calculate sp. rate with two-point calc.
        self._product.set_method_flag(method=method, flag=True)   # Set flag.

        # Metabolites
        data = self._process_data_dict[method]
        for s in self._spc_list:
            s = s.upper()   # Name
            spc = self._spc_dict[s] # Species object
            spc.sp_rate_twopt() # Calculate SP. rate
            spc.set_method_flag(method=method, flag=True)   # Set Flag True
            
            title = f'Two-Pt. Calc. q{s.capitalize()} (mmol/109 cell/hr)'
            data[title] = self._spc_dict[s].get_sp_rate(method='twopt')

        # SP. rates for Nitrogen and AA Carbon
        self.sp_rate_Nit_AAC(method=method)

        # Ratio Calc.
        self.ratio_calc(method=method)

        # Set twopt Flag True
        self.set_process_flag(process=method, flag=True)

    #*** End two_pt_calc ***#

