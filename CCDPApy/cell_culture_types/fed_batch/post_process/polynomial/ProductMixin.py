import numpy as np
import pandas as pd

from CCDPApy.Constants import RUN_TIME_DAY_COLUMN, RUN_TIME_HOUR_COLUMN
from CCDPApy.Constants import ProductNameSpace
from .GetterMixin import GetterMixin

Constants = ProductNameSpace()

class ProductMixin(GetterMixin):
    '''Product/IgG Mixin Class for polynomial regression.
    Methods
    -------
        polynomial
    '''
    def polynomial(self, deg, data_num=50):
        '''Calculate the cumulative concentration and specific rate of produc/IgG using polynomial regression.
        Parameters
        ----------
            deg : int
                a polynomial degree for polynomial regression.
        '''
        idx = self.measurement_index
        s = self.cumulative_conc['value'].values[idx]
        t = self.run_time_hour[idx]
        xv = self.viable_cell_conc['value'].values
        v = self.volume_before_sampling#[idx]
        unit = self.cumulative_conc['unit'].iat[0]
        state = self.cumulative_conc['state'].iat[0]
        # Get run time dataframe
        run_time = self.run_time

        # Fitting a polynomial
        poly_func = np.poly1d(np.polyfit(x=t, y=s, deg=deg))

        # Calculate cumulative concentration from the polynomial function
        t_poly = np.linspace(t[0], t[-1], data_num)
        day_poly = np.floor(t_poly / 24).astype(int)
        run_time_poly = pd.DataFrame(data={RUN_TIME_DAY_COLUMN: day_poly,
                                           RUN_TIME_HOUR_COLUMN: t_poly})
        s_poly = poly_func(t_poly)
        s_poly = pd.DataFrame(data=s_poly, columns=['value'])
        s_poly['unit'] = unit
        s_poly['state'] = state
        s_poly['method'] = 'polynomial'
        s_poly['degree'] = deg
        s_poly.index.name = 'Cumulative concentration'

        # Get the derivetive of the polynomial, and evaluate the derivetive at the run time.
        poly_deriv = poly_func.deriv()
        y = poly_deriv(self.run_time_hour)

        # Calculate the specific rate from the derivetive of the polynomial function
        r_poly = y / (xv * v) * 1000
        r_poly[0] = np.nan
        r_poly = pd.DataFrame(data=r_poly, columns=['value'])
        r_poly['unit'] = Constants.SP_RATE_UNIT
        r_poly['method'] = 'polynomial'
        r_poly['degree'] = deg
        r_poly.index.name = Constants.SP_RATE

        # Store the variables
        self._poly_degree = deg
        self._poly_func = poly_func
        self._cumulative_poly = pd.concat([run_time_poly, s_poly], axis=1)
        self._sp_rate_poly = pd.concat([run_time, r_poly], axis=1)