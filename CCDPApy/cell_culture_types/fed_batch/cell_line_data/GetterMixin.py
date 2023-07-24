class GetterMixin:
    def get_conc_before_feed(self):
        '''get measured data for concentration before feeding.'''
        return self._conc_before_feed_data
    
    def get_conc_after_feed(self):
        '''get measured data for concentration before feeding.'''
        return self._conc_after_feed_data
    
    def get_measured_cumulative_conc(self):
        '''get measured data for calculated cumulative concentration.'''
        return self._measured_cumulative_conc_data

    def get_feed_conc(self):
        '''get feed concentration data.'''
        return self._feed_data

    def get_separate_feed_conc(self):
        '''get separate feed concentration data.'''
        return self._separate_feed_data
    
    def get_polynomial_degree(self):
        '''get polynomial degreee data.'''
        return self._polynomial_degree_data