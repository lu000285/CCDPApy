from .Species import Species
from ...in_process.Perfusion.MetaboliteMixin import MetaboliteMixin as InProcess
from CCDPApy.post_process.Perfusion.polynomial.MetaboliteMixin import MetaboliteMixin as Polynomial
class Metabolite(Species, InProcess, Polynomial):
    '''
    '''
    def __init__(self, name, run_time, culture_volume, flow_rate, conc, feed_conc, viable_cell_conc) -> None:
        '''
        '''
        super().__init__(name, run_time, culture_volume, flow_rate, viable_cell_conc)

        # Store variables
        self._conc = conc
        self._feed_conc = feed_conc
    
    @property
    def get_conc(self):
        return self._conc
    
    @property
    def get_feed_conc(self):
        return self._feed_conc
    