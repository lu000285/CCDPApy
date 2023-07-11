import pandas as pd

class GetterMixin:
    '''
    '''
    @property
    def cell_line(self):
        '''Return the cell line name.
        '''
        return self._cell_line
    
    @property
    def run_id(self):
        '''Return the run ID.
        '''
        return self._run_id
    
    @property
    def experimenter(self):
        '''Returns the name of the experimenter.
        '''
        return self._experimenter
    
    def get_species(self, name):
        '''Return the species object.
        '''
        return self._species[name.lower()]
    
    @property
    def concentration(self):
        '''
        '''
        species = self._species.copy()
        cell = species.pop('cell')
        df_list = []
        for name, s in species.items():
            temp = s.concentration
            temp['species'] = name
            df_list.append(temp)
        df = pd.concat(df_list, axis=0).reset_index(drop=True)
        col = df.columns
        df['cellLine'] = self.cell_line
        df['runID'] = self.run_id
        new_col = ['cellLine', 'runID'] + list(col)
        df = df[new_col]
        return df
    