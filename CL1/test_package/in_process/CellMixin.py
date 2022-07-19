import pandas as pd

###########################################################################
# Cell Mixin
###########################################################################
class CellMixin:

    # Call methods
    def in_process(self):
        self.integral_viable_cell()
        self.cumulative_cells_prod()

    # Calculate Integral of Viable Cell
    def integral_viable_cell(self, initial_conc=0):
        xv = self._xv           # Viable Cell Conc
        t = self._run_time_hour # Run Time (hours)

        # Initialize
        s = pd.Series(data=[initial_conc] * len(t),
                      name='INTEGRAL OF VIABLE CELL CONC.\nIVCC (x106 cells hr/mL)')

        for i in range(1, len(t)):
            s.iat[i] = s.iat[i-1] + (xv.iat[i] + xv.iat[i-1]) / 2 * (t.iat[i] - t.iat[i-1])

        # Integral Of Viable Cell
        self._ixv = s

    # Calculate Cumulative Cell Produced
    def cumulative_cells_prod(self, initial_conc=0):
        # Cells produced = xv(i) * v(i) - xv(i-1) * v(i-1)
        xv = self._xv                   # vialbe cell concentration (10e6 cells/ml)
        v1 = self._v_before_sampling    # culture volume before sampling (ml)
        v2 = self._v_after_sampling     # culture volume after feeding (ml)

        # Initialize
        s = pd.Series(data=[initial_conc] * len(xv),
                      name='CUM CELLS PROD. (x106 cells)')

        for i in range(1, len(xv)):
            s.iat[i] = s.iat[i-1] + xv.iat[i] * v1.iat[i] - xv.iat[i-1] * v2.iat[i-1]
        
        # Cumulative Production
        self._cumulative = s

    # Getters
    # Get Integral of Viable Cells
    def get_ivcc(self):
        return self._ixv

    # Display
    def disp_inpro_data(self):
        self._inpro_data = pd.concat([self._ixv,
                                      self._cumulative],
                                      axis=1)
        print('\n************ Cell In Process Data ************')
        print(self._inpro_data)