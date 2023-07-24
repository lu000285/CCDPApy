import pandas as pd
import numpy as np

from CCDPApy.cell_culture_types.fed_batch.in_process.equation import growth_rate
from CCDPApy.Constants import CellNameSpace, RUN_TIME_DAY_COLUMN, RUN_TIME_HOUR_COLUMN

from .GetterMixin import GetterMixin

CONSTANTS = CellNameSpace()

class CellMixin(GetterMixin):
    '''Cell Mixin Class for polynomial regression.
    '''
    def polynomial(self, deg, data_num=50):
        '''Calculate the cumulative concentration and specific rate of cell using polynomial regression.
        Parameters
        ----------
            deg : int
                a polynomial degree for polynomial regression.
        '''
        idx = self.measurement_index
        t = self.run_time_hour#[idx]
        s = self.cumulative_conc['value'].values#[idx]
        xv = self.viable_cell_conc['value'].values#[idx]
        v1 = self.volume_before_sampling#[idx]
        v2 = self.volume_after_sampling#[idx]
        unit = self.cumulative_conc['unit'].iat[0]
        # state = self.cumulative_conc['state'].iat[0]
        # Get run time dataframe
        run_time = self.run_time

        
        # Fitting a polynomial
        poly_func = np.poly1d(np.polyfit(x=t, y=s, deg=deg))

        # Calculate cumulative concentration from the polynomial function.
        t_poly = np.linspace(t[0], t[-1], data_num)
        day_poly = np.floor(t_poly / 24).astype(int)
        run_time_poly = pd.DataFrame(data={RUN_TIME_DAY_COLUMN: day_poly,
                                           RUN_TIME_HOUR_COLUMN: t_poly})
        s_poly = poly_func(t_poly)
        s_poly = pd.DataFrame(data=s_poly, columns=['value'])
        s_poly['unit'] = unit
        # s_poly['state'] = state
        s_poly['method'] = 'polynomial'
        s_poly['degree'] = deg
        s_poly.index.name = 'Cumulative production'

        # Calculate growth rate from the cumulative production obtained by polynomial regression. 
        r_poly = np.zeros(self.samples)
        r_poly.fill(np.nan)
        s = s_poly['value'].values#[idx]
        for i in range(1, len(t)):
            r_poly[i] = growth_rate(s[i-1], s[i], xv[i-1], xv[i], v1[i], v2[i-1], t[i-1], t[i])
        r_poly = pd.DataFrame(data=r_poly, columns=['value'])
        r_poly['unit'] = CONSTANTS.SP_RATE_UNIT
        r_poly['method'] = 'polynomial'
        r_poly.index.name = CONSTANTS.SP_RATE

        # Store the variables
        self._poly_degree = deg
        self._poly_func = poly_func
        self._cumulative_poly = pd.concat([run_time_poly, s_poly], axis=1)
        self._sp_rate_poly = pd.concat([run_time, r_poly], axis=1)