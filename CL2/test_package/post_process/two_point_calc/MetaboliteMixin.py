import pandas as pd
import numpy as np
from numpy import diff

###########################################################################
class MetaboliteMixinTwoPt:
    # Calculate Specific Rate
    def sp_rate_twopt(self):
        # Get Measurement Index
        idx = self._idx
        s = self._cumulative[idx]           # Cumulative Concentration (mM)
        t = self._run_time_hour[idx]        # Run Time (hrs)
        v1 = self._v_before_sampling[idx]   # Culture Volume Before Sampling (mL)
        v2 = self._v_after_sampling[idx]    # Culture Volume Before sampling (mL)
        xv = self._xv[idx]                  # Viable Cell Concentration (10e6 cells/mL)
        
        # Initialize
        rate = pd.Series(data=[pd.NA] * len(self._sample_num),
                         name='q'+self._name+' (mmol/109 cell/hr)')
        
        # IF Have Direct Mesurement of Cumulative
        if (self._direct_cumulative):
            dsdt = diff(s)/diff(t)
            dsdt = np.insert(dsdt, 0, np.nan)
            rate = dsdt / xv

        else:
            for i in range(1, len(idx)):                
                x = (s.iat[i] - s.iat[i-1]) * 1000

                # With Concentration after Feed
                if (self._use_conc_after_feed):
                    y = xv.iat[i]*v1.iat[i] + xv.iat[i-1]*v1.iat[i]
                    
                # With Feed Concentration OR Without Both
                else:
                    y = xv.iat[i]*v1.iat[i] + xv.iat[i-1]*v2.iat[i-1]

                rate.iat[idx[i]] = x / (y*0.5*(t.iat[i]-t.iat[i-1]))

        # SP. Rate
        self._sp_rate = rate

    ###########################################################################