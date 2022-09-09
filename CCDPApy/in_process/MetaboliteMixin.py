import pandas as pd
import numpy as np

na = np.nan

###########################################################################
# Metabolite Mixin Class
###########################################################################
class MetaboliteMixin:
    # Call Initialize Method
    def in_process(self, use_feed_conc=False, use_conc_after_feed=False):
        # Concentration Profiles to Calculate Cumulative Comsumption/Production
        self._use_feed_conc = use_feed_conc
        self._use_conc_after_feed = use_conc_after_feed

        # IF Measured Data has Cumulative Consumption/Production
        if (self._cumulative.any()):
            self._direct_cumulative = True
            self._cumulative_unit = '(mM)'
            # Calculate Concentration After Feeding
            self.conc_after_feeding()
            # Mid-point calculation of conc. and run time
            self.mid_calc_conc_runtime()
        else:
            self._cumulative_unit = '(mmol)'
            # IF Experiments measure the feed Concentrations
            if (self._use_feed_conc):
                # Calculate Concentration After Feeding
                self.conc_after_feeding()
                # Calculate Cumulative Consumption/Production with Feed Concentraion
                self.cumulative_cons_from_feed()
                # Mid-point calculation of conc. and run time
                self.mid_calc_conc_runtime()

            # IF Experiments measure the concentraions after feeding
            elif (self._use_conc_after_feed):
                # Calculate Cumulative Consumption/Production with Concentraion after Feeding
                self.cumulative_cons_from_conc_after_feed()
                # Mid-point calculation of conc. and run time
                self.mid_calc_conc_runtime()

            else:
                # Calculate Concentration After Feeding
                self.conc_after_feeding()
                # Calculate Cumulative Consumption/Production without Concentraion after Feeding
                self.cumulative_cons_without_feed()
                # Mid-point calculation of conc. and run time
                self.mid_calc_conc_runtime()


    # Calculate Concentration After Feeding
    def conc_after_feeding(self):
        idx = self._idx                     # Measurement Index
        s = self._conc_before_feed[idx]     # Substrate Concentration (mM)
        sf = self._feed_conc[idx]           # Substrate Feed Concentration (mM)
        f_media = self._feed_media_added[idx]     # Feed Flowrate (ml/hr)
        v = self._v_after_sampling[idx]     # Culture Volume After Sampling (ml)
        separate_f = self._feed_data     # Separate Feed DataFrame
        separate_f_added = self._feed_data.sum(axis=1)[idx]# Separate Feed Sum Added (E.g. glutamine, glucose, etc.)

        f = f_media
        if self._name in self._feed_list:
            f = separate_f[f'{self._name.upper()} ADDED (mL)'][idx]

        # Concentration After Feeding
        self._conc_after_feed = ((s*v + sf*f) / (v + f_media + separate_f_added)).rename(f'{self._name} CONC. AFTER FEED (mM)')


    # Calculate Cumulative Consumption/Production With Feed Concentration
    def cumulative_cons_from_feed(self, initial_conc=0):
        idx = self._idx                     # Measurement Index
        s = self._conc_before_feed[idx]     # Substrate Concentration (mM)
        sf = self._feed_conc[idx]           # Substrate Feed Concentration (mM)
        f = self._feed_media_added[idx]     # Feed Flowrate (ml/hr)
        v1 = self._v_before_sampling[idx]   # Culture Volume Before Sampling (ml)
        v2 = self._v_after_sampling[idx]    # Culture Volume After Sampling (ml)
        separate_feed = self._feed_data        # Separate Feed data
        separate_feed_list = self._feed_list    # Separate Feed list

        # Check Species name and separate feed added
        if self._name.upper() in separate_feed_list:
            f = separate_feed[f'{self._name.upper()} ADDED (mL)'][idx]

        # Initialize
        se = pd.Series(data=[na] * len(self._sample_num),
                       name=f'CUM {self._name} {self._cumulative_unit}')
        se.iat[0] = initial_conc

        # Consumed Substrate = sf*f + s[i-1]*v[i-1] - s[i]*v[i]
        for i in range(1, len(idx)):
            si = (sf.iat[i] * f.iat[i-1] - s.iat[i] * v1[i] + s.iat[i-1] * v2[i-1]) / 1000
            se.iat[idx[i]] = se.iat[idx[i-1]] + si

        # The Case that Species is Produced but Not Consumed.
        if (self._production == True):
            se *= -1

        # Cumulative Consumption/Production
        self._cumulative = se.astype('float')


    # Calculate Cumulative Consumption/Production With Concentration After Feeding
    def cumulative_cons_from_conc_after_feed(self, initial_conc=0.0):
        idx = self._idx                     # Measurement Index
        s1 = self._conc_before_feed[idx]    # Substrate Concentration Before Feeding (mM)
        s2 = self._conc_after_feed[idx]     # Substrate Concentration After Feeding (mM)
        v = self._v_before_sampling[idx]    # Culture Volume After Feeding (ml)

        # Initialize
        s = pd.Series([na] * len(self._sample_num),
                      name=f'CUM {self._name} {self._cumulative_unit}')
        s.iat[0] = initial_conc

        for i in range(1, len(idx)):
            si = (s2.iat[i-1] * v.iat[i] - s1.iat[i] * v.iat[i]) / 1000
            s.iat[idx[i]] = s.iat[idx[i-1]] + si

        # The Case that Species is Produced but Not Consumed.
        if (self._production == True):
            s *= -1

        # Cumulative Consumption/Production
        self._cumulative = s.astype('float')


    # Calculate Cumulative Consumption/Production Without Concentration After Feeding
    def cumulative_cons_without_feed(self, initial_conc = 0.0):
        idx = self._idx                     # Measurement Index
        s = self._conc_before_feed[idx]     # Substrate Concentration (mM)
        v1 = self._v_before_sampling[idx]   # Culture Volume Before Sampling (ml)
        v2 = self._v_after_sampling[idx]    # Culture Volume After Sampling (ml)

        # Initialize
        se = pd.Series(data=[na] * len(self._sample_num),
                        name=f'CUM {self._name} {self._cumulative_unit}')
        se.iat[0] = initial_conc

        # Consumed Substrate = sf*f + s[i-1]*v[i-1] - s[i]*v[i]
        for i in range(1, len(idx)):
            si = (- s.iat[i] * v1.iat[i] + s.iat[i-1] * v2.iat[i-1]) / 1000
            se.iat[idx[i]] = se.iat[idx[i-1]] + si

        # The Case that Species is Produced but Not Consumed.
        if (self._production == True):
            se *= -1

        # Cumulative Consumption/Production
        self._cumulative = se.astype('float')


    # Mid-point calculation of conc. and run time
    def mid_calc_conc_runtime(self):
        idx = self._idx                 # Measurement index
        c1 = self._conc_after_feed[idx]      # c1: conc after feeding at t
        c2 = self._conc_before_feed[idx]     # c2: measured conc at t + 1
        t = self._run_time_hour[idx]         # run time hour

        c_mid = pd.Series(data=[na] * (len(idx)-1),
                            name=f'{self._name} CONC. MID. (mM)', dtype='float')
        t_mid = pd.Series(data=[na] * (len(idx)-1),
                            name='RUN TIME MID (HOURS)', dtype='float')

        for i in range(len(idx)-1):
            c_mid.iat[i] = (c1.iat[i]+c2.iat[i+1])/2
            t_mid.iat[i] = (t.iat[i]+t.iat[i+1])/2

        self._conc_mid = c_mid
        self._run_time_mid = t_mid


    # Getters
    # Get Concentration
    def get_conc_before_feed(self):
        return self._conc_before_feed

    # Get Concentration After Feeding
    def get_conc_after_feed(self):
        return self._conc_after_feed

    # Get Concentration After Feeding
    def get_feed_conc(self):
        return self._feed_conc

    # Get Concentration Mid    
    def get_conc_mid(self):
        return self._conc_mid

    # Display
    def disp_inpro_data(self):
        if self._in_process_flag:
            data = pd.concat([self._run_time_hour, self._cumulative],
                            axis=1)
            print(data)
        
