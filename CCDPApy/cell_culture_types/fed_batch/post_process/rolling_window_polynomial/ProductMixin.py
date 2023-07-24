import pandas as pd
import numpy as np

from CCDPApy.Constants import ProductNameSpace
from CCDPApy.Constants import RUN_TIME_DAY_COLUMN, RUN_TIME_HOUR_COLUMN

from .mid_point_calc import mid_point_production
from .GetterMixin import GetterMixin

CONSTANTS = ProductNameSpace()

class ProductMixin(GetterMixin):
    '''Rolling window polynomial regression Mixin Class for Product/IgG.
    '''
    def rolling_window_polynomial(self, degree, windows):
        idx = self.measurement_index
        x = self.run_time_hour[idx]
        v = self.volume_before_sampling[idx]
        y = self.cumulative_conc['value'].values[idx]
        vcc = self.viable_cell_conc['value'].values[idx]
        
        # Get mid points for time (day, hour) and concentration.
        t_day_mid, t_hour_mid, c_mid = mid_point_production(t_day=self.run_time_day[idx],
                                                            t_hour=x,
                                                            c=y)
        
        # Calculate Specific Rate from Derivetive of Polynomial Regression on Cumularive Consumption/Production
        q = np.zeros(len(x)-1)
        q.fill(np.nan)

        # Calculate SP. rate
        x_mid = t_hour_mid
        for i in range(0, len(x_mid)):
            if (i + 1) < (windows / 2):
                x_roll = x[0: windows]
                y_roll = y[0: windows]
                # Polynomial Regression for Cumulative Consumption/Production
                fit = np.polyfit(x_roll, y_roll, degree)  # Fitting data to polynomial Regression (Get slopes)
                p = np.poly1d(fit)  # Get polynomial curve for Cumulative Consumption/Production

                dp1 = p.deriv()      # first derivetive of polynomial fit

                dy = dp1(x_mid[i])      # derivetive values corresponding to x

                q[i] = dy / (vcc[i] * v[i]+vcc[i+1] * v[i+1]) * 2 * 1000

            elif (i + windows / 2) > len(x):
                x_roll = x[int(len(x)-windows/2-1):len(x)]
                y_roll = y[int(len(x)-windows/2-1):len(x)]
                # Polynomial Regression for Cumulative Consumption/Production
                fit = np.polyfit(x_roll, y_roll, degree)  # Fitting data to polynomial Regression (Get slopes)
                p = np.poly1d(fit)  # Get polynomial curve for Cumulative Consumption/Production

                dp1 = p.deriv()      # first derivetive of polynomial fit

                dy = dp1(x_mid[i])      # derivetive values corresponding to x

                q[i] = dy / (vcc[i] * v[i]+vcc[i+1] * v[i+1]) * 2 * 1000
                
            else:
                x_roll = x[int(i-windows/2+1):int(i+windows/2+1)]
                y_roll = y[int(i-windows/2+1):int(i+windows/2+1)]
                # Polynomial Regression for Cumulative Consumption/Production
                fit = np.polyfit(x_roll, y_roll, degree)  # Fitting data to polynomial Regression (Get slopes)
                p = np.poly1d(fit)  # Get polynomial curve for Cumulative Consumption/Production

                dp1 = p.deriv()      # first derivetive of polynomial fit

                dy = dp1(x_mid[i])      # derivetive values corresponding to x
                
                q[i] = dy / (vcc[i] * v[i] + vcc[i+1] * v[i+1]) * 2 * 1000

        # Cumulative concentration middle points.
        conc_mid = pd.DataFrame(data={'Run Time Mid (day)': t_day_mid,
                                            'Run Time Mid (hr)': t_hour_mid,
                                            'value': c_mid})
        conc_mid['unit'] = self.production['unit'].iat[0]

        # Sp. rate by rolling window polynomial
        r_roll_poly = pd.DataFrame(data={RUN_TIME_DAY_COLUMN: t_day_mid,
                                         RUN_TIME_HOUR_COLUMN: t_hour_mid,
                                         'value': q})
        r_roll_poly['unit'] = CONSTANTS.SP_RATE_UNIT
        r_roll_poly['method'] = 'rollingWindowPolynomial'
        r_roll_poly['degree'] = degree
        r_roll_poly['window'] = windows
        r_roll_poly.index.name = CONSTANTS.SP_RATE

        # store values
        self._roll_polyorder = degree
        self._roll_polywindow = windows
        self._production_mid = conc_mid
        self._sp_rate_rolling = r_roll_poly

    @property
    def production_mid(self):
        return self._production_mid