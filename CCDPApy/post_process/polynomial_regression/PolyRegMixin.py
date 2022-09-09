import numpy as np
import pandas as pd

###########################################################################
# Polynomial Regression Mixin Class
class PolyRegMixin:
    '''
    '''
    # Call Function
    def polyreg(self, polyorder=3):
        # Fitting
        self.polyreg_fit(polyorder=polyorder)

        # Get Polyreg Cumulative
        self.polyreg_cumulative()

        # Get Polyreg SP. Rate
        self.polyreg_sp_rate()


    # Fitting cumulative to Polynomial Regression
    def polyreg_fit(self, polyorder=3):
        idx = self._idx                     # Measurement Index
        t = self._run_time_hour[idx]        # Run Time (hrs)
        s = self._cumulative[idx]           # Cumulative Consumption/Production (mM)
        
        # Set Polynomial Regression Order
        self._polyorder = polyorder

        # Polynomial Regression for Cumulative Consumption/Production
        # Fitting data to polynomial Regression (Get slopes)
        fit = np.polyfit(t, s, polyorder)

        # Get Polynomial curve for Cumulative Consumption/Production
        p = np.poly1d(fit)
        
        # Set plyfit
        self._polyfit = p    # use plotting


    def polyreg_cumulative(self):
        t = self._run_time_hour    # Run Time (hrs)

        # Polynomial curve for Cumulative Consumption/Production
        p = self._polyfit

        # Get Polynomial Fit Cumulative Consumption/Production corresponding x values
        name = self._cumulative.name
        self._polyreg_cumulative = pd.Series(data=p(t), name=f'Poly. Reg. {name}')


    def polyreg_sp_rate(self):
        t = self._run_time_hour     # Run Time (hrs)
        xv = self._xv               # Viable Cell Concentration (10e6 cells/mL)
        v = self._v_before_sampling # Culture Volume Before Sampling (mL)

        # Polynomial curve for Cumulative Consumption/Production
        p = self._polyfit

        dpdt = p.deriv() # first derivetive of polynomial fit
        y = dpdt(t)      # derivetive values corresponding to x

        # Calculate Specific Rate from Derivetive of Polynomial Regression on Cumularive Consumption/Production
        name = self._name.lower()
        title = f'Poly. Reg. Order: {self._polyorder} q{name} (mmol/109 cells/hr)'
        q = pd.Series(data=[np.nan] * len(self._sample_num),
                      name=title)

        # Calculate SP. rate
        for i in range(1, len(t)):
            # If has direct calculation of cumulative consumption/production
            if (self._direct_cumulative):
                #print(f'{self._name} use direct CUM for Poly. Reg.')
                q.iat[i] = y[i] / xv.iat[i]
            else:
                q.iat[i] = y[i] / (xv.iat[i] * v.iat[i]) * 1000

        # Polynomial Fit SP. rate
        self._polyreg_sp_rate = q

    def disp_polyreg(self):
        df = pd.concat([self._polyreg_cumulative,
                        self._polyreg_sp_rate],
                        axis=1)
        print('\n************ Post Process Data -Poly. Reg. ************')
        print(df)