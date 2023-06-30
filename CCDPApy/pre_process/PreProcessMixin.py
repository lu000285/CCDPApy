import numpy as np
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
        df = self.param_df

        if 'date' in df and 'time' in df:
            # Check if date is datetime object
            if pd.api.types.is_datetime64_any_dtype(df['date']):
                df['date'] = df['date'].apply(lambda x: x.date())
            # Check if time is datetime object
            if pd.api.types.is_datetime64_any_dtype(df['time']):
                df['time'] = df['time'].apply(lambda x: x.time())

            # Create the datetime column from date and time
            t = pd.to_datetime(df['date'].astype(str) + ' ' + df['time'].astype(str))
            run_time_hour = (t - t.at[0]).apply(lambda t: t.total_seconds() / 3600.0)
            run_time_day = (run_time_hour / 24.0)
            insert_idx = df.columns.get_loc('time') + 1
            df.insert(insert_idx, column='run_time_(hrs)', value=run_time_hour)
            df.insert(insert_idx, column='run_time_(days)', value=run_time_day)


    def culture_volume(self):
        '''
        Calculate culture volume before/after sampling and after feeding from Meaured Data.
        '''
        df = self.param_df
        samples = df['samples'].size
        v_before_sampling = np.zeros(samples)
        v_after_feeding = np.zeros(samples)
        v_after_sampling = df.pop('volume_after_sampling_(mL)')

        if v_after_sampling.isna().all():
            v_after_sampling = np.zeros(samples)
            sample_volume = df['sample_volume_(mL)'].fillna(0).values
            v_before_sampling[0] = self._initial_volume

            # Added Supplements Volume; base + feed media + feed
            base_added = df['base_added_(mL)'].fillna(0).values
            feed_media_added = df['feed_media_added_(mL)'].fillna(0).values
            feed_sum = self.feed_data.fillna(0).sum(axis=1).values
            supplements_added = base_added + feed_media_added + feed_sum

            for i in range(samples):
                # Volume After Sampling
                v_after_sampling[i] = v_before_sampling[i] - sample_volume[i]
                            
                # Volume After Feeding
                v_after_feeding[i] = v_after_sampling[i] + supplements_added[i]
                
                # Volume Before Sampling
                if (i < samples-1):
                    v_before_sampling[i+1] = v_after_feeding[i]

        else:
            x = v_after_sampling.values
            v_before_sampling = x
            v_after_feeding = x

        df['volume_before_sampling_(mL)'] = v_before_sampling
        df['volume_after_feeding_(mL)'] = v_after_feeding
        df['volume_after_sampling_(mL)'] = v_after_sampling
# End PreProcessMixin

