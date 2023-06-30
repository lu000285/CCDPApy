import pandas as pd
import numpy as np

from CCDPApy.in_process.GetterMixin import GetterMixin

###########################################################################
# Metabolite Mixin Class
###########################################################################
class MetaboliteMixin(GetterMixin):
    '''
    '''
    # Call Initialize Method
    def in_process(self, feed_concentration, concentration_after_feed):
        ''' Calculate In-Proccess for metabolites.
        '''
        self._feed_concentration_flag = feed_concentration
        self._concentration_after_feed_flag = concentration_after_feed

        # If measured data already has the calculated cumulative consumption/production
        if (self._measured_cumulative_flag):
            self._cumulative = self._measured_cum_c
            self._cumulative_unit = '(mM)'
            # Calculate Concentration After Feeding
            self.conc_after_feeding()

        else:
            self._cumulative_unit = '(mmol)'
            # IF Experiments measure the feed Concentrations
            if (feed_concentration):
                # Calculate Concentration After Feeding
                self.conc_after_feeding()
                # Calculate Cumulative Consumption/Production with Feed Concentraion
                s = self.cumulative_cons_from_feed()

            # IF Experiments measure the concentraions after feeding
            elif (concentration_after_feed):
                # Calculate Cumulative Consumption/Production with Concentraion after Feeding
                s = self.cumulative_cons_from_conc_after_feed()

            else:
                # Calculate Concentration After Feeding
                self.conc_after_feeding()
                s = self.cumulative_cons_without_feed()

            # The case that species is produced. (cumulative production)
            if (self._production == True):
                s *= -1
            
            # Cumulative Consumption/Production
            name = f'cum{self._name.capitalize()}_{self._cumulative_unit}'
            self._cumulative = pd.Series(data=s, name=name, dtype='float')

        # Specific rate
        rate = self.specific_rate()
        name = f'q{self._name.capitalize()}_(mmol/10^9_cell/hr)'
        self._sp_rate = pd.Series(data=rate, name=name, dtype='float')


    def conc_after_feeding(self):
        ''' Calculate concentration after feeding.
        '''
        idx = self._idx                                                 # Measurement Index
        s = self._c_before_feed.values[idx]                             # Substrate Concentration (mM)
        sf = self._feed_c.values[idx]                                   # Substrate Feed Concentration (mM)
        f_media = self._feed_media_added.values[idx]                    # Feed Flowrate (ml/hr)
        v = self._v_after_sampling.values[idx]                          # Culture Volume After Sampling (ml)
        separate_f = self._feed_data                                    # Separate Feed DataFrame
        separate_f_added = separate_f.fillna(0).sum(axis=1).values[idx] # Separate Feed Sum Added (E.g. glutamine, glucose, etc.)

        f = f_media
        # Check if species has the separate feed
        if self._name in self._feed_list:
            key = f'{self._name.upper()}_ADDED_(mL)'
            f = separate_f[key].values[idx]

        # Concentration After Feeding
        c = ((s*v + sf*f) / (v + f_media + separate_f_added))
        self._c_after_feed = pd.Series(data=c, name=f'{self._name.lower()}_(mM)')

    def cumulative_cons_from_feed(self):
        ''' Calculate ccumulative consumption using the feed concentration.
        '''
        idx = self._idx                     # Measurement Index
        s = self._c_before_feed.values[idx]     # Substrate Concentration (mM)
        sf = self._feed_c.values[idx]           # Substrate Feed Concentration (mM)
        f = self._feed_media_added.values[idx]     # Feed Flowrate (ml/hr)
        v1 = self._v_before_sampling.values[idx]   # Culture Volume Before Sampling (ml)
        v2 = self._v_after_sampling.values[idx]    # Culture Volume After Sampling (ml)
        separate_feed = self._feed_data        # Separate Feed data
        separate_feed_list = self._feed_list    # Separate Feed list

        # Check if species has the separate feed
        if self._name.upper() in separate_feed_list:
            key = f'{self._name.upper()}_ADDED_(mL)'
            f = separate_feed[key].values[idx]

        # Initialize
        c = np.zeros(self._sample_num)
        c.fill(np.nan)
        c[0] = 0

        # Consumed Substrate = sf*f + s[i-1]*v[i-1] - s[i]*v[i]
        for i in range(1, len(idx)):
            c_i = (sf[i] * f[i-1] - s[i] * v1[i] + s[i-1] * v2[i-1]) / 1000
            c[idx[i]] = c[idx[i-1]] + c_i
        return c

    
    def cumulative_cons_from_conc_after_feed(self):
        ''' Calculate cumulative consumption using the concentration after feeding
        '''
        idx = self._idx                     # Measurement Index
        s1 = self._c_before_feed.values[idx]    # Substrate Concentration Before Feeding (mM)
        s2 = self._c_after_feed.values[idx]     # Substrate Concentration After Feeding (mM)
        v = self._v_before_sampling.values[idx]    # Culture Volume After Feeding (ml)

        # Initialize
        c = np.zeros(self._sample_num)
        c.fill(np.nan)
        c[0] = 0

        for i in range(1, len(idx)):
            c_i = (s2[i-1] * v[i] - s1[i] * v[i]) / 1000
            c[idx[i]] = c[idx[i-1]] + c_i
        return c


    def cumulative_cons_without_feed(self):
        ''' Calculate cumulative consumption without the concentration after feeding.
        '''
        idx = self._idx                     # Measurement Index
        s = self._c_before_feed.values[idx]     # Substrate Concentration (mM)
        v1 = self._v_before_sampling.values[idx]   # Culture Volume Before Sampling (ml)
        v2 = self._v_after_sampling.values[idx]    # Culture Volume After Sampling (ml)

        # Initialize
        c = np.zeros(self._sample_num)
        c.fill(np.nan)
        c[0] = 0

        # Consumed Substrate = sf*f + s[i-1]*v[i-1] - s[i]*v[i]
        for i in range(1, len(idx)):
            c_i = (- s[i] * v1[i] + s[i-1] * v2[i-1]) / 1000
            c[idx[i]] = c[idx[i-1]] + c_i
        return c
    
    # Calculate Specific Rate
    def specific_rate(self):
        ''' Calculate specific rate.
        '''
        idx = self._idx                     # Get Measurement Index
        s = self._cumulative.values[idx]           # Cumulative Concentration (mM)
        t = self._run_time_hour.values[idx]        # Run Time (hrs)
        v1 = self._v_before_sampling.values[idx]   # Culture Volume Before Sampling (mL)
        v2 = self._v_after_sampling.values[idx]    # Culture Volume Before sampling (mL)
        xv = self._xv.values[idx]                  # Viable Cell Concentration (10e6 cells/mL)
        
        # Initialize
        r = np.zeros(self._sample_num)
        r.fill(np.nan)
        
        # If there is the measurements of the cumulative concentration.
        if (self._measured_cumulative_flag):
            for i in range(1, len(idx)):                
                c_diff = (s[i] - s[i-1])            # concentration difference
                xv_avg = 0.5 * (xv[i] + xv[i-1])    # average vcc
                r[idx[i]] = c_diff / (t[i] - t[i-1]) / xv_avg

        else:
            for i in range(1, len(idx)):                
                c_diff = (s[i] - s[i-1]) * 1000 # concentration difference
                # With the concentration after feed
                if (self._concentration_after_feed_flag and not self._concentration_after_feed_flag):
                    xv_avg = 0.5 * (xv[i] * v1[i] + xv[i-1] * v1[i]) # Average
                # With the feed concentration OR without both
                else:
                    xv_avg = 0.5 * (xv[i] * v1[i] + xv[i-1] * v2[i-1]) # Average
                r[idx[i]] = c_diff / (t[i]-t[i-1]) / xv_avg
        return r

    # Getters
    # Get Concentration
    def get_concentration_before_feed(self):
        return self._c_before_feed

    # Get Concentration After Feeding
    def get_concentration_after_feed(self):
        return self._c_after_feed

    # Get Concentration After Feeding
    def get_feed_concentration(self):
        return self._feed_c

    @property
    def get_in_process_data(self):
        '''Return in-process data.
        '''
        if self._in_process_flag:
            c_before = self._c_before_feed
            c_after_feed = self._c_after_feed
            feed_c =  self._feed_c
            cc = self._cumulative
            rate = self._sp_rate

            data = [c_before, c_after_feed, feed_c,
                    cc, rate]
            profile = ['concentration', 'concentration', 'concentration',
                       'cumulative', 'spRate']
            kind = ['beforeFeed', 'afterFeed', 'feed',
                    'cumulative', 'rate']
            method = [np.nan, np.nan, np.nan,
                      'twoPoint', 'twoPoint']
            return self.get_profile_data(data_list=data,
                                         profile_list=profile,
                                         kind_list=kind, 
                                         method_list=method)

    # Display
    def disp_in_process(self):
        if self._in_process_flag:
            data = pd.concat([self._run_time_hour, self._cumulative], axis=1)
            print(data)
        
