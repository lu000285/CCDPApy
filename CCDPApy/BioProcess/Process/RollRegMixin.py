import pandas as pd

from .RatioCalcMixin import RatioCalcMixin

class RollRegMixin(RatioCalcMixin):
    '''
    Mixin class for BioProcess to calcuarate specific rates for species using rolling polynomial regression.

    Mehods
    ------
        rolling_regression
    '''
    def roll_regression(self, degree=3, windows=6):
        '''
        Calculate SP. rate for species using rolling polynomial regression.

        Parameters
        ----------
            degree : int, defalut=3, optional
                polynomial degree for rolling polynomial regression.
            windows : int, default=6, optional
                data point size used for rolling polynomial regression.
        '''
        method = 'rollreg'
        species = self._spc_dict

        # Popping cell, and oxygen
        cell = species.pop('cell'.upper())
        oxygen = species.pop('oxygen'.upper())

        # Calculate logistic growth rate
        cell.midcalc_growth_rate_calc()

        # Calculate specific rate using rolling window polynomial
        for spc in species.values():
            # calculate sp. rate
            spc.rolling_window_polynomial(degree, windows)

        # Update dictionary
        species.update({'cell'.upper(): cell, 'oxygen'.upper(): oxygen})
        
        # Set flag true
        self.set_process_flag(process=method, flag=True)

    #*** End rolling_regression ***#