import pandas as pd
import numpy as np

from CCDPApy.constants import MetaboliteNameSpace
from CCDPApy.constants import RUN_TIME_DAY_COLUMN, RUN_TIME_HOUR_COLUMN

from .mid_point_calc import mid_point_conc
from .GetterMixin import GetterMixin

CONSTANTS = MetaboliteNameSpace()

class MetaboliteMixin(GetterMixin):
    '''Rolling window polynomial regression Mixin Class for metabolites.
    '''
    def rolling_window_polynomial(self, degree, windows):
        '''Calculate Specific Rate from Derivetive of Polynomial Regression on Cumularive Consumption/Production.
        '''
        idx = self.measurement_index
        x = self.run_time_hour[idx]
        v = self.volume_before_sampling[idx]
        y = self.cumulative_conc['value'].values[idx]
        vcc = self.viable_cell_conc['value'].values[idx]
        
        # x_mid = self._run_time_mid
        t_day_mid, t_hour_mid, c_mid = mid_point_conc(t_day=self.run_time_day[idx],
                                                      t_hour=x,
                                                      c1=self.conc_after_feed['value'].values[idx],
                                                      c2=self.conc_before_feed['value'].values[idx],)
        
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
                if(self._measured_cumulative_flag):
                    q[idx[i]] = dy / (vcc[i] + vcc[i+1])*2
                else:
                    q[idx[i]] = dy / (vcc[i] * v[i]+vcc[i+1] * v[i+1]) * 2 * 1000

            elif (i + windows / 2) > len(x):
                x_roll = x[int(len(x)-windows/2-1):len(x)]
                y_roll = y[int(len(x)-windows/2-1):len(x)]
                # Polynomial Regression for Cumulative Consumption/Production
                fit = np.polyfit(x_roll, y_roll, degree)  # Fitting data to polynomial Regression (Get slopes)
                p = np.poly1d(fit)  # Get polynomial curve for Cumulative Consumption/Production

                dp1 = p.deriv()      # first derivetive of polynomial fit

                dy = dp1(x_mid[i])      # derivetive values corresponding to x
                if(self._measured_cumulative_flag):
                    q[idx[i]] = dy / (vcc[i] + vcc[i+1]) * 2
                else:
                    q[idx[i]] = dy / (vcc[i] * v[i]+vcc[i+1] * v[i+1]) * 2 * 1000
                
            else:
                x_roll = x[int(i-windows/2+1):int(i+windows/2+1)]
                y_roll = y[int(i-windows/2+1):int(i+windows/2+1)]
                # Polynomial Regression for Cumulative Consumption/Production
                fit = np.polyfit(x_roll, y_roll, degree)  # Fitting data to polynomial Regression (Get slopes)
                p = np.poly1d(fit)  # Get polynomial curve for Cumulative Consumption/Production

                dp1 = p.deriv()      # first derivetive of polynomial fit

                dy = dp1(x_mid[i])      # derivetive values corresponding to x
                if(self._measured_cumulative_flag):
                    q[idx[i]] = dy / (vcc[i] + vcc[i+1]) * 2
                else:
                    q[idx[i]] = dy / (vcc[i] * v[i] + vcc[i+1] * v[i+1]) * 2 * 1000

        #Concentration middle points.
        conc_mid = pd.DataFrame(data={'Run Time Mid (day)': t_day_mid,
                                      'Run Time Mid (hr)': t_hour_mid,
                                      'value': c_mid})
        conc_mid['unit'] = CONSTANTS.CONCE_UNIT

        # Sp. rate by rolling window polynomial
        r_roll_poly = pd.DataFrame(data={RUN_TIME_DAY_COLUMN: t_day_mid,
                                         RUN_TIME_HOUR_COLUMN: t_hour_mid,
                                         'value': q})
        r_roll_poly['unit'] = CONSTANTS.SP_RATE_UNIT
        r_roll_poly['method'] = 'rollingWindowPolynomial'
        r_roll_poly['degree'] = degree
        r_roll_poly['window'] = windows

        # store values
        self._roll_polyorder = degree
        self._roll_polywindow = windows
        self._conc_mid = conc_mid
        self._sp_rate_rolling = r_roll_poly