import pandas as pd

###########################################################################
# PreProcess Mixin Class
###########################################################################
class PreProcessMixn:
    '''
    '''
    # Calculate Run Time (day, hour)
    def run_time(self):

        try: # If TIME is Timestamp('2019-08-23 13:11:00') 
            self._run_time_hour = (self._time - self._time.iat[0]).apply(lambda x: x.total_seconds() / 3600)
        except:
            # Change DATE and TIME to String
            day_str = self._date.dt.strftime('%x ')
            time_str = self._time.apply(lambda x: x.strftime('%X'))
            # Combine DATE and TIME Strings, then Change the DataType to datetime
            dt = pd.to_datetime(day_str + time_str)
            # Calculate Run Time (Hour)
            self._run_time_hour = (dt - dt.iat[0]).apply(lambda x: x.total_seconds() / 3600)

        # Calculate Run Time (Day)
        self._run_time_day = self._run_time_hour / 24

        # Rename
        self._run_time_day = self._run_time_day.rename('RUN TIME (DAYS)')
        self._run_time_hour = self._run_time_hour.rename('RUN TIME (HOURS)')


    # Calculate Culture Volume Before/After Sampling and After Feeding
    def culture_volume(self):
        n = len(self._sample_num) # Number of Samples
        self._v_before_sampling.iat[0] = self._initial_volume   # Initial Volume

        if (len(self._glutamine_feed_added) != n):
            data = self._glutamine_feed_added.iat[0]
            self._glutamine_feed_added = pd.Series(data=[data] * n)
        if (len(self._glucose_feed_added) != n):
            data = self._glucose_feed_added.iat[0]
            self._glucose_feed_added = pd.Series(data=[data] * n)

        for i in range(n):
            # Volume After Sampling
            self._v_after_sampling.iat[i] = self._v_before_sampling.iat[i] - self._sample_volume.iat[i]
            
            # Added Supplements Volume
            supplements_added = self._base_added.iat[i] + self._feed_media_added.iat[i] + self._glucose_feed_added.iat[i] + self._glutamine_feed_added.iat[i]
            
            # Volume After Feeding
            self._v_after_feeding.iat[i] = self._v_after_sampling.iat[i] + supplements_added
            
            # Volume Before Sampling
            if (i < n-1):
                self._v_before_sampling.iat[i+1] = self._v_after_feeding.iat[i]

    # Mid-point calculation of conc. and run time
    def mid_calc_runtime(self):
        t = self._run_time_hour
        t_mid = pd.Series(data=[pd.NA] * (len(t)-1),
                            name='RUN TIME MID (HOURS)')

        for i in range(len(t_mid)):
            t_mid.iat[i] = (t.iat[i] + t.iat[i+1])/2

        self._run_time_mid = t_mid

    # Get Run Time Mid
    def get_time_mid(self):
        return self._run_time_mid

###########################################################################

