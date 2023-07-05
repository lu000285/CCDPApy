class PolynomialMixin:
    '''
    '''
    def polynomial(self, deg=3):
        '''
        '''
        species = self._species

        # Get Cell
        cell = species.pop('cell')

        # Metabolite
        for s in species.values():
            s.polynomial(deg=deg)

        # Update
        species.update({'cell': cell})
    