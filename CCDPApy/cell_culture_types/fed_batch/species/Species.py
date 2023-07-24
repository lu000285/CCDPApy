from CCDPApy.Constants import SPECIES_ABBR, RUN_TIME_DAY_COLUMN, RUN_TIME_HOUR_COLUMN

class Species():
    '''
    Species class.

    Attribute
    ---------
    '''
    # Constructor
    def __init__(self, name, run_time_df, 
                 volume_before_sampling, volume_after_sampling, 
                 feed_media_added, viable_cell_conc) -> None:
        '''
        Parameters
        ---------
        '''
        name = name.capitalize() if name != 'IgG' else 'IgG'
        abbr = SPECIES_ABBR[name] if SPECIES_ABBR.get(name) else name.upper()

        # Store data
        self._name = name
        self._abbr = abbr
        self._run_time = run_time_df
        self._run_time_day = run_time_df[RUN_TIME_DAY_COLUMN].values
        self._run_time_hour = run_time_df[RUN_TIME_HOUR_COLUMN].values
        self._samples = self._run_time_hour.size
        self._volume_before_sampling = volume_before_sampling
        self._volume_after_sampling = volume_after_sampling
        self._feed_media_added = feed_media_added
        self._viable_cell_conc = viable_cell_conc

    @property
    def name(self):
        return self._name
    
    @property
    def abbr(self):
        return self._abbr
    
    @property
    def run_time_day(self):
        return self._run_time_day
    
    @property
    def run_time(self):
        return self._run_time
    
    @property
    def run_time_hour(self):
        return self._run_time_hour
    
    @property
    def samples(self):
        return self._samples
    
    @property
    def volume_before_sampling(self):
        return self._volume_before_sampling
    
    @property
    def volume_after_sampling(self):
        return self._volume_after_sampling
    
    @property
    def feed_media_added(self):
        return self._feed_media_added
    
    @property
    def viable_cell_conc(self):
        return self._viable_cell_conc
    
    