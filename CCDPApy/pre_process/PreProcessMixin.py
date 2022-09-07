import pandas as pd

###########################################################################
# PreProcess Mixin Class
###########################################################################
class PreProcessMixn:
    '''
    Mixin class for MeasuredData class to execute pre-process.
    Calculate run time (day, hour) from meaured data.
    Calculate culture volume before/after sampling and after feeding from meaured data.

    Methods
    -------
        run_time : class method
            Calculate run time (day, hour) from Meaured Data.
        culture_volume : class method
            Calculate culture volume before/after sampling and after feeding from Meaured Data.
    '''

    def run_time(self):
        '''
        Calculate run time (day, hour) from Meaured Data.
        '''
        if (not self.run_time_hour.any() and not self.run_time_day.any()):

            try: # If TIME is Timestamp('2019-08-23 13:11:00') 
                self.run_time_hour = (self.time - self.time.iat[0]).apply(lambda x: x.total_seconds() / 3600)
            except:
                # Change DATE and TIME to String
                day_str = self.date.dt.strftime('%x ')
                time_str = self.time.apply(lambda x: x.strftime('%X'))
                # Combine DATE and TIME Strings, then Change the DataType to datetime
                dt = pd.to_datetime(day_str + time_str)
                # Calculate Run Time (Hour)
                self.run_time_hour = (dt - dt.iat[0]).apply(lambda x: x.total_seconds() / 3600)

            # Calculate Run Time (Day)
            self.run_time_day = self.run_time_hour / 24

            # Rename
            self.run_time_day = self.run_time_day.rename('RUN TIME (DAYS)')
            self.run_time_hour = self.run_time_hour.rename('RUN TIME (HOURS)')


    def culture_volume(self):
        '''
        Calculate culture volume before/after sampling and after feeding from Meaured Data.
        '''
        n = len(self.sample_num) # Number of Samples
        # Initial Volume
        self.v_before_sampling.iat[0] = self.initial_v

        # Added Supplements Volume
        # base + feed media + feed 
        supplements_added = self.base_added + self.feed_media_added + self.feed_data.sum(axis=1)

        for i in range(n):
            # Volume After Sampling
            self.v_after_sampling.iat[i] = self.v_before_sampling.iat[i] - self.sample_volume.iat[i]
                        
            # Volume After Feeding
            self.v_after_feeding.iat[i] = self.v_after_sampling.iat[i] + supplements_added.iat[i]
            
            # Volume Before Sampling
            if (i < n-1):
                self.v_before_sampling.iat[i+1] = self.v_after_feeding.iat[i]

# End PreProcessMixin

