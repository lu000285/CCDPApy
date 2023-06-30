import pandas as pd
import numpy as np

from CCDPApy.in_process.GetterMixin import GetterMixin

###########################################################################
# Product(IgG) Mixin Class
###########################################################################
class ProductMixin(GetterMixin):
    # Call Calculation Function
    def in_process(self):
        cc = self.cumulative_concentration
        self._cumulative = pd.Series(data=cc, name='cumProduct_(mg)')

        rate = self.sp_rate
        self._sp_rate = pd.Series(data=rate, name='qProduct_(mg/10^9_cell/hr)')
        
    @property
    def cumulative_concentration(self):
        ''' Calculate cumulative Product/IgG produced.
        IgG produced = xv(t) * v(t) - xv(t-1) * v(t-1)
        '''
        idx = self._idx
        igg = self._conc.values[idx]            # IgG concentration (10e6 cells/ml)
        v1 = self._v_before_sampling.values[idx]    # Culture Volume Bfore sampling (ml)
        v2 = self._v_after_sampling.values[idx]     # Culture Volume After feeding (ml)

        # Initialize
        c = np.zeros(self._sample_num)
        c.fill(np.nan)
        c[0] = 0

        for i in range(1, len(idx)):
            c_i = (igg[i] * v1[i] - igg[i-1] * v2[i-1]) / 1000
            c[idx[i]] = c[idx[i-1]] + c_i
        return c

    @property
    def sp_rate(self):
        '''Calculate specific rate of Product/IgG.
        '''
        idx = self._idx # Measurement indices
        s = self._cumulative.values[idx]           # Substrate Concentration (mM)
        t = self._run_time_hour.values[idx]        # Run Time (hrs)
        v1 = self._v_before_sampling.values[idx]   # Culture Volume Before Sampling (mL)
        v2 = self._v_after_sampling.values[idx]    # Culture Volume Before sampling (mL)
        xv = self._xv.values[idx]                  # Viable Cell Concentration (10e6 cells/mL)

        r = np.zeros(self._sample_num)
        r.fill(np.nan)

        for i in range(1, len(idx)):
            x = (s[i] - s[i-1]) * 1000
            y = xv[i] * v1[i] + xv[i-1] * v2[i-1]

            r[idx[i]] = x / (y * 0.5 * (t[i] - t[i-1]))
        return r
    
    @property
    def get_in_process_data(self):
        """
        Get In-Process DataFrame.
        """
        if self._in_process_flag:
            data = [self._conc, self._cumulative, self._sp_rate]
            profile = ['concentration', 'cumulative', 'spRate']
            kind = [np.nan, np.nan, np.nan]
            method = [np.nan, 'twoPoint', 'twoPoint']
            return self.get_profile_data(data_list=data,
                                         profile_list=profile,
                                         kind_list=kind, 
                                         method_list=method)
    
    @property
    def disp_in_process(self):
        ''''''
        if self._in_process_flag:
            data = self.get_in_process
            print('\n************ IgG In Process Data ************')
            print(data)