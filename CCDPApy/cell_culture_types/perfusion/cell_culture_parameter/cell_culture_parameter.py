class PerfusionParameters:
    '''Store key parameters for a fed-batch cell culture data processing.'''
    def __init__(self, 
                 cell_line_name:str,
                 recycling_factor=0.25, 
                 concentration_factor=3,
                 regression_method=None, 
                 polynomial_degreee=None) -> None:
        '''
        Attributes
        ----------
            
        '''
        self._cell_line_name = cell_line_name
        self._recycling_factor = recycling_factor
        self._concentration_factor = concentration_factor

        if not isinstance(regression_method, list):
            regression_method = [regression_method]

        if 'polynomial' in regression_method:
            self._polynomial = True
        else:
            self._polynomial = False

    @property
    def cell_line_name(self):
        return self._cell_line_name
    
    @cell_line_name.setter
    def cell_line_name(self, cell_line_name):
        self._cell_line_name = cell_line_name

    @property
    def recycling_factor(self):
        return self._recycling_factor

    @recycling_factor.setter
    def recycling_factor(self, factor):
        self._recycling_factor = factor

    @property
    def concentration_factor(self):
        return self._concentration_factor

    @concentration_factor.setter
    def concentration_factor(self, factor):
        self._concentration_factor = factor

    @property
    def polynomial(self):
        return self._polynomial
    
    @polynomial.setter
    def polynomial(self, polynomial):
        self._polynomial = polynomial

    def __repr__(self) -> str:
        return('\n'.join([f'Cell Line: {self._cell_line_name}',
                         f'Recycling factor: {self._recycling_factor}',
                         f'Concentration factor: {self._concentration_factor}',
                         f'Regression Methods',
                         f'     Polynomial: {self._polynomial}',
                         ]))