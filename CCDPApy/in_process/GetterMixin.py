import pandas as pd

class GetterMixin:
    '''Getter Mixin Class for In-Process
    '''
    @property
    def get_cumulative(self):
        """
        Get cumulative consumption/production.
        """
        return self._cumulative

    @property
    def get_cumulative_unit(self):
        """
        Get cumulative consumption/production unit.
        (mmol) or (mM).
        """
        return self._cumulative_unit
    
    @property
    def get_in_process(self):
        """
        Get In-Process DataFrame.
        """
        if self._in_process_flag:
            t = self._run_time_hour
            cc = self._cumulative
            spr = self._sp_rate
        return pd.concat([t, cc, spr], axis=1)
