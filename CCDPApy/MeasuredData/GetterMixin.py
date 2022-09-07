import pandas as pd

class GetterMixin:
    '''
    Mixin class for MeasuredData Class.

    Methods
    -------
        get_pre_data : 
            Return pre process data.
    '''
    def get_pre_data(self):
        """Return pre process data.
        """
        self.pre_data = pd.concat([self.run_time_day,
                                    self.run_time_hour,
                                    self.v_before_sampling,
                                    self.v_after_sampling,
                                    # self._v_after_feeding,
                                    # self._feed_status,
                                    ], axis=1)
        return self.pre_data