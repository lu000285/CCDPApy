import pandas as pd
import numpy as np

# Rolling Polynomial Regression Mixin Class
class RollPolyregMixin:
    def rolling_poly_regression(self, polyreg_order=3, windows=4):
        idx = self._idx
        x = self._run_time_hour[idx]
        y = self._cumulative[idx]
        vcc = self._xv[idx]
        v = self._v_before_sampling[idx]
        x_mid = self._run_time_mid
        
        self._rollpolyreg_order = polyreg_order
        self._rollpolyreg_window = windows

        # Calculate Specific Rate from Derivetive of Polynomial Regression on Cumularive Consumption/Production
        pre = f'Roll. Poly. Reg. Order: {polyreg_order} Window: {windows}'
        title = f'{pre} q{self._name.capitalize()} (mmol/109 cell/hr)'
        q = pd.Series(data=[pd.NA] * (len(x)-1), name=title)

        # Calculate SP. rate
        for i in range(0, len(x_mid)):
            if i+1 < windows/2:
                x_roll = x[0:windows]
                y_roll = y[0:windows]
                # Polynomial Regression for Cumulative Consumption/Production
                fit = np.polyfit(x_roll, y_roll, polyreg_order)  # Fitting data to polynomial Regression (Get slopes)
                p = np.poly1d(fit)  # Get polynomial curve for Cumulative Consumption/Production

                dp1 = p.deriv()      # first derivetive of polynomial fit

                dy = dp1(x_mid[i])      # derivetive values corresponding to x
                if(self._direct_cumulative):
                    q.iat[i] = dy / (vcc.iat[i] + vcc.iat[i+1])*2
                else:
                    q.iat[i] = dy / (vcc.iat[i] * v.iat[i]+vcc.iat[i+1] * v.iat[i+1])*2 * 1000

            elif i+windows/2 > len(x):
                x_roll = x[int(len(x)-windows/2-1):len(x)]
                y_roll = y[int(len(x)-windows/2-1):len(x)]
                # Polynomial Regression for Cumulative Consumption/Production
                fit = np.polyfit(x_roll, y_roll, polyreg_order)  # Fitting data to polynomial Regression (Get slopes)
                p = np.poly1d(fit)  # Get polynomial curve for Cumulative Consumption/Production

                dp1 = p.deriv()      # first derivetive of polynomial fit

                dy = dp1(x_mid[i])      # derivetive values corresponding to x
                if(self._direct_cumulative):
                    q.iat[i] = dy / (vcc.iat[i] + vcc.iat[i+1])*2
                else:
                    q.iat[i] = dy / (vcc.iat[i] * v.iat[i]+vcc.iat[i+1] * v.iat[i+1])*2 * 1000
                
            else:
                x_roll = x[int(i-windows/2+1):int(i+windows/2+1)]
                y_roll = y[int(i-windows/2+1):int(i+windows/2+1)]
                # Polynomial Regression for Cumulative Consumption/Production
                fit = np.polyfit(x_roll, y_roll, polyreg_order)  # Fitting data to polynomial Regression (Get slopes)
                p = np.poly1d(fit)  # Get polynomial curve for Cumulative Consumption/Production

                dp1 = p.deriv()      # first derivetive of polynomial fit

                dy = dp1(x_mid[i])      # derivetive values corresponding to x
                if(self._direct_cumulative):
                    q.iat[i] = dy / (vcc.iat[i] + vcc.iat[i+1])*2
                else:
                    q.iat[i] = dy / (vcc.iat[i] * v.iat[i]+vcc.iat[i+1] * v.iat[i+1])*2 * 1000

        self._rollpolyreg_sp_rate = q   # Polynomial Fit SP. rate

