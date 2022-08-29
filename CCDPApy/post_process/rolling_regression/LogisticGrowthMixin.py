import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

# Logistic Growth Mixin Class
class LogisticGrowthMixin:

    def LogisticGrowthFit(self):
        tcc = self._xt[0:11]
        t = self._run_time_hour[0:11]
        N0 = tcc[0]
        popt, pcov = curve_fit(lambda t,K,r:LogisticGrowth_fun(t,N0,K,r), t, tcc, p0=[24,0.05])
        return popt

    def midcalc_growth_rate_calc(self):
        df = pd.DataFrame()
        t = self._run_time_mid
        popt = self.LogisticGrowthFit()
        N0 = self._xt[0]
        mu = pd.Series([np.nan] * len(t))
        mu = (t.apply(lambda x:sp_rate_calc(x,N0,*popt))).rename('mu')
        df['Sp. Growth (1/hr)'] = mu
        df['mu_max'] = pd.Series([popt[1]] * len(t))
        df['N0'] = pd.Series([N0] * len(t))
        df['K_mu'] = pd.Series([popt[0]] * len(t))
        # print(f'N0: {N0}')
        # print(f'popt: {popt}')
        # print('mu:')
        # print(mu)
        return df

# Logistic Growth Function
def LogisticGrowth_fun(t,N0,K,r):
    return K*N0/(N0+(K-N0)*np.exp(-r*t))

# Specific rate calculation: mu = dx_t/dt/x_t
def sp_rate_calc(t,N0,K,r):
    return (K-N0)*r*np.exp(-r*t)/(N0+(K-N0)*np.exp(-r*t))

