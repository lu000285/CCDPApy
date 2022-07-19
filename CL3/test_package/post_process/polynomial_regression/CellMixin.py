import pandas as pd
from .PolyRegMixin import PolyRegMixin

# Cell Poly. Reg. Mixin Class
class CellMixinPolyReg(PolyRegMixin):
    
    def polyreg(self, polyorder=3):
        super().polyreg_fit(polyorder=polyorder)
        super().polyreg_cumulative()

    def disp_polyreg(self):
        df = pd.concat([self._polyreg_cumulative],
                        axis=1)
        print('\n************ Post Process Data -Poly. Reg. ************')
        print(df)
