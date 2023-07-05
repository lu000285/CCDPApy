class GetterMixin:
    '''
    '''
    @property
    def get_cell_line(self):
        '''Return the cell line name.
        '''
        return self._cell_line
    @property
    def get_run_id(self):
        '''Return the run ID.
        '''
        return self._run_id
    @property
    def get_experimenter(self):
        '''Returns the name of the experimenter.
        '''
        return self._experimenter
    
    def get_species(self, name):
        '''Return the species object.
        '''
        return self._species[name.lower()]
    